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

obj.configureTestCase(ip, port, 'RDKV_CERT_PVS_AppManager_TimeToRelaunchApp')
pre_requisite_reboot(obj, "yes")

# ============================================================
# LOAD MODULE
# ============================================================
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  : %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
Summ_list = []

if expectedResult in result.upper():

    print("\n Check Pre conditions\n")

    final_status = "SUCCESS"

    # ========================================================
    # FETCH APP DETAILS
    # ========================================================
    app_id = PerformanceTestVariables.primary_app_name
    app_url = PerformanceTestVariables.primary_app_url

    thunder_port = rdkv_performancelib.devicePort

    # ========================================================
    # EVENT LISTENER
    # ========================================================
    event_listener = createEventListener(
        ip,
        thunder_port,
        ['{"jsonrpc": "2.0","id": 7,"method": "org.rdk.LifecycleManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'],
        "/jsonrpc",
        False
    )

    time.sleep(5)

    # ========================================================
    # INITIAL LAUNCH (PRE-CONDITION)
    # ========================================================
    print("\nLaunching app (initial)...\n")

    status = rdkservice_install_launch_app(obj, app_id, app_id, app_url)

    if status != "SUCCESS":
        print("Initial launch failed")
        final_status = "FAILURE"

    # ========================================================
    # TERMINATE APP
    # ========================================================
    if final_status == "SUCCESS":

        print("\nTerminating app before relaunch...\n")

        tdkTestObj = obj.createTestStep('rdkservice_terminateApp')
        tdkTestObj.addParameter("appId", app_id)
        tdkTestObj.executeTestCase(expectedResult)

        if tdkTestObj.getResult() != "SUCCESS":
            print("Failed to terminate app")
            final_status = "FAILURE"

        time.sleep(5)

    # ========================================================
    # RELAUNCH (START TIMER)
    # ========================================================
    if final_status == "SUCCESS":

        print("\nRelaunching app...\n")

        start_time = getCurrentTime()

        status = rdkservice_install_launch_app(obj, app_id, app_id, app_url)

        if status != "SUCCESS":
            print("Relaunch failed")
            final_status = "FAILURE"

    # ========================================================
    # CAPTURE EVENT
    # ========================================================
    if final_status == "SUCCESS":

        print("\nWaiting for relaunch event...\n")

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
            print("\nRelaunch event not captured\n")
            final_status = "FAILURE"

    # ========================================================
    # TIME CALCULATION
    # ========================================================
    if final_status == "SUCCESS":

        start_ms = getTimeInMilliSec(start_time)
        end_ms = getTimeInMilliSec(end_time)

        relaunch_time = end_ms - start_ms

        print("\nTime taken to relaunch app: {} ms".format(relaunch_time))

        Summ_list.append("Relaunch time: {} ms".format(relaunch_time))

        # ====================================================
        # THRESHOLD VALIDATION
        # ====================================================
        conf_file, _ = getConfigFileName(obj.realpath)

        _, threshold = getDeviceConfigKeyValue(conf_file, "APP_LAUNCH_THRESHOLD_VALUE")
        _, offset = getDeviceConfigKeyValue(conf_file, "THRESHOLD_OFFSET")

        if threshold and offset:

            print("\nThreshold: {} ms".format(threshold))

            if 0 < relaunch_time < (int(threshold) + int(offset)):
                print("\nRelaunch time within threshold\n")
            else:
                print("\nRelaunch time exceeded threshold\n")
                final_status = "FAILURE"
        else:
            print("\nThreshold not configured\n")
            final_status = "FAILURE"

    # ========================================================
    # TERMINATE APP (FINAL CLEANUP)
    # ========================================================
    print("\nFinal termination of app...\n")

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