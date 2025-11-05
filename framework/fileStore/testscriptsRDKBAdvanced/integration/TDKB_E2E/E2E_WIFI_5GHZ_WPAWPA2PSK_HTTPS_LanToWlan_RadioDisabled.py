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
<?xml version="1.0" encoding="UTF-8"?>
<xml>
  <id/>
  <version>2</version>
  <name>E2E_WIFI_5GHZ_WPAWPA2PSK_HTTPS_LanToWlan_RadioDisabled</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Verify that https traffic between wireless and wired clients should be denied when Radio interface parameter for 5GHZ [Device.WiFi.Radio.2.Enable] is disabled.</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Broadband</box_type>
    <box_type>Emulator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_223</test_case_id>
    <test_objective>Verify that https traffic between wireless and wired clients should be denied when Radio interface parameter for 5GHZ [Device.WiFi.Radio.2.Enable] is disabled.</test_objective>
    <test_type>Negative</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.AccessPoint.2.Security.ModeEnabled : None
Device.WiFi.Radio.2.Enable
Device.WiFi.SSID.2.Enable</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save security mode,Radio enable and ssid enable status of 2.4GHz
3. Set security mode to WPAWPA2PSK,radio enable and ssid enable to true using tdkb_e2e_SetMultipleParams
3. Try to connect to 5GHZ from WIFI client and Lan Client
4. Disable radio and send HTTPS request to wlan client from lan client
4. Revert the values</automation_approch>
    <except_output>HTTPS request should fail since radio is disabled</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WIFI_5GHZ_WPAWPA2PSK_HTTPS_LanToWlan_RadioDisabled</test_script>
    <skipped>No</skipped>
    <release_version>M54</release_version>
    <remarks>WLAN,LAN</remarks>
  </test_cases>
  <script_tags/>
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
obj.configureTestCase(ip,port,'E2E_WIFI_5GHZ_WPAWPA2PSK_HTTPS_LanToWlan_RadioDisabled');

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
        ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_5ghz_index
        keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_5ghz_index
        securityMode = "Device.WiFi.AccessPoint.%s.Security.ModeEnabled" %tdkbE2EUtility.ssid_5ghz_index
        radioEnable = "Device.WiFi.Radio.%s.Enable" %tdkbE2EUtility.radio_5ghz_index
        ssidEnable = "Device.WiFi.SSID.%s.Enable" %tdkbE2EUtility.ssid_5ghz_index

        #Get the value of the wifi parameters that are currently set.
        paramList=[ssidName,keyPassPhrase,securityMode,radioEnable,ssidEnable]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
            print("EXPECTED RESULT 1: Should retrieve the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            # Set securityMode,radioEnable and ssidEnable for 5ghz"
            setValuesList = [tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd,'WPA-WPA2-Personal','true','true'];
            print("WIFI parameter values that are set: %s" %setValuesList)

            list1 = [ssidName,tdkbE2EUtility.ssid_5ghz_name,'string']
            list2 = [keyPassPhrase,tdkbE2EUtility.ssid_5ghz_pwd,'string']
            list3 = [securityMode,'WPA-WPA2-Personal','string']
            list4 = [radioEnable,'true','bool']
            list5 = [ssidEnable,'true','bool']

            #Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2 + list3 + list4 + list5
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set the ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                print("EXPECTED RESULT 2: Should set the ssid,keypassphrase,securityMode,radioEnable and ssidEnable");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");

                #Retrieve the values after set and compare
                newParamList=[ssidName,keyPassPhrase,securityMode,radioEnable,ssidEnable]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                    print("EXPECTED RESULT 3: Should retrieve the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    #Wait for the changes to reflect in client device
                    time.sleep(60);

                    #Connect to the wifi ssid from wlan client
                    print("TEST STEP 4: From wlan client, Connect to the wifi ssid")
                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd,tdkbE2EUtility.wlan_5ghz_interface);
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS");

                        print("TEST STEP 5: Get the IP address of the wlan client after connecting to wifi")
                        wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_5ghz_interface);
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
                                    tdkTestObj.setResultStatus("SUCCESS");

                                    #Connect to LAN client and obtain its IP
                                    print("TEST STEP 8: Get the IP address of the lan client after connecting to it")
                                    lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
                                    if lanIP:
                                        tdkTestObj.setResultStatus("SUCCESS");

                                        print("TEST STEP 9: Check whether lan ip address is in same DHCP range")
                                        status = "SUCCESS"
                                        status = checkIpRange(curIPAddress,lanIP);
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS");

                                            #Disabling 2.4GHz radio interface of the WG
                                            setValuesList = ['false'];
                                            print("WIFI parameter values that are set: %s" %setValuesList)

                                            list1 = [radioEnable,'false','bool']

                                            #Concatenate the lists with the elements separated by pipe
                                            setParamList = list1
                                            setParamList = "|".join(map(str, setParamList))

                                            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                                            if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print("TEST STEP 10: Set RadioEnable")
                                                print("EXPECTED RESULT 10: Should set the RadioEnable");
                                                print("ACTUAL RESULT 10: %s" %details);
                                                print("[TEST EXECUTION RESULT] : SUCCESS");

                                                #Retrieve the values after set and compare
                                                newParamList=[radioEnable]
                                                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                                                if expectedresult in status and setValuesList == newValues:
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("TEST STEP 11: Get the current radioEnable")
                                                    print("EXPECTED RESULT 11: Should retrieve the current radioEnable")
                                                    print("ACTUAL RESULT 11: %s" %newValues);
                                                    print("[TEST EXECUTION RESULT] : SUCCESS");

                                                    #Wait for the changes to reflect in client device
                                                    time.sleep(60);

                                                    #Send HTTPS request to WLAN client from LAN clinet
                                                    print("TEST STEP 12: Connect to LAN Client and send HTTPS Request to WLAN Client")
                                                    status = verifyNetworkConnectivity(wlanIP,"WGET_HTTPS",lanIP,curIPAddress,"LAN");
                                                    if "SUCCESS" not in status:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print("HTTPS traffic not successful between wired and wireless clients")
                                                        finalStatus = "SUCCESS"
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("HTTPS traffic successful between wired and wireless clients")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("TEST STEP 11: Get the current radioEnable")
                                                    print("EXPECTED RESULT 11: Should retrieve the current radioEnable")
                                                    print("ACTUAL RESULT 11: %s" %newValues);
                                                    print("[TEST EXECUTION RESULT] : FAILURE");
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP 10: Set RadioEnable")
                                                print("EXPECTED RESULT 10: Should set the RadioEnable");
                                                print("ACTUAL RESULT 10: %s" %details);
                                                print("[TEST EXECUTION RESULT] : FAILURE");
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("checkIpRange:lan ip address is not in DHCP range")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("getLanIPAddress:Failed to get the LAN client IP")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("checkIpRange:wlan ip address is not in DHCP range")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("getParameterValue : Failed to get gateway lan ip")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("getWlanIPAddress:Failed to get the wlan ip address")

                        print("TEST STEP 13: From wlan client, Disconnect from the wifi ssid")
                        status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_5ghz_interface);
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("wlanDisconnectWifiSsid : Failed to disconnect Wifi ssid")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("wlanConnectWifiSsid: Failed to connect to the wifi ssid")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                    print("EXPECTED RESULT 3: Should retrieve the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Set the ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                print("EXPECTED RESULT 2: Should set the ssid,keypassphrase,securityMode,radioEnable and ssidEnable");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");

            #Prepare the list of parameter values to be reverted
            list1 = [ssidName,orgValue[0],'string']
            list2 = [keyPassPhrase,orgValue[1],'string']
            list3 = [securityMode,orgValue[2],'string']
            list4 = [radioEnable,orgValue[3],'bool']
            list5 = [ssidEnable,orgValue[4],'bool']

            #Concatenate the lists with the elements separated by pipe
            revertParamList = list1 + list2 + list3 + list4 + list5
            revertParamList = "|".join(map(str, revertParamList))

            #Revert the values to original
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
            if expectedresult in actualresult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 15: Should set the original ssid,keypassphrase,securityMode,radioEnable and ssidEnable");
                print("ACTUAL RESULT 15: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 15: Should set the original ssid,keypassphrase,securityMode,radioEnable and ssidEnable");
                print("ACTUAL RESULT 15: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
            print("EXPECTED RESULT 1: Should retrieve the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : FAILURE");
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