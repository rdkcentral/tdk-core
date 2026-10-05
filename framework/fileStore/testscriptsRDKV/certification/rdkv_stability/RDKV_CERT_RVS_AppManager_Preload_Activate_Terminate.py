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
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_AppManager_PreloadApp_Activate_Terminate');

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
    status = "SUCCESS"
    print("\nCheck the status of AppManagers in the device")
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager", "org.rdk.RDKWindowManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.AppPackageManager":"activated","org.rdk.AppManager":"activated", "org.rdk.RDKWindowManager":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        test_count = int(StabilityTestVariables.AppManager_test_count)
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name = "com.rdkcentral.google"
        app_download_url = PerformanceTestVariables.app_download_url
        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name, app_download_url, launch=False)
        if status == "SUCCESS":
            print("Successfully installed the app")
            for i in range(test_count):
                print("ITERATION :", i+1)
                print("_________________")
                time.sleep(5)
                print(f"\nPreloading {app_name}")
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method", "org.rdk.AppManager.preloadApp")
                tdkTestObj.addParameter("value", '{"appId": "' + app_name + '"}')
                tdkTestObj.executeTestCase(expectedResult)
                status = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails()
                if status == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                    time.sleep(10)
                    print("Verifying preloaded state via getLoadedApps")
                    PRELOAD_FLAG = False
                    loaded_apps = rdkservice_getValue("org.rdk.AppManager.getLoadedApps")
                    print(f"Preload Result {loaded_apps}")
                    if loaded_apps != "EXCEPTION OCCURRED":
                        for item in loaded_apps:
                            if (item.get("appId") == app_name and item.get("lifecycleState") == "APP_STATE_PAUSED" and item.get("targetLifecycleState") == "APP_STATE_PAUSED"):
                                print(f"TargetLifecycle: {item.get('targetLifecycleState')}")
                                print(f"LifecycleState: {item.get('lifecycleState')}")
                                PRELOAD_FLAG = True
                                break
                    if PRELOAD_FLAG:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"{app_name} reached the preloaded state")
                        print(f"\nLaunching {app_name} to activate")
                        time.sleep(3)
                        tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                        tdkTestObj.addParameter("app_name", app_name)
                        tdkTestObj.executeTestCase(expectedResult)
                        status = tdkTestObj.getResult()
                        details = tdkTestObj.getResultDetails()
                        if status == "SUCCESS":
                            tdkTestObj.setResultStatus("SUCCESS")
                            time.sleep(20)
                            print("Verifying the app transitioned to active state")
                            ACTIVE_FLAG = False
                            loaded_apps = rdkservice_getValue("org.rdk.AppManager.getLoadedApps")
                            print(f"Launch Result {loaded_apps}")
                            if loaded_apps != "EXCEPTION OCCURRED":
                                for item in loaded_apps:
                                    if item.get("appId") == app_name and item.get("lifecycleState") == "APP_STATE_ACTIVE":
                                        print(f"LifecycleState: {item.get('lifecycleState')}")
                                        ACTIVE_FLAG = True
                                        break
                            if ACTIVE_FLAG:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"{app_name} successfully activated after preload")
                                print("\nTerminating the app")
                                tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                                tdkTestObj.addParameter("app_id", app_name)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                if result == "SUCCESS":
                                    time.sleep(5)
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print("Verifying no orphaned instance remains after terminate")
                                    running_apps = rdkservice_get_loaded_apps()
                                    print(running_apps)
                                    if app_name not in running_apps:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"Successfully verified {app_name} left no orphaned instance")
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
                                            break
                                    else:
                                        print(f"\nIteration {i+1}: {app_name} orphaned instance still listed in loaded apps after terminate")
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"\nIteration {i+1}: Failed to terminate {app_name}")
                                    break
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"\nIteration {i+1}: {app_name} did not reach APP_STATE_ACTIVE after launch")
                                break
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"\nIteration {i+1}: Failed to launch {app_name}")
                            break
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"\nIteration {i+1}: {app_name} did not reach the preloaded state")
                        break
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"\nIteration {i+1}: Failed to preload {app_name}")
                    break
        else:
            print("Failed to install the app")
            obj.setLoadModuleStatus("FAILURE")
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
