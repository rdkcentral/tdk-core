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
import tdklib
import json
import ast
import time
from rdkv_basic_sanitylib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True);

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_Reboot_Validation');

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result.upper())

expectedResult = "SUCCESS"

if expectedResult in result.upper():

    # Fetch SSH_PORT from device config (needed for port-down check)
    tdkTestObj = obj.createTestStep('rdkv_basic_sanity_getDeviceConfig')
    tdkTestObj.addParameter("basePath", obj.realpath)
    tdkTestObj.addParameter("configKey", json.dumps(["SSH_PORT"]))
    tdkTestObj.executeTestCase(expectedResult)
    configRaw = str(tdkTestObj.getResultDetails()).strip()
    configValues = {}
    try:
        configValues = ast.literal_eval(configRaw)
        failed_keys = [k for k, v in configValues.items() if "FAILURE" in str(v) or str(v).strip() == ""]
        for k, v in configValues.items():
            print("{} : {}".format(k, v))
        if failed_keys:
            for k in failed_keys:
                print("FAILURE: Failed to retrieve %s from device config" % k)
            tdkTestObj.setResultStatus("FAILURE")
            result = "FAILURE"
        else:
            print("SUCCESS: Successfully retrieved all device config values")
            tdkTestObj.setResultStatus("SUCCESS")
    except Exception as e:
        print("FAILURE: Could not parse device config response: {}".format(e))
        tdkTestObj.setResultStatus("FAILURE")
        result = "FAILURE"

    if "FAILURE" != result:
        SSH_PORT = configValues["SSH_PORT"]

        # ==============================================================
        # STEP 1: Reboot device via Thunder + verify onRebootRequest event
        # ==============================================================
        tdkTestObj = obj.createTestStep('rdkv_basic_sanity_rebootDevice')
        tdkTestObj.executeTestCase(expectedResult)
        result  = tdkTestObj.getResult()
        details = str(tdkTestObj.getResultDetails()).strip()
        print("[STEP 1 - Reboot Device] : %s" % details)
        if result == "SUCCESS" and "FAILURE" not in details:
            reboot_event_time = time.time()
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            result = "FAILURE"

        # Wait for device to begin rebooting before checking port status
        if "FAILURE" != result:
            print("INFO: Waiting 3s before checking device status...")
            time.sleep(3)

        # ==============================================================
        # STEP 2: Verify device is down (SSH port + Thunder port both inaccessible)
        # ==============================================================
        if "FAILURE" not in details:
            tdkTestObj = obj.createTestStep('rdkv_basic_sanity_deviceStatus')
            tdkTestObj.addParameter("expectedStatus", "down")
            tdkTestObj.addParameter("sshPort", SSH_PORT)
            tdkTestObj.executeTestCase(expectedResult)
            result  = tdkTestObj.getResult()
            details = str(tdkTestObj.getResultDetails()).strip()
            print("[STEP 2 - Device Down Check] : %s" % details)
            if result == "SUCCESS" and "FAILURE" not in details:
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                result = "FAILURE"

        # ==============================================================
        # STEP 3: Wait for device to come back up (Thunder port accessible)
        # ==============================================================
        if "FAILURE" not in details:
            tdkTestObj = obj.createTestStep('rdkv_basic_sanity_deviceStatus')
            tdkTestObj.addParameter("expectedStatus", "up")
            tdkTestObj.addParameter("sshPort", SSH_PORT)
            tdkTestObj.executeTestCase(expectedResult)
            result  = tdkTestObj.getResult()
            details = str(tdkTestObj.getResultDetails()).strip()
            print("[STEP 3 - Device Up Check] : %s" % details)
            if result == "SUCCESS" and "FAILURE" not in details:
                recovery_secs = time.time() - reboot_event_time
                print("INFO: Device recovery time (onRebootRequest -> port up): {:.1f}s".format(recovery_secs))
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                result = "FAILURE"

        # ==============================================================
        # STEP 4: Get system uptime and verify device freshly rebooted (< 30 secs)
        # ==============================================================
        if "FAILURE" not in details:
            tdkTestObj = obj.createTestStep('rdkv_basic_sanity_getSystemUptime')
            tdkTestObj.executeTestCase(expectedResult)
            result      = tdkTestObj.getResult()
            uptime_str  = str(tdkTestObj.getResultDetails()).strip()
            print("[STEP 4 - System Uptime] : %s" % uptime_str)
            if result != "SUCCESS" or "FAILURE" in uptime_str:
                print("FAILURE: Could not retrieve system uptime")
                tdkTestObj.setResultStatus("FAILURE")
            else:
                try:
                    uptime_secs = float(uptime_str)
                    if uptime_secs < 30:
                        print("SUCCESS: System uptime is {:.1f}s - device has freshly rebooted".format(uptime_secs))
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("FAILURE: System uptime is {:.1f}s - expected < 30s after reboot".format(uptime_secs))
                        tdkTestObj.setResultStatus("FAILURE")
                except ValueError:
                    print("FAILURE: Could not parse uptime value: {}".format(uptime_str))
                    tdkTestObj.setResultStatus("FAILURE")
    else:
        print("FAILURE: Failed to get SSH_PORT from device config")
        tdkTestObj.setResultStatus("FAILURE")

    obj.unloadModule("rdkv_basic_sanity")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("FAILURE: Failed to load module")
