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
import tdklib; 
import time
import StabilityTestUtility
from StabilityTestUtility import *
import PerformanceTestVariables
import rdkv_performancelib
import StabilityTestVariables

obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_AppManager_ClearAllAppData_Launch');

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
        test_count = int(StabilityTestVariables.AppManager_test_count)
        app_bundle_list = StabilityTestVariables.appmanager_test_apps
        app_download_url = PerformanceTestVariables.app_download_url
        if len(app_bundle_list) < 2:
            print("Configure at least two app bundles in StabilityTestVariables.appmanager_test_apps")
            obj.setLoadModuleStatus("FAILURE")
        else:
            app_name_list = []
            install_status = "SUCCESS"
            for app_bundle in app_bundle_list:
                app_name = app_bundle.split("+")[0]
                app_name_list.append(app_name)
                install_status = rdkservice_install_launch_app(obj, app_bundle, app_name, app_download_url, launch=False)
                if install_status != "SUCCESS":
                    print(f"Failed to install {app_name}")
                    break
            if install_status == "SUCCESS":
                print("Successfully installed all configured apps")
                print("App set under test :", app_name_list)
                for i in range(test_count):
                    print("ITERATION :", i+1)
                    print("_________________")
                    print("Getting installed apps before clearing data")
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.getInstalledApps")
                    tdkTestObj.executeTestCase(expectedResult)
                    status = tdkTestObj.getResult()
                    installed_apps_before = tdkTestObj.getResultDetails()
                    print("installed_apps_before:", installed_apps_before)
                    missing_apps = [name for name in app_name_list if name not in str(installed_apps_before)]
                    if status == "SUCCESS" and not missing_apps:
                        print("All apps are installed before clearing data")
                        tdkTestObj.setResultStatus("SUCCESS")
                        print("installed_apps_before:", installed_apps_before)
                        print("\nClearing data for all apps")
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method", "org.rdk.AppManager.clearAllAppData")
                        tdkTestObj.addParameter("value", '{}')
                        tdkTestObj.executeTestCase(expectedResult)
                        status = tdkTestObj.getResult()
                        details = tdkTestObj.getResultDetails()
                        if status == "SUCCESS":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print("Successfully cleared all app data")
                            print("\nVerifying the installed package set is unchanged")
                            tdkTestObj = obj.createTestStep('rdkservice_getValue')
                            tdkTestObj.addParameter("method", "org.rdk.AppManager.getInstalledApps")
                            tdkTestObj.executeTestCase(expectedResult)
                            status = tdkTestObj.getResult()
                            installed_apps = tdkTestObj.getResultDetails()

                            print("installed_apps:", installed_apps)
                            missing_apps = [name for name in app_name_list if name not in str(installed_apps)]
                            if status == "SUCCESS" and not missing_apps:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print("All apps remain installed after clearAllAppData")
                                print("\nVerifying each app is still launchable")
                                launch_status = True
                                for app_name in app_name_list:
                                    print(f"\nLaunching {app_name}")
                                    tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                                    tdkTestObj.addParameter("app_name", app_name)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    status = tdkTestObj.getResult()
                                    details = tdkTestObj.getResultDetails()
                                    if status == "SUCCESS":
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        time.sleep(10)
                                        loaded_apps = rdkservice_get_loaded_apps()
                                        print(loaded_apps)
                                        if app_name in loaded_apps:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"{app_name} is in the list of loaded apps")
                                            print(f"Successfully launched {app_name}")
                                            print(f"Terminating {app_name}")
                                            tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                                            tdkTestObj.addParameter("app_id", app_name)
                                            tdkTestObj.executeTestCase(expectedResult)
                                            result = tdkTestObj.getResult()
                                            if result == "SUCCESS":
                                                time.sleep(5)
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print(f"Successfully terminated {app_name}")
                                                print("\n Validating resource usage:")
                                                tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                                                tdkTestObj.executeTestCase(expectedResult)
                                                resource_usage = tdkTestObj.getResultDetails()
                                                result = tdkTestObj.getResult()
                                                if expectedResult in result and resource_usage != "ERROR":
                                                    print("\n Resource usage is within the expected limit")
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                else:
                                                    print(f"\nIteration {i+1} Error while validating resource usage")
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    launch_status = False
                                                    break
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(f"\nIteration {i+1}: Failed to terminate {app_name}")
                                                launch_status = False
                                                break
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"\nIteration {i+1}: {app_name} is not launchable after clearAllAppData")
                                            launch_status = False
                                            break
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"\nIteration {i+1}: Failed to launch {app_name}")
                                        launch_status = False
                                        break
                                if not launch_status:
                                    break
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"\nIteration {i+1}: Installed package set changed after clearAllAppData. Missing: {missing_apps}")
                                break
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"\nIteration {i+1}: Failed to clear all app data")
                            break
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"\nIteration {i+1}: Failed to get installed apps before clearAllAppData")
                        break
            else:
                print("Failed to install the required apps")
                obj.setLoadModuleStatus("FAILURE")
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
