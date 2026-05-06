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
import rdkv_performancelib

obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

# IP and Port of box, No need to change,
# This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_CERT_PVS_AppManager_ResourceUsage_AppStartupVsIdle')

# The device will reboot before starting the performance testing if
# "pre_req_reboot_pvs" is configured as "Yes"
pre_requisite_reboot(obj,"yes")

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"

if expectedResult in result.upper():

    status = "SUCCESS"

    print("\n===== Measuring Idle Resource Usage =====")

    # Allow system to stabilize
    time.sleep(10)

    # ------------------- Idle Resource Measurement -------------------
    tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
    tdkTestObj.executeTestCase(expectedResult)

    idle_status = tdkTestObj.getResult()
    idle_details = tdkTestObj.getResultDetails()

    if expectedResult in idle_status and idle_details != "ERROR":

        print(f"\n[IDLE] Resource Usage: {idle_details}")
        tdkTestObj.setResultStatus("SUCCESS")

        print("\n===== Launching App for Startup Measurement =====")

        plugins_list = ["org.rdk.AppManager"]
        plugin_status_needed = {"org.rdk.AppManager":"activated"}

        curr_plugins_status_dict = StabilityTestUtility.get_plugins_status(obj,plugins_list)

        if curr_plugins_status_dict != plugin_status_needed:
            status = StabilityTestUtility.set_plugins_status(obj,plugin_status_needed)
            time.sleep(10)

        if status == "SUCCESS":

            app_bundle_name = PerformanceTestVariables.google_bundle
            app_name = app_bundle_name.split('+')[0]

            print(f"\nApp Name: {app_name}")

            app_download_url = PerformanceTestVariables.app_download_url
            app_download_url = app_download_url + "/" + app_bundle_name

            # ------------------- Install and Launch App -------------------
            status = rdkservice_install_launch_app(
                obj,
                app_bundle_name,
                app_name,
                app_download_url,
                launch=True
            )

            if status == "SUCCESS":

                print("\nApp Install and Launch was successful")

                # Allow app startup stabilization
                time.sleep(10)

                # ------------------- Startup Resource Measurement -------------------
                print("\nCapturing resource usage during startup...")

                tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                tdkTestObj.executeTestCase(expectedResult)

                startup_status = tdkTestObj.getResult()
                startup_details = tdkTestObj.getResultDetails()

                if expectedResult in startup_status and startup_details != "ERROR":

                    print(f"\n[STARTUP] Resource Usage: {startup_details}")
                    tdkTestObj.setResultStatus("SUCCESS")

                    # ------------------- Comparison Logic -------------------
                    print("\n===== Comparing Startup vs Idle Resource Usage =====")

                    print(f"\nIdle Resource Usage   : {idle_details}")
                    print(f"Startup Resource Usage: {startup_details}")

                    if startup_details != idle_details:

                        print("\nStartup resource usage differs from idle state")
                        print("Comparison validation successful")
                        tdkTestObj.setResultStatus("SUCCESS")

                    else:

                        print("\nStartup resource usage is same as idle state")
                        print("Unexpected behavior observed")
                        tdkTestObj.setResultStatus("FAILURE")

                else:

                    print("\nFailed to capture startup resource usage")
                    tdkTestObj.setResultStatus("FAILURE")

                # ------------------- Terminate App -------------------
                print(f"\nTerminating app: {app_name}")

                tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                tdkTestObj.addParameter("app_id", app_name)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    print("App terminated successfully")
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print("Unable to terminate the app")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("\nFailed to install and launch app")
        else:
            print("\nAppManager is not active")
    else:

        print("\nFailed to get idle resource usage")
        tdkTestObj.setResultStatus("FAILURE")
        obj.setLoadModuleStatus("FAILURE")

    obj.unloadModule("rdkv_performance")
else:

    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
