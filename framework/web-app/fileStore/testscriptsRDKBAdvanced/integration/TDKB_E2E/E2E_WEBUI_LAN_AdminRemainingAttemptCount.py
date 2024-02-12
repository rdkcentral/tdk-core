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
  <name>E2E_WEBUI_LAN_AdminRemainingAttemptCount</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if number of remaining attempt count decreases after each incorrect login attempt</synopsis>
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
    <test_case_id>TC_TDKB_E2E_512</test_case_id>
    <test_objective>To check if number of remaining attempt count decreases after each incorrect login attempt</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.Users.User.3.X_RDKCENTRAL-COM_RemainingAttempts</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. import selenium module
3. Get the lan mode and check if the device is in router mode
4. Get the lan client ip and get the current lan ip address dhcp range
5. Check the lan client ip is in dhcp range
6. Get default number of remaining attempt
7. Login with incorrect password 3 times
8. Get number of remaining attempt each time after logging in with incorrect password
9. Check if number of remaining attempt decreases after each incorrect login attempt
10. Check if remaining attempt count after 5 minutes is same as default number of remaining attempt count
11. Kill selenium hub and node
12. unload module</automation_approch>
    <except_output>Number of remaining attempt should decrease after each incorrect login attempt</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WEBUI_LAN_AdminRemainingAttemptCount</test_script>
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
obj.configureTestCase(ip,port,'E2E_WEBUI_LAN_AdminRemainingAttemptCount');

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
                            print("TEST STEP 6: Get the default number of remaining attempts")
                            param = "Device.Users.User.3.X_RDKCENTRAL-COM_RemainingAttempts"
                            tdkTestObj,status,orgremainingattempt = getParameterValue(obj,param)
                            print("Default Remaining attempt: %s" %orgremainingattempt);
                            if expectedresult in status and orgremainingattempt == "3":
                                #Set Selenium grid
                                driver,status = startSeleniumGrid(tdkTestObj,"LAN",tdkbE2EUtility.grid_url,"NoLogin");
                                if status == "SUCCESS":
                                    try:
                                        retryCount = 1;
                                        MAX_RETRY = 3;
                                        MIN_REMAINING_ATTEMPT = 0
                                        #Login with incorrect password 3 times
                                        while retryCount <= MAX_RETRY:
                                            driver.find_element_by_id("username").send_keys(tdkbE2EUtility.ui_username)
                                            driver.find_element_by_id("password").send_keys(tdkbE2EUtility.incorrect_ui_password)
                                            driver.find_element_by_class_name("form-btn").submit()
                                            time.sleep(20);
                                            alert_obj = driver.switch_to.alert
                                            alert_obj.accept()
                                            time.sleep(10);
                                            print("TEST STEP 7: Get the current Number of remaining attempts")
                                            tdkTestObj,status,currentremainingattempt = getParameterValue(obj,param)
                                            print("Current Remaining attempt: %s" %currentremainingattempt);
                                            if expectedresult in status:
                                                if (int(currentremainingattempt)) == (int(int(orgremainingattempt) - retryCount)):
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("TEST STEP 8:Check if remaining attempt decreases after each incorrect login attempt")
                                                    print("EXPECTED RESULT 8:Remaining attempt should decrease after each incorrect login attempt")
                                                    print("ACTUAL RESULT 8:Remaining attempt count :%s" %currentremainingattempt);
                                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                                    if int(currentremainingattempt) == int(MIN_REMAINING_ATTEMPT):
                                                        print("Wait for 5 minutes till account lockout time")
                                                        time.sleep(300);
                                                        print("Current remaining attempt reached minimum remaining attempt")
                                                        tdkTestObj,status,lastremainingattempt = getParameterValue(obj,param)
                                                        if expectedresult in status:
                                                            tdkTestObj.setResultStatus("SUCCESS");
                                                            print("TEST STEP 9:Get the remaining attempt count after 5 minutes")
                                                            print("EXPECTED RESULT 9:Should get the remaining attempt count after 5 minutes")
                                                            print("ACTUAL RESULT 9:REMAINING ATTEMPT after 5 minutes: %s" %lastremainingattempt);
                                                            print("[TEST EXECUTION RESULT] : SUCCESS");
                                                            if int(lastremainingattempt) == int(orgremainingattempt):
                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                print("TEST STEP 10:Remaining attempt count after 5 minutes and default remaining attempt count should be same")
                                                                print("EXPECTED RESULT 10:Should get the same value for remaining attempt count after 5 minutes and default remaining attempt count ")
                                                                print("ACTUAL RESULT 10:Remaining attempt count after 5 minutes and default remaining attempt count are same");
                                                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                                            else:
                                                                tdkTestObj.setResultStatus("FAILURE");
                                                                print("TEST STEP 10:Remaining attempt count after 5 minutes and default remaining attempt count should be same")
                                                                print("EXPECTED RESULT 10:Should get the same value for remaining attempt count after 5 minutes and default remaining attempt count ")
                                                                print("ACTUAL RESULT 10:Remaining attempt count after 5 minutes and default remaining attempt count are not same");
                                                                print("[TEST EXECUTION RESULT] : FAILURE");
                                                        else:
                                                            tdkTestObj.setResultStatus("FAILURE");
                                                            print("TEST STEP 9:Get the remaining attempt count after 5 minutes")
                                                            print("EXPECTED RESULT 9:Should get the remaining attempt count after 5 minutes")
                                                            print("ACTUAL RESULT 9:Failed to get the remaining attempt count after 5 minutes");
                                                            print("[TEST EXECUTION RESULT] : FAILURE");
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("TEST STEP 8:Check if remaining attempt decreases after each incorrect login attempt")
                                                    print("EXPECTED RESULT 8:Remaining attempt should decrease after each incorrect login attempt")
                                                    print("ACTUAL RESULT 8:Remaining attempt count is not getting decreased after each incorrect login attempt");
                                                    print("[TEST EXECUTION RESULT] : FAILURE");
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP 7:Failed to get number of remaining attempts")
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
                                    print("TEST STEP 11:Executing Post-requisite")
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("Post-requisite success")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 11:Couldnt kill node and hub")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 6: Failed to get the default number of remaining attempts")
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