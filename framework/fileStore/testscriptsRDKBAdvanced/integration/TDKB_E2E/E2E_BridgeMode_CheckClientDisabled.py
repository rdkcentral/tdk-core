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
  <name>E2E_BridgeMode_CheckClientDisabled</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check if the Connected clients are disabled when the gateway is in bridge mode and if the clients are enabled back on disabling bridge mode</synopsis>
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

  <box_type>BPI</box_type></box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_479</test_case_id>
    <test_objective>Check if the Connected clients are disabled when the gateway is in bridge mode and if the clients are enabled back on disabling bridge mode</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode
Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress
Device.Hosts.HostNumberOfEntries
Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Get the current LanMode and save it
3. Get the current LAN IP address DHCP range
4. Set the LanMode as bridge mode
5. Get the ip address of the lan client
6. Check if the lan client ip is not in the DHCP range
7. Check if Device.Hosts.HostNumberOfEntries and
Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber are 0
8. Change lanmode to router
9. Get the lan ip and check if it is within the DHCP range
10. Check if Device.Hosts.HostNumberOfEntries and
Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber are greater than 0
11. Revert the Lanmode to its initial value
12. Unload tdkb_e2e module</automation_approch>
    <except_output>When gateway is in bridge mode, connected client should be disabled and when bridge mode is disabled client should be enabled back</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_BridgeMode_CheckClientDisabled</test_script>
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
import tdkbE2EUtility
from tdkbE2EUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_BridgeMode_CheckClientDisabled');

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

        #Assign the parameters names to a variable
        lanMode = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode"

        #Get the value of the wifi parameters that are currently set.
        tdkTestObj,status,orgValue = getParameterValue(obj,lanMode)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current lanMode")
            print("EXPECTED RESULT 1: Should retrieve the current lanMode")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            print("TEST STEP 2: Get the current LAN IP address DHCP range")
            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
            tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
            print("LAN IP Address: %s" %curIPAddress);

            if expectedresult in status and curIPAddress:
                tdkTestObj.setResultStatus("SUCCESS");

                status = setLanModeAndVerify(obj,'bridge-static')

                if expectedresult in status:

                    #Connect to LAN client and obtain its IP
                    print("TEST STEP 3: Get the IP address of the lan client after connecting to it")
                    lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
                    if lanIP:
                        #check if the lan client's IP is not in the local ip range
                        status = checkIpRange(curIPAddress,lanIP)
                        if expectedresult not in status:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("Lan client IP has changed");

                            paramList=["Device.Hosts.HostNumberOfEntries", "Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber"]
                            tdkTestObj,status,valueList = getMultipleParameterValues(obj,paramList)
                            print("Connected client list [Device.Hosts.HostNumberOfEntries, Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber] received as: ", valueList)
                            if expectedresult in status and valueList == ['0','0']:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("SUCCESS: Client got disabled")

                                #Disable bridge mode and check if client is enabled back
                                status = setLanModeAndVerify(obj,'router')
                                if expectedresult in status:
                                    print("Lan mode set as router")

                                    #Connect to LAN client and obtain its IP
                                    print("TEST STEP 4: Get the IP address of the lan client after connecting to it")
                                    lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
                                    if lanIP:
                                        status = checkIpRange(curIPAddress,lanIP)
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("Lan client IP has returned to its expected range")

                                            paramList=["Device.Hosts.HostNumberOfEntries", "Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber"]
                                            tdkTestObj,status,valueList = getMultipleParameterValues(obj,paramList)
                                            print("Connected Client list [Device.Hosts.HostNumberOfEntries, Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber] received as: ", valueList)
                                            if expectedresult in status and int(valueList[0]) > 0 and int(valueList[1]) > 0:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print("SUCCESS: Client is enabled back")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("FAILURE: Client is not enabled back")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("FAILURE: Lan client IP has not returned to its expected range")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("SUCCESS: Failed to get lan ip")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("Failed to disable bridge mode")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("Failed to get connected client count")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("Lan client IP not changed with bridge mode");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("FAILURE: Failed to get lan ip")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("Failed to set bridge mode")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("getLanIPAddress:Failed to get the LAN IP address DHCP range")

            #revert the params
            status = setLanModeAndVerify(obj,orgValue)
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current lanMode")
            print("EXPECTED RESULT 1: Should retrieve the current lanMode")
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
