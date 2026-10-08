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

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import StabilityTestUtility
from StabilityTestUtility import *
import PerformanceTestVariables
from web_socket_util import *
import rdkv_performancelib
import StabilityTestVariables

obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_AppManager_Launch_Uninstall');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
pre_condition_status = check_device_state(obj)
if expectedResult in result.upper() and expectedResult in pre_condition_status:
    status = "SUCCESS"
    print("\nCheck the status of AppManagers in the device")
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.AppPackageManager":"activated","org.rdk.AppManager":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj, plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        event_payload = '{"jsonrpc": "2.0","id": 1,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppUninstalled", "id": "client.events.1" }}'
        event_listener = createEventListener(ip, rdkv_performancelib.devicePort, [event_payload], "/jsonrpc", False)
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_download_url = PerformanceTestVariables.app_download_url
        app_name= "com.rdkcentral.google"
        test_count = int(StabilityTestVariables.AppManager_test_count)
        for iteration in range(test_count):
            print("ITERATION :", iteration + 1)
            print("_________________")
            #App may have been auto-uninstalled by the previous iteration, so re-verify it each time
            status = rdkservice_install_launch_app(obj, app_bundle_name, app_name, app_download_url, launch=False)
            if status == "SUCCESS":
                print("Successfully installed or verified the test app")
                tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                tdkTestObj.addParameter("app_name", app_name)
                tdkTestObj.executeTestCase(expectedResult)
                status = tdkTestObj.getResult()
                if status == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                    time.sleep(10)
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.getLoadedApps")
                    tdkTestObj.executeTestCase(expectedResult)
                    status = tdkTestObj.getResult()
                    loaded_before_uninstall = tdkTestObj.getResultDetails()
                    if status == "SUCCESS":
                        loaded_before_text = str(loaded_before_uninstall)
                        if app_name in loaded_before_text and "APP_STATE_ACTIVE" in loaded_before_text:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"{app_name} is active before uninstall conflict test")
                            print("Attempting to uninstall the active app")
                            tdkTestObj = obj.createTestStep('rdkservice_uninstall_app')
                            tdkTestObj.addParameter("app_id", app_name)
                            tdkTestObj.executeTestCase(expectedResult)
                            uninstall_status = tdkTestObj.getResult()
                            uninstall_details = tdkTestObj.getResultDetails()
                            if uninstall_status != "SUCCESS":
                                getloaded_after_uninstall = rdkservice_get_loaded_apps()
                                if app_name in getloaded_after_uninstall :
                                    print("Uninstall was rejected safely; the active app record remains valid")
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print("Terminating the active app to allow uninstall")
                                    tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                                    tdkTestObj.addParameter("app_id",app_name)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    terminate_status = tdkTestObj.getResult()
                                    if terminate_status == "SUCCESS":
                                        time.sleep(5)
                                        print("Checking whether the app is automatically uninstalled after termination")
                                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                        tdkTestObj.addParameter("method", "org.rdk.AppManager.getInstalledApps")
                                        tdkTestObj.executeTestCase(expectedResult)
                                        status = tdkTestObj.getResult()
                                        installed_after_uninstall = tdkTestObj.getResultDetails()
                                        if status == "SUCCESS":
                                            installed_after_text = str(installed_after_uninstall)
                                            if app_name not in installed_after_text:
                                                print("The app was automatically uninstalled after termination")
                                                tdkTestObj.setResultStatus("SUCCESS")
                                            else:
                                                print("The app was not automatically uninstalled after termination")
                                                tdkTestObj.setResultStatus("FAILURE")
                                                break
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print("Failed to query installed apps after termination")
                                            break
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print("Failed to terminate the active app")
                                        break
                                else:
                                    print("Uninstall was not rejected safely; the active app record is inconsistent")
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            else:
                                print("Uninstall succeeded while the app was active, which is unexpected")
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print(f"{app_name} is not active before uninstall conflict test")
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("Failed to query loaded apps after launching the app")
                        break
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"Failed to launch {app_name}")
                    break
            else:
                print("Failed to install or verify the test app")
                break
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Required AppManager plugins are not active")
    obj.unloadModule("rdkv_stability")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module or device precondition")