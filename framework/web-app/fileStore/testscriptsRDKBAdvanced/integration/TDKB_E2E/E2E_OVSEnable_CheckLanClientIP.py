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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_OVSEnable_CheckLanClientIP</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check if the Lan client gets proper IP when OVS is enabled in gateway</synopsis>
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
    <test_case_id>TC_TDKB_E2E_552</test_case_id>
    <test_objective>Check if the Lan client gets proper IP when OVS is enabled in gateway</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband</test_setup>
    <pre_requisite>A LAN client should be available</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.OVS.Enable</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Check if OVS is enabled
3. If OVS is not enabled, enable it and do a reboot
4. From lan client, refresh the lan interface connected to DUT
5. Check if the connection is success and ip received by lan client is in proper range when OVS is enabled
6. Revert OVS enabled state to its initial value
7. Unload tdkb_e2e module</automation_approch>
    <expected_output>Lan client gets proper IP when OVS is enabled in gateway</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_OVSEnable_CheckLanClientIP</test_script>
    <skipped>No</skipped>
    <release_version>M94</release_version>
    <remarks>LAN</remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library, which provides a wrapper for tdk testcase script
import tdklib;
import time;
import tdkbE2EUtility
from tdkbE2EUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_OVSEnable_CheckLanClientIP');

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

        OVSParam= "Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.OVS.Enable"

        #Get the current value of the OVS Enable state
        tdkTestObj, retStatus,OVSValue = getParameterValue(obj, OVSParam)

        if expectedresult in retStatus:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current OVS Enable state")
            print("EXPECTED RESULT 1: Should retrieve the current OVS Enable state")
            print("ACTUAL RESULT 1: OVS Enabled state is %s" %OVSValue) ;
            print("[TEST EXECUTION RESULT] : SUCCESS");

            if OVSValue == "false":
                # Set OVS Enable as true
                OVSSet = "%s|true|bool" %OVSParam

                tdkTestObj, OVSResult, details = setMultipleParameterValues(obj, OVSSet)
                if expectedresult in OVSResult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 2: Set the OVS Enable as true")
                    print("EXPECTED RESULT 2: Should set OVS enable as true");
                    print("ACTUAL RESULT 2: %s" %details);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    #Retrieve the values after set and compare
                    tdkTestObj, retStatus, newOVSValue = getParameterValue(obj, OVSParam)
                    print("OVS Enabled state is: %s" %newOVSValue) ;

                    if expectedresult in retStatus and newOVSValue == "true":
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TEST STEP 3: Get the current OVS Enable state")
                        print("EXPECTED RESULT 3: Should retrieve the set value as the current OVS Enable state")
                        print("ACTUAL RESULT 3: %s " %newOVSValue) ;
                        print("[TEST EXECUTION RESULT] : SUCCESS");

                        #rebooting the device
                        obj.initiateReboot();
                        sleep(300);
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 3: Get the current OVS Enable state")
                        print("EXPECTED RESULT 3: Should retrieve the set value as the current OVS Enable state")
                        print("ACTUAL RESULT 3:  %s" %newOVSValue) ;
                        print("[TEST EXECUTION RESULT] : FAILURE");
                        obj.unloadModule("tdkb_e2e");
                        exit()
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    details = tdkTestObj.getResultDetails();
                    print("TEST STEP 2: Set the OVS Enable as true")
                    print("EXPECTED RESULT 2: Should set OVS enable as true");
                    print("ACTUAL RESULT 2: %s" %details);
                    print("[TEST EXECUTION RESULT] : FAILURE");
                    obj.unloadModule("tdkb_e2e");
                    exit()

            print("TEST STEP 4: Get the IP address of the lan client after connecting to it")
            print("EXPECTED RESULT 4: Should retrieve the IP address of the lan client ");
            lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
            if lanIP:
                tdkTestObj.setResultStatus("SUCCESS");
                print("ACTUAL RESULT 4: LAN IP retrieved is %s " %lanIP) ;
                print("[TEST EXECUTION RESULT] : SUCCESS");

                print("TEST STEP 5: Get the current Gateway IP address")
                print("EXPECTED RESULT 5: Should retrieve the current Gateway IP address")
                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                tdkTestObj,status,curIPAddress = getParameterValue(obj,param)

                if expectedresult in status and curIPAddress:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("ACTUAL RESULT 5 :GW IP Address: %s" %curIPAddress);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    print("TEST STEP 6: Check whether lan ip address is in same DHCP range")
                    print("EXPECTED RESULT 6: LAN ip should be in valid DHCP range")
                    status = "SUCCESS"
                    status = checkIpRange(curIPAddress,lanIP);
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("ACTUAL RESULT 6: LAN ip address is in valid DHCP range")
                        print("[TEST EXECUTION RESULT] : SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("ACTUAL RESULT 6: LAN Client IP address is not in valid DHCP range")
                        print("[TEST EXECUTION RESULT] : FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("ACTUAL RESULT 5 :Failed to get the Gateway IP address")
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("ACTUAL RESULT 4: Failed to get the LAN Client IP address")
                print("[TEST EXECUTION RESULT] : FAILURE");

            #Revert the OVS state to original value
            if OVSValue == "false":
                #Prepare the list of parameter values to be reverted
                OVSParam = "%s|%s|bool" %(OVSParam, OVSValue)

                tdkTestObj, OVSResult, details = setMultipleParameterValues(obj,OVSParam)
                if  expectedresult in OVSResult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("EXPECTED RESULT 7: Should set the original OVS Enabled status");
                    print("ACTUAL RESULT 7: %s" %details);
                    print("[TEST EXECUTION RESULT] : SUCCESS");
                    #rebooting the device
                    obj.initiateReboot();
                    sleep(300);
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    details = tdkTestObj.getResultDetails();
                    print("EXPECTED RESULT 7: Should set the original OVS Enabled status");
                    print("ACTUAL RESULT 7: %s" %details);
                    print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current OVS Enable state")
            print("EXPECTED RESULT 1: Should retrieve the current OVS Enable state")
            print("ACTUAL RESULT 1: %s " %OVSValue) ;
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