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
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_ETHAGENT_WEBUI_WAN_GetConnectedDeviceDetails</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To disconnect and connect lan client and check if it is updated in WEBUI under connected devices</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>20</execution_time>
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
    <test_case_id>TC_TDKB_E2E_519</test_case_id>
    <test_objective>To disconnect and connect lan client and check if it is updated in WEBUI under connected devices</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,RPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. import selenium module
3. Get the connected device number
4. Check if connected device number is greater than 0
5. Get the connected client host name from configuration file.
6. Check if it is under online devices in WEBUI
7. Bring down the lan interface
8. Check if it is listed under offline devices in WEBUI
9. unload module</automation_approch>
    <except_output>After disconnecting and connecting lan client, it should be updated in WEBUI under connected devices</except_output>
    <priority>High</priority>
    <test_stub_interface>None</test_stub_interface>
    <test_script>E2E_ETHAGENT_WEBUI_WAN_GetConnectedDeviceDetails</test_script>
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
from selenium import webdriver;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");
obj1 = tdklib.TDKScriptingLibrary("tdkbtr181","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_ETHAGENT_WEBUI_WAN_GetConnectedDeviceDetails');
obj1.configureTestCase(ip,port,'E2E_ETHAGENT_WEBUI_WAN_GetConnectedDeviceDetails');

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

        NoOfClientsConnected = "Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber"
        tdkTestObj,status,orgValue = getParameterValue(obj,NoOfClientsConnected)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the no of clients connected");
            print("EXPECTED RESULT 1: Should retrieve the no of clients connected")
            print("ACTUAL RESULT 1: No of clients connected:%s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");
            #Check if any clients are connected
            if int(orgValue) > 0:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2:Check if there are clients connected to device")
                print("EXPECTED RESULT 2: Clients should be connected")
                print("ACTUAL RESULT 2:clients are connected");
                print("[TEST EXECUTION RESULT] : SUCCESS");
                connectedHostname = tdkbE2EUtility.connected_lan_hostname
                print("ConnectedHostname is %s" %connectedHostname)
                #Set Selenium grid
                driver,status = startSeleniumGrid(tdkTestObj,"WAN",tdkbE2EUtility.mso_grid_url,"MSOLogin");
                if status == "SUCCESS":
                    try:
                        driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/ul/li[2]/a").click()
                        table = driver.find_element_by_xpath("//*[@id='online-private']/table")
                        test_row = driver.find_elements_by_xpath("//div[@id='online-private']/table[1]/tbody[1]/tr")
                        test_col = driver.find_elements_by_xpath("//div[@id='online-private']/table[1]/tbody[1]/tr[2]/td")
                        noOfRows = len(test_row)+1
                        noOfColumns = len(test_col)
                        allData = [];
                        for i in range(2, noOfRows):
                            ro = [];
                            for j in range(1, noOfColumns) :
                                ro.append(table.find_element_by_xpath("//tr["+str(i)+"]/td["+str(j)+"]").text);
                            allData.append(ro);
                            print("Entries of table are %s" %allData)
                            rowdata = allData[0]
                            onlineDevice = rowdata[0]
                            print("Online device from UI is %s" %onlineDevice)
                            if connectedHostname == onlineDevice:
                                #Set the result status of execution
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("TEST STEP 3:Check if connected host name and online device from UI are same");
                                print("EXPECTED RESULT 3 : Connected host name and online device from UI should be same")
                                print("ACTUAL RESULT 3:Connected host name and online device from UI are same")
                                #Get the result of execution
                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                print("Disconnect the lan client")
                                status= bringdownInterface(tdkbE2EUtility.lan_interface,"LAN");
                                if status == "SUCCESS":
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("TEST STEP 4: Check if lan client is disconnected");
                                    print("EXPECTED RESULT 4 : LAN client should be disconnected")
                                    print("ACTUAL RESULT 4:LAN client is disconnected")
                                    #Get the result of execution
                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                    print("Waiting to reflect the changes in UI")
                                    time.sleep(500);
                                    driver.refresh();
                                    print("Get the offline device from UI")
                                    offlineDevice=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div[4]/table/tbody/tr[2]/td[1]/a/u").text
                                    if connectedHostname == offlineDevice:
                                        #Set the result status of execution
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("TEST STEP 5:Check whether disconnected lan client is under offline device");
                                        print("EXPECTED RESULT 5: Offline device from UI and  host name should be same")
                                        print("ACTUAL RESULT 5:Offline device from UI and connected host name are same")
                                        #Get the result of execution
                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                    else:
                                        #Set the result status of execution
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 5:Check whether disconnected lan client is under offline device");
                                        print("EXPECTED RESULT 5: Offline device from UI and connected host name should be same")
                                        print("ACTUAL RESULT 5:Offline device from UI and connected host name are not same")
                                        #Get the result of execution
                                        print("[TEST EXECUTION RESULT] : FAILURE");
                                    status= bringupInterface(tdkbE2EUtility.lan_interface,"LAN");
                                    if status == "SUCCESS":
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("TEST STEP 6: Revert the changes by bringing up the interface");
                                        print("EXPECTED RESULT 6 : LAN client should be brought up")
                                        print("ACTUAL RESULT 6:LAN client is brought up")
                                        #Get the result of execution
                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                        print("Waiting to reflect the changes")
                                        time.sleep(100);
                                        break;
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 6:Revert the changes by bringing up the interface");
                                        print("EXPECTED RESULT 6: LAN client should be brought up")
                                        print("ACTUAL RESULT 6 :Failed to revert the changes")
                                        #Get the result of execution
                                        print("[TEST EXECUTION RESULT] : FAILURE");
                                        break;
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 4: Check if lan client is disconnected");
                                    print("EXPECTED RESULT 4 : LAN client should be disconnected")
                                    print("ACTUAL RESULT 4 :LAN client is not disconnected")
                                    #Get the result of execution
                                    print("[TEST EXECUTION RESULT] : FAILURE");
                            else:
                                #Set the result status of execution
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 3:Check if connected host name and online device from UI are same");
                                print("EXPECTED RESULT 3 : Connected host name and online device from UI should be same")
                                print("ACTUAL RESULT 3:Connected host name and online device from UI are not same")
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
                    print("TEST STEP 7:Executing Post-requisite")
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("Post-requisite success")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 7:Couldnt kill node and hub")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2:No clients connected to gateway");
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
    obj1.unloadModule("tdkbtr181");
else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");