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

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeTo_CloseApp')

expectedResult = "SUCCESS"
Summ_list = []

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

        # Install + Launch
        status = rdkservice_install_launch_app(obj,app_bundle_name,app_name,app_download_url,launch=True)

        if status == "SUCCESS":

            print("\nRegistering lifecycle events")

            thunder_port = rdkv_performancelib.devicePort

            event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'],"/jsonrpc",False)

            time.sleep(3)

            print(f"\nClosing {app_name}")

            # Start time
            start_time = datetime.now(UTC)

            #Close using your lib function
            tdkTestObj = obj.createTestStep('rdkservice_close_app')
            tdkTestObj.addParameter("app_id", app_name)
            tdkTestObj.executeTestCase(expectedResult)
            if tdkTestObj.getResult() != "SUCCESS":
                print("Failed to send close command")
            else:
                print("App closed successfully")
                time.sleep(10)  # allow cleanup
                continue_count = 0
                closed = False

                while True:
                    if continue_count > 120:
                        print("Timeout waiting for close event")
                        break

                    if len(event_listener.getEventsBuffer()) == 0:
                        time.sleep(1)
                        continue_count += 1
                        continue

                    event = event_listener.getEventsBuffer().pop(0)
                    print("\nEvent:", event)

                    if app_name in event and "APP_STATE_DESTROYED" in event:
                        print("Received close event")
                        closed = True
                        break

                if closed:

                    close_time_str = str(event).split("$$$")[0]

                    end_time = datetime.strptime(close_time_str, "%H:%M:%S.%f")
                    start_time_dt = datetime.strptime(str(start_time.time()), "%H:%M:%S.%f")

                    time_taken = end_time - start_time_dt
                    time_taken_ms = time_taken.total_seconds() * 1000

                    print("\nTime taken to close app: {} ms".format(time_taken_ms))

                    # Threshold
                    conf_file, file_status = getConfigFileName(obj.realpath)

                    config_status, close_threshold = getDeviceConfigKeyValue(conf_file, "APPMANAGER_CLOSE_THRESHOLD_VALUE")

                    if not close_threshold:
                        print("Close threshold not found, using default (2000 ms)")
                        close_threshold = "2000"

                    config_status, offset = getDeviceConfigKeyValue(conf_file, "THRESHOLD_OFFSET")

                    if not offset:
                        offset = "500"

                    threshold = int(close_threshold)
                    offset_val = int(offset)

                    Summ_list.append(f"CLOSE_THRESHOLD : {threshold} ms")
                    Summ_list.append(f"OFFSET : {offset_val} ms")
                    Summ_list.append(f"Time taken : {time_taken_ms} ms")

                    if 0 < int(time_taken_ms) < (threshold + offset_val):
                        print("\nClose time within threshold")
                        obj.setTestResult("SUCCESS")
                    else:
                        print("\nClose time exceeded threshold")
                        obj.setTestResult("FAILURE")

                    getSummary(Summ_list, obj)


                else:
                    print("Failed to receive close event")
                    obj.setTestResult("FAILURE")

            event_listener.disconnect()


        else:
            print("Install/Launch failed")

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
