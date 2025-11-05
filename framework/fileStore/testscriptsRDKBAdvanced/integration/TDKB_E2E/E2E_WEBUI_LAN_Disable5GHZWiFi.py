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
  <name>E2E_WEBUI_LAN_Disable5GHZWiFi</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To disable 5GHZ wifi via GUI page and check if the broadcasting of 5GHZ SSID is stopped or not</synopsis>
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
  <box_type>BPI</box_type></box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_475</test_case_id>
    <test_objective>To disable 5GHZ wifi via GUI page and check if the broadcasting of 5GHZ SSID is stopped or not</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Import selenium module
3. Start selenium hub in TM machine
4. Start Node in lan client machine
5. Get the lan client IP
6. check if the lan client has the ip in dhcp range
7. Try to access the WEBUI of the gateway using selenium grid
8. Validate if the UI page is accessible or not
9. Disable 5GHZ wifi from UI
10. Check if 5GHZ SSID is broadcasting or not
11. Kill selenium hub and node
12.  unload module</automation_approch>
    <except_output>The 5GHZ SSID should not broadcast when the 5GHZ SSID is disabled from UI</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WEBUI_LAN_Disable5GHZWiFi</test_script>
    <skipped>No</skipped>
    <release_version>M64</release_version>
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
obj.configureTestCase(ip,port,'E2E_WEBUI_LAN_Disable5GHZWiFi');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

        wifiEnable = "Device.WiFi.SSID.%s.Enable" %tdkbE2EUtility.ssid_5ghz_index
        #Get the value of the wifi parameters that are currently set.
        paramList=[wifiEnable]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current wifienable status")
            print("EXPECTED RESULT 1: Should retrieve the current wifienable status")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            if orgValue[0] == "false":
                setValuesList = ['true'];
                print("WIFI parameter values that are set: %s" %setValuesList)
                setParamList = "%s|true|bool" %(wifiEnable)
                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP : Set the wifi enable status to true")
                    print("EXPECTED RESULT : Should set the wifi enable status to true");
                    print("ACTUAL RESULT : %s" %details);
                    print("[TEST EXECUTION RESULT] : SUCCESS");
                    #Retrieve the values after set and compare
                    newParamList=[wifiEnable]
                    tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TEST STEP : Get the current wifi enable status")
                        print("EXPECTED RESULT : Should retrieve the current wifi enable status")
                        print("ACTUAL RESULT : %s" %(newValues));
                        print("[TEST EXECUTION RESULT] : SUCCESS");

                        #Wait for the changes to reflect in client device
                        time.sleep(60);
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP : Failed to set the wifi enable status to true")
                        print("EXPECTED RESULT : Should retrieve the wifi enable status as true")
                        print("[TEST EXECUTION RESULT] : FAILURE");
                        obj.unloadModule("tdkb_e2e");
                        exit();

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
                        tdkTestObj.setResultStatus("SUCCESS");
                        #Set Selenium grid
                        driver,status = startSeleniumGrid(tdkTestObj,"LAN",tdkbE2EUtility.grid_url);
                        if status == "SUCCESS":
                            try:
                                time.sleep(10);
                                #To click on option "Connection" in UI
                                driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/ul/li[1]/ul/li[2]/a').click()
                                #To click on WiFi option under connection
                                driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/ul/li[1]/ul/li[2]/ul/li[4]/a").click()
                                time.sleep(10);
                                # To click on edit option for 5GHz wifi
                                driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div[2]/table/tbody/tr[3]/td[5]/a").click()
                                # To Disable 5Ghz WiFi
                                driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div[2]/form/div[1]/span[2]/ul/a[2]/li/label").click()
                                #To save the settings
                                driver.find_element_by_id("save_settings").submit()
                                time.sleep(10);
                                driver.quit();

                                #Check if 5GHz wifi broadcasting is stopped to validate the disabling of wifi
                                print("TEST STEP 5: Check if the SSID name is listed in wifi client")
                                status = wlanIsSSIDAvailable(tdkbE2EUtility.ssid_5ghz_name);
                                if expectedresult not in status:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("Network name",tdkbE2EUtility.ssid_5ghz_name,"is not broadcasted on the network");
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("Network name",tdkbE2EUtility.ssid_5ghz_name,"is broadcasted on the network");
                            except Exception as error:
                                tdkTestObj.setResultStatus("FAILURE");
                                print(error);
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

            #Prepare the list of parameter values to be reverted
            revertParamList = "%s|%s|bool" %(wifiEnable,orgValue[0])

            #Revert the values to original
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 6: Should set the original wifi enable status");
                print("ACTUAL RESULT 6: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 6: Should set the original wifi enable status");
                print("ACTUAL RESULT 6: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current wifi enable status")
            print("EXPECTED RESULT 1: Should retrieve the current wifi enable status")
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