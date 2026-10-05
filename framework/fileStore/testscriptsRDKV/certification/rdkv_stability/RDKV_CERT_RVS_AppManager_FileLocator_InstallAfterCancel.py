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

import ast
import json
import time

import tdklib
import StabilityTestUtility
from StabilityTestUtility import *
import PerformanceTestVariables
from web_socket_util import *
import rdkv_performancelib
import StabilityTestVariables

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_AppManager_FileLocator_InstallAfterCancel');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)
expectedResult = "SUCCESS"
pre_condition_status = check_device_state(obj)

if expectedResult in result.upper() and expectedResult in pre_condition_status:
    status = "SUCCESS"
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]
    plugin_status_needed = {
        "org.rdk.DownloadManager": "activated",
        "org.rdk.AppPackageManager": "activated",
        "org.rdk.AppManager": "activated"
    }
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj, plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj, plugin_status_needed)
        time.sleep(10)
    else:
        status = "SUCCESS"

    if status == "SUCCESS":
        test_count = int(StabilityTestVariables.AppManager_test_count)
        app_bundle_name = PerformanceTestVariables.Large_Validation_File
        app_name = "com.rdkcentral.google"
        app_download_url = PerformanceTestVariables.app_download_url.rstrip("/") + "/" + app_bundle_name
        seen_download_ids = []
        thunder_port = rdkv_performancelib.devicePort
        payload = ['{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.DownloadManager.1.register", "params": {"event": "onAppDownloadStatus", "id": "client.events.1" }}']
        event_listener = createEventListener(ip, thunder_port, payload, "/jsonrpc", False)
        time.sleep(5)

        for iteration in range(test_count):
            print("ITERATION :", iteration + 1)
            print("_________________")
            event_listener.clearEventsBuffer()
            tdkTestObj = obj.createTestStep('rdkservice_download_app_bundle')
            tdkTestObj.addParameter("download_url", app_download_url)
            tdkTestObj.executeTestCase(expectedResult)
            status = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails()
            if status == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
                download_id = ast.literal_eval(details)
                if download_id not in seen_download_ids:
                    seen_download_ids.append(download_id)
                    print("Download started with unique ID:", download_id)
                    progress = 0
                    progress_check_count = 0
                    while progress_check_count < 30 and progress == 0:
                        time.sleep(1)
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method", "org.rdk.DownloadManager.progress")
                        tdkTestObj.addParameter("value", '{"downloadId": "' + str(download_id) + '"}')
                        tdkTestObj.executeTestCase(expectedResult)
                        status = tdkTestObj.getResult()
                        if status == "SUCCESS":
                            progress = ast.literal_eval(tdkTestObj.getResultDetails())
                        progress_check_count += 1
                    if status == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                        if progress > 0 and progress < 100:
                            print("Download is in progress; cancelling it")
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
                                    _, json_part = event.split("$$$", 1)
                                    json_part = json_part.encode().decode("unicode_escape")
                                    outer = json.loads(json_part)
                                    download_status = json.loads(outer["params"]["downloadStatus"])
                                    event_download_id = download_status[0]["downloadId"]
                                    file_locator = download_status[0]["fileLocator"]
                                    if int(event_download_id) == int(download_id) and file_locator:
                                        print("Cancellation event has the expected unique download ID")
                                        print("Proceeding with immediate installation after cancellation with fileLocator:", file_locator)
                                        tdkTestObj = obj.createTestStep('rdkservice_install_app')
                                        tdkTestObj.addParameter("fileLocator", file_locator)
                                        tdkTestObj.addParameter("app_id", app_name)
                                        tdkTestObj.executeTestCase(expectedResult)
                                        status = tdkTestObj.getResult()
                                        if status == "FAILURE":
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print("Immediate installation failed as expected after cancellation")
                                        else:
                                            print("Immediate installation unexpectedly succeeded after cancellation")
                                            tdkTestObj.setResultStatus("FAILURE")
                                            break
                                    else:
                                        print("Cancellation event ID or package URL was invalid or reused")
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                                else:
                                    print("Timed out waiting for the download cancellation event")
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            else:
                                print("Failed to cancel the in-progress download")
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print("Download was not mid-flight; progress was:", progress)
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print("Failed to query download progress")
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print("Download ID was reused:", download_id)
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            else:
                print("Failed to start download of", app_bundle_name)
                tdkTestObj.setResultStatus("FAILURE")
                break

        event_listener.disconnect()
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Required AppManager plugins are not active")
    obj.unloadModule("rdkv_stability")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load the rdkv_stability module or device precondition")
