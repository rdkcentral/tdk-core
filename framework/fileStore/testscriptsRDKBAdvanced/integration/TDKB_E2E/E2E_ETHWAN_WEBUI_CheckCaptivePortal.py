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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>1</version>
  <name>E2E_ETHWAN_WEBUI_CheckCaptivePortal</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Captive Portal page must be available in ethwan mode</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>true</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Broadband</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_525</test_case_id>
    <test_objective>Captive Portal page must be available in ethwan mode</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband</test_setup>
    <pre_requisite>1. The broadband device should be in ETHWAN setup
2. The EthWAN mode should be enabled
3. TDK Agent must be up and running
4. Lan client should be connected to the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.Ethernet.X_RDKCENTRAL-COM_WAN.Enabled</input_parameters>
    <automation_approch>1. Load module
2. Check if ethwan mode is enabled or not
3. If enabled get and save values of ssid name and password of 2.4Ghz and 5ghz
4. Factory reset the device
5. Start selenium hub and node to access webui
6. Check if the Captive portal page displayed
7. Set new ssid and passwords
8. Revert all values
9. Unload module
</automation_approch>
    <except_output>Captive Portal page must be available in ethwan mode</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_ETHWAN_WEBUI_CheckCaptivePortal</test_script>
    <skipped>No</skipped>
    <release_version>M68</release_version>
    <remarks>LAN</remarks>
  </test_cases>
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
pamobj = tdklib.TDKScriptingLibrary("pam","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WEBUI_LAN_ConfigCaptivePortal');
pamobj.configureTestCase(ip,port,'E2E_WEBUI_LAN_ConfigCaptivePortal');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
pamloadmodulestatus =pamobj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;
print("[LIB LOAD STATUS]  :  %s" %pamloadmodulestatus) ;

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in pamloadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    pamobj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

        ethwanMode = "Device.Ethernet.X_RDKCENTRAL-COM_WAN.Enabled"
        ssidName_2g = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
        keyPassPhrase_2g = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
        ssidName_5g = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_5ghz_index
        keyPassPhrase_5g = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_5ghz_index

        paramList = [ethwanMode,ssidName_2g,keyPassPhrase_2g,ssidName_5g,keyPassPhrase_5g]
        #Get the value of the parameters that are currently set.
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status and  orgValue[0] == "true":
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current ethwan status, ssid name and password of 2.4GHz and 5GHz");
            print("EXPECTED RESULT 1: Should retrieve the current ethwan status as true")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            #Initiate factory reset to get the captive portal page
            #save device's current state before it goes for reboot
            obj.saveCurrentState();

            #Initiate Factory reset before checking the default value
            tdkTestObj = pamobj.createTestStep('pam_Setparams');
            tdkTestObj.addParameter("ParamName","Device.X_CISCO_COM_DeviceControl.FactoryReset");
            tdkTestObj.addParameter("ParamValue","Router,Wifi,VoIP,Dect,MoCA");
            tdkTestObj.addParameter("Type","string");
            expectedresult="SUCCESS";
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();

            if expectedresult in actualresult:
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Initiate factory reset ");
                print("EXPECTED RESULT 2: Should inititate factory reset");
                print("ACTUAL RESULT 2: %s" %details);
                #Get the result of execution
                print("[TEST EXECUTION RESULT] : SUCCESS");

                #Restore the device state saved before reboot
                obj.restorePreviousStateAfterReboot();
                time.sleep(160)

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
                            driver,status = startSeleniumGrid(tdkTestObj,"LAN",tdkbE2EUtility.grid_url,"CaptivePortal");
                            if status == "SUCCESS":
                                try:
                                    #configure wifi settings for 2.4ghz
                                    driver.find_element_by_xpath('//*[@id="get_set_up"]').click()
                                    driver.find_element_by_id("WiFi_Name").send_keys("ssid_2g")
                                    driver.find_element_by_id("WiFi_Password").send_keys("password_2g")
                                    driver.find_element_by_xpath('//*[@id="button_next"]').click()
                                    driver.find_element_by_xpath('//*[@id="button_next_01"]').click()
                                    time.sleep(100);
                                    text = driver.find_element_by_css_selector('#ready > h1:nth-child(1)').text
                                    if text == "Your Wi-Fi is Ready":
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("Successfully configured the captive portal page")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("Failed to configure the captive portal page")
                                except Exception as error:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print(error);
                                #Revert the SSID name and passwords
                                list1 = [ssidName_2g,orgValue[1],'string']
                                list2 = [keyPassPhrase_2g,orgValue[2],'string']
                                list3 = [ssidName_5g,orgValue[3],'string']
                                list4 = [keyPassPhrase_5g,orgValue[4],'string']

                                #Concatenate the lists with the elements separated by pipe
                                revertParamList = list1 + list2 + list3 + list4
                                revertParamList = "|".join(map(str, revertParamList))

                                #Revert the values to original
                                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
                                if expectedresult in actualresult:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("EXPECTED RESULT 6: Should set the original ssid,keypassphrase,2ghz and 5ghz Radio enable status");
                                    print("ACTUAL RESULT 6: %s" %details);
                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    details = tdkTestObj.getResultDetails();
                                    print("EXPECTED RESULT 6: Should set the original ssid,keypassphrase,2ghz and 5ghz Radio enable status");
                                    print("ACTUAL RESULT 6: %s" %details);
                                    print("[TEST EXECUTION RESULT] : FAILURE");

                                driver.quit();
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
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Initiate factory reset ");
                print("EXPECTED RESULT 2: Should inititate factory reset");
                print("ACTUAL RESULT 2: %s" %details);
                #Get the result of execution
                print("[TEST EXECUTION RESULT] : FAILURE");
            #Revert the login password to previous value
            changeAdminPassword(pamobj,tdkbE2EUtility.ui_password);
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current ethwan status,ssid and password of 2.4GHz and 5GHz")
            print("EXPECTED RESULT 1: Should retrieve the current ethwan status as true")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        obj.setLoadModuleStatus("FAILURE");
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup();
    obj.unloadModule("tdkb_e2e");
    pamobj.unloadModule("pam");

else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");