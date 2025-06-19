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
  <name>E2E_ParentalControl_ManagedSites_5GHZ_Block_WebsiteURL</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Verify that WG supports blocking of websites using url (www.google.com) for Wi-Fi client associated using 5GHZ radio through Parental control (managed sites)</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
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
    <test_case_id>TC_TDKB_E2E_117</test_case_id>
    <test_objective>Verify that WG supports blocking of websites using url (www.google.com) for Wi-Fi client associated using 5GHZ radio through Parental control (managed sites)</test_objective>
    <test_type>Negative</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.2.SSID
Device.WiFi.AccessPoint.2.Security.KeyPassphrase
Device.X_Comcast_com_ParentalControl.ManagedSites.Enable
Device.X_Comcast_com_ParentalControl.ManagedSites.BlockedSite.
Device.WiFi.AccessPoint.2.Security.ModeEnabled</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save managedSiteEnable and securityMode
3. Enable managed sites and set WPA2PSK as security mode
4.Add new rule to Device.X_Comcast_com_ParentalControl.ManagedSites.BlockedSite.
5. Set values to all fields in new rule
6.Check whether the WLAN client is able to access the url using wget
7.Delete the added rule and revert all params values
8.Unload tdkb_e2e module</automation_approch>
    <except_output>The Client should not access the blocked URL</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_ParentalControl_ManagedSites_5GHZ_Block_WebsiteURL</test_script>
    <skipped>No</skipped>
    <release_version>M57</release_version>
    <remarks>WLAN</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import tdkbE2EUtility
from tdkbE2EUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");
obj1 = tdklib.TDKScriptingLibrary("advancedconfig","RDKB");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_ParentalControl_ManagedSites_5GHZ_Block_WebsiteURL');
obj1.configureTestCase(ip,port,'E2E_ParentalControl_ManagedSites_5GHZ_Block_WebsiteURL');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 =obj1.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper() :
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

        #Assign the WIFI parameters names to a variable
        ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_5ghz_index
        keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_5ghz_index
        managedSiteEnable = "Device.X_Comcast_com_ParentalControl.ManagedSites.Enable"
        blockedSite = "Device.X_Comcast_com_ParentalControl.ManagedSites.BlockedSite."
        securityMode = "Device.WiFi.AccessPoint.%s.Security.ModeEnabled" %tdkbE2EUtility.ssid_5ghz_index

        #Get the value of the wifi parameters that are currently set.
        paramList=[ssidName,keyPassPhrase,managedSiteEnable,securityMode]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current ssid,keypassphrase,managedSiteEnable and securityMode")
            print("EXPECTED RESULT 1: Should retrieve the current ssid,keypassphrase,managedSiteEnable and securityMode")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            # Set the SSID name,password,managedSiteEnable,blockedSite and securityMode"
            setValuesList = [tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd,'true','WPA2-Personal'];
            print("Parameter values that are set: %s" %setValuesList)

            list1 = [ssidName,tdkbE2EUtility.ssid_5ghz_name,'string']
            list2 = [keyPassPhrase,tdkbE2EUtility.ssid_5ghz_pwd,'string']
            list3 = [securityMode,'WPA2-Personal','string']

            managedSiteEnableStatus = "%s|true|bool" %managedSiteEnable

            #Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2 + list3
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
            tdkTestObj,actualresult1,details = setMultipleParameterValues(obj,managedSiteEnableStatus)
            if expectedresult in actualresult and expectedresult in actualresult1:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set the ssid,keypassphrase,managedSiteEnable and securityMode")
                print("EXPECTED RESULT 2: Should set the ssid,keypassphrase,managedSiteEnable and securityMode");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");

                #Retrieve the values after set and compare
                newParamList=[ssidName,keyPassPhrase,managedSiteEnable,securityMode]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)
                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current ssid,keypassphrase,managedSiteEnable and securityMode")
                    print("EXPECTED RESULT 3: Should retrieve the current ssid,keypassphrase,managedSiteEnable and securityMode")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    # Adding a new row to BlockedSite
                    tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject");
                    tdkTestObj.addParameter("paramName","Device.X_Comcast_com_ParentalControl.ManagedSites.BlockedSite.");
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    if expectedresult in actualresult:
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TEST STEP 4: Adding new rule for site blocking");
                        print("EXPECTED RESULT 4: Should add new rule");
                        print("ACTUAL RESULT 4: added new rule %s" %details);
                        print("[TEST EXECUTION RESULT] : SUCCESS");
                        temp = details.split(':');
                        instance = temp[1];

                        if (int(instance) > 0):
                            print("INSTANCE VALUE: %s" %instance)
                            #Set a blocking url (www.google.com)
                            blockMethod = "Device.X_Comcast_com_ParentalControl.ManagedSites.BlockedSite.%s.BlockMethod" %instance
                            site = "Device.X_Comcast_com_ParentalControl.ManagedSites.BlockedSite.%s.Site" %instance
                            alwaysBlock = "Device.X_Comcast_com_ParentalControl.ManagedSites.BlockedSite.%s.AlwaysBlock" %instance

                            blocked_url = "http://"+tdkbE2EUtility.website_url
                            setValuesList = ['URL',blocked_url,'true'];
                            print("Parameter values that are set: %s" %setValuesList)

                            list1 = [blockMethod,'URL','string']
                            list2 = [site,blocked_url,'string']
                            list3 = [alwaysBlock,'true','bool']

                            #Concatenate the lists with the elements separated by pipe
                            setParamList= list1 + list2 + list3
                            setParamList = "|".join(map(str, setParamList))

                            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                            if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("TEST STEP 5: Set the blockMethod,site and alwaysBlock")
                                print("EXPECTED RESULT 5: Should set the blockMethod,site and alwaysBlock");
                                print("ACTUAL RESULT 5: %s" %details);
                                print("[TEST EXECUTION RESULT] : SUCCESS");

                                #Retrieve the values after set and compare
                                newParamList=[blockMethod,site,alwaysBlock]
                                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)
                                if expectedresult in status and setValuesList == newValues:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("TEST STEP 6: Get the current blockMethod,site and alwaysBlock")
                                    print("EXPECTED RESULT 6: Should retrieve the current blockMethod,site and alwaysBlock")
                                    print("ACTUAL RESULT 6: %s" %newValues);
                                    print("[TEST EXECUTION RESULT] : SUCCESS");

                                    #Wait for the changes to reflect in client device
                                    time.sleep(60);

                                    #Connect to the wifi ssid from wlan client
                                    print("TEST STEP 7: From wlan client, Connect to the wifi ssid")
                                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd,tdkbE2EUtility.wlan_5ghz_interface);
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS");

                                        print("TEST STEP 8: Get the IP address of the wlan client after connecting to wifi")
                                        wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_5ghz_interface);
                                        if wlanIP:
                                            tdkTestObj.setResultStatus("SUCCESS");

                                            print("TEST STEP 9: Get the current LAN IP address DHCP range")
                                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                            tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                                            print("LAN IP Address: %s" %curIPAddress);

                                            if expectedresult in status and curIPAddress:
                                                tdkTestObj.setResultStatus("SUCCESS");

                                                print("TEST STEP 10: Check whether wlan ip address is in same DHCP range")
                                                status = "SUCCESS"
                                                status = checkIpRange(curIPAddress,wlanIP);
                                                if expectedresult in status:
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("wlan ip address is in same DHCP range")
                                                    print("TEST STEP 11: Add Static route")
                                                    #set new static route to wan client
                                                    status = addStaticRoute(tdkbE2EUtility.website_url, curIPAddress,tdkbE2EUtility.wlan_5ghz_interface);
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print("Successfully added the static route")
                                                        print("TEST STEP 12:Check the Http connectivity from WLAN to URL")

                                                        status = parentalCntrlWgetToWAN("WGET_HTTP", wlanIP, curIPAddress,tdkbE2EUtility.website_url)

                                                        if expectedresult not in status:
                                                            tdkTestObj.setResultStatus("SUCCESS");
                                                            print("Http connection from WLAN to the URL is blocked")
                                                        else:
                                                            tdkTestObj.setResultStatus("FAILURE");
                                                            print("Http connection from WLAN to the URL is success")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("Failed to add static route")

                                                    #delete the added route
                                                    print("TEST STEP 13: Delete the static route")
                                                    status = delStaticRoute(tdkbE2EUtility.website_url, curIPAddress,tdkbE2EUtility.wlan_5ghz_interface);
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print("Successfully deleted the added route")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("Failed to delete the added route");
                                                    print("TEST STEP 14: From wlan client, Disconnect from the wifi ssid")
                                                    status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_5ghz_interface);
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        finalStatus = "SUCCESS";
                                                        print("Disconnect from WIFI SSID: SUCCESS")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("TEST STEP 14:Disconnect from WIFI SSID: FAILED")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("TEST STEP 10:WLAN Client IP address is not in the same Gateway DHCP range")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP 9:Failed to get the Gateway IP address")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP 8:Failed to get the WLAN Client IP address")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 7:Failed to connect to WIFI SSID")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 6: Get the current blockMethod,site and alwaysBlock")
                                    print("EXPECTED RESULT 6: Should retrieve the current blockMethod,site and alwaysBlock")
                                    print("ACTUAL RESULT 6: %s" %newValues);
                                    print("[TEST EXECUTION RESULT] : FAILURE");
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 5: Set the blockMethod,site and alwaysBlock")
                                print("EXPECTED RESULT 5: Should set the blockMethod,site and alwaysBlock");
                                print("ACTUAL RESULT 5: %s" %details);
                                print("[TEST EXECUTION RESULT] : FAILURE")

                            #Delete the created table entry
                            tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject");
                            tdkTestObj.addParameter("paramName","Device.X_Comcast_com_ParentalControl.ManagedSites.BlockedSite.%s." %instance);
                            expectedresult = "SUCCESS";
                            tdkTestObj.executeTestCase(expectedresult);
                            actualresult = tdkTestObj.getResult();
                            print("[TEST EXECUTION RESULT] : %s" %actualresult) ;
                            details = tdkTestObj.getResultDetails();
                            if expectedresult in actualresult:
                                #Set the result status of execution
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("[TEST STEP ]: Deleting the added rule");
                                print("[EXPECTED RESULT ]: Should delete the added rule");
                                print("[ACTUAL RESULT]: %s" %details);
                                print("[TEST EXECUTION RESULT] : %s" %actualresult);
                                print("Added table is deleted successfully\n")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("[TEST STEP ]: Deleting the added rule");
                                print("[EXPECTED RESULT ]: Should delete the added rule");
                                print("[ACTUAL RESULT]: %s" %details);
                                print("[TEST EXECUTION RESULT] : %s" %actualresult);
                                print("Added table could not be deleted\n")
                        else:
                            print("Table add returned invalid instance")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 4: Adding new rule for site blocking");
                        print("EXPECTED RESULT 4: Should add new rule");
                        print("ACTUAL RESULT 4: added new rule %s" %details);
                        print("[TEST EXECUTION RESULT] : FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current ssid,keypassphrase,managedSiteEnable and securityMode")
                    print("EXPECTED RESULT 3: Should retrieve the current ssid,keypassphrase,managedSiteEnable and securityMode")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("TEST STEP 2: Set the ssid,keypassphrase,managedSiteEnable and securityMode")
                print("EXPECTED RESULT 2: Should set the ssid,keypassphrase,managedSiteEnable and securityMode");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");

            #Prepare the list of parameter values to be reverted
            list1 = [ssidName,orgValue[0],'string']
            list2 = [keyPassPhrase,orgValue[1],'string']
            list3 = [securityMode,orgValue[3],'string']

            #Concatenate the lists with the elements separated by pipe
            revertParamList = list1 + list2 + list3
            revertParamList = "|".join(map(str, revertParamList))

            managedSiteEnableStatus = "%s|%s|bool" %(managedSiteEnable,orgValue[2])

            #Revert the values to original
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
            tdkTestObj,actualresult1,details = setMultipleParameterValues(obj,managedSiteEnableStatus)
            if expectedresult in actualresult and expectedresult in actualresult1 and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 15: Should set the original ssid,keypassphrase,managedSiteEnable and securityMode");
                print("ACTUAL RESULT 15: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 15: Should set the original ssid,keypassphrase,managedSiteEnable and securityMode");
                print("ACTUAL RESULT 15: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current ssid,keypassphrase,managedSiteEnable and securityMode")
            print("EXPECTED RESULT 1: Should retrieve the current ssid,keypassphrase,managedSiteEnable and securityMode")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        obj.setLoadModuleStatus("FAILURE");
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup();
    obj.unloadModule("tdkb_e2e");
    obj1.unloadModule("advancedconfig");

else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");
