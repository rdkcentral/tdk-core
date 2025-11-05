##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
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
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_SANITY_6GHZ_WIFI_CheckSSIDBroadcast</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_SetMultipleParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check 6ghz SSID is broadcasting or not</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>BPI</box_type>
    <!--  -->
    <box_type>Broadband</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_653</test_case_id>
    <test_objective>check whether 6GHZ SSID is broadcasting or not</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband, BPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.{i}.SSID
    Device.WiFi.AccessPoint.{i}.Security.KeyPassphrase</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save ssid name and password of 6GHZ
3. Check whether SSID for 6GHZ are broadcasting or not
5. Revert the values to original value
6.Unload tdkb_e2e module</automation_approch>
    <expected_output>The SSIDs for 6GHZ should broadcast</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_SANITY_6GHZ_WIFI_CheckSSIDBroadcast</test_script>
    <skipped></skipped>
    <release_version>M140</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import time
import tdkbE2EUtility
from tdkbE2EUtility import *

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e", "1")

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_SANITY_6GHZ_WIFI_CheckSSIDBroadcast')

# Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  : {loadmodulestatus}")

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"
    step = 1

    # Parse the device configuration file
    print(f"TEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Should parse the device configuration file successfully")
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Parsed the device configuration file successfully")
        print("[TEST EXECUTION RESULT] : SUCCESS")

        # Assign the WIFI parameters names to a variable
        ssidName_6g = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase_6g = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"

        # Get the value of the wifi parameters that are currently set
        paramList = [ssidName_6g, keyPassPhrase_6g]
        tdkTestObj, status, orgValue = getMultipleParameterValues(obj, paramList)

        step =+ 1
        print(f"TEST STEP {step}: Get the current ssid,keypassphrase of 6GHZ")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase of 6GHZ")

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            setValuesList = [tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd]
            print(f"WIFI parameter values that are set: {setValuesList}")

            list1 = [ssidName_6g, tdkbE2EUtility.ssid_6ghz_name, 'string']
            list2 = [keyPassPhrase_6g, tdkbE2EUtility.ssid_6ghz_pwd, 'string']

            # Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2
            setParamList = "|".join(map(str, setParamList))

            step += 1
            print(f"TEST STEP {step}: Set the ssid,keypassphrase of 6GHZ")
            print(f"EXPECTED RESULT {step}: Should set the ssid,keypassphrase of 6GHZ")

            tdkTestObj, actualresult, details = setMultipleParameterValues(obj, setParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                # Retrieve the values after set and compare
                newParamList = [ssidName_6g, keyPassPhrase_6g]
                tdkTestObj, status, newValues = getMultipleParameterValues(obj, newParamList)

                step += 1
                print(f"TEST STEP {step}: Get the current ssid,keypassphrase of 6GHZ")
                print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase of 6GHZ")

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    # Wait for the changes to reflect in client device
                    time.sleep(60)

                    step += 1
                    print(f"TEST STEP {step}: Check if the SSID name is listed in wifi client")
                    print(f"EXPECTED RESULT {step}: SSID name should be broadcasted and visible in client scan")

                    # Check if the SSID name is listed in wifi client
                    status = wlanIsSSIDAvailable(tdkbE2EUtility.ssid_6ghz_name)
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Network name {tdkbE2EUtility.ssid_6ghz_name} is broadcasted on the network")
                        print("[TEST EXECUTION RESULT] : SUCCESS")
                        finalStatus = "SUCCESS"
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Network name {tdkbE2EUtility.ssid_6ghz_name} is not broadcasted on the network")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")

            # Prepare the list of parameter values to be reverted
            list1 = [ssidName_6g, orgValue[0], 'string']
            list2 = [keyPassPhrase_6g, orgValue[1], 'string']

            revertParamList = list1 + list2
            revertParamList = "|".join(map(str, revertParamList))

            step += 1
            print(f"TEST STEP {step}: Revert ssid,keypassphrase of 6GHZ to original")
            print(f"EXPECTED RESULT {step}: Should set the original ssid,keypassphrase of 6GHZ")

            # Revert the values to original
            tdkTestObj, actualresult, details = setMultipleParameterValues(obj, revertParamList)
            if expectedresult in actualresult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                details = tdkTestObj.getResultDetails()
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print(f" ACTUAL RESULT {step}: Failed to parse the device configuration file")
        print("[TEST EXECUTION RESULT] : FAILURE")

    # Handle any post execution cleanup required
    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")

else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")

