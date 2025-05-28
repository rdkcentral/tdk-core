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
  <version>1</version>
  <name>E2E_RouterMode_CheckLANIPAddress</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Verify that when Bridge mode is disabled ensure that Ethernet client should get back IP address only through DHCP server</synopsis>
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
  <box_type>BPI</box_type></box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_203</test_case_id>
    <test_objective>Verify that when Bridge mode is disabled ensure that Ethernet client should get back IP address only through DHCP server</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save lanMode
3. Set lanMode as router
4.  Connect to the LAN client
5.Check if ping to default GW IP and GW IP are success
6.Unload tdkb_e2e module</automation_approch>
    <except_output>Ping from LAN to Default Gateway WAN IP Address  and Ping from LAN to DHCP server should be success</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_RouterMode_CheckLANIPAddress</test_script>
    <skipped>No</skipped>
    <release_version>M57</release_version>
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

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_RouterMode_CheckLANIPAddress');

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
        lanMode = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode"
        gwIP = "Device.DHCPv4.Client.1.IPRouters"

        #Get the value of the wifi parameters that are currently set.
        paramList=[lanMode,gwIP]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current lanMode and GatewayIP")
            print("EXPECTED RESULT 1: Should retrieve the current lanMode and gatewayIP")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            # Set securityMode and radioEnable for 2.4ghz"
            setValuesList = ['router'];
            print("WIFI parameter values that are set: %s" %setValuesList)

            lanModeValue="%s|router|string" %lanMode

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,lanModeValue)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set the lanMode")
                print("EXPECTED RESULT 2: Should set lanMode");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");

                #Retrieve the values after set and compare
                newParamList=[lanMode]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current lanMode")
                    print("EXPECTED RESULT 3: Should retrieve the current lanMode")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    #Connect to LAN client and obtain its IP
                    print("TEST STEP 4: Get the IP address of the lan client after connecting to it")
                    lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
                    if lanIP:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TEST STEP 5: Get the current LAN IP address DHCP range")
                        param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                        tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                        print("LAN IP Address: %s" %curIPAddress);

                        if expectedresult in status and curIPAddress:
                            tdkTestObj.setResultStatus("SUCCESS");
                            #Send ping request to WLAN client from LAN client
                            print("TEST STEP 6:Check the PING from LAN");
                            status = verifyNetworkConnectivity(orgValue[1], "PING", lanIP, curIPAddress, "LAN")
                            if expectedresult in status:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("Ping successful from LAN to Default Gateway WAN IP Address")
                                status = verifyNetworkConnectivity(curIPAddress, "PING", lanIP, curIPAddress, "LAN")
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("Ping successful from LAN to DHCP server")
                                    finalStatus = "SUCCESS"
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("Ping not successful from LAN to DHCP server")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("Ping not successful from LAN to Default Gateway WAN IP Address")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("getParameterValue : Failed to get gateway lan ip")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("getLanIPAddress:Failed to get the LAN client IP")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current lanMode")
                    print("EXPECTED RESULT 3: Should retrieve the current lanMode")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Set the lanMode")
                print("EXPECTED RESULT 2: Should set lanMode");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
            #revert the params
            lanModeValue="%s|%s|string" %(lanMode,orgValue[0])
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,lanModeValue)
            if expectedresult in actualresult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 7: Should set the lan mode");
                print("ACTUAL RESULT 7: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 7: Should set the original lan mode");
                print("ACTUAL RESULT 7: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current lanMode and GatewayIP")
            print("EXPECTED RESULT 1: Should retrieve the current lanMode and gatewayIP")
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