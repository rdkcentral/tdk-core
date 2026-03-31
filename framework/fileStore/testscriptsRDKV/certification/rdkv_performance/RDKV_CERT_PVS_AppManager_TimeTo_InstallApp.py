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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeTo_InstallApp')

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

    # Required AppManager plugins
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.PackageManagerRDKEMS":"activated", "org.rdk.AppManager":"activated"}
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
                    print(f"\n App ID to install: {app_id} \n")

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
                                    print(f"\n Installation timing test is not applicable - app already exists \n")
                                else:
                                    print(f"\n App {app_id} is not installed, proceeding with installation timing test \n")
                            else:
                                print(f"\n Could not parse installed apps list, assuming app {app_id} is not installed \n")
                        except json.JSONDecodeError:
                            print(f"\n Error parsing installed apps response, assuming app {app_id} is not installed \n")
                    else:
                        print(f"\n Failed to get installed apps list, assuming app {app_id} is not installed \n")
                    
                    if app_already_installed:
                        # App is already installed - installation timing test not applicable
                        print(f"\n Test Result: App {app_id} is already installed on the device \n")
                        print(f"\n Installation timing measurement is not applicable for pre-installed apps \n")
                        
                        Summ_list.append(f'App {app_id} is already installed')
                        Summ_list.append('Installation timing test not applicable')
                        Summ_list.append('Test completed successfully - app pre-exists')
                        
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.setResultStatus("SUCCESS")
                        status = "SUCCESS"
                        # App not installed - proceed with installation timing test
                        # Use individual TDK test steps to download and install app
                        download_timeout = 120  # 2 minutes
                        install_timeout = 120   # 2 minutes
                        
                        # Initialize results dictionary
                        results_dict = {
                            "download_time": 0,
                            "install_time": 0,
                            "app_instance_id": "",
                            "download_success": False,
                            "install_success": False
                        }
                        
                        # Step 1: Download the app
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
                                
                                # Step 2: Install the downloaded app (Main focus of this test)
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
                                        status = "SUCCESS"
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
                        
                        if status == "SUCCESS" and results_dict["install_success"]:
                            app_instance_id = results_dict["app_instance_id"]
                            test_app_id = app_id
                            time_taken_for_install = results_dict["install_time"]
                            
                            print(f"\n Download Time: {results_dict['download_time']}ms \n")
                            print(f"\n Install Time: {time_taken_for_install}ms \n")
                            
                            Summ_list.append(f'Time taken to download app: {results_dict["download_time"]}ms')
                            Summ_list.append(f'Time taken to install app: {time_taken_for_install}ms')

                            # Validate performance against thresholds manually like Cobalt script
                            config_status, app_install_threshold = getDeviceConfigKeyValue(conf_file, "APP_INSTALL_THRESHOLD_VALUE")
                            offset_status, offset = getDeviceConfigKeyValue(conf_file, "THRESHOLD_OFFSET")
                            
                            Summ_list.append('APP_INSTALL_THRESHOLD_VALUE: {}ms'.format(app_install_threshold))
                            Summ_list.append('THRESHOLD_OFFSET: {}ms'.format(offset))
                            
                            if all(value != "" for value in (app_install_threshold, offset)):
                                print(f"\n Threshold value for time taken to install app: {app_install_threshold} ms")
                                print("\n Validate the time: \n")
                                
                                if 0 < time_taken_for_install < (int(app_install_threshold) + int(offset)):
                                    print(f"\n Time taken for installing {test_app_id} is within the expected range \n")
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print(f"\n Time taken for installing {test_app_id} is not within the expected range \n")
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print("\n Please configure the APP_INSTALL_THRESHOLD_VALUE in device configuration file \n")
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print(f"\n Download/Install operation failed for app {app_id} \n")
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.setResultStatus("FAILURE")

                # Disconnect event listener
                if event_listener:
                    print("\n Disconnecting event listener \n")
                    event_listener.disconnect()

        else:
            print("\n AppManager plugins preconditions are not met \n")
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
