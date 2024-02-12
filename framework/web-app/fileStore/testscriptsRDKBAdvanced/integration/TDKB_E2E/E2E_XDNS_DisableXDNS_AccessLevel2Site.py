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
  <name>E2E_XDNS_DisableXDNS_AccessLevel2Site</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To disable xDNS and test if connectivity to level2 (medium) websites work as expected</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>30</execution_time>
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
    <test_case_id>TC_TDKB_E2E_413</test_case_id>
    <test_objective>To disable xDNS and test if connectivity to level2 (medium) websites work as expected</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway
Ensure that xdns process is running in gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.DeviceInfo.X_RDKCENTRAL-COM_EnableXDNS</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Get and save the value of Device.DeviceInfo.X_RDKCENTRAL-COM_EnableXDNS
3. Set Device.DeviceInfo.X_RDKCENTRAL-COM_EnableXDNS as false
4. Connect to lan client
5. Get the lan client ip and check if its in valid range
6. From lan client do nslookup of a level2 site
7. Check if nslookup was success
8. Revert  the value of Device.DeviceInfo.X_RDKCENTRAL-COM_EnableXDNS
9. Unload tdkb_e2e module</automation_approch>
    <except_output>nslookup of level2 site from Lan client should be success</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_XDNS_DisableXDNS_AccessLevel2Site</test_script>
    <skipped>No</skipped>
    <release_version>M60</release_version>
    <remarks>LAN</remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import tdkbE2EUtility
from tdkbE2EUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_XDNS_DisableXDNS_AccessLevel2Site');

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

        #Assign the  parameters names to a variable
        xdnsEnable = "Device.DeviceInfo.X_RDKCENTRAL-COM_EnableXDNS"

        #Get the value of the wifi parameters that are currently set.
        paramList=[xdnsEnable]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current enable status of XDNS")
            print("EXPECTED RESULT 1: Should retrieve the current enable status of XDNS")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            #Disabling XDNS
            setValuesList = ['false'];
            print("WIFI parameter values that are set: %s" %setValuesList)

            xdnsEnableValue="%s|false|bool" %xdnsEnable

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,xdnsEnableValue)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Disable XDNS")
                print("EXPECTED RESULT 2: Should disable XDNS");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");

                #Retrieve the values after set and compare
                newParamList=[xdnsEnable]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current xdnsEnable")
                    print("EXPECTED RESULT 3: Should retrieve the current xdnsEnable")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    time.sleep(30);

                    #Connect to LAN client and obtain its IP
                    print("TEST STEP 4: Get the IP address of the lan client after connecting to it")
                    lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
                    if lanIP:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TEST STEP 5: Get the current LAN IP address DHCP range")
                        param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                        tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                        print("LAN IP Address: %s" %curIPAddress);

                        if expectedresult in status and curIPAddress:
                            tdkTestObj.setResultStatus("SUCCESS");
                            #Check if the site is accessible
                            status = verifyNetworkConnectivity(tdkbE2EUtility.xdns_level2_site, "PING_TO_HOST", lanIP, curIPAddress,"LAN")
                            if expectedresult in status:
                                tdkTestObj.setResultStatus("SUCCESS");
                                finalStatus = "SUCCESS";
                                print("TEST STEP 6:Check if the level2 site accessible with xdns disbaled")
                                print("EXPECTED RESULT 6:The level2 site should be accessible with xdns disabled")
                                print("[TEST EXECUTION RESULT] : SUCCESS");
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 6:Check if the level2 site accessible with xdns disbaled")
                                print("EXPECTED RESULT 6:The level2 site should be accessible with xdns disabled")
                                print("[TEST EXECUTION RESULT] : FAILURE");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("getParameterValue : Failed to get gateway lan ip")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("getLanIPAddress:Failed to get the LAN client IP")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current xdnsEnable")
                    print("EXPECTED RESULT 3: Should retrieve the current xdnsEnable")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Disable XDNS")
                print("EXPECTED RESULT 2: Should disable XDNS");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
            #revert the params
            xdnsEnableValue="%s|%s|bool" %(xdnsEnable,orgValue[0])
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,xdnsEnableValue)
            if expectedresult in actualresult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 7: Should revert the xdns enable status");
                print("ACTUAL RESULT 7: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 7: Should revert the xdns enable status");
                print("ACTUAL RESULT 7: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current enable status of XDNS")
            print("EXPECTED RESULT 1: Should retrieve the current enable status of XDNS")
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