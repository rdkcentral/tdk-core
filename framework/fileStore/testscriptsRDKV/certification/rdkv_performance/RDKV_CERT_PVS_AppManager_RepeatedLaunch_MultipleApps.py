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
from StabilityTestUtility import *
from PerformanceTestVariables import *
from web_socket_util import *
from rdkv_performancelib import *
import rdkv_performancelib
import json
from datetime import datetime
import time
import threading

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_RepeatedLaunch_MultipleApps')

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"no")


#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    status = "SUCCESS"
    event_listener = None
    app_instance_id = ""
    test_app_id = ""
    
    # Use dictionary for request tracking to avoid nonlocal scoping issues
    request_tracking = {
        'launch_requests_sent': 0,
        'launch_responses_received': 0,
        'error_responses': 0,
        'launch_events_received': 0,
        'duplicate_instances_detected': 0
    }

    # Ensure plugins active
    essential_plugins = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]
    plugin_status_needed = {p: "activated" for p in essential_plugins}
    status = set_plugins_status(obj, plugin_status_needed)
    
    if status != "SUCCESS":
        print(f"\n Failed to activate essential AppManager plugins \n")
        obj.setLoadModuleStatus("FAILURE")
    else:
        print(f"\n Essential AppManager plugins activated successfully \n")

    if status == "SUCCESS":
        # Get app configuration
        conf_file, conf_status = get_configfile_name(obj)
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_id = app_bundle_name.split('+')[0]
        app_download_url = PerformanceTestVariables.app_download_url
        
        print(f"\n App download URL: {app_download_url} \n")
        print(f"\n Target App ID for multiple launch stress test: {app_id} \n")
        
        if not app_download_url or not app_id:
            print("\n Failed to get app configuration from PerformanceTestVariables \n")
            status = "FAILURE"

        if status == "SUCCESS":
            # Setup event listener for lifecycle changes, download status, and app installation
            thunder_port = rdkv_performancelib.devicePort
            lifecycle_event = '{"jsonrpc": "2.0","id": 7,"method": "org.rdk.LifecycleManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'
            download_event = '{"jsonrpc": "2.0","id": 8,"method": "org.rdk.DownloadManager.1.register","params": {"event": "onAppDownloadStatus", "id": "client.events.2" }}'
            install_event = '{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppInstalled", "id": "client.events.3" }}'
            event_listener = createEventListener(ip, thunder_port, [lifecycle_event, download_event, install_event], "/jsonrpc", False)
            time.sleep(5)
            
            # Get test configuration
            multiple_launch_count_status, multiple_launch_count = getDeviceConfigKeyValue(conf_file, "MULTIPLE_LAUNCH_REQUEST_COUNT")
            if multiple_launch_count_status != "SUCCESS" or not multiple_launch_count:
                multiple_launch_count = "5"  # Default to 5 simultaneous launch requests
                
            launch_delay_status, launch_delay = getDeviceConfigKeyValue(conf_file, "LAUNCH_REQUEST_DELAY_MS")
            if launch_delay_status != "SUCCESS" or not launch_delay:
                launch_delay = "100"  # Default to 100ms delay between requests

            print(f"\n Test Configuration: {multiple_launch_count} launch requests with {launch_delay}ms delay \n")

            # Function to check system health during stress test
            def check_system_health():
                health_status = {
                    "app_manager_responsive": False,
                    "system_stable": False
                }
                
                try:
                    response, json_response, status = rdkv_performancelib.rdkservice_get_loaded_apps()
                    health_status["app_manager_responsive"] = (status == "SUCCESS")
                    if status == "SUCCESS":
                        print(f"\n AppManager responsive - Running apps: {json_response} \n")
                    else:
                        print(f"\n AppManager check failed: {response} \n")
                except Exception as e:
                    print(f"\n System health check failed: {e} \n")
                    health_status["app_manager_responsive"] = False
                
                health_status["system_stable"] = health_status["app_manager_responsive"]
                
                return health_status

            # Phase 1: Install and prepare app
            print(f"\n === PHASE 1: Installing {app_id} === \n")
            
            app_installed = False
            if status == "SUCCESS":
                install_status = rdkservice_install_launch_app(obj, app_bundle_name, app_id, app_download_url, launch=False)
                if install_status == "SUCCESS":
                    app_installed = True
                    print(f"[SUCCESS] App {app_id} installed successfully \n")
                else:
                    print(f"[FAILURE] Failed to install app {app_id}: {install_status} \n")
                    status = "FAILURE"

            # Phase 2: Validate app installation and establish clean state
            if app_installed and status == "SUCCESS":
                print(f"\n === PHASE 2: Validating Installation and Clean State === \n")
                
                # Verify app is installed
                loaded_apps = rdkservice_get_loaded_apps()
                if loaded_apps and app_id in str(loaded_apps):
                    print(f"[SUCCESS] App {app_id} verified as installed \n")
                else:
                    print(f"[INFO] App not yet in loaded state, will launch during stress test \n")
                
                # Terminate any existing instances
                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getLoadedApps")
                tdkTestObj.executeTestCase(expectedResult)
                loaded_result = tdkTestObj.getResult()
                
                if loaded_result == "SUCCESS":
                    loaded_details = tdkTestObj.getResultDetails()
                    try:
                        loaded_data = json.loads(loaded_details)
                        if isinstance(loaded_data, list):
                            loaded_apps = loaded_data
                        elif "apps" in loaded_data:
                            loaded_apps = loaded_data["apps"]
                        else:
                            loaded_apps = []
                        
                        for loaded_app in loaded_apps:
                            if loaded_app.get("appId") == app_id or loaded_app.get("id") == app_id:
                                print(f"[INFO] Terminating existing instance of {app_id} \n")
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.addParameter("method", "org.rdk.AppManager.1.terminateApp")
                                tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                                tdkTestObj.executeTestCase(expectedResult)
                                time.sleep(2)
                                break
                    except json.JSONDecodeError:
                        print(f"[ERROR] Error parsing loaded apps response \n")

                print(f"[SUCCESS] Clean state established \n")

                # Phase 3: Multiple Launch Requests Stress Test
                print(f"\n === PHASE 3: Sending {multiple_launch_count} Rapid Launch Requests === \n")
                print(f"[INFO] Launch delay between requests: {launch_delay}ms \n")

                launch_results = []
                instance_ids_seen = set()
                
                def send_launch_request(request_id, tracking):
                    try:
                        print(f"[INFO] [Request {request_id}] Sending launch for {app_id}")
                        tracking['launch_requests_sent'] += 1
                        
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method", "org.rdk.AppManager.1.launchApp")
                        tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                        
                        tdkTestObj.executeTestCase(expectedResult)
                        launch_result = tdkTestObj.getResult()
                        tracking['launch_responses_received'] += 1
                        
                        if launch_result == "SUCCESS":
                            launch_results.append({"request_id": request_id, "result": "SUCCESS"})
                            print(f"[SUCCESS] [Request {request_id}] Launch accepted")
                        else:
                            launch_results.append({"request_id": request_id, "result": "FAILURE"})
                            tracking['error_responses'] += 1
                            print(f"[FAILURE] [Request {request_id}] Launch rejected")
                            
                    except Exception as e:
                        tracking['error_responses'] += 1
                        print(f"[ERROR] [Request {request_id}] Exception: {e}")
                        launch_results.append({"request_id": request_id, "result": "EXCEPTION"})

                # Send multiple launch requests with small delays
                for i in range(int(multiple_launch_count)):
                    send_launch_request(i + 1, request_tracking)
                    if i < int(multiple_launch_count) - 1:
                        time.sleep(int(launch_delay) / 1000.0)

                print(f"[SUCCESS] All {multiple_launch_count} launch requests sent \n")
                
                # Phase 4: Monitor lifecycle events
                print(f"\n === PHASE 4: Monitoring App Lifecycle Events === \n")
                
                monitoring_timeout = 60
                continue_count = 0
                
                while continue_count < monitoring_timeout:
                    if len(event_listener.getEventsBuffer()) > 0:
                        event_log = event_listener.getEventsBuffer().pop(0)
                        
                        if app_id in event_log and "onAppLifecycleStateChanged" in str(event_log):
                            request_tracking['launch_events_received'] += 1
                            try:
                                event_data = json.loads(event_log.split('$$$')[1])
                                app_state = event_data.get("state", "UNKNOWN")
                                instance_id = event_data.get("instanceId", "unknown")
                                
                                print(f"[EVENT] State: {app_state} | Instance: {instance_id}")
                                
                                if instance_id and instance_id not in instance_ids_seen:
                                    instance_ids_seen.add(instance_id)
                                elif instance_id and instance_id in instance_ids_seen:
                                    request_tracking['duplicate_instances_detected'] += 1
                            except Exception as e:
                                print(f"[INFO] Event received but parsing skipped")
                            
                    continue_count += 1
                    time.sleep(1)
                
                print(f"[INFO] Monitoring complete - {request_tracking['launch_events_received']} events received \n")
                
                # Phase 5: System stability validation
                print(f"\n === PHASE 5: System Stability Validation === \n")
                
                post_stress_health = check_system_health()
                
                if post_stress_health["system_stable"]:
                    print(f"[SUCCESS] System remains stable after stress test \n")
                else:
                    print(f"[WARNING] System shows instability after stress test \n")
                    status = "FAILURE"
                
                # Phase 6: Cleanup - Terminate all app instances
                print(f"\n === PHASE 6: Cleanup and Termination === \n")
                
                # Terminate app using rdkv_terminate_app function with test step
                print(f"[INFO] Terminating {app_id}")
                tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                tdkTestObj.addParameter("app_id", app_id)
                tdkTestObj.executeTestCase(expectedResult)
                terminate_result = tdkTestObj.getResult()
                if terminate_result == "SUCCESS":
                    print(f"[SUCCESS] App {app_id} terminated successfully \n")
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print(f"[FAILURE] Terminate failed: {terminate_result} \n")
                    tdkTestObj.setResultStatus("FAILURE")
                    status = "FAILURE"
                time.sleep(2)                
                # Analysis and Results
                print(f"\n === STRESS TEST RESULTS === \n")
                print(f"Launch Requests Sent: {request_tracking['launch_requests_sent']}")
                print(f"Launch Responses Received: {request_tracking['launch_responses_received']}") 
                print(f"Error Responses: {request_tracking['error_responses']}")
                print(f"Lifecycle Events Received: {request_tracking['launch_events_received']}")
                print(f"Unique Instance IDs: {len(instance_ids_seen)}")
                print(f"Duplicate Instances Detected: {request_tracking['duplicate_instances_detected']}")
                
                # Behavioral assessment
                test_app_id = app_id
                behavioral_analysis_passed = True
                
                # Check 1: Most launches should be accepted
                if request_tracking['launch_responses_received'] > 0:
                    error_rate = (request_tracking['error_responses'] / request_tracking['launch_responses_received']) * 100
                    if error_rate > 30:  # More than 30% errors is problematic
                        print(f"\n[FAILURE] High error rate: {error_rate:.1f}% ({request_tracking['error_responses']}/{request_tracking['launch_responses_received']})")
                        behavioral_analysis_passed = False
                    else:
                        print(f"[SUCCESS] Acceptable error rate: {error_rate:.1f}%")
                
                # Check 2: System should handle duplicates gracefully
                if request_tracking['duplicate_instances_detected'] > 0:
                    print(f"\n[WARNING] {request_tracking['duplicate_instances_detected']} duplicate instances detected")
                else:
                    print(f"[SUCCESS] No duplicate instances detected")
                
                # Check 3: System should remain responsive
                if not post_stress_health["system_stable"]:
                    print(f"\n[FAILURE] System instability detected after stress test")
                    behavioral_analysis_passed = False
                else:
                    print(f"[SUCCESS] System remained stable")
                    
                # Check 4: Events should be reasonable
                if request_tracking['launch_events_received'] == 0 and request_tracking['launch_responses_received'] > 0:
                    print(f"\n[WARNING] No lifecycle events received despite launch responses")
                
                # Final assessment
                if behavioral_analysis_passed:
                    print(f"\n === TEST RESULT: PASSED === \n")
                    print(f"System handled {multiple_launch_count} rapid launches appropriately")
                    status = "SUCCESS"
                else:
                    print(f"\n === TEST RESULT: FAILED === \n")
                    print(f"System showed problematic behavior during stress test")
                    status = "FAILURE"

            else:
                print(f"\n Cannot perform stress test - app {app_id} is not installed \n")
                status = "FAILURE"

        # Disconnect event listener
        if event_listener:
            print("[INFO] Disconnecting event listener \n")
            event_listener.disconnect()

    # Report final status - CRITICAL: must be called in all paths
    if status == "SUCCESS":
        print("[SUCCESS] Repeated launch stress test completed successfully")
    else:
        print("[FAILURE] Repeated launch stress test failed")
    
    obj.setLoadModuleStatus(status)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
