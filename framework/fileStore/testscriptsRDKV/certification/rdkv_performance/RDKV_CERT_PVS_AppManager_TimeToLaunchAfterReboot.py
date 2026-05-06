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

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeToLaunchAfterReboot')

expectedResult = "SUCCESS"
Summ_list = []

# Load module
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

if expectedResult in result.upper():

    status = "SUCCESS"

    #Ensure plugins active before install
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

        print("\nEnsuring app is installed before reboot")

        #Install app (no launch)
        status = rdkservice_install_launch_app(obj,app_bundle_name,app_name,app_download_url,launch=False)

        if status == "SUCCESS":

            print("App installed successfully")

            # í´¹ Reboot logic (same as your Lightning script)
            conf_file, file_status = getConfigFileName(obj.realpath)
            result1, rebootwaitTime = getDeviceConfigKeyValue(conf_file, "REBOOT_WAIT_TIME")

            print("\n Rebooting device...")

            tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
            tdkTestObj.addParameter("waitTime", float(rebootwaitTime))

            tdkTestObj.executeTestCase(expectedResult)

            result = tdkTestObj.getResultDetails()

            if expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                print("\n Device is rebooted")

                uptime = get_device_uptime(obj)

                if uptime != -1 and uptime < 280:
                    print("\n Device reboot validated, uptime: {}\n".format(uptime))
                else:
                    print("\n Error validating uptime after reboot")
                    tdkTestObj.setResultStatus("FAILURE")
                    obj.setTestResult("FAILURE")
            else:
                print("\n Error while rebooting the device")
                tdkTestObj.setResultStatus("FAILURE")
                obj.setTestResult("FAILURE")

            #Give some buffer after reboot
            time.sleep(10)

            #Ensure plugins active after reboot
            curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)

            if curr_plugins_status_dict != plugin_status_needed:
                print("Waiting for plugins after reboot...")
                time.sleep(15)
                curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)

            if curr_plugins_status_dict == plugin_status_needed:

                print("\nRegistering lifecycle events")

                thunder_port = rdkv_performancelib.devicePort
                event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'],"/jsonrpc",False)

                time.sleep(3)

                print(f"\nLaunching {app_name} after reboot")

                tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                tdkTestObj.addParameter("app_name", app_name)

                #Start time (only launch measurement)
                start_time = datetime.now(UTC)

                tdkTestObj.executeTestCase(expectedResult)

                status = tdkTestObj.getResult()

                if status == "SUCCESS":

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
                            print("Received launch event")
                            launched = True
                            break

                    if launched:

                        launch_time_str = str(event).split("$$$")[0]

                        end_time = datetime.strptime(launch_time_str, "%H:%M:%S.%f")
                        start_time_dt = datetime.strptime(str(start_time.time()), "%H:%M:%S.%f")

                        time_taken = end_time - start_time_dt
                        time_taken_ms = time_taken.total_seconds() * 1000

                        print("\nTime taken to launch after reboot: {} ms".format(time_taken_ms))

                        # í´¹ Threshold logic
                        config_status, launch_threshold = getDeviceConfigKeyValue(conf_file, "APPMANAGER_LAUNCH_AFTER_REBOOT_THRESHOLD")

                        if not launch_threshold:
                            print("Threshold not found, using default (5000 ms)")
                            launch_threshold = "5000"

                        config_status, offset = getDeviceConfigKeyValue(conf_file, "THRESHOLD_OFFSET")

                        if not offset:
                            offset = "500"

                        threshold = int(launch_threshold)
                        offset_val = int(offset)

                        Summ_list.append(f"LAUNCH_AFTER_REBOOT_THRESHOLD : {threshold} ms")
                        Summ_list.append(f"OFFSET : {offset_val} ms")
                        Summ_list.append(f"Time taken : {time_taken_ms} ms")

                        if 0 < int(time_taken_ms) < (threshold + offset_val):
                            print("\nLaunch after reboot within threshold")
                        else:
                            print("\nLaunch after reboot exceeded threshold")

                        getSummary(Summ_list, obj)

                    else:
                        print("Failed to receive launch event")
                        obj.setTestResult("FAILURE")

                else:
                    print("Launch failed")
                    obj.setTestResult("FAILURE")

                event_listener.disconnect()

            else:
                print("Plugins not active after reboot")
                obj.setTestResult("FAILURE")

        else:
            print("App installation failed")

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
