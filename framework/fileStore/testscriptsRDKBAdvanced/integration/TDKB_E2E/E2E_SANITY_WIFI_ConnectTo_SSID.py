##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2019 RDK Management
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
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_SANITY_WIFI_ConnectTo_SSID</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if the connection to 2.4GHZ and 5GHz SSIDs are success or not</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>30</execution_time>
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
    <box_type>Broadband</box_type>
    <!--  -->
    <box_type>Emulator</box_type>
    <!--  -->
    <box_type>RPI</box_type>
    <!--  -->
  <box_type>BPI</box_type></box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_402</test_case_id>
    <test_objective>To check if the connection to 2.4GHZ and 5GHz SSIDs are success or not</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.1.SSID
Device.WiFi.AccessPoint.1.Security.KeyPassphrase
Device.WiFi.SSID.2.SSID
Device.WiFi.AccessPoint.2.Security.KeyPassphrase</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save ssid name and password of 2.4GHZ and 5GHZ
3. Check whether SSID for 2.4GHZ and 5GHZ are broadcasting and able to connect to those SSIDs
5. Revert the values to original value
6.Unload tdkb_e2e module</automation_approch>
    <except_output>The SSIDs for both 2.4GHZ and 5GHZ should broadcast and should be able to connect to them</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WIFI_ConnectTo_SSID</test_script>
    <skipped>No</skipped>
    <release_version>M59</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
    <!--  -->
  </script_tags>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import time
import tdkbE2EUtility
from tdkbE2EUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_SANITY_WIFI_ConnectTo_SSID')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"
    step = 1
    status = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")

        if tdkbE2EUtility.mlo_capability == "False":
            #Assign the WIFI parameters names to a variable
            ssidName_2g = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
            keyPassPhrase_2g = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
            ssidName_5g = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_5ghz_index
            keyPassPhrase_5g = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_5ghz_index

            paramList = [ssidName_2g,keyPassPhrase_2g,ssidName_5g,keyPassPhrase_5g]
            setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd]

            list1 = [ssidName_2g,tdkbE2EUtility.ssid_2ghz_name,'string']
            list2 = [keyPassPhrase_2g,tdkbE2EUtility.ssid_2ghz_pwd,'string']
            list3 = [ssidName_5g,tdkbE2EUtility.ssid_5ghz_name,'string']
            list4 = [keyPassPhrase_5g,tdkbE2EUtility.ssid_5ghz_pwd,'string']

            setParamList = list1 + list2 + list3 + list4

            wifiClientList = [
                [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.wlan_2ghz_interface],
                [tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd,tdkbE2EUtility.wlan_5ghz_interface]
            ]
        else:
            #Assign the MLO WIFI parameters names to a variable
            mloSsidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
            mloKeyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index

            paramList = [mloSsidName,mloKeyPassPhrase]
            setValuesList = [tdkbE2EUtility.ssid_name,tdkbE2EUtility.ssid_pwd]

            list1 = [mloSsidName,tdkbE2EUtility.ssid_name,'string']
            list2 = [mloKeyPassPhrase,tdkbE2EUtility.ssid_pwd,'string']

            setParamList = list1 + list2

            wifiClientList = [
                [tdkbE2EUtility.ssid_name,tdkbE2EUtility.ssid_pwd,tdkbE2EUtility.wlan_interface]
            ]

        #Get the value of the wifi parameters that are currently set.
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"\nTEST STEP {step}: Get the current WiFi SSID and keypassphrase values")
            print(f"EXPECTED RESULT {step}: Should retrieve the current WiFi SSID and keypassphrase values")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            print("Parameter values that are set: %s" %setValuesList)

            #Concatenate the lists with the elements separated by pipe
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
            step = step + 1

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"\nTEST STEP {step}: Set the WiFi SSID and keypassphrase values")
                print(f"EXPECTED RESULT {step}: Should set the WiFi SSID and keypassphrase values")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                #Retrieve the values after set and compare
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,paramList)
                step = step + 1

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"\nTEST STEP {step}: Get the updated WiFi SSID and keypassphrase values")
                    print(f"EXPECTED RESULT {step}: Should retrieve the updated WiFi SSID and keypassphrase values")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Wait for the changes to reflect in client device
                    time.sleep(60)

                    validationStatus = "SUCCESS"

                    for wifiClient in wifiClientList:
                        ssidName = wifiClient[0]
                        ssidPassword = wifiClient[1]
                        wlanInterface = wifiClient[2]

                        step = step + 1
                        print(f"\nTEST STEP {step}: From WLAN client, connect to the configured WiFi SSID")
                        print(f"EXPECTED RESULT {step}: WLAN client should connect to the configured WiFi SSID successfully")
                        status = wlanConnectWifiSsid(ssidName,ssidPassword,wlanInterface)

                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: WLAN client connected to WiFi SSID successfully")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            step = step + 1
                            print(f"\nTEST STEP {step}: Get the IP address of the WLAN client after connecting to WiFi")
                            print(f"EXPECTED RESULT {step}: WLAN client should get an IP address")
                            wlanIP = getWlanIPAddress(wlanInterface)

                            if wlanIP:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: WLAN IP Address is {wlanIP}")
                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                step = step + 1
                                print(f"\nTEST STEP {step}: Get the current LAN IP address DHCP range")
                                print(f"EXPECTED RESULT {step}: Should get the current LAN IP address DHCP range")
                                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                                print("Gateway LAN IP Address: %s" %curIPAddress)

                                if expectedresult in status and curIPAddress:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: LAN IP Address retrieved as {curIPAddress}")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    step = step + 1
                                    print(f"\nTEST STEP {step}: Check whether WLAN IP address is in same DHCP range")
                                    print(f"EXPECTED RESULT {step}: WLAN IP address should be in same DHCP range")
                                    status = "SUCCESS"
                                    status = checkIpRange(curIPAddress,wlanIP)

                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: WLAN IP address is in same DHCP range")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        step = step + 1
                                        print(f"\nTEST STEP {step}: From WLAN client, disconnect from the WiFi SSID")
                                        print(f"EXPECTED RESULT {step}: WLAN client should disconnect from WiFi SSID successfully")
                                        status = wlanDisconnectWifiSsid(wlanInterface)

                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step}: Disconnect from WiFi SSID is successful")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                        else:
                                            validationStatus = "FAILURE"
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: Disconnect from WiFi SSID failed")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                            break
                                    else:
                                        validationStatus = "FAILURE"
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: WLAN IP address is not in same DHCP range")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                        break
                                else:
                                    validationStatus = "FAILURE"
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Failed to get the current LAN IP address DHCP range")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                    break
                            else:
                                validationStatus = "FAILURE"
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to get the WLAN IP address")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                                break
                        else:
                            validationStatus = "FAILURE"
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to connect to the configured WiFi SSID")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                            break

                    if expectedresult in validationStatus:
                        finalStatus = "SUCCESS"
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"\nTEST STEP {step}: Get the updated WiFi SSID and keypassphrase values")
                    print(f"EXPECTED RESULT {step}: Should retrieve the updated WiFi SSID and keypassphrase values")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"\nTEST STEP {step}: Set the WiFi SSID and keypassphrase values")
                print(f"EXPECTED RESULT {step}: Should set the WiFi SSID and keypassphrase values")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")

            #Prepare the list of parameter values to be reverted
            revertParamList = []
            index = 0
            for param in paramList:
                revertParamList = revertParamList + [param,orgValue[index],'string']
                index = index + 1

            #Concatenate the lists with the elements separated by pipe
            revertParamList = "|".join(map(str, revertParamList))

            #Revert the values to original
            step = step + 1
            print(f"\nTEST STEP {step}: Revert the WiFi SSID and keypassphrase values to original")
            print(f"EXPECTED RESULT {step}: Should set the original WiFi SSID and keypassphrase values")
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)

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
            print(f"\nTEST STEP {step}: Get the current WiFi SSID and keypassphrase values")
            print(f"EXPECTED RESULT {step}: Should retrieve the current WiFi SSID and keypassphrase values")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")

else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")