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
import json
import ast
import shlex

obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_AppManager_Download_InvalidURL');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    status ="SUCCESS"
    package_size = 10
    print("\nCheck the status of AppManagers in the device")
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.PackageManagerRDKEMS":"activated","org.rdk.AppManager":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        conf_file,_ = getConfigFileName(obj.realpath)
        config_status,file_locator = getDeviceConfigKeyValue(conf_file,"PACKAGEMANAGER_FILE_LOCATOR")
        file_locator,_ = file_locator.split("/CDL")
        print("File locator URL from the configuration is : ", file_locator)
        ssh_params = rdkv_performancelib.rdkservice_getSSHParams(obj.realpath, ip)
        if ssh_params == "" or ssh_params == "{}":
            raise Exception("Failed to get SSH parameters from configuration")
        
        ssh_params_dict = json.loads(ssh_params)
        ssh_method = ssh_params_dict.get("ssh_method")
        credentials = ssh_params_dict.get("credentials")
        
        if not ssh_method or not credentials:
            raise Exception("SSH method or credentials not found in configuration")        
        print("DownloadManager is in active state")
        print("Register for the Download event")
        thunder_port = rdkv_performancelib.devicePort
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 2,"method": "org.rdk.DownloadManager.1.register","params": {"event": "onAppDownloadStatus", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(5)
        test_count = StabilityTestVariables.AppManager_test_count
        app_bundle_name = PerformanceTestVariables.google_bundle
        valid_app_download_url = PerformanceTestVariables.app_download_url + app_bundle_name
        failing_app_download_url = PerformanceTestVariables.invalid_app_download_url + app_bundle_name
        
        for iteration in range(test_count):
            print(f"\n################################# Iteration {iteration + 1} #################################")
            event_listener.clearEventsBuffer()
            print("------Attempting to download package from an invalid URL------")
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method", "org.rdk.DownloadManager.1.download")
            tdkTestObj.addParameter("value", json.dumps({"url": failing_app_download_url}))
            tdkTestObj.executeTestCase(expectedResult)
            time.sleep(5)
            failure_status = tdkTestObj.getResult()
            failure_details = tdkTestObj.getResultDetails()
            if failure_status != "SUCCESS":
                continue_count = 0
                while True:
                    if continue_count > 120:
                        break
                    if len(event_listener.getEventsBuffer()) == 0:
                        time.sleep(1)
                        continue_count += 1
                        continue
                    event = event_listener.getEventsBuffer().pop(0)
                    print("\nEvent:", event)
                    break
                if "onAppDownloadStatus" in str(event) and "DOWNLOAD_FAILURE" in str(event):
                    print("Received Download Failure event")
                    event_listener.clearEventsBuffer()
                    print("------Attempting to download package from a valid URL------")
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method", "org.rdk.DownloadManager.1.download")
                    tdkTestObj.addParameter("value", json.dumps({"url": valid_app_download_url}))
                    tdkTestObj.executeTestCase(expectedResult)
                    status = tdkTestObj.getResult()
                    result = tdkTestObj.getResultDetails()
                    if status == "SUCCESS":
                        download_id = ast.literal_eval(result)
                        print("Checking for download event")
                        continue_count = 0
                        while True:
                            if continue_count > 120:
                                break
                            if len(event_listener.getEventsBuffer()) == 0:
                                time.sleep(1)
                                continue_count += 1
                                continue
                            event = event_listener.getEventsBuffer().pop(0)
                            print("\nEvent:", event)
                            break
                        if "onAppDownloadStatus" in str(event) and "DOWNLOAD_FAILURE" not in str(event):
                            _, json_part = event.split("$$$", 1)
                            json_part = json_part.encode().decode("unicode_escape")
                            outer = json.loads(json_part)
                            inner = json.loads(outer["params"]["downloadStatus"])
                            event_download_id = inner[0]["downloadId"]
                            filelocator_url = inner[0]["fileLocator"]
                            print(f"Download ID from the event is : {event_download_id}")
                            if ( int(event_download_id) == download_id and event_download_id in filelocator_url):
                                print("SUCCESS : Package download successful with correct download status")
                                print("Delete the downloaded package from the device")
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.addParameter("method", "org.rdk.DownloadManager.delete")
                                tdkTestObj.addParameter("value", '{"fileLocator": "' + filelocator_url + '"}')
                                tdkTestObj.executeTestCase(expectedResult)
                                status = tdkTestObj.getResult()
                                if status == "SUCCESS":
                                    cmd = "ls -l " + shlex.quote(filelocator_url)
                                    output = rdkv_performancelib.rdkservice_getRequiredLog(ssh_method, credentials, cmd)
                                    print("ls output:\n", output)
                                    if ("No such file or directory" in output) or ("cannot access" in output.lower()):
                                        print("Verification passed: package not found on DUT")
                                        print("Successfully deleted the downloaded package from the device")
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print(f"Iteration {iteration+1}: Verification failed: package still exists on DUT. ls output:\n", output)
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                                else:
                                    print(f"Iteration {iteration+1}: Failed to delete the downloaded package from the device")
                                    tdkTestObj.setResultStatus("FAILURE")   
                                    break 
                            else:
                                print(f"Iteration {iteration+1}: Failed to download package with download ID :{download_id}")
                                tdkTestObj.setResultStatus("FAILURE") 
                        else:
                            print(f"Iteration {iteration+1}: Failed to receive the download event")
                            obj.setLoadModuleStatus("FAILURE")
                            break  
                    else:
                        print(f"Iteration {iteration+1}: Failed to download {app_bundle_name} from {app_download_url}")
                        obj.setLoadModuleStatus("FAILURE") 
                        break
                else:
                    print(f"Iteration {iteration+1}: Failed to receive DOWNLOAD FAILURE event")   
                    tdkTestObj.setResultStatus("FAILURE") 
            else:
                print(f"Iteration {iteration+1}: Download API accepting invalid URL")
                tdkTestObj.setResultStatus("FAILURE")
                break
        event_listener.disconnect()   
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")  
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")

