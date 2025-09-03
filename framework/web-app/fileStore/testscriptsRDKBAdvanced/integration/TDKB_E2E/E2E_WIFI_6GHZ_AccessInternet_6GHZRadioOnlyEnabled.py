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
  <name>E2E_WIFI_6GHZ_AccessInternet_6GHZRadioOnlyEnabled</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_SetMultipleParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify that wireless client is able to connect to WG and access internet when 6GHz radio is enabled and 5GHZ,2.4GHZ radio is disabled in WG</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <test_case_id>TC_TDKB_E2E_655</test_case_id>
    <test_objective>To check if the wifi connection to 6GHz SSID is success or not</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband, BPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.{i}.SSID
Device.WiFi.AccessPoint.{i}.Security.KeyPassphrase
Device.WiFi.Radio.{i}.Enable
Device.WiFi.Radio.{i}.Enable
Device.WiFi.Radio.{i}.Enable</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save ssid name and password of 6GHZ
3. Check whether SSID for 6GHZ is broadcasting and able to connect to SSID
5. Revert the values to original value
6.Unload tdkb_e2e module</automation_approch>
    <expected_output>The SSID 6GHZ should broadcast and should be able to connect to it</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WIFI_6GHZ_AccessInternet_6GHZRadioOnlyEnabled</test_script>
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
obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_AccessInternet_6GHZRadioOnlyEnabled')

# Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")

step = 1

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"

    # Parse the device configuration file
    print(f"TEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Should parse the device configuration file successfully")
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Device configuration file parsed successfully")
        print("[TEST EXECUTION RESULT] : SUCCESS")

        step += 1
        # Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"
        RadioEnable_2ghz = f"Device.WiFi.Radio.{tdkbE2EUtility.radio_2ghz_index}.Enable"
        RadioEnable_5ghz = f"Device.WiFi.Radio.{tdkbE2EUtility.radio_5ghz_index}.Enable"
        RadioEnable_6ghz = f"Device.WiFi.Radio.{tdkbE2EUtility.radio_6ghz_index}.Enable"

        # Get the value of the wifi parameters that are currently set.
        paramList = [ssidName, keyPassPhrase, RadioEnable_2ghz, RadioEnable_5ghz, RadioEnable_6ghz]
        print(f"TEST STEP {step}: Get the current ssid, keypassphrase, 2ghz, 5ghz and 6ghz Radio enable status")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid, keypassphrase, 2ghz, 5ghz and 6ghz Radio enable status")
        tdkTestObj, status, orgValue = getMultipleParameterValues(obj, paramList)
        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            step += 1
            # Set the SSID name,password,2ghz, 5ghz and 6ghz Radio enable status
            setValuesList = [tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,'false','false','true']
            print(f"WIFI parameter values that are set: {setValuesList}")

            list1 = [ssidName,tdkbE2EUtility.ssid_6ghz_name,'string']
            list2 = [keyPassPhrase,tdkbE2EUtility.ssid_6ghz_pwd,'string']
            list3 = [RadioEnable_2ghz,'false','bool']
            list4 = [RadioEnable_5ghz,'false','bool']
            list5 = [RadioEnable_6ghz,'true','bool']

            setParamList = list1 + list2 + list3 + list4 + list5
            setParamList = "|".join(map(str, setParamList))

            print(f"TEST STEP {step}: Set the ssid, keypassphrase, 2ghz, 5ghz and 6ghz Radio enable status")
            print(f"EXPECTED RESULT {step}: Should set the ssid, keypassphrase, 2ghz, 5ghz and 6ghz Radio enable status")
            tdkTestObj, actualresult, details = setMultipleParameterValues(obj, setParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                step += 1
                # Retrieve the values after set and compare
                newParamList = [ssidName, keyPassPhrase, RadioEnable_2ghz, RadioEnable_5ghz, RadioEnable_6ghz]
                print(f"TEST STEP {step}: Get the ssid, keypassphrase, 2ghz, 5ghz and 6ghz Radio enable status after set")
                print(f"EXPECTED RESULT {step}: Retrieved values should match the set values")
                tdkTestObj, status, newValues = getMultipleParameterValues(obj, newParamList)
                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    # Wait for changes to reflect
                    time.sleep(60)

                    step += 1
                    # Connect to the wifi ssid from wlan client
                    print(f"TEST STEP {step}: Connect to the wifi ssid from wlan client")
                    print(f"EXPECTED RESULT {step}: WLAN client should connect to the wifi ssid successfully")
                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,tdkbE2EUtility.wlan_6ghz_interface)
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: WLAN client connected successfully")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        step += 1
                        # Get the IP address of the wlan client after connecting to wifi
                        print(f"TEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                        print(f"EXPECTED RESULT {step}: Should retrieve wlan client IP address")
                        wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)
                        if wlanIP:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: WLAN IP is {wlanIP}")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            step += 1
                            # Get LAN IP address
                            print(f"TEST STEP {step}: Get the current LAN IP address DHCP range")
                            print(f"EXPECTED RESULT {step}: Should retrieve LAN IP address successfully")
                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                            tdkTestObj, status, curIPAddress = getParameterValue(obj, param)
                            if expectedresult in status and curIPAddress:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: LAN IP Address is {curIPAddress}")
                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                step += 1
                                # Check IP range
                                print(f"TEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                                print(f"EXPECTED RESULT {step}: WLAN IP should be in same DHCP range as LAN IP")
                                status = checkIpRange(curIPAddress, wlanIP)
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: WLAN IP is in DHCP range")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    step += 1
                                    # Verify network connectivity
                                    print(f"TEST STEP {step}: Verify WLAN client is able to access Internet")
                                    print(f"EXPECTED RESULT {step}: WLAN client should have Internet access")
                                    status = verifyNetworkConnectivity(tdkbE2EUtility.network_ip, "PING_TO_HOST", wlanIP, curIPAddress, "WLAN_6G")
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: Internet access verified successfully")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        step += 1
                                        # Disconnect WLAN client
                                        print(f"TEST STEP {step}: Disconnect WLAN client from the wifi ssid")
                                        print(f"EXPECTED RESULT {step}: WLAN client should disconnect successfully")
                                        status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            finalStatus = "SUCCESS"
                                            print(f"ACTUAL RESULT {step}: WLAN disconnected successfully")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: WLAN disconnect failed")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: Internet access failed")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: WLAN IP not in DHCP range")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to retrieve LAN IP Address")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to get WLAN IP")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: WLAN client failed to connect")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")

            # Revert values to original
            list1 = [ssidName, orgValue[0], 'string']
            list2 = [keyPassPhrase, orgValue[1], 'string']
            list3 = [RadioEnable_2ghz, orgValue[2], 'bool']
            list4 = [RadioEnable_5ghz, orgValue[3], 'bool']
            list5 = [RadioEnable_6ghz, orgValue[4], 'bool']

            revertParamList = list1 + list2 + list3 + list4 + list5
            revertParamList = "|".join(map(str, revertParamList))

            step += 1
            print(f"TEST STEP {step}: Revert the wifi parameters to original values")
            print(f"EXPECTED RESULT {step}: Original wifi parameters should be restored")
            tdkTestObj, actualresult, details = setMultipleParameterValues(obj, revertParamList)
            if expectedresult in actualresult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
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

