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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_ResourceUsage_Download_AppBundle');
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
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_download_url = PerformanceTestVariables.app_download_url

        print(f"Start download of {app_bundle_name}")
        app_download_url = app_download_url + "/" + app_bundle_name
        tdkTestObj = obj.createTestStep('rdkservice_download_app_bundle')
        tdkTestObj.addParameter("download_url", app_download_url)
        tdkTestObj.executeTestCase(expectedResult)
        status = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        if status == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
            print("Successfully started download of bundle")
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