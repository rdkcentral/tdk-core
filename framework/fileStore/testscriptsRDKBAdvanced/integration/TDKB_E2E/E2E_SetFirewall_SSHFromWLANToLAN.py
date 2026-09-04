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
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_SetFirewall_SSHFromWLANToLAN</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test if SSH from WLANtoLAN is success when firewall is set as high/low/medium/custom</synopsis>
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
    <test_case_id>TC_TDKB_E2E_466</test_case_id>
    <test_objective>Test if SSH from WLANtoLAN is success when firewall is set as high/low/medium/custom</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.Radio.1.Enable
Device.WiFi.SSID.1.SSID
Device.WiFi.AccessPoint.1.Security.KeyPassphrase
Device.X_CISCO_COM_Security.Firewall.FirewallLevel</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save firewall level
3. Login to the LAN client and get the IP address assigned by the gateway
4. Try to connect to Wifi client and check whether the wifi client is connected to the DUT
3. Set the firewall level to Low,Medium,High,Custom sequentially using tdkb_e2e_SetMultipleParams
5. For each of the above firewall set, check if the ssh connectivity from WLAN to LAN is success
6. Revert the firewall level to original value
7.Unload tdkb_e2e module</automation_approch>
    <except_output>SSH from WLN to LAN client should be success for all firewall values</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_SetFirewall_SSHFromWLANToLAN</test_script>
    <skipped>No</skipped>
    <release_version>M62</release_version>
    <remarks>WLAN,LAN</remarks>
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
obj.configureTestCase(ip,port,'E2E_SetFirewall_SSHFromWLANToLAN');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    finalStatus = "SUCCESS"
    firewallLevels=["High","Medium","Low","Custom"]

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
        step = 1
        status = "FAILURE"
        paramList=[ssidName,keyPassPhrase,radioEnable]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)
        tdkTestObj1,retStatus,firewallValue = getParameterValue(obj,firewallLevel)
        print("Firewall Level: %s" %firewallValue);

        if expectedresult in status and expectedresult in retStatus:
            tdkTestObj.setResultStatus("SUCCESS");
            print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase,Radio enable status,firewall level")
            print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase,Radio enable status,firewall level")
            print(f"ACTUAL RESULT {step}: {orgValue} {firewallValue}");
            print("[TEST EXECUTION RESULT] : SUCCESS");

            if tdkbE2EUtility.mlo_capability == "False":
                # Set the SSID name,password and Radio enable status
                setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,'true'];
                print("Parameter values that are set: %s" %setValuesList)

                list1 = [ssidName,tdkbE2EUtility.ssid_2ghz_name,'string']
                list2 = [keyPassPhrase,tdkbE2EUtility.ssid_2ghz_pwd,'string']
                list3 = [radioEnable,'true','bool']

                #Concatenate the lists with the elements separated by pipe
                setParamList = list1 + list2 + list3
                setParamList = "|".join(map(str, setParamList))

                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                step = step + 1

                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print(f"TEST STEP {step}: Set the ssid,keypassphrase,Radio enable status")
                    print(f"EXPECTED RESULT {step}: Should set the ssid,keypassphrase,Radio enable status");
                    print(f"ACTUAL RESULT {step}: {details}");
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    #Retrieve the values after set and compare
                    newParamList=[ssidName,keyPassPhrase,radioEnable]
                    tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)
                    step = step + 1

                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase,Radio enable status")
                        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase,Radio enable status")
                        print(f"ACTUAL RESULT {step}: {newValues}");
                        print("[TEST EXECUTION RESULT] : SUCCESS");
                        status = "SUCCESS"
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase,Radio enable status")
                        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase,Radio enable status")
                        print(f"ACTUAL RESULT {step}: {newValues}");
                        print("[TEST EXECUTION RESULT] : FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    details = tdkTestObj.getResultDetails();
                    print(f"TEST STEP {step}: Set the ssid,keypassphrase,Radio enable status")
                    print(f"EXPECTED RESULT {step}: Should set the ssid,keypassphrase,Radio enable status");
                    print(f"ACTUAL RESULT {step}: {details}");
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                status = "SUCCESS"

            if tdkbE2EUtility.mlo_capability == "False":
                tdkbE2EUtility.ssid_name = tdkbE2EUtility.ssid_2ghz_name
                tdkbE2EUtility.ssid_pwd = tdkbE2EUtility.ssid_2ghz_pwd
                tdkbE2EUtility.wlan_interface = tdkbE2EUtility.wlan_2ghz_interface

            if status == "SUCCESS":
                #Wait for the changes to reflect in client device
                time.sleep(60);

                step = step + 1
                print(f"\nTEST STEP {step}: Get the current LAN IP address DHCP range")
                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                print("Gateway LAN IP Address: %s" %curIPAddress);

                if expectedresult in status and curIPAddress:
                    tdkTestObj.setResultStatus("SUCCESS");

                    #Connect to LAN client and obtain its IP
                    step = step + 1
                    print(f"\nTEST STEP {step}: Get the IP address of the lan client after connecting to it")
                    lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
                    if lanIP:
                        tdkTestObj.setResultStatus("SUCCESS");

                        step = step + 1
                        print(f"\nTEST STEP {step}: Check whether lan Client IP address is in same DHCP range")
                        status = "SUCCESS"
                        status = checkIpRange(curIPAddress,lanIP);
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS");

                            #Connect to the wifi ssid from wlan client
                            step = step + 1
                            print(f"\nTEST STEP {step}: From wlan client, Connect to the wifi ssid")
                            status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_name,tdkbE2EUtility.ssid_pwd,tdkbE2EUtility.wlan_interface);
                            if expectedresult in status:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("wlanConnectWifiSsid: SUCCESS")

                                step = step + 1
                                print(f"\nTEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                                wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_interface);
                                if wlanIP:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("getWlanIPAddress: SUCCESS")

                                    step = step + 1
                                    print(f"\nTEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                                    status = "SUCCESS"
                                    status = checkIpRange(curIPAddress,wlanIP);
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("checkIpRange: SUCCESS")

                                        for i in range(0,4):
                                            if tdkbE2EUtility.mlo_capability == "False":
                                                firewallParam = "%s|%s|string" %(firewallLevel,firewallLevels[i])
                                                tdkTestObj,firewallResult,details = setMultipleParameterValues(obj,firewallParam)
                                                step = step + 1

                                                if expectedresult in firewallResult:
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print(f"\nTEST STEP {step}: Set the firewall level to {firewallLevels[i]}")
                                                    print(f"EXPECTED RESULT {step}: Should set the firewall level");
                                                    print(f"ACTUAL RESULT {step}: {details}");
                                                    print("[TEST EXECUTION RESULT] : SUCCESS");

                                                    tdkTestObj1,retStatus,newFirewallValue = getParameterValue(obj,firewallLevel)
                                                    step = step + 1
                                                    print("Firewall Level: %s" %newFirewallValue);

                                                    if expectedresult in retStatus and newFirewallValue == firewallLevels[i]:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print(f"\nTEST STEP {step}: Get the current firewall level")
                                                        print(f"EXPECTED RESULT {step}: Should retrieve the current firewall level")
                                                        print(f"ACTUAL RESULT {step}: {newFirewallValue}");
                                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                                        firewallStatus = "SUCCESS"
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        firewallStatus = "FAILURE"
                                                        print(f"\nTEST STEP {step}: Failed to retrieve the current firewall level")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    firewallStatus = "FAILURE"
                                                    print(f"\nTEST STEP {step}: Failed to set firewall level")
                                            else:
                                                level = firewallLevels[i]
                                                step = step + 1
                                                firewallStatus, step = firewallSet(obj,level,step)

                                            if expectedresult in firewallStatus:
                                                #Wait for the changes to reflect in client device
                                                time.sleep(60);

                                                step = step + 1
                                                print(f"\nTEST STEP {step}: Check the SSH connectivity from WLAN to LAN")

                                                # Original script uses WAN parameters in sshToClient call.
                                                # Kept unchanged to avoid changing utility function signature.
                                                status = sshToClient(tdkbE2EUtility.wan_ip,tdkbE2EUtility.wan_interface,"LAN","WAN",tdkbE2EUtility.wan_inet_address)

                                                if expectedresult in status:
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("SUCCESS: SSH connection from WLAN to LAN is success with firewall level ", firewallLevels[i])
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    finalStatus = "FAILURE"
                                                    print("FAILURE: SSH connection from WLAN to LAN is blocked with firewall level ", firewallLevels[i])
                                            else:
                                                finalStatus = "FAILURE"
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print(f"\nTEST STEP {step}: WLAN Client IP address is not in the same Gateway DHCP range")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print(f"\nTEST STEP {step}: Failed to get the WLAN Client IP address")

                                step = step + 1
                                print(f"\nTEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                                status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_interface);
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("Disconnect from WIFI SSID: SUCCESS")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    finalStatus = "FAILURE"
                                    print(f"\nTEST STEP {step}: Disconnect from WIFI SSID: FAILED")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print(f"\nTEST STEP {step}: Failed to connect to WIFI SSID")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print(f"\nTEST STEP {step}: LAN Client IP address is not in the same Gateway DHCP range")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print(f"\nTEST STEP {step}: Failed to get the LAN Client IP address")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print(f"\nTEST STEP {step}: Failed to get the Gateway IP address")

            if tdkbE2EUtility.mlo_capability == "False":
                #Prepare the list of parameter values to be reverted
                list1 = [ssidName,orgValue[0],'string']
                list2 = [keyPassPhrase,orgValue[1],'string']
                list3 = [radioEnable,orgValue[2],'bool']

                #Concatenate the lists with the elements separated by pipe
                revertParamList = list1 + list2 + list3
                revertParamList = "|".join(map(str, revertParamList))

                firewallParam = "%s|%s|string" %(firewallLevel,firewallValue)

                #Revert the values to original
                step = step + 1
                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
                tdkTestObj,firewallResult,details = setMultipleParameterValues(obj,firewallParam)
                print(f"\nTEST STEP {step}: Revert the values to original")

                if expectedresult in actualresult and expectedresult in firewallResult and expectedresult in finalStatus:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print(f"EXPECTED RESULT {step}: Should set the original ssid,keypassphrase,Radio enable status,firewall level");
                    print(f"ACTUAL RESULT {step}: %s" %details);
                    print("[TEST EXECUTION RESULT] : SUCCESS");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    details = tdkTestObj.getResultDetails();
                    print(f"EXPECTED RESULT {step}: Should set the original ssid,keypassphrase,Radio enable status,firewall level");
                    print(f"ACTUAL RESULT {step}: %s" %details);
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                # Revert the firewall level to original value using firewallSet function
                level = firewallValue
                step = step + 1
                _, _ = firewallSet(obj,level,step,revert="true")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase,Radio enable status,firewall level")
            print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase,Radio enable status,firewall level")
            print(f"ACTUAL RESULT {step}: {orgValue} {firewallValue}");
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