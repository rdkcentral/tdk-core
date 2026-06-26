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
from datetime import datetime, UTC

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeTo_LaunchApp_LifeCycle');
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
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.PackageManagerRDKEMS":"activated","org.rdk.AppManager":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name = app_bundle_name.split("+")[0]
        app_download_url = PerformanceTestVariables.app_download_url

        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name,app_download_url,launch =False)
        if status == "SUCCESS":
            print("Successfully installed the app")
            print("Register for the launch event")
            thunder_port=rdkv_performancelib.devicePort
            event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'],"/jsonrpc",False)
            time.sleep(5)
            print(f"\nLaunching {app_name}")
            event_dict = {"APP_STATE_LOADING": False, "APP_STATE_INITIALIZING" : False, "APP_STATE_PAUSED" : False, "APP_STATE_ACTIVE":False}
            tdkTestObj = obj.createTestStep('rdkservice_launch_app')
            tdkTestObj.addParameter("app_name", app_name)
            start_time = datetime.now(UTC).time()
            print(f"Start time - {start_time}")
            tdkTestObj.executeTestCase(expectedResult)
            status = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails()
            if status == "SUCCESS":
                print("Check for all events")
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
                        if "\"newState\":\"APP_STATE_LOADING\"" in event:
                            print("Received APP_STATE_LOADING event")
                            event_dict["APP_STATE_LOADING"] = True
                            Load_time = datetime.strptime(str(event).split("$$$")[0], "%H:%M:%S.%f")
                            print(f"App loading time: {Load_time} seconds\n")
                        if "\"newState\":\"APP_STATE_INITIALIZING\"" in event:
                            print ("Received APP_STATE_INITIALIZING event")
                            Ini_time = datetime.strptime(str(event).split("$$$")[0], "%H:%M:%S.%f")
                            print(f"App initialization time: {Ini_time} seconds\n")
                            event_dict["APP_STATE_INITIALIZING"] = True
                        if "\"newState\":\"APP_STATE_PAUSED\"" in event:
                            print("Received APP_STATE_PAUSED event")
                            Paused_time = datetime.strptime(str(event).split("$$$")[0], "%H:%M:%S.%f")
                            print(f"App paused time: {Paused_time} seconds\n")
                            event_dict["APP_STATE_PAUSED"] = True
                        if "\"newState\":\"APP_STATE_ACTIVE\"" in event:
                            print("Received APP_STATE_ACTIVE event")
                            Active_time = datetime.strptime(str(event).split("$$$")[0], "%H:%M:%S.%f")
                            print(f"App active time: {Active_time} seconds\n")
                            event_dict["APP_STATE_ACTIVE"] = True
                            break   
                if all(event_dict.values()):
                    try:
                        print("Received all launch events successfully")
                        tdkTestObj.setResultStatus("SUCCESS")  
                        launch_start_time = datetime.strptime(str(start_time), "%H:%M:%S.%f") 
                        time_load_ms = (Load_time - launch_start_time).total_seconds() * 1000
                        time_init_ms = (Ini_time - Load_time).total_seconds() * 1000
                        time_paused_ms = (Paused_time - Ini_time).total_seconds() * 1000
                        time_active_ms = (Active_time - Paused_time).total_seconds() * 1000
                        time_total_ms = (Active_time - launch_start_time).total_seconds() * 1000

                        print(f"Load time (ms): {time_load_ms:.2f}")
                        print(f"Initialize time (ms): {time_init_ms:.2f}")
                        print(f"Paused transition time (ms): {time_paused_ms:.2f}")
                        print(f"Active transition time (ms): {time_active_ms:.2f}")
                        print(f"Total time to active (ms): {time_total_ms:.2f}")

                        # Get threshold values from config file
                        conf_file,file_status = getConfigFileName(obj.realpath)
                        config_status,launch_threshold = getDeviceConfigKeyValue(conf_file,"APPMANAGER_LAUNCH_EVENT_THRESHOLD_VALUE")
                        config_status,launch_offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                        
                        Summ_list.append('LAUNCH_THRESHOLD_VALUE :{}ms'.format(launch_threshold))
                        Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(launch_offset))
                        Summ_list.append('App launch initiated at :{}'.format(start_time))
                        Summ_list.append('Time taken to load app :{}ms'.format(time_load_ms))
                        Summ_list.append('Time taken to initialize app :{}ms'.format(time_init_ms))
                        Summ_list.append('Time taken to pause app :{}ms'.format(time_paused_ms))
                        Summ_list.append('Time taken for app to be active :{}ms'.format(time_active_ms))
                        Summ_list.append('Total time for app launch :{}ms'.format(time_total_ms))

                        print("\n Validate the load time:")
                        try:
                            if 0 < int(time_load_ms) < (int(launch_threshold) + int(launch_offset)):
                                print(f"\n Load time {time_load_ms:.2f}ms is within the expected range")
                            else:
                                print(f"\n Load time {time_load_ms:.2f}ms is not within the expected range")
                                tdkTestObj.setResultStatus("FAILURE")
                        except Exception:
                            print("\n Error validating load time due to invalid threshold/offset values")
                            tdkTestObj.setResultStatus("FAILURE")

                        print("\n Validate the initialization time:")
                        try:
                            if 0 < int(time_init_ms) < (int(launch_threshold) + int(launch_offset)):
                                print(f"\n Initialization time {time_init_ms:.2f}ms is within the expected range")
                            else:
                                print(f"\n Initialization time {time_init_ms:.2f}ms is not within the expected range")
                                tdkTestObj.setResultStatus("FAILURE")
                        except Exception:
                            print("\n Error validating initialization time due to invalid threshold/offset values")
                            tdkTestObj.setResultStatus("FAILURE")

                        print("\n Validate the pause time:")
                        try:
                            if 0 < int(time_paused_ms) < (int(launch_threshold) + int(launch_offset)):
                                print(f"\n Pause time {time_paused_ms:.2f}ms is within the expected range")
                            else:
                                print(f"\n Pause time {time_paused_ms:.2f}ms is not within the expected range")
                                tdkTestObj.setResultStatus("FAILURE")
                        except Exception:
                            print("\n Error validating Pause time due to invalid threshold/offset values")
                            tdkTestObj.setResultStatus("FAILURE")

                        print("\n Validate the Active time:")
                        try:
                            if 0 < int(time_active_ms) < (int(launch_threshold) + int(launch_offset)):
                                print(f"\n Active time {time_active_ms:.2f}ms is within the expected range")
                            else:
                                print(f"\n Active time {time_active_ms:.2f}ms is not within the expected range")
                                tdkTestObj.setResultStatus("FAILURE")
                        except Exception:
                            print("\n Error validating Active time due to invalid threshold/offset values")
                            tdkTestObj.setResultStatus("FAILURE")    
                        
                        getSummary(Summ_list,obj)
                    finally:
                        try:
                            event_listener.disconnect()
                        except Exception as e:
                            print(f"Error disconnecting event listener: {e}")
                else:
                    print("Failed to receive launch event")
                    print([name for name, value in event_dict.items() if not value])
                    tdkTestObj.setResultStatus("FAILURE")
                    try:
                        event_listener.disconnect()
                    except Exception as e:
                        print(f"Error disconnecting event listener: {e}")

  
                print("\n Terminating the app")
                tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                tdkTestObj.addParameter("app_id",app_name)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    print("Successfully terminated the app")
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("Unable to terminate the app")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("Unable to launch the app")
        else:
            print("Failed to install the app")
            obj.setLoadModuleStatus("FAILURE")
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")