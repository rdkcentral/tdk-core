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
  <name>E2E_WIFI_2.4GHZ_802.11n_20MHzBW_FromWlanToWan_GetThroughput</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Configure the GW in 802.11n mode with autochannel enabled, HT20(BW:20MHz), guard interval 400ns. Using iperf check throughput from 2.4GHZWLAN to WAN. The average speed of transfer will be 10mbps depending on class of service constraints.</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>true</advanced_script>
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
    <test_case_id>TC_TDKB_E2E_482</test_case_id>
    <test_objective>Configure the GW in 802.11n mode with autochannel enabled, HT20(BW:20MHz), guard interval 400ns. Using iperf check throughput from 2.4GHZWLAN to WAN. The average speed of transfer will be 10mbps depending on class of service constraints.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.1.SSID
Device.WiFi.AccessPoint.1.Security.KeyPassphrase
Device.WiFi.Radio.1.OperatingStandards
Device.WiFi.Radio.1.AutoChannelEnable
Device.WiFi.Radio.1.OperatingChannelBandwidth
Device.WiFi.Radio.1.GuardInterval </input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save security mode , ssid name ,password,operating stds, autochannel enable, bw, and guard interval
3. Set the security mode for 2.4GHz to WPA2PSK , ssid name, password,operating stds, autochannel enable, bw, and guard interval using tdkb_e2e_SetMultipleParams
4. Connect to the wlan client and get the IP
5. Check the TCP connection from WLAN to WAN and get the throughput
6.Unload tdkb_e2e module</automation_approch>
    <except_output>The average speed of transfer will be 10mbps depending on class of service constraints</except_output>
    <priority>High</priority>
    <test_stub_interface>TDKB_E2E</test_stub_interface>
    <test_script>E2E_WIFI_2.4GHZ_802.11n_20MHzBW_FromWlanToWan_GetThroughput</test_script>
    <skipped>No</skipped>
    <release_version>M63_2</release_version>
    <remarks>WLAN,WAN</remarks>
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

obj.configureTestCase(ip,port,'E2E_WIFI_2.4GHZ_802.11n_20MHzBW_FromWlanToWan_GetThroughput');

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
        operatingStandard = "Device.WiFi.Radio.%s.OperatingStandards" %tdkbE2EUtility.radio_2ghz_index
        autoEnable = "Device.WiFi.Radio.%s.AutoChannelEnable" %tdkbE2EUtility.radio_2ghz_index
        ChannelBW = "Device.WiFi.Radio.%s.OperatingChannelBandwidth" %tdkbE2EUtility.radio_2ghz_index
        GuardInterval = "Device.WiFi.Radio.%s.GuardInterval" %tdkbE2EUtility.radio_2ghz_index

        #Get the value of the wifi parameters that are currently set.
        paramList=[ssidName,keyPassPhrase,operatingStandard,autoEnable,ChannelBW,GuardInterval]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current SSID, KeyPassphrase, operating standard, autoEnable,ChannelBW,GuardInterval")
            print("EXPECTED RESULT 1: Should retrieve the current SSID, KeyPassphrase, operating standard,autoEnable,ChannelBW,GuardInterval")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : %s" %status);

            # Set the operating standard as 'n'
            setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,'n','true','20MHz','400nsec'];
            print("WIFI parameter values that are set: %s" %setValuesList)

            list1 = [ssidName,tdkbE2EUtility.ssid_2ghz_name,'string']
            list2 = [keyPassPhrase,tdkbE2EUtility.ssid_2ghz_pwd,'string']
            list3 = [operatingStandard,'n','string']
            list4 = [autoEnable,'true','bool']
            list5 = [ChannelBW,'20MHz','string']
            list6 = [GuardInterval,'400nsec','string']

            #Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2 + list3 + list4 + list5 + list6
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set the SSID, KeyPassphrase, operating standard,autoEnable,ChannelBW,GuardInterval")
                print("EXPECTED RESULT 2: Should set the SSID, KeyPassphrase, operating standard,autoEnable,ChannelBW,GuardInterval");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : %s" %actualresult);

                #Retrieve the values after set and compare
                newParamList=[ssidName,keyPassPhrase,operatingStandard,autoEnable,ChannelBW,GuardInterval]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current SSID, KeyPassphrase, operating standard,autoEnable,ChannelBW,GuardInterval")
                    print("EXPECTED RESULT 3: Should retrieve the current SSID, KeyPassphrase, operating standard,autoEnable,ChannelBW,GuardInterval")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Wait for the changes to reflect in client device
                    time.sleep(60);

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

                                    #Verify TCP from WAN to WLAN
                                    print("TEST STEP 10:Check TCP from WLAN to WAN");
                                    status,serverOutput,clientOutput = tcp_udpInClients("WLAN","WAN",tdkbE2EUtility.wan_ip,wlanIP,"TCP_Throughput");
                                    print("Bandwidth recieved from server : %s" %serverOutput);
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        bandwidth = serverOutput.split(" ")[0];
                                        #Convert bandwidth to Mbps
                                        if "Gbits/sec" in serverOutput:
                                            throughput = float(bandwidth)*1000;
                                        elif "Kbits/sec" in serverOutput:
                                            throughput = float(bandwidth)*.001;
                                        print(throughput);
                                        print(int(throughput));
                                        if int(throughput) <= 10:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("Throughtput is 10Mbps")

                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("Throughtput is not correct")

                                        print("TEST STEP 9: From wlan client, Disconnect from the wifi ssid")
                                        status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_2ghz_interface);
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            finalStatus = "SUCCESS"
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("Failed to get the throughput")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current SSID, KeyPassphrase, operating standard")
                    print("EXPECTED RESULT 3: Should retrieve the current SSID, KeyPassphrase, operating standard")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("TEST STEP 2: Set the SSID, KeyPassphrase, operating standard")
                print("EXPECTED RESULT 2: Should set the SSID, KeyPassphrase, operating standard");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : %s" %actualresult);

            #Prepare the list of parameter values to be reverted
            list1 = [ssidName,orgValue[0],'string']
            list2 = [keyPassPhrase,orgValue[1],'string']
            list3 = [operatingStandard,orgValue[2],'string']
            list4 = [autoEnable,orgValue[3],'bool']
            list5 = [ChannelBW,orgValue[4],'string']
            list6 = [GuardInterval,orgValue[5],'string']

            #Concatenate the lists with the elements separated by pipe
            revertParamList = list1 + list2 + list3 + list4 +list5 + list6
            revertParamList = "|".join(map(str, revertParamList))

            #Revert the values to original
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
            if expectedresult in actualresult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 10: Should set the original SSID, KeyPassphrase, operating standard");
                print("ACTUAL RESULT 10: %s" %details);
                print("[TEST EXECUTION RESULT] : %s" %actualresult);
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 10: Should set the original SSID, KeyPassphrase, operating standard");
                print("ACTUAL RESULT 10: %s" %details);
                print("[TEST EXECUTION RESULT] : %s" %actualresult);
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current SSID, KeyPassphrase, operating standard")
            print("EXPECTED RESULT 1: Should retrieve the current SSID, KeyPassphrase, operating standard")
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