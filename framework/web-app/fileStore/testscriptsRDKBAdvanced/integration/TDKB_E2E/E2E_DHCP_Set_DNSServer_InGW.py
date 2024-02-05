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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_DHCP_Set_DNSServer_InGW</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_SetMultipleParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify that DNS server details can be updated with a valid global DNS server in WG (ex.4.4.4.4). Ensure that Client receives Comcast DNS server configuration</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>30</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
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
    <test_case_id>TC_TDKB_E2E_280</test_case_id>
    <test_objective>Verify that DNS server details can be updated with a valid global DNS server in WG (ex.4.4.4.4). Ensure that Client receives Comcast DNS server configuration</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress
Device.DNS.Client.Server.1.DNSServer</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save DNSServer and lanip of GW
3. Change the DNS server in GW as 4.4.4.4
4. Connect the lan client and check if its assigned  valid IP by the GW
5. Get the DNS server names from the lan client
6. Check if the DNS server names from the LAN client and GW are the same or not
7. Revert the DNS server in GW
6.Unload tdkb_e2e module</automation_approch>
    <except_output>Change in DNS server in GW should be reflected in client</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_DHCP_Set_DNSServer_InGW</test_script>
    <skipped>No</skipped>
    <release_version>M57</release_version>
    <remarks>LAN</remarks>
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
obj.configureTestCase(ip,port,'E2E_DHCP_Set_DNSServer_InGW');

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

        dnsServer="Device.DHCPv4.Server.Pool.1.DNSServers"
        lanIPAddress = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
        #Get the value of the wifi parameters that are currently set.
        paramList=[dnsServer, lanIPAddress]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current dnsServer and lanIPAddress in GW")
            print("EXPECTED RESULT 1: Should retrieve the current dnsServer and lanIPAddress in GW")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            #set the DNS server in GW
            setValuesList = ['4.4.4.4']
            print("Parameter value that is set: %s" %setValuesList)

            setParamList = [dnsServer,'4.4.4.4','string']
            setParamList = "|".join(map(str, setParamList))
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)

            if expectedresult in actualresult :
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set the DNS server in GW")
                print("EXPECTED RESULT 2: Should set the DNS server in GW");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");

                #Retrieve the values after set and compare
                newParamList=[dnsServer]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current DNS server in GW")
                    print("EXPECTED RESULT 3: Should retrieve the current DNS server in GW")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    #Wait for the changes to reflect in client device
                    time.sleep(60);

                    #Connect to Lan Client and get the IP address
                    print("TEST STEP 4:Connect to LAN Client and get the IP address after network refresh")
                    lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);

                    if lanIP:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("getlanIPAddress: SUCCESS")

                        print("TEST STEP 5: Check whether lan ip address is in same DHCP range")
                        status = "SUCCESS"
                        LanIP = orgValue[1];
                        status = checkIpRange(LanIP,lanIP);
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("checkIpRange: SUCCESS")

                            print("TEST STEP 6: Get the DHCP server DNSServer of LAN client")
                            DNSServerInClient = str(getLanDhcpDetails(tdkbE2EUtility.lan_dns_server));
                            DNSServer = '4.4.4.4'
                            if DNSServerInClient:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("getLanDhcpDetails SUCCESS")

                                print("TEST STEP 7: Check whether DNSServer from client is matching with the value in GW")
                                if DNSServer in DNSServerInClient:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("DNSServer from client is matching with the value in GW")
                                    finalStatus = "SUCCESS";
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("DNSServer from client is not matching with the value in GW")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 6:Failed to get the DNSServer of LAN client")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("TEST STEP 5:LAN Client IP address is not in the same Gateway DHCP range")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 4:Failed to get the LAN Client IP address")

                    #Revert the DNS server to its original value
                    revertParamList = [dnsServer,orgValue[0],'string']
                    revertParamList = "|".join(map(str, revertParamList))
                    tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)

                    if expectedresult in actualresult and expectedresult in finalStatus:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("EXPECTED RESULT 8: Should set the original DNS server back");
                        print("ACTUAL RESULT 8: %s" %details);
                        print("[TEST EXECUTION RESULT] : SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print("EXPECTED RESULT 8: Should set the original DNS server back");
                        print("ACTUAL RESULT 8: %s" %details);
                        print("[TEST EXECUTION RESULT] : FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current DNS server in GW")
                    print("EXPECTED RESULT 3: Should retrieve the current DNS server in GW same as the set value")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : FAILURE");

            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Set the DNS server in GW")
                print("EXPECTED RESULT 2: Should set the DNS server in GW");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");

        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current DNSServer and lanIPAddress in GW")
            print("EXPECTED RESULT 1: Should retrieve the current DNSServer and lanIPAddress in GW")
            print("ACTUAL RESULT 1: %s" %newValues);
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