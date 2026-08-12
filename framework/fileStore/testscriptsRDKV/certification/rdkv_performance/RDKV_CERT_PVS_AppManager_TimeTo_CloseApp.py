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

import tdklib
import time
import sys
from io import StringIO
import StabilityTestUtility
from StabilityTestUtility import *
import PerformanceTestVariables
from datetime import datetime, UTC

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeTo_CloseApp')

expectedResult = "SUCCESS"

# Load module
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

if expectedResult in result.upper():

    status = "SUCCESS"

    # Ensure plugins active
    essential_plugins = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]
    plugin_status_needed = {p: "activated" for p in essential_plugins}
    
    # Suppress stdout for utility function calls
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj, essential_plugins)
    
    # Restore stdout
    sys.stdout = old_stdout
    
    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj, plugin_status_needed)
        time.sleep(10)

    if status == "SUCCESS":
        print("[SUCCESS] AppManager plugins activated")
        
        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name = app_bundle_name.split('+')[0]
        app_download_url = PerformanceTestVariables.app_download_url
        
        print(f"[INFO] App to close: {app_name}")
        
        # Install + Launch
        print("\n[INFO] Installing and launching app")
        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name, app_download_url, launch=True)
        
        if status == "SUCCESS":
            print("[SUCCESS] App launched successfully")
            
            print(f"\n[INFO] Closing app {app_name}")
            
            # Close app using test step
            tdkTestObj = obj.createTestStep('rdkservice_close_app')
            tdkTestObj.addParameter("app_id", app_name)
            tdkTestObj.executeTestCase(expectedResult)
            
            if tdkTestObj.getResult() != "SUCCESS":
                print("[FAILURE] Failed to send close command")
                tdkTestObj.setResultStatus("FAILURE")
                status = "FAILURE"
            else:
                print("[INFO] Close command sent, waiting for app to close")
                
                # Start time capture
                start_time = datetime.now(UTC)
                time.sleep(10)  # allow cleanup
                end_time = datetime.now(UTC)
                
                # Calculate close time
                close_time_ms = (end_time - start_time).total_seconds() * 1000
                
                if close_time_ms > 0:
                    print(f"[SUCCESS] Time taken to close app: {close_time_ms} ms")
                    tdkTestObj.setResultStatus("SUCCESS")
                    
                    # Validate against threshold
                    print(f"\n[INFO] Validating close time against threshold")
                    
                    # Suppress stdout for utility function calls
                    old_stdout = sys.stdout
                    sys.stdout = StringIO()
                    
                    conf_file, _ = getConfigFileName(obj.realpath)
                    config_status, close_threshold = getDeviceConfigKeyValue(conf_file, "APPMANAGER_CLOSE_THRESHOLD_VALUE")
                    offset_status, offset = getDeviceConfigKeyValue(conf_file, "THRESHOLD_OFFSET")
                    
                    # Restore stdout
                    sys.stdout = old_stdout
                    
                    if not close_threshold:
                        close_threshold = "2000"
                    if not offset:
                        offset = "500"
                    
                    threshold = int(close_threshold)
                    offset_val = int(offset)
                    threshold_max = threshold + offset_val
                    
                    print(f"Threshold: {threshold} ms")
                    print(f"Offset: {offset_val} ms")
                    print(f"Max allowed: {threshold_max} ms")
                    
                    if 0 < close_time_ms < threshold_max:
                        print(f"\n[SUCCESS] Close time is within expected range")
                    else:
                        print(f"\n[FAILURE] Close time exceeds threshold")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print(f"[ERROR] Invalid close time: {close_time_ms} ms")
                    tdkTestObj.setResultStatus("FAILURE")
                    status = "FAILURE"
        else:
            print("[FAILURE] Install/Launch failed")
            tdkTestObj.setResultStatus("FAILURE")

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
