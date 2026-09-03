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
import json
import ast
import shlex

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_Cancel_LargeFile_Download');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"

if expectedResult in result.upper():
    status ="SUCCESS"
    print("\nCheck the status of AppManagers in the device")
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager", "org.rdk.RDKWindowManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.AppPackageManager":"activated","org.rdk.AppManager":"activated", "org.rdk.RDKWindowManager":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        conf_file,_ = getConfigFileName(obj.realpath)
        config_status,file_locator = getDeviceConfigKeyValue(conf_file,"PACKAGEMANAGER_FILE_LOCATOR")
        file_locator = file_locator.rstrip("/") + "/"
        print("File locator URL from the configuration is : ", file_locator)
        tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
        tdkTestObj.addParameter("realpath", obj.realpath)
        tdkTestObj.addParameter("deviceIP", ip)
        tdkTestObj.executeTestCase(expectedResult)
        status = tdkTestObj.getResult()
        ssh_params = tdkTestObj.getResultDetails()
        if status == expectedResult and ssh_params not in ("", "{}"):
            tdkTestObj.setResultStatus("SUCCESS")
            ssh_params_dict = json.loads(ssh_params)
            ssh_method = ssh_params_dict.get("ssh_method")
            credentials = ssh_params_dict.get("credentials")
            if not ssh_method or not credentials:
                print("SSH method or credentials not found in configuration")
                tdkTestObj.setResultStatus("FAILURE")
            else:
                cmd = "du -sk " + shlex.quote(file_locator) + " | awk '{print $1}'" 
                tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                tdkTestObj.addParameter("ssh_method", ssh_method)
                tdkTestObj.addParameter("credentials", credentials)
                tdkTestObj.addParameter("command", cmd)
                tdkTestObj.executeTestCase(expectedResult)
                status = tdkTestObj.getResult()
                output = tdkTestObj.getResultDetails()
                output = output.strip().splitlines()[-1]
                initial_used_memory = int(float(output))
                if status == expectedResult:
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                print("Disk usage :\n", initial_used_memory,"KB")
                print("Register for the Download event")
                thunder_port = rdkv_performancelib.devicePort
                event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 2,"method": "org.rdk.DownloadManager.1.register","params": {"event": "onAppDownloadStatus", "id": "client.events.1" }}'],"/jsonrpc",False)
                time.sleep(5)
                app_bundle_name = PerformanceTestVariables.Large_Validation_File
                app_download_url = PerformanceTestVariables.app_download_url.rstrip("/") + "/" + app_bundle_name
                time.sleep(1)
                event_listener.clearEventsBuffer() 
                print(f"\nStart download of {app_bundle_name}")
                tdkTestObj = obj.createTestStep('rdkservice_download_app_bundle')
                tdkTestObj.addParameter("download_url", app_download_url)
                tdkTestObj.executeTestCase(expectedResult)
                time.sleep(15)
                status = tdkTestObj.getResult()
                result = tdkTestObj.getResultDetails()
                if status == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                    download_id = ast.literal_eval(result)
                    print(f"Download ID for {app_bundle_name} is : {download_id}")
                    time.sleep(2)
                    print("Checking for progress of the download")   
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method", "org.rdk.DownloadManager.progress")
                    tdkTestObj.addParameter("value", '{"downloadId": "' + str(download_id) + '"}')
                    tdkTestObj.executeTestCase(expectedResult)
                    status = tdkTestObj.getResult()   
                    result = tdkTestObj.getResultDetails()           
                    if status == expectedResult:
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                    progress = ast.literal_eval(result)
                    print(f"Progress of the download is : {progress}")
                    if progress > 0 and progress < 100:
                        print(f"Download of {app_bundle_name} is in progress")
                        print("Cancelling the download and check the status")
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method", "org.rdk.DownloadManager.cancel")
                        tdkTestObj.addParameter("value", '{"downloadId": "' + str(download_id) + '"}')
                        tdkTestObj.executeTestCase(expectedResult)
                        status = tdkTestObj.getResult()
                        if status == "SUCCESS":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print("Checking for cancellation event")
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
                                break
                            if "onAppDownloadStatus" in str(event) and "DOWNLOAD_FAILURE" in str(event):
                                print("Received the download cancellation event")
                                _, json_part = event.split("$$$", 1)
                                json_part = json_part.encode().decode("unicode_escape")
                                outer = json.loads(json_part)
                                inner = json.loads(outer["params"]["downloadStatus"])
                                event_download_id = inner[0]["downloadId"]
                                print(f"Download ID from the event is : {event_download_id}")
                                filelocator_url = inner[0]["fileLocator"]
                                print(f"File locator URL from the event is : {filelocator_url}")
                                if int(event_download_id) == download_id and str(download_id) in filelocator_url:
                                    print("Package download cancelled successfully with correct download status")
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print("Deleting the package from the device ...")
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                    tdkTestObj.addParameter("method", "org.rdk.DownloadManager.delete")
                                    tdkTestObj.addParameter("value", '{"fileLocator": "' + filelocator_url + '"}')
                                    tdkTestObj.executeTestCase(expectedResult)
                                    status = tdkTestObj.getResult()
                                    if status == "SUCCESS":
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print("Verifying the package deletion from the device ...")
                                        cmd = "ls -l " + shlex.quote(filelocator_url)
                                        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                        tdkTestObj.addParameter("ssh_method", ssh_method)
                                        tdkTestObj.addParameter("credentials", credentials)
                                        tdkTestObj.addParameter("command", cmd)
                                        tdkTestObj.executeTestCase(expectedResult)
                                        status = tdkTestObj.getResult()
                                        output = tdkTestObj.getResultDetails()
                                        if status == expectedResult and "No such file or directory" in output:
                                            print("Package deleted successfully from the device")
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print("Checking the disk usage after deletion of the package")
                                            cmd = "du -sk " + shlex.quote(file_locator) + " | awk '{print $1}'"
                                            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                            tdkTestObj.addParameter("ssh_method", ssh_method)
                                            tdkTestObj.addParameter("credentials", credentials)
                                            tdkTestObj.addParameter("command", cmd)
                                            tdkTestObj.executeTestCase(expectedResult)
                                            status = tdkTestObj.getResult()
                                            output = tdkTestObj.getResultDetails()
                                            output = output.strip().splitlines()[-1]
                                            final_used_memory = int(float(output))
                                            print("Disk usage after deletion of the package :\n", final_used_memory,"KB")
                                            if status == expectedResult and final_used_memory <= initial_used_memory:
                                                print("Disk usage is back to the initial value after deletion of the package")
                                                tdkTestObj.setResultStatus("SUCCESS")
                                            else:
                                                print(f"Disk usage is not back to the initial value after deletion of the package")
                                                tdkTestObj.setResultStatus("FAILURE")    
                                        else:
                                            print(f"Package deletion failed from the device")
                                            tdkTestObj.setResultStatus("FAILURE")  
                                    else:
                                        print(f"Failed to delete the package from the device")
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print(f"Package download cancellation failed with incorrect download status")
                                    tdkTestObj.setResultStatus("FAILURE")   
                        else:
                            print(f"Failed to cancel the download of {app_bundle_name}")
                            tdkTestObj.setResultStatus("FAILURE")      
                    else:
                        print(f"Download of {app_bundle_name} is not in progress, progress is : {progress}")
                        print(f"Please verify the size of {app_bundle_name} configured as Large_Validation_File in PerformanceTestVariables. A small file can complete downloading before the progress check and leave no window to cancel it")
                        tdkTestObj.setResultStatus("FAILURE") 
                else:
                    print(f"Failed to download {app_bundle_name} from {app_download_url}")
                    tdkTestObj.setResultStatus("FAILURE") 
            
                event_listener.disconnect()   
        else:
            print("Failed to get SSH parameters from configuration")
            tdkTestObj.setResultStatus("FAILURE")
            obj.setLoadModuleStatus("FAILURE")
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")  
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")