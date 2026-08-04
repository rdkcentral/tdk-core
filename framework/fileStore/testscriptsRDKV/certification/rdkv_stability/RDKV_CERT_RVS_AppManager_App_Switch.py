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
import ast

obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_AppManager_App_Switch');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
rebootwaitTime = StabilityTestVariables.rebootwaitTime
#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

if expectedResult in (result.upper() and pre_condition_status):
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
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_download_url = PerformanceTestVariables.app_download_url
        app_name_1= "com.rdkcentral.testapp1"
        app_name_2= "com.rdkcentral.testapp2"

        print("\nRebooting the device ...")
        tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
        tdkTestObj.addParameter("waitTime",rebootwaitTime)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResultDetails()
        if expectedResult in result:
            print("Device rebooted successfully")
            tdkTestObj.setResultStatus("SUCCESS")
            print("\n Launching Test App 1 :")
            status = rdkservice_install_launch_app(obj, app_bundle_name, app_name_1,app_download_url)
            if status == "SUCCESS":
                print("Test App 1 launched successfully")
                print("\n Launching Test App 2 :")
                status = rdkservice_install_launch_app(obj, app_bundle_name, app_name_2,app_download_url)
                if status == "SUCCESS":
                    print("Test App 2 launched successfully")
                    print("Fetching app instance id ...")
                    result = rdkservice_getValue("org.rdk.AppManager.getLoadedApps")
                    app_instance_id_1 = app_instance_id_2 = ""
                    if result != "EXCEPTION OCCURRED":
                        for item in result:
                            if item.get("appId") == app_name_1 and item.get("lifecycleState") == "APP_STATE_ACTIVE":
                                app_instance_id_1= item.get("appInstanceId", "")
                            elif item.get("appId") == app_name_2 and item.get("lifecycleState") == "APP_STATE_ACTIVE":
                                app_instance_id_2= item.get("appInstanceId", "")   
                    if app_instance_id_1 and app_instance_id_2:
                        print(f"\nappInstanceId of Test_App_1 : {app_instance_id_1}")  
                        print(f"\nappInstanceId of Test_App_2 : {app_instance_id_2}")
                        print("\nFetching Zorder...")
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method", "org.rdk.RDKWindowManager.getZOrder")
                        tdkTestObj.addParameter("value", '{"clientId": "' + app_instance_id_1 + '"}')
                        tdkTestObj.executeTestCase(expectedResult)
                        status_1 = tdkTestObj.getResult()
                        result_1 = tdkTestObj.getResultDetails()
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method", "org.rdk.RDKWindowManager.getZOrder")
                        tdkTestObj.addParameter("value", '{"clientId": "' + app_instance_id_2 + '"}')
                        tdkTestObj.executeTestCase(expectedResult)
                        status_2 = tdkTestObj.getResult()
                        result_2 = tdkTestObj.getResultDetails()
                        if expectedResult in status_1 and expectedResult in status_2:
                            Zorder_App_1 = ast.literal_eval(result_1)
                            Zorder_App_2 = ast.literal_eval(result_2)
                            print(f"\nZorde of App 1: {Zorder_App_1}")
                            print(f"\nZorde of App 1: {Zorder_App_2}")
                            for iteration in range(test_count):
                                print(f"###################Iteration {iteration+1}###################")
                                print("Switching Zorder...")
                                Zorder_App_1,Zorder_App_2 = Zorder_App_2,Zorder_App_1
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.addParameter("method", "org.rdk.RDKWindowManager.setZOrder")
                                tdkTestObj.addParameter("value", '{"clientId": "' + app_instance_id_1 + '","zOrder": ' + str(Zorder_App_1) + '}')
                                tdkTestObj.executeTestCase(expectedResult)
                                status = tdkTestObj.getResult()
                                if expectedResult in status:
                                    print("\nFetching Zorder...")
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                    tdkTestObj.addParameter("method", "org.rdk.RDKWindowManager.getZOrder")
                                    tdkTestObj.addParameter("value", '{"clientId": "' + app_instance_id_1 + '"}')
                                    tdkTestObj.executeTestCase(expectedResult)
                                    status_1 = tdkTestObj.getResult()
                                    result_1 = tdkTestObj.getResultDetails()
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                    tdkTestObj.addParameter("method", "org.rdk.RDKWindowManager.getZOrder")
                                    tdkTestObj.addParameter("value", '{"clientId": "' + app_instance_id_2 + '"}')
                                    tdkTestObj.executeTestCase(expectedResult)
                                    status_2 = tdkTestObj.getResult()
                                    result_2 = tdkTestObj.getResultDetails()
                                    if expectedResult in status_1 and expectedResult in status_2:
                                        Get_Zorder_App_1 = ast.literal_eval(result_1)
                                        Get_Zorder_App_2 = ast.literal_eval(result_2)
                                        print(f"Zorder of Test APP 1: {Get_Zorder_App_1}")
                                        print(f"Zorder of Test APP 2: {Get_Zorder_App_2}")
                                        if Get_Zorder_App_1 != Get_Zorder_App_2:
                                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                            tdkTestObj.addParameter("method", "org.rdk.RDKWindowManager.setZOrder")
                                            tdkTestObj.addParameter("value", '{"clientId": "' + app_instance_id_2 + '","zOrder": ' + str(Zorder_App_2) + '}')
                                            tdkTestObj.executeTestCase(expectedResult)
                                            status = tdkTestObj.getResult()
                                            if expectedResult in status:
                                                print("\nFetching Zorder...")
                                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                                tdkTestObj.addParameter("method", "org.rdk.RDKWindowManager.getZOrder")
                                                tdkTestObj.addParameter("value", '{"clientId": "' + app_instance_id_1 + '"}')
                                                tdkTestObj.executeTestCase(expectedResult)
                                                status_1 = tdkTestObj.getResult()
                                                result_1 = tdkTestObj.getResultDetails()
                                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                                tdkTestObj.addParameter("method", "org.rdk.RDKWindowManager.getZOrder")
                                                tdkTestObj.addParameter("value", '{"clientId": "' + app_instance_id_2 + '"}')
                                                tdkTestObj.executeTestCase(expectedResult)
                                                status_2 = tdkTestObj.getResult()
                                                result_2 = tdkTestObj.getResultDetails()
                                                if expectedResult in status_1 and expectedResult in status_2:
                                                    Get_Zorder_App_1 = ast.literal_eval(result_1)
                                                    Get_Zorder_App_2 = ast.literal_eval(result_2)
                                                    print(f"Zorder of Test APP 1: {Get_Zorder_App_1}")
                                                    print(f"Zorder of Test APP 2: {Get_Zorder_App_2}")
                                                    if Get_Zorder_App_2 != Get_Zorder_App_1:
                                                        print("App switching sucessfull")
                                                    else:
                                                        print(f"Iteration {iteration+1}: Zorder of both apps should not be same\n")
                                                        tdkTestObj.setResultStatus("FAILURE")  
                                                        break
                                                else:
                                                    print(f"Iteration {iteration+1}: Failed to get Zorder\n")
                                                    tdkTestObj.setResultStatus("FAILURE") 
                                                    break
                                            else:
                                                print(f"Iteration {iteration+1}: Failed to set Zorder\n")
                                                tdkTestObj.setResultStatus("FAILURE") 
                                                break
                                        else:
                                            print(f"Iteration {iteration+1}: Zorder of both apps should not be same\n")
                                            tdkTestObj.setResultStatus("FAILURE")  
                                            break 
                                    else:
                                        print(f"Iteration {iteration+1}: Failed to get Zorder\n")
                                        tdkTestObj.setResultStatus("FAILURE")       
                                        break   
                                else:
                                    print(f"Iteration {iteration+1}: Failed to set Zorder\n")
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                        else:
                            print("Failed to receive Zorder\n")
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print("App instance id of Test App 1 not received")
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.setResultStatus("FAILURE") 


                    print("\n Terminating the apps")
                    tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                    tdkTestObj.addParameter("app_id",app_name_1)
                    tdkTestObj.executeTestCase(expectedResult)
                    result1 = tdkTestObj.getResult()

                    tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                    tdkTestObj.addParameter("app_id",app_name_2)
                    tdkTestObj.executeTestCase(expectedResult)
                    result2 = tdkTestObj.getResult()

                    if result1 == "SUCCESS" and result2 == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                        print("Successfully terminated the apps")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("Unable to terminate the apps")                          
                else:
                    print("Failed to launch Test App 2")
                    tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("Failed to launch Test App 1")
                tdkTestObj.setResultStatus("SUCCESS")
        else:
            print("Failed to reboot the device")        
            obj.setLoadModuleStatus("FAILURE") 
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")


