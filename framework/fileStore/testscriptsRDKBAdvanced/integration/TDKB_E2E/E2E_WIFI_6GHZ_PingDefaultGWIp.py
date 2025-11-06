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
  <name>E2E_WIFI_6GHZ_PingDefaultGWIp</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_SetMultipleParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify that ping from 6GHZ WLAN client to Default GW ip (like,10.0.0.1) is success</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <test_case_id>TC_TDKB_E2E_656</test_case_id>
    <test_objective>Verify that ping from 6GHZ WLAN client to Default GW ip (like,10.0.0.1) is success</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband, BPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.{i}.SSID
    Device.WiFi.AccessPoint.{i}.Security.KeyPassphrase</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save the default gateway ip address
3. Connect the WiFi client to the 6GHZ SSID  of gateway
4. Check if the WiFi client's ip received from gateway is in valid range
5. From WLAN client check if ping to gateway's default ip is success or not
6. Disconnect the WiFi client
7. Unload tdkb_e2e module</automation_approch>
    <expected_output>Ping from WLAN client to gateway's default ip should be success</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WIFI_6GHZ_PingDefaultGWIp</test_script>
    <skipped></skipped>
    <release_version>M140</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import time
from tdkbE2EUtility import *
import tdkbE2EUtility

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e", "1")

# IP and Port of box, No need to change
# This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_PingDefaultGWIp')

# Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
step = 1
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"

    # Parse the device configuration file
    print(f"TEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Should successfully parse the device configuration file")
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Parsed the device configuration file successfully")
        print("[TEST EXECUTION RESULT] : SUCCESS")

        # Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"

        # Get the value of the wifi parameters that are currently set.
        step += 1
        paramList = [ssidName, keyPassPhrase]
        tdkTestObj, status, orgValue = getMultipleParameterValues(obj, paramList)

        print(f"TEST STEP {step}: Get the current value of ssid and keypassphrase")
        print(f"EXPECTED RESULT {step}: Should retrieve the current value of ssid and keypassphrase")
        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            setValuesList = [tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd]
            print(f"WIFI parameter values that are set: {setValuesList}")

            list1 = [ssidName, tdkbE2EUtility.ssid_6ghz_name, 'string']
            list2 = [keyPassPhrase, tdkbE2EUtility.ssid_6ghz_pwd, 'string']

            # Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2
            setParamList = "|".join(map(str, setParamList))

            step += 1
            tdkTestObj, actualresult, details = setMultipleParameterValues(obj, setParamList)
            print(f"TEST STEP {step}: Set the ssid and keypassphrase")
            print(f"EXPECTED RESULT {step}: Should set the ssid and keypassphrase")
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                # Retrieve the values after set and compare
                step += 1
                newParamList = [ssidName, keyPassPhrase]
                tdkTestObj, status, newValues = getMultipleParameterValues(obj, newParamList)
                print(f"TEST STEP {step}: Get the current ssid and keypassphrase after set")
                print(f"EXPECTED RESULT {step}: Retrieved values should match the set values")

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    # Wait for the changes to reflect in client device
                    time.sleep(60)

                    # Connect to the wifi ssid from wlan client
                    step += 1
                    print(f"TEST STEP {step}: From wlan client, Connect to the wifi ssid")
                    print(f"EXPECTED RESULT {step}: WLAN client should connect to the wifi ssid successfully")
                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd, tdkbE2EUtility.wlan_6ghz_interface)
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: WLAN client connected successfully")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        # Get WLAN IP
                        step += 1
                        print(f"TEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                        print(f"EXPECTED RESULT {step}: Should retrieve a wlan client IP address")
                        wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)
                        if wlanIP:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: WLAN IP is {wlanIP}")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            # Get LAN IP
                            step += 1
                            print(f"TEST STEP {step}: Get the current LAN IP address DHCP range")
                            print(f"EXPECTED RESULT {step}: Should retrieve the current LAN IP address")
                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                            tdkTestObj, status, curIPAddress = getParameterValue(obj, param)
                            if expectedresult in status and curIPAddress:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: LAN IP Address is {curIPAddress}")
                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                # Check IP range
                                step += 1
                                print(f"TEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                                print(f"EXPECTED RESULT {step}: WLAN IP should be in same DHCP range as LAN")
                                status = checkIpRange(curIPAddress, wlanIP)
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: WLAN IP is in same DHCP range")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    # Ping test
                                    step += 1
                                    print(f"TEST STEP {step}: Check the PING from WLAN to default GW IP")
                                    print(f"EXPECTED RESULT {step}: PING should be successful")
                                    status = verifyNetworkConnectivity(curIPAddress, "PING", wlanIP, curIPAddress)
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: verifyNetworkConnectivity SUCCESS")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")
                                        finalStatus = "SUCCESS"
                                        print("Ping successful from WLAN client to default gateway ip")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: Ping not successful from WLAN client to default gateway ip")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: WLAN IP not in same DHCP range")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to get current LAN IP address DHCP range")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to get WLAN IP address after connection")
                            print("[TEST EXECUTION RESULT] : FAILURE")

                        # Disconnect wifi
                        step += 1
                        print(f"TEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                        print(f"EXPECTED RESULT {step}: WLAN client should disconnect successfully")
                        status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: WiFi disconnected successfully")
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: WiFi disconnect failed")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: WLAN client failed to connect to wifi ssid")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Retrieved values {newValues} do not match set values {setValuesList}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                details = tdkTestObj.getResultDetails()
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")

            # Revert values
            step += 1
            print(f"TEST STEP {step}: Revert ssid and keypassphrase to original values")
            print(f"EXPECTED RESULT {step}: Should revert the ssid and keypassphrase successfully")
            list1 = [ssidName, orgValue[0], 'string']
            list2 = [keyPassPhrase, orgValue[1], 'string']
            revertParamList = list1 + list2
            revertParamList = "|".join(map(str, revertParamList))

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
        print(f"ACTUAL RESULT {step}: Failed to parse the device configuration file")
        print("[TEST EXECUTION RESULT] : FAILURE")

    # Handle any post execution cleanup required
    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")

else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")
