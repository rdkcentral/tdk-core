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
import rdkv_performancelib
import StabilityTestVariables

obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_AppManager_Launch_Close');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}{}_{}_{}_CPUMemoryInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}

result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

if expectedResult in (result.upper() and pre_condition_status):
    status ="SUCCESS"
    print("\nCheck the status of AppManagers in the device")
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.PackageManagerRDKEMS":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":
        test_count = StabilityTestVariables.launch_close_count
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name= "com.rdkcentral.google"
        app_download_url = PerformanceTestVariables.app_download_url
       # app_download_url = app_download_url + "/" + app_bundle_name
        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name,app_download_url,launch =False)
        if status == "SUCCESS":
            print("Successfully installed the app")
            for i in range(test_count):
                print("ITERATION :", i+1)
                print("_________________")
                print(f"\nLaunching {app_name}")
                time.sleep(10)
                tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                tdkTestObj.addParameter("app_name", app_name)
                tdkTestObj.executeTestCase(expectedResult)
                status = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails()
                if status == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                    print("Check if the app is launched")
                    loaded_apps = rdkv_performancelib.rdkservice_get_loaded_apps()
                    print(loaded_apps)
                    if app_name in loaded_apps:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print("Successfully launched the app")
                        time.sleep(10)
                        print("Killing the app")
                        param = '{"appId": "' + app_name + '"}'
                        tdkTestObj = obj.createTestStep('rdkservice_close_app')
                        tdkTestObj.addParameter("app_id",app_name)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        if result == "SUCCESS":
                            time.sleep(10)
                            tdkTestObj.setResultStatus("SUCCESS")
                            print("\n Validating resource usage:")
                            tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                            tdkTestObj.executeTestCase(expectedResult)
                            resource_usage = tdkTestObj.getResultDetails()
                            result = tdkTestObj.getResult()
                            if expectedResult in result and resource_usage != "ERROR":
                                print("\n Resource usage is within the expected limit")
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print("\n Error while validating resource usage")
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"\nFailed to kill {app_name}")
                            break
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("App is not listed in loaded apps")
                        break
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"\nFailed to launch {app_name}")
                    break
        else:
            print("Failed to install the app")
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
