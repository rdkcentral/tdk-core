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
Summ_list=[]
if expectedResult in result.upper():
    status ="SUCCESS"
    print("\nCheck the status of AppManagers in the device")
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager", "org.rdk.RDKWindowManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.AppPackageManager":"activated","org.rdk.AppManager":"activated", "org.rdk.RDKWindowManager":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    test_status = "FAILURE"
    download_id = None
    if status == "SUCCESS":
        bundle_name = PerformanceTestVariables.Large_Validation_File
        download_url = PerformanceTestVariables.app_download_url + bundle_name
        print("Starting download of %s" % bundle_name)

        tdkTestObj = obj.createTestStep("rdkservice_download_app_bundle")
        tdkTestObj.addParameter("download_url", download_url)
        tdkTestObj.executeTestCase(expectedResult)
        if tdkTestObj.getResult() == expectedResult:
            try:
                download_id = ast.literal_eval(tdkTestObj.getResultDetails())
            except (SyntaxError, ValueError):
                download_id = None

        if download_id is not None:
            print("Download ID: %s" % download_id)
            progress = None
            progress_wait_time = PerformanceTestVariables.progress_wait_time
            for _ in range(progress_wait_time):
                tdkTestObj = obj.createTestStep("rdkservice_setValue")
                tdkTestObj.addParameter("method", "org.rdk.DownloadManager.progress")
                tdkTestObj.addParameter("value", '{"downloadId": "%s"}' % download_id)
                tdkTestObj.executeTestCase(expectedResult)
                if tdkTestObj.getResult() == expectedResult:
                    try:
                        progress = ast.literal_eval(tdkTestObj.getResultDetails())
                    except (SyntaxError, ValueError):
                        progress = None
                if isinstance(progress, (int, float)) and 0 < progress < 100:
                    break
                time.sleep(1)

            if isinstance(progress, (int, float)) and 0 < progress < 100:
                print("Progress before pause: %s" % progress)
                tdkTestObj = obj.createTestStep("rdkservice_setValue")
                tdkTestObj.addParameter("method", "org.rdk.DownloadManager.pause")
                tdkTestObj.addParameter("value", '{"downloadId": "%s"}' % download_id)
                tdkTestObj.executeTestCase(expectedResult)
                if tdkTestObj.getResult() == expectedResult:
                    time.sleep(3)
                    tdkTestObj = obj.createTestStep("rdkservice_setValue")
                    tdkTestObj.addParameter("method", "org.rdk.DownloadManager.progress")
                    tdkTestObj.addParameter("value", '{"downloadId": "%s"}' % download_id)
                    tdkTestObj.executeTestCase(expectedResult)
                    try:
                        paused_progress = ast.literal_eval(tdkTestObj.getResultDetails())
                    except (SyntaxError, ValueError):
                        paused_progress = None

                    if paused_progress == progress:
                        print("Download paused at progress: %s" % paused_progress)
                        tdkTestObj = obj.createTestStep("rdkservice_setValue")
                        tdkTestObj.addParameter("method", "org.rdk.DownloadManager.resume")
                        tdkTestObj.addParameter("value", '{"downloadId": "%s"}' % download_id)
                        tdkTestObj.executeTestCase(expectedResult)
                        if tdkTestObj.getResult() == expectedResult:
                            time.sleep(5)
                            tdkTestObj = obj.createTestStep("rdkservice_setValue")
                            tdkTestObj.addParameter("method", "org.rdk.DownloadManager.progress")
                            tdkTestObj.addParameter("value", '{"downloadId": "%s"}' % download_id)
                            tdkTestObj.executeTestCase(expectedResult)
                            try:
                                resumed_progress = ast.literal_eval(tdkTestObj.getResultDetails())
                            except (SyntaxError, ValueError):
                                resumed_progress = None
                            print("Progress after resume: %s" % resumed_progress)
                            if isinstance(resumed_progress, (int, float)) and resumed_progress > paused_progress:
                                print("Download pause and resume validated successfully")
                                test_status = "SUCCESS"
                            else:
                                print("Download progress did not advance after resume")
                        else:
                            print("Failed to resume the download")
                    else:
                        print("Download progress changed while paused")
                else:
                    print("Failed to pause the download")
            else:
                print("Download did not reach an active progress state")
        else:
            print("Failed to obtain a valid download ID")
    else:
        print("DownloadManager is not active")

    if test_status != "SUCCESS":
        print("Download pause/resume test failed; exiting gracefully")
    obj.setLoadModuleStatus(test_status)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")