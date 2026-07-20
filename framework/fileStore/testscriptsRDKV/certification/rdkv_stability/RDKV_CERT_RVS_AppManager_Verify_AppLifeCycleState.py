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
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_AppManager_Verify_AppLifeCycleState');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

if expectedResult in (result.upper() and pre_condition_status):
    status ="SUCCESS"
    print("\nCheck the status of AppManagers in the device")
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.PackageManagerRDKEMS":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        test_count = StabilityTestVariables.AppManager_test_count
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name= "com.rdkcentral.css3"
        app_download_url = PerformanceTestVariables.app_download_url
        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name,app_download_url,launch =False)
        if status == "SUCCESS":
            print("Successfully installed the app")
            for iteration in range(test_count):
                time.sleep(1)
                print("ITERATION :", iteration+1)
                print("_________________")
                print(f"\nPreloading {app_name}")
                time.sleep(5)
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method", "org.rdk.AppManager.preloadApp")
                tdkTestObj.addParameter("value", '{"appId": "' + app_name + '"}')
                tdkTestObj.executeTestCase(expectedResult)
                status = tdkTestObj.getResult()
                result = tdkTestObj.getResultDetails()
                if not result:
                    time.sleep(10)
                    STATE_FLAG = False
                    result = rdkservice_getValue("org.rdk.AppManager.getLoadedApps")
                    print(f"Preload Result {result}")
                    if result != "EXCEPTION OCCURRED":
                        for item in result:
                            if item.get("appId") == app_name and item.get("lifecycleState") == item.get("targetLifecycleState"):
                                print(f"TargetLifecycle: {item.get("targetLifecycleState")}")
                                print(f"LifecycleChange: {item.get("lifecycleState")}")
                                STATE_FLAG = True
                                break
                    if STATE_FLAG :
                        tdkTestObj.setResultStatus("SUCCESS")
                        print("lifecycleState matches the targetLifecycleState")
                        print(f"\nLaunching {app_name}")
                        time.sleep(3)
                        tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                        tdkTestObj.addParameter("app_name", app_name)
                        tdkTestObj.executeTestCase(expectedResult)
                        status = tdkTestObj.getResult()
                        details = tdkTestObj.getResultDetails()    
                        if status == "SUCCESS":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print("Check if the app is launched")
                            time.sleep(20)
                            STATE_FLAG = False
                            result = rdkservice_getValue("org.rdk.AppManager.getLoadedApps")
                            if result != "EXCEPTION OCCURRED":
                                for item in result:
                                    if item.get("appId") == app_name and item.get("lifecycleState") == item.get("targetLifecycleState"):
                                        print(f"TargetLifecycle: {item.get("targetLifecycleState")}")
                                        print(f"LifecycleChange: {item.get("lifecycleState")}")
                                        STATE_FLAG = True
                                        break
                            if STATE_FLAG :
                                tdkTestObj.setResultStatus("SUCCESS")
                                print("lifecycleState matches the targetLifecycleState")
                                print("Successfully launched the app")
                                time.sleep(10)
                                print("Closing the app")
                                param = '{"appId": "' + app_name + '"}'
                                tdkTestObj = obj.createTestStep('rdkservice_close_app')
                                tdkTestObj.addParameter("app_id",app_name)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                if result == "SUCCESS":
                                    time.sleep(10)
                                    STATE_FLAG = False
                                    result = rdkservice_getValue("org.rdk.AppManager.getLoadedApps")
                                    if result != "EXCEPTION OCCURRED":
                                        for item in result:
                                            if item.get("appId") == app_name and item.get("lifecycleState") == item.get("targetLifecycleState"):
                                                print(f"TargetLifecycle: {item.get("targetLifecycleState")}")
                                                print(f"LifecycleChange: {item.get("lifecycleState")}")
                                                STATE_FLAG = True
                                                break
                                    if STATE_FLAG :
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print("lifecycleState matches the targetLifecycleState")
                                        print("\n Validating resource usage:")
                                        tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                                        tdkTestObj.executeTestCase(expectedResult)
                                        resource_usage = tdkTestObj.getResultDetails()
                                        result = tdkTestObj.getResult()
                                        if expectedResult in result and resource_usage != "ERROR":
                                            print("\n Resource usage is within the expected limit")
                                            tdkTestObj.setResultStatus("SUCCESS")
                                        else:
                                            print(f"Iteration {iteration+1}: Error while validating resource usage")
                                            tdkTestObj.setResultStatus("FAILURE")
                                            break
                                        tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                                        tdkTestObj.addParameter("app_id", app_name)
                                        tdkTestObj.executeTestCase(expectedResult)
                                        status = tdkTestObj.getResult()
                                        details = tdkTestObj.getResultDetails()
                                        if status == "SUCCESS": 
                                            print("App terminated successfully")
                                            tdkTestObj.setResultStatus("SUCCESS")
                                        else:
                                            print(f"Iteration {iteration+1}: Failed to terminate app")
                                            tdkTestObj.setResultStatus("FAILURE")       
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE") 
                                        print(f"Iteration {iteration+1}: lifecycleState does not matches the targetLifecycleState")  
                                        break                            
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"Iteration {iteration+1}: Failed to close {app_name}")
                                    break
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"Iteration {iteration+1}: lifecycleState does not matches the targetLifecycleState")
                                break
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"Iteration {iteration+1}: Failed to launch {app_name}")
                            break
                    else:
                        print(f"Iteration {iteration+1}: lifecycleState does not matches the targetLifecycleState")

                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"Iteration {iteration+1}: Failed to preload {app_name}")
                    break
        else:
            print("Failed to install the app")
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
