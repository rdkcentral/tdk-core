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

# use tdklib library
import tdklib; 
import time
import StabilityTestUtility
from StabilityTestUtility import *
import PerformanceTestVariables
from datetime import datetime, UTC

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeToInstall_DownloadedApp')

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
Summ_list = []

if expectedResult in result.upper():

    status ="SUCCESS"

    print("\nCheck the status of AppManagers in the device")

    plugins_list = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager"]
    plugin_status_needed = {
        "org.rdk.DownloadManager":"activated",
        "org.rdk.PackageManagerRDKEMS":"activated",
        "org.rdk.AppManager":"activated"
    }

    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)

    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)

    if status == "SUCCESS":

        app_bundle = PerformanceTestVariables.google_bundle
        app_name = app_bundle_name.split('+')[0]
        print(app_name)
        app_download_url = PerformanceTestVariables.app_download_url

        # -------------------------------
        # STEP 1: DOWNLOAD
        # -------------------------------
        print("\nStarting download")

        start_download = datetime.now(UTC)

        status = rdkservice_download_app_bundle(app_download_url)

        end_download = datetime.now(UTC)

        if status != "SUCCESS":
            print("Download failed")

        download_time = (end_download - start_download).total_seconds() * 1000

        print(f"Download Time: {download_time} ms")

        # -------------------------------
        # STEP 2: INSTALL
        # -------------------------------
        print("\nStarting install")

        fileLocator = app_download_url   # Using same URL

        start_install = datetime.now(UTC)

        status = rdkservice_install_app(fileLocator, app_name)

        end_install = datetime.now(UTC)

        if status != "SUCCESS":
            print("Install failed")
        install_time = (end_install - start_install).total_seconds() * 1000

        print(f"Install Time: {install_time} ms")

        # -------------------------------
        # TOTAL TIME
        # -------------------------------
        total_time = download_time + install_time

        print(f"\nTotal Time (Download + Install): {total_time} ms")

        # -------------------------------
        # THRESHOLD HANDLING
        # -------------------------------
        conf_file, file_status = getConfigFileName(obj.realpath)

        _, download_threshold = getDeviceConfigKeyValue(conf_file,"APPMANAGER_DOWNLOAD_THRESHOLD_VALUE")
        _, install_threshold = getDeviceConfigKeyValue(conf_file,"APPMANAGER_INSTALL_THRESHOLD_VALUE")
        _, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")

        if not download_threshold:
            download_threshold = "2000"
        if not install_threshold:
            install_threshold = "2000"
        if not offset:
            offset = "10"

        allowed_time = int(download_threshold) + int(install_threshold) + int(offset)

        print(f"\nDownload Threshold : {download_threshold} ms")
        print(f"Install Threshold  : {install_threshold} ms")
        print(f"Offset             : {offset} ms")
        print(f"Allowed Time       : {allowed_time} ms")

        # -------------------------------
        # VALIDATION
        # -------------------------------
        if 0 < int(total_time) < allowed_time:
            print("\nTime within expected range")
            print(f"Measured: {total_time} ms | Allowed: {allowed_time} ms")
        else:
            diff = int(total_time) - allowed_time

            print("\nTime exceeded threshold")
            print(f"Measured : {total_time} ms")
            print(f"Allowed  : {allowed_time} ms")
            print(f"Exceeded by: {diff} ms")
        # -------------------------------
        # SUMMARY
        # -------------------------------
        Summ_list.append(f"Download Time : {download_time} ms")
        Summ_list.append(f"Install Time  : {install_time} ms")
        Summ_list.append(f"Total Time    : {total_time} ms")
        Summ_list.append(f"Allowed Time  : {allowed_time} ms")

        getSummary(Summ_list, obj)

    else:
        print("Plugins not active")
        obj.setLoadModuleStatus("FAILURE")

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
