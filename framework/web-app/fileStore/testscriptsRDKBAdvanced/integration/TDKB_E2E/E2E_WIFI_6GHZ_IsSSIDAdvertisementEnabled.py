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
  <name>E2E_WIFI_6GHZ_IsSSIDAdvertisementEnabled</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_SetMultipleParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify whether Network name broadcast (SSID advertisement) is enabled by default in gateway</synopsis>
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
    <test_case_id>TC_TDKB_E2E_666</test_case_id>
    <test_objective>Verify whether Network name broadcast (SSID advertisement) is enabled by default in gateway</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband, BPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.{i}.SSID
Device.WiFi.AccessPoint.{i}.Security.KeyPassphrase
Device.WiFi.AccessPoint.{i}.SSIDAdvertisementEnabled</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2.Do a factory reset
3.Using tdkb_e2e_Get, get and save SSIDAdvertisementEnabled status
4.Set SSIDAdvertisementEnabled to True using tdkb_e2e_SetMultipleParams
5.Try to connect to Wifi client and check if the ssid is listing properly
6.Revert the values of SSIDAdvertisementEnabled
7.Unload the tdkb_e2e module</automation_approch>
    <expected_output>The ssid name for 6GHZ should be listed with SSIDAdvertisementEnabled</expected_output>
    <priority>High</priority>
    <test_stub_interface>None</test_stub_interface>
    <test_script>E2E_WIFI_6GHZ_IsSSIDAdvertisementEnabled</test_script>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_IsSSIDAdvertisementEnabled')

#Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"
    step = 1

    #Parse the device configuration file
    print(f"TEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Should parse the device configuration file successfully")
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Parsed the device configuration file successfully")
        print("[TEST EXECUTION RESULT] : SUCCESS")

        obj.saveCurrentState()
        #Initiate Factory reset
        step =+ 1
        FR_value = "Router,Wifi,VoIP,Dect,MoCA"
        FR_Paramvalue = f"Device.X_CISCO_COM_DeviceControl.FactoryReset|{FR_value}|string"
        tdkTestObj, actualresult, details = setMultipleParameterValues(obj, FR_Paramvalue)

        print(f"TEST STEP {step}: Initiate factory reset")
        print(f"EXPECTED RESULT {step}: Should initiate factory reset")

        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Factory Rest Success")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            obj.restorePreviousStateAfterReboot()
            time.sleep(160)

            #Assign the WIFI parameters names to a variable
            ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
            keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"
            ssidAdvertStatus = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.SSIDAdvertisementEnabled"

            #Get the value of the wifi parameters that are currently set.
            step += 1
            print(f"TEST STEP {step}: Get the current ssid, keypassphrase, ssidAdvertStatus and check whether ssid advertisement is enabled by default")
            print(f"EXPECTED RESULT {step}: Should retrieve the current ssid, keypassphrase and ssidAdvertStatus, ssid advertisement should be enabled by default")
            paramList = [ssidName, keyPassPhrase, ssidAdvertStatus]
            tdkTestObj, status, orgValue = getMultipleParameterValues(obj, paramList)
            if expectedresult in status and "true" in orgValue[2]:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {orgValue}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                # Set the SSID name and password
                setValuesList = [tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd]
                print(f"WIFI parameter values that are set: {setValuesList}")

                list1 = [ssidName, tdkbE2EUtility.ssid_6ghz_name, 'string']
                list2 = [keyPassPhrase, tdkbE2EUtility.ssid_6ghz_pwd, 'string']

                #Concatenate the lists with the elements separated by pipe
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

                    #Retrieve the values after set and compare
                    newParamList = [ssidName, keyPassPhrase]
                    step += 1
                    print(f"TEST STEP {step}: Get the current ssid and keypassphrase")
                    print(f"EXPECTED RESULT {step}: Should retrieve the current ssid and keypassphrase")
                    tdkTestObj, status, newValues = getMultipleParameterValues(obj, newParamList)

                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: {newValues}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        #Wait for the changes to reflect in client device
                        time.sleep(60)

                        #Check if the SSID name is listed in wifi client
                        step += 1
                        print(f"TEST STEP {step}: Check if the SSID name is listed in wifi client")
                        print(f"EXPECTED RESULT {step}: SSID should be broadcasted on the network")
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

                #Prepare the list of parameter values to be reverted
                list1 = [ssidName, orgValue[0], 'string']
                list2 = [keyPassPhrase, orgValue[1], 'string']

                #Concatenate the lists with the elements separated by pipe
                revertParamList = list1 + list2
                revertParamList = "|".join(map(str, revertParamList))

                step += 1
                print(f"TEST STEP {step}: Revert the values to original")
                print(f"EXPECTED RESULT {step}: Should set the original ssid and keypassphrase")
                tdkTestObj, actualresult, details = setMultipleParameterValues(obj, revertParamList)
                if expectedresult in actualresult and "SUCCESS" in finalStatus:
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
            tdkTestObj.setLoadModuleStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Factory Reset failed")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to parse the device configuration file")
        print("[TEST EXECUTION RESULT] : FAILURE")

    #Handle any post execution cleanup required
    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")

else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")
