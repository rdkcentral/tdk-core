##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2026 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

import tdklib
from StabilityTestUtility import *
from rdkv_performancelib import *
import time
import os

# ============================================================
# INITIALIZATION
# ============================================================
obj = tdklib.TDKScriptingLibrary("rdkv_performance", "1", standAlone=True)
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip, port, 'RDKV_CERT_PVS_AppManager_ResourceUsage_LowMemory')
pre_requisite_reboot(obj, "no")

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  : %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"

if expectedResult in result.upper():

    print("\n Check Pre conditions\n")

    final_status = "SUCCESS"
    
    app_download_url = PerformanceTestVariables.app_download_url
    print("\napp_download_url", app_download_url)
    app_bundle_name = PerformanceTestVariables.app_bundle_name
    print(f"\nApp bundle name: {app_bundle_name}")
    app_name = app_bundle_name.split("+")[0]
    print(f"\nApp name: {app_name}")

    memory_stress_process = None
    
    # ========================================================
    # CREATE LOW MEMORY CONDITION
    # ========================================================
    print("\nCreating low memory condition...\n")

    try:
        # Simulate memory usage (allocate large memory block)
        memory_stress_process = os.popen("stress --vm 1 --vm-bytes 70% --timeout 60")
        print("Memory stress started")
        time.sleep(5)
    except Exception as e:
        print("Failed to create memory stress:", str(e))
        final_status = "FAILURE"

    # ========================================================
    # INSTALL + LAUNCH APP
    # ========================================================
    if final_status == "SUCCESS":

        print("\nInstalling and launching app under low memory...\n")

        status = rdkservice_install_launch_app(obj, app_id, app_id, app_download_url)

        if status != "SUCCESS":
            print("App install/launch failed under low memory")            
            tdkTestObj.setResultStatus("FAILURE")
        else:
            print("\nWaiting before validation...\n")
            time.sleep(15)

            print("\nValidating Resource Usage under low memory...\n")

            tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
            tdkTestObj.executeTestCase(expectedResult)

            result = tdkTestObj.getResult()
            resource_usage = tdkTestObj.getResultDetails()

            if expectedResult in result and resource_usage != "ERROR":
                print("\nResource usage validated successfully under low memory\n")

            else:
                print("\nResource usage validation failed under low memory\n")
                tdkTestObj.setResultStatus("FAILURE")

            print("\nTerminating app...\n")
            tdkTestObj = obj.createTestStep('rdkservice_terminateApp')
            tdkTestObj.addParameter("app_id", app_id)
            tdkTestObj.executeTestCase(expectedResult)

            if tdkTestObj.getResult() == "SUCCESS":
                print("App terminated successfully")
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("App termination failed")
                tdkTestObj.setResultStatus("FAILURE")

            # ========================================================
            # CLEANUP MEMORY STRESS
            # ========================================================
            print("\nCleaning up memory stress...\n")

            try:
                os.system("killall stress")
                print("Memory stress stopped")
            except Exception as e:
                print("Failed to stop memory stress:", str(e))

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
