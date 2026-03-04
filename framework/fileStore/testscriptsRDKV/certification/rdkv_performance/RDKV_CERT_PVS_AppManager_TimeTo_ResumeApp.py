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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeTo_ResumeApp')

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
                print(f"\n App ID for resume test: {app_id} \n")

                # Use TDK test steps for complete app lifecycle management
                download_timeout = 120  # 2 minutes
                install_timeout = 120   # 2 minutes
                launch_timeout = 120    # 2 minutes
                suspend_timeout = 60    # 1 minute
                resume_timeout = 60     # 1 minute
                
                # Initialize results dictionary
                results_dict = {
                    "download_time": 0,
                    "install_time": 0,
                    "launch_time": 0,
                    "suspend_time": 0,
                    "resume_time": 0,
                    "app_instance_id": "",
                    "download_success": False,
                    "install_success": False,
                    "launch_success": False,
                    "suspend_success": False,
                    "resume_success": False
                }

                # Step 0: Check current app status (installed, running, suspended)
                print(f"\n Checking current status of app {app_id}... \n")
                
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
                        
                # Check if app is running
                app_running = False
                app_suspended = False
                if app_installed:
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.getRunningApps") 
                    tdkTestObj.addParameter("value", "{}")
                    tdkTestObj.executeTestCase(expectedResult)
                    running_apps_result = tdkTestObj.getResult()
                    running_apps_details = tdkTestObj.getResultDetails()
                    
                    if running_apps_result == "SUCCESS":
                        try:
                            running_apps_data = json.loads(running_apps_details)
                            if "result" in running_apps_data and "apps" in running_apps_data["result"]:
                                for running_app in running_apps_data["result"]["apps"]:
                                    if running_app.get("id") == app_id:
                                        app_running = True
                                        app_state = running_app.get("state", "").lower()
                                        if app_state in ["suspended", "paused"]:
                                            app_suspended = True
                                        break
                        except json.JSONDecodeError:
                            print(f"\n Error parsing running apps response \n")

                print(f"\n App Status - Installed: {app_installed}, Running: {app_running}, Suspended: {app_suspended} \n")

                # Step 1: Install app if not installed (prerequisite)
                if not app_installed:
                    print(f"\n App {app_id} not installed, downloading and installing as prerequisite... \n")
                    
                    # Download app
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method", "org.rdk.DownloadManager.1.download")
                    tdkTestObj.addParameter("value", '{"url": "' + app_download_url + '", "appId": "' + app_id + '"}')
                    download_start_time = str(datetime.utcnow()).split()[1]
                    tdkTestObj.executeTestCase(expectedResult)
                    download_result = tdkTestObj.getResult()
                    
                    if download_result == "SUCCESS":
                        # Wait for download completion
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
                                    results_dict["download_success"] = True
                                    break
                                    
                        if download_success:
                            # Install app
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method", "org.rdk.PackageManagerRDKEMS.1.install")
                            tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                            tdkTestObj.executeTestCase(expectedResult)
                            install_result = tdkTestObj.getResult()
                            
                            if install_result == "SUCCESS":
                                # Wait for installation completion
                                continue_count = 0
                                install_success = False
                                
                                while continue_count < install_timeout:
                                    if len(event_listener.getEventsBuffer()) == 0:
                                        continue_count += 1
                                        time.sleep(1)
                                        continue
                                        
                                    event_log = event_listener.getEventsBuffer().pop(0)
                                    if app_id in event_log and "onAppInstalled" in str(event_log):
                                        install_success = True
                                        results_dict["install_success"] = True
                                        break
                                        
                                if not install_success:
                                    print(f"\n Failed to install app {app_id} \n")
                                    status = "FAILURE"
                            else:
                                print(f"\n Failed to initiate installation for {app_id} \n")
                                status = "FAILURE"
                        else:
                            print(f"\n Failed to download app {app_id} \n")
                            status = "FAILURE"
                    else:
                        print(f"\n Failed to initiate download for {app_id} \n")
                        status = "FAILURE"

                # Step 2: Launch app if not running (prerequisite)
                if status == "SUCCESS" and not app_running:
                    print(f"\n App {app_id} not running, launching as prerequisite... \n")
                    
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.launchApp")
                    tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                    launch_start_time = str(datetime.utcnow()).split()[1]
                    tdkTestObj.executeTestCase(expectedResult)
                    launch_result = tdkTestObj.getResult()
                    
                    if launch_result == "SUCCESS":
                        # Wait for launch completion
                        continue_count = 0
                        launch_success = False
                        
                        while continue_count < launch_timeout:
                            if len(event_listener.getEventsBuffer()) == 0:
                                continue_count += 1
                                time.sleep(1)
                                continue
                                
                            event_log = event_listener.getEventsBuffer().pop(0)
                            if app_id in event_log and "onAppLifecycleStateChanged" in str(event_log):
                                event_data = json.loads(event_log.split('$$$')[1])
                                if event_data.get("state", "").lower() in ["running", "launched", "started"]:
                                    launch_success = True
                                    results_dict["launch_success"] = True
                                    app_instance_id = event_data.get("instanceId", "")
                                    break
                                    
                        if not launch_success:
                            print(f"\n Failed to launch app {app_id} \n")
                            status = "FAILURE"
                    else:
                        print(f"\n Failed to initiate launch for {app_id} \n")
                        status = "FAILURE"

                # Step 3: Suspend app if not already suspended (prerequisite)
                if status == "SUCCESS" and not app_suspended:
                    print(f"\n App {app_id} not suspended, suspending as prerequisite... \n")
                    
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.suspendApp")
                    tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                    suspend_start_time = str(datetime.utcnow()).split()[1]
                    tdkTestObj.executeTestCase(expectedResult)
                    suspend_result = tdkTestObj.getResult()
                    
                    if suspend_result == "SUCCESS":
                        # Wait for suspend completion
                        continue_count = 0
                        suspend_success = False
                        
                        while continue_count < suspend_timeout:
                            if len(event_listener.getEventsBuffer()) == 0:
                                continue_count += 1
                                time.sleep(1)
                                continue
                                
                            event_log = event_listener.getEventsBuffer().pop(0)
                            if app_id in event_log and "onAppLifecycleStateChanged" in str(event_log):
                                event_data = json.loads(event_log.split('$$$')[1])
                                if event_data.get("state", "").lower() in ["suspended", "paused"]:
                                    suspend_success = True
                                    results_dict["suspend_success"] = True
                                    break
                                    
                        if not suspend_success:
                            print(f"\n Failed to suspend app {app_id} \n")
                            status = "FAILURE"
                    else:
                        print(f"\n Failed to initiate suspend for {app_id} \n")
                        status = "FAILURE"
                
                # Step 4: Resume the app (Main focus of this test)
                if status == "SUCCESS":
                    print(f"\n Starting app resume for {app_id}... \n")
                    
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.1.resumeApp")
                    tdkTestObj.addParameter("value", '{"appId": "' + app_id + '"}')
                    resume_start_time = str(datetime.utcnow()).split()[1]
                    tdkTestObj.executeTestCase(expectedResult)
                    resume_result = tdkTestObj.getResult()
                    
                    if resume_result == "SUCCESS":
                        print(f"\n Resume initiated successfully for {app_id} \n")
                        
                        # Wait for resume completion
                        continue_count = 0
                        resumed_time = ""
                        resume_success = False
                        
                        while continue_count < resume_timeout:
                            if len(event_listener.getEventsBuffer()) == 0:
                                continue_count += 1
                                time.sleep(1)
                                continue
                                
                            event_log = event_listener.getEventsBuffer().pop(0)
                            print(f"\n Resume event: {event_log} \n")
                            
                            if app_id in event_log and "onAppLifecycleStateChanged" in str(event_log):
                                event_data = json.loads(event_log.split('$$$')[1])
                                app_state = event_data.get("state", "").lower()
                                
                                if app_state in ["running", "resumed", "active", "started"]:
                                    print(f"\n Event: App lifecycle changed to {app_state} for {app_id} \n")
                                    resumed_time = event_log.split('$$$')[0]
                                    resume_success = True
                                    break
                                    
                        if resumed_time and resume_success:
                            resume_start_time_in_millisec = getTimeInMilliSec(resume_start_time)
                            resumed_time_in_millisec = getTimeInMilliSec(resumed_time)
                            resume_time_taken = resumed_time_in_millisec - resume_start_time_in_millisec
                            results_dict["resume_time"] = resume_time_taken
                            results_dict["resume_success"] = True
                            status = "SUCCESS"
                            print(f"\n App resume completed successfully in {resume_time_taken}ms \n")
                        else:
                            print(f"\n App resume event not received or resume failed for {app_id} \n")
                            tdkTestObj.setResultStatus("FAILURE")
                            status = "FAILURE"
                    else:
                        print(f"\n Failed to initiate resume for {app_id} \n")
                        tdkTestObj.setResultStatus("FAILURE")
                        status = "FAILURE"
                
                if status == "SUCCESS" and results_dict["resume_success"]:
                    test_app_id = app_id
                    time_taken_for_resume = results_dict["resume_time"]
                    
                    print(f"\n Resume Time: {time_taken_for_resume}ms \n")
                    
                    Summ_list.append(f'Time taken to resume app: {time_taken_for_resume}ms')
                    
                    # Add prerequisite operation times to summary if performed
                    if results_dict["download_time"] > 0:
                        print(f"\n Download Time (prerequisite): {results_dict['download_time']}ms \n")
                        Summ_list.append(f'Time taken to download app (prerequisite): {results_dict["download_time"]}ms')
                    
                    if results_dict["install_time"] > 0:
                        print(f"\n Install Time (prerequisite): {results_dict['install_time']}ms \n")
                        Summ_list.append(f'Time taken to install app (prerequisite): {results_dict["install_time"]}ms')
                        
                    if results_dict["launch_time"] > 0:
                        print(f"\n Launch Time (prerequisite): {results_dict['launch_time']}ms \n")
                        Summ_list.append(f'Time taken to launch app (prerequisite): {results_dict["launch_time"]}ms')
                        
                    if results_dict["suspend_time"] > 0:
                        print(f"\n Suspend Time (prerequisite): {results_dict['suspend_time']}ms \n")
                        Summ_list.append(f'Time taken to suspend app (prerequisite): {results_dict["suspend_time"]}ms')

                    # Validate performance against thresholds
                    config_status, app_resume_threshold = getDeviceConfigKeyValue(conf_file, "APP_RESUME_THRESHOLD_VALUE")
                    offset_status, offset = getDeviceConfigKeyValue(conf_file, "THRESHOLD_OFFSET")
                    
                    Summ_list.append('APP_RESUME_THRESHOLD_VALUE: {}ms'.format(app_resume_threshold))
                    Summ_list.append('THRESHOLD_OFFSET: {}ms'.format(offset))
                    
                    if all(value != "" for value in (app_resume_threshold, offset)):
                        print(f"\n Threshold value for time taken to resume app: {app_resume_threshold} ms")
                        print("\n Validate the time: \n")
                        
                        if 0 < time_taken_for_resume < (int(app_resume_threshold) + int(offset)):
                            print(f"\n Time taken for resuming {test_app_id} is within the expected range \n")
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print(f"\n Time taken for resuming {test_app_id} is not within the expected range \n")
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print("\n Please configure the APP_RESUME_THRESHOLD_VALUE in device configuration file \n")
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print(f"\n Resume operation failed for app {app_id} \n")
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
