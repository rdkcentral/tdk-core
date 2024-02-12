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
  <name>E2E_WEBUI_WAN_CheckPublicWiFiSecurityMode</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if the security mode of public wifi network is open for both 2.4Ghz and 5Ghz</synopsis>
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
    <test_case_id>TC_TDKB_E2E_528</test_case_id>
    <test_objective>To check if the security mode of public wifi network is open for both 2.4Ghz and 5Ghz</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. import selenium module
3. Get the lan mode and check if the device is in router mode
4.Enable public wifi
4. Start selenium hub in TM machine
5. Start Node in wan client machine
6. Try to access the WEBUI of the gateway using selenium grid
7. Navigate to Connection and navigate to WiFi option
8.Check if the security mode of public wifi network is open for both 2.4Ghz and 5Ghz
9. Kill selenium hub and node
10. unload module</automation_approch>
    <expected_output>security mode of public wifi network should be open for both 2.4Ghz and 5Ghz</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WEBUI_WAN_CheckPublicWiFiSecurityMode</test_script>
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


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");


#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WEBUI_WAN_CheckPublicWiFiSecurityMode');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();


print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus);


if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");

    #Get current values of public wifi params
    expectedresult="SUCCESS";
    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")
        tdkTestObj,actualresult,orgValue = getPublicWiFiParamValues(obj);
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1:Get values of PublicWiFi params")
            print("ACTUAL RESULT 1:%s" %orgValue)
            print("[TEST EXECUTION RESULT] : SUCCESS");

            #Set values to enable public wifi
            setvalues = [tdkbE2EUtility.dscpmarkpolicy,tdkbE2EUtility.primary_remote_end_point,tdkbE2EUtility.secondary_remote_end_point,tdkbE2EUtility.ssid_2ghz_public_name,tdkbE2EUtility.ssid_5ghz_public_name,"true","true","true"];
            tdkTestObj, actualresult, details = setPublicWiFiParamValues(obj,setvalues);
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Enable public wifi")
                print("ACTUAL RESULT 2:%s" %details)
                print("[TEST EXECUTION RESULT] : SUCCESS");

                #Set Selenium grid
                driver,status = startSeleniumGrid(tdkTestObj,"WAN",tdkbE2EUtility.mso_grid_url,"MSOLogin");
                if status == "SUCCESS":
                    try:
                        # To click on the Connection option
                        driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/ul/li[1]/ul/li[2]/a").click()
                        # To click on WiFi option
                        driver.find_element_by_xpath('//*[@id="nav"]/ul/li[1]/ul/li[2]/ul/li[4]/a').click()
                        time.sleep(10);
                        public_wifi1 = driver.find_element_by_xpath('//*[@id="public_wifi"]/tbody/tr[2]/td[4]').text
                        public_wifi2 = driver.find_element_by_xpath('//*[@id="public_wifi"]/tbody/tr[2]/td[4]').text
                        if "Open" in public_wifi1:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("TEST STEP 3:Should get the 2.4GHZ Public WiFiSecurity Mode as open")
                            print("ACTUAL RESULT 3: %s" %public_wifi1);
                            print("[TEST EXECUTION RESULT] : SUCCESS");
                            if "Open" in public_wifi2:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("TEST STEP 4:Should get the 5GHZ Public WiFiSecurity Mode as open")
                                print("ACTUAL RESULT 4: %s" %public_wifi2);
                                print("[TEST EXECUTION RESULT] : SUCCESS");
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 4:Should get the 5GHZ Public WiFiSecurity Mode as open")
                                print("ACTUAL RESULT 4: %s" %public_wifi2);
                                print("[TEST EXECUTION RESULT] : FAILURE");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("TEST STEP 3:Should get the 2.4GHZ Public WiFiSecurity Mode as open")
                            print("ACTUAL RESULT 3: %s" %public_wifi1);
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
                #Revert the values of public wifi params
                tdkTestObj, actualresult, details = setPublicWiFiParamValues(obj,orgValue);
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP :Revert the PublicWiFi param values")
                    print("ACTUAL RESULT :%s" %details)
                    print("[TEST EXECUTION RESULT] : SUCCESS");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP :Revert the PublicWiFi param values")
                    print("ACTUAL RESULT :%s" %details)
                    print("[TEST EXECUTION RESULT] : FAILURE");

            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Enable public wifi")
                print("ACTUAL RESULT 2:%s" %details)
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1:Get values of PublicWiFi params")
            print("ACTUAL RESULT 1:Failed to get values of PublicWiFi params")
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