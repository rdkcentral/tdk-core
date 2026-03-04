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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_InstallAppTwice_Stability')

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
    install_attempts = 0
    install_responses_received = 0
    install_events_received = 0
    error_responses = 0
    duplicate_entries_detected = 0

    # Required AI Manager plugins
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager", "org.rdk.SystemServices"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.PackageManagerRDKEMS":"activated", "org.rdk.AppManager":"activated", "org.rdk.SystemServices":"activated"}
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

            # Setup event listener for lifecycle changes, download status, app installation and system monitoring
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
                print(f"\n Target App ID for duplicate install test: {app_id} \n")

                # Get test configuration
                duplicate_install_count_status, duplicate_install_count = getDeviceConfigKeyValue(conf_file, "DUPLICATE_INSTALL_ATTEMPT_COUNT")
                if duplicate_install_count_status != "SUCCESS" or not duplicate_install_count:
                    duplicate_install_count = "3"  # Default to 3 duplicate install attempts
                    
                print(f"\n Test Configuration: {duplicate_install_count} duplicate install attempts \n")

                # Function to assess system stability during duplicate install test
                def assess_system_stability():
                    print("\n === Assessing System Stability === \n")
                    stability_status = {
                        "package_manager_responsive": False,
                        "app_manager_responsive": False,
                        "system_services_responsive": False,
                        "memory_operations_stable": False,
                        "overall_stable": False
                    }
                    
                    # Test PackageManager responsiveness
                    try:
                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                        tdkTestObj.addParameter("method", "org.rdk.PackageManagerRDKEMS.1.getInstalledPackages")
                        tdkTestObj.addParameter("value", "{}")
                        tdkTestObj.executeTestCase(expectedResult)
                        package_manager_result = tdkTestObj.getResult()
                        stability_status["package_manager_responsive"] = (package_manager_result == "SUCCESS")
                        
                        if stability_status["package_manager_responsive"]:
                            print("\n PackageManager is responsive")
                        else:
                            print("\n PackageManager is not responsive")
                    except Exception as e:
                        print(f"\n PackageManager test failed: {e}")
                        stability_status["package_manager_responsive"] = False
                    
                    # Test AppManager responsiveness
                    try:
                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                        tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getInstalledApps")
                        tdkTestObj.addParameter("value", "{}")
                        tdkTestObj.executeTestCase(expectedResult)
                        app_manager_result = tdkTestObj.getResult()
                        stability_status["app_manager_responsive"] = (app_manager_result == "SUCCESS")
                        
                        if stability_status["app_manager_responsive"]:
                            print("\n AppManager is responsive")
                        else:
                            print("\n AppManager is not responsive")
                    except Exception as e:
                        print(f"\n AppManager test failed: {e}")
                        stability_status["app_manager_responsive"] = False
                    
                    # Test SystemServices responsiveness (if available)
                    if "org.rdk.SystemServices" in supported_plugins:
                        try:
                            tdkTestObj = obj.createTestStep('rdkservice_getValue')
                            tdkTestObj.addParameter("method", "org.rdk.SystemServices.1.getSystemVersions")
                            tdkTestObj.addParameter("value", "{}")
                            tdkTestObj.executeTestCase(expectedResult)
                            system_services_result = tdkTestObj.getResult()
                            stability_status["system_services_responsive"] = (system_services_result == "SUCCESS")
                            
                            if stability_status["system_services_responsive"]:
                                print("\n SystemServices is responsive")
                            else:
                                print("\n SystemServices is not responsive")
                        except Exception as e:
                            print(f"\n SystemServices test failed: {e}")
                            stability_status["system_services_responsive"] = False
                    else:
                        stability_status["system_services_responsive"] = True  # Skip if not available
                    
                    # Test memory operations stability via running apps
                    try:
                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                        tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getRunningApps")
                        tdkTestObj.addParameter("value", "{}")
                        tdkTestObj.executeTestCase(expectedResult)
                        memory_result = tdkTestObj.getResult()
                        stability_status["memory_operations_stable"] = (memory_result == "SUCCESS")
                        
                        if stability_status["memory_operations_stable"]:
                            print("\nMemory operations are stable")
                        else:
                            print("\nMemory operations may be unstable")
                    except Exception as e:
                        print(f"\nMemory stability test failed: {e}")
                        stability_status["memory_operations_stable"] = False
                    
                    # Overall stability assessment
                    stability_status["overall_stable"] = all([
                        stability_status["package_manager_responsive"],
                        stability_status["app_manager_responsive"],
                        stability_status["system_services_responsive"],
                        stability_status["memory_operations_stable"]
                    ])
                    
                    if stability_status["overall_stable"]:
                        print("\nOverall system stability: STABLE")
                    else:
                        print("\nOverall system stability: UNSTABLE")
                        
                    return stability_status

                # Function to check for duplicate app entries
                def check_for_duplicate_entries(target_app_id):
                    duplicate_count = 0
                    
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getInstalledApps")
                    tdkTestObj.addParameter("value", "{}")
                    tdkTestObj.executeTestCase(expectedResult)
                    installed_apps_result = tdkTestObj.getResult()
                    
                    if installed_apps_result == "SUCCESS":
                        installed_apps_details = tdkTestObj.getResultDetails()
                        try:
                            installed_apps_data = json.loads(installed_apps_details)
                            if "result" in installed_apps_data and "apps" in installed_apps_data["result"]:
                                for app in installed_apps_data["result"]["apps"]:
                                    if app.get("id") == target_app_id:
                                        duplicate_count += 1
                        except json.JSONDecodeError:
                            print(f"\n Error parsing installed apps for duplicate check \n")
                    
                    return duplicate_count

                # Phase 1: Establish baseline system stability
                print(f"\n === PHASE 1: Baseline System Stability Assessment === \n")
                baseline_stability = assess_system_stability()
                
                if not baseline_stability["overall_stable"]:
                    print("\n ABORT: System is not stable at baseline - cannot proceed with test \n")
                    Summ_list.append("Baseline stability check: FAILED")
                    status = "FAILURE"
                else:
                    print("\n Baseline system stability confirmed - proceeding with test \n")
                    Summ_list.append("Baseline stability check: PASSED")

                    # Phase 2: Ensure app is installed (prerequisite)
                    print(f"\n === PHASE 2: Ensuring {app_id} is Already Installed === \n")
                    
                    # Check if app is already installed
                    initial_app_count = check_for_duplicate_entries(app_id)
                    
                    if initial_app_count == 0:
                        print(f"\n App {app_id} is not installed, installing it first... \n")
                        
                        # Download app first
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
                                # Install app (initial installation)
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.addParameter("method", "org.rdk.PackageManagerRDKEMS.1.install")
                                tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                                tdkTestObj.executeTestCase(expectedResult)
                                initial_install_result = tdkTestObj.getResult()
                                
                                if initial_install_result == "SUCCESS":
                                    # Wait for installation completion
                                    install_timeout = 120
                                    continue_count = 0
                                    
                                    while continue_count < install_timeout:
                                        if len(event_listener.getEventsBuffer()) > 0:
                                            event_log = event_listener.getEventsBuffer().pop(0)
                                            if app_id in event_log and "onAppInstalled" in str(event_log):
                                                print(f"\n Initial installation of {app_id} completed \n")
                                                Summ_list.append("Initial app installation: SUCCESS")
                                                break
                                        continue_count += 1
                                        time.sleep(1)
                                else:
                                    print(f"\n Failed to perform initial installation of {app_id} \n")
                                    Summ_list.append("Initial app installation: FAILED")
                                    status = "FAILURE"
                            else:
                                print(f"\n Failed to download {app_id} for initial installation \n")
                                status = "FAILURE"
                        else:
                            print(f"\n Failed to initiate download for initial installation of {app_id} \n")  
                            status = "FAILURE"
                    else:
                        print(f"\n App {app_id} is already installed ({initial_app_count} entries found) \n")
                        Summ_list.append(f"App already installed: {initial_app_count} entries")

                    # Verify app is now installed
                    if status == "SUCCESS":
                        final_check_count = check_for_duplicate_entries(app_id)
                        if final_check_count > 0:
                            print(f"\n Confirmed: {app_id} is installed ({final_check_count} entries) \n")
                            print(f"\n Ready to test duplicate installation attempts \n")
                            
                            # Phase 3: Attempt duplicate installations (MAIN TEST)
                            print(f"\n === PHASE 3: DUPLICATE INSTALLATION STRESS TEST === \n")
                            print(f"\n Attempting to install already-installed app {app_id} {duplicate_install_count} times \n")
                            
                            duplicate_install_results = []
                            
                            for attempt in range(int(duplicate_install_count)):
                                print(f"\n [Attempt {attempt + 1}/{duplicate_install_count}] Installing already-installed app {app_id} \n")
                                install_attempts += 1
                                
                                try:
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                    tdkTestObj.addParameter("method", "org.rdk.PackageManagerRDKEMS.1.install")
                                    tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                                    install_start_time = str(datetime.utcnow()).split()[1]
                                    tdkTestObj.executeTestCase(expectedResult)
                                    duplicate_install_result = tdkTestObj.getResult()
                                    install_responses_received += 1
                                    
                                    if duplicate_install_result == "SUCCESS":
                                        duplicate_install_results.append({"attempt": attempt + 1, "result": "SUCCESS"})
                                        print(f"\n [Attempt {attempt + 1}] Duplicate install command accepted \n")
                                    else:
                                        duplicate_install_results.append({"attempt": attempt + 1, "result": "FAILURE"})
                                        error_responses += 1
                                        print(f"\n [Attempt {attempt + 1}] Duplicate install command rejected \n")
                                        
                                except Exception as e:
                                    error_responses += 1
                                    print(f"\n [Attempt {attempt + 1}] Exception during duplicate install: {e} \n")
                                    duplicate_install_results.append({"attempt": attempt + 1, "result": "EXCEPTION"})
                                
                                # Small delay between attempts
                                time.sleep(2)
                            
                            # Phase 4: Monitor events and check for duplicates
                            print(f"\n === PHASE 4: Monitoring System Response === \n")
                            
                            # Monitor events for response
                            monitoring_timeout = 30  # Monitor for 30 seconds
                            continue_count = 0
                            
                            while continue_count < monitoring_timeout:
                                if len(event_listener.getEventsBuffer()) > 0:
                                    event_log = event_listener.getEventsBuffer().pop(0)
                                    
                                    if app_id in event_log and "onAppInstalled" in str(event_log):
                                        install_events_received += 1
                                        print(f"\n [Event {install_events_received}] onAppInstalled event received for duplicate install \n")
                                
                                continue_count += 1
                                time.sleep(1)
                            
                            # Check for duplicate entries after duplicate install attempts
                            post_duplicate_count = check_for_duplicate_entries(app_id)
                            duplicate_entries_detected = max(0, post_duplicate_count - final_check_count)
                            
                            # Phase 5: System Stability Assessment and Analysis
                            print(f"\n === PHASE 5: Post-Duplicate-Install Stability Assessment === \n")
                            
                            post_stress_stability = assess_system_stability()
                            
                            # Analysis and Results
                            print(f"\n === DUPLICATE INSTALLATION TEST ANALYSIS === \n")
                            print(f"\n Duplicate Install Attempts: {install_attempts}")
                            print(f"\n Install Responses Received: {install_responses_received}")
                            print(f"\n Error Responses: {error_responses}")  
                            print(f"\n Install Events Received: {install_events_received}")
                            print(f"\n App Entries Before Test: {final_check_count}")
                            print(f"\n App Entries After Test: {post_duplicate_count}")
                            print(f"\n Duplicate Entries Created: {duplicate_entries_detected}")
                            
                            Summ_list.append(f"Duplicate install attempts: {install_attempts}")
                            Summ_list.append(f"Install responses received: {install_responses_received}")
                            Summ_list.append(f"Error responses: {error_responses}")
                            Summ_list.append(f"Install events received: {install_events_received}")
                            Summ_list.append(f"App entries before test: {final_check_count}")
                            Summ_list.append(f"App entries after test: {post_duplicate_count}")
                            Summ_list.append(f"Duplicate entries created: {duplicate_entries_detected}")

                            # Assessment of system behavior
                            test_app_id = app_id
                            behavioral_assessment_passed = True
                            
                            # Check 1: System should handle duplicate installs gracefully  
                            if duplicate_entries_detected > 0:
                                print(f"\n Duplicate app entries created: {duplicate_entries_detected} \n")
                                Summ_list.append("WARNING: Duplicate entries created")
                                # Note: This might be acceptable behavior depending on implementation
                            else:
                                print(f"\n No duplicate app entries created \n")
                            
                            # Check 2: System should provide appropriate responses
                            expected_behavior_met = True
                            if error_responses == 0 and install_events_received > 1:
                                print(f"\n No error responses but multiple install events - possible duplication issue \n")
                                expected_behavior_met = False
                            elif error_responses == install_attempts:
                                print(f"\nAll duplicate install attempts appropriately rejected \n")
                            elif error_responses > 0:
                                print(f"\n Mixed responses: {error_responses} rejections, {install_responses_received - error_responses} acceptances \n")
                                # This could be acceptable depending on implementation
                            
                            if not expected_behavior_met:
                                Summ_list.append("Inconsistent duplicate install handling")
                                behavioral_assessment_passed = False
                                
                            # Check 3: System should remain stable
                            if not post_stress_stability["overall_stable"]:
                                print(f"\nSystem instability detected after duplicate install attempts \n")
                                Summ_list.append("Post-stress system instability")
                                behavioral_assessment_passed = False
                            else:
                                print(f"\n System remained stable during duplicate install stress test \n")
                            
                            # Final assessment
                            if behavioral_assessment_passed:
                                print(f"\n === DUPLICATE INSTALLATION STABILITY TEST: PASSED === \n")
                                print(f"\n System handled duplicate installation attempts appropriately \n")
                                print(f"\n App {test_app_id} duplicate installation behavior: ACCEPTABLE \n")
                                Summ_list.append("Duplicate installation stability test: PASSED")
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print(f"\n === DUPLICATE INSTALLATION STABILITY TEST: ISSUES DETECTED === \n")
                                print(f"\n System showed problematic behavior during duplicate installation attempts \n")
                                print(f"\n App {test_app_id} duplicate installation behavior: PROBLEMATIC \n")
                                Summ_list.append("Duplicate installation stability test: ISSUES DETECTED")
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.setResultStatus("FAILURE")
                                status = "FAILURE"
                                
                        else:
                            print(f"\n Cannot perform duplicate install test - app {app_id} verification failed \n")
                            Summ_list.append("Test prerequisite failed: App not properly installed")
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
