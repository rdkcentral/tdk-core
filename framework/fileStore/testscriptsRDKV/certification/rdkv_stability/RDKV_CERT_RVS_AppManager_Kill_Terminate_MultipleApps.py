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
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_AppManager_Kill_Terminate_MultipleApps');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

if expectedResult in result.upper() and expectedResult in pre_condition_status:
    status ="SUCCESS"
    print("\nCheck the status of AppManagers in the device")
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.AppPackageManager":"activated","org.rdk.AppManager":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        test_count = StabilityTestVariables.AppManager_test_count
        app_bundle_list = StabilityTestVariables.appmanager_test_apps
        app_download_url = PerformanceTestVariables.app_download_url
        
        #Two distinct app bundles are required, one per app id under test
        if len(app_bundle_list) >= 2:
            app_name_1 = app_bundle_list[0].split("+")[0]
            app_name_2 = app_bundle_list[1].split("+")[0]
            app_ids = [app_name_1, app_name_2]
            status = rdkservice_install_launch_app(obj, app_bundle_list[0], app_name_1, app_download_url, launch=False)
            if status == "SUCCESS":
                print("Successfully installed {}".format(app_name_1))
                status = rdkservice_install_launch_app(obj, app_bundle_list[1], app_name_2,app_download_url,launch =False)
                if status == "SUCCESS":
                    print("Successfully installed {}".format(app_name_2))
                    lifecycle_sequence = [
                    ("launch", app_ids[0]),
                    ("launch", app_ids[1]),
                    ("kill", app_ids[0]),
                    ("kill", app_ids[1]),
                    ("launch", app_ids[0]),
                    ("launch", app_ids[1]),
                    ("terminate", app_ids[0]),
                    ("terminate", app_ids[1])
                    ]
                    test_count = StabilityTestVariables.AppManager_test_count
                    for iteration in range(test_count):
                        print("\n################################# Cycle %s #################################" % (iteration + 1))
                        for lifecycle_action, target_app_id in lifecycle_sequence:
                            print("%s %s" % (lifecycle_action, target_app_id))
                            if lifecycle_action == "launch":
                                tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                                tdkTestObj.addParameter("app_name", target_app_id)
                                print("Launching app: %s" % target_app_id)
                                tdkTestObj.executeTestCase(expectedResult)
                            elif lifecycle_action == "kill":
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.addParameter("method", "org.rdk.AppManager.killApp")
                                tdkTestObj.addParameter("value", '{"appId": "' + target_app_id + '"}')
                                print("Killing app: %s" % target_app_id)
                                tdkTestObj.executeTestCase(expectedResult)
                            else:
                                tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                                tdkTestObj.addParameter("app_id", target_app_id)
                                print("Terminating app: %s" % target_app_id)
                                tdkTestObj.executeTestCase(expectedResult)

                            status = tdkTestObj.getResult()
                            if status == "SUCCESS":
                                tdkTestObj.setResultStatus("SUCCESS")
                                print("App lifecycle action succeeded for app: %s" % target_app_id)
                                time.sleep(10)
                                loaded_app_ids = rdkservice_get_loaded_apps()
                                app_active = target_app_id in loaded_app_ids
                                if lifecycle_action == "launch":
                                    app_state_valid = app_active
                                    expected_state = "present with APP_STATE_ACTIVE state"
                                else:
                                    app_state_valid = not app_active
                                    expected_state = "absent"

                                if app_state_valid:
                                    print("getLoadedApps verified %s is %s after %s" % (target_app_id, expected_state, lifecycle_action))
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print("FAILURE: Expected %s to be %s in getLoadedApps after %s" % (target_app_id, expected_state, lifecycle_action))
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            else:
                                print("FAILURE : %s failed for %s" % (lifecycle_action, target_app_id))
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                else:
                    print("FAILURE: Failed to install {}".format(app_name_2))      
            else:
                print("FAILURE: Failed to install {}".format(app_name_1))        
        else:
            print("Configure at least two app bundles in StabilityTestVariables.appmanager_test_apps")
            obj.setLoadModuleStatus("FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Required AppManager plugins are not active")
    obj.unloadModule("rdkv_stability")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module or device precondition")