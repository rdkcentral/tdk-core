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
from rdkv_performancelib import *
from datetime import datetime, UTC

# Test component
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeToRunApplication')

expectedResult = "SUCCESS"

# Load module
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

if expectedResult in result.upper():

    status = "SUCCESS"

    # Ensure plugins active
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated","org.rdk.AppPackageManager":"activated","org.rdk.AppManager":"activated"}

    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)

    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
    
    if status != "SUCCESS":
        print("[FAILURE] Failed to activate required plugins")
        obj.setLoadModuleStatus("FAILURE")
        obj.unloadModule("rdkv_performance")
    else:

        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name = app_bundle_name.split('+')[0]
        print(app_name)
        app_download_url = PerformanceTestVariables.app_download_url

        # Install app if needed
        print(f"\n[INFO] Installing {app_name} for run-time measurement")
        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name, app_download_url, launch=False)

        if status == "SUCCESS":

            print(f"\n[INFO] Launching {app_name} for run-time measurement")

            # Capture start time
            start_time = datetime.now(UTC)

            tdkTestObj = obj.createTestStep('rdkservice_launch_app')
            tdkTestObj.addParameter("app_name", app_name)
            tdkTestObj.executeTestCase(expectedResult)
            launch_result = tdkTestObj.getResult()

            if launch_result == "SUCCESS":
                print(f"[INFO] Launch command executed")

                # Validate app is in loaded apps before measuring
                print(f"\n[INFO] Validating app {app_name} reached loaded state")
                time.sleep(3)  # Brief wait for app to start initializing
                
                app_active = False
                validate_count = 0
                while validate_count < 30:  # 30 seconds timeout for validation
                    loaded_apps = rdkservice_get_loaded_apps()
                    if loaded_apps and app_name in str(loaded_apps):
                        print(f"[SUCCESS] App {app_name} verified in loaded apps (ACTIVE state)")
                        app_active = True
                        break
                    
                    time.sleep(1)
                    validate_count += 1
                
                if not app_active:
                    print(f"[ERROR] App {app_name} failed to reach ACTIVE state")
                    status = "FAILURE"
                else:
                    # Capture end time after app is fully loaded and validated
                    end_time = datetime.now(UTC)
                    
                    # Calculate time taken
                    time_taken = end_time - start_time
                    time_taken_ms = time_taken.total_seconds() * 1000
                    
                    print(f"[INFO] Time from launch command to app fully running: {time_taken_ms:.2f} ms")
                    
                    # Get threshold configuration
                    old_stdout = sys.stdout
                    sys.stdout = StringIO()
                    
                    conf_file, file_status = getConfigFileName(obj.realpath)
                    config_status, run_threshold = getDeviceConfigKeyValue(
                        conf_file, "APP_LAUNCH_THRESHOLD_VALUE"
                    )
                    
                    sys.stdout = old_stdout
                    
                    if not run_threshold:
                        print("[FAILURE] APP_LAUNCH_THRESHOLD_VALUE not configured in device configuration file")
                        status = "FAILURE"
                    else:
                        threshold = int(run_threshold)
                        threshold_max = threshold
                        
                        print(f"[INFO] Threshold validation:")
                        print(f"[INFO]   Time taken: {time_taken_ms:.2f} ms")
                        print(f"[INFO]   Max allowed: {threshold_max} ms")
                        
                        if 0 < time_taken_ms < threshold_max:
                            print(f"[SUCCESS] Run time within threshold")
                            status = "SUCCESS"
                        else:
                            print(f"[FAILURE] Run time exceeded threshold")
                            status = "FAILURE"
            else:
                print("[FAILURE] Launch command failed")
                status = "FAILURE"

        else:
            print("[FAILURE] App install failed")
            status = "FAILURE"

    # Report final test status
    if status == "SUCCESS":
        print("\n[SUCCESS] TimeToRunApplication test completed successfully")
    else:
        print("\n[FAILURE] TimeToRunApplication test failed")
    
    obj.setLoadModuleStatus(status)
    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
