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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeToLaunch_InstalledApp')

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

            # Setup event listener for lifecycle changes, download status, and app installation at the beginning
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
                print(f"\n App ID to launch: {app_id} \n")

                # Step 0: Check if app is already installed
                print(f"\n Checking if app {app_id} is already installed... \n")
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
                            if app_id in installed_app_ids:
                                app_already_installed = True
                                print(f"\n App {app_id} is already installed \n")
                            else:
                                print(f"\n App {app_id} is not installed, will download and install first \n")
                        else:
                            print(f"\n Could not parse installed apps list, assuming app {app_id} is not installed \n")
                    except json.JSONDecodeError:
                        print(f"\n Error parsing installed apps response, assuming app {app_id} is not installed \n")
                else:
                    print(f"\n Failed to get installed apps list, assuming app {app_id} is not installed \n")

            # Use individual TDK test steps to download, install and launch app
            download_timeout = 120  # 2 minutes
            install_timeout = 120   # 2 minutes  
            launch_timeout = 120    # 2 minutes
            
            # Initialize results dictionary
            results_dict = {
                "download_time": 0,
                "install_time": 0, 
                "launch_time": 0,
                "app_instance_id": "",
                "download_success": False,
                "install_success": False,
                "launch_success": False
            }
            
            # Step 1: Download and Install app if not already installed
            if not app_already_installed:
                # Step 1a: Download the app
                print(f"\n Starting app download for {app_id}... \n")
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method", "org.rdk.DownloadManager.1.download")
                tdkTestObj.addParameter("value", '{"url": "' + app_download_url + '", "appId": "' + app_id + '"}')
                download_start_time = str(datetime.utcnow()).split()[1]
                tdkTestObj.executeTestCase(expectedResult)
                download_result = tdkTestObj.getResult()
                
                if download_result == "SUCCESS":
                    print(f"\n Download initiated successfully for {app_id} \n")
                    
                    # Wait for download completion
                    continue_count = 0
                    downloaded_time = ""
                    download_success = False
                    
                    while continue_count < download_timeout:
                        if len(event_listener.getEventsBuffer()) == 0:
                            continue_count += 1
                            time.sleep(1)
                            continue
                            
                        event_log = event_listener.getEventsBuffer().pop(0)
                        print(f"\n Download event: {event_log} \n")
                        
                        if app_id in event_log and "onAppDownloadStatus" in str(event_log):
                            event_data = json.loads(event_log.split('$$$')[1])
                            if event_data.get("status") == "Downloaded":
                                print(f"\n App {app_id} downloaded successfully \n")
                                downloaded_time = event_log.split('$$$')[0]
                                download_success = True
                                break
                            elif event_data.get("status") in ["Failed", "Error"]:
                                print(f"\n App {app_id} download failed \n")
                                break
                    
                    if downloaded_time and download_success:
                        download_start_time_in_millisec = getTimeInMilliSec(download_start_time)
                        downloaded_time_in_millisec = getTimeInMilliSec(downloaded_time)
                        download_time_taken = downloaded_time_in_millisec - download_start_time_in_millisec
                        results_dict["download_time"] = download_time_taken
                        results_dict["download_success"] = True
                        print(f"\n App download completed successfully in {download_time_taken}ms \n")
                        
                        # Step 1b: Install the downloaded app
                        print(f"\n Starting app installation for {app_id}... \n")
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method", "org.rdk.PackageManagerRDKEMS.1.install")
                        tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                        install_start_time = str(datetime.utcnow()).split()[1]
                        tdkTestObj.executeTestCase(expectedResult)
                        install_result = tdkTestObj.getResult()
                        
                        if install_result == "SUCCESS":
                            print(f"\n Installation initiated successfully for {app_id} \n")
                            
                            # Wait for installation completion
                            continue_count = 0
                            installed_time = ""
                            install_success = False
                            
                            while continue_count < install_timeout:
                                if len(event_listener.getEventsBuffer()) == 0:
                                    continue_count += 1
                                    time.sleep(1)
                                    continue
                                    
                                event_log = event_listener.getEventsBuffer().pop(0)
                                print(f"\n Install event: {event_log} \n")
                                
                                if app_id in event_log and "onAppInstalled" in str(event_log):
                                    print(f"\n Event: onAppInstalled triggered for {app_id} \n")
                                    installed_time = event_log.split('$$$')[0]
                                    event_data = json.loads(event_log.split('$$$')[1])
                                    app_instance_id = event_data.get("instanceId", "")
                                    install_success = True
                                    break
                                    
                            if installed_time and install_success:
                                install_start_time_in_millisec = getTimeInMilliSec(install_start_time)
                                installed_time_in_millisec = getTimeInMilliSec(installed_time)
                                install_time_taken = installed_time_in_millisec - install_start_time_in_millisec
                                results_dict["install_time"] = install_time_taken
                                results_dict["install_success"] = True
                                results_dict["app_instance_id"] = app_instance_id
                                print(f"\n App installation completed successfully in {install_time_taken}ms \n")
                            else:
                                print(f"\n App installation event not received or installation failed for {app_id} \n")
                                tdkTestObj.setResultStatus("FAILURE")
                                status = "FAILURE"
                        else:
                            print(f"\n Failed to initiate installation for {app_id} \n")
                            tdkTestObj.setResultStatus("FAILURE")
                            status = "FAILURE"
                    else:
                        print(f"\n App download event not received or download failed for {app_id} \n")
                        tdkTestObj.setResultStatus("FAILURE")
                        status = "FAILURE"
                else:
                    print(f"\n Failed to initiate download for {app_id} \n")
                    tdkTestObj.setResultStatus("FAILURE")
                    status = "FAILURE"
            else:
                print(f"\n App {app_id} is already installed, skipping download and install steps \n")
                results_dict["download_success"] = True  # Skip download
                results_dict["install_success"] = True   # Skip install
            
            # Step 2: Launch the installed app (either freshly installed or already existing)
            if status == "SUCCESS":
            print(f"\n Starting app download for {app_id}... \n")
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method", "org.rdk.DownloadManager.1.download")
            tdkTestObj.addParameter("value", '{"url": "' + app_download_url + '", "appId": "' + app_id + '"}')
            download_start_time = str(datetime.utcnow()).split()[1]
            tdkTestObj.executeTestCase(expectedResult)
            download_result = tdkTestObj.getResult()
            
            if download_result == "SUCCESS":
                print(f"\n Download initiated successfully for {app_id} \n")
                
                # Wait for download completion
                continue_count = 0
                downloaded_time = ""
                download_success = False
                
                while continue_count < download_timeout:
                    if len(event_listener.getEventsBuffer()) == 0:
                        continue_count += 1
                        time.sleep(1)
                        continue
                        
                    event_log = event_listener.getEventsBuffer().pop(0)
                    print(f"\n Download event: {event_log} \n")
                    
                    if app_id in event_log and "onAppDownloadStatus" in str(event_log):
                        event_data = json.loads(event_log.split('$$$')[1])
                        if event_data.get("status") == "Downloaded":
                            print(f"\n App {app_id} downloaded successfully \n")
                            downloaded_time = event_log.split('$$$')[0]
                            download_success = True
                            break
                        elif event_data.get("status") in ["Failed", "Error"]:
                            print(f"\n App {app_id} download failed \n")
                            break
                
                if downloaded_time and download_success:
                    download_start_time_in_millisec = getTimeInMilliSec(download_start_time)
                    downloaded_time_in_millisec = getTimeInMilliSec(downloaded_time)
                    download_time_taken = downloaded_time_in_millisec - download_start_time_in_millisec
                    results_dict["download_time"] = download_time_taken
                    results_dict["download_success"] = True
                    print(f"\n App download completed successfully in {download_time_taken}ms \n")
                    
                    # Step 2: Install the downloaded app
                    print(f"\n Starting app installation for {app_id}... \n")
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method", "org.rdk.PackageManagerRDKEMS.1.install")
                    tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                    install_start_time = str(datetime.utcnow()).split()[1]
                    tdkTestObj.executeTestCase(expectedResult)
                    install_result = tdkTestObj.getResult()
                    
                    if install_result == "SUCCESS":
                        print(f"\n Installation initiated successfully for {app_id} \n")
                        
                        # Wait for installation completion
                        continue_count = 0
                        installed_time = ""
                        install_success = False
                        
                        while continue_count < install_timeout:
                            if len(event_listener.getEventsBuffer()) == 0:
                                continue_count += 1
                                time.sleep(1)
                                continue
                                
                            event_log = event_listener.getEventsBuffer().pop(0)
                            print(f"\n Install event: {event_log} \n")
                            
                            if app_id in event_log and "onAppInstalled" in str(event_log):
                                print(f"\n Event: onAppInstalled triggered for {app_id} \n")
                                installed_time = event_log.split('$$$')[0]
                                event_data = json.loads(event_log.split('$$$')[1])
                                app_instance_id = event_data.get("instanceId", "")
                                install_success = True
                                break
                                
                        if installed_time and install_success:
                            install_start_time_in_millisec = getTimeInMilliSec(install_start_time)
                            installed_time_in_millisec = getTimeInMilliSec(installed_time)
                            install_time_taken = installed_time_in_millisec - install_start_time_in_millisec
                            results_dict["install_time"] = install_time_taken
                            results_dict["install_success"] = True
                            results_dict["app_instance_id"] = app_instance_id
                            print(f"\n App installation completed successfully in {install_time_taken}ms \n")
                            
                            # Step 3: Launch the installed app
                            print(f"\n Starting app launch for {app_id}... \n")
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method", "org.rdk.AppManager.1.launchApp")
                            tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                            launch_start_time = str(datetime.utcnow()).split()[1]
                            tdkTestObj.executeTestCase(expectedResult)
                            launch_result = tdkTestObj.getResult()
                            
                            if launch_result == "SUCCESS":
                                print(f"\n Launch initiated successfully for {app_id} \n")
                                
                                # Wait for launch completion (using lifecycle events)
                                continue_count = 0
                                launched_time = ""
                                launch_success = False
                                
                                while continue_count < launch_timeout:
                                    if len(event_listener.getEventsBuffer()) == 0:
                                        continue_count += 1
                                        time.sleep(1) 
                                        continue
                                        
                                    event_log = event_listener.getEventsBuffer().pop(0)
                                    print(f"\n Launch event: {event_log} \n")
                                    
                                    if app_id in event_log and "onAppLifecycleStateChanged" in str(event_log):
                                        event_data = json.loads(event_log.split('$$$')[1])
                                        if event_data.get("state") == "running":
                                            print(f"\n Event: App lifecycle changed to running for {app_id} \n")
                                            launched_time = event_log.split('$$$')[0]
                                            launch_success = True
                                            break
                                            
                                if launched_time and launch_success:
                                    launch_start_time_in_millisec = getTimeInMilliSec(launch_start_time)
                                    launched_time_in_millisec = getTimeInMilliSec(launched_time)
                                    launch_time_taken = launched_time_in_millisec - launch_start_time_in_millisec
                                    results_dict["launch_time"] = launch_time_taken
                                    results_dict["launch_success"] = True
                                    status = "SUCCESS"
                                    print(f"\n App launch completed successfully in {launch_time_taken}ms \n")
                                else:
                                    print(f"\n App launch event not received or launch failed for {app_id} \n")
                                    tdkTestObj.setResultStatus("FAILURE")
                                    status = "FAILURE"
                            else:
                                print(f"\n Failed to initiate launch for {app_id} \n")
                                tdkTestObj.setResultStatus("FAILURE")
                                status = "FAILURE"
                        else:
                            print(f"\n App installation event not received or installation failed for {app_id} \n")
                            tdkTestObj.setResultStatus("FAILURE")
                            status = "FAILURE"
                    else:
                        print(f"\n Failed to initiate installation for {app_id} \n")
                        tdkTestObj.setResultStatus("FAILURE")
                        status = "FAILURE"
                else:
                    print(f"\n App download event not received or download failed for {app_id} \n")
                    tdkTestObj.setResultStatus("FAILURE")
                    status = "FAILURE"
            else:
                print(f"\n Failed to initiate download for {app_id} \n")
                tdkTestObj.setResultStatus("FAILURE")
                status = "FAILURE"
            
            if status == "SUCCESS" and results_dict["launch_success"]:
                app_instance_id = results_dict["app_instance_id"]
                test_app_id = app_id
                time_taken_for_launch = results_dict["launch_time"]
                
                print(f"\n Download Time: {results_dict['download_time']}ms \n")
                print(f"\n Install Time: {results_dict['install_time']}ms \n")
                print(f"\n Launch Time: {time_taken_for_launch}ms \n")
                
                Summ_list.append(f'Time taken to launch app: {time_taken_for_launch}ms')
                
                # Add download and install times to summary only if operations were performed
                if results_dict["download_time"] > 0:
                    Summ_list.append(f'Time taken to download app: {results_dict["download_time"]}ms')
                if results_dict["install_time"] > 0:
                    Summ_list.append(f'Time taken to install app: {results_dict["install_time"]}ms')

                # Validate performance against thresholds manually like Cobalt script
                config_status, app_launch_threshold = getDeviceConfigKeyValue(conf_file, "APP_LAUNCH_THRESHOLD_VALUE")
                offset_status, offset = getDeviceConfigKeyValue(conf_file, "THRESHOLD_OFFSET")
                
                Summ_list.append('APP_LAUNCH_THRESHOLD_VALUE: {}ms'.format(app_launch_threshold))
                Summ_list.append('THRESHOLD_OFFSET: {}ms'.format(offset))
                
                if all(value != "" for value in (app_launch_threshold, offset)):
                    print(f"\n Threshold value for time taken to launch app: {app_launch_threshold} ms")
                    print("\n Validate the time: \n")
                    
                    if 0 < time_taken_for_launch < (int(app_launch_threshold) + int(offset)):
                        print(f"\n Time taken for launching {test_app_id} is within the expected range \n")
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print(f"\n Time taken for launching {test_app_id} is not within the expected range \n")
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("\n Please configure the APP_LAUNCH_THRESHOLD_VALUE in device configuration file \n")
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.setResultStatus("FAILURE")
                
                # Terminate the launched app using TDK test step
                if app_instance_id:
                    print(f"\n Terminating app {test_app_id} \n")
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.terminateApp")
                    tdkTestObj.addParameter("value", '{"appId": "' + test_app_id + '"}')
                    tdkTestObj.executeTestCase(expectedResult)
                    terminate_result = tdkTestObj.getResult()
                    if terminate_result == "SUCCESS":
                        print("App termination initiated successfully")
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("Unable to terminate app")
                        tdkTestObj.setResultStatus("FAILURE")
            else:
                print(f"\n Download/Install/Launch operation failed for app {app_id} \n")
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.setResultStatus("FAILURE")

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
