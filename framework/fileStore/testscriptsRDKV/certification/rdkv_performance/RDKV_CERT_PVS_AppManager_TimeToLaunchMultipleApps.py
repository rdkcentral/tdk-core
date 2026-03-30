##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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
from StabilityTestUtility import *
from rdkv_performancelib import *
from web_socket_util import *
import PerformanceTestVariables
import time

# ============================================================
# INITIALIZATION
# ============================================================
obj = tdklib.TDKScriptingLibrary("rdkv_performance", "1", standAlone=True)
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip, port, 'RDKV_CERT_PVS_AppManager_TimeToLaunchMultipleApps')
pre_requisite_reboot(obj, "yes")

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  : %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
Summ_list = []

if expectedResult in result.upper():

    print("\n Check Pre conditions\n")

    final_status = "SUCCESS"

    # ========================================================
    # FETCH MULTIPLE APPS
    # ========================================================
    app_list = PerformanceTestVariables.multiple_application_names
    app_url_list = PerformanceTestVariables.multiple_application_urls

    thunder_port = rdkv_performancelib.devicePort

    # ========================================================
    # EVENT LISTENER
    # ========================================================
    event_listener = createEventListener(
        ip,
        thunder_port,
        ['{"jsonrpc": "2.0","id": 3,"method": "org.rdk.LifecycleManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'],
        "/jsonrpc",
        False
    )

    time.sleep(5)

    # ========================================================
    # LOOP THROUGH APPS
    # ========================================================
    for i in range(len(app_list)):

        if final_status != "SUCCESS":
            break

        app_id = app_list[i]
        app_url = app_url_list[i]

        print(f"\nLaunching App: {app_id}\n")

        # ====================================================
        # START TIMER
        # ====================================================
        start_time = getCurrentTime()

        status = rdkservice_install_launch_app(obj, app_id, app_id, app_url)

        if status != "SUCCESS":
            print(f"{app_id} launch failed")
            final_status = "FAILURE"
            break

        # ====================================================
        # CAPTURE EVENT
        # ====================================================
        continue_count = 0
        end_time = ""

        while True:

            if continue_count > 60:
                break

            if len(event_listener.getEventsBuffer()) == 0:
                time.sleep(1)
                continue_count += 1
                continue

            event = event_listener.getEventsBuffer().pop(0)
            print("\nEvent:", event)

            if app_id in str(event):
                end_time = getCurrentTime()
                break

        if not end_time:
            print(f"Launch event not captured for {app_id}")
            final_status = "FAILURE"
            break

        # ====================================================
        # TIME CALCULATION
        # ====================================================
        start_ms = getTimeInMilliSec(start_time)
        end_ms = getTimeInMilliSec(end_time)

        launch_time = end_ms - start_ms

        print(f"\nTime taken to launch {app_id}: {launch_time} ms")

        Summ_list.append(f"{app_id} launch time: {launch_time} ms")

        # ====================================================
        # THRESHOLD VALIDATION
        # ====================================================
        conf_file, _ = getConfigFileName(obj.realpath)

        _, threshold = getDeviceConfigKeyValue(conf_file, "APP_LAUNCH_THRESHOLD_VALUE")
        _, offset = getDeviceConfigKeyValue(conf_file, "THRESHOLD_OFFSET")

        if threshold and offset:

            if not (0 < launch_time < (int(threshold) + int(offset))):
                print(f"{app_id} launch time exceeded threshold")
                final_status = "FAILURE"

        else:
            print("Threshold not configured")
            final_status = "FAILURE"

        time.sleep(5)

    # ========================================================
    # TERMINATE ALL APPS
    # ========================================================
    print("\nTerminating all apps...\n")

    for app_id in app_list:

        tdkTestObj = obj.createTestStep('rdkservice_terminateApp')
        tdkTestObj.addParameter("appId", app_id)
        tdkTestObj.executeTestCase(expectedResult)

    # ========================================================
    # FINAL STATUS
    # ========================================================
    if final_status == "SUCCESS":
        obj.setLoadModuleStatus("SUCCESS")
    else:
        obj.setLoadModuleStatus("FAILURE")

    # ========================================================
    # CLEANUP
    # ========================================================
    if event_listener:
        event_listener.disconnect()

    getSummary(Summ_list, obj)

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")