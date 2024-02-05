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
  <name>E2E_WEBUI_LAN_IsUIAccessible_OnBridgeMode</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Check whether the admin UI page is accessible on bridge mode</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>true</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Broadband</box_type>
    <box_type>Emulator</box_type>

  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_515</test_case_id>
    <test_objective>Check whether the admin UI page is accessible on bridge mode</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>1. A LAN client should be connected to the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. import selenium module
3. Set the lanmode as bridge-static
4. check if the lan client has the ip in dhcp range
5. Start selenium hub in TM machine
6. Start Node in lan client machine
7. Try to access the WEBUI of the gateway using selenium grid
8. Validate if the UI page is accessible or not
9. Kill selenium hub and node
10. unload module</automation_approch>
    <except_output>The admin login page should be accessible on bridge mode</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WEBUI_LAN_IsUIAccessible_OnBridgeMode</test_script>
    <skipped>No</skipped>
    <release_version>M67</release_version>
    <remarks/>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WEBUI_LAN_IsUIAccessible_OnBridgeMode');

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

        param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
        tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
        print("LAN IP Address: %s" %curIPAddress);

        if expectedresult in status and curIPAddress:
            tdkTestObj.setResultStatus("SUCCESS");
            #Connect to LAN client and obtain its IP
            print("TEST STEP 1: Get the IP address of the lan client after connecting to it")
            lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
            if lanIP:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Get the current LAN IP address DHCP range")

                print("TEST STEP 3: Check whether lan ip address is in same DHCP range")
                status = "SUCCESS"
                status = checkIpRange(curIPAddress,lanIP);
                if expectedresult in status:
                    tdkTestObj.setResultStatus("SUCCESS");

                    #Check if the UI page is accessible or not
                    driver,status = startSeleniumGrid(tdkTestObj,"LAN",tdkbE2EUtility.grid_url,"NoLogin");
                    if status == "SUCCESS":
                        time.sleep(10);
                        driver.quit();

                        #Get the lanmode
                        lanMode = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode"
                        #Get the value of the wifi parameters that are currently set.
                        tdkTestObj,status,orgValue = getParameterValue(obj,lanMode)

                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("TEST STEP 4: Get the current lanMode")
                            print("EXPECTED RESULT 4: Should retrieve the current lanMode")
                            print("ACTUAL RESULT 4: %s" %orgValue);
                            print("[TEST EXECUTION RESULT] : SUCCESS");

                            #Set the lanmode to bridge-static
                            if orgValue == "router":
                                setValuesList = "bridge-static";
                                print("Parameter values that are set: %s" %setValuesList)

                                lanModeValue="%s|bridge-static|string" %lanMode

                                tdkTestObj,actualresult1,details = setMultipleParameterValues(obj,lanModeValue)
                                time.sleep(90);
                                if expectedresult in actualresult1:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("TEST STEP 5: Set the lanMode as bridge mode")
                                    print("EXPECTED RESULT 5: Should set the lanMode as bridge mode");
                                    print("ACTUAL RESULT 5: %s" %details);
                                    print("[TEST EXECUTION RESULT] : SUCCESS");

                                    tdkTestObj,status,newValues = getParameterValue(obj,lanMode)

                                    if expectedresult in status and setValuesList == newValues:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("TEST STEP 6: Get the current lanMode")
                                        print("EXPECTED RESULT 6: Should retrieve the current lanMode")
                                        print("ACTUAL RESULT 6: %s" %newValues);
                                        print("[TEST EXECUTION RESULT] : SUCCESS");

                                        #Check if the UI accessible in bridge mode also
                                        status,driver = openLocalWebUI(tdkbE2EUtility.grid_url,tdkTestObj,"NoLogin");
                                        if status == "SUCCESS":
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            time.sleep(10);
                                            driver.quit();
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("Failed to open UI in bridge mode")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 6: Get the current lanMode")
                                        print("EXPECTED RESULT 6: Should retrieve the current lanMode")
                                        print("ACTUAL RESULT 6: %s" %newValues);
                                        print("[TEST EXECUTION RESULT] : FAILURE");
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 5: Set the lanMode as bridge mode")
                                    print("EXPECTED RESULT 5: Should set the lanMode as bridge mode");
                                    print("ACTUAL RESULT 5: %s" %details);
                                    print("[TEST EXECUTION RESULT] : FAILURE");
                                #Restore the lanmode value
                                lanModeValue="%s|router|string" %lanMode
                                tdkTestObj,actualresult1,details = setMultipleParameterValues(obj,lanModeValue)
                                time.sleep(90);
                                if expectedresult in actualresult1:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("TEST STEP 7: Set the lanMode as previous value")
                                    print("EXPECTED RESULT 7: Should set the lanMode as previous value");
                                    print("ACTUAL RESULT 7: %s" %details);
                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 7: Set the lanMode as previous value")
                                    print("EXPECTED RESULT 7: Should set the lanMode as previous value");
                                    print("ACTUAL RESULT 7: %s" %details);
                                    print("[TEST EXECUTION RESULT] : FAILURE");
                            else:
                                print("\nLanMode is already bridge-static and UI is accessible\n")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("TEST STEP 4: Get the current lanMode")
                            print("EXPECTED RESULT 4: Should retrieve the current lanMode")
                            print("ACTUAL RESULT 4: %s" %orgValue);
                            print("[TEST EXECUTION RESULT] : FAILURE");
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
                print("getLanIPAddress:Failed to get the LAN client IP")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("getParameterValue : Failed to get gateway lan ip")
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