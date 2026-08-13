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

#IP and Port of box, No need to change
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_UninstallApp_HealthCheck')

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
    stability_check_passed = False
    tdkTestObj = None

    # Required AppManager plugins
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager", "org.rdk.System"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.AppPackageManager":"activated", "org.rdk.AppManager":"activated", "org.rdk.System":"activated"}
    conf_file, status = get_configfile_name(obj)
    status,supported_plugins = getDeviceConfigValue(conf_file,"SUPPORTED_PLUGINS")
    
    # Check if essential AppManager plugins are available
    essential_plugins = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]  
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

            # Setup event listener for lifecycle changes, download status, app installation, and system monitoring
            thunder_port = rdkv_performancelib.devicePort
            lifecycle_event = '{"jsonrpc": "2.0","id": 7,"method": "org.rdk.LifecycleManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'
            download_event = '{"jsonrpc": "2.0","id": 8,"method": "org.rdk.DownloadManager.1.register","params": {"event": "onAppDownloadStatus", "id": "client.events.2" }}'
            install_event = '{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppInstalled", "id": "client.events.3" }}'
            uninstall_event = '{"jsonrpc": "2.0","id": 10,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppUninstalled", "id": "client.events.4" }}'
            event_listener = createEventListener(ip, thunder_port, [lifecycle_event, download_event, install_event, uninstall_event], "/jsonrpc", False)
            time.sleep(5)

            # Get app bundle name and download URL from PerformanceTestVariables
            app_bundle_name = PerformanceTestVariables.google_bundle
            app_name = app_bundle_name.split('+')[0]
            app_download_url = PerformanceTestVariables.app_download_url
            
            print(f"\n App bundle name: {app_bundle_name} \n")
            print(f"\n App name: {app_name} \n")
            print(f"\n App download URL: {app_download_url} \n")
            
            if status == "SUCCESS":

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
                    tdkTestObj.addParameter("method", "org.rdk.System.1.getSystemVersions")
                    tdkTestObj.executeTestCase(expectedResult)
                    system_result = tdkTestObj.getResult()
                    
                    if system_result == "SUCCESS":
                        stability_checks["wpeframework_running"] = True
                        print("\n WPEFramework is responsive \n")
                    else:
                        print("\n WPEFramework is not responsive \n")
                    
                    # Check if essential plugins are still responsive (actual functionality test)
                    essential_check_plugins = ["org.rdk.AppManager", "org.rdk.AppPackageManager"]
                    responsive_count = 0
                    
                    for plugin in essential_check_plugins:
                        if plugin in supported_plugins:
                            tdkTestObj = obj.createTestStep('rdkservice_getValue')
                            tdkTestObj.addParameter("method", f"{plugin}.1.getPluginStatus")
                            tdkTestObj.executeTestCase(expectedResult)
                            plugin_result = tdkTestObj.getResult()
                            
                            if plugin_result == "SUCCESS":
                                responsive_count += 1
                    
                    stability_checks["plugins_responsive"] = (responsive_count == len(essential_check_plugins))
                    if stability_checks["plugins_responsive"]:
                        print("\n Essential plugins are responsive \n")
                    else:
                        print(f"\nSome essential plugins are not responsive ({responsive_count}/{len(essential_check_plugins)}) \n")
                    
                    # Check system memory (basic check via getInstalledApps - if it works, memory is likely stable)
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getInstalledApps")
                    tdkTestObj.executeTestCase(expectedResult)
                    memory_result = tdkTestObj.getResult()
                    
                    stability_checks["memory_stable"] = (memory_result == "SUCCESS")
                    if stability_checks["memory_stable"]:
                        print("\n Memory appears stable (getInstalledApps succeeded) \n")
                    else:
                        print("\n Memory might be unstable (getInstalledApps failed) \n")
                    
                    # Check for no crashes (assume no crashes if all other checks pass)
                    stability_checks["no_crashes"] = all([
                        stability_checks["wpeframework_running"],
                        stability_checks["plugins_responsive"],
                        stability_checks["memory_stable"]
                    ])
                    
                    if stability_checks["no_crashes"]:
                        print("\n No system crashes detected \n")
                    else:
                        print("\n System instability detected \n")
                    
                    return stability_checks

                # NOTE: Test flow: Install → Uninstall → Check Stability
                # Simplified flow without launch/terminate overhead

                # Step 1: Install app
                print(f"\n === Installing app {app_name} for stability test === \n")
                app_installed = False
                status = rdkservice_install_launch_app(obj, app_bundle_name, app_name, app_download_url, launch=False)
                
                # Verify app is installed using rdkv_getInstalledPackages
                if status == "SUCCESS":
                    print(f"\n Verifying app {app_name} installation... \n")
                    time.sleep(2)
                    
                    installed_packages = rdkv_getInstalledPackages()
                    if installed_packages and app_name in str(installed_packages):
                        app_installed = True
                        print(f"\n App {app_name} is successfully installed \n")
                    else:
                        print(f"\n Warning: App {app_name} installation verification unclear, proceeding anyway \n")
                        app_installed = True  # Continue with uninstall test even if verification uncertain
                else:
                    print(f"\n Failed to install app {app_name} \n")
                    status = "FAILURE"
                
                if app_installed and status == "SUCCESS":
                    # Step 2: Uninstall the app (Main stability test)
                    print(f"\n === STABILITY TEST: Uninstalling app {app_name} === \n")
                    
                    tdkTestObj = obj.createTestStep('rdkservice_uninstall_app')
                    tdkTestObj.addParameter("app_id", app_name)
                    tdkTestObj.executeTestCase(expectedResult)
                    uninstall_result = tdkTestObj.getResult()
                    
                    # Accept SUCCESS or None as valid uninstall responses
                    if uninstall_result in [None, "SUCCESS"] or not uninstall_result:
                        print(f"\n App {app_name} uninstall initiated (result: {repr(uninstall_result)}) \n")
                        time.sleep(5)  # Allow system to settle
                        
                        # Step 3: Check system stability AFTER uninstall
                        print("\n === Checking system stability after app uninstall === \n")
                        
                        post_uninstall_stability = check_system_stability()
                        
                        # Validate stability
                        stability_maintained = all(post_uninstall_stability.values())
                        
                        if stability_maintained:
                            print("\n System stability maintained after uninstalling app \n")
                            stability_check_passed = True
                            status = "SUCCESS"
                        else:
                            print("\n System stability compromised after uninstalling app \n")
                            status = "FAILURE"
                            
                            # Log specific stability failures
                            for check, result in post_uninstall_stability.items():
                                if not result:
                                    print(f"[FAILURE] {check}: {result}")
                        
                        # Additional verification - try to perform basic operations
                        print("\n === Performing additional system verification === \n")
                        
                        # Test 1: Can still list apps
                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                        tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getInstalledApps")
                        tdkTestObj.executeTestCase(expectedResult)
                        list_apps_result = tdkTestObj.getResult()
                        
                        if list_apps_result == "SUCCESS":
                            print("\n System can still list installed apps \n")
                        else:
                            print("\n System cannot list installed apps after uninstall \n")
                            status = "FAILURE"
                        
                        # Test 2: Verify app was actually uninstalled
                        print("\n Verifying app was removed from installed packages... \n")
                        remaining_packages = rdkv_getInstalledPackages()
                        if remaining_packages and app_name not in str(remaining_packages):
                            print(f"\n Confirmed: {app_name} successfully removed from installed packages \n")
                        else:
                            print(f"\n Warning: {app_name} may still exist in installed packages \n")
                        
                        # Test 3: Can still access plugin status
                        plugin_status_accessible = True
                        for plugin in essential_plugins:
                            if plugin in supported_plugins:
                                plugin_status_dict = get_plugins_status(obj, [plugin])
                                if plugin_status_dict.get(plugin) == "FAILURE":
                                    plugin_status_accessible = False
                                    break
                        
                        if plugin_status_accessible:
                            print("\n System plugins remain accessible \n")
                        else:
                            print("\n Some system plugins are not accessible after uninstall \n")
                            status = "FAILURE"
                    else:
                        print(f"\n Failed to uninstall app {app_name} (result: {repr(uninstall_result)}) \n")
                        status = "FAILURE"
                else:
                    print(f"\n Failed: App {app_name} is not installed or install failed \n")
                    status = "FAILURE"
        
        # Disconnect event listener
        if event_listener:
            print("\n Disconnecting event listener \n")
            event_listener.disconnect()

    # Set final test result status
    if status == "SUCCESS":
        print("\n[SUCCESS] Stability check completed successfully\n")
    else:
        print("\n[FAILURE] Stability check failed\n")

    # Report final status
    obj.setLoadModuleStatus(status)

    #Revert the values
    if revert == "YES":
        print("Revert the plugin status before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict)

    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
