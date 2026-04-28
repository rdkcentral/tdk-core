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
from datetime import datetime, UTC


obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeTo_Download_AppBundle');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
Summ_list=[]
if expectedResult in result.upper():
    print("Check the status of Download Manager")
    status ="SUCCESS"
    plugins_list = ["org.rdk.DownloadManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        print("DownloadManager is in active state")
        print("Register for the Download event")
        thunder_port = rdkv_performancelib.devicePort
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 2,"method": "org.rdk.DownloadManager.1.register","params": {"event": "onAppDownloadStatus", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(5)
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_download_url = PerformanceTestVariables.app_download_url

        print(f"Start download of {app_bundle_name}")
        app_download_url = app_download_url + "/" + app_bundle_name
        tdkTestObj = obj.createTestStep('rdkservice_download_app_bundle')
        tdkTestObj.addParameter("download_url", app_download_url)
        #start_time = str(datetime.utcnow()).split()[1]
        start_time = datetime.now(UTC).time()
        print(start_time)
        tdkTestObj.executeTestCase(expectedResult)
        status = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        if status == "SUCCESS":
            print("Check for download event")
            tdkTestObj.setResultStatus("SUCCESS")
            continue_count = 0
            end_time = ""
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
            if "onAppDownloadStatus" in str(event):
                print("Received Download event successfully")
                tdkTestObj.setResultStatus("SUCCESS")
                event_data = str(event).split("$$$")[1]
                download_time = str(event).split("$$$")[0]
                download_start_time = datetime.strptime(str(start_time), "%H:%M:%S.%f")
                downloaded_time = datetime.strptime(str(download_time), "%H:%M:%S.%f")
                conf_file,file_status = getConfigFileName(obj.realpath)
                config_status,download_threshold = getDeviceConfigKeyValue(conf_file,"APPMANAGER_DOWNLOAD_THRESHOLD_VALUE")
                config_status,download_offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                Summ_list.append('APP_DOWNLOAD_THRESHOLD_VALUE :{}ms'.format(download_threshold))
                Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(download_offset))
                Summ_list.append('App download initiated at :{}'.format(start_time))
                Summ_list.append('App downloaded at :{}'.format(download_time))
                time_taken_for_download = downloaded_time - download_start_time
                time_taken_for_download = time_taken_for_download.total_seconds() * 1000
                print("\nDownload initiated at ", start_time)
                print("\n Download completed at ", download_time)
                print("\n Time taken to download the app : {}(ms)".format(time_taken_for_download))
                Summ_list.append('Time taken to download app :{}ms'.format(time_taken_for_download))
                print("\n Threshold value for time taken to download bundle: {} ms".format(download_threshold))
                print("\n Validate the time:")
                if 0 < time_taken_for_download < (int(download_threshold) + int(download_offset)) :
                     print("\n Time taken for downloading the app is within the expected range")
                     tdkTestObj.setResultStatus("SUCCESS")
                     event_listener.disconnect()
                else:
                    print("\n Time taken for downloading the app is not within the expected range")
                    tdkTestObj.setResultStatus("FAILURE")
                getSummary(Summ_list,obj)
            else:
                print("Failed to receive download event")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("Failed to start downlod of bundle")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")