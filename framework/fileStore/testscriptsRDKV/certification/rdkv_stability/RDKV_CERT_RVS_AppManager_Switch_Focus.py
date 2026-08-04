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
import StabilityTestVariables
from web_socket_util import *
import rdkv_performancelib
from datetime import datetime, UTC

obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_AppManager_Switch_Focus');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
Summ_list=[]
if expectedResult in result.upper():
    status ="SUCCESS"
    print("\nCheck the status of AppManagers in the device")
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager", "org.rdk.RDKWindowManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.AppPackageManager":"activated","org.rdk.AppManager":"activated", "org.rdk.RDKWindowManager":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        test_count = StabilityTestVariables.AppManager_test_count
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_download_url = PerformanceTestVariables.app_download_url
        app_name_1 = "com.rdkcentral.testapp1"
        app_name_2 = "com.rdkcentral.testapp2"
        status_1 = rdkservice_install_launch_app(obj, app_bundle_name, app_name_1,app_download_url)
        print(status_1)
        time.sleep(5)
        status_2 = rdkservice_install_launch_app(obj, app_bundle_name, app_name_2,app_download_url)
        print(status_2)
        if status_1 == "SUCCESS" and status_2 == "SUCCESS":
            time.sleep(20)
            result = rdkservice_getValue("org.rdk.AppManager.getLoadedApps")
            app_instance_id_1 = app_instance_id_2 = ""
            if result != "EXCEPTION OCCURRED":
                for item in result:
                    if item.get("appId") == app_name_1 and item.get("lifecycleState") == "APP_STATE_ACTIVE":
                        app_instance_id_1 = item.get("appInstanceId", "")
                    elif item.get("appId") == app_name_2 and item.get("lifecycleState") == "APP_STATE_ACTIVE":
                        app_instance_id_2 = item.get("appInstanceId", "")    

                    if app_instance_id_1 and app_instance_id_2:
                        break   
            if not app_instance_id_1 or not app_instance_id_2:
                print("App instance id not received")
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.setResultStatus("FAILURE")
            else:
                time.sleep(5)
                continue_count = 0
                thunder_port=rdkv_performancelib.devicePort
                event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.RDKWindowManager.1.register","params": {"event": "onFocus", "id": "client.events.1" }}'],"/jsonrpc",False)
                time.sleep(10)
                for iteration in range(test_count):
                    event_listener.clearEventsBuffer()
                    event = ""
                    method = "org.rdk.RDKWindowManager.1.setFocus"
                    value = '{"client": "'+app_instance_id_1+'"}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method",method)
                    tdkTestObj.addParameter("value",value)
                    tdkTestObj.executeTestCase(expectedResult)
                    status = tdkTestObj.getResult()
                    if status == "SUCCESS":
                        focus_received = False
                        while True:
                            if continue_count > 120:
                                break
                            if len(event_listener.getEventsBuffer()) == 0:
                                time.sleep(1)
                                continue_count += 1
                                continue
                            event = event_listener.getEventsBuffer().pop(0)
                            if "onFocus" in str(event) and app_instance_id_1 in str(event):
                                print("\nEvent name:", event)
                                focus_received = True
                                break

                        if focus_received:
                            print("Received onFocus event successfully")
                            print(f"Successfully set focus for {app_name_1}")
                            tdkTestObj.setResultStatus("SUCCESS")

                            print(f"\nSetting focus of {app_name_2}")
                            event_listener.clearEventsBuffer()
                            event = ""
                            method = "org.rdk.RDKWindowManager.1.setFocus"
                            value = '{"client": "'+app_instance_id_2+'"}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method",method)
                            tdkTestObj.addParameter("value",value)
                            tdkTestObj.executeTestCase(expectedResult)
                            status = tdkTestObj.getResult()
                            if status == "SUCCESS":
                                focus_received = False
                                while True:
                                    if continue_count > 120:
                                        break
                                    if len(event_listener.getEventsBuffer()) == 0:
                                        time.sleep(1)
                                        continue_count += 1
                                        continue
                                    event = event_listener.getEventsBuffer().pop(0)
                                    if "onFocus" in str(event) and app_instance_id_2 in str(event):
                                        print("\nEvent name:", event)
                                        focus_received = True
                                        break
                                if focus_received:
                                    print("Received onFocus event successfully")
                                    print(f"Successfully set focus for {app_name_2}")
                                    tdkTestObj.setResultStatus("SUCCESS") 
                                else:
                                    print(f"Iteration {iteration+1}: Failed to receive onFocus event")
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            else:
                                print(f"Iteration {iteration+1}: Failed to Set Focus for {app_name_2}")
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print(f"Iteration {iteration+1}: Failed to receive onFocus event")
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print(f"Iteration {iteration+1}: Failed to Set Focus for {app_name_1}")
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                event_listener.disconnect()
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
            print("Failed to install the apps")
            obj.setLoadModuleStatus("FAILURE")
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")