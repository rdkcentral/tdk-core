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
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_PortTriggering_WANtoWLAN_BOTH_TargetNETCAT_TriggerTCP</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if the Port Triggering rule in GW takes effect so that an inbound packet with target port 54321 is forwarded to the WLAN machine (which is running a NETCAT server) after it sends an outbound packet through the GW that triggers the 12345 port configured in the rule with protocol as BOTH.</synopsis>
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
    <box_type>RPI</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_611</test_case_id>
    <test_objective>To check if the Port Triggering rule in GW takes effect so that inbound packet with target port 54321 is forwarded to the WLAN machine (which is running a NETCAT server) after it sends an outbound packet through the GW that triggers the 12345 port configured in the rule with protocol as BOTH.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.NAT.X_CISCO_COM_PortTriggers.Enable - true/false
Device.WiFi.SSID.{i}.SSID to configure custom SSID
Device.WiFi.AccessPoint.{i}.Security.KeyPassphrase - to configure custom keypassphrase
Device.WiFi.Radio.{i}.Enable - true
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.TriggerProtocol - BOTH
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.TriggerPortStart - 12345
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.TriggerPortEnd - 12345
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.ForwardProtocol - BOTH
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.ForwardPortStart - 54321
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.ForwardPortEnd - 54321
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.Description - MyPTRule
Device.NAT.X_CISCO_COM_PortTriggers.Trigger.{i}.Enable - true
Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.WlanIPAddress</input_parameters>
    <automation_approch>1. Load the E2E, Advanced Config Modules
2. Check if Device.NAT.X_CISCO_COM_PortTriggers.Enable is enabled, if not enable it.
3. Check if a wlan client is connected to the GW by fetching the IP corresponding to the configuration interface.
4. Check if the wlan IP is in the expected DHCP range.
5. Add a new instance to the port triggering rule table
6. To the added instance, configure the rule: Trigger Port(start:end) - 12345:12345, TargetPort(start:end) - 54321:54321 (for NETCAT), Trigger Protocol - BOTH, Target Protocol - BOTH, Description - MyPTRule
7. Enable the added port trigger rule
8. Check if the rule is added and enabled successfully by fetching the values of corresponding DMs
9. Add a static route in the WLAN client so that an outbound packet can be sent from the client via the DUT GW to the external network
10. Send an outbound packet to trigger the port 12345 with a TCP packet
11. From WAN client, send an inbound packet to the target port 54321 via the DUT GW WAN IP. The packet should be successfully forwarded to the WLAN client.
12. Delete the added route
13. Delete the added port triggering rule
14. Revert Device.NAT.X_CISCO_COM_PortTriggers.Enable if required
15. Unload the modules</automation_approch>
    <expected_output>Port Triggering rule in GW should take effect so that an inbound packet with target port 54321 is forwarded to the WLAN machine (which is running a NETCAT server) after it sends an outbound packet through the GW that triggers the 12345 port configured in the rule.</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_PortTriggering_WANtoWLAN_BOTH_TargetNETCAT_TriggerTCP</test_script>
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
import random;
import tdkbE2EUtility
from tdkbE2EUtility import *;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");
obj1 = tdklib.TDKScriptingLibrary("advancedconfig","RDKB");
#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_PortTriggering_WANtoWLAN_BOTH_TargetNETCAT_TriggerTCP');
obj1.configureTestCase(ip,port,'E2E_PortTriggering_WANtoWLAN_BOTH_TargetNETCAT_TriggerTCP');
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
            #Assign the WIFI parameters names to a variable
            ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
            keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
            radioEnable = "Device.WiFi.Radio.%s.Enable" %tdkbE2EUtility.radio_2ghz_index
            #Get the value of the wifi parameters that are currently set.
            step = step + 1
            print("\nTEST STEP %d: Get the current ssid,keypassphrase,Radio enable status" %step)
            print("EXPECTED RESULT %d: Should retrieve the current ssid,keypassphrase,Radio enable status" %step)
            paramList=[ssidName,keyPassPhrase,radioEnable]
            tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)
            if expectedresult in status:
                tdkTestObj.setResultStatus("SUCCESS");
                print("ACTUAL RESULT %d: Values retrieved: %s" %(step, orgValue));
                print("[TEST EXECUTION RESULT] : SUCCESS");
                # Set the SSID name, KeyPassphrase, Radio enable
                step = step + 1
                print("\nTEST STEP %d: Set the ssid, keypassphrase, radio enable" %step)
                print("EXPECTED RESULT %d: Should set the ssid, keypassphrase, radio enable successfully" %step);
                setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,'true'];
                print("Parameter values that are set: %s" %setValuesList)
                list1 = [ssidName,tdkbE2EUtility.ssid_2ghz_name,'string']
                list2 = [keyPassPhrase,tdkbE2EUtility.ssid_2ghz_pwd,'string']
                list3 = [radioEnable,'true','bool']
                #Concatenate the lists with the elements separated by pipe
                setParamList = list1 + list2 + list3
                setParamList = "|".join(map(str, setParamList))
                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("ACTUAL RESULT %d: Details: %s" %(step, details));
                    print("[TEST EXECUTION RESULT] : SUCCESS");
                    #Retrieve the values after set and compare
                    step = step + 1
                    print("\nTEST STEP %d: Get the current ssid, keypassphrase, radio enable" %step)
                    print("EXPECTED RESULT %d: Should retrieve the current ssid, keypassphrase, radio enable" %step)
                    tdkTestObj,status,newValues = getMultipleParameterValues(obj, paramList)
                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("ACTUAL RESULT %d: GET values:  %s" %(step, newValues));
                        print("[TEST EXECUTION RESULT] : SUCCESS");
                        #Wait for the changes to reflect in client device
                        time.sleep(60);
                        #Connect to the wifi ssid from wlan client
                        step = step + 1
                        print("\nTEST STEP %d: From wlan client, connect to the WiFi SSID" %step)
                        print("EXPECTED RESULT %d: The wlan client should be successfully connected to the WiFi SSID" %step)
                        status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.wlan_2ghz_interface);
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("ACTUAL RESULT %d: Wlan client successfully connected to WiFi SSID" %(step));
                            print("[TEST EXECUTION RESULT] : SUCCESS");
                            #Get the WLAN IP address of connected client
                            step = step + 1
                            print("\nTEST STEP %d: Get the WLAN IP address of the connected client" %step)
                            print("EXPECTED RESULT %d: The current WLAN IP address of the connected client should be obtained" %step)
                            wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_2ghz_interface);
                            if wlanIP != "":
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("ACTUAL RESULT %d : Current WLAN IP address is obtained as %s" %(step, wlanIP))
                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                #Check if the current Wlan IP is in the DHCP range
                                step = step + 1;
                                print("\nTEST STEP %d: Check if the current WLAN IP address is in DHCP range" %step)
                                print("EXPECTED RESULT %d: The current WLAN IP address should be in DHCP range" %step)
                                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                                print("WLAN IP Address: %s" %curIPAddress);
                                if expectedresult in status and curIPAddress:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    status = checkIpRange(curIPAddress,wlanIP);
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("ACTUAL RESULT %d : Current WLAN IP address is in same DHCP range" %step)
                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                        #Set the Port Triggering rule and enable it:- Trigger Port(start:end) - 12345:12345, TargetPort(start:end) - 54321:54321 (for NETCAT), Trigger Protocol - BOTH, Target Protocol - BOTH, Description - MyPTRule
                                        step = step + 1
                                        triggerStart = "12345"
                                        triggerEnd = "12345"
                                        targetStart = "54321"
                                        targetEnd = "54321"
                                        triggerProtocol = "BOTH"
                                        targetProtocol = "BOTH"
                                        description = "MyPTRule"
                                        enablePTRule = "true"
                                        status, tdkTestObj, instance, step = SetPTRule(obj, obj1, triggerStart, triggerEnd, targetStart, targetEnd, triggerProtocol, targetProtocol, description, enablePTRule, step)
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            #Set new static route in WLAN client
                                            step = step + 1
                                            print("\nTEST STEP %d: Add a new static route in WLAN client to route the trigger via DUT" %step)
                                            print("EXPECTED RESULT %d: A new static route should be added in WLAN client to route the trigger via DUT" %step)
                                            status = addStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress, tdkbE2EUtility.wlan_2ghz_interface, "WLAN");
                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print("ACTUAL RESULT %d: Static route added successfully" %step)
                                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                                #Start the NETCAT server in WLAN
                                                step = step + 1
                                                #Custom Message to be sent from server to client
                                                value = random.randint(0, 1000)
                                                message = "Message from server " + str(value)
                                                print("\nTEST STEP %d: Start the NETCAT server in WLAN client at port %s" %(step, targetStart))
                                                print("EXPECTED RESULT %d: NETCAT server should be started successfully in WLAN client" %step)
                                                #Since targetProtocol BOTH is not supported in server side, passing the target protocol TCP
                                                target_protocol = "TCP"
                                                status = PTinitServer("NETCAT", wlanIP, targetStart, target_protocol, tdkbE2EUtility.server_logfile, "WLAN", message)
                                                if expectedresult in status:
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("ACTUAL RESULT %d: NETCAT server started successfully and listening to port: %s" %(step, targetStart))
                                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                                    #Trigger the port
                                                    step = step + 1
                                                    print("\nTEST STEP %d: Trigger the Port %s through a specified outbound packet from WLAN client" %(step, triggerStart))
                                                    print("EXPECTED RESULT %d: Port should be triggered successfully" %step)
                                                    trigger_protocol = "TCP"
                                                    status = triggerPort(tdkbE2EUtility.wan_ip, triggerStart, trigger_protocol, "WLAN")
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print("ACTUAL RESULT %d: Port Triggered successfully" %step)
                                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                                        #Check if the specified inbound packets are forwarded to the WLAN client that triggered it
                                                        step = step + 1
                                                        print("\nTEST STEP %d: Check if the specified inbound packets are forwarded to the WLAN client that triggered it" %step)
                                                        print("EXPECTED RESULT %d: NETCAT client running in WAN machine should connect to the server running in WLAN with the GW WAN IP of DUT" %step)
                                                        #Since targetProtocol BOTH is not supported in server side, passing the target protocol TCP
                                                        status = PTClientRequest("NETCAT", tdkbE2EUtility.wan_ip, targetStart, target_protocol, tdkbE2EUtility.client_logfile, "WAN");
                                                        if message in status:
                                                            tdkTestObj.setResultStatus("SUCCESS");
                                                            print("ACTUAL RESULT %d: NETCAT from WAN to the WLAN is success with the GW WAN IP of DUT" %step)
                                                            print("[TEST EXECUTION RESULT] : SUCCESS");
                                                        else:
                                                            tdkTestObj.setResultStatus("FAILURE");
                                                            print("ACTUAL RESULT %d: NETCAT from WAN to the WLAN failed with the GW WAN IP of DUT" %step)
                                                            print("[TEST EXECUTION RESULT] : FAILURE");
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("ACTUAL RESULT %d: Port not triggered successfully" %step)
                                                        print("[TEST EXECUTION RESULT] : FAILURE");
                                                    #Kill the server-client processes running
                                                    step = step + 1
                                                    print("\nTEST STEP %d: Execute the post-requisites in server and client" %step)
                                                    print("EXPECTED RESULT %d: Post-requisites in server and client should be completed successfully" %step)
                                                    status = PTServerClientPostRequisite("NETCAT", "WLAN", "WAN")
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print("ACTUAL RESULT %d: Post-requisites in server and client success" %step)
                                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("ACTUAL RESULT %d: Post-requisites in server and client failed" %step)
                                                        print("[TEST EXECUTION RESULT] : FAILURE");
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("ACTUAL RESULT %d: NETCAT server not started successfully" %step)
                                                    print("[TEST EXECUTION RESULT] : FAILURE");
                                                #Delete the newly added route in WLAN client
                                                step = step + 1;
                                                print("\nTEST STEP %d: Delete the added static route in WLAN client" %step)
                                                print("EXPECTED RESULT %d: The added static route should be deleted successfully" %step)
                                                status = delStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress, tdkbE2EUtility.wlan_2ghz_interface, "WLAN");
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
                                        print("ACTUAL RESULT %d : Current WLAN IP address is not in same DHCP range" %step)
                                        print("[TEST EXECUTION RESULT] : FAILURE");
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("ACTUAL RESULT %d : Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress not retrieved" %step)
                                    print("[TEST EXECUTION RESULT] : FAILURE");
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("ACTUAL RESULT %d : Current WLAN IP address not obtained" %step)
                                print("[TEST EXECUTION RESULT] : FAILURE");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("ACTUAL RESULT %d: Wlan client not connected to WiFi SSID" %(step));
                            print("[TEST EXECUTION RESULT] : FAILURE");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("ACTUAL RESULT %d: Value not retrieved successfully" %step);
                        print("[TEST EXECUTION RESULT] : FAILURE");
                    #Prepare the list of parameter values to be reverted
                    step = step + 1
                    list1 = [ssidName,orgValue[0],'string']
                    list2 = [keyPassPhrase,orgValue[1],'string']
                    list3 = [radioEnable,orgValue[2],'bool']
                    #Concatenate the lists with the elements separated by pipe
                    revertParamList = list1 + list2 + list3
                    revertParamList = "|".join(map(str, revertParamList))
                    #Revert the values to original
                    print("\nTEST STEP %d: Should set the original ssid, keypassphrase, radio enable" %step);
                    print("EXPECTED RESULT %d: Should set the original ssid, keypassphrase, radio enable" %step);
                    tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("ACTUAL RESULT %d: Details: %s" %(step, details));
                        print("[TEST EXECUTION RESULT] : SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("ACTUAL RESULT %d: Details : %s" %(step, details));
                        print("[TEST EXECUTION RESULT] : FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("ACTUAL RESULT %d: Details: %s" %(step, details));
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("ACTUAL RESULT %d: Values not retrieved successfully" %step);
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