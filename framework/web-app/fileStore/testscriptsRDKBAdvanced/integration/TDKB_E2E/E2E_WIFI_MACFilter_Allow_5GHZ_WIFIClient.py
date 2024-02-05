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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_WIFI_MACFilter_Allow_5GHZ_WIFIClient</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify that MAC Filter based Access control allow specific clients that are connected via 5GHz radio</synopsis>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_138</test_case_id>
    <test_objective>Verify that MAC Filter based Access control allow specific clients that are connected via 5GHz radio</test_objective>
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
2. Using tdkb_e2e_Get, get and save MACFilter.FilterAsBlackList, MACFilter.Enable
3.  Connect to the WIFI client and get the MAC address of the WLAN  interface
4. Disconnect the WiFi client
5. Enable MACFilter.Enable and disable MACFilter.FilterAsBlackList
6.Add new rule to Device.WiFi.AccessPoint.2.X_CISCO_COM_MacFilterTable.
7. Set the devicename and mac details of client to be blocked in the MAC filter rule
8.Try to connect the blocked client to the GW 5GHZ SSID. That connection attempt should be success
9.Delete the added rule and revert all params values
10.Unload tdkb_e2e module</automation_approch>
    <except_output>After adding the blocking rule, as the black list option is disabled, the client should be able to connect</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WIFI_MACFilter_Allow_5GHZ_WIFIClient</test_script>
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
obj.configureTestCase(ip,port,'E2E_WIFI_MACFilter_Allow_5GHZ_WIFIClient');
obj1.configureTestCase(ip,port,'E2E_WIFI_MACFilter_Allow_5GHZ_WIFIClient');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 =obj1.getLoadModuleResult();

print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS");
    obj1.setLoadModuleStatus("SUCCESS");
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
        radioEnable = "Device.WiFi.Radio.%s.Enable" %tdkbE2EUtility.radio_5ghz_index
        macFilterEnable = "Device.WiFi.AccessPoint.%s.X_CISCO_COM_MACFilter.Enable" %tdkbE2EUtility.ssid_5ghz_index
        macFilterBlackList = "Device.WiFi.AccessPoint.%s.X_CISCO_COM_MACFilter.FilterAsBlackList" %tdkbE2EUtility.ssid_5ghz_index

        #Get the value of the wifi parameters that are currently set.
        paramList=[ssidName,keyPassPhrase,radioEnable,macFilterEnable,macFilterBlackList]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
            print("EXPECTED RESULT 1: Should retrieve the current ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
            print("ACTUAL RESULT 1:  %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            # Set the SSID name,password,Radio enable status ,macFilterEnable, macFilterBlackList
            setValuesList = [tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd,'true'];
            print("Parameter values that are set: %s" %setValuesList)

            list1 = [ssidName,tdkbE2EUtility.ssid_5ghz_name,'string']
            list2 = [keyPassPhrase,tdkbE2EUtility.ssid_5ghz_pwd,'string']
            list3 = [radioEnable,'true','bool']

            #Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2 + list3
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set the ssid,keypassphrase,Radio enable status")
                print("EXPECTED RESULT 2: Should set the ssid,keypassphrase,Radio enable status")
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : %s" %actualresult);

                #Retrieve the values after set and compare
                newParamList=[ssidName,keyPassPhrase,radioEnable]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current SSID, KeyPassphrase")
                    print("EXPECTED RESULT 3: Should retrieve the current SSID, KeyPassphrase")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : SUCCESS")
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
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    #From the client, get its MAC
                                    MAC = getWlanMACAddress(tdkbE2EUtility.wlan_5ghz_interface);
                                    print("TEST STEP : Get the MAC address of wlan client")
                                    print("MAC retrieved is %s" %MAC)

                                    print("TEST STEP : From wlan client, Disconnect from the wifi ssid")
                                    status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_5ghz_interface);
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("Disconnect from WIFI SSID: SUCCESS")

                                        if MAC:
                                            # Set the macFilterEnable, macFilterBlackList
                                            setValuesList = ['true','false'];
                                            print("Parameter values that are set: %s" %setValuesList)

                                            list1 = [macFilterEnable,'true','bool']
                                            list2 = [macFilterBlackList,'false','bool']

                                            #Concatenate the lists with the elements separated by pipe
                                            setParamList = list1 + list2
                                            setParamList = "|".join(map(str, setParamList))

                                            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                                            if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print("TEST STEP 8: Set the macFilterEnable, macFilterBlackList")
                                                print("EXPECTED RESULT 8: Should set the macFilterEnable, macFilterBlackList")
                                                print("ACTUAL RESULT 8: %s" %details);
                                                print("[TEST EXECUTION RESULT] : %s" %actualresult);

                                                #Retrieve the values after set and compare
                                                newParamList=[macFilterEnable,macFilterBlackList]
                                                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                                                if expectedresult in status and setValuesList == newValues:
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("TEST STEP 9: Get the current macFilterEnable, macFilterBlackList")
                                                    print("EXPECTED RESULT 9: Should retrieve the current macFilterEnable, macFilterBlackList")
                                                    print("ACTUAL RESULT 9: %s" %newValues);
                                                    print("[TEST EXECUTION RESULT] : SUCCESS")
                                                    #Wait for the changes to reflect in client device
                                                    time.sleep(60);

                                                    # Adding a new row to BlockedSite
                                                    tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject");
                                                    tdkTestObj.addParameter("paramName","Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable." %tdkbE2EUtility.ssid_5ghz_index);
                                                    tdkTestObj.executeTestCase(expectedresult);
                                                    actualresult = tdkTestObj.getResult();
                                                    details = tdkTestObj.getResultDetails();
                                                    if expectedresult in actualresult:
                                                        #Set the result status of execution
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print("TEST STEP 10: Adding new Mac filter rule");
                                                        print("EXPECTED RESULT 10: Should add new rule");
                                                        print("ACTUAL RESULT 10: added new rule %s" %details);
                                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                                        temp = details.split(':');
                                                        instance = temp[1];

                                                        if (instance > 0):
                                                            print("INSTANCE VALUE: %s" %instance)
                                                            #Set the name and MAC of the device to be blocked
                                                            deviceName = "Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable.%s.DeviceName" %(tdkbE2EUtility.ssid_5ghz_index, instance)
                                                            deviceMAC = "Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable.%s.MACAddress" %(tdkbE2EUtility.ssid_5ghz_index, instance)

                                                            setValuesList = [tdkbE2EUtility.ssid_5ghz_name,MAC]
                                                            print("Parameter values that are set: %s" %setValuesList)
                                                            list1 = [deviceName,tdkbE2EUtility.ssid_5ghz_name,'string']
                                                            list2 = [deviceMAC,MAC,'string']

                                                            #Concatenate the lists with the elements separated by pipe
                                                            setParamList= list1 + list2
                                                            setParamList = "|".join(map(str, setParamList))

                                                            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                                                            if expectedresult in actualresult:
                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                print("TEST STEP 11: Set the name and MAC of client device in the filter")
                                                                print("EXPECTED RESULT 11: Should set the name and MAC of client device in the filter")
                                                                print("ACTUAL RESULT 11: %s" %details);
                                                                print("[TEST EXECUTION RESULT] : SUCCESS");

                                                                #Retrieve the values after set and compare
                                                                newParamList=[deviceName,deviceMAC]
                                                                time.sleep(60);
                                                                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)
                                                                if expectedresult in status and setValuesList == newValues:
                                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                                    print("TEST STEP 12: Get the current value of name and MAC of client device in the filter")
                                                                    print("EXPECTED RESULT 12: Should retrieve the current name and mac of client device in the filter")
                                                                    print("ACTUAL RESULT 12: %s" %newValues);
                                                                    print("[TEST EXECUTION RESULT] : SUCCESS");

                                                                    #Connect to the wifi ssid from wlan client after enabling MAC filtering
                                                                    print("TEST STEP 13: From wlan client, try to Connect to the wifi ssid with mac filtering enabled")
                                                                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd,tdkbE2EUtility.wlan_5ghz_interface);
                                                                    if expectedresult in status:
                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                        finalStatus = "SUCCESS";
                                                                        print("EXPECTED RESULT 13: Connection attempt should be success after enabling the MAC filter")
                                                                        print("ACTUAL RESULT 13: Connection from client is success after enabling the MAC filter")
                                                                        print("TEST STEP 14: From wlan client, Disconnect from the wifi ssid")
                                                                        status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_5ghz_interface);
                                                                        if expectedresult in status:
                                                                            tdkTestObj.setResultStatus("SUCCESS");
                                                                            print("Disconnect from WIFI SSID: SUCCESS")
                                                                        else:
                                                                            tdkTestObj.setResultStatus("FAILURE");
                                                                            print("TEST STEP 14:Disconnect from WIFI SSID: FAILED")
                                                                    else:
                                                                        tdkTestObj.setResultStatus("FAILURE");
                                                                        print("EXPECTED RESULT 13: Connection attempt should be success after enabling the MAC filter")
                                                                        print("ACTUAL RESULT 13: Connection from client failed after enabling the MAC filter")
                                                                else:
                                                                    tdkTestObj.setResultStatus("FAILURE");
                                                                    print("TEST STEP 12: Get the current value of name and MAC of client device in the filter")
                                                                    print("EXPECTED RESULT 12: Should retrieve the current name and mac of client device in the filter")
                                                                    print("ACTUAL RESULT 12: %s" %newValues);
                                                                    print("[TEST EXECUTION RESULT] : FAILURE");

                                                            else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print("TEST STEP 11: Set the name and MAC of client device in the filter")
                                                                print("EXPECTED RESULT 11: Should set the name and MAC of client device in the filter")
                                                                print("ACTUAL RESULT 11: %s" %details);
                                                                print("[TEST EXECUTION RESULT] : FAILURE");

                                                            #Delete the created table entry
                                                            tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject");
                                                            tdkTestObj.addParameter("paramName","Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable.%s." %(tdkbE2EUtility.ssid_5ghz_index,instance));
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
                                                            print("Invalid INSTANCE VALUE: %s" %instance)
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("TEST STEP 10: Adding new Mac filter rule");
                                                        print("EXPECTED RESULT 10: Should add new rule");
                                                        print("ACTUAL RESULT 10: adding new rule failed%s" %details);
                                                        print("[TEST EXECUTION RESULT] : FAILURE");
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("TEST STEP 9: Get the current macFilterEnable, macFilterBlackList")
                                                    print("EXPECTED RESULT 9: Should retrieve the current macFilterEnable, macFilterBlackList")
                                                    print("ACTUAL RESULT 9: %s" %newValues);
                                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP 8: Set the macFilterEnable, macFilterBlackList")
                                                print("EXPECTED RESULT 8: Should set the macFilterEnable, macFilterBlackList")
                                                print("ACTUAL RESULT 8: %s" %details);
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
                                print("Failed to get the current LAN IP address DHCP range")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("Failed to get the wlan address")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("Failed to connect to wlan client")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current ssid,keypassphrase,macFilterEnable, macFilterBlackList")
                    print("EXPECTED RESULT 3: Should retrieve the current ssid,keypassphrase,macFilterEnable, macFilterBlackList")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Set the ssid,keypassphrase,macFilterEnable, macFilterBlackList")
                print("EXPECTED RESULT 2: Should set the ssid,keypassphrase,macFilterEnable, macFilterBlackList")
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");

            #Prepare the list of parameter values to be reverted
            list1 = [ssidName,orgValue[0],'string']
            list2 = [keyPassPhrase,orgValue[1],'string']
            list3 = [radioEnable,orgValue[2],'bool']

            list4 = [macFilterEnable,orgValue[3],'bool']
            list5 = [macFilterBlackList,orgValue[4],'bool']

            #Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2 + list3 + list4 + list5
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
            if expectedresult in actualresult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 15: Set the ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
                print("EXPECTED RESULT 15: Should set the ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
                print("ACTUAL RESULT 15: %s" %details);
                print("[TEST EXECUTION RESULT] : %s" %actualresult);
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 15: Set the ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
                print("EXPECTED RESULT 15: Should set the ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
                print("ACTUAL RESULT 15: %s" %details);
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