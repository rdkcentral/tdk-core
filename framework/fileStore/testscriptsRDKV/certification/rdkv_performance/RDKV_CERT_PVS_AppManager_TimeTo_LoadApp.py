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
import sys
from io import StringIO
import StabilityTestUtility
from StabilityTestUtility import *
from PerformanceTestVariables import *
from web_socket_util import *
from rdkv_performancelib import *
import rdkv_performancelib
import json
from datetime import datetime, UTC

# Test component
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeTo_LoadApp')

expectedResult = "SUCCESS"

# Load module
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

if expectedResult in result.upper():

    status = "SUCCESS"
    revert = "NO"
    
    print("\n[INFO] Activating AppManager plugins")
    
    # Ensure plugins active
    essential_plugins = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]
    plugin_status_needed = {p: "activated" for p in essential_plugins}
    
    # Suppress stdout for utility function calls
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj, essential_plugins)
    
    # Restore stdout
    sys.stdout = old_stdout
    
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = StabilityTestUtility.set_plugins_status(obj, plugin_status_needed)
        time.sleep(10)
    
    if status == "SUCCESS":
        print("[SUCCESS] AppManager plugins activated")
        
        # Get app configuration from PerformanceTestVariables
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name = app_bundle_name.split('+')[0]
        app_download_url = PerformanceTestVariables.app_download_url
        
        print(f"[INFO] App to load: {app_name}")
        
        # Get config file for thresholds
        conf_file, _ = getConfigFileName(obj.realpath)
        
        # INSTALL APP (using utility function)
        print(f"\n[INFO] Ensuring app {app_name} is installed")
        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name, app_download_url, launch=False)
        
        if status == "SUCCESS":
            print("[SUCCESS] App installation/verification completed")
            
            thunder_port = rdkv_performancelib.devicePort
            
            # CREATE EVENT LISTENER
            print("\n[INFO] Creating event listener")
            lifecycle_event = '{"jsonrpc": "2.0","id": 7,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'
            download_event = '{"jsonrpc": "2.0","id": 8,"method": "org.rdk.DownloadManager.1.register","params": {"event": "onAppDownloadStatus", "id": "client.events.2" }}'
            install_event = '{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppPackageManager.1.register","params": {"event": "onAppInstalled", "id": "client.events.3" }}'
            event_listener = createEventListener(ip, thunder_port, [lifecycle_event, download_event, install_event], "/jsonrpc", False)
            time.sleep(3)
            
            if event_listener:
                print("[SUCCESS] Event listener created")
                
                download_time_ms = 0
                install_time_ms = 0
                launch_time_ms = 0
                load_time_ms = 0
                
                # LAUNCH AND LOAD THE APP
                if status == "SUCCESS":
                    print(f"\n[INFO] Launching app {app_name}")
                    tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                    tdkTestObj.addParameter("app_name", app_name)
                    launch_start_time = datetime.now(UTC)  # Full datetime object
                    tdkTestObj.executeTestCase(expectedResult)
                    launch_result = tdkTestObj.getResult()
                    
                    if launch_result == "SUCCESS":
                        print("[INFO] Launch initiated, waiting for ACTIVE state")
                        
                        # Validate app is in loaded apps
                        print("\n[INFO] Validating app reached loaded state")
                        time.sleep(3)  # Brief wait for app to start initializing
                        
                        app_active = False
                        validate_count = 0
                        while validate_count < 30:  # 30 seconds timeout for validation
                            loaded_apps = rdkservice_get_loaded_apps()
                            if loaded_apps and app_name in str(loaded_apps):
                                print(f"[SUCCESS] App {app_name} verified in loaded apps (ACTIVE state)")
                                app_active = True
                                break
                            else:
                                # Check if app exists but still initializing
                                all_apps_result = rdkservice_getValue("org.rdk.AppManager.getLoadedApps")
                                if all_apps_result != "EXCEPTION OCCURRED":
                                    app_exists = any(item["appId"] == app_name for item in all_apps_result)
                                    if app_exists:
                                        print(f"[INFO] App exists but still initializing, waiting...")
                                        time.sleep(1)
                                        validate_count += 1
                                        continue
                            
                            time.sleep(1)
                            validate_count += 1
                        
                        if not app_active:
                            print(f"[ERROR] App {app_name} failed to reach ACTIVE state")
                            status = "FAILURE"
                        else:
                            # App confirmed ACTIVE via getLoadedApps - record the time
                            print(f"\n[SUCCESS] App {app_name} confirmed ACTIVE state via getLoadedApps")
                            launch_end_time = datetime.now(UTC)
                            
                            # Calculate launch time from command execution to ACTIVE confirmation
                            launch_time_delta = launch_end_time - launch_start_time
                            launch_time_ms = launch_time_delta.total_seconds() * 1000
                            load_time_ms = launch_time_ms
                            
                            print(f"[SUCCESS] Launch time (to ACTIVE): {launch_time_ms:.2f} ms")
                            
                            # Try to refine timing with event listener if available
                            print("\n[INFO] Checking for APP_STATE_ACTIVE event for timestamp refinement")
                            event_captured = False
                            continue_count = 0
                            launched_time = None
                            
                            while continue_count < 30 and not event_captured:  # Reduced timeout to 30s
                                if len(event_listener.getEventsBuffer()) == 0:
                                    time.sleep(1)
                                    continue_count += 1
                                    continue
                                
                                event_log = event_listener.getEventsBuffer().pop(0)
                                
                                if app_name in event_log and '"newState":"APP_STATE_ACTIVE"' in event_log:
                                    print(f"[INFO] APP_STATE_ACTIVE event received")
                                    try:
                                        launched_time = event_log.split('$$$')[0]
                                        event_captured = True
                                        # Use event timestamp if available and valid
                                        try:
                                            launch_end_dt = datetime.fromisoformat(launched_time.replace('Z', '+00:00')) if 'T' in launched_time else launch_end_time
                                            launch_time_delta = launch_end_dt - launch_start_time
                                            refined_launch_time_ms = launch_time_delta.total_seconds() * 1000
                                            if 0 < refined_launch_time_ms < 60000:  # Sanity check
                                                launch_time_ms = refined_launch_time_ms
                                                load_time_ms = refined_launch_time_ms
                                                print(f"[INFO] Using event timestamp - Launch time: {launch_time_ms:.2f} ms")
                                        except:
                                            print(f"[INFO] Could not parse event timestamp, using getLoadedApps time")
                                    except:
                                        pass
                                continue_count += 1
                            
                            if not event_captured:
                                print(f"[INFO] No event received, using getLoadedApps confirmation time: {launch_time_ms:.2f} ms")
                            
                            status = "SUCCESS"
                    else:
                        print("[FAILURE] Failed to initiate launch")
                        status = "FAILURE"
                
                if status == "SUCCESS" and load_time_ms > 0:
                    print(f"\n{'='*60}")
                    print("VALIDATION RESULTS")
                    print(f"{'='*60}")
                    
                    if download_time_ms > 0:
                        print(f"Download Time: {download_time_ms} ms")
                    if install_time_ms > 0:
                        print(f"Install Time: {install_time_ms} ms")
                    print(f"Launch Time: {launch_time_ms:.2f} ms")
                    print(f"Load Time: {load_time_ms:.2f} ms")
                    
                    # Get thresholds
                    old_stdout = sys.stdout
                    sys.stdout = StringIO()
                    
                    config_status, app_load_threshold = getDeviceConfigKeyValue(conf_file, "APPMANAGER_LAUNCH_THRESHOLD_VALUE")
                    
                    # Restore stdout
                    sys.stdout = old_stdout
                    
                    if not app_load_threshold:
                        print("[FAILURE] APPMANAGER_LAUNCH_THRESHOLD_VALUE not configured in device configuration file")
                        status = "FAILURE"
                    else:
                        threshold = int(app_load_threshold)
                        threshold_max = threshold
                        
                        print(f"\nThreshold: {threshold} ms")
                        print(f"Max allowed: {threshold_max} ms")
                        
                        if 0 < load_time_ms < threshold_max:
                            print(f"\n[SUCCESS] Load time is within expected range")
                            print(f"Measured: {load_time_ms:.2f} ms | Allowed: {threshold_max} ms")
                            status = "SUCCESS"
                        else:
                            print(f"\n[FAILURE] Load time exceeds threshold")
                            print(f"Measured: {load_time_ms:.2f} ms | Allowed: {threshold_max} ms")
                            status = "FAILURE"
                    
                    # TERMINATE APP
                    print(f"\n[INFO] Terminating app for cleanup")
                    tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                    tdkTestObj.addParameter("app_id", app_name)
                    tdkTestObj.executeTestCase(expectedResult)
                    terminate_result = tdkTestObj.getResult()
                    if terminate_result == "SUCCESS":
                        print("[SUCCESS] App terminated successfully")
                    else:
                        print("[FAILURE] Failed to terminate app")
                
                # Disconnect event listener
                print("\n[INFO] Disconnecting event listener")
                event_listener.disconnect()
            else:
                print("[FAILURE] Failed to create event listener")
                status = "FAILURE"
        else:
            print("[FAILURE] App installation failed")
            status = "FAILURE"
    
    # Report final status - CRITICAL: must be called in all paths
    if status == "SUCCESS":
        print("\n[SUCCESS] Load app test completed successfully")
    else:
        print("\n[FAILURE] Load app test failed")
    
    obj.setLoadModuleStatus(status)
    
    # Revert plugin status if changed
    if revert == "YES":
        print("\n[INFO] Reverting plugin status before exit")
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        StabilityTestUtility.set_plugins_status(obj, curr_plugins_status_dict)
        
        sys.stdout = old_stdout

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("[FAILURE] Failed to load module")
