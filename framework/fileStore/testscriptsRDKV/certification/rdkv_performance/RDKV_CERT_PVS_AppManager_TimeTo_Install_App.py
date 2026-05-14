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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeTo_Install_App');
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
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.PackageManagerRDKEMS":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name = app_bundle_name.split("+")[0]
        app_download_url = PerformanceTestVariables.app_download_url
        app_download_url = app_download_url + "/" + app_bundle_name
        print(f"Check if {app_bundle_name} is already installed in the device")
        tdkTestObj = obj.createTestStep('rdkv_getInstalledPackages')
        tdkTestObj.executeTestCase(expectedResult)
        status = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        if status == "SUCCESS" :
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
                if status =="SUCCESS":
                    print(f"Successfully uninstalled {app_name}")
                    tdkTestObj.setResultStatus("SUCCESS")
                    uninstalled = True
                else:
                    print(f"Failed to uninstall {app_name}")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print(f"{app_name} is not installed in the device")
                uninstalled = True
            if uninstalled:
                print(f"Start downloding {app_name} from {app_download_url}")
                tdkTestObj = obj.createTestStep('rdkservice_download_app_bundle')
                tdkTestObj.addParameter("download_url", app_download_url)
                tdkTestObj.executeTestCase(expectedResult)
                status = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails()
                if status == "SUCCESS":
                    print("Successfully downloaded the app bundle")
                    tdkTestObj.setResultStatus("SUCCESS")

                    conf_file,result = getConfigFileName(obj.realpath)
                    fileLocator = ""
                    if result == "SUCCESS":
                        status,fileLocator = getDeviceConfigKeyValue(conf_file,"PACKAGEMANAGER_FILE_LOCATOR")
                    if fileLocator != "":
                        fileLocator = fileLocator + str(details)
                        print (fileLocator)
                        print("Register for install event")
                        thunder_port=rdkv_performancelib.devicePort
                        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppInstalled", "id": "client.events.1" }}'],"/jsonrpc",False)
                        time.sleep(5)
                        tdkTestObj = obj.createTestStep('rdkservice_install_app')
                        tdkTestObj.addParameter("fileLocator", fileLocator)
                        tdkTestObj.addParameter("app_id", app_name)
                        start_time = datetime.now(UTC).time()
                        tdkTestObj.executeTestCase(expectedResult)
                        status = tdkTestObj.getResult()
                        details = tdkTestObj.getResultDetails()
                        if status == "SUCCESS":
                            print("Check for install event")
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
                            if "onAppInstalled" in event:
                                print("Received install event successfully")
                                tdkTestObj.setResultStatus("SUCCESS")
                                event_data = str(event).split("$$$")[1]
                                install_time = str(event).split("$$$")[0]
                                install_start_time = datetime.strptime(str(start_time), "%H:%M:%S.%f")
                                installed_time = datetime.strptime(str(install_time), "%H:%M:%S.%f")
                                conf_file,file_status = getConfigFileName(obj.realpath)
                                config_status,install_threshold = getDeviceConfigKeyValue(conf_file,"APPMANAGER_INSTALL_THRESHOLD_VALUE")
                                config_status,install_offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                Summ_list.append('APP_INSTALL_THRESHOLD_VALUE :{}ms'.format(install_threshold))
                                Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(install_offset))
                                Summ_list.append('App install initiated at :{}'.format(start_time))
                                Summ_list.append('App installed at :{}'.format(install_time))
                                time_taken_for_install = installed_time - install_start_time
                                time_taken_for_install = time_taken_for_install.total_seconds() * 1000
                                print("\nInstall initiated at ", start_time)
                                print("\n Install completed at ", install_time)
                                print("\n Time taken to install the app : {}(ms)".format(time_taken_for_install))
                                Summ_list.append('Time taken to install app :{}ms'.format(time_taken_for_install))
                                print("\n Threshold value for time taken to install the app: {} ms".format(install_threshold))
                                print("\n Validate the time:")
                                if 0 < time_taken_for_install < (int(install_threshold) + int(install_offset)) :
                                    print("\n Time taken for installing the app is within the expected range")
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    event_listener.disconnect()
                                else:
                                    print("\n Time taken for installing the app is not within the expected range")
                                    tdkTestObj.setResultStatus("FAILURE")
                                getSummary(Summ_list,obj)
                            else:
                                print("Failed to receive install event")
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("Failed to install the app")
                            tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("Failed to download the app bundle")
                    tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("Failed to get the installed apps")
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
