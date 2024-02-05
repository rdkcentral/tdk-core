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
  <name>E2E_XfinityWiFi_Connect2.4GHZ_PreferPrivate</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check if connection to xfinity WiFi 2.4GHZ is failing when PreferPrivate Wifi option is enabled</synopsis>
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
    <test_case_id>TC_TDKB_E2E_464</test_case_id>
    <test_objective>Check if connection to xfinity WiFi 2.4GHZ is failing when PreferPrivate Wifi option is enabled</test_objective>
    <test_type>Negative</test_type>
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
4. Get and save the value of Device.WiFi.X_RDKCENTRAL-COM_PreferPrivate
5. Set Device.WiFi.X_RDKCENTRAL-COM_PreferPrivate as true
6. From WiFi client machine try to connect to xfinitywiFi2.4GHz
7. Check if the connection attempt failed
8. Revert the value of Device.WiFi.X_RDKCENTRAL-COM_PreferPrivate
9. Revert back the values of XfinityWiFi parameters
10. Unload wifiagent and tdkb_e2e modul</automation_approch>
    <except_output>WiFi client should not be able to connect to  XfinityWiFi2.4GHZ</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e,wifiagent</test_stub_interface>
    <test_script>E2E_XfinityWiFi_Connect2.4GHZ_PreferPrivate</test_script>
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
obj.configureTestCase(ip,port,'E2E_XfinityWiFi_Connect2.4GHZ_PreferPrivate');

#Get the result of connection with test component and DUT
loadmodulestatus =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  ", loadmodulestatus);

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
        tdkTestObj,actualresult,orgValue = getPublicWiFiParamValues(obj);
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1:Get values of PublicWiFi params")
            print("TEST STEP 1 : Should get values of PublicWiFi params")
            print("ACTUAL RESULT 1:%s" %orgValue)
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

                preference = "Device.WiFi.X_RDKCENTRAL-COM_PreferPrivate"
                tdkTestObj,retStatus,pref = getParameterValue(obj,preference)
                if expectedresult in retStatus:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the privatePreference")
                    print("EXPECTED RESULT 3: Should retrieve the current privatePreference")
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    prefParam = "%s|true|boolean" %preference
                    tdkTestObj,prefResult,details = setMultipleParameterValues(obj,prefParam)
                    if expectedresult in prefResult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TEST STEP 4: Set the privatePreference")
                        print("EXPECTED RESULT 4: Should set the privatePreference")
                        print("ACTUAL RESULT 4: %s" %details);
                        print("[TEST EXECUTION RESULT] : SUCCESS");

                        #Retrieve the values after set and compare
                        tdkTestObj,retStatus,newPrefValue = getParameterValue(obj,preference)
                        print("PreferPrivate: %s" %newPrefValue);
                        if expectedresult in retStatus and newPrefValue == "true":
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("TEST STEP 5: Get the current privatePreference")
                            print("EXPECTED RESULT 5: Should retrieve the current privatePreference")
                            print("[TEST EXECUTION RESULT] : SUCCESS");

                            #Connect to the wifi ssid from wlan client
                            print("TEST STEP 6: From wlan client, Connect to the wifi ssid")
                            print("EXPECTED RESULT 6: Connection attempt to xfinity WiFi should fail")
                            status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_2ghz_public_name,"",tdkbE2EUtility.wlan_2ghz_public_ssid_interface,"Open");
                            if expectedresult not in status:
                                tdkTestObj.setResultStatus("SUCCESS");
                                finalStatus = "SUCCESS";
                                print("SUCCESS: WLAN client connection to xfinityWiFi failed")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("FAILURE:Connection to the xfinity2.4GHZ SSID success")

                                status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_2ghz_public_ssid_interface);
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("TEST STEP 10:Disconnect from WIFI SSID: SUCCESS")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 10:Disconnect from WIFI SSID: FAILED")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("TEST STEP 5: Get the current privatePreference")
                            print("EXPECTED RESULT 5: Should retrieve the current privatePreference")
                            print("[TEST EXECUTION RESULT] : FAILURE");

                        #Revert the preference value
                        prefParam = "%s|%s|boolean" %(preference,pref)
                        tdkTestObj,prefResult,details = setMultipleParameterValues(obj,prefParam)
                        if expectedresult in prefResult and expectedresult in finalStatus:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("EXPECTED RESULT 11: Should set the original privatePreference");
                            print("ACTUAL RESULT 11: %s" %details);
                            print("[TEST EXECUTION RESULT] : SUCCESS");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            details = tdkTestObj.getResultDetails();
                            print("EXPECTED RESULT 11: Should set the original privatePreference");
                            print("ACTUAL RESULT 11: %s" %details);
                            print("[TEST EXECUTION RESULT] : FAILURE");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 4: Set the privatePreference as true")
                        print("EXPECTED RESULT 4: Should set the privatePreference as true")
                        print("ACTUAL RESULT 4: %s" %details);
                        print("[TEST EXECUTION RESULT] : FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the privatePreference")
                    print("EXPECTED RESULT 3: Should retrieve the current privatePreference")
                    print("[TEST EXECUTION RESULT] : FAILURE");

                #Revert the values of public wifi params
                tdkTestObj, actualresult, details = setPublicWiFiParamValues(obj,orgValue);
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 11:Revert the PublicWiFi param values")
                    print("TEST STEP 11: Should revert the PublicWiFi values")
                    print("ACTUAL RESULT 11:%s" %details)
                    print("[TEST EXECUTION RESULT] : SUCCESS");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 11:Revert the PublicWiFi param values")
                    print("TEST STEP 11: Should revert the PublicWiFi param values")
                    print("ACTUAL RESULT 11:%s" %details)
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
            print("ACTUAL RESULT 1:%s" %orgValue)
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        print("Failed to parse the configuration file")
        obj.setLoadModuleStatus("FAILURE");
    obj.unloadModule("tdkb_e2e");

else:
    print("Failed to load e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");