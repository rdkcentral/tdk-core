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
  <name>E2E_WIFI_6GHZ_WPA3Personal_PingRouterPublicIP</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_SetMultipleParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify that ICMP traffic from a wireless client to router's public ip is successful when the wireless client is associated using WPA3-Personal authentication on the 6 GHz band.</synopsis>
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
    <test_case_id>TC_TDKB_E2E_660</test_case_id>
    <test_objective>Verify that ICMP traffic from a wireless client to router's public ip is successful when the wireless client is associated using WPA3-Personal authentication on the 6 GHz band.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband, BPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.{i}.SSID
Device.WiFi.AccessPoint.{i}.Security.KeyPassphrase
Device.WiFi.AccessPoint.{i}.Security.ModeEnabled</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save security mode
3. Set the security mode for 6GHz to WPA3-Personal if Security mode is not WPA3-Personal using tdkb_e2e_SetMultipleParams
4. Using tdkb_e2e_Get, get and save the current gateway ip address
5. Connect the WiFi client to the 6GHZ SSID  of gateway
6. Check if the WiFi client's ip received from gateway is in valid range
7. From WLAN client check if ping to gateway's public ip is success or not
8. Disconnect the WiFi client
9. Unload tdkb_e2e module</automation_approch>
    <expected_output>Ping should be success between wlan client and gateway's public ip address when the security mode for 6GHz is set to WPA3-Personal</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WIFI_6GHZ_WPA3Personal_PingRouterPublicIP</test_script>
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
import tdkutility
from tdkutility import *

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e", "1")
wifi_obj = tdklib.TDKScriptingLibrary("wifiagent","1")


# IP and Port of box, No need to change,
# This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_WPA3Personal_PingRouterPublicIP')
wifi_obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_WPA3Personal_PingRouterPublicIP')


# Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
loadmodulestatus1 = wifi_obj.getLoadModuleResult()

print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus1}")

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS")
    wifi_obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"
    step = 1
    exit_flag = 0
    sm_flag = 0

    # Parse the device configuration file
    print(f"TEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Device configuration file should be parsed successfully")
    status = tdkbE2EUtility.parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Parsed the device configuration file successfully")
        print("[TEST EXECUTION RESULT] : SUCCESS")

        # Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"
        securityMode = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.ModeEnabled"

        # Get the value of the wifi parameters that are currently set.
        paramList = [ssidName, keyPassPhrase, securityMode]
        step += 1
        print(f"TEST STEP {step}: Get the current ssid, keypassphrase and securityMode")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid, keypassphrase and securityMode")
        tdkTestObj,status,orgValue = tdkbE2EUtility.getMultipleParameterValues(obj, paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            initial_secMode = orgValue[2]

            # Check and change Security Mode to WPA3-Personal if not already
            if initial_secMode != "WPA3-Personal":
                step += 1
                print(f"\nTEST STEP {step}: Get the initial security configuration")
                print(f"EXPECTED RESULT {step}: Should successfully get initial security configuration")
                initial_config = {}
                tdkTestObj, actualresult, initial_config = tdkutility.getSecurityModeEnabledConfig(wifi_obj, initial_secMode, tdkbE2EUtility.ssid_6ghz_index)

                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Initial security configuration retrieved successfully")
                    print("TEST EXECUTION RESULT : SUCCESS")

                    # Set the security mode to WPA3-Personal
                    step += 1
                    print(f"\nTEST STEP {step}: Set security mode to WPA3-Personal")
                    print(f"EXPECTED RESULT {step}: Should set security mode to WPA3-Personal")
                    SAE_Pass = "asdf@1234"  # test values not real secrets
                    Encryption_Mode = "AES"
                    config_SET = {
                        f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.SAEPassphrase": SAE_Pass,
                        f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.X_CISCO_COM_EncryptionMethod": Encryption_Mode
                    }
                    tdkTestObj, actualresult = tdkutility.setSecurityModeEnabledConfig(wifi_obj, "WPA3-Personal", tdkbE2EUtility.ssid_6ghz_index, config_SET, initial_secMode)
                    details = tdkTestObj.getResultDetails()

                    if expectedresult in actualresult:
                        sm_flag = 1
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Security mode changed to WPA3-Personal. Details: {details}")
                        print("TEST EXECUTION RESULT : SUCCESS")

                        time.sleep(2)
                        # Validate the security mode with get
                        step += 1
                        print(f"\nTEST STEP {step}: Get the Security Mode and check it is changed to WPA3-Personal")
                        print(f"EXPECTED RESULT {step}: Should successfully set security mode to WPA3-Personal")
                        tdkTestObj = wifi_obj.createTestStep("WIFIAgent_Get")
                        tdkTestObj.addParameter("paramName", f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.ModeEnabled")
                        tdkTestObj.executeTestCase(expectedresult)
                        actualresult = tdkTestObj.getResult()
                        details = tdkTestObj.getResultDetails()

                        if expectedresult in actualresult and details != "":
                            sec_mode = details.split("VALUE:")[1].split(' ')[0].split(',')[0]
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Security Mode: {sec_mode}")
                            print("TEST EXECUTION RESULT : SUCCESS")

                            if sec_mode != "WPA3-Personal":
                                tdkTestObj.setResultStatus("FAILURE")
                                print("Security mode is not WPA3-Personal")
                                exit_flag = 1
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Get operation failed. Details: {details}")
                            print("TEST EXECUTION RESULT : FAILURE")
                            exit_flag = 1
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to set security mode to WPA3-Personal. Details: {details}")
                        print("TEST EXECUTION RESULT : FAILURE")
                        exit_flag = 1
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Failed to retrieve Initial security configuration")
                    print("TEST EXECUTION RESULT : FAILURE")
                    exit_flag = 1
            else:
                print(f"\nChanging Security mode not required as Current security mode is {initial_secMode}")

            if exit_flag != 1:
                # Set ssid and password for 6ghz
                setValuesList = [tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd]
                print(f"WIFI parameter values that are set: {setValuesList}")

                list1 = [ssidName, tdkbE2EUtility.ssid_6ghz_name, 'string']
                list2 = [keyPassPhrase, tdkbE2EUtility.ssid_6ghz_pwd, 'string']

                # Concatenate the lists with the elements separated by pipe
                setParamList = list1 + list2
                setParamList = "|".join(map(str, setParamList))

                step += 1
                print(f"TEST STEP {step}: Set the ssid and keypassphrase")
                print(f"EXPECTED RESULT {step}: Should set the ssid and keypassphrase")
                tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj, setParamList)
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    # Retrieve the values after set and compare
                    newParamList = [ssidName, keyPassPhrase]
                    step += 1
                    print(f"TEST STEP {step}: Get the current ssid and keypassphrase")
                    print(f"EXPECTED RESULT {step}: Retrieved values should match the set values")
                    tdkTestObj,status,newValues = tdkbE2EUtility.getMultipleParameterValues(obj, newParamList)

                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: {newValues}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        # Wait for the changes to reflect in client device
                        time.sleep(60)

                        # Connect to the wifi ssid from wlan client
                        step += 1
                        print(f"TEST STEP {step}: From wlan client, Connect to the wifi ssid")
                        print(f"EXPECTED RESULT {step}: WLAN client should connect to wifi successfully")
                        status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd, tdkbE2EUtility.wlan_6ghz_interface)
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: WLAN client connected successfully")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            # Get wlan IP address
                            step += 1
                            print(f"TEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                            print(f"EXPECTED RESULT {step}: WLAN client should get a valid IP address")
                            wlanIP = tdkbE2EUtility.getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)
                            if wlanIP:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: WLAN IP = {wlanIP}")
                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                # Get Gateway IP address
                                step += 1
                                print(f"TEST STEP {step}: Get the current LAN IP address DHCP range")
                                print(f"EXPECTED RESULT {step}: Should retrieve the LAN IP Address DHCP range")
                                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                tdkTestObj,status,curIPAddress = tdkbE2EUtility.getParameterValue(obj, param)

                                if expectedresult in status and curIPAddress:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: LAN IP Address:{curIPAddress}")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    # Check WLAN IP in same DHCP range
                                    step += 1
                                    print(f"TEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                                    print(f"EXPECTED RESULT {step}: WLAN IP should be in same DHCP range as GW")
                                    status = tdkbE2EUtility.checkIpRange(curIPAddress, wlanIP)
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: WLAN IP is in DHCP range")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        # Ping from WLAN to router's public ip
                                        step += 1
                                        print(f"TEST STEP {step}: Check the PING from WLAN to router's public ip")
                                        print(f"EXPECTED RESULT {step}: PING should be successful")
                                        status = tdkbE2EUtility.verifyNetworkConnectivity(tdkbE2EUtility.gw_wan_ip, "PING", wlanIP, curIPAddress)
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step}: Ping successful from WLAN to router's public ip")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                            finalStatus = "SUCCESS"
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: Ping failed from WLAN to router's public ip")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: WLAN IP not in DHCP range")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Failed to get LAN IP Address")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to get WLAN IP")
                                print("[TEST EXECUTION RESULT] : FAILURE")

                            # Disconnect WLAN
                            step += 1
                            print(f"TEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                            print(f"EXPECTED RESULT {step}: WLAN client should disconnect successfully")
                            status = tdkbE2EUtility.wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                            if expectedresult in status:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: WLAN disconnected successfully")
                                print("[TEST EXECUTION RESULT] : SUCCESS")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: WLAN disconnect failed")
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

                #Revert operation for security mode
                if sm_flag == 1:
                    print("Reverting to initial Security Mode...")
                    step += 1
                    tdkTestObj, actualresult = tdkutility.setSecurityModeEnabledConfig(wifi_obj, initial_secMode, tdkbE2EUtility.ssid_6ghz_index, initial_config, sec_mode)
                    details = tdkTestObj.getResultDetails()

                    step += 1
                    print(f"\nTEST STEP {step} : Revert Security Mode to initial security mode : {initial_secMode}")
                    print(f"EXPECTED RESULT {step} : Reverting to initial security mode should be success")

                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step} : Reverting Mode to initial value was successful Details : {details}")
                        print("TEST EXECUTION RESULT : SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step} : Reverting Mode to initial value was NOT successful Details : {details}")
                        print("TEST EXECUTION RESULT : FAILURE")
                else:
                    print("\nReverting Security Mode not required...")

                # Revert values back
                list1 = [ssidName, orgValue[0], 'string']
                list2 = [keyPassPhrase, orgValue[1], 'string']

                if sm_flag == 1:
                    revertParamList = list1
                else:
                    revertParamList = list1 + list2
                revertParamList = "|".join(map(str, revertParamList))

                step += 1
                print(f"TEST STEP {step}: Revert to original ssid and keypassphrase")
                print(f"EXPECTED RESULT {step}: Should set the original values back successfully")
                tdkTestObj, actualresult, details = tdkbE2EUtility.setMultipleParameterValues(obj, revertParamList)
                if expectedresult in actualresult and "SUCCESS" in finalStatus:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    details = tdkTestObj.getResultDetails()
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                print("Not proceding further due to security mode change failure")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to parse the device configuration file")
        print("[TEST EXECUTION RESULT] : FAILURE")

    # Handle any post execution cleanup required
    tdkbE2EUtility.postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")
    wifi_obj.unloadModule("wifiagent")

else:
    print("Failed to load tdkb_e2e and wifi module")
    obj.setLoadModuleStatus("FAILURE")
    wifi_obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")
