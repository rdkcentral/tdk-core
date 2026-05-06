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
from web_socket_util import *
import rdkv_performancelib
from datetime import datetime, UTC

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeToTerminateFromBackground')

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
Summ_list = []

if expectedResult in result.upper():

    status ="SUCCESS"

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

        app_bundle_1 = PerformanceTestVariables.google_bundle
        app_A = app_bundle_1.split('+')[0]
        print("\napp_A")
        app_bundle_2 = PerformanceTestVariables.keytest_bundle
        app_B = app_bundle_2.split('+')[0]
        print("\napp_B")
        app_url = PerformanceTestVariables.app_download_url

        # Ensure apps installed
        rdkservice_install_launch_app(obj, app_bundle_1, app_A, app_url, launch=False)
        rdkservice_install_launch_app(obj, app_bundle_2, app_B, app_url, launch=False)

        thunder_port = rdkv_performancelib.devicePort

        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'],"/jsonrpc",False)

        time.sleep(3)

        # 🔹 Step 1: Launch App A
        print("\nLaunching App A")
        tdkTestObj = obj.createTestStep('rdkservice_launch_app')
        tdkTestObj.addParameter("app_name", app_A)
        tdkTestObj.executeTestCase(expectedResult)

        # Wait ACTIVE
        while True:
            if len(event_listener.getEventsBuffer()) == 0:
                time.sleep(1)
                continue
            event = event_listener.getEventsBuffer().pop(0)
            if app_A in event and "APP_STATE_ACTIVE" in event:
                print("App A ACTIVE")
                break

        time.sleep(10)

        #Step 2: Launch App B → A goes background
        print("\nLaunching App B")
        tdkTestObj = obj.createTestStep('rdkservice_launch_app')
        tdkTestObj.addParameter("app_name", app_B)
        tdkTestObj.executeTestCase(expectedResult)

        background = False

        while True:
            if len(event_listener.getEventsBuffer()) == 0:
                time.sleep(1)
                continue
            event = event_listener.getEventsBuffer().pop(0)
            if app_A in event and ("APP_STATE_BACKGROUND" in event or "APP_STATE_SUSPENDED" in event):
                print("App A moved to background")
                background = True
                break

        if not background:
            print("Failed to push App A to background")
            obj.setTestResult("FAILURE")

        time.sleep(2)

        # Clear old events
        event_listener.getEventsBuffer().clear()

        #Step 3: Terminate from background
        print("\nTerminating App A from background")

        start_time = datetime.now(UTC).time()

        tdkTestObj = obj.createTestStep('rdkv_terminate_app')
        tdkTestObj.addParameter("app_id", app_A)
        tdkTestObj.executeTestCase(expectedResult)

        continue_count = 0
        terminated = False

        while True:
            if continue_count > 120:
                print("Timeout waiting for destroy event")
                break

            if len(event_listener.getEventsBuffer()) == 0:
                time.sleep(1)
                continue_count += 1
                continue

            event = event_listener.getEventsBuffer().pop(0)
            print("\nEvent:", event)

            if app_A in event and "APP_STATE_DESTROYED" in event:
                print("App destroyed successfully")
                terminated = True
                break

        if terminated:

            destroy_time = str(event).split("$$$")[0]

            start_dt = datetime.strptime(str(start_time), "%H:%M:%S.%f")
            end_dt = datetime.strptime(str(destroy_time), "%H:%M:%S.%f")

            time_taken = end_dt - start_dt
            time_taken_ms = time_taken.total_seconds() * 1000

            print("\nTime taken to terminate from background: {} ms".format(time_taken_ms))

            # Threshold
            conf_file, file_status = getConfigFileName(obj.realpath)

            _, threshold = getDeviceConfigKeyValue(conf_file,"APPMANAGER_TERMINATE_THRESHOLD_VALUE")
            _, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")

            if not threshold:
                threshold = "2000"
            if not offset:
                offset = "10"

            allowed_time = int(threshold) + int(offset)

            print(f"\nThreshold : {threshold} ms")
            print(f"Offset    : {offset} ms")
            print(f"Allowed   : {allowed_time} ms")

            if 0 < int(time_taken_ms) < allowed_time:
                print("\nTerminate within expected range")
                print(f"Measured: {time_taken_ms} ms | Allowed: {allowed_time} ms")
                obj.setTestResult("SUCCESS")
            else:
                diff = int(time_taken_ms) - allowed_time
                print("\nTerminate exceeded threshold")
                print(f"Measured : {time_taken_ms} ms")
                print(f"Allowed  : {allowed_time} ms")
                print(f"Exceeded by: {diff} ms")
                obj.setTestResult("FAILURE")

            Summ_list.append(f"Time taken : {time_taken_ms} ms")
            Summ_list.append(f"Allowed time : {allowed_time} ms")

            getSummary(Summ_list, obj)

        else:
            print("Terminate event not received")
            obj.setTestResult("FAILURE")

        event_listener.disconnect()

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
