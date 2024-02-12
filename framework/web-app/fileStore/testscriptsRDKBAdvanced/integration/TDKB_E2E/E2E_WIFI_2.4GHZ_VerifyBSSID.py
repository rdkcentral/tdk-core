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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>1</version>
  <name>E2E_WIFI_2.4GHZ_VerifyBSSID</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Verify that MAC address of 2.4 GHz radio band obtained through parameter (Device.WiFi.SSID.1.BSSID) matches with the address obtained from Wireless Client</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Broadband</box_type>
    <box_type>Emulator</box_type>
    <box_type>RPI</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_170</test_case_id>
    <test_objective>Verify that MAC address of 2.4 GHz radio band obtained through parameter (Device.WiFi.SSID.1.BSSID) matches with the address obtained from Wireless Client</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the WIFI client setup is ready and WIFI client is listing the SSIDs properly.</pre_requisite>
    <api_or_interface_used>tdkb_e2e_Get</api_or_interface_used>
    <input_parameters>Device.WiFi.Radio.1.Enable
Device.WiFi.AccessPoint.1.Security.X_CISCO_COM_EncryptionMethod
Device.WiFi.AccessPoint.1.Security.ModeEnabled
Device.WiFi.AccessPoint.1.Security.KeyPassphrase
Device.WiFi.SSID.1.BSSID</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save encryption method and security mode
3. Set encryption method and security mode to AES and WPA2-Personal using tdkb_e2e_SetMultipleParams
3. Try to connect to Wifi client and check whether the wifi client is connected to the DUT using AES and WPA2-Personal
4. Get the current value of Device.WiFi.SSID.1.BSSID
5. Get the Access point MAC address of the WIFI client after connecting to the SSID and compare the Access point MAC address of WLAN client and the value returned by Device.WiFi.SSID.1.BSSID are same
6. Revert the values of encryption method and security mode
7.Unload tdkb_e2e module</automation_approch>
    <except_output>Verify whether the Access point MAC address of WLAN client and the value returned by Device.WiFi.SSID.1.BSSID are same</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WIFI_2.4GHZ_VerifyBSSID</test_script>
    <skipped>No</skipped>
    <release_version>M53</release_version>
    <remarks>WLAN</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import tdkbE2EUtility
from tdkbE2EUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WIFI_2.4GHZ_VerifyBSSID');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

        #Assign the WIFI parameters names to a variable
        ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
        keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index

        #Get the value of the wifi parameters that are currently set.
        paramList=[ssidName,keyPassPhrase]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current SSID, KeyPassphrase")
            print("EXPECTED RESULT 1: Should retrieve the current SSID, KeyPassphrase")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : %s" %status);

            # Set the security mode as WPA2-PSK and encryption method as "AES"
            setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd];
            print("WIFI parameter values that are set: %s" %setValuesList)

            list1 = [ssidName,tdkbE2EUtility.ssid_2ghz_name,'string']
            list2 = [keyPassPhrase,tdkbE2EUtility.ssid_2ghz_pwd,'string']

            #Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set the SSID, KeyPassphrase")
                print("EXPECTED RESULT 2: Should set the SSID, KeyPassphrase");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : %s" %actualresult);

                #Wait for the changes to reflect in client device
                time.sleep(60);

                #Retrieve the values after set and compare
                newParamList=[ssidName,keyPassPhrase]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current SSID, KeyPassphrase")
                    print("EXPECTED RESULT 3: Should retrieve the current SSID, KeyPassphrase")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Connect to the wifi ssid from wlan client using valid wifi password
                    print("TEST STEP 4: From wlan client, Connect to the wifi ssid using valid wifi password")
                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.wlan_2ghz_interface);
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TEST STEP 5: Get the IP address of the wlan client after connecting to wifi")
                        wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_2ghz_interface);
                        if wlanIP:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("TEST STEP 6: Get the current LAN IP address DHCP range")
                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                            tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                            print("LAN IP Address: %s" %curIPAddress);

                            if expectedresult in status and curIPAddress:
                                tdkTestObj.setResultStatus("SUCCESS");

                                print("TEST STEP 7: Check whether wlan ip address is in same DHCP range")
                                status = "SUCCESS"
                                status = checkIpRange(curIPAddress,wlanIP);
                                if expectedresult in status:
                                    print("TEST STEP 7: SUCCESS, wlan ip address is in same DHCP range")
                                    tdkTestObj.setResultStatus("SUCCESS");

                                    #Get the BSSID of the gateway
                                    getMAC = "Device.WiFi.SSID.%s.BSSID" %tdkbE2EUtility.ssid_2ghz_index
                                    tdkTestObj,status, MAC1 = getParameterValue(obj, getMAC)
                                    if expectedresult in status and MAC1:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("TEST STEP 8: Get the BSSID MAC from WG")
                                        print("EXPECTED RESULT 8: Should get the BSSID MAC from WG")
                                        print("ACTUAL RESULT 8: %s" %MAC1);
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        #From the client, get the Access Point MAC address
                                        MAC2 = getWlanAccessPoint(tdkbE2EUtility.wlan_2ghz_interface);

                                        print("TEST STEP 9: Check if the Access Point MAC address from client is same as the one from WG")
                                        print("EXPECTED RESULT 9: Both MAC addresses should be the same")
                                        if MAC1.upper() == MAC2.upper():
                                            print("ACTUAL RESULT 8: Both MACS are same %s %s" %(MAC1,MAC2));
                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                            finalStatus = "SUCCESS"
                                        else:
                                            print("ACTUAL RESULT 8: Both MACS are not same %s %s" %(MAC1,MAC2));
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                            tdkTestObj.setResultStatus("FAILURE");
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 8: Get the BSSID MAC from WG")
                                        print("EXPECTED RESULT 8: Should get the BSSID MAC from WG")
                                        print("ACTUAL RESULT 8: %s" %MAC1);
                                        print("[TEST EXECUTION RESULT] : FAILURE")

                                        print("TEST STEP 9: From wlan client, Disconnect from the wifi ssid")
                                        status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_2ghz_interface);
                                        print("TEST STEP 9: Disconnect the WiFi connection")
                                        if expectedresult in status:
                                            print("TEST STEP 9: Connection successfully disconnected")
                                            tdkTestObj.setResultStatus("SUCCESS");
                                        else:
                                            print("TEST STEP 9: Failed to Disconnect")
                                            tdkTestObj.setResultStatus("FAILURE");
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 7: FAILURE, wlan ip address is not in the same DHCP range")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 6: Failed to get the current LAN IP address DHCP range")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("TEST STEP 5: Failed to get the IP address of the wlan client after connecting to wifi")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 4: Failed to connect from wlan client, to the wifi ssid using valid wifi password")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current SSID, KeyPassphrase")
                    print("EXPECTED RESULT 3: Should retrieve the current SSID, KeyPassphrase")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("TEST STEP 2: Set the SSID, KeyPassphrase")
                print("EXPECTED RESULT 2: Should set the SSID, KeyPassphrase");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : %s" %actualresult);

            #Prepare the list of parameter values to be reverted
            list1 = [ssidName,orgValue[0],'string']
            list2 = [keyPassPhrase,orgValue[1],'string']

            #Concatenate the lists with the elements separated by pipe
            revertParamList = list1 + list2
            revertParamList = "|".join(map(str, revertParamList))

            #Revert the values to original
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
            if expectedresult in actualresult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 10: Should set the original SSID, KeyPassphrase");
                print("ACTUAL RESULT 10: %s" %details);
                print("[TEST EXECUTION RESULT] : %s" %actualresult);
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 10: Should set the original SSID, KeyPassphrase");
                print("ACTUAL RESULT 10: %s" %details);
                print("[TEST EXECUTION RESULT] : %s" %actualresult);
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current SSID, KeyPassphrase")
            print("EXPECTED RESULT 1: Should retrieve the current SSID, KeyPassphrase")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : %s" %status);
    else:
        obj.setLoadModuleStatus("FAILURE");
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup();
    obj.unloadModule("tdkb_e2e");
else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");