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
  <name>E2E_SANITY_CheckLANIPAddress</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>To check if the lan client is getting IP or not</synopsis>
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
    <test_case_id>TC_TDKB_E2E_410</test_case_id>
    <test_objective>To check if the lan client is getting IP or not</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. ssh to lan client connectted to the gateway
3. Check if the interface is getting the proper IP
4.  Check the range of IP obtained
5.Unload tdkb_e2e module</automation_approch>
    <except_output>The LAN client should get the IP address in the expected range</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_SANITY_CheckLANIPAddress</test_script>
    <skipped>No</skipped>
    <release_version>M59</release_version>
    <remarks>LAN</remarks>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
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
obj.configureTestCase(ip,port,'E2E_SANITY_CheckLANIPAddress');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

        print("TEST STEP 1: Get the current LAN IP address DHCP range")
        param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
        tdkTestObj,status,curIPAddress = getParameterValue(obj,param)

        if expectedresult in status and curIPAddress:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Should get the current LAN IP address DHCP range")
            print("TEST STEP 1: current LAN IP address DHCP range is :%s" %curIPAddress)
            print("TEST EXECUTION STATUS: SUCCESS")

            print("TEST STEP 2: Get the IP address of the lan client after connecting to it")
            lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
            if lanIP:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Should get the IP address of the lan client")
                print("TEST STEP 2: The LAN IP address is :%s" %lanIP)
                print("TEST EXECUTION STATUS: SUCCESS")

                print("TEST STEP 3: Check whether lan ip address is in same DHCP range")
                status = "SUCCESS"
                status = checkIpRange(curIPAddress,lanIP);
                if expectedresult in status:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: The lan IP should be in the same DHCP range")
                    print("TEST STEP 3:LAN client has got the IP address in the expected range")
                    print("TEST EXECUTION STATUS: SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: The lan IP should be in the same DHCP range")
                    print("TEST STEP 3:LAN client IP address is not in the expected range")
                    print("TEST EXECUTION STATUS: FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Should get the IP address of the lan client")
                print("TEST STEP 2: The LAN IP address is :%s" %lanIP)
                print("TEST EXECUTION STATUS: FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Should get the current LAN IP address DHCP range")
            print("TEST STEP 1: current LAN IP address DHCP range is :%s" %curIPAddress)
            print("TEST EXECUTION STATUS: FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE");
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    obj.unloadModule("tdkb_e2e");

else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");