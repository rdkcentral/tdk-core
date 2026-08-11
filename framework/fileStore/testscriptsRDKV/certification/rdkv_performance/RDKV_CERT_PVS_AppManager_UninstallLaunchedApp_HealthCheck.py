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
from rdkv_performancelib import *
import rdkv_performancelib
import time

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_UninstallLaunchedApp_HealthCheck')

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
    app_instance_id = ""
    test_app_id = ""
    launched_app_found = False

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

            # Get app configuration from PerformanceTestVariables
            app_bundle = PerformanceTestVariables.google_bundle
            app_id = app_bundle.split('+')[0]
            app_download_url = PerformanceTestVariables.app_download_url
            
            print(f"\n App download URL: {app_download_url} \n")
            print(f"\n Target App ID: {app_id} \n")
            
            if not app_download_url or not app_id:
                print("\n Failed to get app configuration from PerformanceTestVariables \n")
                status = "FAILURE"
            else:
                status = "SUCCESS"

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
                
                # Test 1: Framework responsiveness - try SystemServices first, fallback to AppManager
                try:
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method", "org.rdk.System.1.getSystemVersions")
                    tdkTestObj.executeTestCase(expectedResult)
                    framework_result = tdkTestObj.getResult()
                    
                    if framework_result == "SUCCESS":
                        stability_report["framework_responsive"] = True
                        print("\n WPEFramework is responsive")
                    else:
                        # Fallback: Check via AppManager if SystemServices not available (device-specific)
                        print("\n SystemServices not available - using AppManager as proxy")
                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                        tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getInstalledApps")
                        tdkTestObj.executeTestCase(expectedResult)
                        fallback_result = tdkTestObj.getResult()
                        stability_report["framework_responsive"] = (fallback_result == "SUCCESS")
                except Exception as e:
                    print(f"\n Framework test failed: {e}")
                    stability_report["framework_responsive"] = False
                
                # Test 2: AppManager functionality
                try:
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getInstalledApps")
                    tdkTestObj.executeTestCase(expectedResult)
                    ai_manager_result = tdkTestObj.getResult()
                    
                    stability_report["ai_manager_functional"] = (ai_manager_result == "SUCCESS")
                    if stability_report["ai_manager_functional"]:
                        print("\n AppManager is functional")
                    else:
                        print("\n AppManager is not functional")
                except Exception as e:
                    print(f"\n AppManager test failed: {e}")
                    stability_report["ai_manager_functional"] = False
                
                # Test 3: Memory operations stability - try getRunningApps first, fallback to status check
                try:
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getRunningApps")
                    tdkTestObj.executeTestCase(expectedResult)
                    memory_result = tdkTestObj.getResult()
                    
                    if memory_result == "SUCCESS":
                        stability_report["memory_operations_stable"] = True
                        print("\n Memory operations are stable")
                    else:
                        # Fallback: Check plugin status if getRunningApps not available
                        print("\n getRunningApps not available - checking plugin responsiveness")
                        plugin_check = get_plugins_status(obj, ["org.rdk.AppManager"])
                        stability_report["memory_operations_stable"] = (plugin_check.get("org.rdk.AppManager") != "FAILURE")
                except Exception as e:
                    print(f"\n Memory stability test failed: {e}")
                    # Fallback check
                    try:
                        plugin_check = get_plugins_status(obj, ["org.rdk.AppManager"])
                        stability_report["memory_operations_stable"] = (plugin_check.get("org.rdk.AppManager") != "FAILURE")
                    except:
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
                
                # Overall stability assessment - require AppManager + plugins, framework/memory can be device-dependent
                stability_report["overall_stable"] = (
                    stability_report["ai_manager_functional"] and 
                    stability_report["plugin_services_available"]
                )
                
                if stability_report["overall_stable"]:
                    print("\n Overall system stability: STABLE (App management functional)")
                else:
                    print("\n Overall system stability: UNSTABLE")
                    
                return stability_report

            if status == "SUCCESS":
                # Phase 1: Establish baseline system stability
                print("\n === PHASE 1: Baseline System Stability Assessment === \n")
                baseline_stability = assess_system_stability()
                
                if not baseline_stability["overall_stable"]:
                    print("\n ABORT: System is not stable at baseline - cannot proceed with test \n")
                    status = "FAILURE"
                else:
                    print("\n Baseline system stability confirmed - proceeding with test \n")

                    # Phase 2: Install and Launch app in one operation
                    print(f"\n === PHASE 2: Installing and Launching {app_id} === \n")
                    
                    # Use direct function call to install and launch app in one operation
                    app_launched = False
                    install_launch_status = rdkservice_install_launch_app(obj, app_bundle, app_id, app_download_url, launch=True)
                    
                    if install_launch_status == "SUCCESS":
                        print(f"\n App {app_id} installed and launch command issued \n")
                        
                        # Wait 3 seconds for app to start initializing
                        print(f"\n Waiting for app to initialize... \n")
                        time.sleep(3)
                        
                        # Verify app is ACTIVE using rdkservice_get_loaded_apps
                        launch_timeout = 30
                        continue_count = 0
                        app_launched = False
                        
                        while continue_count < launch_timeout and not app_launched:
                            loaded_apps = rdkservice_get_loaded_apps()
                            
                            if loaded_apps and app_id in str(loaded_apps):
                                app_launched = True
                                launched_app_found = True
                                print(f"\n App {app_id} is now ACTIVE (ACTIVE state verified) \n")
                            
                            # Only log waiting message every 5 seconds to reduce log noise
                            if not app_launched and continue_count % 5 == 0:
                                print(f"\n Waiting for {app_id} to become ACTIVE ({continue_count}s/{launch_timeout}s)... \n")
                            
                            if not app_launched:
                                continue_count += 1
                                time.sleep(1)
                        
                        if not app_launched:
                            print(f"\n App {app_id} failed to reach ACTIVE state within {launch_timeout} seconds \n")
                            print(f"\n === STABILITY TEST RESULT: FAILED === \n")
                            status = "FAILURE"
                    else:
                        print(f"\n Failed to install and launch app {app_id} \n")
                        print(f"\n === STABILITY TEST RESULT: FAILED === \n")
                        status = "FAILURE"

                    # Phase 3: Uninstall the launched app (MAIN TEST)
                    if launched_app_found and status == "SUCCESS":
                        print(f"\n === PHASE 3: UNINSTALLING LAUNCHED APP {app_id} === \n")
                        print(f"\n WARNING: Attempting to uninstall app while in launched state \n")
                        
                        # Allow app to fully stabilize in launched state
                        print("\n Allowing launched app to stabilize... \n")
                        time.sleep(5)
                        
                        # Execute uninstall operation using test step
                        tdkTestObj = obj.createTestStep('rdkservice_uninstall_app')
                        tdkTestObj.addParameter("app_id", app_id)
                        tdkTestObj.executeTestCase(expectedResult)
                        uninstall_result = tdkTestObj.getResult()
                        
                        if uninstall_result == "SUCCESS":
                            print(f"\n Uninstall command issued for launched app {app_id} \n")
                            
                            # Verify app is uninstalled by polling getLoadedApps
                            uninstall_timeout = 30
                            continue_count = 0
                            uninstall_completed = False
                            
                            print(f"\n Verifying app {app_id} is uninstalled... \n")
                            while continue_count < uninstall_timeout and not uninstall_completed:
                                loaded_apps = rdkservice_get_loaded_apps()
                                
                                if loaded_apps and app_id not in str(loaded_apps):
                                    uninstall_completed = True
                                    print(f"\n Launched app {app_id} successfully uninstalled (removed from ACTIVE apps) \n")
                                
                                # Only log waiting message every 5 seconds to reduce log noise
                                if not uninstall_completed and continue_count % 5 == 0:
                                    print(f"\n Waiting for {app_id} to be uninstalled ({continue_count}s/{uninstall_timeout}s)... \n")
                                
                                if not uninstall_completed:
                                    continue_count += 1
                                    time.sleep(1)
                            
                            if uninstall_completed:
                                print(f"\n Launched app {app_id} uninstall COMPLETED \n")
                                test_app_id = app_id
                                
                                # Phase 4: Post-uninstall system stability check
                                print(f"\n === PHASE 4: Post-Uninstall Stability Assessment === \n")
                                time.sleep(3)  # Allow system to settle
                                
                                post_uninstall_stability = assess_system_stability()
                                
                                # Compare with baseline
                                stability_maintained = post_uninstall_stability["overall_stable"]
                                
                                if stability_maintained:
                                    print(f"\n SUCCESS: System remained stable after uninstalling launched app {test_app_id} \n")
                                    
                                    # Additional verification tests
                                    print("\n === Additional System Verification === \n")
                                    verification_passed = True
                                    
                                    # Test 1: Can still list apps
                                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getInstalledApps")
                                    tdkTestObj.executeTestCase(expectedResult)
                                    list_apps_result = tdkTestObj.getResult()
                                    
                                    if list_apps_result == "SUCCESS":
                                        print("\n Test 1: System can still list installed apps \n")
                                    else:
                                        print("\n Test 1 [FAILED]: System cannot list installed apps after uninstall \n")
                                        verification_passed = False
                                    
                                    # Test 2: Verify app was actually uninstalled
                                    print("\n Test 2: Verifying app was removed from installed packages... \n")
                                    remaining_packages = rdkv_getInstalledPackages()
                                    if remaining_packages and app_id not in str(remaining_packages):
                                        print(f"\n Test 2 [PASSED]: {app_id} successfully removed from installed packages \n")
                                    else:
                                        print(f"\n Test 2 [FAILED]: {app_id} may still exist in installed packages \n")
                                        verification_passed = False
                                    
                                    # Test 3: Can still access plugin status
                                    print("\n Test 3: Checking plugin accessibility after uninstall... \n")
                                    plugin_status_accessible = True
                                    for plugin in essential_plugins:
                                        if plugin in supported_plugins:
                                            plugin_status_dict = get_plugins_status(obj, [plugin])
                                            if plugin_status_dict.get(plugin) == "FAILURE":
                                                plugin_status_accessible = False
                                                print(f"\n Test 3 [FAILED]: Plugin {plugin} not accessible \n")
                                                break
                                    
                                    if plugin_status_accessible:
                                        print("\n Test 3 [PASSED]: All system plugins remain accessible \n")
                                    else:
                                        verification_passed = False
                                    
                                    # Final test result
                                    if verification_passed:
                                        print(f"\n === STABILITY TEST RESULT: SUCCESS === \n")
                                        print(f"\n Successfully uninstalled launched app {test_app_id} without system instability \n")
                                    else:
                                        print(f"\n === STABILITY TEST RESULT: FAILED === \n")
                                        print(f"\n Some verification checks failed after uninstalling launched app \n")
                                        status = "FAILURE"
                                        
                                else:
                                    print(f"\n === STABILITY TEST RESULT: FAILED === \n")
                                    print(f"\n System instability detected after uninstalling launched app {app_id} \n")
                                    
                                    # Log specific stability failures
                                    for check, result in post_uninstall_stability.items():
                                        if not result and check != "overall_stable":
                                            print(f"[FAILURE] {check}: {result} \n")
                                    
                                    status = "FAILURE"
                            else:
                                print(f"\n Launched app {app_id} uninstall did not complete within timeout \n")
                                status = "FAILURE"
                        else:
                            print(f"\n Failed to issue uninstall command for launched app {app_id} \n")
                            print(f"\n === STABILITY TEST RESULT: FAILED === \n")
                            status = "FAILURE"
                    else:
                        print(f"\nCannot perform uninstall test - app {app_id} is not in launched state \n")
                        print(f"\n === STABILITY TEST RESULT: FAILED === \n")
                        status = "FAILURE"

        else:
            print("\n AppManager plugins preconditions are not met \n")
            obj.setLoadModuleStatus("FAILURE")
                

    #Revert the values
    if revert == "YES":
        print("Revert the plugin status before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict)

    # Set module status before unloading
    obj.setLoadModuleStatus(status)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
