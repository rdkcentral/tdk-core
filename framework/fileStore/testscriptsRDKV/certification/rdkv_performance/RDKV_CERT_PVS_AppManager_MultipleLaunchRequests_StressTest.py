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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_MultipleLaunchRequests_StressTest')

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"no")

#Execution summary variable
Summ_list=[]

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status = "SUCCESS"
    event_listener = None
    app_instance_id = ""
    test_app_id = ""
    launch_requests_sent = 0
    launch_responses_received = 0
    launch_events_received = 0
    duplicate_instances_detected = 0
    error_responses = 0

    # Required AI Manager plugins
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.PackageManagerRDKEMS":"activated", "org.rdk.AppManager":"activated"}
    conf_file, status = get_configfile_name(obj)
    status,supported_plugins = getDeviceConfigValue(conf_file,"SUPPORTED_PLUGINS")
    
    # Check if essential AI Manager plugins are available
    essential_ai_plugins = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager"]  
    missing_plugins = [plugin for plugin in essential_ai_plugins if plugin not in supported_plugins]
    
    if missing_plugins:
        print(f"\n Essential AI Manager plugins not available on this device: {missing_plugins}")
        print("\n This test requires AI Manager functionality which is not supported on this device")
        print(f"\n Available plugins: {supported_plugins}")
        status = "FAILURE"
        obj.setLoadModuleStatus("FAILURE")
    else:
        # Remove unsupported plugins from the list
        for plugin in plugins_list[:]:
            if plugin not in supported_plugins:
                plugins_list.remove(plugin)
                plugin_status_needed.pop(plugin)

        # Get initial plugin status using library function
        curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
        
        print(f"\n Current plugin status: {curr_plugins_status_dict}")
        print(f"\n Plugins being checked: {plugins_list}")
        print(f"\n Required plugin status: {plugin_status_needed}")

        # Check for failed plugin status
        failed_plugins = [plugin for plugin in plugins_list if curr_plugins_status_dict.get(plugin, "FAILURE") == "FAILURE"]
        if failed_plugins:
            print(f"\n Failed to get status for plugins: {failed_plugins}")
            print("\n Error while getting status of AI Manager plugins")
            status = "FAILURE"
        elif curr_plugins_status_dict != plugin_status_needed:
            revert = "YES"
            status = set_plugins_status(obj,plugin_status_needed)
            time.sleep(10)
            new_plugins_status_dict = get_plugins_status(obj,plugins_list)
            if new_plugins_status_dict != plugin_status_needed:
                status = "FAILURE"
        else:
            print("\n AI Manager plugins are already in the required state \n")

        if status == "SUCCESS":
            print("\n AI Manager plugins are available and activated successfully \n")

            # Setup event listener for lifecycle changes, download status, and app installation
            thunder_port = rdkv_performancelib.devicePort
            lifecycle_event = '{"jsonrpc": "2.0","id": 7,"method": "org.rdk.LifecycleManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'
            download_event = '{"jsonrpc": "2.0","id": 8,"method": "org.rdk.DownloadManager.1.register","params": {"event": "onAppDownloadStatus", "id": "client.events.2" }}'
            install_event = '{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppInstalled", "id": "client.events.3" }}'
            event_listener = createEventListener(ip, thunder_port, [lifecycle_event, download_event, install_event], "/jsonrpc", False)
            time.sleep(5)

            # Get app download URL and app name from configuration file
            config_status, app_download_url = getDeviceConfigKeyValue(conf_file, "PACKAGEMANAGER_APPLICATION_HOSTEDURL")
            app_name_status, app_id = getDeviceConfigKeyValue(conf_file, "PACKAGEMANAGER_APPLICATION_NAME")

            if config_status != "SUCCESS" or not app_download_url:
                print("\n PACKAGEMANAGER_APPLICATION_HOSTEDURL not configured in device configuration file \n")
                status = "FAILURE"
            elif app_name_status != "SUCCESS" or not app_id:
                print("\n PACKAGEMANAGER_APPLICATION_NAME not configured in device configuration file \n")
                status = "FAILURE"
            else:
                print(f"\n App download URL: {app_download_url} \n")
                print(f"\n Target App ID for multiple launch stress test: {app_id} \n")

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
                        "ai_manager_responsive": False,
                        "lifecycle_manager_responsive": False,
                        "system_stable": False
                    }
                    
                    # Check AI Manager responsiveness
                    try:
                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                        tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getRunningApps")
                        tdkTestObj.addParameter("value", "{}")
                        tdkTestObj.executeTestCase(expectedResult)
                        ai_manager_result = tdkTestObj.getResult()
                        health_status["ai_manager_responsive"] = (ai_manager_result == "SUCCESS")
                    except Exception as e:
                        print(f"\n System health check failed: {e} \n")
                        health_status["ai_manager_responsive"] = False
                    
                    # Check Lifecycle Manager responsiveness
                    try:
                        plugin_status = get_plugins_status(obj, ["org.rdk.AppManager"])
                        health_status["lifecycle_manager_responsive"] = (plugin_status.get("org.rdk.AppManager") != "FAILURE")
                    except Exception as e:
                        health_status["lifecycle_manager_responsive"] = False
                    
                    health_status["system_stable"] = all([
                        health_status["ai_manager_responsive"],
                        health_status["lifecycle_manager_responsive"]
                    ])
                    
                    return health_status

                # Phase 1: Prepare app for multiple launch test
                print(f"\n === PHASE 1: Preparing {app_id} for Multiple Launch Test === \n")
                
                # Check if app is installed
                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getInstalledApps")
                tdkTestObj.addParameter("value", "{}")
                tdkTestObj.executeTestCase(expectedResult)
                installed_apps_result = tdkTestObj.getResult()
                installed_apps_details = tdkTestObj.getResultDetails()
                
                app_installed = False
                if installed_apps_result == "SUCCESS":
                    try:
                        installed_apps_data = json.loads(installed_apps_details)
                        if "result" in installed_apps_data and "apps" in installed_apps_data["result"]:
                            installed_app_ids = [app.get("id", "") for app in installed_apps_data["result"]["apps"]]
                            app_installed = app_id in installed_app_ids
                    except json.JSONDecodeError:
                        print(f"\n Error parsing installed apps response \n")

                # Install app if needed
                if not app_installed and status == "SUCCESS":
                    print(f"\n Installing {app_id} for stress test... \n")
                    
                    # Download
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method", "org.rdk.DownloadManager.1.download")
                    tdkTestObj.addParameter("value", '{"url": "' + app_download_url + '", "appId": "' + app_id + '"}')
                    tdkTestObj.executeTestCase(expectedResult)
                    download_result = tdkTestObj.getResult()
                    
                    if download_result == "SUCCESS":
                        # Wait for download completion
                        download_timeout = 120
                        continue_count = 0
                        download_success = False
                        
                        while continue_count < download_timeout and not download_success:
                            if len(event_listener.getEventsBuffer()) > 0:
                                event_log = event_listener.getEventsBuffer().pop(0)
                                if app_id in event_log and "onAppDownloadStatus" in str(event_log):
                                    event_data = json.loads(event_log.split('$$$')[1])
                                    if event_data.get("status") == "Downloaded":
                                        download_success = True
                            continue_count += 1
                            time.sleep(1)
                            
                        if download_success:
                            # Install
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method", "org.rdk.PackageManagerRDKEMS.1.install")
                            tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                            tdkTestObj.executeTestCase(expectedResult)
                            install_result = tdkTestObj.getResult()
                            
                            if install_result == "SUCCESS":
                                # Wait for installation completion
                                install_timeout = 120
                                continue_count = 0
                                
                                while continue_count < install_timeout:
                                    if len(event_listener.getEventsBuffer()) > 0:
                                        event_log = event_listener.getEventsBuffer().pop(0)
                                        if app_id in event_log and "onAppInstalled" in str(event_log):
                                            app_installed = True
                                            print(f"\n App {app_id} installed successfully \n")
                                            Summ_list.append("App installation: SUCCESS")
                                            break
                                    continue_count += 1
                                    time.sleep(1)

                # Phase 2: Terminate any existing instances
                if app_installed and status == "SUCCESS":
                    print(f"\n === PHASE 2: Ensuring Clean State for {app_id} === \n")
                    
                    # Check if app is already running
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getRunningApps")
                    tdkTestObj.addParameter("value", "{}")
                    tdkTestObj.executeTestCase(expectedResult)
                    running_apps_result = tdkTestObj.getResult()
                    
                    if running_apps_result == "SUCCESS":
                        running_apps_details = tdkTestObj.getResultDetails()
                        try:
                            running_apps_data = json.loads(running_apps_details)
                            if "result" in running_apps_data and "apps" in running_apps_data["result"]:
                                for running_app in running_apps_data["result"]["apps"]:
                                    if running_app.get("id") == app_id:
                                        print(f"\n Terminating existing instance of {app_id} \n")
                                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                        tdkTestObj.addParameter("method", "org.rdk.AppManager.1.terminateApp")
                                        tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                                        tdkTestObj.executeTestCase(expectedResult)
                                        time.sleep(3)  # Allow termination to complete
                                        break
                        except json.JSONDecodeError:
                            print(f"\n Error parsing running apps response \n")

                    print(f"\n Clean state established for {app_id} \n")
                    Summ_list.append("Clean state preparation: SUCCESS")

                    # Phase 3: Multiple Launch Requests Stress Test
                    print(f"\n === PHASE 3: MULTIPLE LAUNCH REQUESTS STRESS TEST === \n")
                    print(f"\n Sending {multiple_launch_count} rapid launch requests for {app_id} \n")

                    # Track launch request results
                    launch_results = []
                    launch_start_times = []
                    instance_ids_seen = set()
                    
                    # Function to send a single launch request
                    def send_launch_request(request_id):
                        nonlocal launch_requests_sent, launch_responses_received, error_responses
                        
                        try:
                            print(f"\n [Request {request_id}] Sending launch request for {app_id} \n")
                            launch_requests_sent += 1
                            
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method", "org.rdk.AppManager.1.launchApp")
                            tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                            launch_start_time = str(datetime.utcnow()).split()[1]
                            launch_start_times.append(launch_start_time)
                            
                            tdkTestObj.executeTestCase(expectedResult)
                            launch_result = tdkTestObj.getResult()
                            launch_responses_received += 1
                            
                            if launch_result == "SUCCESS":
                                launch_results.append({"request_id": request_id, "result": "SUCCESS", "start_time": launch_start_time})
                                print(f"\n [Request {request_id}] Launch command accepted \n")
                            else:
                                launch_results.append({"request_id": request_id, "result": "FAILURE", "start_time": launch_start_time})
                                error_responses += 1
                                print(f"\n [Request {request_id}] Launch command rejected \n")
                                
                        except Exception as e:
                            error_responses += 1
                            print(f"\n [Request {request_id}] Exception during launch: {e} \n")
                            launch_results.append({"request_id": request_id, "result": "EXCEPTION", "start_time": None})

                    # Send multiple launch requests with small delays
                    stress_test_start_time = str(datetime.utcnow()).split()[1]
                    
                    for i in range(int(multiple_launch_count)):
                        send_launch_request(i + 1)
                        if i < int(multiple_launch_count) - 1:  # Don't delay after last request
                            time.sleep(int(launch_delay) / 1000.0)  # Convert ms to seconds

                    print(f"\n All {multiple_launch_count} launch requests sent \n")
                    
                    # Phase 4: Monitor system response and events
                    print(f"\n === PHASE 4: Monitoring System Response === \n")
                    
                    # Monitor events for a extended period
                    monitoring_timeout = 60  # Monitor for 1 minute
                    continue_count = 0
                    unique_launch_events = []
                    
                    while continue_count < monitoring_timeout:
                        if len(event_listener.getEventsBuffer()) > 0:
                            event_log = event_listener.getEventsBuffer().pop(0)
                            
                            if app_id in event_log and "onAppLifecycleStateChanged" in str(event_log):
                                launch_events_received += 1
                                event_time = event_log.split('$$$')[0]
                                event_data = json.loads(event_log.split('$$$')[1])
                                app_state = event_data.get("state", "").lower()
                                instance_id = event_data.get("instanceId", "")
                                
                                print(f"\n [Event {launch_events_received}] App lifecycle: {app_state}, Instance: {instance_id} \n")
                                
                                if instance_id:
                                    if instance_id in instance_ids_seen:
                                        duplicate_instances_detected += 1
                                        print(f"\n WARNING: Duplicate instance ID detected: {instance_id} \n")
                                    else:
                                        instance_ids_seen.add(instance_id)
                                
                                unique_launch_events.append({
                                    "state": app_state,
                                    "instance_id": instance_id,
                                    "event_time": event_time
                                })
                                
                        continue_count += 1
                        time.sleep(1)
                    
                    # Phase 5: System Health Check and Analysis
                    print(f"\n === PHASE 5: System Health Check and Analysis === \n")
                    
                    post_stress_health = check_system_health()
                    
                    # Check current running apps
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getRunningApps")
                    tdkTestObj.addParameter("value", "{}")
                    tdkTestObj.executeTestCase(expectedResult)
                    final_running_result = tdkTestObj.getResult()
                    
                    active_instances_count = 0
                    if final_running_result == "SUCCESS":
                        final_running_details = tdkTestObj.getResultDetails()
                        try:
                            final_running_data = json.loads(final_running_details)
                            if "result" in final_running_data and "apps" in final_running_data["result"]:
                                for running_app in final_running_data["result"]["apps"]:
                                    if running_app.get("id") == app_id:
                                        active_instances_count += 1
                        except json.JSONDecodeError:
                            print(f"\n Error parsing final running apps response \n")

                    # Analysis and Results
                    print(f"\n === STRESS TEST ANALYSIS === \n")
                    print(f"\n Launch Requests Sent: {launch_requests_sent}")
                    print(f"\n Launch Responses Received: {launch_responses_received}") 
                    print(f"\n Error Responses: {error_responses}")
                    print(f"\n Lifecycle Events Received: {launch_events_received}")
                    print(f"\n Unique Instance IDs: {len(instance_ids_seen)}")
                    print(f"\n Duplicate Instances Detected: {duplicate_instances_detected}")
                    print(f"\n Active App Instances: {active_instances_count}")
                    
                    Summ_list.append(f"Launch requests sent: {launch_requests_sent}")
                    Summ_list.append(f"Launch responses received: {launch_responses_received}")
                    Summ_list.append(f"Error responses: {error_responses}")
                    Summ_list.append(f"Lifecycle events received: {launch_events_received}")
                    Summ_list.append(f"Unique instance IDs: {len(instance_ids_seen)}")
                    Summ_list.append(f"Active app instances: {active_instances_count}")

                    # Assessment of behavior
                    test_app_id = app_id
                    behavioral_analysis_passed = True
                    
                    # Check 1: System should handle multiple launch requests gracefully
                    if error_responses > (int(multiple_launch_count) * 0.8):  # More than 80% errors is unusual
                        print(f"\nHigh error rate: {error_responses}/{launch_requests_sent} requests failed \n")
                        Summ_list.append("High error rate detected")
                        behavioral_analysis_passed = False
                    else:
                        print(f"\n Acceptable error handling: {error_responses}/{launch_requests_sent} requests failed \n")
                    
                    # Check 2: System should not create excessive duplicate instances
                    if active_instances_count > 3:  # More than 3 instances might indicate poor resource management
                        print(f"\n Excessive app instances: {active_instances_count} active instances \n")
                        Summ_list.append("Excessive app instances created")
                        behavioral_analysis_passed = False
                    else:
                        print(f"\n Reasonable instance management: {active_instances_count} active instances \n")
                    
                    # Check 3: System should remain responsive
                    if not post_stress_health["system_stable"]:
                        print(f"\n System instability detected after stress test \n")
                        Summ_list.append("Post-stress system instability")
                        behavioral_analysis_passed = False
                    else:
                        print(f"\n System remained stable during stress test \n")
                        
                    # Check 4: Events should be reasonable
                    if launch_events_received == 0 and launch_responses_received > 0:
                        print(f"\n No lifecycle events received despite successful launch responses \n")
                        Summ_list.append("Missing lifecycle events")
                        behavioral_analysis_passed = False
                    
                    # Final assessment
                    if behavioral_analysis_passed:
                        print(f"\n === MULTIPLE LAUNCH STRESS TEST: PASSED === \n")
                        print(f"\n System handled {multiple_launch_count} rapid launch requests appropriately \n")
                        print(f"\n App {test_app_id} behavior under multiple launch stress: ACCEPTABLE \n")
                        Summ_list.append("Multiple launch stress test: PASSED")
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print(f"\n === MULTIPLE LAUNCH STRESS TEST: ISSUES DETECTED === \n")
                        print(f"\n System showed problematic behavior during multiple launch requests \n")
                        print(f"\n App {test_app_id} behavior under multiple launch stress: PROBLEMATIC \n")
                        Summ_list.append("Multiple launch stress test: ISSUES DETECTED")
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.setResultStatus("FAILURE")
                        status = "FAILURE"

                else:
                    print(f"\n Cannot perform stress test - app {app_id} is not installed \n")
                    Summ_list.append("Test prerequisite failed: App not installed")
                    status = "FAILURE"

            # Disconnect event listener
            if event_listener:
                print("\n Disconnecting event listener \n")
                event_listener.disconnect()

        else:
            print("\n AI Manager plugins preconditions are not met \n")
            obj.setLoadModuleStatus("FAILURE")
                
    getSummary(Summ_list, obj)

    #Revert the values
    if revert == "YES":
        print("Revert the plugin status before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict)

    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
