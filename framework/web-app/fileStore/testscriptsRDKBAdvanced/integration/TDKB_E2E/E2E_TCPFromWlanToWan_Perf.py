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
  <name>E2E_TCPFromWlanToWan_Perf</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test to monitor the data transfer rate from 2.4WLAN client to WAN client over long duration</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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
    <test_case_id>TC_TDKB_E2E_483</test_case_id>
    <test_objective>Test to monitor the data transfer rate from 2.4WLAN client to WAN client over long duration</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the WIFI client setup is ready and WIFI client is listing the SSIDs properly.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.Radio.2.Enable
Device.WiFi.AccessPoint.2.Security.X_CISCO_COM_EncryptionMethod
Device.WiFi.AccessPoint.2.Security.ModeEnabled
Device.WiFi.AccessPoint.2.Security.KeyPassphrase</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save security mode
3. Set the security mode for 5GHz to WPAWPA2PSK using tdkb_e2e_SetMultipleParams
3. Try to connect to Wifi client and check whether the wifi client is connected to the DUT
4. From the wlan client, do iperf data transfer to WAN client .Monitor the throughput and save its values to an output file
5.Check if the average throughput is within the expected range or not and transfer the output log file to TM
6. Revert the security mode to original value
7.Unload tdkb_e2e module</automation_approch>
    <except_output>Tthe average throughput value during data transfer from WLAN to WAN should be within the expected range</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_TCPFromWlanToWan_Perf</test_script>
    <skipped>No</skipped>
    <release_version>M64</release_version>
    <remarks>WLAN,WAN</remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import tdkbE2EUtility
from tdkbE2EUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_TCPFromWlanToWan_Perf');

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
        securityMode = "Device.WiFi.AccessPoint.%s.Security.ModeEnabled" %tdkbE2EUtility.ssid_2ghz_index
        radioEnable = "Device.WiFi.Radio.%s.Enable" %tdkbE2EUtility.ssid_2ghz_index
        ssidEnable = "Device.WiFi.SSID.%s.Enable" %tdkbE2EUtility.ssid_2ghz_index

        #Get the value of the wifi parameters that are currently set.
        paramList=[ssidName,keyPassPhrase,securityMode,radioEnable,ssidEnable]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
            print("EXPECTED RESULT 1: Should retrieve the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            # Set securityMode,radioEnable and ssidEnable for 2ghz"
            setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,'WPA2-Personal','true','true'];
            print("WIFI parameter values that are set: %s" %setValuesList)

            list1 = [ssidName,tdkbE2EUtility.ssid_2ghz_name,'string']
            list2 = [keyPassPhrase,tdkbE2EUtility.ssid_2ghz_pwd,'string']
            list3 = [securityMode,'WPA2-Personal','string']
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
                    tdkTestObj.setResultStatus("SUCCESS");

                    #Connect to the wifi ssid from wlan client
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
                                    status = addStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress,tdkbE2EUtility.wlan_2ghz_interface);
                                    if expectedresult in status:
                                        print("TEST STEP 8:Static route add success")
                                        tdkTestObj.setResultStatus("SUCCESS");

                                        #Verify TCP from WLAN to LAN
                                        print("TEST STEP 9:Check TCP from WLAN to LAN");
                                        #tdkTestObj.getExecDetails()
                                        status,clientOutput,clientOutput_avg = getThroughput("WLAN","WAN",tdkbE2EUtility.wan_ip,wlanIP,tdkbE2EUtility.wlan_2ghz_throughput_outfile,tdkbE2EUtility.wlan_2ghz_throughput_to_wan,tdkTestObj);
                                        print("Average Bandwidth received from client : %s" %clientOutput_avg);
                                        print("Bandwidth received from client : %s" %clientOutput);
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("Average throughput recieved is within the expected range")
                                            print("TCP from WLAN to LAN : SUCCESS")

                                            print("TEST STEP 10: From wlan client, Disconnect from the wifi ssid")
                                            status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_2ghz_interface);
                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                finalStatus = "SUCCESS";
                                                print("Disconnect from WIFI SSID: SUCCESS")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP 11:Disconnect from WIFI SSID: FAILED")

                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP 10:TCP from WLAN to LAN failed")
                                            print("Average throughput recieved is within the expected range")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 8:Static route add failed")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("checkIpRange:wlan ip address is not in DHCP range")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("getParameterValue : Failed to get gateway lan ip address range")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("getWlanIPAddress:Failed to get the wlan ip address")
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
                print("EXPECTED RESULT 13: Should set the original ssid,keypassphrase,securityMode,radioEnable and ssidEnable");
                print("ACTUAL RESULT 13: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 13: Should set the original ssid,keypassphrase,securityMode,radioEnable and ssidEnable");
                print("ACTUAL RESULT 13: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current ssid,keypassphrase and securityMode")
            print("EXPECTED RESULT 1: Should retrieve the current ssid,keypassphrase and securityMode")
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