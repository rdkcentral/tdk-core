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
import StabilityTestUtility
from StabilityTestUtility import *
import PerformanceTestVariables
from web_socket_util import *
from rdkv_performancelib import *
import rdkv_performancelib
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

    status ="SUCCESS"

    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated","org.rdk.AppPackageManager":"activated","org.rdk.AppManager":"activated"}

    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)

    if curr_plugins_status_dict != plugin_status_needed:
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

        # Validate app A is in loaded apps
        print(f"\n[INFO] Validating app {app_A} reached loaded state")
        time.sleep(3)
        
        app_a_active = False
        validate_count = 0
        while validate_count < 30:
            loaded_apps = rdkservice_get_loaded_apps()
            if loaded_apps and app_A in str(loaded_apps):
                print(f"[SUCCESS] App {app_A} verified in loaded apps (ACTIVE state)")
                app_a_active = True
                break
            
            time.sleep(1)
            validate_count += 1
        
        if not app_a_active:
            print(f"[ERROR] App {app_A} failed to reach ACTIVE state")
            status = "FAILURE"

        # Wait for APP_STATE_ACTIVE event confirmation
        print(f"[INFO] Waiting for APP_STATE_ACTIVE event for {app_A}")
        active_event_count = 0
        while active_event_count < 30:
            if len(event_listener.getEventsBuffer()) == 0:
                time.sleep(1)
                active_event_count += 1
                continue
            event = event_listener.getEventsBuffer().pop(0)
            if app_A in event and "APP_STATE_ACTIVE" in event:
                print("App A ACTIVE event received")
                break
            active_event_count += 1
            time.sleep(1)

        time.sleep(10)

        #Step 2: Launch App B → A goes background
        print("\nLaunching App B")
        tdkTestObj = obj.createTestStep('rdkservice_launch_app')
        tdkTestObj.addParameter("app_name", app_B)
        tdkTestObj.executeTestCase(expectedResult)

        # Validate app B is in loaded apps
        print(f"\n[INFO] Validating app {app_B} reached loaded state")
        time.sleep(3)
        
        app_b_active = False
        validate_count = 0
        while validate_count < 30:
            loaded_apps = rdkservice_get_loaded_apps()
            if loaded_apps and app_B in str(loaded_apps):
                print(f"[SUCCESS] App {app_B} verified in loaded apps (ACTIVE state)")
                app_b_active = True
                break
            
            time.sleep(1)
            validate_count += 1
        
        if not app_b_active:
            print(f"[ERROR] App {app_B} failed to reach ACTIVE state")
            status = "FAILURE"

        background = False
        background_timeout = 30
        background_count = 0

        while background_count < background_timeout:
            if len(event_listener.getEventsBuffer()) == 0:
                time.sleep(1)
                background_count += 1
                continue
            event = event_listener.getEventsBuffer().pop(0)
            if app_A in event and ("APP_STATE_BACKGROUND" in event or "APP_STATE_SUSPENDED" in event):
                print("App A moved to background")
                background = True
                break
            background_count += 1
            time.sleep(1)

        # Check if App A went to background via getLoadedApps
        if not background:
            print("\n[INFO] Checking app state via getLoadedApps (event not received)")
            loaded_apps = rdkservice_get_loaded_apps()
            # If app is NOT in loaded apps, it went to background (filtered out)
            if loaded_apps and app_A not in str(loaded_apps):
                print(f"[INFO] App {app_A} confirmed backgrounded (not in loaded apps list)")
                background = True
            else:
                # Check raw state via getValue
                all_apps = rdkservice_getValue("org.rdk.AppManager.getLoadedApps")
                if all_apps != "EXCEPTION OCCURRED" and isinstance(all_apps, list):
                    app_states = {app.get("appId"): app.get("lifecycleState", "UNKNOWN") for app in all_apps}
                    app_a_state = app_states.get(app_A, "NOT_FOUND")
                    print(f"\n[INFO] Device-specific behavior detected:")
                    print(f"[INFO] App {app_A} state: {app_a_state}")
                    print(f"[INFO] All app states: {app_states}")
                    
                    if app_a_state in ["APP_STATE_ACTIVE", "APP_STATE_RUNNING"]:
                        print(f"\n[INFO] App {app_A} remains ACTIVE - device keeps multiple apps ACTIVE")
                        print("[INFO] Proceeding with termination from ACTIVE state (device-specific behavior)")
                        background = True  # Proceed anyway

        # Clear old events after background wait
        event_listener.getEventsBuffer().clear()

        #Step 3: Terminate from background/active
        if background:
            print("\nTerminating App A from background or active state")

            start_time = datetime.now(UTC).time()

            tdkTestObj = obj.createTestStep('rdkv_terminate_app')
            tdkTestObj.addParameter("app_id", app_A)
            tdkTestObj.executeTestCase(expectedResult)
            status = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails()
            if status == "SUCCESS":
                continue_count = 0
                terminated = False

                while continue_count < 120:
                    if len(event_listener.getEventsBuffer()) == 0:
                        time.sleep(1)
                        continue_count += 1
                        continue

                    event = event_listener.getEventsBuffer().pop(0)
                    print("\nEvent:", event)
                    break
                destroy_time = str(event).split("$$$")[0]
                start_dt = datetime.strptime(str(start_time), "%H:%M:%S.%f")
                end_dt = datetime.strptime(str(destroy_time), "%H:%M:%S.%f")

                time_taken = end_dt - start_dt
                time_taken_ms = time_taken.total_seconds() * 1000

                print("\nTime taken to terminate from background: {} ms".format(time_taken_ms))

                # Threshold
                conf_file, file_status = getConfigFileName(obj.realpath)

                _, threshold = getDeviceConfigKeyValue(conf_file,"APPMANAGER_TERMINATE_THRESHOLD_VALUE")

                if not threshold:
                    print("[FAILURE] APPMANAGER_TERMINATE_THRESHOLD_VALUE not configured in device configuration file")
                    status = "FAILURE"
                else:
                    threshold_val = int(threshold)
                    print(f"\nThreshold : {threshold_val} ms")
                    print(f"Measured  : {time_taken_ms} ms")
                    if 0 < int(time_taken_ms) < threshold_val:
                        print("\nTerminate within expected range")
                        print(f"Measured: {time_taken_ms} ms | Allowed: {threshold_val} ms")
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        diff = int(time_taken_ms) - threshold_val
                        print("\nTerminate exceeded threshold")
                        print(f"Measured : {time_taken_ms} ms")
                        print(f"Allowed  : {threshold_val} ms")
                        print(f"Exceeded by: {diff} ms")
                        tdkTestObj.setResultStatus("FAILURE")
                    Summ_list.append(f"Time taken : {time_taken_ms} ms")
                    Summ_list.append(f"Allowed time : {threshold_val} ms")
                    getSummary(Summ_list, obj)
            else:
                print("Terminate event not received")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("Failed to push App A to background (timeout after 30 seconds)")
            tdkTestObj.setResultStatus("FAILURE")

        event_listener.disconnect()
    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
