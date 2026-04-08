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
import json
import time

# ============================================================
# INITIALIZATION
# ============================================================
obj = tdklib.TDKScriptingLibrary("rdkv_performance", "1", standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip, port, 'RDKV_CERT_PVS_AppManager_ResourceUsage_AfterMultipleLaunch')
pre_requisite_reboot(obj, "no")

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  : %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"

if expectedResult in result.upper():

    print("\n Check Pre conditions\n")
    app_download_url = PerformanceTestVariables.app_download_url
    print("\napp_download_url", app_download_url)
    app_bundle_name = PerformanceTestVariables.app_bundle_name
    print(f"\nApp bundle name: {app_bundle_name}")
    app_name = app_bundle_name.split("+")[0]
    print(f"\nApp name: {app_name}")

    launch_count = 5
    print("\nEnsuring app is installed...\n")

    # ========================================================
    # INSTALL + LAUNCH APP (Ensure app exists)
    # ========================================================
    print("\nInstalling the app...\n")

    status = rdkservice_install_launch_app(obj, app_bundle_name, app_name,app_download_url, launch = False)

    if status != "SUCCESS":
        print("App installation was failed")
        tdkTestObj.setResultStatus("FAILURE")
    else:
        # ========================================================
        # MULTIPLE LAUNCHES
        # ========================================================
        print(f"\nPerforming {launch_count} consecutive launches...\n")
        for i in range(launch_count):
            print(f"\nIteration {i+1}/{launch_count}")
            tdkTestObj = obj.createTestStep('rdkservice_launchApp')
            tdkTestObj.addParameter("app_id", app_id)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()

            if result == "SUCCESS":
                print("Launch successful")
                tdkTestObj.setResultStatus("SUCCESS")
                # ========================================================
                # RESOURCE USAGE VALIDATION
                # ========================================================
                print("\nWaiting before validation...\n")
                time.sleep(20)

                print("\nValidating Resource Usage after multiple launches...\n")

                tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                tdkTestObj.executeTestCase(expectedResult)

                result = tdkTestObj.getResult()
                resource_usage = tdkTestObj.getResultDetails()
                if expectedResult in result and resource_usage != "ERROR":
                    print("\nResource usage validated successfully\n")
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print("\nResource usage validation failed\n")
                    tdkTestObj.setResultStatus("FAILURE")
                # ========================================================
                # TERMINATE APP
                # ========================================================
                print("\nTerminating App...\n")
                tdkTestObj = obj.createTestStep('rdkservice_terminateApp')
                tdkTestObj.addParameter("app_id", app_id)
                tdkTestObj.executeTestCase(expectedResult)
                if tdkTestObj.getResult() == "SUCCESS":
                    print("App terminated successfully")
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print("App termination failed")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("Launch failed")
                tdkTestObj.setResultStatus("FAILURE")
                break

            # Optional: short delay to simulate realistic usage
            time.sleep(3)


    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
