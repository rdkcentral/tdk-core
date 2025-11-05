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
  <name>E2E_WIFI_ConnectTo_InvalidSSID</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify that Wireless client is not able to connect to WG with SSID that is not configured in WG</synopsis>
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
  <box_type>BPI</box_type></box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_41</test_case_id>
    <test_objective>Verify that Wireless client is not able to connect to WG with SSID that is not configured in WG</test_objective>
    <test_type>Negative</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Invalid ssid
Invalid passwod</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. From WLAN cliet, try to connect to an invalid SSID and password combination
3. Check if this connection attempt is failing
4. Unload tdkb_e2e module</automation_approch>
    <except_output>Connection attempt from WLAN client should fail</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WIFI_ConnectTo_InvalidSSID</test_script>
    <skipped>No</skipped>
    <release_version>M53</release_version>
    <remarks>WLAN</remarks>
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
obj.configureTestCase(ip,port,'E2E_WIFI_ConnectTo_InvalidSSID');

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

        #Connect to the invalid wifi ssid from wlan client
        tdkTestObj = obj.createTestStep("tdkb_e2e_Get");
        tdkTestObj.addParameter("paramName","Device.WiFi.SSID.1.SSID")
        tdkTestObj.executeTestCase(expectedresult);

        print("TEST STEP 4: From wlan client, Connect to the wifi ssid")
        expectedresult = "Couldn't find the SSID in available SSIDs list"
        status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_invalid_name,tdkbE2EUtility.ssid_invalid_pwd,tdkbE2EUtility.wlan_invalid_interface);

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("EXPECTED RESULT 3: Connection to invalid SSID should fail")
            print("ACTUAL RESULT 3: Connection to invalid SSID failed : %s" %status) ;
            print("[TEST EXECUTION RESULT] : SUCCESS")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("EXPECTED RESULT 3: Connection to invalid SSID should fail")
            print("ACTUAL RESULT 3: Connection to invalid SSID didn't fail") ;
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        print("Failed to parse the device configuration file")

    obj.unloadModule("tdkb_e2e");
else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");