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
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_AppManager_Verify_onAppInstalled_onAppUninstalled_Events');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
rebootwaitTime = StabilityTestVariables.rebootwaitTime
#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

if expectedResult in (result.upper() and pre_condition_status):
    status ="SUCCESS"
    print("\nCheck the status of AppManagers in the device")
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.AppPackageManager":"activated","org.rdk.AppManager":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        test_count = int(StabilityTestVariables.AppManager_test_count)
        app_bundle = PerformanceTestVariables.google_bundle
        app_name = "com.rdkcentral.google"
        app_download_url = PerformanceTestVariables.app_download_url + "/" + app_bundle
        thunder_port=rdkv_performancelib.devicePort
        payloads = []
        events = ['{"org.rdk.AppManager": "onAppInstalled"}','{"org.rdk.AppManager": "onAppUninstalled"}']
        for item in events:
            parsed_item = json.loads(item)
            for callsign, event_name in parsed_item.items():
                payload = '{"jsonrpc": "2.0","id": 1,"method": "'+callsign+'.1.register","params": {"event": "'+event_name+'", "id": "client.events.1" }}'
                payloads.append(payload)
        print("Event Registration List : ", payloads)
        event_listener = createEventListener(ip,thunder_port,payloads,"/jsonrpc",False)
        time.sleep(3)
        print(f"Check if {app_bundle} is already installed in the device")
        tdkTestObj = obj.createTestStep('rdkv_getInstalledPackages')
        tdkTestObj.executeTestCase(expectedResult)
        status = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        if status == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
            if app_name in details:
                uninstalled=False
                print(f"{app_name} is already installed in the device.")
                print(f"Uninstalling {app_name}")
                tdkTestObj = obj.createTestStep('rdkservice_uninstall_app')
                tdkTestObj.addParameter("app_id", app_name)
                tdkTestObj.executeTestCase(expectedResult)
                status = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails()
                print(f"uninstallation status {status}")
                if status == "SUCCESS":
                    print("Check for all events")
                    tdkTestObj.setResultStatus("SUCCESS")
                    continue_count = 0
                    event = ""
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
                            print("Event received")
                            print(f"Successfully uninstalled {app_name}")
                            uninstalled = True
                            break  
                else:
                    print(f"Iteration {iteration+1}: Failed to uninstall {app_name}")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print(f"{app_name} is not installed in the device")
                uninstalled = True       
            if uninstalled:
                for iteration in range(test_count):
                    print("ITERATION :", iteration + 1)
                    print("_________________")
                    install_event_count = 0
                    uninstall_event_count = 0
                    event_listener.clearEventsBuffer()
                    print(f"Start downloding {app_name} from {app_download_url}")
                    tdkTestObj = obj.createTestStep('rdkservice_download_app_bundle')
                    tdkTestObj.addParameter("download_url", app_download_url)
                    tdkTestObj.executeTestCase(expectedResult)
                    status = tdkTestObj.getResult()
                    details = tdkTestObj.getResultDetails()
                    if status == "SUCCESS":
                        time.sleep(10)
                        print("Successfully downloaded the app bundle")
                        tdkTestObj.setResultStatus("SUCCESS")
                        conf_file,result = getConfigFileName(obj.realpath)
                        fileLocator = ""
                        if result == "SUCCESS":
                            status,fileLocator = getDeviceConfigKeyValue(conf_file,"PACKAGEMANAGER_FILE_LOCATOR")
                        if fileLocator != "":
                            fileLocator = fileLocator + str(details)
                            print (fileLocator)
                            event_listener.clearEventsBuffer()
                            tdkTestObj = obj.createTestStep('rdkservice_install_app')
                            tdkTestObj.addParameter("fileLocator", fileLocator)
                            tdkTestObj.addParameter("app_id", app_name)
                            tdkTestObj.executeTestCase(expectedResult)
                            status = tdkTestObj.getResult()
                            details = tdkTestObj.getResultDetails()
                            if status == "SUCCESS":
                                print("Check for installation events")
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
                                    if "onAppInstalled" in event and app_name in event:
                                        event_buffer = True
                                        install_event_count = install_event_count + 1
                                        
                                if install_event_count == 1:
                                    print("Successfully received installation event")
                                    print(f"Checking {app_bundle} is installed in the device")
                                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                    tdkTestObj.addParameter("method","org.rdk.AppPackageManager.1.listPackages")
                                    tdkTestObj.executeTestCase(expectedResult)
                                    status = tdkTestObj.getResult()
                                    result = ast.literal_eval(tdkTestObj.getResultDetails())
                                    print(f"Result of installed :{result}")
                                    if status == "SUCCESS": 
                                        uninstall_event_count = 0    
                                        print(f"Uninstalling package for iteration {iteration + 1}")
                                        tdkTestObj = obj.createTestStep('rdkservice_uninstall_app')
                                        tdkTestObj.addParameter("app_id", app_name)
                                        tdkTestObj.executeTestCase(expectedResult)
                                        status = tdkTestObj.getResult()
                                        details = tdkTestObj.getResultDetails()
                                        if status == "SUCCESS":
                                            print("Check for uninstallation events")
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
                                                    uninstall_event_count = uninstall_event_count + 1
                                                    
                                            if uninstall_event_count == 1:
                                                print(f"Successfully uninstalled {app_name}")
                                                print(f"Check if {app_bundle} is already installed in the device")
                                                tdkTestObj = obj.createTestStep('rdkv_getInstalledPackages')
                                                tdkTestObj.executeTestCase(expectedResult)
                                                status = tdkTestObj.getResult()
                                                details = tdkTestObj.getResultDetails()
                                                if status == "SUCCESS":
                                                    if app_name not in details:
                                                        print("Verification completed. App has been uninstalled successfully")
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                    else:
                                                        print(f"Iteration {iteration+1}: Stale package entry still present after uninstall")
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        break
                                                else:
                                                    print(f"Iteration {iteration+1}: Failed to retrieve package list\n")
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    break
                                            elif install_event_count > 1:
                                                print(f"Iteration {iteration+1}: Duplicated event received for onAppUninstalled")
                                                tdkTestObj.setResultStatus("FAILURE")
                                                break
                                            else:
                                                print(f"Iteration {iteration+1}: Failed to receive uninstallation event")
                                                tdkTestObj.setResultStatus("FAILURE")
                                                break        
                                        else:
                                            print(f"Iteration {iteration+1}: Failed to uninstall {app_name}")
                                            tdkTestObj.setResultStatus("FAILURE")
                                            break     
                                    else:
                                        print(f"Iteration {iteration+1}: Failed to retrieve package list\n")
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                                elif install_event_count > 1:
                                    print(f"Iteration {iteration+1}: Duplicated event received for ")
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                                else:
                                    print(f"Iteration {iteration+1}: Failed to receive installation event")
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            else:
                                print(f"Iteration {iteration+1}: Failed to trigger package installation")
                                tdkTestObj.setResultStatus("FAILURE")
                                break    
                        else:
                            print(f"Iteration {iteration+1}: Failed to retrieve file locator")
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print(f"Iteration {iteration+1}: Failed to download the app bundle")
                        tdkTestObj.setResultStatus("FAILURE")
                        break          
            else:
                print(f"Iteration {iteration+1}: Failed to uninstall the app")
                tdkTestObj.setResultStatus("FAILURE")
                
        else:
            print(f"Iteration {iteration+1}: Failed to retrieve package list\n")
            tdkTestObj.setResultStatus("FAILURE")
        event_listener.disconnect()     
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")