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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeTo_Kill_App');
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
        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name, app_download_url)
        if status == "SUCCESS":
            print("Successfully installed the app")
            print("Register for the kill event")
            thunder_port=rdkv_performancelib.devicePort
            event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'],"/jsonrpc",False)
            time.sleep(10)
            print(f"\nKilling {app_name}")
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method", "org.rdk.AppManager.killApp")
            tdkTestObj.addParameter("value", '{"appId": "' + app_name + '"}')
            start_time = datetime.now(UTC).time()
            tdkTestObj.executeTestCase(expectedResult)
            status = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails()
            if status == "SUCCESS":
                print("Successfully killed the app")
                tdkTestObj.setResultStatus("SUCCESS")
                continue_count = 0
                end_time = ""
                event = None
                unloaded_flag = False
                while True:
                    if continue_count > 120:
                        break
                    if len(event_listener.getEventsBuffer()) == 0:
                        time.sleep(1)
                        continue_count += 1
                        continue
                    event = event_listener.getEventsBuffer().pop(0)
                    print("\nEvent:", event)
                    if app_name in str(event) and "onAppLifecycleStateChanged" in str(event):
                        if "APP_STATE_UNLOADED" in str(event):
                            print("Received unload event")
                            tdkTestObj.setResultStatus("SUCCESS")
                            unloaded_flag = True
                            break   
                if unloaded_flag:
                    try:
                        print("Received unload event successfully")
                        tdkTestObj.setResultStatus("SUCCESS")
                        kill_time = str(event).split("$$$")[0]
                        kill_start_time = datetime.strptime(str(start_time), "%H:%M:%S.%f")
                        kill_end_time = datetime.strptime(str(kill_time), "%H:%M:%S.%f")
                        conf_file,file_status = getConfigFileName(obj.realpath)
                        config_status,kill_threshold = getDeviceConfigKeyValue(conf_file,"APPMANAGER_KILL_THRESHOLD_VALUE")
                        config_status,kill_offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                        Summ_list.append('APP_KILL_THRESHOLD_VALUE :{}ms'.format(kill_threshold))
                        Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(kill_offset))
                        Summ_list.append('App Kill initiated at :{}'.format(start_time))
                        Summ_list.append('App killed at :{}'.format(kill_time))
                        time_taken_for_kill = kill_end_time - kill_start_time
                        time_taken_for_kill = time_taken_for_kill.total_seconds() * 1000
                        print("\nKill initiated at ", start_time)
                        print("\n Kill completed at ", kill_time)
                        print("\n Time taken to kill the app : {}(ms)".format(time_taken_for_kill))
                        Summ_list.append('Time taken to kill app :{}ms'.format(time_taken_for_kill))
                        print("\n Threshold value for time taken to kill the app: {} ms".format(kill_threshold))
                        print("\n Validate the time:")
                        try:
                            if 0 < int(time_taken_for_kill) < (int(kill_threshold) + int(kill_offset)) :
                                print("\n Time taken for killing the app is within the expected range")
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print("\n Time taken for killing the app is not within the expected range")
                                tdkTestObj.setResultStatus("FAILURE")
                        except Exception:
                            print("\n Error validating time due to invalid threshold/offset values")
                            tdkTestObj.setResultStatus("FAILURE")
                        getSummary(Summ_list,obj)
                    finally:
                        # Ensure websocket listener is always disconnected to avoid leaking threads
                        try:
                            event_listener.disconnect()
                        except Exception as e:
                            print(f"Error disconnecting event listener: {e}")
                else:
                    print("Failed to receive unload event")
                    tdkTestObj.setResultStatus("FAILURE")
                    try:
                        event_listener.disconnect()
                    except Exception as e:
                        print(f"Error disconnecting event listener: {e}")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"\nFailed to kill {app_name}")
                # Ensure websocket listener is disconnected on failure path
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
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("Unable to terminate the app")

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