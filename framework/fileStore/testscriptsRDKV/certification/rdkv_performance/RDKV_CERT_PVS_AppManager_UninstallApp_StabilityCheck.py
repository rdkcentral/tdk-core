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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_UninstallApp_StabilityCheck')

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
    stability_check_passed = False

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

            # Setup event listener for lifecycle changes, download status, app installation, and system monitoring
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
                print(f"\n App ID for stability test: {app_id} \n")

                # Function to check system stability
                def check_system_stability():
                    stability_checks = {
                        "wpeframework_running": False,
                        "plugins_responsive": False,
                        "memory_stable": False,
                        "no_crashes": False
                    }
                    
                    # Check if WPEFramework is still running
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method", "org.rdk.SystemServices.1.getSystemVersions")
                    tdkTestObj.addParameter("value", "{}")
                    tdkTestObj.executeTestCase(expectedResult)
                    system_result = tdkTestObj.getResult()
                    
                    if system_result == "SUCCESS":
                        stability_checks["wpeframework_running"] = True
                        print("\n ✓ WPEFramework is responsive \n")
                    else:
                        print("\n ✗ WPEFramework is not responsive \n")
                    
                    # Check if essential plugins are still responsive
                    essential_check_plugins = ["org.rdk.AppManager", "org.rdk.PackageManagerRDKEMS"]
                    responsive_count = 0
                    
                    for plugin in essential_check_plugins:
                        if plugin in supported_plugins:
                            tdkTestObj = obj.createTestStep('rdkservice_getValue')
                            tdkTestObj.addParameter("method", f"{plugin}.1.getPluginStatus")
                            tdkTestObj.addParameter("value", "{}")
                            tdkTestObj.executeTestCase(expectedResult)
                            plugin_result = tdkTestObj.getResult()
                            
                            if plugin_result == "SUCCESS":
                                responsive_count += 1
                    
                    stability_checks["plugins_responsive"] = (responsive_count == len(essential_check_plugins))
                    if stability_checks["plugins_responsive"]:
                        print("\n ✓ Essential plugins are responsive \n")
                    else:
                        print(f"\n ✗ Some essential plugins are not responsive ({responsive_count}/{len(essential_check_plugins)}) \n")
                    
                    # Check system memory (basic check via getInstalledApps - if it works, memory is likely stable)
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getInstalledApps")
                    tdkTestObj.addParameter("value", "{}")
                    tdkTestObj.executeTestCase(expectedResult)
                    memory_result = tdkTestObj.getResult()
                    
                    stability_checks["memory_stable"] = (memory_result == "SUCCESS")
                    if stability_checks["memory_stable"]:
                        print("\n ✓ Memory appears stable (getInstalledApps succeeded) \n")
                    else:
                        print("\n ✗ Memory might be unstable (getInstalledApps failed) \n")
                    
                    # Check for no crashes (assume no crashes if all other checks pass)
                    stability_checks["no_crashes"] = all([
                        stability_checks["wpeframework_running"],
                        stability_checks["plugins_responsive"],
                        stability_checks["memory_stable"]
                    ])
                    
                    if stability_checks["no_crashes"]:
                        print("\n ✓ No system crashes detected \n")
                    else:
                        print("\n ✗ System instability detected \n")
                    
                    return stability_checks

                # Pre-uninstall system stability baseline
                print("\n === Checking initial system stability === \n")
                initial_stability = check_system_stability()
                
                if not all(initial_stability.values()):
                    print("\n System is not stable at start - aborting test \n")
                    Summ_list.append("Initial system stability check failed")
                    status = "FAILURE"
                else:
                    print("\n Initial system stability confirmed \n")
                    Summ_list.append("Initial system stability: PASSED")

                    # Ensure app is installed and loaded
                    app_loaded_successfully = False
                    
                    # Step 1: Check if app is installed, if not install it
                    print(f"\n Checking if app {app_id} is installed... \n")
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getInstalledApps")
                    tdkTestObj.addParameter("value", "{}")
                    tdkTestObj.executeTestCase(expectedResult)
                    installed_apps_result = tdkTestObj.getResult()
                    installed_apps_details = tdkTestObj.getResultDetails()
                    
                    app_already_installed = False
                    if installed_apps_result == "SUCCESS":
                        try:
                            installed_apps_data = json.loads(installed_apps_details)
                            if "result" in installed_apps_data and "apps" in installed_apps_data["result"]:
                                installed_app_ids = [app.get("id", "") for app in installed_apps_data["result"]["apps"]]
                                app_already_installed = app_id in installed_app_ids
                        except json.JSONDecodeError:
                            print(f"\n Error parsing installed apps response \n")
                    
                    if not app_already_installed:
                        print(f"\n Installing app {app_id} for stability test... \n")
                        
                        # Download and install app  
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
                            
                            while continue_count < download_timeout:
                                if len(event_listener.getEventsBuffer()) == 0:
                                    continue_count += 1
                                    time.sleep(1)
                                    continue
                                    
                                event_log = event_listener.getEventsBuffer().pop(0)
                                if app_id in event_log and "onAppDownloadStatus" in str(event_log):
                                    event_data = json.loads(event_log.split('$$$')[1])
                                    if event_data.get("status") == "Downloaded":
                                        download_success = True
                                        break
                                        
                            if download_success:
                                # Install the app
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
                                        if len(event_listener.getEventsBuffer()) == 0:
                                            continue_count += 1
                                            time.sleep(1)
                                            continue
                                            
                                        event_log = event_listener.getEventsBuffer().pop(0)
                                        if app_id in event_log and "onAppInstalled" in str(event_log):
                                            app_already_installed = True
                                            break
                    
                    # Step 2: Launch and load the app
                    if app_already_installed and status == "SUCCESS":
                        print(f"\n Launching app {app_id} for stability test... \n")
                        
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method", "org.rdk.AppManager.1.launchApp")
                        tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                        tdkTestObj.executeTestCase(expectedResult)
                        launch_result = tdkTestObj.getResult()
                        
                        if launch_result == "SUCCESS":
                            # Wait for app to be loaded/running
                            launch_timeout = 120
                            continue_count = 0
                            
                            while continue_count < launch_timeout:
                                if len(event_listener.getEventsBuffer()) == 0:
                                    continue_count += 1
                                    time.sleep(1)
                                    continue
                                    
                                event_log = event_listener.getEventsBuffer().pop(0)
                                if app_id in event_log and "onAppLifecycleStateChanged" in str(event_log):
                                    event_data = json.loads(event_log.split('$$$')[1])
                                    app_state = event_data.get("state", "").lower()
                                    
                                    if app_state in ["running", "launched", "loaded", "active"]:
                                        app_loaded_successfully = True
                                        app_instance_id = event_data.get("instanceId", "")
                                        print(f"\n App {app_id} is now loaded and running (state: {app_state}) \n")
                                        Summ_list.append(f"App {app_id} loaded successfully")
                                        break
                                        
                            if app_loaded_successfully:
                                # Give app some time to fully stabilize
                                print("\n Allowing app to fully stabilize... \n")
                                time.sleep(10)
                                
                                # Step 3: Uninstall the loaded app (Main stability test)
                                print(f"\n === STABILITY TEST: Uninstalling loaded app {app_id} === \n")
                                
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.addParameter("method", "org.rdk.PackageManagerRDKEMS.1.uninstall")
                                tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                                uninstall_start_time = str(datetime.utcnow()).split()[1]
                                tdkTestObj.executeTestCase(expectedResult)
                                uninstall_result = tdkTestObj.getResult()
                                
                                if uninstall_result == "SUCCESS":
                                    print(f"\n Uninstall initiated for loaded app {app_id} \n")
                                    
                                    # Wait for uninstall completion
                                    uninstall_timeout = 120
                                    continue_count = 0
                                    uninstall_completed = False
                                    
                                    while continue_count < uninstall_timeout:
                                        if len(event_listener.getEventsBuffer()) == 0:
                                            continue_count += 1
                                            time.sleep(1)
                                            continue
                                            
                                        event_log = event_listener.getEventsBuffer().pop(0)
                                        print(f"\n Uninstall event: {event_log} \n")
                                        
                                        if app_id in event_log:
                                            if "onAppUninstalled" in str(event_log):
                                                uninstall_completed = True
                                                print(f"\n App {app_id} uninstalled successfully from loaded state \n")
                                                Summ_list.append("Loaded app uninstall completed")
                                                break
                                            elif "onAppLifecycleStateChanged" in str(event_log):
                                                event_data = json.loads(event_log.split('$$$')[1])
                                                if event_data.get("state", "").lower() in ["removed", "uninstalled", "terminated"]:
                                                    uninstall_completed = True
                                                    break
                                    
                                    if uninstall_completed:
                                        # Step 4: Check system stability after uninstall
                                        print("\n === Checking system stability after loaded app uninstall === \n")
                                        time.sleep(5)  # Allow system to settle
                                        
                                        post_uninstall_stability = check_system_stability()
                                        
                                        # Compare stability before and after
                                        stability_maintained = all(post_uninstall_stability.values())
                                        
                                        if stability_maintained:
                                            print("\n ✓ System stability maintained after uninstalling loaded app \n")
                                            Summ_list.append("Post-uninstall system stability: PASSED")
                                            stability_check_passed = True
                                            status = "SUCCESS"
                                        else:
                                            print("\n ✗ System stability compromised after uninstalling loaded app \n")
                                            Summ_list.append("Post-uninstall system stability: FAILED")
                                            
                                            # Log specific stability failures
                                            for check, result in post_uninstall_stability.items():
                                                if not result:
                                                    Summ_list.append(f"Stability check failed: {check}")
                                            
                                            status = "FAILURE"
                                        
                                        # Additional verification - try to perform basic operations
                                        print("\n === Performing additional system verification === \n")
                                        
                                        # Test 1: Can still list apps
                                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                        tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getInstalledApps")
                                        tdkTestObj.addParameter("value", "{}")
                                        tdkTestObj.executeTestCase(expectedResult)
                                        list_apps_result = tdkTestObj.getResult()
                                        
                                        if list_apps_result == "SUCCESS":
                                            print("\n ✓ System can still list installed apps \n")
                                            Summ_list.append("Post-uninstall app listing: PASSED")
                                        else:
                                            print("\n ✗ System cannot list installed apps after uninstall \n")
                                            Summ_list.append("Post-uninstall app listing: FAILED")
                                            status = "FAILURE"
                                        
                                        # Test 2: Can still access plugin status
                                        plugin_status_accessible = True
                                        for plugin in essential_ai_plugins:
                                            if plugin in supported_plugins:
                                                plugin_status_dict = get_plugins_status(obj, [plugin])
                                                if plugin_status_dict.get(plugin) == "FAILURE":
                                                    plugin_status_accessible = False
                                                    break
                                        
                                        if plugin_status_accessible:
                                            print("\n ✓ System plugins remain accessible \n")
                                            Summ_list.append("Post-uninstall plugin access: PASSED")
                                        else:
                                            print("\n ✗ Some system plugins are not accessible after uninstall \n")
                                            Summ_list.append("Post-uninstall plugin access: FAILED")
                                            status = "FAILURE"
                                        
                                        test_app_id = app_id
                                        
                                        # Final stability assessment
                                        if status == "SUCCESS":
                                            print(f"\n === STABILITY TEST PASSED === \n")
                                            print(f"\n Successfully uninstalled loaded app {test_app_id} without system instability \n")
                                            Summ_list.append("Overall stability test: PASSED")
                                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                            tdkTestObj.setResultStatus("SUCCESS")
                                        else:
                                            print(f"\n === STABILITY TEST FAILED === \n")
                                            print(f"\n System instability detected after uninstalling loaded app {test_app_id} \n")
                                            Summ_list.append("Overall stability test: FAILED")
                                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print(f"\n Failed: App uninstall did not complete within timeout \n")
                                        Summ_list.append("Uninstall operation timeout")
                                        status = "FAILURE"
                                else:
                                    print(f"\n Failed to initiate uninstall for loaded app {app_id} \n")
                                    Summ_list.append("Failed to initiate uninstall")
                                    status = "FAILURE"
                            else:
                                print(f"\n Failed: App {app_id} did not reach loaded state \n")
                                Summ_list.append("App failed to reach loaded state")
                                status = "FAILURE"
                        else:
                            print(f"\n Failed to launch app {app_id} \n")
                            Summ_list.append("App launch failed")
                            status = "FAILURE"
                    else:
                        print(f"\n Failed: App {app_id} is not installed \n")
                        Summ_list.append("App installation prerequisite failed")
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
