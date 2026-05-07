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
import StabilityTestUtility
from StabilityTestUtility import *
import PerformanceTestVariables
from web_socket_util import *
import rdkv_performancelib
from datetime import datetime, UTC

# Test component
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeToRepeatedLaunch')

expectedResult = "SUCCESS"
Summ_list = []
launch_times = []

# Load module
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

if expectedResult in result.upper():

    status = "SUCCESS"

    # Ensure plugins active
    plugins_list = ["org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager"]
    plugin_status_needed = {"org.rdk.DownloadManager":"activated","org.rdk.PackageManagerRDKEMS":"activated","org.rdk.AppManager":"activated"}

    curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)

    if curr_plugins_status_dict != plugin_status_needed:
        status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)

    if status == "SUCCESS":

        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name = app_bundle_name.split('+')[0]
        print(app_name)
        app_download_url = PerformanceTestVariables.app_download_url

        # Install app once
        status = rdkservice_install_launch_app(obj,app_bundle_name,app_name,app_download_url,launch=False)

        if status == "SUCCESS":

            thunder_port = rdkv_performancelib.devicePort

            # Register event listener once
            event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'],"/jsonrpc",False)

            time.sleep(3)

            print("\nStarting repeated launch test")

            for i in range(3):

                print(f"\nIteration {i+1}: Launching {app_name}")

                # Launch app
                tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                tdkTestObj.addParameter("app_name", app_name)

                start_time = datetime.now(UTC)

                tdkTestObj.executeTestCase(expectedResult)
                status = tdkTestObj.getResult()

                if status != "SUCCESS":
                    print("Launch failed")
                    obj.setTestResult("FAILURE")
                    break

                # Wait for ACTIVE
                continue_count = 0
                launched = False

                while True:
                    if continue_count > 120:
                        print("Timeout waiting for launch event")
                        break

                    if len(event_listener.getEventsBuffer()) == 0:
                        time.sleep(1)
                        continue_count += 1
                        continue

                    event = event_listener.getEventsBuffer().pop(0)
                    print("\nEvent:", event)

                    if app_name in event and "APP_STATE_ACTIVE" in event:
                        launched = True
                        break
                    # Calculate launch time
                    launch_time_str = str(event).split("$$$")[0]

                    end_time = datetime.strptime(launch_time_str, "%H:%M:%S.%f")
                    start_time_dt = datetime.strptime(str(start_time.time()), "%H:%M:%S.%f")

                    time_taken = end_time - start_time_dt
                    time_taken_ms = time_taken.total_seconds() * 1000

                    print(f"Launch time (Iteration {i+1}): {time_taken_ms} ms")

                    launch_times.append(time_taken_ms)

                    #Terminate app
                    print("Terminating app...")

                    tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                    tdkTestObj.addParameter("app_id", app_name)
                    tdkTestObj.executeTestCase(expectedResult)

                    result = tdkTestObj.getResult()

                    if result != "SUCCESS":
                        print("Failed to terminate app")
                        obj.setTestResult("FAILURE")
                    else:
                        #Validate results
                        if len(launch_times) > 0:
                            print("\nAll Launch Times:", launch_times)
                            conf_file, file_status = getConfigFileName(obj.realpath)
                            config_status, launch_threshold = getDeviceConfigKeyValue(conf_file, "APPMANAGER_LAUNCH_THRESHOLD_VALUE")
                            if not launch_threshold:
                                launch_threshold = "3000"
                                config_status, offset = getDeviceConfigKeyValue(conf_file, "THRESHOLD_OFFSET")
                            if not offset:
                                offset = "500"
                            threshold = int(launch_threshold)
                            offset_val = int(offset)
                            all_pass = True
                            for t in launch_times:
                                if not (0 < int(t) < (threshold + offset_val)):
                                    all_pass = False
                                    break
                            Summ_list.append(f"Launch times : {launch_times}")
                            Summ_list.append(f"Threshold : {threshold} ms")
                            if all_pass:
                                print("\nAll launches within threshold")
                                obj.setTestResult("SUCCESS")
                            else:
                                print("\nOne or more launches exceeded threshold")
                                obj.setTestResult("FAILURE")

                if not launched:
                    print("Launch event not received")
                    break

                getSummary(Summ_list, obj)

            event_listener.disconnect()

        else:
            print("App install failed")

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
