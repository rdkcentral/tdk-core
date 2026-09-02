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
from web_socket_util import *
import rdkv_performancelib
import StabilityTestVariables
from datetime import datetime

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_AppManager_KillApp_LifeCycle');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    status ="SUCCESS"
    print("\nCheck the status of AppManagers in the device")
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.AppPackageManager":"activated","org.rdk.AppManager":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name= "com.rdkcentral.google"
        app_download_url = PerformanceTestVariables.app_download_url
        test_count = StabilityTestVariables.AppManager_test_count
        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name,app_download_url,launch =False)
        if status == "SUCCESS":
            print("Successfully installed the app")
            print(f"\nLaunching {app_name}")
            thunder_port=rdkv_performancelib.devicePort
            event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'],"/jsonrpc",False)
            time.sleep(5)
            for i in range(4):
                print("ITERATION: ", i+1)
                event_listener.clearEventsBuffer()
                tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                tdkTestObj.addParameter("app_name", app_name)
                tdkTestObj.executeTestCase(expectedResult)
                status = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails()
                if status == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                    time.sleep(30)
                    print("Check if the app is launched")
                    loaded_apps = rdkservice_get_loaded_apps()
                    print(loaded_apps)
                    if app_name in loaded_apps:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print("Successfully launched the app")
                        print("\n Killing the app")
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method", "org.rdk.AppManager.killApp")
                        tdkTestObj.addParameter("value", '{"appId": "' + app_name + '"}')
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if result == "SUCCESS":
                            event_dict = {"APP_STATE_PAUSED" : False, "APP_STATE_TERMINATING" : False, "APP_STATE_UNLOADED" : False}
                            tdkTestObj.setResultStatus("SUCCESS")
                            continue_count = 0
                            while True:
                                if continue_count > 120:
                                    break
                                if len(event_listener.getEventsBuffer()) == 0:
                                    time.sleep(1)
                                    continue_count += 1
                                    continue
                                event = event_listener.getEventsBuffer().pop(0)
                                print("\nEvent:", event)
                                if app_name in event and "onAppLifecycleStateChanged" in str(event):
                                    if "\"newState\":\"APP_STATE_PAUSED\"" in event:
                                        print ("Received APP_STATE_PAUSED event")
                                        paused_time = datetime.strptime(str(event).split("$$$")[0], "%H:%M:%S.%f")
                                        event_dict["APP_STATE_PAUSED"] = True
                                    if "\"newState\":\"APP_STATE_TERMINATING\"" in event:
                                        print ("Received APP_STATE_TERMINATING event")
                                        terminate_time = datetime.strptime(str(event).split("$$$")[0], "%H:%M:%S.%f")
                                        event_dict["APP_STATE_TERMINATING"] = True
                                    if "\"newState\":\"APP_STATE_UNLOADED\"" in event:
                                        print ("Received APP_STATE_UNLOADED event")
                                        unload_time = datetime.strptime(str(event).split("$$$")[0], "%H:%M:%S.%f")
                                        event_dict["APP_STATE_UNLOADED"] = True
                                        break    
                            if all(event_dict.values()):
                                print("Received all Kill events successfully")
                                loaded_apps = rdkservice_get_loaded_apps()
                                print(loaded_apps)
                                if app_name not in loaded_apps:
                                    print(f"Successfully verified {app_name} was removed from loaded apps")
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print(f"\nIteration {i+1}: {app_name} is still listed in loaded apps after kill")
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            else:
                                print(f"\nIteration {i+1}: Failed to receive Kill event")
                                print([name for name, value in event_dict.items() if not value])
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"\nIteration {i+1}: Unable to terminate the app")
                            break
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"\nIteration {i+1}: App is not listed in loaded apps")
                        break
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"\nIteration {i+1}: Unable to launch the app")
                    break
            event_listener.disconnect()        
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("Failed to install the app")
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")