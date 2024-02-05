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
  <name>E2E_XDNS_SetInvalidDnsIPV4_AccessLevel1Site</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Set Invalid DNSIPV4 address and try to access the level1 site</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Broadband</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_424</test_case_id>
    <test_objective>Set Invalid DNSIPV4 address and try to access the level1 site</test_objective>
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
and EnableXDNS status
3. Connect to the LAN client and get its MAC
4. Add a new table to Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.
5. Add new rule in this table with LAN client MAC, invalid DNS ipv4 and valid ipv6 ips and a tag name for rule
6. If the default DNS ips are empty, set dns ip values
7. Enable Device.DeviceInfo.X_RDKCENTRAL-COM_EnableXDNS
8. From LAN client do a nslookup to any level1 site via default dns server
9. Nslookup should resolve successfully
10. Revert the value of  Device.DeviceInfo.X_RDKCENTRAL-COM_EnableXDNS
11. Delete the added Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable. table
12. Unload tdkb_e2e module</automation_approch>
    <except_output>nslookup should resolve the level1 site successfully</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_XDNS_SetInvalidDnsIPV4_AccessLevel1Site</test_script>
    <skipped>No</skipped>
    <release_version>M60</release_version>
    <remarks>LAN</remarks>
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
obj1 = tdklib.TDKScriptingLibrary("tdkbtr181","RDKB");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_XDNS_SetInvalidDnsIPV4_AccessLevel1Site');
obj1.configureTestCase(ip,port,'E2E_XDNS_SetInvalidDnsIPV4_AccessLevel1Site');

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
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current enable status  and default params of XDNS")
            print("EXPECTED RESULT 1: Should retrieve the current enable status and default params of XDNS")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            #Connect to the lan client
            print("TEST STEP 2: Connect to LAN Client and get the IP address")
            lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
            if lanIP:
                tdkTestObj.setResultStatus("SUCCESS");

                print("TEST STEP 3: Get the current LAN IP address DHCP range")
                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                print("LAN IP Address: %s" %curIPAddress);

                if expectedresult in status and curIPAddress:
                    tdkTestObj.setResultStatus("SUCCESS");

                    print("TEST STEP 4: Check whether lan ip address is in same DHCP range")
                    status = "SUCCESS"
                    status = checkIpRange(curIPAddress,lanIP);
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("lan ip address is in same DHCP range")
                        lanMAC = getLanMACAddress(tdkbE2EUtility.lan_interface)
                        print("TEST STEP : Get the MAC address of lan client")
                        print("MAC retrieved is %s" %lanMAC)

                        # Adding a new row to BlockedSite
                        tdkTestObj = obj1.createTestStep("TDKB_TR181Stub_AddObject");
                        tdkTestObj.addParameter("paramName","Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.");
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        details = tdkTestObj.getResultDetails();
                        if expectedresult in actualresult:
                            #Set the result status of execution
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("TEST STEP 5: Adding new rule");
                            print("EXPECTED RESULT 5: Should add new rule");
                            print("ACTUAL RESULT 5: added new rule %s" %details);
                            print("[TEST EXECUTION RESULT] : SUCCESS");
                            temp = details.split(':');
                            instance = temp[1];

                            if (instance > 0):
                                print("INSTANCE VALUE: %s" %instance)
                                #Set values to added rule
                                macAddress = "Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s.MacAddress" %instance
                                dnsipv4 = "Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s.DnsIPv4" %instance
                                dnsipv6 = "Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s.DnsIPv6" %instance
                                tag = "Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s.Tag" %instance

                                setValuesList = [lanMAC,"A.B.C.D",tdkbE2EUtility.xdns_level1_ipv6_dns_server,"Default"];
                                print("Parameter values that are set: %s" %setValuesList)

                                list1 = [macAddress,lanMAC,'string']
                                list2 = [dnsipv4,'A.B.C.D','string']
                                list3 = [dnsipv6,tdkbE2EUtility.xdns_level1_ipv6_dns_server,'string']
                                list4 = [tag,'Default','string']

                                #Concatenate the lists with the elements separated by pipe
                                setParamList= list1 + list2 + list3 + list4
                                setParamList = "|".join(map(str, setParamList))

                                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                                if expectedresult in actualresult:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("TEST STEP 6: Set all the fields of added rule")
                                    print("EXPECTED RESULT 6: Should set all the fields of added rule");
                                    print("ACTUAL RESULT 6: %s" %details);
                                    print("[TEST EXECUTION RESULT] : SUCCESS");

                                    #Check if the default params are empty or not
                                    if '' in (orgValue[1],orgValue[2],orgValue[3]):

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
                                        setValuesList = [orgValue[1],orgValue[2],orgValue[3],'true']
                                    #Enable XDNS
                                    xdnsEnableValue="%s|true|bool" %xdnsEnable

                                    tdkTestObj,actualresult1,details = setMultipleParameterValues(obj,xdnsEnableValue)
                                    if expectedresult in  actualresult1:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("TEST STEP 7: Enable XDNS")
                                        print("EXPECTED RESULT 7: Should enable XDNS");
                                        print("ACTUAL RESULT 7: %s" %details);
                                        print("[TEST EXECUTION RESULT] : SUCCESS");

                                        #Retrieve the values after set and compare
                                        newParamList=[defaultIPV4,defaultIPV6,defaultTag,xdnsEnable]
                                        tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                                        if expectedresult in status and setValuesList == newValues:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("TEST STEP 8: Get the current xdnsEnable and default params")
                                            print("EXPECTED RESULT 8: Should retrieve the current xdnsEnable and default params")
                                            print("ACTUAL RESULT 8: %s" %newValues);
                                            print("[TEST EXECUTION RESULT] : SUCCESS");

                                            #Check if the site is accessible
                                            status = verifyNetworkConnectivity(tdkbE2EUtility.xdns_level1_site, "PING_TO_HOST", lanIP, curIPAddress,"LAN")
                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print("TEST STEP 9:Check if the level1 site accessible after setting invalid dnsipv4 address")
                                                print("EXPECTED RESULT 9:The level1 site should be accessible after setting invalid dnsipv4 address")
                                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                                finalStatus = "SUCCESS"
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP 9:Check if the level1 site accessible after setting invalid dnsipv4 address")
                                                print("EXPECTED RESULT 9:The level1 site should be accessible after setting invalid dnsipv4 address")
                                                print("[TEST EXECUTION RESULT] : FAILURE");
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP 8: Get the current xdnsEnable and default params")
                                            print("EXPECTED RESULT 8: Should retrieve the current xdnsEnable and default params")
                                            print("ACTUAL RESULT 8: %s" %newValues);
                                            print("[TEST EXECUTION RESULT] : FAILURE");
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 7: Enable XDNS")
                                        print("EXPECTED RESULT 7: Should enable XDNS");
                                        print("ACTUAL RESULT 7: %s" %details);
                                        print("[TEST EXECUTION RESULT] : FAILURE");
                                    #revert the params
                                    xdnsEnableValue="%s|%s|bool" %(xdnsEnable,orgValue[0])
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
                                    print("TEST STEP 6: Set all the fields of added rule")
                                    print("EXPECTED RESULT 6: Should set all the fields of added rule");
                                    print("ACTUAL RESULT 6: %s" %details);
                                    print("[TEST EXECUTION RESULT] : FAILURE");
                                #Delete the added rule
                                tdkTestObj = obj1.createTestStep("TDKB_TR181Stub_DelObject");
                                tdkTestObj.addParameter("paramName","Device.X_RDKCENTRAL-COM_XDNS.DNSMappingTable.%s." %instance);
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
                            print("TEST STEP 5: Adding new rule");
                            print("EXPECTED RESULT 5: Should add new rule");
                            print("ACTUAL RESULT 5: added new rule %s" %details);
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
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current enable status  and default params of XDNS")
            print("EXPECTED RESULT 1: Should retrieve the current enable status and default params of XDNS")
            print("ACTUAL RESULT 1: %s" %orgValue);
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