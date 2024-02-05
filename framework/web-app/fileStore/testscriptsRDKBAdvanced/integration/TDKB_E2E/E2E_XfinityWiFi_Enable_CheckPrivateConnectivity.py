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
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_XfinityWiFi_Enable_CheckPrivateConnectivity</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check if the enabling of XfinityWiFi is not affecting the connectivity to private WiFi</synopsis>
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
    <test_case_id>TC_TDKB_E2E_465</test_case_id>
    <test_objective>Check if the enabling of XfinityWiFi is not affecting the connectivity to private WiFi</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.X_COMCAST-COM_GRE.Tunnel.1.DSCPMarkPolicy
Device.X_COMCAST-COM_GRE.Tunnel.1.DSCPMarkPolicy
Device.X_COMCAST-COM_GRE.Tunnel.1.PrimaryRemoteEndpoint
Device.X_COMCAST-COM_GRE.Tunnel.1.SecondaryRemoteEndpoint
Device.WiFi.SSID.5.SSID
Device.WiFi.SSID.6.SSID
Device.WiFi.SSID.5.Enable
Device.WiFi.SSID.6.Enable
Device.DeviceInfo.X_COMCAST_COM_xfinitywifiEnable</input_parameters>
    <automation_approch>1. Load wifiagent and tdkb_e2e module
 2. Using WIFIAgent_Get, get and save Device.WiFi.SSID.5.Enable, Device.WiFi.SSID.6.Enable
3.Set Device.WiFi.SSID.5.Enable, Device.WiFi.SSID.6.Enable and Device.DeviceInfo.X_COMCAST_COM_xfinitywifiEnable as true to enable xfinityWiFi
4. From WiFi client machine try to connect to private WiFi 2.4GHz
5. Check if the connection attempt was success and client got ip in the expected ip range
6.Disconnect the connection
7. Revert the value of Device.WiFi.X_RDKCENTRAL-COM_PreferPrivate
8. Revert back the values of XfinityWiFi parameters
9. Unload wifiagent and tdkb_e2e module</automation_approch>
    <except_output>Even after enabling Xfinity WiFi, WLAN client should be able to connect to private WiFi SSIDs</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e,wifiagent</test_stub_interface>
    <test_script>E2E_XfinityWiFi_Enable_CheckPrivateConnectivity</test_script>
    <skipped>No</skipped>
    <release_version>M62</release_version>
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

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_XfinityWiFi_Enable_CheckPrivateConnectivity');

#Get the result of connection with test component and DUT
loadmodulestatus =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :   ", loadmodulestatus);

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");

    #Get current values of public wifi params
    expectedresult="SUCCESS";
    finalStatus = "FAILURE"
    #Parse the device configuration file^M
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")
        tdkTestObj,actualresult,orgXFValue = getPublicWiFiParamValues(obj);
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1:Get values of PublicWiFi params")
            print("TEST STEP 1 : Should get values of PublicWiFi params")
            print("ACTUAL RESULT 1:%s" %orgXFValue)
            print("[TEST EXECUTION RESULT] : SUCCESS");

            #Set values to enable public wifi
            setvalues = [tdkbE2EUtility.dscpmarkpolicy,tdkbE2EUtility.primary_remote_end_point,tdkbE2EUtility.secondary_remote_end_point,tdkbE2EUtility.ssid_2ghz_public_name,tdkbE2EUtility.ssid_5ghz_public_name,"true","true","true"];
            tdkTestObj, actualresult, details = setPublicWiFiParamValues(obj,setvalues);
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Enable public wifi")
                print("TEST STEP 2 : Should enable PublicWiFi")
                print("ACTUAL RESULT 2:%s" %details)
                print("[TEST EXECUTION RESULT] : SUCCESS");

                #Assign the WIFI parameters names to a variable
                ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
                keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
                radioEnable = "Device.WiFi.Radio.%s.Enable" %tdkbE2EUtility.radio_2ghz_index
                #Get the value of the wifi parameters that are currently set.
                paramList=[ssidName,keyPassPhrase,radioEnable]
                tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)
                if expectedresult in status :
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current ssid,keypassphrase,Radio enable status")
                    print("EXPECTED RESULT 3: Should retrieve the current ssid,keypassphrase,Radio enable status")
                    print("ACTUAL RESULT 3: %s " %orgValue);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    # Set the SSID name,password,Radio enable status "
                    setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,'true'];
                    print("Parameter values that are set: %s" %setValuesList)

                    list1 = [ssidName,tdkbE2EUtility.ssid_2ghz_name,'string']
                    list2 = [keyPassPhrase,tdkbE2EUtility.ssid_2ghz_pwd,'string']
                    list3 = [radioEnable,'true','bool']
                    #Concatenate the lists with the elements separated by pipe
                    setParamList = list1 + list2 + list3
                    setParamList = "|".join(map(str, setParamList))

                    tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                    if expectedresult in actualresult :
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TEST STEP 4: Set the ssid,keypassphrase,Radio enable status")
                        print("EXPECTED RESULT 4: Should set the ssid,keypassphrase,Radio enable status");
                        print("ACTUAL RESULT 4: %s" %details);
                        print("[TEST EXECUTION RESULT] : SUCCESS");

                        #Retrieve the values after set and compare
                        newParamList=[ssidName,keyPassPhrase,radioEnable]
                        tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)
                        if expectedresult in status and setValuesList == newValues:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("TEST STEP 5: Get the current ssid,keypassphrase,Radio enable status")
                            print("EXPECTED RESULT 5: Should retrieve the current ssid,keypassphrase,Radio enable status")
                            print("ACTUAL RESULT 5: %s " %newValues);
                            print("[TEST EXECUTION RESULT] : SUCCESS");

                            #Wait for the changes to reflect in client device
                            time.sleep(60);

                            #Connect to the wifi ssid from wlan client
                            print("TEST STEP 6: From wlan client, Connect to the wifi ssid")
                            status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.wlan_2ghz_interface);
                            if expectedresult in status:
                                tdkTestObj.setResultStatus("SUCCESS");

                                print("TEST STEP 7: Get the IP address of the wlan client after connecting to wifi")
                                wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_2ghz_interface);
                                if wlanIP:
                                    tdkTestObj.setResultStatus("SUCCESS");

                                    print("TEST STEP 8: Get the current LAN IP address DHCP range")
                                    param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                    tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                                    print("LAN IP Address: %s" %curIPAddress);

                                    if expectedresult in status and curIPAddress:
                                        tdkTestObj.setResultStatus("SUCCESS");

                                        print("TEST STEP 9: Check whether wlan ip address is in same DHCP range")
                                        status = "SUCCESS"
                                        status = checkIpRange(curIPAddress,wlanIP);
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("wlan ip address is in same DHCP range")

                                            status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_2ghz_interface);
                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                finalStatus = "SUCCESS";
                                                print("TEST STEP 10:Disconnect from WIFI SSID: SUCCESS")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP 10:Disconnect from WIFI SSID: FAILED")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP 9:WLAN Client IP address is not in the same Gateway DHCP range")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 8:Failed to get the Gateway IP address")

                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 7:Failed to get the WLAN Client IP address")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 6:Failed to connect to WIFI SSID")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("TEST STEP 5: Get the current ssid,keypassphrase,Radio enable status")
                            print("EXPECTED RESULT 5: Should retrieve the current ssid,keypassphrase,Radio enable status")
                            print("ACTUAL RESULT 5: %s " %newValues);
                            print("[TEST EXECUTION RESULT] : FAILURE");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print("TEST STEP 4: Set the ssid,keypassphrase,Radio enable status")
                        print("EXPECTED RESULT 4: Should set the ssid,keypassphrase,Radio enable status");
                        print("ACTUAL RESULT 4: %s" %details);
                        print("[TEST EXECUTION RESULT] : FAILURE");

                    #Prepare the list of parameter values to be reverted
                    list1 = [ssidName,orgValue[0],'string']
                    list2 = [keyPassPhrase,orgValue[1],'string']
                    list3 = [radioEnable,orgValue[2],'bool']

                    #Concatenate the lists with the elements separated by pipe
                    revertParamList = list1 + list2 + list3
                    revertParamList = "|".join(map(str, revertParamList))
#Revert         the values to original
                    tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
                    if expectedresult in actualresult and expectedresult in finalStatus:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("EXPECTED RESULT 11: Should set the original ssid,keypassphrase,Radio enable status");
                        print("ACTUAL RESULT 11: %s" %details);
                        print("[TEST EXECUTION RESULT] : SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print("EXPECTED RESULT 11: Should set the original ssid,keypassphrase,Radio enable status");
                        print("ACTUAL RESULT 11: %s" %details);
                        print("[TEST EXECUTION RESULT] : FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current ssid,keypassphrase,Radio enable status")
                    print("EXPECTED RESULT 3: Should retrieve the current ssid,keypassphrase,Radio enable status")
                    print("ACTUAL RESULT 3: %s " %orgValue);
                    print("[TEST EXECUTION RESULT] : FAILURE");

                #Revert the values of public wifi params
                tdkTestObj, actualresult, details = setPublicWiFiParamValues(obj,orgXFValue);
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 12:Revert the PublicWiFi param values")
                    print("TEST STEP 12: Should revert the PublicWiFi values")
                    print("ACTUAL RESULT 12:%s" %details)
                    print("[TEST EXECUTION RESULT] : SUCCESS");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 12:Revert the PublicWiFi param values")
                    print("TEST STEP 12: Should revert the PublicWiFi param values")
                    print("ACTUAL RESULT 12:%s" %details)
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Enable public wifi")
                print("TEST STEP 2 : Should enable PublicWiFi")
                print("ACTUAL RESULT 2:%s" %details)
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1:Get values of PublicWiFi params")
            print("TEST STEP 1 : Should get values of PublicWiFi params")
            print("ACTUAL RESULT 1:%s" %orgXFValue)
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        obj.setLoadModuleStatus("FAILURE");
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup();
    obj.unloadModule("tdkb_e2e");
else:
    print("FAILURE to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");