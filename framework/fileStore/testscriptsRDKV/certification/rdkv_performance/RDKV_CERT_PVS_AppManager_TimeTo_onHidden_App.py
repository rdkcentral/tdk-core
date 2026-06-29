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
from datetime import datetime, UTC

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeTo_onHidden_App');
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
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager", "org.rdk.RDKWindowManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.PackageManagerRDKEMS":"activated","org.rdk.AppManager":"activated", "org.rdk.RDKWindowManager":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name = app_bundle_name.split("+")[0]
        app_download_url = PerformanceTestVariables.app_download_url
        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name,app_download_url)
        if status == "SUCCESS":
            time.sleep(10)
            hidden_received = False
            result = rdkservice_getValue("org.rdk.AppManager.getLoadedApps")
            appInstanceId = ""
            if result != "EXCEPTION OCCURRED":
                for item in result:
                    if item.get("appId") == app_name and item.get("lifecycleState") == "APP_STATE_ACTIVE":
                        appInstanceId = item.get("appInstanceId", "")
                        break
            if not appInstanceId:
                print("App instance id not received")
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.setResultStatus("FAILURE")
            else:
                time.sleep(5)
                continue_count = 0
                payloads = []
                events = ['{"org.rdk.RDKWindowManager": "onHidden"}']
                thunder_port=rdkv_performancelib.devicePort
                event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.RDKWindowManager.1.register","params": {"event": "onHidden", "id": "client.events.1" }}'],"/jsonrpc",False)
                time.sleep(3)
                method = "org.rdk.RDKWindowManager.1.setVisible"
                visible_state = False
                value = '{"client": "'+appInstanceId+'", "visible": '+json.dumps(visible_state)+'}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method",method)
                tdkTestObj.addParameter("value",value)
                start_time = datetime.now(UTC).time()
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResultDetails()

                while True:
                    if continue_count > 120:
                        break
                    if len(event_listener.getEventsBuffer()) == 0:
                        time.sleep(1)
                        continue_count += 1
                        continue
                    event = event_listener.getEventsBuffer().pop(0)
                    print("\nEvent:", event)
                    if "onHidden" in str(event) and appInstanceId in str(event):
                        hidden_received = True
                        hidden_time = str(event).split("$$$")[0]
                        break

                if hidden_received:
                    
                    print("Received onHidden event successfully")
                    tdkTestObj.setResultStatus("SUCCESS")
                    hidden_start_time = datetime.strptime(str(start_time), "%H:%M:%S.%f")
                    hidden_end_time = datetime.strptime(str(hidden_time), "%H:%M:%S.%f")
                    conf_file,file_status = getConfigFileName(obj.realpath)
                    config_status,hidden_threshold = getDeviceConfigKeyValue(conf_file,"APPMANAGER_SET_VISIBLE_THRESHOLD_VALUE")
                    config_status,hidden_offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                    time_to_hidden = (hidden_end_time - hidden_start_time).total_seconds() * 1000
                    Summ_list.append('HIDDEN_THRESHOLD_VALUE :{}ms'.format(hidden_threshold))
                    Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(hidden_offset))
                    Summ_list.append('SetVisible initiated at :{}'.format(start_time))
                    Summ_list.append('App hidden at :{}'.format(hidden_time))
                    Summ_list.append('Time taken to hide app :{}ms'.format(time_to_hidden))
                    print("\nSetVisible initiated at", start_time)
                    print("\nApp hidden at", hidden_time)
                    print("\nTime taken to receive onHidden event: {} ms".format(time_to_hidden))
                    print("\nThreshold value for onHidden: {} ms".format(hidden_threshold))
                    print("\nValidate the time:")
                    try:
                        if 0 < int(time_to_hidden) < (int(hidden_threshold) + int(hidden_offset)) :
                            print("\nTime taken for onHidden event is within the expected range")
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print("\nTime taken for onHidden event is not within the expected range")
                            tdkTestObj.setResultStatus("FAILURE")
                    except Exception:
                        print("\nError validating time due to invalid threshold/offset values")
                        tdkTestObj.setResultStatus("FAILURE")
                    getSummary(Summ_list,obj)
                    
                else:
                    print("Failed to receive onHidden event")
                    tdkTestObj.setResultStatus("FAILURE")
                    
                event_listener.disconnect()
            print("\n Terminating the app")
            tdkTestObj = obj.createTestStep('rdkv_terminate_app')
            tdkTestObj.addParameter("app_id",app_name)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if result == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("Unable to terminate the app")
                    
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"\nFailed to launch {app_name}")
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")