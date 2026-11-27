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
import rdkv_performancelib
import StabilityTestUtility
from StabilityTestUtility import *
import FireboltTestVariables
import shutil

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_firebolt","1",standAlone=True);

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_FIREBOLT_SchemaValidation');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    status ="SUCCESS"
    print("\nCheck the status of AppManagers in the device")
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated", "org.rdk.AppPackageManager":"activated","org.rdk.AppManager":"activated"}
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    if status == "SUCCESS":

        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('firebolt_execute');
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
            print("Successfully registered the reportid")
            app_bundle=FireboltTestVariables.firebolt_bundle
            app_name = FireboltTestVariables.firebolt_app_id
            app_download_url = FireboltTestVariables.app_download_url
            status = rdkv_performancelib.rdkservice_install_launch_app(obj, app_bundle, app_name,app_download_url)
            if status == "SUCCESS":
                print("Successfully launched the app and started the test")
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(10)
                report_path = obj.realpath+"/fileStore/" + FireboltTestVariables.reports_directory
                print(report_path)
                report_name_prefix = "tdk_%s" % (obj.execID)
                found = []
                for _ in range(10):
                # The report server stores each format in its own sub folder (json, html, xlsx).
                    for folder, _dirs, files in os.walk(report_path):
                        found.extend(os.path.join(folder, name) for name in files if name.startswith(report_name_prefix))
                    if found:
                        break
                    time.sleep(3)
                if found:
                    print("Reports found: %s" % found)
                    tdkTestObj.setResultStatus("SUCCESS")
                    download_path = '{}{}_{}_{}'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
                    for report in found:
                        if report.lower().endswith((".html", ".xlsx")):
                            destination = "%s_%s" % (download_path, os.path.basename(report))
                            shutil.copy(report, destination)
                            print("Copied %s to %s" % (report, destination))
                else:
                    print("No report with prefix %s found in %s" % (report_name_prefix, report_path))
                    tdkTestObj.setResultStatus("FAILURE")
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
                print("Failed to launch the app")
                tdkTestObj.setResultStatus("FAILURE")

        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("Failed to start the suite")
    obj.unloadModule("rdkv_firebolt");
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")