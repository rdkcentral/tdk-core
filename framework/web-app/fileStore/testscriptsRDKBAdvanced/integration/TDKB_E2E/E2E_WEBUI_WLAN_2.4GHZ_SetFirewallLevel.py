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
  <name>E2E_WEBUI_WLAN_2.4GHZ_SetFirewallLevel</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To get the firewall level and set it to a different value. Check if the change is reflecting in the UI page from WLAN Client</synopsis>
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
    <test_case_id>TC_TDKB_E2E_466</test_case_id>
    <test_objective>To get the firewall level and set it to a different value. Check if the change is reflecting in the UI page from WLAN Client</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. import selenium module
3. Change the value of firewall level through dmcli
4. Start selenium hub in TM machine
5. Start Node in lan client machine
6. Connect wlan client
7. Try to access the WEBUI of the gateway using selenium grid
8. Validate if the UI page is accessible or not
9. Get the value of firewall level from UI page
10. Verify if the change in firewall value reflects in UI
11. Kill selenium hub and node
12. unload module</automation_approch>
    <except_output>The changed firewall value must reflect in the UI page</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_WEBUI_WLAN_2.4GHZ_SetFirewallLevel</test_script>
    <skipped>No</skipped>
    <release_version>M64</release_version>
    <remarks>WLAN</remarks>
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
obj.configureTestCase(ip,port,'E2E_WEBUI_WLAN_2.4GHZ_SetFirewallLevel');

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

        #Assign the WIFI parameters names to a variable
        ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
        keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
        firewall = "Device.X_CISCO_COM_Security.Firewall.FirewallLevel"

        #Get the value of the wifi parameters that are currently set.
        paramList=[ssidName,keyPassPhrase,firewall]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current ssid and keypassphrase and firewall level")
            print("EXPECTED RESULT 1: Should retrieve the current ssid and keypassphrase and firewall level")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            if orgValue[2] == "Low":
                firewallValue = "Medium"
            else:
                firewallValue = "Low"

            # Set securityMode for 2ghz"
            setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,firewallValue];
            print("WIFI parameter values that are set: %s" %setValuesList)

            list1 = [ssidName,tdkbE2EUtility.ssid_2ghz_name,'string']
            list2 = [keyPassPhrase,tdkbE2EUtility.ssid_2ghz_pwd,'string']

            #Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2
            setParamList = "|".join(map(str, setParamList))

            firewallParam = "%s|%s|string" %(firewall,firewallValue)

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
            tdkTestObj,firewallResult,details = setMultipleParameterValues(obj,firewallParam)
            if expectedresult in actualresult and expectedresult in firewallResult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set the ssid and keypassphrase and firewall level")
                print("EXPECTED RESULT 2: Should set the ssid and keypassphrase and firewall level");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");

                #Retrieve the values after set and compare
                newParamList=[ssidName,keyPassPhrase,firewall]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current ssid and keypassphrase and firewall")
                    print("EXPECTED RESULT 3: Should retrieve the current ssid and keypassphrase and firewall")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    #Wait for the changes to reflect in client device
                    time.sleep(60);

                    #Set Selenium grid
                    driver,status = startSeleniumGrid(tdkTestObj,"WLAN",tdkbE2EUtility.grid_url);
                    if status == "SUCCESS":

                        #Connect to the wifi ssid from wlan client
                        print("TEST STEP 4: From wlan client, Connect to the wifi ssid")
                        status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.wlan_2ghz_interface);
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS");

                            print("TEST STEP 5: Get the IP address of the wlan client after connecting to wifi")
                            wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_2ghz_interface);
                            if wlanIP:
                                tdkTestObj.setResultStatus("SUCCESS");

                                print("TEST STEP 6: Get the current LAN IP address DHCP range")
                                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                                print("LAN IP Address: %s" %curIPAddress);

                                if expectedresult in status and curIPAddress:
                                    tdkTestObj.setResultStatus("SUCCESS");

                                    print("TEST STEP 7: Check whether wlan ip address is in same DHCP range")
                                    status = "SUCCESS"
                                    status = checkIpRange(curIPAddress,wlanIP);
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        status,driver = openLocalWebUI(tdkbE2EUtility.grid_url,tdkTestObj,"LocalLogin");
                                        if status == "SUCCESS":
                                            try:
                                                time.sleep(20);
                                                firewallText = driver.find_element_by_css_selector("div.form-row:nth-child(5) > span:nth-child(2)").text
                                                print(firewallText);
                                                if firewallText == firewallValue:
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("Firewall level is ", firewallText, "and is validated through dmcli output")
                                                    finalStatus = "SUCCESS"
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("Failed to get the firewall same as the dmcli output")
                                            except Exception as error:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print(error);
                                            time.sleep(10);
                                            driver.quit();
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("checkIpRange:wlan ip address is not in DHCP range")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("getParameterValue : Failed to get gateway lan ip")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("getWlanIPAddress:Failed to get the wlan ip address")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("wlanConnectWifiSsid: Failed to connect to the wifi ssid")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("Failed to set the selenium grid")
                    #Kill selenium hub and node
                    status = tdkbWEBUIUtility.kill_hub_node("WLAN")
                    if status == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("Post-requisite success")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("Couldnt kill node and hub")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current ssid and keypassphrase")
                    print("EXPECTED RESULT 3: Should retrieve the current ssid and keypassphrase")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Set the ssid and keypassphrase")
                print("EXPECTED RESULT 2: Should set the ssid and keypassphrase");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");

            #Prepare the list of parameter values to be reverted
            list1 = [ssidName,orgValue[0],'string']
            list2 = [keyPassPhrase,orgValue[1],'string']

            #Concatenate the lists with the elements separated by pipe
            revertParamList = list1 + list2
            revertParamList = "|".join(map(str, revertParamList))

            firewallParam = "%s|%s|string" %(firewall,orgValue[2])
            #Revert the values to original
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
            tdkTestObj,firewallResult,details = setMultipleParameterValues(obj,firewallParam)
            if expectedresult in actualresult and expectedresult in firewallResult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 8: Should set the original ssid and keypassphrase and firewall level");
                print("ACTUAL RESULT 8: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 8: Should set the original ssid and keypassphrase and firewall level");
                print("ACTUAL RESULT 8: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current ssid and keypassphrase and firewall level")
            print("EXPECTED RESULT 1: Should retrieve the current ssid and keypassphrase and firewall level")
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