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
import time
import json
import StabilityTestUtility
from StabilityTestUtility import *
import PerformanceTestVariables
from web_socket_util import *
import rdkv_performancelib
import StabilityTestVariables

obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_AppManager_Install_Uninstall_AppStates');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

if expectedResult in result.upper() and expectedResult in pre_condition_status:
    status ="SUCCESS"
    print("\nCheck the status of AppManagers in the device")
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.AppPackageManager":"activated","org.rdk.AppManager":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    else:
        status = "SUCCESS"
    if status == "SUCCESS":
        test_count = int(StabilityTestVariables.AppManager_test_count)
        app_bundle = PerformanceTestVariables.google_bundle
        app_name = "com.rdkcentral.google"
        app_download_url = PerformanceTestVariables.app_download_url
        thunder_port = rdkv_performancelib.devicePort

        callsign = "org.rdk.AppManager"
        event_name = "onAppUninstalled"
        payload = '{"jsonrpc": "2.0","id": 1,"method": "'+callsign+'.1.register","params": {"event": "'+event_name+'", "id": "client.events.1" }}'

        event_listener = createEventListener(ip,thunder_port,[payload],"/jsonrpc",False)
        time.sleep(3)

        status = rdkservice_install_launch_app(obj, app_bundle, app_name, app_download_url, launch=False)
        installed = status == "SUCCESS"

        if installed:
            for iteration in range(test_count):
                print("ITERATION :", iteration + 1)
                print("_____________________________________")
                event_listener.clearEventsBuffer()

                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                tdkTestObj.addParameter("method", "org.rdk.AppManager.getInstalledApps")
                tdkTestObj.executeTestCase(expectedResult)
                status = tdkTestObj.getResult()
                installed_apps_before_launch = tdkTestObj.getResultDetails()
                if status == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                    print("Installed apps before launching the app:", installed_apps_before_launch)
                    print("Checking if the app is installed before launching")
                    tdkTestObj = obj.createTestStep('rdkservice_getValueWithParams')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.isInstalled")
                    tdkTestObj.addParameter("params", '{"appId": "'+app_name+'"}')
                    tdkTestObj.executeTestCase(expectedResult)
                    status = tdkTestObj.getResult()
                    is_installed_before_launch = tdkTestObj.getResultDetails()
                    print("Status of isInstalled check:", status)
                    if status == "SUCCESS":
                        print("isInstalled result before launching the app:", is_installed_before_launch)
                        tdkTestObj.setResultStatus("SUCCESS")
                        time.sleep(5)
                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                        tdkTestObj.addParameter("method", "org.rdk.AppManager.getLoadedApps")
                        tdkTestObj.executeTestCase(expectedResult)
                        status = tdkTestObj.getResult()
                        loaded_apps_before_launch = tdkTestObj.getResultDetails()
                        if status == "SUCCESS":
                            print("Loaded apps before launching the app:", loaded_apps_before_launch)
                            tdkTestObj.setResultStatus("SUCCESS")
                            tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                            tdkTestObj.addParameter("app_name", app_name)
                            tdkTestObj.executeTestCase(expectedResult)
                            status = tdkTestObj.getResult()
                            details = tdkTestObj.getResultDetails()
                            if status == "SUCCESS":
                                tdkTestObj.setResultStatus("SUCCESS")
                                time.sleep(5)
                                print("Successfully launched the app")
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.addParameter("method", "org.rdk.AppManager.terminateApp")
                                tdkTestObj.addParameter("value", '{"appId": "'+app_name+'"}')
                                tdkTestObj.executeTestCase(expectedResult)
                                status = tdkTestObj.getResult()
                                details = tdkTestObj.getResultDetails()
                                if status == "SUCCESS":
                                    time.sleep(10)
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print("Successfully terminated the app")
                                    tdkTestObj = obj.createTestStep('rdkservice_uninstall_app')
                                    tdkTestObj.addParameter("app_id", app_name)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    status = tdkTestObj.getResult()
                                    details = tdkTestObj.getResultDetails()
                                    if status == "SUCCESS":
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print("Successfully uninstalled the app")
                                        continue_count = 0
                                        event = ""
                                        event_buffer = False
                                        while True:
                                            if continue_count > 120:
                                                break
                                            if len(event_listener.getEventsBuffer()) == 0:
                                                time.sleep(1)
                                                continue_count += 1
                                                continue
                                            event = event_listener.getEventsBuffer().pop(0)
                                            print("\nEvent:", event)
                                            if "onAppUninstalled" in event and app_name in event:
                                                event_buffer = True
                                                print("Event received from AppManager event listener")
                                                break
                                        if event_buffer:
                                            print("Event buffer received from AppManager events")
                                            tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                            tdkTestObj.addParameter("method", "org.rdk.AppManager.getInstalledApps")
                                            tdkTestObj.executeTestCase(expectedResult)
                                            status = tdkTestObj.getResult()
                                            installed_apps_after_uninstall = tdkTestObj.getResultDetails()
                                            if status == "SUCCESS":
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                tdkTestObj = obj.createTestStep('rdkservice_getValueWithParams')
                                                tdkTestObj.addParameter("method", "org.rdk.AppManager.isInstalled")
                                                tdkTestObj.addParameter("params", '{"appId": "'+app_name+'"}')
                                                tdkTestObj.executeTestCase(expectedResult)
                                                status = tdkTestObj.getResult()
                                                is_installed_after_uninstall = tdkTestObj.getResultDetails()
                                                if status == "SUCCESS":
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                                    tdkTestObj.addParameter("method", "org.rdk.AppManager.getLoadedApps")
                                                    tdkTestObj.executeTestCase(expectedResult)
                                                    status = tdkTestObj.getResult()
                                                    loaded_apps_after_uninstall = tdkTestObj.getResultDetails()
                                                    if status == "SUCCESS":
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        initial_installed = app_name in str(installed_apps_before_launch)
                                                        initial_isinstalled = "true" in str(is_installed_before_launch).lower()
                                                        initial_loaded = app_name in str(loaded_apps_before_launch)
                                                        final_installed = app_name in str(installed_apps_after_uninstall)
                                                        final_isinstalled = "true" in str(is_installed_after_uninstall).lower()
                                                        final_loaded = app_name in str(loaded_apps_after_uninstall)
                                                        uninstall_event = "onAppUninstalled" in str(event) and app_name in str(event)
                                                        #Installed list, isInstalled and loaded list must agree with each other and with the event stream
                                                        initial_consistent = initial_installed and initial_isinstalled and not initial_loaded
                                                        final_consistent = not final_installed and not final_isinstalled and not final_loaded
                                                        if initial_consistent and final_consistent and uninstall_event:
                                                            print("App state results and event stream are consistent across query surfaces")
                                                            #Reinstall the app so it is available for the next iteration
                                                            status = rdkservice_install_launch_app(obj, app_bundle, app_name, app_download_url, launch=False)
                                                            if status != "SUCCESS":
                                                                print("Failed to reinstall the app for the next iteration")
                                                                break
                                                        else:
                                                            print("App state results and event stream diverged across query surfaces")
                                                            print("initial_installed=%s initial_isinstalled=%s initial_loaded=%s final_installed=%s final_isinstalled=%s final_loaded=%s uninstall_event=%s" % (initial_installed, initial_isinstalled, initial_loaded, final_installed, final_isinstalled, final_loaded, uninstall_event))
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                            break
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        print("Failed to fetch loaded app list for consistency check")
                                                        break
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    print("Failed to fetch isInstalled state for consistency check")
                                                    break
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print("Failed to fetch installed app list for consistency check")
                                                break
                                        else:
                                            print("Failed to receive AppManager install/uninstall event")
                                            tdkTestObj.setResultStatus("FAILURE")
                                            break
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print("Failed to uninstall the app")
                                        break
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print("Failed to terminate the app")
                                    break
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print("Failed to launch the app")
                                break
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print("Failed to get loaded apps")
                            break
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("Failed to get isInstalled result")
                        break
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("Failed to get installed apps")
                    break
        else:
            print("The app is not available for the app state and event consistency flow")
            obj.setLoadModuleStatus("FAILURE")

        event_listener.disconnect()
    else:
        print("The AppManager plugins are not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_stability")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
