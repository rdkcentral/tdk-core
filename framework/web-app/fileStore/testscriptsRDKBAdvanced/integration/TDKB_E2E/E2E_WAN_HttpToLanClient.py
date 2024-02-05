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
  <name>E2E_WAN_HttpToLanClient</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify that http connection from WAN to LAN client ip is not success</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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
    <box_type>RPI</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_540</test_case_id>
    <test_objective>Verify that http connection from WAN to LAN client ip is not success</test_objective>
    <test_type>Negative</test_type>
    <test_setup>Broadband,RPI</test_setup>
    <pre_requisite>LAN client device and a WAN machine with the tdkb e2e WAN configuration should be available</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save the current gateway ip address
3.Get the LAN client IP
4. Check if the LAN client's ip received from gateway is in valid range
5. From WAN client check if HTTP connection to LAN client ip is success or not
6.Unload tdkb_e2e module</automation_approch>
    <expected_output> HTTP connection to LAN client ip is not success</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WAN_HttpToLanClient</test_script>
    <skipped>No</skipped>
    <release_version>M93</release_version>
    <remarks>LAN,WAN</remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import tdkbE2EUtility
from tdkbE2EUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WAN_HttpToLanClient');

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

        lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
        if lanIP:
            print("TEST STEP 1: Get the current GW IP address")
            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
            tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
            print("GW IP Address: %s" %curIPAddress);

            if expectedresult in status and curIPAddress:
                tdkTestObj.setResultStatus("SUCCESS");

                print("TEST STEP 2: Check whether lan ip address is in same DHCP range")
                status = "SUCCESS"
                status = checkIpRange(curIPAddress,lanIP);
                if expectedresult in status:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("lan ip address is in same DHCP range")
                    tdkTestObj.setResultStatus("SUCCESS");

                    print("TEST STEP 3: Check the http connection from WAN to LAN client ip")
                    expectedresult = "FAILURE"
                    status =verifyNetworkConnectivity(lanIP, "WGET_HTTP", tdkbE2EUtility.wan_ip, curIPAddress, "WAN")
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("SUCCESS: http connection from WAN to LAN client ip is not successful")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 3: FAILURE : http connection from WAN to LAN client ip is not blocked")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 2:LAN Client IP address is not in the same Gateway DHCP range")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 1:Failed: to get GW IP address")
        else:
            print("Failed: to get client LAN IP address")
    else:
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup();
    obj.unloadModule("tdkb_e2e");

else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");