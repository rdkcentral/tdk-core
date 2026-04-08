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
import json
import time

obj = tdklib.TDKScriptingLibrary("rdkv_performance", "1", standAlone=True)
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip, port, 'RDKV_CERT_PVS_AppManager_ResourceUsage_MultipleAppsActive')
pre_requisite_reboot(obj, "no")

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  : %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"

if expectedResult in result.upper():

    print("\n Check Pre conditions\n")

    # Configure multiple apps
    app_list = multiple_application_names
    app_url_list = multiple_application_urls

    launched_apps = []

    # ========================================================
    # INSTALL + LAUNCH MULTIPLE APPS
    # ========================================================
    print("\nLaunching multiple apps...\n")

    for i in range(len(app_list)):

        app_id = app_list[i]
        app_download_url = app_url_list[i]

        print(f"\nProcessing App: {app_id}\n")

        status = rdkservice_install_launch_app(obj, app_id, app_id, app_download_url)

        if status == "SUCCESS":
            print(f"App {app_id} installed and launched")
            launched_apps.append(app_id)

            # ========================================================
            # RESOURCE USAGE VALIDATION
            # ========================================================
            print("\nWaiting for system stabilization...\n")
            time.sleep(20)

            print("\nValidating Resource Usage with multiple apps active...\n")
            
            tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
            tdkTestObj.executeTestCase(expectedResult)

            result = tdkTestObj.getResult()
            resource_usage = tdkTestObj.getResultDetails()

            if expectedResult in result and resource_usage != "ERROR":
                print("\nResource usage validated successfully\n")
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("\nResource usage validation failed\n")
                tdkTestObj.setResultStatus("FAILURE")

            # ========================================================
            # TERMINATE ALL APPS
            # ========================================================
            print("\nTerminating all launched apps...\n")

            for app_id in launched_apps:
                tdkTestObj = obj.createTestStep('rdkservice_terminateApp')
                tdkTestObj.addParameter("appId", app_id)
                tdkTestObj.executeTestCase(expectedResult)

                if tdkTestObj.getResult() == "SUCCESS":
                    print(f"App {app_id} terminated successfully")
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print(f"Failed to terminate {app_id}")
                    tdkTestObj.setResultStatus("FAILURE")

        else:
            print(f"Failed to install/launch {app_id}")
            final_status = "FAILURE"
            break

        # Delay to simulate realistic multi-app scenario
        time.sleep(5)

    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
