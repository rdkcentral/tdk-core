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
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_WEBUI_WAN_AddBlockedSites</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Add same blocking site two times in ui only the case should change and check if it is allowed</synopsis>
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
    <box_type>Emulator</box_type>
    <!--  -->
    <box_type>RPI</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_531</test_case_id>
    <test_objective>Add same blocking site two times in ui only the case should change and check if it is allowed</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,RPI,Emulator</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. import selenium module
3. Get the lan mode and check if the device is in router mode
4.Retrieve the lan MAC address
5. Start selenium hub in TM machine
6. Start Node in wan client machine
7. Try to access the WEBUI of the gateway using selenium grid
8. Navigate to Parental control
9.Enable managed sites
10.Add same blocking site two times in different case.
11.Check if it is not allowed
12. Kill selenium hub and node
13. unload module</automation_approch>
    <expected_output>Adding same blocking site two times in ui with different cases should not be allowed</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WEBUI_WAN_AddBlockedSites</test_script>
    <skipped>No</skipped>
    <release_version>M71</release_version>
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
from selenium.common.exceptions import NoSuchElementException;


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");
obj1 = tdklib.TDKScriptingLibrary("tdkbtr181","RDKB");


#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WEBUI_WAN_AddBlockedSites');
obj1.configureTestCase(ip,port,'E2E_WEBUI_WAN_AddBlockedSites');
count = 0;
delete_status = "FAILURE"

popup_message = "Invalid Inputs!"

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 =obj1.getLoadModuleResult();

print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus1) ;


if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
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
                tdkTestObj = obj1.createTestStep('TDKB_TR181Stub_Get');
                tdkTestObj.addParameter("ParamName","Device.X_Comcast_com_ParentalControl.ManagedSites.Enable");
                expectedresult="SUCCESS";

                #Execute the test case in DUT
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                siteEnable = tdkTestObj.getResultDetails();

                if expectedresult in actualresult:
                    #Set the result status of execution
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the enable status of managed site");
                    print("ACTUAL RESULT 3: Managed site Enable status is %s" %siteEnable);
                    #Get the result of execution
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    #Set Selenium grid
                    driver,status = startSeleniumGrid(tdkTestObj,"WAN",tdkbE2EUtility.mso_grid_url,"MSOLogin");
                    if status == "SUCCESS":
                        try:
                            # To click on the Parental control
                            driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a').click()
                            time.sleep(5);
                            #To enable managed sites
                            driver.find_element_by_xpath('//*[@id="managed-sites-switch"]/a[1]/li/label').click()
                            time.sleep(4)
                            #Check if sites are present already or not
                            try:
                                site = driver.find_element_by_xpath('//*[@id="managed-sites-items"]/div[1]/table/tbody/tr[2]/td[2]').text
                                driver.refresh();
                                time.sleep(5);
                                print("Site is available in blocked site table")
                                try:
                                    #To click on Add blocked site
                                    driver.find_element_by_css_selector("#add_blocked_site").click()
                                    time.sleep(4)
                                    new_case = site.replace("http://","").upper();
                                    driver.find_element_by_id("url").send_keys(new_case)
                                    time.sleep(3);
                                    driver.find_element_by_xpath('//*[@id="pageForm"]/div/div/div[4]/input[1]').click()
                                    time.sleep(10);
                                    #Check if popup comes after adding same site with different case
                                    try:
                                        text = driver.find_element_by_xpath('//*[@id="popup_message"]').text
                                        if text == popup_message:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("TEST STEP 4: Check if it allows same site to be blocked with different case")
                                            print("ACTUAL RESULT 4: It does not allow same site to be blocked with different case");
                                            print("[TEST EXECUTION RESULT] : SUCCESS");
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP 4: Check if it allows same site to be blocked with different case")
                                            print("ACTUAL RESULT 4: It allows same site to be blocked with different case");
                                            print("[TEST EXECUTION RESULT] : FAILURE");
                                    except NoSuchElementException:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("FAILURE:It allows same site to be blocked with different case");
                                        elem = driver.find_elements_by_xpath('//*[@title="Delete Blocked Site"]')
                                        for x in elem:
                                            id = x.get_attribute("id")
                                            tdkTestObj = obj1.createTestStep("TDKB_TR181Stub_Get");
                                            tdkTestObj.addParameter("ParamName","Device.X_Comcast_com_ParentalControl.ManagedSites.BlockedSite.%s.Site" %id);
                                            tdkTestObj.executeTestCase(expectedresult);
                                            actualresult = tdkTestObj.getResult();
                                            details = tdkTestObj.getResultDetails().strip().replace("http://","");
                                            if new_case == details:
                                                inst = id;
                                                #Delete the added row
                                                tdkTestObj = obj1.createTestStep("TDKB_TR181Stub_DelObject");
                                                tdkTestObj.addParameter("paramName","Device.X_Comcast_com_ParentalControl.ManagedSites.BlockedSite.%s." %inst);
                                                expectedresult = "SUCCESS";
                                                tdkTestObj.executeTestCase(expectedresult);
                                                actualresult = tdkTestObj.getResult();
                                                details = tdkTestObj.getResultDetails();
                                                if expectedresult in actualresult:
                                                    #Set the result status of execution
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("TEST STEP : Deleting the added blocked site");
                                                    print("ACTUAL RESULT: %s" %details);
                                                    print("TEST EXECUTION RESULT : SUCCESS");
                                                else:
                                                    #Set the result status of execution
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("TEST STEP :Delete the added Blocked site");
                                                    print("ACTUAL RESULT :%s" %details);
                                                    print("TEST EXECUTION RESULT : FAILURE");
                                                delete_status = "SUCCESS"
                                                break;
                                        if delete_status != "SUCCESS":
                                            print("Instance does not match with blocked site")
                                            tdkTestObj.setResultStatus("FAILURE");
                                except Exception as error:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print(error);
                            except NoSuchElementException:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("No site available in blocked sites table")
                                driver.refresh();
                                #To click on Add blocked site
                                driver.find_element_by_css_selector("#add_blocked_site").click()
                                time.sleep(4)

                                blocked_site = tdkbE2EUtility.blocked_site
                                blocked_site = blocked_site.replace('"', '')

                                driver.find_element_by_id("url").send_keys(blocked_site)
                                time.sleep(3);
                                driver.find_element_by_xpath('//*[@id="pageForm"]/div/div/div[4]/input[1]').click()
                                time.sleep(10);
                                driver.find_element_by_css_selector("#add_blocked_site").click()
                                new_case = blocked_site.upper()
                                driver.find_element_by_id("url").send_keys(new_case)
                                time.sleep(3);
                                driver.find_element_by_xpath('//*[@id="pageForm"]/div/div/div[4]/input[1]').click()
                                time.sleep(10);
                                #Check if popup message is coming after adding same site with different case
                                try:
                                    text = driver.find_element_by_xpath('//*[@id="popup_message"]').text
                                    if text == popup_message:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("TEST STEP 3: Check if it allows same site to be blocked with different case")
                                        print("ACTUAL RESULT 3: It does not allow same site to be blocked with different case");
                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                        driver.find_element_by_xpath('//*[@id="popup_ok"]').click()
                                        driver.find_element_by_xpath('//*[@id="nav"]/ul/li[3]/a').click()
                                        elem = driver.find_element_by_xpath('//*[@title="Delete Blocked Site"]')
                                        inst = elem.get_attribute("id")
                                        #Delete the added row
                                        tdkTestObj = obj1.createTestStep("TDKB_TR181Stub_DelObject");
                                        tdkTestObj.addParameter("paramName","Device.X_Comcast_com_ParentalControl.ManagedSites.BlockedSite.%s." %inst);
                                        expectedresult = "SUCCESS";
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details = tdkTestObj.getResultDetails();
                                        if expectedresult in actualresult:
                                            #Set the result status of execution
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("TEST STEP : Deleting the added blocked site");
                                            print("ACTUAL RESULT: %s" %details);
                                            print("TEST EXECUTION RESULT : SUCCESS");
                                        else:
                                            #Set the result status of execution
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP :Delete the added Blocked site");
                                            print("ACTUAL RESULT :%s" %details);
                                            print("TEST EXECUTION RESULT : FAILURE") ;
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 3: Check if it allows same site to be blocked with different case")
                                        print("ACTUAL RESULT 3: It allows same site to be blocked with different case");
                                        print("[TEST EXECUTION RESULT] : FAILURE");
                                except NoSuchElementException:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("FAILURE:It allows same site to be blocked with different case");
                                    elem = driver.find_elements_by_xpath('//*[@title="Delete Blocked Site"]')
                                    for x in elem:
                                        id = x.get_attribute("id")
                                        tdkTestObj = obj1.createTestStep("TDKB_TR181Stub_Get");
                                        tdkTestObj.addParameter("ParamName","Device.X_Comcast_com_ParentalControl.ManagedSites.BlockedSite.%s.Site" %id);
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details = tdkTestObj.getResultDetails().strip().replace("http://","");
                                        if new_case == details or blocked_site == details:
                                            count = count + 1;
                                            inst = id;
                                            #Delete the added row
                                            tdkTestObj = obj1.createTestStep("TDKB_TR181Stub_DelObject");
                                            tdkTestObj.addParameter("paramName","Device.X_Comcast_com_ParentalControl.ManagedSites.BlockedSite.%s." %inst);
                                            expectedresult = "SUCCESS";
                                            tdkTestObj.executeTestCase(expectedresult);
                                            actualresult = tdkTestObj.getResult();
                                            details = tdkTestObj.getResultDetails();
                                            if expectedresult in actualresult:
                                                #Set the result status of execution
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print("TEST STEP : Deleting the added blocked site");
                                                print("ACTUAL RESULT: %s" %details);
                                                print("TEST EXECUTION RESULT : SUCCESS");
                                            else:
                                                #Set the result status of execution
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP :Delete the added Blocked site");
                                                print("ACTUAL RESULT :%s" %details);
                                                print("TEST EXECUTION RESULT : FAILURE") ;
                                            if count == 2:
                                                delete_status = "SUCCESS"
                                                break;
                                    if delete_status == "FAILURE":
                                        print("Instance does not match with blocked site")
                                        tdkTestObj.setResultStatus("FAILURE");
                            tdkTestObj = obj1.createTestStep('TDKB_TR181Stub_Set');
                            tdkTestObj.addParameter("ParamName","Device.X_Comcast_com_ParentalControl.ManagedSites.Enable")
                            tdkTestObj.addParameter("ParamValue",siteEnable);
                            tdkTestObj.addParameter("Type","bool");

                            #Execute the test case in DUT
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            details = tdkTestObj.getResultDetails();

                            if expectedresult in actualresult:
                                #Set the result status of execution
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("TEST STEP :Revert the blocked site enable status ");
                                print("ACTUAL RESULT :%s" %details);
                                #Get the result of execution
                                print("[TEST EXECUTION RESULT] : SUCCESS");
                            else:
                                #Set the result status of execution
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP :Revert the blocked site enable status ");
                                print("ACTUAL RESULT :%s" %details);
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
                    status = tdkbWEBUIUtility.kill_hub_node("WAN")
                    if status == "SUCCESS":
                        print("TEST STEP 5:Executing Post-requisite")
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("Post-requisite success")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 5:Couldnt kill node and hub")
                else:
                    #Set the result status of execution
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the enable status of managed site");
                    print("ACTUAL RESULT 3:Failed to get Managed site Enable status");
                    #Get the result of execution
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2:Device is in bridge mode")
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