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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeTo_TerminateApp_LifeCycle');
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
        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name,app_download_url)
        if status == "SUCCESS":
            thunder_port=rdkv_performancelib.devicePort
            event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'],"/jsonrpc",False)
            time.sleep(20)
            print("\n Terminating the app")
            tdkTestObj = obj.createTestStep('rdkv_terminate_app')
            tdkTestObj.addParameter("app_id", app_name)
            start_time = datetime.now(UTC).time()
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
                    print("Received all terminate events successfully")
                    tdkTestObj.setResultStatus("SUCCESS") 
                    terminate_start_time = datetime.strptime(str(start_time), "%H:%M:%S.%f")
                    time_paused_ms = (paused_time - terminate_start_time).total_seconds() * 1000
                    time_terminated_ms = (terminate_time - paused_time).total_seconds() * 1000
                    time_unload_ms = (unload_time - terminate_time).total_seconds() * 1000
                    time_total_ms = (unload_time - terminate_start_time).total_seconds() * 1000

                    print(f"Paused time (ms): {time_paused_ms:.2f}")
                    print(f"Terminated time (ms): {time_terminated_ms:.2f}")
                    print(f"Unload time (ms): {time_unload_ms:.2f}")
                    print(f"Total close time (ms): {time_total_ms:.2f}")

                    # Get threshold values from config file
                    conf_file,_ = getConfigFileName(obj.realpath)
                    config_status,terminate_threshold = getDeviceConfigKeyValue(conf_file,"APPMANAGER_TERMINATE_LIFECYCLE_THRESHOLD_VALUE")
                    config_status,terminate_offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                    
                    Summ_list.append('TERMINATE_LIFECYCLE_THRESHOLD_VALUE :{}ms'.format(terminate_threshold))
                    Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(terminate_offset))
                    Summ_list.append('App termination initiated at :{}'.format(start_time))
                    Summ_list.append('Time taken to pause app :{}ms'.format(time_paused_ms))
                    Summ_list.append('Time taken to terminate app :{}ms'.format(time_terminated_ms))
                    Summ_list.append('Time taken to unload app :{}ms'.format(time_unload_ms))

                    print("\n Validate the pause time:")
                    try:
                        if 0 < int(time_paused_ms) < (int(terminate_threshold) + int(terminate_offset)):
                            print(f"\n Pause time {time_paused_ms:.2f}ms is within the expected range")
                        else:
                            print(f"\n Pause time {time_paused_ms:.2f}ms is not within the expected range")
                            tdkTestObj.setResultStatus("FAILURE")
                    except Exception:
                        print("\n Error validating pause time due to invalid threshold/offset values")
                        tdkTestObj.setResultStatus("FAILURE")

                    print("\n Validate the terminate time:")
                    try:
                        if 0 < int(time_terminated_ms) < (int(terminate_threshold) + int(terminate_offset)):
                            print(f"\n Terminate time {time_terminated_ms:.2f}ms is within the expected range")
                        else:
                            print(f"\n Terminate time {time_terminated_ms:.2f}ms is not within the expected range")
                            tdkTestObj.setResultStatus("FAILURE")
                    except Exception:
                        print("\n Error validating terminate time due to invalid threshold/offset values")
                        tdkTestObj.setResultStatus("FAILURE")

                    print("\n Validate the unload time:")
                    try:
                        if 0 < int(time_unload_ms) < (int(terminate_threshold) + int(terminate_offset)):
                            print(f"\n Unload time {time_unload_ms:.2f}ms is within the expected range")
                        else:
                            print(f"\n Unload time {time_unload_ms:.2f}ms is not within the expected range")
                            tdkTestObj.setResultStatus("FAILURE")
                    except Exception:
                        print("\n Error validating total close time due to invalid threshold/offset values")
                        tdkTestObj.setResultStatus("FAILURE")
                    getSummary(Summ_list,obj)     
                else:
                    print("Failed to receive terminate event")
                    print([name for name, value in event_dict.items() if not value])
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("Unable to terminate the app")
            event_listener.disconnect()          
        else:
            print("Failed to Launch the app")
            obj.setLoadModuleStatus("FAILURE")
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")