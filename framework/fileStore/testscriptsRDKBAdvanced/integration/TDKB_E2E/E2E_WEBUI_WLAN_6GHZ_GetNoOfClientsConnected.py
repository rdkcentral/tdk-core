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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_WEBUI_WLAN_6GHZ_GetNoOfClientsConnected</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_SetMultipleParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check if the number of clients connected to WLAN using 6GHZ is successfully updated in UI.</synopsis>
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
    <test_case_id>TC_TDKB_E2E_677</test_case_id>
    <test_objective>Check if the number of clients connected to WLAN using 6GHZ is successfully updated in UI.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband, BPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
    2. TDK Agent should be in a running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.{i}.SSID
Device.WiFi.AccessPoint.{i}.Security.KeyPassphrase
Device.WiFi.AccessPoint.{i}.AssociatedDeviceNumberOfEntries</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Import selenium module
3. Start selenium hub in TM machine
4. Start Node in wlan client machine
5. From Wlan clinet connect to 6GHZ SSID
6. check if the wlan client has the ip in dhcp range
7. Try to access the WEBUI of the gateway using selenium grid
8. Validate if the UI page is accessible or not
9. Try to login to the page with credentials
10. Validate if login is success or not
11. Check if the number of clients connected to 6GHZ WiFi network is updated in UI or not.
12. Kill selenium hub and node
13. unload module</automation_approch>
    <expected_output>Number of clients connected to 6GHZ WiFi network should to updated successfully in UI</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WEBUI_WLAN_6GHZ_GetNoOfClientsConnected</test_script>
    <skipped></skipped>
    <release_version>M141</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import time
import tdkbE2EUtility
from tdkbE2EUtility import *
import tdkbWEBUIUtility
from tdkbWEBUIUtility import *

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e", "1")

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WEBUI_WLAN_6GHZ_GetNoOfClientsConnected')

# Get the result of connection with test component and STB
loadmodulestatus = obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")

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
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"
        noOfClientsConnected = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.AssociatedDeviceNumberOfEntries"

        # Get the value of the wifi parameters that are currently set.
        paramList = [ssidName, keyPassPhrase, noOfClientsConnected]
        step += 1
        print(f"TEST STEP {step}: Get the current ssid, keypassphrase and number of clients connected to WLAN 6GHZ")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid, keypassphrase and clients connected count")
        tdkTestObj, status, orgValue = getMultipleParameterValues(obj, paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Current ssid, keypassphrase and number of clients connected retrived successfully. The values: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            # Set ssid and keypassphrase
            setValuesList = [tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd]
            print(f"WIFI parameter values that are set: {setValuesList}")

            list1 = [ssidName, tdkbE2EUtility.ssid_6ghz_name, 'string']
            list2 = [keyPassPhrase, tdkbE2EUtility.ssid_6ghz_pwd, 'string']

            setParamList = "|".join(map(str, list1 + list2))

            step += 1
            print(f"TEST STEP {step}: Set the ssid and keypassphrase")
            print(f"EXPECTED RESULT {step}: Should set the ssid and keypassphrase")
            tdkTestObj, actualresult, details = setMultipleParameterValues(obj, setParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                # Retrieve the values after set and compare
                newParamList = [ssidName, keyPassPhrase]
                step += 1
                print(f"TEST STEP {step}: Get the current ssid and keypassphrase after set")
                print(f"EXPECTED RESULT {step}: Should retrieve the current ssid and keypassphrase")
                tdkTestObj, status, newValues = getMultipleParameterValues(obj, newParamList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: The parameter values after SET: {newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    # Wait for the changes to reflect in client device
                    time.sleep(60)

                    # Set Selenium grid
                    step += 1
                    print(f"TEST STEP {step}: Start Selenium grid")
                    print(f"EXPECTED RESULT {step}: Should star Selenium grid successfully")
                    driver, status = startSeleniumGrid(tdkTestObj, "WLAN", tdkbE2EUtility.grid_url)
                    if status == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Selenium grid set successfully")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        # Connect to the wifi ssid from wlan client
                        step += 1
                        print(f"TEST STEP {step}: From wlan client, Connect to the wifi ssid")
                        print(f"EXPECTED RESULT {step}: WLAN client should connect to the wifi ssid")
                        status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,tdkbE2EUtility.wlan_6ghz_interface)
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: WLAN client connected successfully")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            # Get the IP address of wlan client
                            step += 1
                            print(f"TEST STEP {step}: Get the IP address of the wlan client after connecting")
                            print(f"EXPECTED RESULT {step}: Should retrieve a valid wlan IP address")
                            wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)
                            if wlanIP:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: wlan IP is {wlanIP}")
                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                # Get LAN IP
                                step += 1
                                print(f"TEST STEP {step}: Get the current LAN IP address DHCP range")
                                print(f"EXPECTED RESULT {step}: Should retrieve LAN IP address")
                                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                tdkTestObj, status, curIPAddress = getParameterValue(obj, param)

                                if expectedresult in status and curIPAddress:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: LAN IP {curIPAddress}")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    # Check DHCP range
                                    step += 1
                                    print(f"TEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                                    print(f"EXPECTED RESULT {step}: WLAN IP should be in the same DHCP range")
                                    status = checkIpRange(curIPAddress, wlanIP)
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: WLAN IP {wlanIP} is in DHCP range")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        # Login to WebUI and validate number of connected clients
                                        step += 1
                                        print(f"TEST STEP {step}: Login to Local WebUI and get No of clients connected count")
                                        print(f"EXPECTED RESULT {step}: Should login to UI and get No of clients connected count")
                                        status, driver = openLocalWebUI(tdkbE2EUtility.grid_url, tdkTestObj, "LocalLogin")
                                        if status == "SUCCESS":
                                            try:
                                                time.sleep(5)
                                                driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/ul/li[1]/ul/li[2]/a").click()
                                                driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/ul/li[1]/ul/li[2]/ul/li[1]/a").click()
                                                num = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div[3]/div[3]/div[4]/span[2]").text
                                                print(f"ACTUAL RESULT {step}: Number of clients connected to WiFi network: {num}")

                                                if int(num) == int(orgValue[2]) + 1:
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    print("[TEST EXECUTION RESULT] : SUCCESS")
                                                    print("Number of clients connected to WiFi network is successfully updated")
                                                    finalStatus = "SUCCESS"
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                                    print("Failed to update the number of clients connected")
                                            except Exception as error:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(error)
                                            time.sleep(10)
                                            driver.quit()
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: Failed to Login WebUI")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}:wlan IP address is not in DHCP range")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Failed to get gateway LAN IP")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to get the wlan IP address")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to connect wlan client to the wifi ssid")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to set Selenium grid")
                        print("[TEST EXECUTION RESULT] : FAILURE")

                    # Kill selenium hub and node
                    step += 1
                    print(f"TEST STEP {step}: Kill selenium hub and node")
                    print(f"EXPECTED RESULT {step}: Should kill selenium hub and node successfully")
                    status = tdkbWEBUIUtility.kill_hub_node("WLAN")
                    if status == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Post-requisite success")
                        print("[TEST EXECUTION RESULT] : SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Couldn't kill node and hub")
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
            list1 = [ssidName, orgValue[0], 'string']
            list2 = [keyPassPhrase, orgValue[1], 'string']

            revertParamList = "|".join(map(str, list1 + list2))

            # Revert the values to original
            step += 1
            print(f"TEST STEP {step}: Revert the original ssid and keypassphrase")
            print(f"EXPECTED RESULT {step}: Should set the original ssid and keypassphrase")
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
            print(f"ACTUAL RESULT {step}: Failed to get current ssid, keypassphrase and number of clients connected")
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
