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
  <name>E2E_WEBUI_LAN_Admin_PasswordReset</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Device.Users.User.3.X_RDKCENTRAL-COM_PasswordReset should reset the admin password to default.</synopsis>
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
    <test_case_id>TC_TDKB_E2E_513</test_case_id>
    <test_objective>Device.Users.User.3.X_RDKCENTRAL-COM_PasswordReset should reset the admin password to default.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.Users.User.3.X_RDKCENTRAL-COM_PasswordReset</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. import selenium module
3. Get the lan mode and check if the device is in router mode
4. Get the lan client ip and get the current lan ip address dhcp range
5. Check the lan client ip is in dhcp range
6. Check if default password is changed after factory reset
7. If default password is changed,reset the password using Device.Users.User.3.X_RDKCENTRAL-COM_PasswordReset
8. Login with default password
9. Check if You are using default password.Please change the password prompt is displayed after resetting the password
10.If default password is not changed,change the password and reset the password
11. Login with default password and check if You are using default password.Please change the password prompt is displayed
12. Kill selenium hub and node
13. unload module</automation_approch>
    <except_output>After resetting the password,You are using default password.Please change the password prompt  should be displayed</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WEBUI_LAN_Admin_PasswordReset</test_script>
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
from tdkutility import changeAdminPassword;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");
sysobj = tdklib.TDKScriptingLibrary("sysutil","1");
tadobj = tdklib.TDKScriptingLibrary("tad","1");
pamobj = tdklib.TDKScriptingLibrary("pam","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WEBUI_LAN_Admin_PasswordReset');
sysobj.configureTestCase(ip,port,'E2E_WEBUI_LAN_Admin_PasswordReset');
tadobj.configureTestCase(ip,port,'E2E_WEBUI_LAN_Admin_PasswordReset');
pamobj.configureTestCase(ip,port,'E2E_WEBUI_LAN_Admin_PasswordReset');

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
                            cmd= "cat /tmp/syscfg.db  | grep -i user_password_3";
                            tdkTestObj = sysobj.createTestStep('ExecuteCmd');
                            tdkTestObj.addParameter("command",cmd);
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            user_password_3 = tdkTestObj.getResultDetails().strip().replace("\\n", "");
                            if user_password_3 == "":
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("TEST STEP 6: Check if default password is changed after factory reset");
                                print("EXPECTED RESULT 6: Default password is changed after factory reset.user_password_3 entry should not be present in syscfg.db");
                                print("ACTUAL RESULT 6:Default password is changed after factory reset.user_password_3 entry is not present in syscfg.db");
                                #Get the result of execution
                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                tdkTestObj = tadobj.createTestStep('TADstub_Set');
                                tdkTestObj.addParameter("ParamName","Device.Users.User.3.X_RDKCENTRAL-COM_PasswordReset");
                                tdkTestObj.addParameter("ParamValue","true");
                                tdkTestObj.addParameter("Type","boolean");
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details = tdkTestObj.getResultDetails();
                                #Set the result status of execution
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("TEST STEP 7: Set value for Device.Users.User.3.X_RDKCENTRAL-COM_PasswordReset")
                                print("EXPECTED RESULT 7: Should set value for Device.Users.User.3.X_RDKCENTRAL-COM_PasswordReset");
                                print("ACTUAL RESULT 7: Admin password is reset");
                                #Get the result of execution
                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                #Set Selenium grid
                                driver,status = startSeleniumGrid(tdkTestObj,"LAN",tdkbE2EUtility.grid_url,"NoLogin");
                                if status == "SUCCESS":
                                    try:
                                        print("Logging in with default password")
                                        driver.find_element_by_id("username").send_keys(tdkbE2EUtility.ui_username)
                                        driver.find_element_by_id("password").send_keys(tdkbE2EUtility.default_ui_password)
                                        driver.find_element_by_class_name("form-btn").submit()
                                        time.sleep(30);
                                        DEFAULT_MESSAGE_POPUP = "You are using default password. Please change the password."
                                        defaultmessage_popup = driver.find_element_by_xpath('//*[@id="popup_message"]').text
                                        if defaultmessage_popup == DEFAULT_MESSAGE_POPUP:
                                            #Set the result status of execution
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("TEST STEP 8: Check if change default password popup is displayed")
                                            print("EXPECTED RESULT 8: Change default password popup should be displayed");
                                            print("ACTUAL RESULT 8: Change default password popup is displayed");
                                            #Get the result of execution
                                            print("[TEST EXECUTION RESULT] : SUCCESS");
                                            #Click on ok button
                                            driver.find_element_by_xpath('//*[@id="popup_ok"]').click()
                                            print("Reverting the login password to previous value")
                                            #Revert the login password to previous value
                                            changeAdminPassword(pamobj,tdkbE2EUtility.ui_password);
                                        else:
                                            #Set the result status of execution
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP 8: Check if change default password popup is displayed")
                                            print("EXPECTED RESULT 8: Change default password popup should be displayed");
                                            print("ACTUAL RESULT 8: Change default password popup is not displayed");
                                            #Get the result of execution
                                            print("[TEST EXECUTION RESULT] : FAILURE");
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
                                    print("TEST STEP 9:Executing Post-requisite")
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("Post-requisite success")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 9:Couldnt kill node and hub")
                            else:
                                tdkTestObj.setResultStatus("SUCCESS");
                                #Change the default password value
                                changeAdminPassword(pamobj,tdkbE2EUtility.ui_password);
                                print("TEST STEP 6: Default password is not changed after factory reset.Change the default password");
                                print("EXPECTED RESULT 6:Default password should be changed");
                                print("ACTUAL RESULT 6: Default password is changed");
                                #Get the result of execution
                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                tdkTestObj = tadobj.createTestStep('TADstub_Set');
                                tdkTestObj.addParameter("ParamName","Device.Users.User.3.X_RDKCENTRAL-COM_PasswordReset");
                                tdkTestObj.addParameter("ParamValue","true");
                                tdkTestObj.addParameter("Type","boolean");
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details = tdkTestObj.getResultDetails();
                                #Set the result status of execution
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("TEST STEP 8: Set value for Device.Users.User.3.X_RDKCENTRAL-COM_PasswordReset")
                                print("EXPECTED RESULT 8: Should set value for Device.Users.User.3.X_RDKCENTRAL-COM_PasswordReset");
                                print("ACTUAL RESULT 8: Admin password is reset");
                                #Get the result of execution
                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                #Set Selenium grid
                                driver,status = startSeleniumGrid(tdkTestObj,"LAN",tdkbE2EUtility.grid_url);
                                if status == "SUCCESS":
                                    try:
                                        driver.find_element_by_id("username").send_keys(tdkbE2EUtility.ui_username)
                                        driver.find_element_by_id("password").send_keys(tdkbE2EUtility.default_ui_password)
                                        driver.find_element_by_class_name("form-btn").submit()
                                        time.sleep(30);
                                        defaultmessage_popup = driver.find_element_by_xpath('//*[@id="popup_message"]').text
                                        print(defaultmessage_popup)
                                        #Click on ok button
                                        driver.find_element_by_xpath('//*[@id="popup_ok"]').click()
                                        #Revert the login password to previous value
                                        changeAdminPassword(pamobj,tdkbE2EUtility.ui_password);
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
                                    print("TEST STEP 8:Executing Post-requisite")
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("Post-requisite success")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 8:Couldnt kill node and hub")
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
    tadobj.unloadModule("tad");
    sysobj.unloadModule("sysutil");
    pamobj.unloadModule("pam");
else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");