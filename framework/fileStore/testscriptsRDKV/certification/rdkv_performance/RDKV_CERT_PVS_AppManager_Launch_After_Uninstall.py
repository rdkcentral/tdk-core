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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_LaunchAfterUninstall');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"

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
    test_status = "FAILURE"

    if status == "SUCCESS":
        print("Checking whether the application is available for uninstall")
        installed_packages = rdkv_getInstalledPackages()
        if installed_packages and app_name in str(installed_packages):
            print("Application is already installed: %s" % app_name)
            status = "SUCCESS"
        else:
            print("Application is unavailable; installing: %s" % app_name)
            status = rdkservice_install_launch_app(obj, app_bundle_name, app_name, app_download_url, launch=False)
        if status == "SUCCESS":
            print("Application installed successfully")
            tdkTestObj = obj.createTestStep("rdkservice_uninstall_app")
            tdkTestObj.addParameter("app_id", app_name)
            tdkTestObj.executeTestCase(expectedResult)
            uninstall_result = tdkTestObj.getResult()

            if uninstall_result in (None, "", expectedResult):
                print("Application uninstalled successfully")
                time.sleep(5)
                print("Attempting to launch the uninstalled application")
                tdkTestObj = obj.createTestStep("rdkservice_launch_app")
                tdkTestObj.addParameter("app_name", app_name)
                tdkTestObj.executeTestCase(expectedResult)
                launch_result = tdkTestObj.getResult()

                if launch_result != expectedResult:
                    print("Launch was rejected as expected")
                    test_status = "SUCCESS"
                else:
                    print("FAILURE: Uninstalled application launched successfully")
            else:
                print("Failed to uninstall the application")
        else:
            print("Failed to install the application")
    else:
        print("AppManager plugins are not active")

    obj.setLoadModuleStatus(test_status)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")