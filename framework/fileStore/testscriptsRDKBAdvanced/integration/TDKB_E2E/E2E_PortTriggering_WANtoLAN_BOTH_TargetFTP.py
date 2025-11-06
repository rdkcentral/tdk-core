##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2024 RDK Management
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
  <version>17</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_PortTriggering_WANtoLAN_BOTH_TargetFTP</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if the Port Triggering rule in GW takes effect so that inbound packet with target port 21 is forwarded to the LAN machine (which is running an FTP server) after it sends an outbound packet through the GW that triggers the 12345 port configured in the rule with protocol as BOTH.</synopsis>
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
    <box_type>RPI</box_type>
    <!--  -->
  <box_type>BPI</box_type></box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_604</test_case_id>
    <test_objective>To check if the Port Triggering rule in GW takes effect so that an inbound packet with target port 21 is forwarded to the LAN machine (which is running an FTP server) after it sends an outbound packet through the GW that triggers the 12345 port configured in the rule with protocol as BOTH.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband, RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.NAT.X_CISCO_COM_PortTriggers.Enable - true/false
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.TriggerProtocol - BOTH
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.TriggerPortStart - 12345
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.TriggerPortEnd - 12345
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.ForwardProtocol - BOTH
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.ForwardPortStart - 21
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.ForwardPortEnd - 21
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.Description - MyPTRule
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.Enable - true
Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress</input_parameters>
    <automation_approch>1. Load the E2E, Advanced Config Modules
2. Check if Device.NAT.X_CISCO_COM_PortTriggers.Enable is enabled, if not enable it.
3. Check if a lan client is connected to the GW by fetching the IP corresponding to the configuration interface.
4. Check if the lan IP is in the expected DHCP range.
5. Add a new instance to the port triggering rule table
6. To the added instance, configure the rule: Trigger Port(start:end) - 12345:12345, TargetPort(start:end) - 21:21 (for FTP), Trigger Protocol - BOTH, Target Protocol - BOTH, Description - MyPTRule
7. Enable the added port trigger rule
8. Check if the rule is added and enabled successfully by fetching the values of corresponding DMs
9. Add a static route in the LAN client so that an outbound packet can be sent from the client via the DUT GW to the external network
10. Send an outbound packet to trigger the port 12345 with a TCP packet
11. From WAN client, send an inbound packet to the target port 21 via the DUT GW WAN IP. The packet should be successfully forwarded to the LAN client.
12. Delete the added route
13. Delete the added port triggering rule
14. Revert Device.NAT.X_CISCO_COM_PortTriggers.Enable if required
15. Unload the modules</automation_approch>
    <expected_output>Port Triggering rule in GW should take effect so that an inbound packet with target port 21 is forwarded to the LAN machine (which is running both FTP and TCP servers) after it sends an outbound packet through the GW that triggers the 12345 port configured in the rule.</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_PortTriggering_WANtoLAN_BOTH_TargetFTP</test_script>
    <skipped>No</skipped>
    <release_version>M123</release_version>
    <remarks></remarks>
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
obj1 = tdklib.TDKScriptingLibrary("advancedconfig","RDKB");
#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_PortTriggering_WANtoLAN_BOTH_TargetFTP');
obj1.configureTestCase(ip,port,'E2E_PortTriggering_WANtoLAN_BOTH_TargetFTP');
#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 =obj1.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus1) ;
if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper() :
    obj.setLoadModuleStatus("SUCCESS");
    obj1.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    status = "FAILURE"
    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        print("Parsed the device configuration file successfully")
        #Check if Port Triggering is enabled, else enable the feature
        step = 1
        status, tdkTestObj, revertFlag, step = PTPreRequisite(obj, step)
        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            #Get the LAN IP address of connected client
            step = step + 1
            print("\nTEST STEP %d: Get the LAN IP address of the connected client" %step)
            print("EXPECTED RESULT %d: The current LAN IP address of the connected client should be obtained" %step)
            lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
            if lanIP != "":
                tdkTestObj.setResultStatus("SUCCESS");
                print("ACTUAL RESULT %d : Current LAN IP address is obtained as %s" %(step, lanIP))
                print("[TEST EXECUTION RESULT] : SUCCESS");
                #Check if the current Lan IP is in the DHCP range
                step = step + 1;
                print("\nTEST STEP %d: Check if the current LAN IP address is in DHCP range" %step)
                print("EXPECTED RESULT %d: The current LAN IP address should be in DHCP range" %step)
                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                print("LAN IP Address: %s" %curIPAddress);
                if expectedresult in status and curIPAddress:
                    tdkTestObj.setResultStatus("SUCCESS");
                    status = checkIpRange(curIPAddress,lanIP);
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("ACTUAL RESULT %d : Current LAN IP address is in same DHCP range" %step)
                        print("[TEST EXECUTION RESULT] : SUCCESS");
                        #Set the Port Triggering rule and enable it:- Trigger Port(start:end) - 12345:12345, TargetPort(start:end) - 21:21 (for FTP), Trigger Protocol - BOTH, Target Protocol - BOTH, Description - MyPTRule
                        step = step + 1
                        triggerStart = "12345"
                        triggerEnd = "12345"
                        targetStart = "21"
                        targetEnd = "21"
                        triggerProtocol = "BOTH"
                        targetProtocol = "BOTH"
                        description = "MyPTRule"
                        enablePTRule = "true"
                        status, tdkTestObj, instance, step = SetPTRule(obj, obj1, triggerStart, triggerEnd, targetStart, targetEnd, triggerProtocol, targetProtocol, description, enablePTRule, step)
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS");
                            #Set new static route in LAN client
                            step = step + 1
                            print("\nTEST STEP %d: Add a new static route in LAN client to route the trigger via DUT" %step)
                            print("EXPECTED RESULT %d: A new static route should be added in LAN client to route the trigger via DUT" %step)
                            status = addStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress, tdkbE2EUtility.lan_interface, "LAN");
                            if expectedresult in status:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("ACTUAL RESULT %d: Static route added successfully" %step)
                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                #Trigger the port
                                step = step + 1
                                print("\nTEST STEP %d: Trigger the Port %s through a specified outbound packet from LAN client" %(step, triggerStart))
                                print("EXPECTED RESULT %d: Port should be triggered successfully" %step)
                                trigger_protocol = "TCP"
                                status = triggerPort(tdkbE2EUtility.wan_ip, triggerStart, trigger_protocol, "LAN")
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("ACTUAL RESULT %d: Port Triggered successfully" %step)
                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                    #Check if the specified inbound packets are forwarded to the LAN client that triggered it
                                    step = step + 1
                                    print("\nTEST STEP %d: Check if the specified inbound packets are forwarded to the LAN client that triggered it" %step)
                                    print("EXPECTED RESULT %d: FTP from WAN to the LAN should be success with the GW WAN IP of DUT" %step)
                                    status = ftpToClient("LAN", tdkbE2EUtility.gw_wan_ip, "WAN");
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("ACTUAL RESULT %d: FTP from WAN to the LAN is success with the GW WAN IP of DUT" %step)
                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("ACTUAL RESULT %d: FTP from WAN to the LAN failed with the GW WAN IP of DUT" %step)
                                        print("[TEST EXECUTION RESULT] : FAILURE");
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("ACTUAL RESULT %d: Port not triggered successfully" %step)
                                    print("[TEST EXECUTION RESULT] : FAILURE");
                                #Delete the newly added route in LAN client
                                step = step + 1;
                                print("\nTEST STEP %d: Delete the added static route in LAN client" %step)
                                print("EXPECTED RESULT %d: The added static route should be deleted successfully" %step)
                                status = delStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress, tdkbE2EUtility.lan_interface, "LAN");
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("ACTUAL RESULT %d: Added route is deleted successfully" %step)
                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("ACTUAL RESULT %d: Added route is not deleted successfully" %step)
                                    print("[TEST EXECUTION RESULT] : FAILURE");
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("ACTUAL RESULT %d: Static route not added successfully" %step)
                                print("[TEST EXECUTION RESULT] : FAILURE");
                            #Delete the added PT rule
                            step = step + 1
                            DeletePTRule(obj1, instance, step)
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("\nPort triggering rule not set, not proceeding further...")
                        #Revert the PT enable if required
                        if revertFlag == 1:
                            step = step + 1
                            PTRevertPreRequisite(obj, step);
                        else:
                            print("\nReverting the Port Triggering Enable is not required")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("ACTUAL RESULT %d : Current LAN IP address is not in same DHCP range" %step)
                        print("[TEST EXECUTION RESULT] : FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("ACTUAL RESULT %d : Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress not retrieved" %step)
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("ACTUAL RESULT %d : Current LAN IP address not obtained" %step)
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("Cannot enable port triggering feature, not proceeding further...")
    else:
        obj.setLoadModuleStatus("FAILURE");
        print("Failed to parse the device configuration file")
    #Handle any post execution cleanup required
    postExecutionCleanup();
    obj.unloadModule("tdkb_e2e");
    obj1.unloadModule("advancedconfig");
else:
    print("Failed to load tdkb_e2e module");
    print("Failed to load advanedconfig module");
    obj.setLoadModuleStatus("FAILURE");
    obj1.setLoadModuleStatus("FAILURE");
