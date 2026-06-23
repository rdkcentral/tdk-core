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

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_ResourceUsage_ClearAppData');
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
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.PackageManagerRDKEMS":"activated","org.rdk.AppManager":"activated"}
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
            print("\n Validating resource usage before clearing app data:")
            tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
            tdkTestObj.executeTestCase(expectedResult)
            resource_usage = tdkTestObj.getResultDetails()
            result = tdkTestObj.getResult()
            if expectedResult in result and resource_usage != "ERROR":
                print("\n Resource usage is within the expected limit")
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(5)
                print("\n Terminating the app")
                tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                tdkTestObj.addParameter("app_id",app_name)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()

                if result == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")

                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method", "org.rdk.AppManager.clearAppData")
                    tdkTestObj.addParameter("value", '{"appId": "' + app_name + '"}')
                    tdkTestObj.executeTestCase(expectedResult)
                    status = tdkTestObj.getResult()
                    if status == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"\nCleared app data for {app_name} successfully")
                        print("\n Validating resource usage after clearing app data:")
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

                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"\nFailed to clear app data for {app_name}")

                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("Unable to terminate the app")
            else:
                print("\n Error while validating resource usage")
                tdkTestObj.setResultStatus("FAILURE")

        else:
            obj.setLoadModuleStatus("FAILURE")
            print("Failed to Launch the app")
    else:
        print("The download manager is not active")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
