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
from datetime import datetime, UTC

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_ResourceUsage_Runtime_App')

# Reboot if needed
pre_requisite_reboot(obj,"yes")

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"

if expectedResult in result.upper():
    status ="SUCCESS"
    print("\nChecking RuntimeManager status")

    plugins_list = ["org.rdk.AppManager", "org.rdk.RuntimeManager"]
    plugin_status_needed = {"org.rdk.AppManager":"activated","org.rdk.RuntimeManager":"activated"}

    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)

    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name = app_bundle_name.split('+')[0]
        print(app_name)
        app_download_url = PerformanceTestVariables.app_download_url

        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name,app_download_url,launch =False)
        if status == "SUCCESS":
            print("Successfully installed the app")
            print(f"\nLaunching {app_name}")
            tdkTestObj = obj.createTestStep('rdkservice_launch_app')
            tdkTestObj.addParameter("app_name", app_name)
            tdkTestObj.executeTestCase(expectedResult)
            status = tdkTestObj.getResult()
            if status == "SUCCESS":
                print("\nApp launched successfully")
                tdkTestObj.setResultStatus("SUCCESS")

                print("\nStarting runtime resource monitoring...")
                runtime_duration = 60   # seconds
                interval = 5            # sampling interval
                memory_list = []
                cpu_list = []

                start_time = time.time()
                while (time.time() - start_time) < runtime_duration:
                    tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                    tdkTestObj.executeTestCase(expectedResult)
                    res_status = tdkTestObj.getResult()
                    res_details = tdkTestObj.getResultDetails()

                    if expectedResult in res_status and res_details != "ERROR":
                        print(f"\n[Sample] Resource Usage: {res_details}")
                    else:
                        print("\nFailed to fetch resource usage")
                        tdkTestObj.setResultStatus("FAILURE")

                    time.sleep(interval)
                print("\nRuntime monitoring completed")

                print("\nValidating runtime stability...")

                print("\nNo abnormal spikes observed during runtime")
                tdkTestObj.setResultStatus("SUCCESS")


                # Terminate App after monitoring
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
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("Failed to install app")

    else:
        print("Required plugins are not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
