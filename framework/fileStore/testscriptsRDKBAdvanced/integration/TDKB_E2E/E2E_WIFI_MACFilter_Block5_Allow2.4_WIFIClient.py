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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_WIFI_MACFilter_Block5_Allow2.4_WIFIClient</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify that MAC address based Access control allows 2.4GHZ SSID to connect to WG and deny access for 5GHZ SSID</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>30</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>true</advanced_script>
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
    <test_case_id>TC_TDKB_E2E_45</test_case_id>
    <test_objective>Verify that MAC address based Access control allows 2.4GHZ SSID to connect to WG and deny access for 5GHZ SSID</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.AccessPoint.%s.X_CISCO_COM_MACFilter.Enable
Device.WiFi.AccessPoint.%s.X_CISCO_COM_MACFilter.FilterAsBlackList
Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable.
Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable.%s.DeviceName
Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable.%s.MACAddress</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save MACFilter.FilterAsBlackList, MACFilter.Enable values of 2.4 and 5 GHZ access points
3. Connect the WIFI client to 2.4 SSID and get the MAC address of the WLAN  interface
4. Disconnect the WiFi client
5. Connect the WIFI client to 5GHZ SSID and get the MAC address of the WLAN  interface
6. Disconnect the WiFi client
7. Enable MACFilter.Enable and disable MACFilter.FilterAsBlackList of 2.4GHZ accesspoint
8. Enable both MACFilter.Enable and MACFilter.FilterAsBlackList of 5GHZ accesspoint
9.Add new rule to Device.WiFi.AccessPoint.2.X_CISCO_COM_MacFilterTable.
10. Set the devicename and mac details of client to be blocked in the MAC filter rule
11.Add new rule to Device.WiFi.AccessPoint.1.X_CISCO_COM_MacFilterTable.
12. Set the devicename and mac details of client to be blocked in the MAC filter rule
13.Try to connect the blocked client to the GW's 2.4GHZ SSID. That connection attempt should be success
14.Try to connect the blocked client to the GW's 5GHZ SSID. That connection attempt should fail
15.Delete the added rules and revert all params values
16.Unload tdkb_e2e module</automation_approch>
    <except_output>Connection attempt to 2.4GHZ SSID should succeed and connection to 5GHZ should fail</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WIFI_MACFilter_Block5_Allow2.4_WIFIClient</test_script>
    <skipped>No</skipped>
    <release_version>M57</release_version>
    <remarks>WLAN</remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import tdkbE2EUtility
from tdkbE2EUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");
obj1 = tdklib.TDKScriptingLibrary("advancedconfig","RDKB");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WIFI_MACFilter_Block5_Allow2.4_WIFIClient');
obj1.configureTestCase(ip,port,'E2E_WIFI_MACFilter_Block5_Allow2.4_WIFIClient');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 =obj1.getLoadModuleResult();

print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS");
    obj1.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    finalStatus1 = "FAILURE"
    finalStatus2 = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

        #Assign the WIFI parameters names to a variable
        ssidName2 = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
        keyPassPhrase2 = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
        radioEnable2 = "Device.WiFi.Radio.%s.Enable" %tdkbE2EUtility.radio_2ghz_index
        macFilterEnable2 = "Device.WiFi.AccessPoint.%s.X_CISCO_COM_MACFilter.Enable" %tdkbE2EUtility.ssid_2ghz_index
        macFilterBlackList2 = "Device.WiFi.AccessPoint.%s.X_CISCO_COM_MACFilter.FilterAsBlackList" %tdkbE2EUtility.ssid_2ghz_index

        ssidName5 = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_5ghz_index
        keyPassPhrase5 = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_5ghz_index
        radioEnable5 = "Device.WiFi.Radio.%s.Enable" %tdkbE2EUtility.radio_5ghz_index
        macFilterEnable5 = "Device.WiFi.AccessPoint.%s.X_CISCO_COM_MACFilter.Enable" %tdkbE2EUtility.ssid_5ghz_index
        macFilterBlackList5 = "Device.WiFi.AccessPoint.%s.X_CISCO_COM_MACFilter.FilterAsBlackList" %tdkbE2EUtility.ssid_5ghz_index

        #Get the value of the wifi parameters that are currently set.
        paramList=[ssidName2,keyPassPhrase2,radioEnable2,macFilterEnable2,macFilterBlackList2,ssidName5,keyPassPhrase5,radioEnable5,macFilterEnable5,macFilterBlackList5]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
            print("EXPECTED RESULT 1: Should retrieve the current ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
            print("ACTUAL RESULT 1:  %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            # Set the SSID name,password,Radio enable status ,macFilterEnable, macFilterBlackList
            setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,'true',tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd,'true'];
            print("Parameter values that are set: %s" %setValuesList)

            list1 = [ssidName2,tdkbE2EUtility.ssid_2ghz_name,'string']
            list2 = [keyPassPhrase2,tdkbE2EUtility.ssid_2ghz_pwd,'string']
            list3 = [radioEnable2,'true','bool']

            list4 = [ssidName5,tdkbE2EUtility.ssid_5ghz_name,'string']
            list5 = [keyPassPhrase5,tdkbE2EUtility.ssid_5ghz_pwd,'string']
            list6 = [radioEnable5,'true','bool']

            #Concatenate the lists with the elements separated by pipe
            setParamList2 = list1 + list2 + list3
            setParamList5 = list4 + list5 + list6
            setParamList2 = "|".join(map(str, setParamList2))
            setParamList5 = "|".join(map(str, setParamList5))

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList5)
            tdkTestObj,actualresult1,details1 = setMultipleParameterValues(obj,setParamList5)
            if expectedresult in actualresult and expectedresult in actualresult1:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set the ssid,keypassphrase,Radio enable status")
                print("EXPECTED RESULT 2: Should set the ssid,keypassphrase,Radio enable status")
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : %s" %actualresult);

                #Retrieve the values after set and compare
                newParamList=[ssidName2,keyPassPhrase2,radioEnable2,ssidName5,keyPassPhrase5,radioEnable5]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current SSID, KeyPassphrase")
                    print("EXPECTED RESULT 3: Should retrieve the current SSID, KeyPassphrase")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                    #Wait for the changes to reflect in client device
                    time.sleep(60);

                    #Connect to the 2.4GHz wifi ssid from wlan client
                    print("TEST STEP 4: From wlan client, Connect to the wifi ssid")
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
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    #From the client, get its MAC
                                    MAC2 = getWlanMACAddress(tdkbE2EUtility.wlan_2ghz_interface);
                                    print("TEST STEP : Get the MAC address of wlan client")
                                    print("MAC retreived is %s" %MAC2)

                                    print("TEST STEP : From wlan client, Disconnect from the wifi ssid")
                                    status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_2ghz_interface);
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("Disconnect from WIFI SSID: SUCCESS")

                                        if MAC2:
                                            #Connect to the 5GHz wifi ssid from wlan client
                                            print("TEST STEP 8: From wlan client, Connect to the wifi ssid")
                                            status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd,tdkbE2EUtility.wlan_5ghz_interface);
                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS");

                                                print("TEST STEP 9: Get the IP address of the wlan client after connecting to wifi")
                                                wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_5ghz_interface);
                                                if wlanIP:
                                                    tdkTestObj.setResultStatus("SUCCESS");

                                                    print("TEST STEP 10: Check whether wlan ip address is in same DHCP range")
                                                    status = "SUCCESS"
                                                    status = checkIpRange(curIPAddress,wlanIP);
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                                        #From the client, get its MAC
                                                        MAC5 = getWlanMACAddress(tdkbE2EUtility.wlan_5ghz_interface);
                                                        print("TEST STEP 11: Get the MAC address of wlan client")
                                                        print("MAC retreived is %s" %MAC5)

                                                        print("TEST STEP 11: From wlan client, Disconnect from the wifi ssid")
                                                        status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_5ghz_interface);
                                                        if expectedresult in status:
                                                            tdkTestObj.setResultStatus("SUCCESS");
                                                            print("Disconnect from WIFI SSID: SUCCESS")

                                                            if MAC5:
                                                                # Set the SSID name,password,Radio enable status ,macFilterEnable, macFilterBlackList
                                                                setValuesList = ['true','false','true','true'];
                                                                print("Parameter values that are set: %s" %setValuesList)

                                                                list1 = [macFilterEnable2,'true','bool']
                                                                list2 = [macFilterBlackList2,'false','bool']

                                                                list3 = [macFilterEnable5,'true','bool']
                                                                list4 = [macFilterBlackList5,'true','bool']

                                                                #Concatenate the lists with the elements separated by pipe
                                                                setParamList2 = list1 + list2
                                                                setParamList5 = list3 + list4
                                                                setParamList2 = "|".join(map(str, setParamList2))
                                                                setParamList5 = "|".join(map(str, setParamList5))

                                                                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList2)
                                                                tdkTestObj,actualresult1,details1= setMultipleParameterValues(obj,setParamList5)
                                                                if expectedresult in actualresult and expectedresult in actualresult1:
                                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                                    print("TEST STEP 12: Set the macFilterEnable, macFilterBlackList")
                                                                    print("EXPECTED RESULT 12: Should set the macFilterEnable, macFilterBlackList")
                                                                    print("ACTUAL RESULT 12: %s %s" %(details,details1));
                                                                    print("[TEST EXECUTION RESULT] : %s %s" %(actualresult,actualresult1))

                                                                    #Retrieve the values after set and compare
                                                                    newParamList=[macFilterEnable2,macFilterBlackList2,macFilterEnable5,macFilterBlackList5]
                                                                    tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                                                                    if expectedresult in status and setValuesList == newValues:
                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                        print("TEST STEP 13: Get the current macFilterEnable, macFilterBlackList")
                                                                        print("EXPECTED RESULT 13: Should retrieve the current macFilterEnable, macFilterBlackList")
                                                                        print("ACTUAL RESULT 13: %s" %newValues);
                                                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                                                        # Adding a new MACFilter rule for 2.4 GHz
                                                                        tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject");
                                                                        tdkTestObj.addParameter("paramName","Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable." %tdkbE2EUtility.ssid_2ghz_index);
                                                                        tdkTestObj.executeTestCase(expectedresult);
                                                                        actualresult = tdkTestObj.getResult();
                                                                        details = tdkTestObj.getResultDetails();
                                                                        if expectedresult in actualresult:
                                                                            #Set the result status of execution
                                                                            tdkTestObj.setResultStatus("SUCCESS");
                                                                            print("TEST STEP 14 Adding new Mac filter rule");
                                                                            print("EXPECTED RESULT 14: Should add new rule");
                                                                            print("ACTUAL RESULT 14: added new rule %s" %details);
                                                                            print("[TEST EXECUTION RESULT] : SUCCESS");
                                                                            temp = details.split(':');
                                                                            instance2= temp[1];
                                                                            print("2.4 INSTANCE VALUE: %s" %instance2)

                                                                            if (int(instance2) > 0):
                                                                                #Adding a new MACFilter rule for 5GHz
                                                                                tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject");
                                                                                tdkTestObj.addParameter("paramName","Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable." %tdkbE2EUtility.ssid_5ghz_index);
                                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                                actualresult = tdkTestObj.getResult();
                                                                                details = tdkTestObj.getResultDetails();
                                                                                if expectedresult in actualresult:
                                                                                    #Set the result status of execution
                                                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                                                    print("TEST STEP 15: Adding new Mac filter rule");
                                                                                    print("EXPECTED RESULT 15: Should add new rule");
                                                                                    print("ACTUAL RESULT 15: added new rule %s" %details);
                                                                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                                                                    temp = details.split(':');
                                                                                    instance5= temp[1];
                                                                                    print("5 INSTANCE VALUE: %s" %instance5)

                                                                                    if (int(instance5) > 0):

                                                                                        #Set the name and MAC of the device to be blocked
                                                                                        deviceName2 = "Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable.%s.DeviceName" %(tdkbE2EUtility.ssid_2ghz_index, instance2)
                                                                                        deviceMAC2 = "Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable.%s.MACAddress" %(tdkbE2EUtility.ssid_2ghz_index, instance2)
                                                                                        deviceName5 = "Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable.%s.DeviceName" %(tdkbE2EUtility.ssid_5ghz_index, instance5)
                                                                                        deviceMAC5 = "Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable.%s.MACAddress" %(tdkbE2EUtility.ssid_5ghz_index, instance5)

                                                                                        setValuesList = [tdkbE2EUtility.ssid_2ghz_name,MAC2,tdkbE2EUtility.ssid_5ghz_name,MAC5]
                                                                                        print("Parameter values that are set: %s" %setValuesList)
                                                                                        list1 = [deviceName2,tdkbE2EUtility.ssid_2ghz_name,'string']
                                                                                        list2 = [deviceMAC2,MAC2,'string']
                                                                                        list3 = [deviceName5,tdkbE2EUtility.ssid_5ghz_name,'string']
                                                                                        list4 = [deviceMAC5,MAC5,'string']

                                                                                        #Concatenate the lists with the elements separated by pipe
                                                                                        setParamList2 = list1 + list2
                                                                                        setParamList5 = list3 + list4
                                                                                        setParamList2 = "|".join(map(str, setParamList2))
                                                                                        setParamList5 = "|".join(map(str, setParamList5))

                                                                                        tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList2)
                                                                                        tdkTestObj,actualresult1,details1 = setMultipleParameterValues(obj,setParamList5)
                                                                                        if expectedresult in actualresult and expectedresult in actualresult1:
                                                                                            tdkTestObj.setResultStatus("SUCCESS");
                                                                                            print("TEST STEP 16: Set the name and MAC of client device in the filter")
                                                                                            print("EXPECTED RESULT 16: Should set the name and MAC of client device in the filter")
                                                                                            print("ACTUAL RESULT 16: %s" %details);
                                                                                            print("[TEST EXECUTION RESULT] : SUCCESS");

                                                                                            #Retrieve the values after set and compare
                                                                                            newParamList=[deviceName2,deviceMAC2,deviceName5,deviceMAC5]
                                                                                            time.sleep(60);
                                                                                            tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)
                                                                                            newValues[1] = newValues[1].lower()
                                                                                            newValues[3] = newValues[3].lower()

                                                                                            if expectedresult in status and setValuesList == newValues:
                                                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                                                print("TEST STEP 17: Get the current value of name and MAC of client device in the filter")
                                                                                                print("EXPECTED RESULT 17: Should retrieve the current name and mac of client device in the filter")
                                                                                                print("ACTUAL RESULT 17: %s" %newValues);
                                                                                                print("[TEST EXECUTION RESULT] : SUCCESS");

                                                                                                #Connect to the 2.4wifi ssid from wlan client after enabling MAC filtering
                                                                                                print("TEST STEP 18: From wlan client, try to Connect to the 2.4 wifi ssid with mac filtering enabled")
                                                                                                status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.wlan_2ghz_interface);
                                                                                                if expectedresult in status:
                                                                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                                                                    finalStatus1 = "SUCCESS";
                                                                                                    print("EXPECTED RESULT 18: Connection attempt should be success after enabling the MAC filter")
                                                                                                    print("ACTUAL RESULT 18: Connection from client is success after enabling the MAC filter")
                                                                                                    print("TEST STEP 19: From wlan client, Disconnect from the wifi ssid")
                                                                                                    status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_2ghz_interface);
                                                                                                    if expectedresult in status:
                                                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                                                        print("Disconnect from WIFI SSID: SUCCESS")
                                                                                                        #Connect to the 5 wifi ssid from wlan client after enabling MAC filtering
                                                                                                        print("TEST STEP 20: From wlan client, try to Connect to the 5GHz wifi ssid with mac filtering enabled")
                                                                                                        status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd,tdkbE2EUtility.wlan_5ghz_interface);
                                                                                                        if expectedresult not in status:
                                                                                                            tdkTestObj.setResultStatus("SUCCESS");
                                                                                                            finalStatus2 = "SUCCESS";
                                                                                                            print("EXPECTED RESULT 20: Connection attempt should fail after enabling the MAC filter")
                                                                                                            print("ACTUAL RESULT 20: Connection from client failed after enabling the MAC filter")
                                                                                                        else:
                                                                                                            tdkTestObj.setResultStatus("FAILURE");
                                                                                                            print("EXPECTED RESULT 20 Connection attempt should fail after enabling the MAC filter")
                                                                                                            print("ACTUAL RESULT 20: Connection from client is success even after enabling the MAC filter")
                                                                                                            print("TEST STEP 21: From wlan client, Disconnect from the wifi ssid")
                                                                                                            status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_5ghz_interface);
                                                                                                            if expectedresult in status:
                                                                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                                                                print("Disconnect from WIFI SSID: SUCCESS")
                                                                                                            else:
                                                                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                                                                print("TEST STEP 21:Disconnect from 5GHz WIFI SSID: FAILED")
                                                                                                    else:
                                                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                                                        print("TEST STEP 20:Disconnect from 2.4GHz WIFI SSID: FAILED")
                                                                                                else:
                                                                                                    tdkTestObj.setResultStatus("FAILURE");
                                                                                                    print("EXPECTED RESULT 19: Connection attempt should be success after enabling the MAC filter")
                                                                                                    print("ACTUAL RESULT 19: Connection from client failed after enabling the MAC filter")


                                                                                            else:
                                                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                                                print("TEST STEP 18: Get the current value of name and MAC of client device in the filter")
                                                                                                print("EXPECTED RESULT 18: Should retrieve the current name and mac of client device in the filter")
                                                                                                print("ACTUAL RESULT 18: %s" %newValues);
                                                                                                print("[TEST EXECUTION RESULT] : FAILURE");

                                                                                        else:
                                                                                            tdkTestObj.setResultStatus("FAILURE");
                                                                                            print("TEST STEP 17: Set the name and MAC of client device in the filter")
                                                                                            print("EXPECTED RESULT 17: Should set the name and MAC of client device in the filter")
                                                                                            print("ACTUAL RESULT 17: %s" %details);
                                                                                            print("[TEST EXECUTION RESULT] : FAILURE");

                                                                                        #Delete the created table entry
                                                                                        tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject");
                                                                                        tdkTestObj.addParameter("paramName","Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable.%s." %(tdkbE2EUtility.ssid_5ghz_index,instance5));
                                                                                        expectedresult = "SUCCESS";
                                                                                        tdkTestObj.executeTestCase(expectedresult);
                                                                                        actualresult = tdkTestObj.getResult();
                                                                                        print("[TEST EXECUTION RESULT] : %s" %actualresult) ;
                                                                                        details = tdkTestObj.getResultDetails();

                                                                                        if expectedresult in actualresult:
                                                                                            #Set the result status of execution
                                                                                            tdkTestObj.setResultStatus("SUCCESS");
                                                                                            print("[TEST STEP ]: Deleting the added rule");
                                                                                            print("[EXPECTED RESULT ]: Should delete the added rule");
                                                                                            print("[ACTUAL RESULT]: %s" %details);
                                                                                            print("[TEST EXECUTION RESULT] : %s" %actualresult);
                                                                                            print("Added table is deleted successfully\n")
                                                                                        else:
                                                                                            tdkTestObj.setResultStatus("FAILURE");
                                                                                            print("[TEST STEP ]: Deleting the added rule");
                                                                                            print("[EXPECTED RESULT ]: Should delete the added rule");
                                                                                            print("[ACTUAL RESULT]: %s" %details);
                                                                                            print("[TEST EXECUTION RESULT] : %s" %actualresult);
                                                                                            print("Added table could not be deleted\n")
                                                                                    else:
                                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                                        print("Invalid INSTANCE VALUE: %s" %instance5)
                                                                                else:
                                                                                    tdkTestObj.setResultStatus("FAILURE");
                                                                                    print("TEST STEP 16: Adding new Mac filter rule");
                                                                                    print("EXPECTED RESULT 16: Should add new rule");
                                                                                    print("ACTUAL RESULT 16: adding new rule failed%s" %details);
                                                                                    print("[TEST EXECUTION RESULT] : FAILURE");

                                                                                #Delete the created table entry
                                                                                tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject");
                                                                                tdkTestObj.addParameter("paramName","Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable.%s." %(tdkbE2EUtility.ssid_2ghz_index,instance2));
                                                                                expectedresult = "SUCCESS";
                                                                                tdkTestObj.executeTestCase(expectedresult);
                                                                                actualresult = tdkTestObj.getResult();
                                                                                print("[TEST EXECUTION RESULT] : %s" %actualresult) ;
                                                                                details = tdkTestObj.getResultDetails();

                                                                                if expectedresult in actualresult:
                                                                                    #Set the result status of execution
                                                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                                                    print("[TEST STEP ]: Deleting the added rule");
                                                                                    print("[EXPECTED RESULT ]: Should delete the added rule");
                                                                                    print("[ACTUAL RESULT]: %s" %details);
                                                                                    print("[TEST EXECUTION RESULT] : %s" %actualresult);
                                                                                    print("Added table is deleted successfully\n")
                                                                                else:
                                                                                    tdkTestObj.setResultStatus("FAILURE");
                                                                                    print("[TEST STEP ]: Deleting the added rule");
                                                                                    print("[EXPECTED RESULT ]: Should delete the added rule");
                                                                                    print("[ACTUAL RESULT]: %s" %details);
                                                                                    print("[TEST EXECUTION RESULT] : %s" %actualresult);
                                                                                    print("Added table could not be deleted\n")
                                                                            else:
                                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                                print("Invalid INSTANCE VALUE: %s" %instance2)
                                                                        else:
                                                                            tdkTestObj.setResultStatus("FAILURE");
                                                                            print("TEST STEP 14: Adding new Mac filter rule");
                                                                            print("EXPECTED RESULT 14: Should add new rule");
                                                                            print("ACTUAL RESULT 14: adding new rule failed%s" %details);
                                                                            print("[TEST EXECUTION RESULT] : FAILURE");
                                                                    else:
                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                        print("TEST STEP 13: Get the current macFilterEnable, macFilterBlackList")
                                                                        print("EXPECTED RESULT 13: Should retrieve the current macFilterEnable, macFilterBlackList")
                                                                        print("ACTUAL RESULT 13: %s" %newValues);
                                                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                                                else:
                                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                                    print("TEST STEP 12: Set the macFilterEnable, macFilterBlackList")
                                                                    print("EXPECTED RESULT 12: Should set the macFilterEnable, macFilterBlackList")
                                                                    print("ACTUAL RESULT 12: %s %s" %(details,details1));
                                                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                                            else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print("TEST STEP : Get the wlan MAC");
                                                                print("[TEST EXECUTION RESULT] : FAILURE");
                                                        else:
                                                            tdkTestObj.setResultStatus("FAILURE");
                                                            print("TEST STEP :Disconnect from WIFI SSID: FAILED")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("wlan ip address is not in same DHCP range")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("Failed to get the wlan address")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("Failed to connect to wlan client")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP :Disconnect from WIFI SSID: FAILED")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("wlan ip address is not in same DHCP range")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("Failed to get the current LAN IP address DHCP range")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("Failed to get the wlan address")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("Failed to connect to wlan client")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current ssid,keypassphrase")
                    print("EXPECTED RESULT 3: Should retrieve the current ssid,keypassphrase")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Set the ssid,keypassphrase")
                print("EXPECTED RESULT 2: Should set the ssid,keypassphrase")
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");

            #Prepare the list of parameter values to be reverted
            list1 = [ssidName2,orgValue[0],'string']
            list2 = [keyPassPhrase2,orgValue[1],'string']
            list3 = [radioEnable2,orgValue[2],'bool']
            list4 = [macFilterEnable2,orgValue[3],'bool']
            list5 = [macFilterBlackList2,orgValue[4],'bool']

            list6 = [ssidName5,orgValue[5],'string']
            list7 = [keyPassPhrase5,orgValue[6],'string']
            list8 = [radioEnable5,orgValue[7],'bool']
            list9 = [macFilterEnable5,orgValue[8],'bool']
            list10 = [macFilterBlackList5,orgValue[9],'bool']

            #Concatenate the lists with the elements separated by pipe
            setParamList2 = list1 + list2 + list3 + list4 + list5
            setParamList5 = list6 + list7 + list8 + list9 + list10
            setParamList2 = "|".join(map(str, setParamList2))
            setParamList5 = "|".join(map(str, setParamList5))

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList2)
            tdkTestObj,actualresult1,details1 = setMultipleParameterValues(obj,setParamList5)
            if expectedresult in actualresult and expectedresult in actualresult1 and expectedresult in finalStatus1 and expectedresult in finalStatus2:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 20: Set the ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
                print("EXPECTED RESULT 20: Should set the ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
                print("ACTUAL RESULT 20: %s" %details);
                print("[TEST EXECUTION RESULT] : %s" %actualresult);
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 20: Set the ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
                print("EXPECTED RESULT 20: Should set the ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
                print("ACTUAL RESULT 20: %s" %details);
                print("[TEST EXECUTION RESULT] : %s" %actualresult);
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current ssid,keypassphrase,macFilterEnable, macFilterBlackList")
            print("EXPECTED RESULT 1: Should retrieve the current ssid,keypassphrase,macFilterEnable, macFilterBlackList")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        obj.setLoadModuleStatus("FAILURE");
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup();
    obj.unloadModule("tdkb_e2e");
    obj1.unloadModule("advancedconfig");

else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");
