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
  <name>E2E_ETHWAN_WEBUI_LAN_CheckBridgeModeOption</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Gateway MUST grays out bridge mode option in the local UI (ADMIN) in EWAN mode according to the partner ID. And put a note indicating, "Bridge Mode not supported in Ethernet WAN mode".</synopsis>
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
    <test_case_id>TC_TDKB_E2E_526</test_case_id>
    <test_objective>Gateway MUST grays out bridge mode option in the local UI (ADMIN) in EWAN mode according to the partner ID. And put a note indicating, "Bridge Mode not supported in Ethernet WAN mode".</test_objective>
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
3. If enabled, start selenium hub and node to access webui
4. Check if bridge-mode option is grayed out in ethwan mode
5. Exit the browser
6. Unload module</automation_approch>
    <except_output>Gateway MUST grays out bridge mode option in the local UI (ADMIN) in EWAN mode according to the partner ID. And put a note indicating, "Bridge Mode not supported in Ethernet WAN mode".</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_ETHWAN_WEBUI_LAN_CheckBridgeModeOption</test_script>
    <skipped>No</skipped>
    <release_version>M68</release_version>
    <remarks>LAN</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import tdkbE2EUtility;
from tdkbE2EUtility import *;
import tdkbWEBUIUtility;
from tdkbWEBUIUtility import *;
import re;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");
obj1 = tdklib.TDKScriptingLibrary("sysutil","RDKB");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_ETHWAN_WEBUI_LAN_CheckBridgeModeOption');
obj1.configureTestCase(ip,port,'E2E_ETHWAN_WEBUI_LAN_CheckBridgeModeOption');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 =obj1.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus1) ;

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS");
    obj1.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

        ethwanmode = "Device.Ethernet.X_RDKCENTRAL-COM_WAN.Enabled"
        #Get the value of the wifi parameters that are currently set.
        tdkTestObj,status,orgValue = getParameterValue(obj,ethwanmode)

        if expectedresult in status and orgValue == "true":
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current ethwan mode")
            print("EXPECTED RESULT 1: Should retrieve the current ethwan mode as true");
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            #Connect to LAN client and obtain its IP
            print("TEST STEP 2: Get the IP address of the lan client after connecting to it")
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
                        bridgeModeStatus = tdkbE2EUtility.bridgemode_status
                        #Set Selenium grid
                        driver,status = startSeleniumGrid(tdkTestObj,"LAN",tdkbE2EUtility.grid_url);
                        if status == "SUCCESS":
                            if bridgeModeStatus == "Enabled":
                                expectedResult = True;
                            else:
                                expectedResult = False;
                            #Check if the bridgemode enabling button is grayed out or not
                            isButtonEnabled = driver.find_element_by_id("at_a_glance_enabled").is_enabled()
                            if isButtonEnabled == expectedResult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("SUCCESS: The behaviour of bridge mode enabling option is as expected")
                                #Check if the given text is present in the web page
                                text = "Bridge Mode not supported in Ethernet WAN mode"
                                if expectedResult == False:
                                    if (text in driver.page_source):
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("SUCCESS: Warning about the bridge mode option is displayed");
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("FAILURE: Warning about the bridge mode option is not displayed");
                                else:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("Bridge mode is supported")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("FAILURE: The bridge mode enabling option is not grayed out in ethwan mode")
                            time.sleep(10);
                            driver.quit();
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("Failed to set selenium grid")
                        #Kill selenium hub and node
                        status = tdkbWEBUIUtility.kill_hub_node("LAN")
                        if status == "SUCCESS":
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("Post-requisite success")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("Couldnt kill node and hub")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("checkIpRange:lan ip address is not in DHCP range")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("getParameterValue : Failed to get gateway lan ip")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("getLanIPAddress:Failed to get the LAN client IP")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current lanMode")
            print("EXPECTED RESULT 1: Should retrieve the current lanMode")
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