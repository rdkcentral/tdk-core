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

# Test component
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeToRepeatedLaunch')

expectedResult = "SUCCESS"
launch_times = []

# Load module
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

if expectedResult in result.upper():

    status = "SUCCESS"

    # Ensure plugins active
    essential_plugins = ["org.rdk.DownloadManager", "org.rdk.AppPackageManager", "org.rdk.AppManager"]
    
    plugin_status_needed = {p: "activated" for p in essential_plugins}
    
    print(f"[INFO] Activating plugins: {essential_plugins}")
    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj, essential_plugins)

    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj, plugin_status_needed)
        time.sleep(10)

    if status == "SUCCESS":

        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name = app_bundle_name.split('+')[0]
        print(app_name)
        app_download_url = PerformanceTestVariables.app_download_url

        # INSTALL APP
        print("\n[INFO] Installing app")
        
        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name, app_download_url, launch=False)

        if status == "SUCCESS":
            print("[SUCCESS] App installation successful")

            print("\n[INFO] Starting repeated launch test (3 iterations)")

            # LOOP: 3 iterations of launch/terminate
            for i in range(3):
                iter_num = i + 1
                print(f"\n{'='*60}")
                print(f"[ITERATION {iter_num}] Launching {app_name}")
                print(f"{'='*60}")

                # Capture start time
                start_time = datetime.now(UTC)

                # LAUNCH APP - Test Step (per iteration)
                tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                tdkTestObj.addParameter("app_name", app_name)
                tdkTestObj.executeTestCase(expectedResult)
                
                launch_result = tdkTestObj.getResult()
                if launch_result != "SUCCESS":
                    print(f"[FAILURE] Launch command failed at iteration {iter_num}")
                    tdkTestObj.setResultStatus("FAILURE")
                    break

                print(f"[INFO] Launch command executed, waiting for app to fully load")
                
                # Wait for app to load
                time.sleep(10)
                
                # Capture end time
                end_time = datetime.now(UTC)
                
                # Calculate launch time
                time_taken = end_time - start_time
                launch_time_ms = time_taken.total_seconds() * 1000
                
                if launch_time_ms > 0:
                    print(f"[SUCCESS] Launch time (Iteration {iter_num}): {launch_time_ms} ms")
                    launch_times.append(launch_time_ms)
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print(f"[ERROR] Invalid launch time (≤0): {launch_time_ms} ms")
                    tdkTestObj.setResultStatus("FAILURE")
                    break

                # TERMINATE APP - Test Step (per iteration)
                print(f"[INFO] Terminating app...")
                tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                tdkTestObj.addParameter("app_id", app_name)
                
                tdkTestObj.executeTestCase(expectedResult)
                terminate_result = tdkTestObj.getResult()

                if terminate_result != "SUCCESS":
                    print(f"[FAILURE] Failed to terminate app at iteration {iter_num}")
                    tdkTestObj.setResultStatus("FAILURE")
                    break
                else:
                    print(f"[SUCCESS] App terminated successfully")
                    tdkTestObj.setResultStatus("SUCCESS")
                    time.sleep(2)  # Wait before next iteration

            # VALIDATION - After all iterations
            print(f"\n{'='*60}")
            print("VALIDATION RESULTS")
            print(f"{'='*60}")
            
            if len(launch_times) == 3:
                print(f"All 3 Launch Times: {launch_times}")
                
                # Suppress stdout for utility function calls
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                
                conf_file, file_status = getConfigFileName(obj.realpath)
                config_status, launch_threshold = getDeviceConfigKeyValue(conf_file, "APPMANAGER_LAUNCH_THRESHOLD_VALUE")
                if not launch_threshold:
                    launch_threshold = "3000"
                
                config_status, offset = getDeviceConfigKeyValue(conf_file, "THRESHOLD_OFFSET")
                if not offset:
                    offset = "500"
                
                # Restore stdout
                sys.stdout = old_stdout
                
                threshold = int(launch_threshold)
                offset_val = int(offset)
                threshold_max = threshold + offset_val
                
                all_pass = True
                for idx, t in enumerate(launch_times):
                    within_threshold = (0 < t < threshold_max)
                    status_str = "PASS" if within_threshold else "FAIL"
                    print(f"Iteration {idx + 1}: {t} ms [{status_str}] (threshold: 0 < time < {threshold_max})")
                    if not within_threshold:
                        all_pass = False
                
                if all_pass:
                    print("\n[SUCCESS] All launches within threshold - VALIDATION PASSED")
                else:
                    print("\n[FAILURE] One or more launches exceeded threshold - VALIDATION FAILED")
            
            else:
                print(f"\n[FAILURE] Expected 3 successful launches, got {len(launch_times)}")

        else:
            print("[FAILURE] App installation failed")

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
