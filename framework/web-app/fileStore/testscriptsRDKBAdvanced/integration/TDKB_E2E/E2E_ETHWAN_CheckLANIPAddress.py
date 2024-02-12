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
  <version>2</version>
  <name>E2E_ETHWAN_CheckLANIPAddress</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Ethernet/WIFI client should get both ipv6 and ipv4 address when in ethwan mode.</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>true</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Broadband</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_524</test_case_id>
    <test_objective>Ethernet/WIFI client should get both ipv6 and ipv4 address when in ethwan mode.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband</test_setup>
    <pre_requisite>1. The broadband device should be in ETHWAN setup
2. The EthWAN mode should be enabled
3. TDK Agent must be up and running
4. Lan client should be connected to the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.Ethernet.X_RDKCENTRAL-COM_WAN.Enabled</input_parameters>
    <automation_approch>1. Load module
2. Check if ethwan mode is enabled or not
3. If enabled check the IPV4 and IPV6 address of lan client
4. Unload module</automation_approch>
    <except_output>Ethernet client should get IPV4 and IPV6 addresses in ethwan mode</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_ETHWAN_CheckLANIPAddress</test_script>
    <skipped>No</skipped>
    <release_version>M68</release_version>
    <remarks>LAN</remarks>
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
obj.configureTestCase(ip,port,'E2E_ETHWAN_CheckLANIPAddress');

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

        #Assign the WIFI parameters names to a variable
        param = "Device.Ethernet.X_RDKCENTRAL-COM_WAN.Enabled"

        #Get the value of the parameters that are currently set.
        tdkTestObj,status,orgValue = getParameterValue(obj,param)

        if expectedresult in status and orgValue == "true":
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current ethwan status");
            print("EXPECTED RESULT 1: Should retrieve the current ethwan status as true")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            #Connect to LAN client and obtain its IP
            lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
            if lanIP:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Get the current LAN IP address DHCP range")
                print("TEST STEP 2: The IPV4 address of lan client is %s" %lanIP)
                print("TEST STEP 2: SUCCESS")

                #get ipv6 address
                lanIPV6 = getLanIPV6Address(tdkbE2EUtility.lan_interface);
                if lanIPV6:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current LAN IP address DHCP range")
                    print("TEST STEP 3: The IPV6 address of lan client is %s" %lanIPV6)
                    print("TEST STEP 3: SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current LAN IP address DHCP range")
                    print("TEST STEP 3: The IPV6 address of lan client is %s" %lanIPV6)
                    print("TEST STEP 3: FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Get the current LAN IP address DHCP range")
                print("TEST STEP 2: The IPV4 address of lan client is %s" %lanIP)
                print("TEST STEP 2: FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current ethwan status")
            print("EXPECTED RESULT 1: Should retrieve the current ethwan status as true")
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