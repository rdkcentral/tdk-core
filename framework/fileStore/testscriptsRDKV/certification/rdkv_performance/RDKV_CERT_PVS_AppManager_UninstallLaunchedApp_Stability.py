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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_UninstallLaunchedApp_Stability')

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"no")


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
    launched_app_found = False

    # Required AppManager plugins
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager", "org.rdk.SystemServices"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.PackageManagerRDKEMS":"activated", "org.rdk.AppManager":"activated", "org.rdk.SystemServices":"activated"}
    conf_file, status = get_configfile_name(obj)
    status,supported_plugins = getDeviceConfigValue(conf_file,"SUPPORTED_PLUGINS")
    
    # Check if essential AppManager plugins are available
    essential_plugins = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager"]  
    missing_plugins = [plugin for plugin in essential_plugins if plugin not in supported_plugins]
    
    if missing_plugins:
        print(f"\n Essential AppManager plugins not available on this device: {missing_plugins}")
        print("\n This test requires AppManager functionality which is not supported on this device")
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
            print("\n Error while getting status of AppManager plugins")
            status = "FAILURE"
        elif curr_plugins_status_dict != plugin_status_needed:
            revert = "YES"
            status = set_plugins_status(obj,plugin_status_needed)
            time.sleep(10)
            new_plugins_status_dict = get_plugins_status(obj,plugins_list)
            if new_plugins_status_dict != plugin_status_needed:
                status = "FAILURE"
        else:
            print("\n AppManager plugins are already in the required state \n")

        if status == "SUCCESS":
            print("\n AppManager plugins are available and activated successfully \n")

            # Setup event listener for lifecycle changes, download status, app installation and uninstall
            thunder_port = rdkv_performancelib.devicePort
            lifecycle_event = '{"jsonrpc": "2.0","id": 7,"method": "org.rdk.LifecycleManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'
            download_event = '{"jsonrpc": "2.0","id": 8,"method": "org.rdk.DownloadManager.1.register","params": {"event": "onAppDownloadStatus", "id": "client.events.2" }}'
            install_event = '{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppInstalled", "id": "client.events.3" }}'
            uninstall_event = '{"jsonrpc": "2.0","id": 10,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppUninstalled", "id": "client.events.4" }}'
            event_listener = createEventListener(ip, thunder_port, [lifecycle_event, download_event, install_event, uninstall_event], "/jsonrpc", False)
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
                print(f"\n Target App ID: {app_id} \n")

                # Function to check system stability indicators
                def assess_system_stability():
                    print("\n === Assessing System Stability === \n")
                    stability_report = {
                        "framework_responsive": False,
                        "ai_manager_functional": False, 
                        "memory_operations_stable": False,
                        "plugin_services_available": False,
                        "overall_stable": False
                    }
                    
                    # Test 1: Framework responsiveness
                    try:
                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                        tdkTestObj.addParameter("method", "org.rdk.SystemServices.1.getSystemVersions")
                        tdkTestObj.addParameter("value", "{}")
                        tdkTestObj.executeTestCase(expectedResult)
                        framework_result = tdkTestObj.getResult()
                        
                        stability_report["framework_responsive"] = (framework_result == "SUCCESS")
                        if stability_report["framework_responsive"]:
                            print("\n WPEFramework is responsive")
                        else:
                            print("\n WPEFramework is not responsive")
                    except Exception as e:
                        print(f"\n Framework test failed: {e}")
                        stability_report["framework_responsive"] = False
                    
                    # Test 2: AppManager functionality
                    try:
                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                        tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getInstalledApps")
                        tdkTestObj.addParameter("value", "{}")
                        tdkTestObj.executeTestCase(expectedResult)
                        ai_manager_result = tdkTestObj.getResult()
                        
                        stability_report["ai_manager_functional"] = (ai_manager_result == "SUCCESS")
                        if stability_report["ai_manager_functional"]:
                            print("\n AppManager (AppManager) is functional")
                        else:
                            print("\n AppManager (AppManager) is not functional")
                    except Exception as e:
                        print(f"\n AppManager test failed: {e}")
                        stability_report["ai_manager_functional"] = False
                    
                    # Test 3: Memory operations stability (via running apps check)
                    try:
                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                        tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getRunningApps")
                        tdkTestObj.addParameter("value", "{}")
                        tdkTestObj.executeTestCase(expectedResult)
                        memory_result = tdkTestObj.getResult()
                        
                        stability_report["memory_operations_stable"] = (memory_result == "SUCCESS")
                        if stability_report["memory_operations_stable"]:
                            print("\n Memory operations are stable")
                        else:
                            print("\n Memory operations may be unstable")
                    except Exception as e:
                        print(f"\n Memory stability test failed: {e}")
                        stability_report["memory_operations_stable"] = False
                    
                    # Test 4: Plugin services availability
                    available_plugins = 0
                    for plugin in essential_plugins:
                        if plugin in supported_plugins:
                            plugin_check = get_plugins_status(obj, [plugin])
                            if plugin_check.get(plugin) != "FAILURE":
                                available_plugins += 1
                    
                    stability_report["plugin_services_available"] = (available_plugins == len(essential_plugins))
                    if stability_report["plugin_services_available"]:
                        print(f"\n All {len(essential_plugins)} essential plugin services are available")
                    else:
                        print(f"\n Only {available_plugins}/{len(essential_plugins)} plugin services are available")
                    
                    # Overall stability assessment
                    stability_report["overall_stable"] = all([
                        stability_report["framework_responsive"],
                        stability_report["ai_manager_functional"],
                        stability_report["memory_operations_stable"],
                        stability_report["plugin_services_available"]
                    ])
                    
                    if stability_report["overall_stable"]:
                        print("\n Overall system stability: STABLE")
                    else:
                        print("\n Overall system stability: UNSTABLE")
                        
                    return stability_report

                # Phase 1: Establish baseline system stability
                print("\n === PHASE 1: Baseline System Stability Assessment === \n")
                baseline_stability = assess_system_stability()
                
                if not baseline_stability["overall_stable"]:
                    print("\n ABORT: System is not stable at baseline - cannot proceed with test \n")
                    status = "FAILURE"
                else:
                    print("\n Baseline system stability confirmed - proceeding with test \n")

                    # Phase 2: Ensure app is installed and launched
                    print(f"\n === PHASE 2: Preparing {app_id} for Launch === \n")
                    
                    # Check if app is already installed
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
                        print(f"\n Installing {app_id}... \n")
                        
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
                                                break
                                        continue_count += 1
                                        time.sleep(1)
                    
                    # Phase 3: Launch the app
                    if app_installed and status == "SUCCESS":
                        print(f"\n === PHASE 3: Launching {app_id} === \n")
                        
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method", "org.rdk.AppManager.1.launchApp")
                        tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                        launch_start_time = str(datetime.utcnow()).split()[1]
                        tdkTestObj.executeTestCase(expectedResult)
                        launch_result = tdkTestObj.getResult()
                        
                        if launch_result == "SUCCESS":
                            print(f"\n Launch command issued for {app_id} \n")
                            
                            # Wait for app to enter launched state
                            launch_timeout = 120
                            continue_count = 0
                            app_launched = False
                            
                            while continue_count < launch_timeout and not app_launched:
                                if len(event_listener.getEventsBuffer()) > 0:
                                    event_log = event_listener.getEventsBuffer().pop(0)
                                    print(f"\n Launch event: {event_log} \n")
                                    
                                    if app_id in event_log and "onAppLifecycleStateChanged" in str(event_log):
                                        event_data = json.loads(event_log.split('$$$')[1])
                                        app_state = event_data.get("state", "").lower()
                                        
                                        if app_state in ["launched", "running", "started", "active"]:
                                            app_launched = True
                                            launched_app_found = True
                                            app_instance_id = event_data.get("instanceId", "")
                                            print(f"\n App {app_id} successfully launched (state: {app_state}) \n")
                                            break
                                
                                continue_count += 1
                                time.sleep(1)
                            
                            if not app_launched:
                                print(f"\n App {app_id} failed to reach launched state within timeout \n")
                                status = "FAILURE"
                        else:
                            print(f"\n Failed to issue launch command for {app_id} \n")
                            status = "FAILURE"
                    else:
                        print(f"\n App {app_id} is not installed - cannot proceed with launch \n")
                        status = "FAILURE"

                    # Phase 4: Uninstall the launched app (MAIN TEST)
                    if launched_app_found and status == "SUCCESS":
                        print(f"\n === PHASE 4: UNINSTALLING LAUNCHED APP {app_id} === \n")
                        print(f"\n WARNING: Attempting to uninstall app while in launched state \n")
                        
                        # Allow app to fully stabilize in launched state
                        print("\n Allowing launched app to stabilize... \n")
                        time.sleep(5)
                        
                        # Execute uninstall operation
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method", "org.rdk.PackageManagerRDKEMS.1.uninstall")
                        tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                        uninstall_start_time = str(datetime.utcnow()).split()[1]
                        tdkTestObj.executeTestCase(expectedResult)
                        uninstall_result = tdkTestObj.getResult()
                        
                        if uninstall_result == "SUCCESS":
                            print(f"\n Uninstall command issued for launched app {app_id} \n")
                            
                            # Monitor uninstall process
                            uninstall_timeout = 120
                            continue_count = 0
                            uninstall_completed = False
                            app_terminated = False
                            
                            while continue_count < uninstall_timeout and not uninstall_completed:
                                if len(event_listener.getEventsBuffer()) > 0:
                                    event_log = event_listener.getEventsBuffer().pop(0)
                                    print(f"\n Uninstall event: {event_log} \n")
                                    
                                    if app_id in event_log:
                                        if "onAppUninstalled" in str(event_log):
                                            uninstall_completed = True
                                            print(f"\n Launched app {app_id} successfully uninstalled \n")
                                            
                                        elif "onAppLifecycleStateChanged" in str(event_log):
                                            event_data = json.loads(event_log.split('$$$')[1])
                                            app_state = event_data.get("state", "").lower()
                                            
                                            if app_state in ["terminated", "stopped", "destroyed", "removed"]:
                                                app_terminated = True
                                                print(f"\n App {app_id} lifecycle changed to: {app_state} \n")
                                            elif app_state in ["uninstalled", "removed"]:
                                                uninstall_completed = True
                                
                                continue_count += 1
                                time.sleep(1)
                            
                            if uninstall_completed:
                                print(f"\n Launched app {app_id} uninstall COMPLETED \n")
                                test_app_id = app_id
                                
                                # Phase 5: Post-uninstall system stability check
                                print(f"\n === PHASE 5: Post-Uninstall Stability Assessment === \n")
                                time.sleep(3)  # Allow system to settle
                                
                                post_uninstall_stability = assess_system_stability()
                                
                                # Compare with baseline
                                stability_maintained = post_uninstall_stability["overall_stable"]
                                
                                if stability_maintained:
                                    print(f"\n SUCCESS: System remained stable after uninstalling launched app {test_app_id} \n")
                                    
                                    # Additional verification tests
                                    print("\n === Additional System Verification === \n")
                                    
                                    # Test: Can still install apps
                                    verification_passed = True
                                    
                                    # Verify app listing still works
                                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getInstalledApps")
                                    tdkTestObj.addParameter("value", "{}")
                                    tdkTestObj.executeTestCase(expectedResult)
                                    list_result = tdkTestObj.getResult()
                                    
                                    if list_result == "SUCCESS":
                                        print("\n App listing functionality verified \n")
                                        
                                        # Confirm target app is actually removed
                                        list_details = tdkTestObj.getResultDetails()
                                        try:
                                            list_data = json.loads(list_details)
                                            if "result" in list_data and "apps" in list_data["result"]:
                                                remaining_app_ids = [app.get("id", "") for app in list_data["result"]["apps"]]
                                                if app_id not in remaining_app_ids:
                                                    print(f"\n Confirmed: {app_id} successfully removed from installed apps \n")
                                                else:
                                                    print(f"\n Warning: {app_id} still appears in installed apps list \n")
                                                    verification_passed = False
                                        except json.JSONDecodeError:
                                            print("\n Could not verify app removal from installed list \n")
                                            verification_passed = False
                                    else:
                                        print("\nApp listing functionality compromised after uninstall \n")
                                        verification_passed = False
                                    
                                    # Final test result
                                    if verification_passed:
                                        print(f"\n === STABILITY TEST RESULT: PASSED === \n")
                                        print(f"\n Successfully uninstalled launched app {test_app_id} without system instability \n")
                                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print(f"\n === STABILITY TEST RESULT: PARTIAL === \n")
                                        print(f"\n App was uninstalled but some verification checks failed \n")
                                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                        tdkTestObj.setResultStatus("FAILURE")
                                        status = "FAILURE"
                                        
                                else:
                                    print(f"\n === STABILITY TEST RESULT: FAILED === \n")
                                    print(f"\n System instability detected after uninstalling launched app {app_id} \n")
                                    
                                    # Log specific stability failures
                                    for check, result in post_uninstall_stability.items():
                                        if not result and check != "overall_stable":
                                    
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                    tdkTestObj.setResultStatus("FAILURE")
                                    status = "FAILURE"
                                    
                            else:
                                print(f"\nLaunched app {app_id} uninstall did not complete within timeout \n")
                                if app_terminated:
                                    print(f"\n Note: App was terminated but uninstall event not confirmed \n")
                                else:
                                status = "FAILURE"
                        else:
                            print(f"\n Failed to issue uninstall command for launched app {app_id} \n")
                            status = "FAILURE"
                    else:
                        print(f"\nCannot perform uninstall test - app {app_id} is not in launched state \n")
                        status = "FAILURE"

            # Disconnect event listener
            if event_listener:
                print("\n Disconnecting event listener \n")
                event_listener.disconnect()

        else:
            print("\n AppManager plugins preconditions are not met \n")
            obj.setLoadModuleStatus("FAILURE")
                

    #Revert the values
    if revert == "YES":
        print("Revert the plugin status before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict)

    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
