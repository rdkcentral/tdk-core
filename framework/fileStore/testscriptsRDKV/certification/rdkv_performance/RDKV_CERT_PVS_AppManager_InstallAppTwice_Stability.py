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

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_InstallAppTwice_Stability')

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
    plugin_status_needed = {"org.rdk.DownloadManager":"activated","org.rdk.PackageManagerRDKEMS":"activated","org.rdk.AppManager":"activated"}

    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)

    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)

    if status == "SUCCESS":

        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name = app_bundle_name.split('+')[0]
        print(app_name)
        app_download_url = PerformanceTestVariables.app_download_url

        # ------------------- First Install -------------------
        print("\nInstalling app (First time)")

        status = rdkservice_install_launch_app(obj,app_bundle_name,app_name,app_download_url,launch=False)

        if status == "SUCCESS":

            print("First install successful")

            # Resource usage after first install
            print("\n[First Install] Resource Usage")

            tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
            tdkTestObj.executeTestCase(expectedResult)

            if tdkTestObj.getResult() == "SUCCESS":
                print(tdkTestObj.getResultDetails())
                tdkTestObj.setResultStatus("SUCCESS")

                # ------------------- Re-Install -------------------
                print("\nInstalling app again (Second time)")
                status = rdkservice_install_launch_app(obj,app_bundle_name,app_name,app_download_url,launch=False)
                tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                tdkTestObj.addParameter("app_name", app_name)
                tdkTestObj.executeTestCase(expectedResult)
                if tdkTestObj.getResult() == "SUCCESS":
                    print("Second install completed successfully (reinstall)")
                    # Resource usage after second install
                    print("\n[Second Install] Resource Usage")

                    tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                    tdkTestObj.executeTestCase(expectedResult)
                    if tdkTestObj.getResult() == "SUCCESS":
                        print(tdkTestObj.getResultDetails())
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("Failed to fetch resource usage after second install")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("Second Launch was failed")


            else:
                print("Failed to fetch resource usage after first install")
                tdkTestObj.setResultStatus("FAILURE")
                status = "FAILURE"

            print("\nFinal cleanup: Uninstalling app")
            
            tdkTestObj = obj.createTestStep('rdkservice_uninstall_app')
            tdkTestObj.addParameter("app_id", app_name)
            tdkTestObj.executeTestCase(expectedResult)
            if tdkTestObj.getResult() == "SUCCESS":
                print("Cleanup successful")
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("Cleanup failed")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("Failed to Install the app")

    else:
        print("Required plugins are not active")
        obj.setLoadModuleStatus("FAILURE")

    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")


