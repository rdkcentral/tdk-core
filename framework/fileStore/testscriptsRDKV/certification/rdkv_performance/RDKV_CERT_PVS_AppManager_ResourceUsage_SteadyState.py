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
import time
import StabilityTestUtility
from StabilityTestUtility import *
import PerformanceTestVariables
import rdkv_performancelib

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

# Device details
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_ResourceUsage_SteadyState')

# Reboot for clean state
pre_requisite_reboot(obj,"yes")

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"

if expectedResult in result.upper():
    status = "SUCCESS"

    print("\nChecking AppManager plugins status")

    plugins_list = ["org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.AppManager":"activated"}

    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)

    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name = app_bundle_name.split('+')[0]
        print(app_name)
        app_download_url = PerformanceTestVariables.app_download_url

        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name,app_download_url,launch =True)
        if status == "SUCCESS":
            print("\nApp installation and launch was successfull")
            # í¿¢ Important step: Wait for steady state
            print("\nWaiting for app to reach steady state...")
            time.sleep(20)   # allow CPU/memory to stabilize

            print("\nValidating resource usage in steady state...")
            tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
            tdkTestObj.executeTestCase(expectedResult)
            res_status = tdkTestObj.getResult()
            res_details = tdkTestObj.getResultDetails()

            if expectedResult in res_status and res_details != "ERROR":
                print(f"\n[STEADY STATE] Resource Usage: {res_details}")
                print("\nResource usage is stable in steady state")
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("\nFailed to validate steady state resource usage")
                tdkTestObj.setResultStatus("FAILURE")

            # Terminate app after validation
            print(f"\nTerminating app: {app_name}")

            tdkTestObj = obj.createTestStep('rdkv_terminate_app')
            tdkTestObj.addParameter("app_id", app_name)
            tdkTestObj.executeTestCase(expectedResult)

            if tdkTestObj.getResult() == "SUCCESS":
                print("App terminated successfully")
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("Failed to terminate app")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("Failed to launch app")

    else:
        print("AppManager is not active")
        obj.setLoadModuleStatus("FAILURE")

    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
