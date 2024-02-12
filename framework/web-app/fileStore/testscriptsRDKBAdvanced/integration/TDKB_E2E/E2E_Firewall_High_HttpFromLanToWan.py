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
  <name>E2E_Firewall_High_HttpFromLanToWan</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_SetMultipleParams</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Verify that when Firewall Config is set to High HTTP access from LAN to WAN should not be blocked</synopsis>
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
    <test_case_id>TC_TDKB_E2E_285</test_case_id>
    <test_objective>Verify that when Firewall Config is set to High HTTP access from LAN to WAN should not be blocked</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>tdkb_e2e_Set</api_or_interface_used>
    <input_parameters>Device.WiFi.Radio.1.Enable
Device.WiFi.SSID.1.SSID
Device.WiFi.AccessPoint.1.Security.KeyPassphrase
Device.X_CISCO_COM_Security.Firewall.FirewallLevel</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save firewall level
3. Set the firewall level to High using tdkb_e2e_SetMultipleParams
4.  Check whether LAN client is connected to GW and it is assigned a valid ip by the GW
5. From the lan client, do HTTP to the WAN client and check whether http is success when the firewall level is set to High
6. Revert the firewall level to original value
7.Unload tdkb_e2e module</automation_approch>
    <except_output>HTTP from LAN to WAN should be success</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_Firewall_High_HttpFromLanToWan</test_script>
    <skipped>No</skipped>
    <release_version>M54</release_version>
    <remarks>LAN,WAN</remarks>
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
obj.configureTestCase(ip,port,'E2E_Firewall_High_HttpFromLanToWan');

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
        firewallLevel = "Device.X_CISCO_COM_Security.Firewall.FirewallLevel"

        #Get the value of the wifi parameters that are currently set.
        tdkTestObj,retStatus,firewallValue = getParameterValue(obj,firewallLevel)
        print("Firewall Level: %s" %firewallValue);

        if expectedresult in retStatus:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current firewall level")
            print("EXPECTED RESULT 1: Should retrieve the current firewall level")
            print("ACTUAL RESULT 1: %s" %firewallValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            # Set firewall level"

            firewallParam = "%s|High|string" %firewallLevel

            tdkTestObj,firewallResult,details = setMultipleParameterValues(obj,firewallParam)
            if expectedresult in firewallResult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set the firewall level")
                print("EXPECTED RESULT 2: Should set the firewall level");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");

                #Retrieve the values after set and compare
                tdkTestObj,retStatus,newFirewallValue = getParameterValue(obj,firewallLevel)
                print("Firewall Level: %s" %newFirewallValue);

                if expectedresult in retStatus and newFirewallValue == "High":
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current firewall level")
                    print("EXPECTED RESULT 3: Should retrieve the current firewall level")
                    print("ACTUAL RESULT 3: %s " %newFirewallValue);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    #Wait for the changes to reflect in client device
                    time.sleep(60);

                    lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
                    if lanIP:
                        tdkTestObj.setResultStatus("SUCCESS");

                        print("TEST STEP 6: Get the current LAN IP address DHCP range")
                        param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                        tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                        print("LAN IP Address: %s" %curIPAddress);

                        if expectedresult in status and curIPAddress:
                            tdkTestObj.setResultStatus("SUCCESS");

                            print("TEST STEP 7: Check whether wlan ip address is in same DHCP range")
                            status = "SUCCESS"
                            status = checkIpRange(curIPAddress,lanIP);
                            if expectedresult in status:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("wlan ip address is in same DHCP range")

                                #set new static route to wan client
                                status = addStaticRoute(tdkbE2EUtility.wan_http_ip, curIPAddress, tdkbE2EUtility.lan_interface, "LAN");
                                #status = addStaticRoute(lanIP, tdkbE2EUtility.lan_interface);
                                if expectedresult in status:
                                    print("TEST STEP 8:Static route add success")

                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("TEST STEP 10:Check the HTTP from LAN to WAN")
                                    status = wgetToWAN("WGET_HTTP", lanIP, curIPAddress, "LAN")

                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("SUCCESS: HTTP from LAN to WAN is success")

                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 10: failed, HTTP from LAN to WAN is blocked")

                                    #delete the added route
                                    print("TEST STEP 12: Delete the static route")
                                    status = delStaticRoute(tdkbE2EUtility.wan_http_ip, curIPAddress, tdkbE2EUtility.lan_interface, "LAN");
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        finalStatus = "SUCCESS";
                                        print("TEST STEP 8:Static route delete success")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 8:Static route delete failed")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 8:Static route add failed")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 9:WLAN Client IP address is not in the same Gateway DHCP range")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("TEST STEP 8:Failed to get the WLAN Client IP address")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 4:Failed to get the Gateway IP address")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current firewall level")
                    print("EXPECTED RESULT 3: Should retrieve the current firewall level")
                    print("ACTUAL RESULT 3:  %s" %newFirewallValue);
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("TEST STEP 2: Set the firewall level")
                print("EXPECTED RESULT 2: Should set the firewall level");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");

            #Prepare the list of parameter values to be reverted
            firewallParam = "%s|%s|string" %(firewallLevel,firewallValue)

            #Revert the values to original
            tdkTestObj,firewallResult,details = setMultipleParameterValues(obj,firewallParam)
            if  expectedresult in firewallResult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 12: Should set the original firewall level");
                print("ACTUAL RESULT 12: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 12: Should set the original firewall level");
                print("ACTUAL RESULT 12: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current firewall level")
            print("EXPECTED RESULT 1: Should retrieve the current firewall level")
            print("ACTUAL RESULT 1: %s " %firewallValue);
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