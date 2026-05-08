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
# use tdklib library,which provides a wrapper for tdk testcase script 
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

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_TimeToLaunch_InstalledApp')

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
Summ_list = []

if expectedResult in result.upper():

    status ="SUCCESS"

    print("\nCheck the status of AppManagers in the device")

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

        app_bundle_name = PerformanceTestVariables.google_bundle
        app_name = app_bundle_name.split('+')[0]
        print(app_name)
        app_download_url = PerformanceTestVariables.app_download_url

        print("\nEnsuring app is already installed")

        # Install once (not part of timing)
        status = rdkservice_install_launch_app(obj,app_bundle_name,app_name,app_download_url,launch=False)

        if status == "SUCCESS":

            print("App is installed successfully")

            print("Register for the launch event")

            thunder_port = rdkv_performancelib.devicePort

            event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}'],"/jsonrpc",False)

            time.sleep(5)

            print(f"\nLaunching installed app {app_name}")

            tdkTestObj = obj.createTestStep('rdkservice_launch_app')
            tdkTestObj.addParameter("app_name", app_name)

            start_time = datetime.now(UTC).time()

            tdkTestObj.executeTestCase(expectedResult)

            status = tdkTestObj.getResult()

            if status == "SUCCESS":

                continue_count = 0

                while True:
                    if continue_count > 120:
                        break

                    if len(event_listener.getEventsBuffer()) == 0:
                        time.sleep(1)
                        continue_count += 1
                        continue

                    event = event_listener.getEventsBuffer().pop(0)
                    print("\nEvent:", event)

                    if app_name in event and "APP_STATE_ACTIVE" in event:
                        print("Received launch event")
                        break   

                if "APP_STATE_ACTIVE" in event:

                    launch_time = str(event).split("$$$")[0]

                    launch_start_time = datetime.strptime(str(start_time), "%H:%M:%S.%f")
                    launched_time = datetime.strptime(str(launch_time), "%H:%M:%S.%f")

                    conf_file, file_status = getConfigFileName(obj.realpath)

                    config_status, launch_threshold = getDeviceConfigKeyValue(conf_file, "APPMANAGER_LAUNCH_THRESHOLD_VALUE")

                    config_status, launch_offset = getDeviceConfigKeyValue(conf_file, "THRESHOLD_OFFSET")

                    # fallback
                    if not launch_threshold:
                        launch_threshold = "2000"
                    if not launch_offset:
                        launch_offset = "10"

                    allowed_time = int(launch_threshold) + int(launch_offset)

                    time_taken_for_launch = launched_time - launch_start_time
                    time_taken_for_launch = time_taken_for_launch.total_seconds() * 1000

                    print("\nLaunch initiated at ", start_time)
                    print("\nLaunch completed at ", launch_time)
                    print("\nTime taken to launch installed app : {} (ms)".format(time_taken_for_launch))

                    Summ_list.append('APP_LAUNCH_THRESHOLD_VALUE :{}ms'.format(launch_threshold))
                    Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(launch_offset))
                    Summ_list.append('Time taken :{}ms'.format(time_taken_for_launch))
                    Summ_list.append('Allowed time :{}ms'.format(allowed_time))

                    print("\nThreshold value: {} ms".format(launch_threshold))
                    print("Offset value: {} ms".format(launch_offset))

                    # í´¹ Improved Validation Logging
                    if 0 < int(time_taken_for_launch) < allowed_time:
                        print("\nTime taken for launching the app is within the expected range")
                        print(f"Measured: {time_taken_for_launch} ms | Allowed: {allowed_time} ms")
                        tdkTestObj.setResultStatus("SUCCESS")
                        event_listener.disconnect()
                    else:
                        diff = int(time_taken_for_launch) - allowed_time

                        print("\nTime taken for launching the app is NOT within the expected range")
                        print(f"Measured : {time_taken_for_launch} ms")
                        print(f"Allowed  : {allowed_time} ms")
                        print(f"Exceeded by: {diff} ms")

                        Summ_list.append('Exceeded by :{}ms'.format(diff))

                        tdkTestObj.setResultStatus("FAILURE")

                    getSummary(Summ_list, obj)

                else:
                    print("Failed to receive launch event")
                    tdkTestObj.setResultStatus("FAILURE")

                # Cleanup
                print("\nTerminating the app")

                tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                tdkTestObj.addParameter("app_id", app_name)
                tdkTestObj.executeTestCase(expectedResult)


            else:
                print("Failed to launch app")
                tdkTestObj.setResultStatus("FAILURE")

        else:
            print("Failed to install app")

    else:
        print("Plugins not active")
        obj.setLoadModuleStatus("FAILURE")

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
