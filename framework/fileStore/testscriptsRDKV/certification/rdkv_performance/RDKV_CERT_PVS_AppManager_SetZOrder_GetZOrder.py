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

import tdklib; 
import time
import ast
import StabilityTestUtility
from StabilityTestUtility import *
import PerformanceTestVariables
from web_socket_util import *
import rdkv_performancelib

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_SetZOrder_GetZOrder');
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

    app_bundle_name = PerformanceTestVariables.google_bundle
    app_name = app_bundle_name.split("+")[0]
    app_download_url = PerformanceTestVariables.app_download_url
    app_instance_id = ""
    requested_zorder = PerformanceTestVariables.requested_zorder

    if status == "SUCCESS":
        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name, app_download_url)
        if status == "SUCCESS":
            print("Application launched successfully")
            time.sleep(5)
            print("Getting the loaded apps to fetch the instance id of %s" % app_name)
            tdkTestObj = obj.createTestStep("rdkservice_getValue")
            tdkTestObj.addParameter("method", "org.rdk.AppManager.getLoadedApps")
            tdkTestObj.executeTestCase(expectedResult)
            if expectedResult in tdkTestObj.getResult():
                tdkTestObj.setResultStatus("SUCCESS")
                loaded_apps = ast.literal_eval(tdkTestObj.getResultDetails())
                for app in loaded_apps:
                    if app.get("appId") == app_name and app.get("lifecycleState") == "APP_STATE_ACTIVE":
                        app_instance_id = app.get("appInstanceId", "")
                        break
                if app_instance_id:
                    print("appInstanceId of %s is : %s" % (app_name, app_instance_id))
                    print("Setting the z-order of the application to %s" % requested_zorder)
                    tdkTestObj = obj.createTestStep("rdkservice_setValue")
                    tdkTestObj.addParameter("method", "org.rdk.RDKWindowManager.setZOrder")
                    tdkTestObj.addParameter(
                        "value",
                        '{"clientId": "%s", "zOrder": %d}' % (app_instance_id, requested_zorder)
                    )
                    tdkTestObj.executeTestCase(expectedResult)
                    if expectedResult in tdkTestObj.getResult():
                        tdkTestObj.setResultStatus("SUCCESS")
                        print("Reading back the z-order of the application")
                        tdkTestObj = obj.createTestStep("rdkservice_setValue")
                        tdkTestObj.addParameter("method", "org.rdk.RDKWindowManager.getZOrder")
                        tdkTestObj.addParameter("value", '{"clientId": "%s"}' % app_instance_id)
                        tdkTestObj.executeTestCase(expectedResult)
                        if expectedResult in tdkTestObj.getResult():
                            actual_zorder = ast.literal_eval(tdkTestObj.getResultDetails())
                            print("Requested z-order: %s, returned z-order: %s" % (requested_zorder, actual_zorder))
                            if actual_zorder == requested_zorder:
                                print("Successfully set and got the application z-order")
                                tdkTestObj.setResultStatus("SUCCESS")
                                print("Resource usage after setting and getting z-order will be validated next")
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
                                print("Returned z-order does not match the requested z-order")
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("org.rdk.RDKWindowManager.getZOrder failed for clientId %s" % app_instance_id)
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print("org.rdk.RDKWindowManager.setZOrder failed for clientId %s" % app_instance_id)
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("Active application instance id was not received for %s" % app_name)
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("Failed to get the loaded apps")        

            print("Terminating the application %s" % app_name)
            tdkTestObj = obj.createTestStep("rdkv_terminate_app")
            tdkTestObj.addParameter("app_id", app_name)
            tdkTestObj.executeTestCase(expectedResult)
            if tdkTestObj.getResult() == expectedResult:
                print("Application terminated successfully")
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("Failed to terminate the application")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("Failed to install or launch the application")
            obj.setLoadModuleStatus("FAILURE")
    else:
        print("AppManager plugins are not active")
        obj.setLoadModuleStatus("FAILURE")

    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")