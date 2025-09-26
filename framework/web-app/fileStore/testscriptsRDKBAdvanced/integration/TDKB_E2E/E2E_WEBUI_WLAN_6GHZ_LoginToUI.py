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
  <name>E2E_WEBUI_WLAN_6GHZ_LoginToUI</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_SetMultipleParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if we can login to the UI page of gateway from the WLAN Client after connecting 6GHZ SSID</synopsis>
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
    <test_case_id>TC_TDKB_E2E_678</test_case_id>
    <test_objective>To check if we can login to the UI page of gateway from the WLAN Client after connecting 6GHZ SSID</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Boradband, BPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
    2. TDK Agent should be in a running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.{i}.SSID
Device.WiFi.AccessPoint.{i}.Security.KeyPassphrase</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Import selenium module
3. Start selenium hub in TM machine
4. Start Node in wlan client machine
5. From Wlan client Connect to 6GHZ SSID
6. check if the wlan client has the ip in dhcp range
7. Try to access the WEBUI of the gateway using selenium grid
8. Validate if the UI page is accessible or not
9. Try to login to the page with credentials
10. Validate if login is success or not
11. Kill selenium hub and node
12. unload module</automation_approch>
    <expected_output>The UI page of gateway should be accessible from WLAN cleint and should be able to login to it successfully</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WEBUI_WLAN_6GHZ_LoginToUI</test_script>
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
import tdkbWEBUIUtility
from tdkbWEBUIUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e", "1")

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WEBUI_WLAN_6GHZ_LoginToUI')

#Get the result of connection with test component
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
        print(f"ACTUAL RESULT {step}: {status}")
        print("[TEST EXECUTION RESULT] : SUCCESS")
        obj.setLoadModuleStatus("SUCCESS")

        #Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"

        #  Get the value of the wifi parameters that are currently set.
        step += 1
        print(f"TEST STEP {step}: Get the current ssid and keypassphrase")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid and keypassphrase")
        paramList = [ssidName, keyPassPhrase]
        tdkTestObj, status, orgValue = getMultipleParameterValues(obj, paramList)
        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Current ssid and keypassphrase : {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            # Set the ssid and keypassphrase
            setValuesList = [tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd]
            print(f"WIFI parameter values that are set: {setValuesList}")

            list1 = [ssidName, tdkbE2EUtility.ssid_6ghz_name, 'string']
            list2 = [keyPassPhrase, tdkbE2EUtility.ssid_6ghz_pwd, 'string']

            setParamList = list1 + list2
            setParamList = "|".join(map(str, setParamList))

            step += 1
            print(f"TEST STEP {step}: Set the ssid and keypassphrase")
            print(f"EXPECTED RESULT {step}: Should set the ssid and keypassphrase")
            tdkTestObj, actualresult, details = setMultipleParameterValues(obj, setParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                # Retrieve the values after set and compare
                step += 1
                print(f"TEST STEP {step}: Get the current ssid and keypassphrase after set")
                print(f"EXPECTED RESULT {step}: Retrieved values should match the set values")
                newParamList = [ssidName, keyPassPhrase]
                tdkTestObj, status, newValues = getMultipleParameterValues(obj, newParamList)
                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: The parameter values after SET: {newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Wait for the changes to reflect in client device
                    time.sleep(60)

                    # Start Selenium grid
                    step += 1
                    print(f"TEST STEP {step}: Start Selenium Grid for WLAN")
                    print(f"EXPECTED RESULT {step}: Selenium Grid should start successfully")
                    driver, status = startSeleniumGrid(tdkTestObj, "WLAN", tdkbE2EUtility.grid_url)
                    if status == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: {status}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        # Connect to the wifi ssid from wlan client
                        step += 1
                        print(f"TEST STEP {step}: From wlan client, connect to the wifi ssid")
                        print(f"EXPECTED RESULT {step}: Should connect successfully to the wifi ssid")
                        status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,tdkbE2EUtility.wlan_6ghz_interface)
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: {status}")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            # Get the IP address of the wlan client after connecting
                            step += 1
                            print(f"TEST STEP {step}: Get the IP address of the wlan client after connecting")
                            print(f"EXPECTED RESULT {step}: WLAN client should have a valid IP address")
                            wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)
                            if wlanIP:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: SUCCESS")
                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                # Get the current LAN IP address DHCP range
                                step += 1
                                print(f"TEST STEP {step}: Get the current LAN IP address DHCP range")
                                print(f"EXPECTED RESULT {step}: Should retrieve the LAN IP successfully")
                                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                tdkTestObj, status, curIPAddress = getParameterValue(obj, param)
                                if expectedresult in status and curIPAddress:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: {curIPAddress}")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    #  Check whether wlan ip address is in same DHCP range
                                    step += 1
                                    print(f"TEST STEP {step}: Check whether wlan IP address is in DHCP range")
                                    print(f"EXPECTED RESULT {step}: WLAN IP should be in DHCP range")
                                    status = checkIpRange(curIPAddress, wlanIP)
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: {status}")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        # Try to access and login to Local WebUI
                                        step += 1
                                        print(f"TEST STEP {step}: Try to access and login to Local WebUI")
                                        print(f"EXPECTED RESULT {step}: WebUI login should be successful")
                                        status, driver = openLocalWebUI(tdkbE2EUtility.grid_url, tdkTestObj, "LocalLogin")
                                        if status == "SUCCESS":
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            finalStatus = "SUCCESS"
                                            print(f"ACTUAL RESULT {step}: {status}")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                            time.sleep(10)
                                            driver.quit()
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: {status}")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: Wlan IP is not in DHCP range")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Failed to get current LAN IP address DHCP range")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to get Wlan IP address")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to connect Wlan client to wifi ssid")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: {status}")
                        print("[TEST EXECUTION RESULT] : FAILURE")

                    # Kill selenium hub and node (post actions)
                    step += 1
                    print(f"TEST STEP {step}: Kill selenium hub and node")
                    print(f"EXPECTED RESULT {step}: Should kill hub and node successfully")
                    status = tdkbWEBUIUtility.kill_hub_node("WLAN")
                    if status == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Post-requisite success")
                        print("[TEST EXECUTION RESULT] : SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to kill node and hub")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: GET operation failed")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to get current ssid and keypassphrase")
            print("[TEST EXECUTION RESULT] : FAILURE")

        # Prepare the list of parameter values to be reverted
        list1 = [ssidName, orgValue[0], 'string']
        list2 = [keyPassPhrase, orgValue[1], 'string']

        revertParamList = list1 + list2
        revertParamList = "|".join(map(str, revertParamList))

        # Revert the values to original
        step += 1
        print(f"TEST STEP {step}: Revert ssid and keypassphrase to original values")
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
        obj.setLoadModuleStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to parse the device configuration file")
        print("[TEST EXECUTION RESULT] : FAILURE")

    #Handle any post execution cleanup required
    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")

else:
    # Module load failed - not a test step but print actual details
    print(f"ACTUAL RESULT: Failed to load module, loadmodulestatus='{loadmodulestatus}'")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")
