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
<?xml version="1.0" encoding="UTF-8"?>
<xml>
  <id/>
  <version>1</version>
  <name>E2E_WEBUI_LAN_ConfigCaptivePortal</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>After doing factory reset verify that Captive Portal page is displaying on taking webui. Also ensure that client is able to connect to the wifi ssids and access internet with configured ssid name and password.</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>true</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Broadband</box_type>
    <box_type>Emulator</box_type>
    <box_type>RPI</box_type>
  <box_type>BPI</box_type></box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_485</test_case_id>
    <test_objective>After doing factory reset verify that Captive Portal page is displaying on taking webui. Also ensure that client is able to connect to the wifi ssids and access internet with configured ssid name and password.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.DeviceInfo.X_RDKCENTRAL-COM_CaptivePortalEnable
Device.WiFi.SSID.{i}.SSID
Device.WiFi.AccessPoint.{i}.Security.KeyPassphrase</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. import selenium module
3.Get and save ssid name and password for 2.4GHz and 5GHz
4.Check if Captive portal status is enabled. If not enabled, enable it
5. check if the lan client has the ip in dhcp range
6. Start selenium hub in TM machine
7. Start Node in lan client machine
8. Try to access the WEBUI of the gateway using selenium grid and verify if it is the captive portal page
9. Configure the wifi ssid and password from UI
10. Connect to ssid with new credentials
11. Check if internet is accessible from wlan client
12. Disconnect wifi ssid
13. Kill selenium hub and node
14. unload module</automation_approch>
    <except_output>Should display the captive portal page after factory reset and should be able to configure the ssid name and password from UI. Wifi client should be able to access internet once it is connected with new credentials</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_2e</test_stub_interface>
    <test_script>E2E_WEBUI_LAN_ConfigCaptivePortal</test_script>
    <skipped>No</skipped>
    <release_version>M64</release_version>
    <remarks>LAN,WLAN</remarks>
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
    finalStatus = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

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
            print("TEST STEP 1: Initiate factory reset ");
            print("EXPECTED RESULT 1: Should inititate factory reset");
            print("ACTUAL RESULT 1: %s" %details);
            #Get the result of execution
            print("[TEST EXECUTION RESULT] : SUCCESS");

            #Restore the device state saved before reboot
            obj.restorePreviousStateAfterReboot();
            time.sleep(160)
            captivePortalStatus = "Device.DeviceInfo.X_RDKCENTRAL-COM_CaptivePortalEnable"
            ssidName_2g = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
            keyPassPhrase_2g = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
            ssidName_5g = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_5ghz_index
            keyPassPhrase_5g = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_5ghz_index
            #Get the value of the wifi parameters that are currently set.
            paramList=[captivePortalStatus,ssidName_2g,keyPassPhrase_2g,ssidName_5g,keyPassPhrase_5g]
            tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

            if expectedresult in status:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Get the current captive portal status,ssid name and password for 2GHz and 5GHz");
                print("EXPECTED RESULT 2: Should retrieve the current captive portal status,ssid name and password for 2GHz and 5GHz")
                print("ACTUAL RESULT 2: %s" %orgValue);
                print("[TEST EXECUTION RESULT] : SUCCESS");

                if orgValue[0] != "True":
                    #Enable captive portal
                    enableParam = "%s|true|bool" %captivePortalStatus
                    tdkTestObj,enableResult,details = setMultipleParameterValues(obj,enableParam)
                    if expectedresult in enableResult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TEST STEP : Enable Captive Portal")
                        print("EXPECTED RESULT : Should enable Captive Portal");
                        print("ACTUAL RESULT : %s" %details);
                        print("[TEST EXECUTION RESULT] : SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP : Enable Captive Portal")
                        print("EXPECTED RESULT : Should enable Captive Portal");
                        print("ACTUAL RESULT : %s" %details);
                        print("[TEST EXECUTION RESULT] : FAILURE");
                        obj.unloadModule("tdkb_e2e");
                        pamobj.unloadModule("pam");
                        exit()

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
                                        #Connect to the ssids with new credentials
                                        print("TEST STEP 6: From wlan client, Connect to the wifi ssid")
                                        status = wlanConnectWifiSsid("ssid_2g","password_2g",tdkbE2EUtility.wlan_2ghz_interface);
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS");

                                            print("TEST STEP 7: Get the IP address of the wlan client after connecting to wifi")
                                            wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_2ghz_interface);
                                            if wlanIP:
                                                tdkTestObj.setResultStatus("SUCCESS");

                                                print("TEST STEP 8: Check whether wlan ip address is in same DHCP range")
                                                status = "SUCCESS"
                                                status = checkIpRange(curIPAddress,wlanIP);
                                                if expectedresult in status:
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    status = verifyNetworkConnectivity(tdkbE2EUtility.network_ip, "PING", wlanIP,curIPAddress)
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print("verifyNetworkConnectivity: SUCCESS")

                                                        print("TEST STEP 9: From wlan client, Disconnect from the wifi ssid")
                                                        status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_2ghz_interface);
                                                        if expectedresult in status:
                                                            tdkTestObj.setResultStatus("SUCCESS");
                                                            finalStatus = "SUCCESS";
                                                            print("wlanDisconnectWifiSsid: SUCCESS")
                                                        else:
                                                            tdkTestObj.setResultStatus("FAILURE");
                                                            print("wlanDisconnectWifiSsid: FAILURE")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("verifyNetworkConnectivity: FAILURE")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("wlan IP for 2.4GHz is not in the expected range")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("Failed to get the wlanIP for 2.4GHz")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("Failed to connect to 2.4GHz SSID")
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
                                if expectedresult in actualresult and expectedresult in finalStatus:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("EXPECTED RESULT 10: Should set the original ssid,keypassphrase,2ghz and 5ghz Radio enable status");
                                    print("ACTUAL RESULT 10: %s" %details);
                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    details = tdkTestObj.getResultDetails();
                                    print("EXPECTED RESULT 10: Should set the original ssid,keypassphrase,2ghz and 5ghz Radio enable status");
                                    print("ACTUAL RESULT 10: %s" %details);
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
                print("TEST STEP 2: Get the current captive portal status,ssid name and password for 2GHz and 5GHz");
                print("EXPECTED RESULT 2: Should retrieve the current captive portal status,ssid name and password for 2GHz and 5GHz")
                print("ACTUAL RESULT 2: %s" %orgValue);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Initiate factory reset ");
            print("EXPECTED RESULT 1: Should inititate factory reset");
            print("ACTUAL RESULT 1: %s" %details);
            #Get the result of execution
            print("[TEST EXECUTION RESULT] : FAILURE");
        #Revert the login password to previous value
        changeAdminPassword(pamobj,tdkbE2EUtility.ui_password);
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