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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_ETHAGENT_WEBUI_WAN_ConnectLANClient_CheckConnectedDevices</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify the no. of connected devices displayed while hovering the mouse on the "Internet" tab displayed on the top right of "at-a-glance" page in Web UI</synopsis>
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
  <box_type>BPI</box_type></box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_522</test_case_id>
    <test_objective>Verify the no. of connected devices displayed while hovering the mouse on the "Internet" tab displayed on the top right of "at-a-glance" page in Web UI</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,RPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. import selenium module
3. Get the lan mode and check if the device is in router mode
4. Get the lan client ip and get the current lan ip address dhcp range
5. Check the lan client ip is in dhcp range
6. Get the connected device through namespace
7. Get the connected devices via WEBUI by hovering the mouse on Internet tab
8. Validate if  connected devices via WEBUI and connected devices via namespace are same
9. Kill selenium hub and node
10. unload module</automation_approch>
    <except_output>connected device displayed while hovering the mouse on the "Internet" tab and connected device retrieved through namespace should be same</except_output>
    <priority>High</priority>
    <test_stub_interface>None</test_stub_interface>
    <test_script>E2E_ETHAGENT_WEBUI_WAN_ConnectLANClient_CheckConnectedDevices</test_script>
    <skipped>No</skipped>
    <release_version>M68</release_version>
    <remarks>None</remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import tdkbE2EUtility;
from tdkbE2EUtility import *;
import tdkbWEBUIUtility;
from tdkbWEBUIUtility import *;
from selenium import webdriver
from selenium.webdriver import ActionChains

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");
obj1 = tdklib.TDKScriptingLibrary("tdkbtr181","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_ETHAGENT_WEBUI_WAN_ConnectLANClient_CheckConnectedDevices');
obj1.configureTestCase(ip,port,'E2E_ETHAGENT_WEBUI_WAN_ConnectLANClient_CheckConnectedDevices');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 =obj1.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus1) ;

if "SUCCESS" in loadmodulestatus.upper()and loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")
        lanMode = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode"
        tdkTestObj,status,orgValue = getParameterValue(obj,lanMode)
        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current lanMode")
            print("EXPECTED RESULT 1: Should retrieve the current lanMode")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");
            print("TEST STEP 2: Check whether device is in router mode")
            #Check if device is in router mode
            if orgValue == "router":
                #Connect to LAN client and obtain its IP
                print("TEST STEP 3: Get the IP address of the lan client after connecting to it")
                lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
                if lanIP:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 4: Get the current LAN IP address DHCP range")
                    param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                    tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                    print("LAN IP Address: %s" %curIPAddress);

                    if expectedresult in status and curIPAddress:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TEST STEP 5: Check whether lan ip address is in same DHCP range")
                        status = "SUCCESS"
                        status = checkIpRange(curIPAddress,lanIP);
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS");
                            tdkTestObj = obj1.createTestStep('TDKB_TR181Stub_Get');
                            tdkTestObj.addParameter("ParamName","Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber");

                            #Execute the test case in DUT
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            connectedDeviceNumber = tdkTestObj.getResultDetails().strip().replace("\\n", "");
                            if expectedresult in actualresult:
                                #Set the result status of execution
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("TEST STEP 6: Get the connected device number");
                                print("EXPECTED RESULT 6 : Should get the current connected device number")
                                print("ACTUAL RESULT 6:%s" %connectedDeviceNumber)
                                #Get the result of execution
                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                #Set Selenium grid
                                driver,status = startSeleniumGrid(tdkTestObj,"WAN",tdkbE2EUtility.mso_grid_url,"MSOLogin");
                                if status == "SUCCESS":
                                    try:
                                        print("Hovering the mouse on Internet tab to get connected devices")
                                        element = driver.find_element_by_link_text('Internet')
                                        hover = ActionChains(driver).move_to_element(element)
                                        hover.perform()
                                        hoverText = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/ul[2]/li[2]/a/div').text
                                        print("Connected status :%s" %hoverText)
                                        connectedDevice=hoverText.splitlines()[1]
                                        noOfConnectedDevice=connectedDevice.split()[0]
                                        print("No of connected devices via WEBUI :%s" %noOfConnectedDevice)
                                        if noOfConnectedDevice == connectedDeviceNumber:
                                            #Set the result status of execution
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("TEST STEP 7: Validate the connected device number from namespace and UI ");
                                            print("EXPECTED RESULT 7 : connected device number retrieved through namspace and WEBUI should be same")
                                            print("ACTUAL RESULT 7:connected device number retrieved through namspace and WEBUI should are same")
                                            #Get the result of execution
                                            print("[TEST EXECUTION RESULT] : SUCCESS");
                                        else:
                                            #Set the result status of execution
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP 7: Validate the connected device number from namespace and UI ");
                                            print("EXPECTED RESULT 7 : connected device number retrieved through namspace and WEBUI should be same")
                                            print("ACTUAL RESULT 7:connected device number retrieved through namspace and WEBUI should are not same")
                                            #Get the result of execution
                                            print("[TEST EXECUTION RESULT] : FAILURE");
                                    except Exception as error:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("exception")
                                        print(error);
                                    time.sleep(10);
                                    driver.quit();
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("Failed to set selenium grid")
                                #Kill selenium hub and node
                                status = tdkbWEBUIUtility.kill_hub_node("LAN")
                                if status == "SUCCESS":
                                    print("TEST STEP 8:Executing Post-requisite")
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("Post-requisite success")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 8:Couldnt kill node and hub")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 6: Failed to get the connected device number");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("TEST STEP 5: checkIpRange:lan ip address is not in DHCP range")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 4: getParameterValue : Failed to get gateway lan ip")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: getLanIPAddress:Failed to get the LAN client IP")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Device is in bridge mode")
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
    obj1.unloadModule("tdkbtr181");

else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");