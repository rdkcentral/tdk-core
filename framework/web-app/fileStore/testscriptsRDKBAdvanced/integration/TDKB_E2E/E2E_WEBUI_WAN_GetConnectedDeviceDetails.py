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
  <version>24</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_WEBUI_WAN_GetConnectedDeviceDetails</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The details of connected devices should be displayed on MSO UI page</synopsis>
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
    <test_case_id>TC_TDKB_E2E_516</test_case_id>
    <test_objective>The details of connected devices should be displayed on MSO UI page</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. import selenium module
3. Start selenium hub in TM machine
4. Start Node in wan client machine
5. Try to access the WEBUI of the gateway using selenium grid
6.Check if the details of connected devices are displayed or not
7. Kill selenium hub and node
8. unload module</automation_approch>
    <expected_output>The details of connected clients should display in MSO UI page</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WEBUI_WAN_GetConnectedDeviceDetails</test_script>
    <skipped>No</skipped>
    <release_version>M67</release_version>
    <remarks></remarks>
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
obj.configureTestCase(ip,port,'E2E_WEBUI_WAN_GetConnectedDeviceDetails');

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

        NoOfClientsConnected = "Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber"
        tdkTestObj,status,orgValue = getParameterValue(obj,NoOfClientsConnected)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the no of clients connected");
            print("EXPECTED RESULT 1: Should retrieve the no of clients connected")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");
            #Check if any clients are connected
            if int(orgValue) >= 0:
                print("No of clients connected to the device is ",orgValue)
                #Set Selenium grid
                driver,status = startSeleniumGrid(tdkTestObj,"WAN",tdkbE2EUtility.mso_grid_url,"MSOLogin");
                if status == "SUCCESS":
                    try:
                        # To click on the Connected Device
                        driver.find_element_by_id('conndev').click()
                        time.sleep(10);
                        # To click on the connected Client Device
                        driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div[3]/table/tbody/tr[2]/td[1]/a/u").click()
                        time.sleep(10);
                        # To Capture the complete connected device details
                        connected_dev_details=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div[3]/table/tbody/tr[2]/td[1]/div/dl").text

                        if  connected_dev_details != "":
                            ipvadd = connected_dev_details.split("\n")[1]
                            mac = connected_dev_details.split("\n")[3]
                            print("The IPV4 address is %s" %ipvadd);
                            print("The MAC address is %s" %mac);

                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("The client device details are not displayed in UI page")
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
                    print("TEST STEP 2:Executing Post-requisite")
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("Post-requisite success")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 2:Couldnt kill node and hub")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP :No clients connected to gateway");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the no of clients connected");
            print("EXPECTED RESULT 1: Should retrieve the no of clients connected")
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