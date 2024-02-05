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
  <name>E2E_WEBUI_LAN_Weak_Account_Lockout_Functionality</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if access is denied when logging in with correct credentials within 5 minutes after 3 incorrect password attempt</synopsis>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_508</test_case_id>
    <test_objective>To check if access is denied when logging in with correct credentials within 5 minutes after 3 incorrect password attempt</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. import selenium module
3. Get the lan mode and check if the device is in router mode
4. Get the lan client ip and get the current lan ip address dhcp range
5. Check the lan client ip is in dhcp range
6. Login with incorrect password 3 times
7. Check if Incorrect password for admin prompt is displayed for first two times.
8. Check if You have 3 failed login attempts and your account will be locked for 5 minutes prompt is displayed when logged in with incorrect password for third time
9. Try logging in with correct credentials within 5 minutes after account gets locked
10.Check if access is denied for logging in with correct credentials within 5 minutes after account gets locked
11.After 5 minutes,check if UI page is opened when logged in with correct credentials
12.Kill selenium hub and node
13. unload module</automation_approch>
    <except_output>Access should be denied after 3 incorrect password attempt</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WEBUI_LAN_Weak_Account_Lockout_Functionality</test_script>
    <skipped>No</skipped>
    <release_version>M67</release_version>
    <remarks>LAN</remarks>
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WEBUI_LAN_Weak_Account_Lockout_Functionality');

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
                            #Set Selenium grid
                            driver,status = startSeleniumGrid(tdkTestObj,"LAN",tdkbE2EUtility.grid_url,"NoLogin");
                            if status == "SUCCESS":
                                try:
                                    MAX_RETRY = 3;
                                    retryCount = 1;
                                    LOCKED_PROMPT = "You have 3 failed login attempts and your account will be locked for 5 minutes"
                                    while (retryCount <= MAX_RETRY):
                                        driver.find_element_by_id("username").send_keys(tdkbE2EUtility.ui_username)
                                        driver.find_element_by_id("password").send_keys(tdkbE2EUtility.incorrect_ui_password)
                                        driver.find_element_by_class_name("form-btn").submit()
                                        time.sleep(30);
                                        alert_obj = driver.switch_to.alert
                                        Incorrect_prompt = alert_obj.text
                                        alert_obj.accept()
                                        time.sleep(10);
                                        if (retryCount < MAX_RETRY):
                                            if (Incorrect_prompt == "Incorrect password for admin!"):
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print("TEST STEP 6: Get the incorrect password prompt")
                                                print("EXPECTED RESULT 6: Should get the incorrect password prompt")
                                                print("ACTUAL RESULT 6: Incorrect password prompt :%s" %Incorrect_prompt);
                                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP 6: Get the incorrect password prompt")
                                                print("EXPECTED RESULT 6: Should get the incorrect password prompt")
                                                print("ACTUAL RESULT 6: Failed to get incorrect password prompt");
                                                print("[TEST EXECUTION RESULT] : FAILURE");
                                        elif(retryCount == 3):
                                            if (Incorrect_prompt == LOCKED_PROMPT):
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print("TEST STEP 7: Get the account locked prompt")
                                                print("EXPECTED RESULT 7: Should Get the account locked prompt")
                                                print("ACTUAL RESULT 7:Account locked prompt: %s" %Incorrect_prompt) ;
                                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                                #Try logging in with correct password within 5 minutes
                                                driver.find_element_by_id("username").send_keys(tdkbE2EUtility.ui_username)
                                                driver.find_element_by_id("password").send_keys(tdkbE2EUtility.ui_password)
                                                driver.find_element_by_class_name("form-btn").submit()
                                                time.sleep(30);
                                                alert_obj = driver.switch_to.alert
                                                Incorrect_prompt = alert_obj.text
                                                alert_obj.accept()
                                                time.sleep(10);
                                                if (Incorrect_prompt == LOCKED_PROMPT):
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("TEST STEP 8: Account is locked.Get the account locked prompt")
                                                    print("EXPECTED RESULT 8: Should Get the account locked prompt")
                                                    print("ACTUAL RESULT 8:Account locked prompt: %s" %Incorrect_prompt) ;
                                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                                    print("Wait for 5 mins and check whether login is success")
                                                    time.sleep(300);
                                                    driver.find_element_by_id("username").send_keys(tdkbE2EUtility.ui_username)
                                                    driver.find_element_by_id("password").send_keys(tdkbE2EUtility.ui_password)
                                                    time.sleep(30);
                                                    checkUI = driver.find_element_by_xpath("/html/body/div[1]/div[3]/h1").text
                                                    if "Gateway > Login" == checkUI:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print("TEST STEP 9:Login to UI page")
                                                        print("EXPECTED RESULT 9: Should login to UI page")
                                                        print("ACTUAL RESULT 9:Successfully logged in to UI page");
                                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("TEST STEP 9:Login to UI page")
                                                        print("EXPECTED RESULT 9: Should login to UI page")
                                                        print("ACTUAL RESULT:Failed to login in to UI page");
                                                        print("[TEST EXECUTION RESULT] : FAILURE");
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("TEST STEP 8:Account is locked. Get the account locked prompt")
                                                    print("EXPECTED RESULT 8: Should Get the account locked prompt")
                                                    print("ACTUAL RESULT 8:Failed to get account locked prompt");
                                                    print("[TEST EXECUTION RESULT] : FAILURE");
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP 7: Get the account locked prompt")
                                                print("EXPECTED RESULT 7: Should Get the account locked prompt")
                                                print("ACTUAL RESULT 7:Failed to get account locked prompt");
                                                print("[TEST EXECUTION RESULT] : FAILURE");
                                        retryCount = retryCount + 1;
                                except Exception as error:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print(error);
                                time.sleep(10);
                                driver.quit();
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("Failed to set selenium grid")
                            #Kill selenium hub and node
                            status = tdkbWEBUIUtility.kill_hub_node("LAN")
                            if status == "SUCCESS":
                                print("TEST STEP 10:Executing Post-requisite")
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("Post-requisite success")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 10:Couldnt kill node and hub")
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

else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");