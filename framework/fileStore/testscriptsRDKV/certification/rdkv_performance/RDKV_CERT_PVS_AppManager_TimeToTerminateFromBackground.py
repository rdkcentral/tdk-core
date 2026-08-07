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

# use tdklib library
import tdklib; 
import time
import json
import StabilityTestUtility
from StabilityTestUtility import *
import PerformanceTestVariables
from PerformanceTestVariables import *
from web_socket_util import *
import rdkv_performancelib
from rdkv_performancelib import rdkservice_install_launch_app
from datetime import datetime, UTC

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeToTerminateFromBackground')

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
Summ_list = []

if expectedResult in result.upper():

    status = "SUCCESS"
    revert = "NO"

    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated","org.rdk.AppPackageManager":"activated","org.rdk.AppManager":"activated"}

    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)

    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)

    if status == "SUCCESS":

        app_bundle_1 = PerformanceTestVariables.google_bundle
        app_A = app_bundle_1.split('+')[0]
        print("\napp_A")
        app_bundle_2 = PerformanceTestVariables.keytest_bundle
        app_B = app_bundle_2.split('+')[0]
        print("\napp_B")
        app_url = PerformanceTestVariables.app_download_url

        # Ensure apps installed
        rdkservice_install_launch_app(obj, app_bundle_1, app_A, app_url, launch=False)
        rdkservice_install_launch_app(obj, app_bundle_2, app_B, app_url, launch=False)

        thunder_port = rdkv_performancelib.devicePort

        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'],"/jsonrpc",False)

        time.sleep(3)

        #Step 1: Launch App A
        print("\nLaunching App A")
        tdkTestObj = obj.createTestStep('rdkservice_launch_app')
        tdkTestObj.addParameter("app_name", app_A)
        tdkTestObj.executeTestCase(expectedResult)

        # Wait ACTIVE with timeout
        timeout_count = 0
        app_a_active = False
        while timeout_count < 30:  # 30 second timeout
            if len(event_listener.getEventsBuffer()) == 0:
                time.sleep(1)
                timeout_count += 1
                continue
            event = event_listener.getEventsBuffer().pop(0)
            if app_A in event and ("ACTIVE" in event or "APP_STATE_ACTIVE" in event):
                print("App A ACTIVE")
                app_a_active = True
                break
            timeout_count += 1
        
        if not app_a_active:
            print("[FAILURE] Timeout waiting for App A to become ACTIVE")
            status = "FAILURE"

        time.sleep(10)

        #Step 2: Launch App B → A goes background
        print("\nLaunching App B")
        tdkTestObj = obj.createTestStep('rdkservice_launch_app')
        tdkTestObj.addParameter("app_name", app_B)
        tdkTestObj.executeTestCase(expectedResult)

        if status == "SUCCESS":
            background = False
            timeout_count = 0
            
            # Wait for App A to move to background with timeout
            while timeout_count < 30:  # 30 second timeout
                if len(event_listener.getEventsBuffer()) == 0:
                    time.sleep(1)
                    timeout_count += 1
                    continue
                event = event_listener.getEventsBuffer().pop(0)
                if app_A in event and ("BACKGROUND" in event or "SUSPENDED" in event or "APP_STATE_BACKGROUND" in event or "APP_STATE_SUSPENDED" in event):
                    print("App A moved to background")
                    background = True
                    break
                timeout_count += 1
            
            if not background:
                print("[FAILURE] Timeout waiting for App A to move to background")
                status = "FAILURE"
            else:
                # Clear old events before measurement
                event_listener.getEventsBuffer().clear()
                time.sleep(2)
                
                # Step 3: Terminate from background
                print("\nTerminating App A from background")
                
                start_time = datetime.now(UTC)  # Full datetime object, not .time()
                
                tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                tdkTestObj.addParameter("app_id", app_A)
                tdkTestObj.executeTestCase(expectedResult)
                terminate_result = tdkTestObj.getResult()
                
                if terminate_result == "SUCCESS":
                    # Wait for terminate/destroy event with timeout
                    timeout_count = 0
                    terminated = False
                    destroy_event = None
                    
                    while timeout_count < 30:  # 30 second timeout
                        if len(event_listener.getEventsBuffer()) == 0:
                            time.sleep(1)
                            timeout_count += 1
                            continue
                        
                        destroy_event = event_listener.getEventsBuffer().pop(0)
                        if app_A in destroy_event and ("DESTROYED" in destroy_event or "DESTROY" in destroy_event or "TERMINATED" in destroy_event):
                            print("\nTerminate event received:", destroy_event)
                            terminated = True
                            break
                        timeout_count += 1
                    
                    if terminated and destroy_event:
                        # Calculate time taken
                        try:
                            destroy_time_str = str(destroy_event).split("$$$")[0]
                            end_time = datetime.fromisoformat(destroy_time_str.replace('Z', '+00:00')) if 'T' in destroy_time_str else datetime.now(UTC)
                        except:
                            end_time = datetime.now(UTC)
                        
                        time_taken = end_time - start_time
                        time_taken_ms = time_taken.total_seconds() * 1000
                        
                        print("\nTime taken to terminate from background: {:.2f} ms".format(time_taken_ms))
                        
                        # Get threshold
                        conf_file, file_status = getConfigFileName(obj.realpath)
                        _, threshold = getDeviceConfigKeyValue(conf_file, "APPMANAGER_TERMINATE_THRESHOLD_VALUE")
                        _, offset = getDeviceConfigKeyValue(conf_file, "THRESHOLD_OFFSET")
                        
                        if not threshold:
                            threshold = "2000"
                        if not offset:
                            offset = "10"
                        
                        allowed_time = int(threshold) + int(offset)
                        print(f"\nThreshold : {threshold} ms")
                        print(f"Offset    : {offset} ms")
                        print(f"Allowed   : {allowed_time} ms")
                        
                        if 0 < time_taken_ms < allowed_time:
                            print("\n[SUCCESS] Terminate within expected range")
                            print(f"Measured: {time_taken_ms:.2f} ms | Allowed: {allowed_time} ms")
                            status = "SUCCESS"
                        else:
                            diff = time_taken_ms - allowed_time
                            print("\n[FAILURE] Terminate exceeded threshold")
                            print(f"Measured : {time_taken_ms:.2f} ms")
                            print(f"Allowed  : {allowed_time} ms")
                            print(f"Exceeded by: {diff:.2f} ms")
                            status = "FAILURE"
                        
                        Summ_list.append(f"Time taken : {time_taken_ms:.2f} ms")
                        Summ_list.append(f"Allowed time : {allowed_time} ms")
                        getSummary(Summ_list, obj)
                    else:
                        print("[FAILURE] Timeout waiting for terminate event")
                        status = "FAILURE"
                else:
                    print("[FAILURE] Terminate command failed")
                    status = "FAILURE"

        event_listener.disconnect()
    
    # Report final status - CRITICAL: must be called in all paths
    if status == "SUCCESS":
        print("\n[SUCCESS] Terminate from background test passed")
    else:
        print("\n[FAILURE] Terminate from background test failed")
    
    obj.setLoadModuleStatus(status)
    
    # Revert plugin status if changed
    if revert == "YES":
        print("Reverting plugin status before exiting")
        StabilityTestUtility.set_plugins_status(obj, curr_plugins_status_dict)
    
    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("[FAILURE] Failed to load module")
