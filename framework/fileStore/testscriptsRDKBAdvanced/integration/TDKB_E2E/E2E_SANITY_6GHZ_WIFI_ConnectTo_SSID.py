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
  <name>E2E_SANITY_6GHZ_WIFI_ConnectTo_SSID</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_SetMultipleParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check whether 6GHZ SSID is broadcasting or not and wifi client able to connect to it</synopsis>
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
    <test_case_id>TC_TDKB_E2E_654</test_case_id>
    <test_objective>To check if the connection to 6GHz SSID is success or not</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband, BPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.{i}.SSID
    Device.WiFi.AccessPoint.{i}.Security.KeyPassphrase</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save ssid name and password of 6GHZ
3. Check whether SSID for 6GHZ is broadcasting and able to connect to SSID
5. Revert the values to original value
6.Unload tdkb_e2e module</automation_approch>
    <expected_output>The SSID 6GHZ should broadcast and should be able to connect to it</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_SANITY_6GHZ_WIFI_ConnectTo_SSID</test_script>
    <skipped></skipped>
    <release_version>M140</release_version>
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

# Initialize step counter
step = 0

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e", "1")

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_SANITY_6GHZ_WIFI_ConnectTo_SSID')

#Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"

    #Parse the device configuration file
    step += 1
    print(f"TEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Should parse the device configuration file successfully")
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Parsed the device configuration file successfully")
        print("[TEST EXECUTION RESULT] : SUCCESS")

        #Assign the WIFI parameters names to a variable
        ssidName_6g = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase_6g = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"

        #Get the value of the wifi parameters
        paramList = [ssidName_6g, keyPassPhrase_6g]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj, paramList)

        step += 1
        print(f"TEST STEP {step}: Get the current ssid,keypassphrase of 6GHz")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase of 6GHz")
        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            # Set the SSID name,password
            setValuesList = [tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd]
            print(f"Parameter values that are set: {setValuesList}")

            list1 = [ssidName_6g, tdkbE2EUtility.ssid_6ghz_name, 'string']
            list2 = [keyPassPhrase_6g, tdkbE2EUtility.ssid_6ghz_pwd, 'string']

            setParamList = list1 + list2
            setParamList = "|".join(map(str, setParamList))

            step += 1
            print(f"TEST STEP {step}: Set the ssid,keypassphrase of 6GHz")
            print(f"EXPECTED RESULT {step}: Should set the ssid,keypassphrase of 6GHz")
            tdkTestObj, actualresult, details = setMultipleParameterValues(obj, setParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                #Retrieve values after set
                newParamList = [ssidName_6g, keyPassPhrase_6g]
                tdkTestObj, status, newValues = getMultipleParameterValues(obj, newParamList)

                step += 1
                print(f"TEST STEP {step}: Get the ssid,keypassphrase of 6GHz after set")
                print(f"EXPECTED RESULT {step}: Should retrieve updated ssid,keypassphrase of 6GHz")
                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    time.sleep(60)

                    # Connect to 6GHz
                    step += 1
                    print(f"TEST STEP {step}: From wlan client, Connect to the 6GHz wifi ssid")
                    print(f"EXPECTED RESULT {step}: Wlan client should connect successfully to 6GHz SSID")
                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,tdkbE2EUtility.wlan_6ghz_interface)
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: {status}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        step += 1
                        print(f"TEST STEP {step}: Get the IP address of wlan client after connecting to 6GHz wifi")
                        print(f"EXPECTED RESULT {step}: Should retrieve valid IP address for wlan client")
                        wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)
                        if wlanIP:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: WLAN IP: {wlanIP}")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            step += 1
                            print(f"TEST STEP {step}: Get the current LAN IP address DHCP range")
                            print(f"EXPECTED RESULT {step}: Should retrieve valid LAN IP address")
                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                            tdkTestObj, status, curIPAddress = getParameterValue(obj, param)

                            if expectedresult in status and curIPAddress:
                                tdkTestObj.setResultStatus("SUCCESS")

                                step += 1
                                print(f"TEST STEP {step}: Check whether wlan IP is in same DHCP range")
                                print(f"EXPECTED RESULT {step}: Wlan IP should be in DHCP range")
                                status = checkIpRange(curIPAddress, wlanIP)
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: Wlan IP is in same DHCP range")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    step += 1
                                    print(f"TEST STEP {step}: Disconnect wlan client from 6GHz SSID")
                                    print(f"EXPECTED RESULT {step}: Wlan client should disconnect successfully")
                                    status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: Disconnect from WIFI SSID: {status}")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")
                                        finalStatus= "SUCCESS"
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: Disconnect from WIFI SSID: {status}")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: wlan IP not in DHCP range for 6GHz")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to get LAN IP")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to get wlan IP for 6GHz")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f" ACTUAL RESULT {step}: Failed to connect to 6GHz SSID")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")

            #Revert values to original
            list1 = [ssidName_6g, orgValue[0], 'string']
            list2 = [keyPassPhrase_6g, orgValue[1], 'string']

            revertParamList = list1 + list2
            revertParamList = "|".join(map(str, revertParamList))

            step += 1
            print(f"TEST STEP {step}: Revert ssid,keypassphrase of 6GHz to original")
            print(f"EXPECTED RESULT {step}: Should revert values successfully")
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

    #Cleanup
    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")

else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")

