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

obj.configureTestCase(ip, port, 'RDKV_CERT_PVS_AppManager_ResourceUsage_Load')
pre_requisite_reboot(obj, "no")

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  : %s" % result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"

if expectedResult in result.upper():

    app_download_url = PerformanceTestVariables.app_download_url
    print("\napp_download_url", app_download_url)
    app_bundle_name = PerformanceTestVariables.app_bundle_name
    print(f"\nApp bundle name: {app_bundle_name}")
    app_name = app_bundle_name.split("+")[0]
    print(f"\nApp name: {app_name}")

    # ========================================================
    # LOAD / ACTIVATE APP
    # ========================================================
    print("\nLoading (activating) app...\n")

    tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
    tdkTestObj.addParameter("plugin", app_id)
    tdkTestObj.addParameter("status", "activate")
    tdkTestObj.executeTestCase(expectedResult)

    result = tdkTestObj.getResult()

    if result == "SUCCESS":
        print("App loaded successfully")
        # ========================================================
        # RESOURCE USAGE VALIDATION
        # ========================================================
        
        print("\nWaiting before validation...\n")
        time.sleep(15)

        print("\nValidating Resource Usage during load...\n")

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
        # DEACTIVATE APP (CLEANUP STEP)
        # ========================================================
        print("\nDeactivating app...\n")

        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin", app_id)
        tdkTestObj.addParameter("status", "deactivate")
        tdkTestObj.executeTestCase(expectedResult)

        if tdkTestObj.getResult() == "SUCCESS":
            print("App deactivated successfully")
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print("App deactivation failed")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("App load failed")
        tdkTestObj.setResultStatus("FAILURE")
    obj.unloadModule("rdkv_performance")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
