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
  <name>E2E_XDNS_DualMask_MultipleClients_Level1</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Set multiple xdns rules for different client MacAddress. From clients check if the corresponding level sites are blocked or not</synopsis>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_504</test_case_id>
    <test_objective>Set multiple xdns rules for different client MacAddress. From clients check if the corresponding level sites are blocked or not</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway
Ensure that xdns process is running in gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.DeviceInfo.X_RDKCENTRAL-COM_EnableXDNS
Device.X_RDKCENTRAL-COM_XDNS.DefaultDeviceDnsIPv4
Device.X_RDKCENTRAL-COM_XDNS.DefaultDeviceDnsIPv6
Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Get and save the default DNS IP values of XDNS
3. If the default DNS ips are empty, set dns ip values
4. Enable Device.DeviceInfo.X_RDKCENTRAL-COM_EnableXDNS
and EnableXDNS status
5. Connect to the WLAN client and get its MAC
6. Connect to the LAN client and get its MAC
7. Add a new table to Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable. for WLAN client
8. Add a new table to Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable. for LAN client
9. Add new rule in first table with WLAN client MAC, level 1 DNS ipv4 and ipv6 secondary dns ips and a tag name for rule
10. Add new rule in second table with LAN client MAC, level 1 DNS ipv4 and ipv6 secondary dns ips and a tag name for rule
11. From WLAN client do a ping to any level1 site
12. From LAN client do a ping to any level1 site
13. Ping should fail as XDNS blocks the DNS resolution of level1 site
14. Revert the value of  Device.DeviceInfo.X_RDKCENTRAL-COM_EnableXDNS
15. Delete the added Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable. tables
16. Unload tdkb_e2e module</automation_approch>
    <except_output>XDNS feature should work as expected for multiple clients also</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_XDNS_DualMask_MultipleClients_Level1</test_script>
    <skipped>No</skipped>
    <release_version>M66</release_version>
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
obj1 = tdklib.TDKScriptingLibrary("tdkbtr181","RDKB");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_XDNS_DualMask_MultipleClients_Level1');
obj1.configureTestCase(ip,port,'E2E_XDNS_DualMask_MultipleClients_Level1');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 =obj1.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper() :
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

        #Assign the  parameters names to a variable
        defaultIPV4 = "Device.X_RDKCENTRAL-COM_XDNS.DefaultDeviceDnsIPv4"
        defaultIPV6 = "Device.X_RDKCENTRAL-COM_XDNS.DefaultDeviceDnsIPv6"
        defaultTag = "Device.X_RDKCENTRAL-COM_XDNS.DefaultDeviceTag"
        xdnsEnable = "Device.DeviceInfo.X_RDKCENTRAL-COM_EnableXDNS"

        #Get the value of the wifi parameters that are currently set.
        paramList=[xdnsEnable,defaultIPV4,defaultIPV6,defaultTag]
        tdkTestObj,status,orgDnsValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current enable status  and default params of XDNS")
            print("EXPECTED RESULT 1: Should retrieve the current enable status and default params of XDNS")
            print("ACTUAL RESULT 1: %s" %orgDnsValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            #Assign the WIFI parameters names to a variable
            ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
            keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
            securityMode = "Device.WiFi.AccessPoint.%s.Security.ModeEnabled" %tdkbE2EUtility.ssid_2ghz_index
            radioEnable = "Device.WiFi.Radio.%s.Enable" %tdkbE2EUtility.radio_2ghz_index
            ssidEnable = "Device.WiFi.SSID.%s.Enable" %tdkbE2EUtility.ssid_2ghz_index

            #Get the value of the wifi parameters that are currently set.
            paramList=[ssidName,keyPassPhrase,securityMode,radioEnable,ssidEnable]
            tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

            if expectedresult in status:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Get the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                print("EXPECTED RESULT 2: Should retrieve the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                print("ACTUAL RESULT 2: %s" %orgValue);
                print("[TEST EXECUTION RESULT] : SUCCESS");

                # Set securityMode,radioEnable and ssidEnable for 2.4ghz"
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
                    print("TEST STEP 3: Set the ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                    print("EXPECTED RESULT 3: Should set the ssid,keypassphrase,securityMode,radioEnable and ssidEnable");
                    print("ACTUAL RESULT 3: %s" %details);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    #Retrieve the values after set and compare
                    newParamList=[ssidName,keyPassPhrase,securityMode,radioEnable,ssidEnable]
                    time.sleep(60);
                    tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TEST STEP 4: Get the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                        print("EXPECTED RESULT 4: Should retrieve the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                        print("ACTUAL RESULT 4: %s" %newValues);
                        print("[TEST EXECUTION RESULT] : SUCCESS");

                        #Connect to the wifi ssid from wlan client
                        print("TEST STEP 5: From wlan client, Connect to the wifi ssid")
                        status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.wlan_2ghz_interface);
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS");

                            print("TEST STEP 6: Get the IP address of the wlan client after connecting to wifi")
                            wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_2ghz_interface);
                            if wlanIP:
                                tdkTestObj.setResultStatus("SUCCESS");

                                print("TEST STEP 7: Get the current LAN IP address DHCP range")
                                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                                print("LAN IP Address: %s" %curIPAddress);

                                if expectedresult in status and curIPAddress:
                                    tdkTestObj.setResultStatus("SUCCESS");

                                    print("TEST STEP 8: Check whether wlan ip address is in same DHCP range")
                                    status = "SUCCESS"
                                    status = checkIpRange(curIPAddress,wlanIP);
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        wlanMAC = getWlanMACAddress(tdkbE2EUtility.wlan_2ghz_interface)
                                        print("TEST STEP : Get the MAC address of wlan client")
                                        print("MAC retrieved is %s" %wlanMAC)

                                        #Connect to the lan client
                                        print("TEST STEP 9: Connect to LAN Client and get the IP address")
                                        lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
                                        if lanIP:
                                            tdkTestObj.setResultStatus("SUCCESS");

                                            print("TEST STEP 10: Get the current LAN IP address DHCP range")
                                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                            tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                                            print("LAN IP Address: %s" %curIPAddress);

                                            if expectedresult in status and curIPAddress:
                                                tdkTestObj.setResultStatus("SUCCESS");

                                                print("TEST STEP 11: Check whether lan ip address is in same DHCP range")
                                                status = "SUCCESS"
                                                status = checkIpRange(curIPAddress,lanIP);
                                                if expectedresult in status:
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("lan ip address is in same DHCP range")
                                                    lanMAC = getLanMACAddress(tdkbE2EUtility.lan_interface)
                                                    print("TEST STEP : Get the MAC address of lan client")
                                                    print("MAC retrieved is %s" %lanMAC)

                                                    #Check if the default params are empty or not
                                                    if '' in (orgDnsValue[1],orgDnsValue[2],orgDnsValue[3]):

                                                        #Set default values
                                                        setValuesList = [tdkbE2EUtility.xdns_dns_server,tdkbE2EUtility.xdns_ipv6_dns_server,'empty','true'];
                                                        print("WIFI parameter values that are set: %s" %setValuesList)

                                                        list1 = [defaultIPV4,tdkbE2EUtility.xdns_dns_server,'string']
                                                        list2 = [defaultIPV6,tdkbE2EUtility.xdns_ipv6_dns_server,'string']
                                                        list3 = [defaultTag,'empty','string']

                                                        #Concatenate the lists with the elements separated by pipe
                                                        setParamList = list1 + list2 + list3
                                                        setParamList = "|".join(map(str, setParamList))
                                                        tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                                                        setValuesList = [tdkbE2EUtility.xdns_dns_server, tdkbE2EUtility.xdns_ipv6_dns_server, 'empty', 'true']
                                                    else:
                                                        print("Default values are already set")
                                                        setValuesList = [orgDnsValue[1],orgDnsValue[2],orgDnsValue[3],'true']
                                                    #Enable XDNS
                                                    xdnsEnableValue="%s|true|bool" %xdnsEnable

                                                    tdkTestObj,actualresult1,details = setMultipleParameterValues(obj,xdnsEnableValue)
                                                    if expectedresult in actualresult1:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print("TEST STEP 12: Enable XDNS")
                                                        print("EXPECTED RESULT 12: Should enable XDNS");
                                                        print("ACTUAL RESULT 12: %s" %details);
                                                        print("[TEST EXECUTION RESULT] : SUCCESS");

                                                        #Retrieve the values after set and compare
                                                        newParamList=[defaultIPV4,defaultIPV6,defaultTag,xdnsEnable]
                                                        tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                                                        if expectedresult in status and setValuesList == newValues:
                                                            tdkTestObj.setResultStatus("SUCCESS");
                                                            print("TEST STEP 13: Get the current xdnsEnable and default params")
                                                            print("EXPECTED RESULT 13: Should retrieve the current xdnsEnable and default params")
                                                            print("ACTUAL RESULT 13: %s" %newValues);
                                                            print("[TEST EXECUTION RESULT] : SUCCESS");

                                                            # Adding a new row to BlockedSite
                                                            tdkTestObj = obj1.createTestStep("TDKB_TR181Stub_AddObject");
                                                            tdkTestObj.addParameter("paramName","Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.");
                                                            tdkTestObj.executeTestCase(expectedresult);
                                                            actualresult = tdkTestObj.getResult();
                                                            details = tdkTestObj.getResultDetails();
                                                            if expectedresult in actualresult:
                                                                #Set the result status of execution
                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                print("TEST STEP 14: Adding new rule for wlan client");
                                                                print("EXPECTED RESULT 14: Should add new rule");
                                                                print("ACTUAL RESULT 14: added new rule %s" %details);
                                                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                                                temp = details.split(':');
                                                                instance1 = temp[1];

                                                                if (instance1 > 0):
                                                                    print("INSTANCE VALUE: %s" %instance1)

                                                                    tdkTestObj.executeTestCase(expectedresult);
                                                                    actualresult = tdkTestObj.getResult();
                                                                    details = tdkTestObj.getResultDetails();
                                                                    if expectedresult in actualresult:
                                                                        #Set the result status of execution
                                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                                        print("TEST STEP 15: Adding new rule for lan client");
                                                                        print("EXPECTED RESULT 15: Should add new rule");
                                                                        print("ACTUAL RESULT 15: added new rule %s" %details);
                                                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                                                        temp = details.split(':');
                                                                        instance2 = temp[1];

                                                                        if (instance2 > 0):
                                                                            print("INSTANCE VALUE: %s" %instance2)
                                                                            #Set values to added rule
                                                                            macAddress1 = "Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s.MacAddress" %instance1
                                                                            dnsipv4_1 = "Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s.DnsIPv4" %instance1
                                                                            dnsipv6_1 = "Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s.DnsIPv6" %instance1
                                                                            tag1 = "Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s.Tag" %instance1
                                                                            macAddress2 = "Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s.MacAddress" %instance2
                                                                            dnsipv4_2 = "Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s.DnsIPv4" %instance2
                                                                            dnsipv6_2 = "Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s.DnsIPv6" %instance2
                                                                            tag2 = "Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s.Tag" %instance2

                                                                            setValuesList = [wlanMAC,tdkbE2EUtility.xdns_level1_secondary_dns_server,tdkbE2EUtility.xdns_level1_ipv6_secondary_dns_server,"Default",lanMAC,tdkbE2EUtility.xdns_level1_secondary_dns_server,tdkbE2EUtility.xdns_level1_ipv6_secondary_dns_server,"Default"];
                                                                            print("Parameter values that are set: %s" %setValuesList)

                                                                            list1 = [macAddress1,wlanMAC,'string']
                                                                            list2 = [dnsipv4_1,tdkbE2EUtility.xdns_level1_secondary_dns_server,'string']
                                                                            list3 = [dnsipv6_1,tdkbE2EUtility.xdns_level1_ipv6_secondary_dns_server,'string']
                                                                            list4 = [tag1,'Default','string']
                                                                            list5 = [macAddress2,lanMAC,'string']
                                                                            list6 = [dnsipv4_2,tdkbE2EUtility.xdns_level1_secondary_dns_server,'string']
                                                                            list7 = [dnsipv6_2,tdkbE2EUtility.xdns_level1_ipv6_secondary_dns_server,'string']
                                                                            list8 = [tag2,'Default','string']

                                                                            #Concatenate the lists with the elements separated by pipe
                                                                            setParamList= list1 + list2 + list3 + list4 + list5 + list6 + list7 + list8
                                                                            setParamList = "|".join(map(str, setParamList))

                                                                            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                                                                            if expectedresult in actualresult:
                                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                                print("TEST STEP 16: Set all the fields of added rule")
                                                                                print("EXPECTED RESULT 16: Should set all the fields of added rule");
                                                                                print("ACTUAL RESULT 16: %s" %details);
                                                                                print("[TEST EXECUTION RESULT] : SUCCESS");

                                                                                #Check if the Level1 site is accessible
                                                                                status1 = verifyNetworkConnectivity(tdkbE2EUtility.xdns_level1_site, "PING_TO_HOST", wlanIP, curIPAddress)
                                                                                status2 = verifyNetworkConnectivity(tdkbE2EUtility.xdns_level1_site, "PING_TO_HOST", lanIP, curIPAddress,"LAN")

                                                                                if expectedresult not in status1 and expectedresult not in status2:
                                                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                                                    print("TEST STEP 17:Check if the level1 site is blocked from both client device")
                                                                                    print("EXPECTED RESULT 17:The level1 site should not be accessible from both the blocked devices")
                                                                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                                                                    finalStatus = "SUCCESS"
                                                                                else:
                                                                                    tdkTestObj.setResultStatus("FAILURE");
                                                                                    print("TEST STEP 17:Check if the level1 site is blocked from both client device")
                                                                                    print("EXPECTED RESULT 17:The level1 site should not be accessible from both the blocked devices")
                                                                                    print("[TEST EXECUTION RESULT] : FAILURE");
                                                                                    print("WLAN connectivity status: %s, LAN connectivity status: %s" %(status1,status2))
                                                                            else:
                                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                                print("TEST STEP 16: Set all the fields of added rule")
                                                                                print("EXPECTED RESULT 16: Should set all the fields of added rule");
                                                                                print("ACTUAL RESULT 16: %s" %details);
                                                                                print("[TEST EXECUTION RESULT] : FAILURE");

                                                                            #Delete the added rule
                                                                            tdkTestObj = obj1.createTestStep("TDKB_TR181Stub_DelObject");
                                                                            tdkTestObj.addParameter("paramName","Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s." %instance2);
                                                                            expectedresult = "SUCCESS";
                                                                            tdkTestObj.executeTestCase(expectedresult);
                                                                            actualresult = tdkTestObj.getResult();
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
                                                                            print("TEST STEP 15: Adding new rule");
                                                                            print("EXPECTED RESULT 15: Should add new rule");
                                                                            print("ACTUAL RESULT 15: added new rule %s" %details);
                                                                            print("[TEST EXECUTION RESULT] : FAILURE");
                                                                    #Delete the added rule
                                                                    tdkTestObj = obj1.createTestStep("TDKB_TR181Stub_DelObject");
                                                                    tdkTestObj.addParameter("paramName","Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s." %instance1);
                                                                    expectedresult = "SUCCESS";
                                                                    tdkTestObj.executeTestCase(expectedresult);
                                                                    actualresult = tdkTestObj.getResult();
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
                                                                    print("TEST STEP 14: Adding new rule");
                                                                    print("EXPECTED RESULT 14: Should add new rule");
                                                                    print("ACTUAL RESULT 14: added new rule %s" %details);
                                                                    print("[TEST EXECUTION RESULT] : FAILURE");
                                                        else:
                                                            tdkTestObj.setResultStatus("FAILURE");
                                                            print("TEST STEP 13: Get the current xdnsEnable and default params")
                                                            print("EXPECTED RESULT 13: Should retrieve the current xdnsEnable and default params")
                                                            print("ACTUAL RESULT 13: %s" %newValues);
                                                            print("[TEST EXECUTION RESULT] : FAILURE");
                                                        #revert the params
                                                        xdnsEnableValue="%s|%s|bool" %(xdnsEnable,orgDnsValue[0])
                                                        tdkTestObj,actualresult,details = setMultipleParameterValues(obj,xdnsEnableValue)
                                                        if expectedresult in actualresult and expectedresult in finalStatus:
                                                            tdkTestObj.setResultStatus("SUCCESS");
                                                            print("EXPECTED RESULT : Should revert the xdns enable status");
                                                            print("ACTUAL RESULT : %s" %details);
                                                            print("[TEST EXECUTION RESULT] : SUCCESS");
                                                        else:
                                                            tdkTestObj.setResultStatus("FAILURE");
                                                            details = tdkTestObj.getResultDetails();
                                                            print("EXPECTED RESULT : Should revert the xdns enable status");
                                                            print("ACTUAL RESULT : %s" %details);
                                                            print("[TEST EXECUTION RESULT] : FAILURE");
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("TEST STEP 12: Enable XDNS")
                                                        print("EXPECTED RESULT 12: Should enable XDNS");
                                                        print("ACTUAL RESULT 12: %s" %details);
                                                        print("[TEST EXECUTION RESULT] : FAILURE");
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("lan ip address is not in same DHCP range")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("Failed to get the current LAN IP address DHCP range")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("Failed to get the LAN client IP address")
                                        print("TEST STEP : Disconnect wlan client from the wifi ssid")
                                        status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_2ghz_interface);
                                        print("TEST STEP : Disconnect the WiFi connection")
                                        if expectedresult in status:
                                            print("TEST STEP : Connection successfully disconnected")
                                            tdkTestObj.setResultStatus("SUCCESS");
                                        else:
                                            print("TEST STEP : Failed to Disconnect")
                                            tdkTestObj.setResultStatus("FAILURE");
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 8: FAILURE, wlan ip address is not in the same DHCP range")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 7: Failed to get the current WLAN IP address DHCP range")

                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 6: Failed to get the IP address of the wlan client")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("TEST STEP 5: Failed to connect from wlan client, to the wifi ssid using valid wifi password")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 4: Get the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                        print("EXPECTED RESULT 4: Should retrieve the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                        print("ACTUAL RESULT 4: %s" %newValues);
                        print("[TEST EXECUTION RESULT] : FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Set the ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                    print("EXPECTED RESULT 3: Should set the ssid,keypassphrase,securityMode,radioEnable and ssidEnable");
                    print("ACTUAL RESULT 3: %s" %details);
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
                    print("EXPECTED RESULT 18: Should set the original ssid,keypassphrase,securityMode,radioEnable and ssidEnable");
                    print("ACTUAL RESULT 18: %s" %details);
                    print("[TEST EXECUTION RESULT] : SUCCESS");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    details = tdkTestObj.getResultDetails();
                    print("EXPECTED RESULT 18: Should set the original ssid,keypassphrase,securityMode,radioEnable and ssidEnable");
                    print("ACTUAL RESULT 18: %s" %details);
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Get the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                print("EXPECTED RESULT 2: Should retrieve the current ssid,keypassphrase,securityMode,radioEnable and ssidEnable")
                print("ACTUAL RESULT 2: %s" %orgValue);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current enable status  and default params of XDNS")
            print("EXPECTED RESULT 1: Should retrieve the current enable status and default params of XDNS")
            print("ACTUAL RESULT 1: %s" %orgDnsValue);
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        obj.setLoadModuleStatus("FAILURE");
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup();
    obj.unloadModule("tdkb_e2e");
    obj1.unloadModule("tdkbtr181");

else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");