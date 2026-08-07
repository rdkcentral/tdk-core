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

import tdklib
import time
import StabilityTestUtility
from StabilityTestUtility import *
import PerformanceTestVariables
from web_socket_util import *
import rdkv_performancelib
from datetime import datetime, UTC

# Test component
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeToResumeApp')

pre_requisite_reboot(obj,"no")

expectedResult = "SUCCESS"
status = "SUCCESS"
revert = "NO"

# Load module
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

if expectedResult in result.upper():

    status = "SUCCESS"

    # ---------------- Plugin Validation ----------------
    plugins_list = [
        "org.rdk.DownloadManager",
        "org.rdk.AppPackageManager",
        "org.rdk.AppManager"
    ]

    plugin_status_needed = {
        "org.rdk.DownloadManager":"activated",
        "org.rdk.AppPackageManager":"activated",
        "org.rdk.AppManager":"activated"
    }

    curr_plugins_status_dict = get_plugins_status(obj, plugins_list)

    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj, plugin_status_needed)
        time.sleep(10)

    if status == "SUCCESS":


        app_bundle_1 = PerformanceTestVariables.google_bundle
        app1_name = app_bundle_1.split('+')[0]
        app_bundle_2 = PerformanceTestVariables.keytest_bundle
        app2_name = app_bundle_2.split('+')[0]
        app_download_url = PerformanceTestVariables.app_download_url
        
        print("[INFO] Installing apps")
        rdkservice_install_launch_app(obj,app_bundle_1,app1_name,app_download_url,launch=False)
        rdkservice_install_launch_app(obj,app_bundle_2,app2_name,app_download_url,launch=False)

        # ---------------- Event Listener ----------------
        thunder_port = rdkv_performancelib.devicePort
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(3)

        # ---------------- Launch App A ----------------
        print(f"[INFO] Launching {app1_name}")

        tdkTestObj = obj.createTestStep('rdkservice_launch_app')
        tdkTestObj.addParameter("app_name", app1_name)
        tdkTestObj.executeTestCase(expectedResult)

        time.sleep(3)
        
        # Wait for lifecycle event with timeout (30 seconds)
        continue_count = 0
        active = False
        while continue_count < 30:
            if len(event_listener.getEventsBuffer()) > 0:
                event = event_listener.getEventsBuffer().pop(0)
                if app1_name in event and '"newState":"APP_STATE_ACTIVE"' in event:
                    print("[INFO] App A ACTIVE")
                    active = True
                    break
            time.sleep(1)
            continue_count += 1

        if not active:
            print("[ERROR] APP_STATE_ACTIVE event not received for App A (timeout after 30s)")
            status = "FAILURE"
            event_listener.disconnect()
        
        if status == "SUCCESS":

            # ---------------- Launch App B ----------------
            print(f"[INFO] Launching {app2_name}")

            tdkTestObj = obj.createTestStep('rdkservice_launch_app')
            tdkTestObj.addParameter("app_name", app2_name)
            tdkTestObj.executeTestCase(expectedResult)

            result = tdkTestObj.getResult()
            if result != "SUCCESS":
                print("[ERROR] Failed to launch App B")
                status = "FAILURE"
            
            if status == "SUCCESS":
                time.sleep(3)
                
                # Wait for background state with timeout
                continue_count = 0
                background = False
                while continue_count < 30:
                    if len(event_listener.getEventsBuffer()) > 0:
                        event = event_listener.getEventsBuffer().pop(0)
                        if app1_name in event and ('"newState":"APP_STATE_BACKGROUND"' in event or '"newState":"APP_STATE_SUSPENDED"' in event):
                            print("[INFO] App A moved to background")
                            background = True
                            break
                    time.sleep(1)
                    continue_count += 1

                if not background:
                    print("[ERROR] App A did not move to background (timeout after 30s)")
                    status = "FAILURE"

                if status == "SUCCESS":
                    time.sleep(2)

                    # Clear Buffer
                    event_listener.getEventsBuffer().clear()

                    # Launch App A again to resume it
                    print(f"\n[INFO] Resuming {app1_name}")

                    tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                    tdkTestObj.addParameter("app_name", app1_name)

                    start_time = datetime.now(UTC)

                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result != "SUCCESS":
                        print("[ERROR] Failed to resume App A")
                        status = "FAILURE"
                    
                    if status == "SUCCESS":
                        time.sleep(3)
                        
                        # Wait for ACTIVE state with timeout
                        continue_count = 0
                        resumed = False
                        event = ""
                        while continue_count < 30:
                            if len(event_listener.getEventsBuffer()) > 0:
                                event = event_listener.getEventsBuffer().pop(0)
                                if app1_name in event and '"newState":"APP_STATE_ACTIVE"' in event:
                                    resumed = True
                                    print("[INFO] App resumed successfully")
                                    break
                            time.sleep(1)
                            continue_count += 1

                        if resumed:
                            # Extract timestamp and calculate duration
                            try:
                                resume_time_str = str(event).split("$$$")[0]
                                end_dt = datetime.strptime(resume_time_str, "%H:%M:%S.%f")
                                
                                # Calculate time difference
                                time_taken = end_dt - start_time.time()
                                time_taken_ms = time_taken.total_seconds() * 1000 if hasattr(time_taken, 'total_seconds') else 0
                            except Exception as e:
                                print(f"[ERROR] Failed to parse time: {e}")
                                time_taken_ms = -1

                            if time_taken_ms > 0:
                                print(f"[INFO] Time taken to resume app: {time_taken_ms} ms")

                                # Get threshold
                                conf_file, _ = getConfigFileName(obj.realpath)
                                _, threshold = getDeviceConfigKeyValue(conf_file,"APPMANAGER_LAUNCH_THRESHOLD_VALUE")
                                _, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                if not threshold:
                                    threshold = "2000"

                                if not offset:
                                    offset = "10"

                                allowed_time = int(threshold) + int(offset)

                                print(f"[INFO] Threshold : {threshold} ms")
                                print(f"[INFO] Offset    : {offset} ms")
                                print(f"[INFO] Allowed   : {allowed_time} ms")

                                # Validation
                                if 0 < int(time_taken_ms) < allowed_time:
                                    print(f"[SUCCESS] Resume time within expected range")
                                    print(f"[SUCCESS] Measured: {time_taken_ms} ms | Allowed: {allowed_time} ms")
                                    status = "SUCCESS"
                                else:
                                    diff = int(time_taken_ms) - allowed_time
                                    print(f"[FAILURE] Resume time exceeded threshold")
                                    print(f"[FAILURE] Measured : {time_taken_ms} ms")
                                    print(f"[FAILURE] Allowed  : {allowed_time} ms")
                                    print(f"[FAILURE] Exceeded by: {diff} ms")
                                    status = "FAILURE"
                            else:
                                print("[ERROR] Invalid time measurement")
                                status = "FAILURE"
                        else:
                            print("[ERROR] App resume failed - ACTIVE state not received (timeout after 30s)")
                            status = "FAILURE"

        # Cleanup
        if status == "SUCCESS":
            print("\n[INFO] Cleaning up apps")

            for app in [app1_name, app2_name]:
                tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                tdkTestObj.addParameter("app_id", app)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    print(f"[SUCCESS] App {app} terminated successfully")
                else:
                    print(f"[ERROR] Unable to terminate app {app}")
                    status = "FAILURE"

        if event_listener:
            event_listener.disconnect()

        # CRITICAL: Report final status BEFORE unload
        if status == "SUCCESS":
            print("\n[SUCCESS] Resume time test passed")
        else:
            print("\n[FAILURE] Resume time test failed")
        
        obj.setLoadModuleStatus(status)
        
        # Revert plugin changes if needed
        if revert == "YES":
            set_plugins_status(obj, curr_plugins_status_dict)

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("[ERROR] Failed to load module")
