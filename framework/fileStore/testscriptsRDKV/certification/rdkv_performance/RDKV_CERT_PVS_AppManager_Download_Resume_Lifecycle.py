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
import time

import tdklib
import PerformanceTestVariables
import StabilityTestUtility
from StabilityTestUtility import *


obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_Download_Resume_Lifecycle');
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
    download_id = None
    if status == "SUCCESS":
        bundle_name = PerformanceTestVariables.Large_Validation_File
        download_url = PerformanceTestVariables.app_download_url.rstrip("/") + "/" + bundle_name
        print("\nStep 1 : Trigger the download of %s from %s" % (bundle_name, download_url))

        tdkTestObj = obj.createTestStep("rdkservice_download_app_bundle")
        tdkTestObj.addParameter("download_url", download_url)
        tdkTestObj.executeTestCase(expectedResult)
        if tdkTestObj.getResult() == expectedResult:
            download_id = ast.literal_eval(tdkTestObj.getResultDetails())

        if download_id is not None:
            print("Download accepted by org.rdk.DownloadManager.download with download ID : %s" % download_id)
            progress = None
            progress_wait_time = PerformanceTestVariables.progress_wait_time
            print("\nStep 2 : Poll org.rdk.DownloadManager.progress for up to %s seconds until the download is in progress (0 < progress < 100)" % progress_wait_time)
            for _ in range(progress_wait_time):
                tdkTestObj = obj.createTestStep("rdkservice_setValue")
                tdkTestObj.addParameter("method", "org.rdk.DownloadManager.progress")
                tdkTestObj.addParameter("value", '{"downloadId": "%s"}' % download_id)
                tdkTestObj.executeTestCase(expectedResult)
                if tdkTestObj.getResult() == expectedResult:
                    progress = ast.literal_eval(tdkTestObj.getResultDetails())
                    print("Current progress of download ID %s : %s" % (download_id, progress))
                if isinstance(progress, (int, float)) and 0 < progress < 100:
                    break
                time.sleep(1)

            if isinstance(progress, (int, float)) and 0 < progress < 100:
                print("Download is in progress at %s percent" % progress)
                print("\nStep 3 : Pause the download using org.rdk.DownloadManager.pause")
                tdkTestObj = obj.createTestStep("rdkservice_setValue")
                tdkTestObj.addParameter("method", "org.rdk.DownloadManager.pause")
                tdkTestObj.addParameter("value", '{"downloadId": "%s"}' % download_id)
                tdkTestObj.executeTestCase(expectedResult)
                if tdkTestObj.getResult() == expectedResult:
                    print("Pause request accepted. Waiting 3 seconds before re-reading the progress to confirm it is frozen")
                    time.sleep(3)
                    tdkTestObj = obj.createTestStep("rdkservice_setValue")
                    tdkTestObj.addParameter("method", "org.rdk.DownloadManager.progress")
                    tdkTestObj.addParameter("value", '{"downloadId": "%s"}' % download_id)
                    tdkTestObj.executeTestCase(expectedResult)
                    paused_progress = ast.literal_eval(tdkTestObj.getResultDetails())
                    print("Progress read after pause : %s (progress before pause : %s)" % (paused_progress, progress))

                    if paused_progress == progress:
                        print("Download is paused, progress is held at %s percent" % paused_progress)
                        print("\nStep 4 : Resume the download using org.rdk.DownloadManager.resume")
                        tdkTestObj = obj.createTestStep("rdkservice_setValue")
                        tdkTestObj.addParameter("method", "org.rdk.DownloadManager.resume")
                        tdkTestObj.addParameter("value", '{"downloadId": "%s"}' % download_id)
                        tdkTestObj.executeTestCase(expectedResult)
                        if tdkTestObj.getResult() == expectedResult:
                            print("Resume request accepted. Waiting 5 seconds before re-reading the progress to confirm it is advancing")
                            time.sleep(5)
                            tdkTestObj = obj.createTestStep("rdkservice_setValue")
                            tdkTestObj.addParameter("method", "org.rdk.DownloadManager.progress")
                            tdkTestObj.addParameter("value", '{"downloadId": "%s"}' % download_id)
                            tdkTestObj.executeTestCase(expectedResult)
                            resumed_progress = ast.literal_eval(tdkTestObj.getResultDetails())
                            print("Progress read after resume : %s (progress while paused : %s)" % (resumed_progress, paused_progress))
                            if isinstance(resumed_progress, (int, float)) and resumed_progress > paused_progress:
                                print("Download pause and resume validated successfully")
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print("Download progress did not advance after resume, it stayed at %s percent" % resumed_progress)
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("org.rdk.DownloadManager.resume failed for download ID %s" % download_id)
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print("Download progress moved from %s to %s while paused, the pause request was not honoured" % (progress, paused_progress))
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("org.rdk.DownloadManager.pause failed for download ID %s" % download_id)
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("Download did not reach an active progress state within %s seconds, last progress read is %s" % (progress_wait_time, progress))
                print("Please verify the size of %s configured as Large_Validation_File in PerformanceTestVariables. A small file can complete downloading before the progress check and leave no window to pause it" % bundle_name)
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("org.rdk.DownloadManager.download did not return a valid download ID for %s" % download_url)
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("DownloadManager is not active")
        obj.setLoadModuleStatus("FAILURE")

    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")