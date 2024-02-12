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
  <name>E2E_CM_GetCMIPAddress</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Verify that CM IP address of WG obtained through parameter (Device.X_CISCO_COM_CableModem.IPAddress)matches with the actual value.</synopsis>
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
    <test_case_id>TC_TDKB_E2E_356</test_case_id>
    <test_objective>Verify that CM IP address of WG obtained through parameter (Device.X_CISCO_COM_CableModem.IPAddress/Device.X_CISCO_COM_CableModem.IPv6Address)matches with the actual value.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband</test_setup>
    <pre_requisite>Enusre CMAgent is up and running in the DUT</pre_requisite>
    <api_or_interface_used>tdkb_e2e_Get</api_or_interface_used>
    <input_parameters>Device.X_CISCO_COM_CableModem.IPAddress
Device.X_CISCO_COM_CableModem.IPv6Address</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get the current CM IP Address and check whether the retrieved CM IP address is the same configured in the device configuration file
3 Unload tdkb_e2e module</automation_approch>
    <except_output>CM IP address of WG obtained through parameter (Device.X_CISCO_COM_CableModem.IPAddress or Device.X_CISCO_COM_CableModem.IPv6Address)should match with the value configured in the device configuration file.</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_CM_GetCMIPAddress</test_script>
    <skipped>No</skipped>
    <release_version>M53</release_version>
    <remarks/>
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

obj.configureTestCase(ip,port,'E2E_CM_GetCMIPAddress');

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

        print("CM IP in device configuration file:%s" %tdkbE2EUtility.cm_ip)
        print("CM IP Type in device configuration file:%s" %tdkbE2EUtility.cm_ip_type)

        #Get the current CM IP Address
        if tdkbE2EUtility.cm_ip_type == "IPV4":
            param = "Device.X_CISCO_COM_CableModem.IPAddress"
        else:
            param = "Device.X_CISCO_COM_CableModem.IPv6Address"

        tdkTestObj,status,cmIPAddress = getParameterValue(obj,param)

        if expectedresult in status and cmIPAddress == tdkbE2EUtility.cm_ip:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current CM IP Address")
            print("EXPECTED RESULT 1: Should retrieve the current CM IP Address")
            print("ACTUAL RESULT 1: %s" %cmIPAddress);
            print("[TEST EXECUTION RESULT] : %s" %status);
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current CM IP Address")
            print("EXPECTED RESULT 1: Should retrieve the current CM IP Address")
            print("ACTUAL RESULT 1: %s" %cmIPAddress);
            print("[TEST EXECUTION RESULT] : %s" %status);
    else:
        obj.setLoadModuleStatus("FAILURE");
        print("Failed to parse the device configuration file")

    #Unload the module
    obj.unloadModule("tdkb_e2e");

else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");