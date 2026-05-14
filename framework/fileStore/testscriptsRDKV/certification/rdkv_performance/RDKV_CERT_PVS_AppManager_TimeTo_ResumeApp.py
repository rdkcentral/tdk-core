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

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeToResumeApp')

pre_requisite_reboot(obj,"no")

expectedResult = "SUCCESS"
Summ_list = []

# Load module
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

if expectedResult in result.upper():

    status = "SUCCESS"

    # ---------------- Plugin Validation ----------------
    plugins_list = [
        "org.rdk.DownloadManager",
        "org.rdk.PackageManagerRDKEMS",
        "org.rdk.AppManager"
    ]

    plugin_status_needed = {
        "org.rdk.DownloadManager":"activated",
        "org.rdk.PackageManagerRDKEMS":"activated",
        "org.rdk.AppManager":"activated"
    }

    curr_plugins_status_dict = get_plugins_status(obj, plugins_list)

    if curr_plugins_status_dict != plugin_status_needed:
        status = set_plugins_status(obj, plugin_status_needed)
        time.sleep(10)

    if status == "SUCCESS":


        app_bundle_1 = PerformanceTestVariables.google_bundle
        app1_name = app_bundle_1.split('+')[0]
        app_bundle_2 = PerformanceTestVariables.keytest_bundle
        app2_name_name = app_bundle_2.split('+')[0]
        app_download_url = PerformanceTestVariables.app_download_url
        
        print("\nInstalling apps")
        rdkservice_install_launch_app(obj,app_bundle_1,app1_name,app_download_url,launch=False)
        rdkservice_install_launch_app(obj,_bundle,app2_name,app_download_url,launch=False)

        # ---------------- Event Listener ----------------
        thunder_port = rdkv_performancelib.devicePort
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'],"/jsonrpc",False)
        time.sleep(3)

        # ---------------- Launch App A ----------------
        print(f"\nLaunching {app1_name}")

        tdkTestObj = obj.createTestStep('rdkservice_launch_app')
        tdkTestObj.addParameter("app_name", app1_name)
        tdkTestObj.executeTestCase(expectedResult)

        # Wait ACTIVE
        while True:

            if len(event_listener.getEventsBuffer()) == 0:
                time.sleep(1)
                continue

            event = event_listener.getEventsBuffer().pop(0)

            print("\nEvent:", event)

            if app1_name in event and "APP_STATE_ACTIVE" in event:
                print("App A ACTIVE")
                break

        time.sleep(2)

        # ---------------- Launch App B ----------------
        print(f"\nLaunching {app2_name}")

        tdkTestObj = obj.createTestStep('rdkservice_launch_app')
        tdkTestObj.addParameter("app_name", app2_name)
        tdkTestObj.executeTestCase(expectedResult)

        background = False

        while True:

            if len(event_listener.getEventsBuffer()) == 0:
                time.sleep(1)
                continue

            event = event_listener.getEventsBuffer().pop(0)

            print("\nEvent:", event)

            if app1_name in event and (
                "APP_STATE_BACKGROUND" in event or
                "APP_STATE_SUSPENDED" in event
            ):
                print("App A moved to background")
                background = True
                break

        if not background:
            print("\nFailed to move App A to background")
            obj.setTestResult("FAILURE")
            event_listener.disconnect()
            obj.unloadModule("rdkv_performance")
            exit()

        time.sleep(2)

        # ---------------- Clear Buffer ----------------
        event_listener.getEventsBuffer().clear()

        # ---------------- Resume App A ----------------
        print(f"\nResuming {app1_name}")

        tdkTestObj = obj.createTestStep('rdkservice_launch_app')
        tdkTestObj.addParameter("app_name", app1_name)

        start_time = datetime.now(UTC).time()

        tdkTestObj.executeTestCase(expectedResult)

        continue_count = 0
        resumed = False
        event = ""

        while True:

            if continue_count > 120:
                print("\nTimeout waiting for resume event")
                obj.setTestResult("FAILURE")
                break

            if len(event_listener.getEventsBuffer()) == 0:
                time.sleep(1)
                continue_count += 1
                continue

            event = event_listener.getEventsBuffer().pop(0)

            print("\nEvent:", event)

            if app1_name in event and "APP_STATE_ACTIVE" in event:
                resumed = True
                print("App resumed successfully")
                break

        if resumed:

            resume_time = str(event).split("$$$")[0]

            start_dt = datetime.strptime(str(start_time), "%H:%M:%S.%f")
            end_dt = datetime.strptime(str(resume_time), "%H:%M:%S.%f")

            time_taken = end_dt - start_dt
            time_taken_ms = time_taken.total_seconds() * 1000

            print("\nTime taken to resume app: {} ms".format(time_taken_ms))

            # ---------------- Threshold ----------------
            conf_file, _ = getConfigFileName(obj.realpath)

            _, threshold = getDeviceConfigKeyValue(conf_file,"APPMANAGER_LAUNCH_THRESHOLD_VALUE")
            _, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
            if not threshold:
                threshold = "2000"

            if not offset:
                offset = "10"

            allowed_time = int(threshold) + int(offset)

            print(f"\nThreshold : {threshold} ms")
            print(f"Offset    : {offset} ms")
            print(f"Allowed   : {allowed_time} ms")

            # ---------------- Validation ----------------
            if 0 < int(time_taken_ms) < allowed_time:

                print("\nResume time within expected range")
                print(f"Measured: {time_taken_ms} ms | Allowed: {allowed_time} ms")

                obj.setTestResult("SUCCESS")

            else:

                diff = int(time_taken_ms) - allowed_time

                print("\nResume time exceeded threshold")
                print(f"Measured : {time_taken_ms} ms")
                print(f"Allowed  : {allowed_time} ms")
                print(f"Exceeded by: {diff} ms")

                obj.setTestResult("FAILURE")

            Summ_list.append(f"Resume time : {time_taken_ms} ms")
            Summ_list.append(f"Allowed time : {allowed_time} ms")

            getSummary(Summ_list, obj)

        # ---------------- Cleanup ----------------
        print("\nCleaning up apps")

        for app in [app1_name, app2_name]:

            tdkTestObj = obj.createTestStep('rdkv_terminate_app')
            tdkTestObj.addParameter("app_id", app)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if result == "SUCCESS":
                print("App terminated successfully")
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("Unable to terminate the app")
                tdkTestObj.setResultStatus("FAILURE")

        event_listener.disconnect()

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
