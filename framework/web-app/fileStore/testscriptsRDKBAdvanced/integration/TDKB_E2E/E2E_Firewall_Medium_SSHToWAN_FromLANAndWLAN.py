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
  <name>E2E_Firewall_Medium_SSHToWAN_FromLANAndWLAN</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify that when Firewall Config is set to Medium SSH access from LAN to WAN and WLAN to WAN should  be success</synopsis>
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
    <test_case_id>TC_TDKB_E2E_470</test_case_id>
    <test_objective>Verify that when Firewall Config is set to Medium SSH access from LAN to WAN and WLAN to WAN should  be success</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.1.SSID
Device.X_CISCO_COM_Security.Firewall.FirewallLevel
Device.WiFi.AccessPoint.1.Security.KeyPassphrase</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save firewallLevel
3. Set the firewall to Medium using tdkb_e2e_SetMultipleParams
3. Login to the LAN client and get the IP address assigned by the gateway
4. Login to the WLAN client and get the IP address assigned by the gateway
5. From the wlan client, do SSH to the WAN client and check whether  it is success
6.From the lan client, do SSH to the WAN client and check whether  it is sucess
7. Revert the firewall to original value
8.Unload tdkb_e2e module</automation_approch>
    <except_output>The SSH to WAN from WLAN and LAN should be success when firewall is medium</except_output>
    <priority>High</priority>
    <test_stub_interface>TDKB_E2E</test_stub_interface>
    <test_script>E2E_Firewall_Medium_SSHToWAN_FromLANAndWLAN</test_script>
    <skipped>No</skipped>
    <release_version>M62</release_version>
    <remarks>WLAN,LAN,WAN</remarks>
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
obj.configureTestCase(ip,port,'E2E_Firewall_Medium_SSHToWAN_FromLANAndWLAN');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    sshFromWlan = ""
    sshFromLan = ""

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

        #Assign the WIFI parameters names to a variable
        ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
        keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
        radioEnable = "Device.WiFi.Radio.%s.Enable" %tdkbE2EUtility.radio_2ghz_index
        firewallLevel = "Device.X_CISCO_COM_Security.Firewall.FirewallLevel"

        #Get the value of the wifi parameters that are currently set.
        paramList=[ssidName,keyPassPhrase,radioEnable]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)
        tdkTestObj1,retStatus,firewallValue = getParameterValue(obj,firewallLevel)
        print("Firewall Level: %s" %firewallValue);

        if expectedresult in status and expectedresult in retStatus:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current ssid,keypassphrase,Radio enable status,firewall level")
            print("EXPECTED RESULT 1: Should retrieve the current ssid,keypassphrase,Radio enable status,firewall level")
            print("ACTUAL RESULT 1: %s %s" %(orgValue,firewallValue));
            print("[TEST EXECUTION RESULT] : SUCCESS");

            # Set the SSID name,password,Radio enable status and firewall level"
            setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,'true'];
            print("Parameter values that are set: %s" %setValuesList)

            list1 = [ssidName,tdkbE2EUtility.ssid_2ghz_name,'string']
            list2 = [keyPassPhrase,tdkbE2EUtility.ssid_2ghz_pwd,'string']
            list3 = [radioEnable,'true','bool']

            firewallParam = "%s|Medium|string" %firewallLevel

            #Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2 + list3
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
            tdkTestObj,firewallResult,details = setMultipleParameterValues(obj,firewallParam)
            if expectedresult in actualresult and expectedresult in firewallResult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set the ssid,keypassphrase,Radio enable status,firewall level")
                print("EXPECTED RESULT 2: Should set the ssid,keypassphrase,Radio enable status,firewall level");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");

                #Retrieve the values after set and compare
                newParamList=[ssidName,keyPassPhrase,radioEnable]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)
                tdkTestObj1,retStatus,newFirewallValue = getParameterValue(obj,firewallLevel)
                print("Firewall Level: %s" %newFirewallValue);
                if expectedresult in status and expectedresult in retStatus and setValuesList == newValues and newFirewallValue == "Medium":
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current ssid,keypassphrase,Radio enable status,firewall level")
                    print("EXPECTED RESULT 3: Should retrieve the current ssid,keypassphrase,Radio enable status,firewall level")
                    print("ACTUAL RESULT 3: %s %s" %(newValues,newFirewallValue));
                    print("[TEST EXECUTION RESULT] : SUCCESS");
                    #Wait for the changes to reflect in client device
                    time.sleep(60);

                    #Connect to the wifi ssid from wlan client
                    print("TEST STEP 4: From wlan client, Connect to the wifi ssid")
                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.wlan_2ghz_interface);
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS");

                        print("TEST STEP 5: Get the IP address of the wlan client and lan client after connecting to wifi")
                        wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_2ghz_interface);
                        if wlanIP:
                            tdkTestObj.setResultStatus("SUCCESS");

                            lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
                            if lanIP:
                                tdkTestObj.setResultStatus("SUCCESS");

                                print("TEST STEP 6: Get the current LAN IP address DHCP range")
                                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                                print("LAN IP Address: %s" %curIPAddress);

                                if expectedresult in status and curIPAddress:
                                    tdkTestObj.setResultStatus("SUCCESS");

                                    print("TEST STEP 7: Check whether wlan ip address and lan ip address are in same DHCP range")
                                    status = "SUCCESS"
                                    status = checkIpRange(curIPAddress,wlanIP);
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("wlan ip address is in same DHCP range")
                                        status = checkIpRange(curIPAddress,lanIP);
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("lan ip address is in same DHCP range")

                                            #add static route to wan client from wlan client
                                            status = addStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress,tdkbE2EUtility.wlan_2ghz_interface);
                                            if expectedresult in status:
                                                print("TEST STEP 8:Static route add success")
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                #Check ssh connectivity from WLAN to WAN client
                                                status = sshToClient(tdkbE2EUtility.wan_ip,tdkbE2EUtility.wan_interface,"WLAN","WAN",tdkbE2EUtility.wan_inet_address)
                                                if expectedresult in status:
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("SUCCESS: SSH connection from WLAN to WAN is success")
                                                    sshFromWlan = "SUCCESS"
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("FAILURE: SSH connection from WLAN to WAN is blocked")
                                                #delete the added route
                                                print("TEST STEP 9: Delete the static route")
                                                status = delStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress,tdkbE2EUtility.wlan_2ghz_interface);
                                                if expectedresult in status:
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("TEST STEP 10:Static route delete success")

                                                    #disconnect wifi client
                                                    print("From wlan client, Disconnect from the wifi ssid")
                                                    status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_2ghz_interface);
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print("Disconnect from WIFI SSID: SUCCESS")

                                                        #add static route to wan client from lan client
                                                        status = addStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress, tdkbE2EUtility.lan_interface, "LAN");
                                                        if expectedresult in status:
                                                            print("TEST STEP 11:Static route add success")
                                                            tdkTestObj.setResultStatus("SUCCESS");
                                                            #Check ssh connectivity from LAN to WAN client
                                                            status = sshToClient(tdkbE2EUtility.wan_ip,tdkbE2EUtility.wan_interface,"LAN","WAN",tdkbE2EUtility.wan_inet_address)
                                                            if expectedresult in status:
                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                print("SUCCESS: SSH connection from LAN to WAN is success")
                                                                sshFromLan = "SUCCESS";
                                                            else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print("FAILURE: SSH connection from LAN to WAN is blocked")

                                                            #delete the added route
                                                            print("TEST STEP 12: Delete the static route")
                                                            status = delStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress, tdkbE2EUtility.lan_interface, "LAN");
                                                            if expectedresult in status:
                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                print("TEST STEP 8:Static route delete success")
                                                            else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print("TEST STEP 8:Static route delete failed")
                                                        else:
                                                            print("TEST STEP 11:Static route add failed")
                                                            tdkTestObj.setResultStatus("FAILURE");
                                                    else:
                                                        print("Disconnect from WIFI SSID: FAILURE")
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("TEST STEP 10:Static route delete failed")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP 8:Static route add failed")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("lan ip address is not in same DHCP range")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("wlan ip address is not in same DHCP range")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("Failed to get the current LAN IP address DHCP range")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("Failed to get the LAN client ip address")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("Failed to get the WLAN client ip address")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("Failed to connect to wlan cleint")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current ssid,keypassphrase,Radio enable status,firewall level")
                    print("EXPECTED RESULT 3: Should retrieve the current ssid,keypassphrase,Radio enable status,firewall level")
                    print("ACTUAL RESULT 3: %s %s" %(newValues,newFirewallValue));
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Set the ssid,keypassphrase,Radio enable status,firewall level")
                print("EXPECTED RESULT 2: Should set the ssid,keypassphrase,Radio enable status,firewall level");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");

            #Prepare the list of parameter values to be reverted
            list1 = [ssidName,orgValue[0],'string']
            list2 = [keyPassPhrase,orgValue[1],'string']
            list3 = [radioEnable,orgValue[2],'bool']

            #Concatenate the lists with the elements separated by pipe
            revertParamList = list1 + list2 + list3
            revertParamList = "|".join(map(str, revertParamList))

            firewallParam = "%s|%s|string" %(firewallLevel,firewallValue)

            #Revert the values to original
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
            tdkTestObj,firewallResult,details = setMultipleParameterValues(obj,firewallParam)
            if expectedresult in actualresult and expectedresult in firewallResult and sshFromWlan and sshFromLan :
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 13: Should set the original ssid,keypassphrase,Radio enable status,firewall level");
                print("ACTUAL RESULT 13: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 13: Should set the original ssid,keypassphrase,Radio enable status,firewall level");
                print("ACTUAL RESULT 13: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current ssid,keypassphrase,Radio enable status,firewall level")
            print("EXPECTED RESULT 1: Should retrieve the current ssid,keypassphrase,Radio enable status,firewall level")
            print("ACTUAL RESULT 1: %s %s" %(orgValue,firewallValue));
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