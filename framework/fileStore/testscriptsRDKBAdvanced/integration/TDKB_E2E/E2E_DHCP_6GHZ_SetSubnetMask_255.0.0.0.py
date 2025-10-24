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
  <name>E2E_DHCP_6GHZ_SetSubnetMask_255.0.0.0</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_SetMultipleParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify that on configuring DHCP Server Subnet mask to 255.0.0.0, it gets reflected successfully on the Wi-Fi Client connected via 6GHz radios
</synopsis>
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
    <test_case_id>TC_TDKB_E2E_674</test_case_id>
    <test_objective>Verify that on configuring DHCP Server Subnet mask to 255.0.0.0, it gets reflected successfully on the Wi-Fi Client connected via 6GHz radios
</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband, BPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
    2. TDK Agent should be in a running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.{i}.SSID
Device.WiFi.AccessPoint.{i}.Security.KeyPassphrase
Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress
Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanSubnetMask
Device.DHCPv4.Server.Pool.1.MinAddress
Device.DHCPv4.Server.Pool.1.MaxAddress</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save LanIP,SubnetMask,Maximum and minimum Address range
3. Set LanIP,SubnetMask to 255.0.0.0,Maximum and minimum Address range using tdkb_e2e_SetMultipleParams
4. Connect to the WIFI client and check whether the subnet mask obtained is valid or not
5. Revert the values to original value
6. Unload tdkb_e2e module
</automation_approch>
    <expected_output>The sub net mask obtained should be 255.0.0.0 in connected wifi client</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_DHCP_6GHZ_SetSubnetMask_255.0.0.0</test_script>
    <skipped></skipped>
    <release_version>M141</release_version>
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
# This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,"E2E_DHCP_6GHZ_SetSubnetMask_255.0.0.0")

# Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")


if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"
    step = 1

    print(f"TEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Should successfully parse the device configuration file")
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Parsed the device configuration file successfully")
        print("[TEST EXECUTION RESULT] : SUCCESS")
        step += 1

        # Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"
        lanIPAddress = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
        lanSubnetMask = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanSubnetMask"
        minAddress = "Device.DHCPv4.Server.Pool.1.MinAddress"
        maxAddress = "Device.DHCPv4.Server.Pool.1.MaxAddress"

        # Get the value of the wifi parameters that are currently set.
        print(f"TEST STEP {step}: Get the current ssid, keypassphrase, lanIPAddress, lanSubnetMask, minAddress and maxAddress")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid, keypassphrase, lanIPAddress, lanSubnetMask, minAddress and maxAddress")
        paramList = [ssidName, keyPassPhrase, lanIPAddress, lanSubnetMask, minAddress, maxAddress]
        tdkTestObj, status, orgValue = getMultipleParameterValues(obj, paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Current ssid, keypassphrase, lanIPAddress, lanSubnetMask, minAddress and maxAddress retrived successfully. The values: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")
            step += 1

            # Set the SSID name,password,lanIPAddress,lanSubnetMask,minAddress and maxAddress
            setValuesList = [tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,"10.0.0.1","255.0.0.0","10.0.0.2","10.0.0.253"]
            print(f"Parameter values that are set: {setValuesList}")

            list1 = [ssidName, tdkbE2EUtility.ssid_6ghz_name, "string"]
            list2 = [keyPassPhrase, tdkbE2EUtility.ssid_6ghz_pwd, "string"]
            list3 = [lanIPAddress, "10.0.0.1", "string"]
            list4 = [lanSubnetMask, "255.0.0.0", "string"]
            list5 = [minAddress, "10.0.0.2", "string"]
            list6 = [maxAddress, "10.0.0.253", "string"]

            setParamList = "|".join(map(str, list1 + list2))
            setParamList1 = "|".join(map(str, list3 + list4 + list5 + list6))

            print(f"TEST STEP {step}: Set the ssid, keypassphrase, lanIPAddress, lanSubnetMask, minAddress and maxAddress")
            print(f"EXPECTED RESULT {step}: Should set the ssid, keypassphrase, lanIPAddress, lanSubnetMask, minAddress and maxAddress")
            tdkTestObj, actualresult, details = setMultipleParameterValues(obj, setParamList)
            tdkTestObj, actualresult1, details = setMultipleParameterValues(obj, setParamList1)

            if expectedresult in actualresult and expectedresult in actualresult1:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")
                step += 1

                # Retrieve the values after set and compare
                print(f"TEST STEP {step}: Get the current ssid, keypassphrase, lanIPAddress, lanSubnetMask, minAddress and maxAddress after set")
                print(f"EXPECTED RESULT {step}: Should retrieve the updated values")
                newParamList = [ssidName, keyPassPhrase, lanIPAddress, lanSubnetMask, minAddress, maxAddress]
                tdkTestObj, status, newValues = getMultipleParameterValues(obj, newParamList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: The parameter values after SET: {newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                    step += 1

                    # Wait for the changes to reflect in client device
                    time.sleep(60)

                    # Connect to the wifi ssid from wlan client
                    print(f"TEST STEP {step}: From wlan client, Connect to the wifi ssid")
                    print(f"EXPECTED RESULT {step}: wlan client should connect to the wifi ssid successfully")
                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,tdkbE2EUtility.wlan_6ghz_interface)

                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: wlanConnectWifiSsid SUCCESS")
                        print("[TEST EXECUTION RESULT] : SUCCESS")
                        step += 1

                        # Get the subnetmask of the wlan client after connecting to wifi
                        print(f"TEST STEP {step}: Get the subnetmask of the wlan client after connecting to wifi")
                        print(f"EXPECTED RESULT {step}: Should successfully get the subnetmask")
                        wlanSubnetMask = getWlanSubnetMask(tdkbE2EUtility.wlan_6ghz_interface)
                        if wlanSubnetMask:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: SubnetMask Retrieved successfully")
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                            step += 1

                            # Check whether subnet mask is 255.0.0.0
                            print(f"TEST STEP {step}: Check whether subnet mask is 255.0.0.0")
                            print(f"EXPECTED RESULT {step}: Subnet mask should be 255.0.0.0")
                            if "255.0.0.0" in wlanSubnetMask:
                                status = "SUCCESS"
                            else:
                                status = "FAILURE"
                            if expectedresult in status:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: Subnet mask changed to 255.0.0.0")
                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                step += 1

                                # Disconnect from wifi
                                print(f"TEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                                print(f"EXPECTED RESULT {step}: Should disconnect from the wifi ssid successfully")
                                status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    finalStatus = "SUCCESS"
                                    print(f"ACTUAL RESULT {step}: Disconnect from WIFI SSID SUCCESS")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Disconnect from WIFI SSID FAILED")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Subnet mask is not 255.0.0.0")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to get the Subnet mask")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to connect to WIFI SSID")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: GET operation failed")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")

            # Prepare the list of parameter values to be reverted
            step += 1
            list1 = [ssidName, orgValue[0], "string"]
            list2 = [keyPassPhrase, orgValue[1], "string"]
            list3 = [lanIPAddress, orgValue[2], "string"]
            list4 = [lanSubnetMask, orgValue[3], "string"]
            list5 = [minAddress, orgValue[4], "string"]
            list6 = [maxAddress, orgValue[5], "string"]

            revertParamList = "|".join(map(str, list1 + list2))
            revertParamList1 = "|".join(map(str, list3 + list4 + list5 + list6))

            print(f"TEST STEP {step}: Revert the parameter values to original")
            print(f"EXPECTED RESULT {step}: Should revert the parameter values successfully")
            tdkTestObj, actualresult, details = setMultipleParameterValues(obj, revertParamList)
            tdkTestObj, actualresult1, details = setMultipleParameterValues(obj, revertParamList1)
            if expectedresult in actualresult and expectedresult in actualresult1 and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to get current ssid, keypassphrase, lanIPAddress, lanSubnetMask, minAddress and maxAddress values")
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
