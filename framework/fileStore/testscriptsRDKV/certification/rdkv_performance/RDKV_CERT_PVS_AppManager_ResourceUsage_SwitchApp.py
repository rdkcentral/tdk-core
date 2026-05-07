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

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_ResourceUsage_SwitchApp')

# Pre-requisite reboot
pre_requisite_reboot(obj,"yes")

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"

if expectedResult in result.upper():

    status = "SUCCESS"

    print("\nCheck the status of AppManagers in the device")

    plugins_list = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager"]
    plugin_status_needed = {
        "org.rdk.DownloadManager":"activated",
        "org.rdk.PackageManagerRDKEMS":"activated",
        "org.rdk.AppManager":"activated"
    }

    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)

    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)

    if status == "SUCCESS":

        # ------------------- App Details -------------------       
        app_bundle_1 = PerformanceTestVariables.google_bundle
        app1_name = app_bundle_1.split('+')[0]
        app_bundle_2 = PerformanceTestVariables.keytest_bundle
        app2_name = app_bundle_2.split('+')[0]

        app_download_url = PerformanceTestVariables.app_download_url

        # ------------------- Install Apps -------------------
        print("\nInstalling Google App")
        status = rdkservice_install_launch_app(obj, app_bundle_1, app1_name, app_download_url, launch=False)

        if status == "SUCCESS":
            print("Google app installed successfully")

            print("\nInstalling KeyTest App")
            status = rdkservice_install_launch_app(obj, app_bundle_2, app2_name, app_download_url, launch=False)

        if status != "SUCCESS":
            print("App installation failed")
            obj.setLoadModuleStatus("FAILURE")

        else:

            # ------------------- Launch App1 -------------------
            print(f"\nLaunching {app1_name}")

            tdkTestObj = obj.createTestStep('rdkservice_launch_app')
            tdkTestObj.addParameter("app_name", app1_name)
            tdkTestObj.executeTestCase(expectedResult)

            if tdkTestObj.getResult() == "SUCCESS":
                print("App1 launched successfully")
                time.sleep(10)

                print("\n[App1 Foreground] Resource Usage")
                tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                tdkTestObj.executeTestCase(expectedResult)
                print(tdkTestObj.getResultDetails())
                tdkTestObj.setResultStatus("SUCCESS")

                # ------------------- Switch to App2 -------------------
                print(f"\nSwitching to {app2_name}")

                tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                tdkTestObj.addParameter("app_name", app2_name)
                tdkTestObj.executeTestCase(expectedResult)

                if tdkTestObj.getResult() == "SUCCESS":
                    print("App2 launched (App1 moved to background)")
                    time.sleep(10)

                    print("\n[App2 Foreground / App1 Background] Resource Usage")
                    tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                    tdkTestObj.executeTestCase(expectedResult)
                    print(tdkTestObj.getResultDetails())
                    tdkTestObj.setResultStatus("SUCCESS")
                    # ------------------- Switch back to App1 -------------------
                    print(f"\nSwitching back to {app1_name}")

                    tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                    tdkTestObj.addParameter("app_name", app1_name)
                    tdkTestObj.executeTestCase(expectedResult)

                    if tdkTestObj.getResult() == "SUCCESS":
                        print("App1 resumed to foreground")
                        time.sleep(10)

                        print("\n[App1 Foreground Again] Resource Usage")
                        tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                        tdkTestObj.executeTestCase(expectedResult)
                        print(tdkTestObj.getResultDetails())
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("Failed to relaunch App1")
                        tdkTestObj.setResultStatus("FAILURE")

                    # ------------------- Cleanup -------------------
                    print("\nCleaning up apps")

                    for app in [app1_name, app2_name]:
                        tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                        tdkTestObj.addParameter("app_id", app)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if result == "SUCCESS":
                            print("App Terminated Successfully")
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print("Failed to terminate app")
                            obj.setTestResult("FAILURE")
                else:
                    print("Failed to launch App2")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("Failed to launch App1")
                tdkTestObj.setResultStatus("FAILURE")

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
