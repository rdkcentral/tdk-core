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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_NotifyComp_SetAttribute_CheckLogFile</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To set attribute active and anybody to Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber and check if logs are updated in NOTIFYLog.txt.0 when there is a change to the namespace</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>25</execution_time>
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
    <test_case_id>TC_TDKB_E2E_527</test_case_id>
    <test_objective>To set attribute active and anybody to Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber and check if logs are updated in NOTIFYLog.txt.0 when there is a change to the namespace</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Get the lan mode and check if the device is in router mode
3. Get the lan client ip and get the current lan ip address dhcp range
4. Check the lan client ip is in dhcp range
5.Get the MAC address
6.Enable the notify comp logs
7.Set attribute active and anybody to Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber
8.Check if logs are updated in NOTIFYLog.txt.0
9.Unload module</automation_approch>
    <except_output>logs should be updated in NOTIFYLog.txt.0 when there is a change to the Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber</except_output>
    <priority>High</priority>
    <test_stub_interface>None</test_stub_interface>
    <test_script>E2E_NotifyComp_SetAttribute_CheckLogFile</test_script>
    <skipped>No</skipped>
    <release_version>M68</release_version>
    <remarks>None</remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import tdkbE2EUtility;
from tdkbE2EUtility import *;


#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");
obj1 = tdklib.TDKScriptingLibrary("tdkbtr181","1");
obj2 = tdklib.TDKScriptingLibrary("sysutil","1");
obj3 = tdklib.TDKScriptingLibrary("wifiagent","RDKB");



#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_NotifyComp_SetAttribute_CheckLogFile');
obj1.configureTestCase(ip,port,'E2E_NotifyComp_SetAttribute_CheckLogFile');
obj2.configureTestCase(ip,port,'E2E_NotifyComp_SetAttribute_CheckLogFile');
obj3.configureTestCase(ip,port,'E2E_NotifyComp_SetAttribute_CheckLogFile');


#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 =obj1.getLoadModuleResult();
loadmodulestatus2 =obj2.getLoadModuleResult();
loadmodulestatus3 =obj3.getLoadModuleResult();

print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus1) ;
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus2) ;
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus3) ;

if "SUCCESS" in loadmodulestatus.upper() and loadmodulestatus1.upper() and loadmodulestatus2.upper() and loadmodulestatus3.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")
        lanMode = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode"
        tdkTestObj,status,orgValue = getParameterValue(obj,lanMode)
        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current lanMode")
            print("EXPECTED RESULT 1: Should retrieve the current lanMode")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");
            print("TEST STEP 2: Check whether device is in router mode")
            #Check if device is in router mode
            if orgValue == "router":
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
                            print("lan ip address is in same DHCP range")
                            lanMAC = getLanMACAddress(tdkbE2EUtility.lan_interface)
                            if lanMAC:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("TEST STEP 6 : Get the MAC address of lan client")
                                print("MAC retrieved is %s" %lanMAC)
                                tdkTestObj = obj1.createTestStep('TDKB_TR181Stub_Set');
                                tdkTestObj.addParameter("ParamName","Device.LogAgent.X_RDKCENTRAL-COM_NotifyComp_LoggerEnable");
                                tdkTestObj.addParameter("ParamValue","true");
                                tdkTestObj.addParameter("Type","boolean");
                                #Execute the test case in DUT
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details = tdkTestObj.getResultDetails();
                                #Set the result status of execution
                                if expectedresult in actualresult:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("TEST STEP 7: Enable the notifycomp logs");
                                    print("EXPECTED RESULT 7 : Should enable the notifycomp logs")
                                    print("ACTUAL RESULT 7:notifycomp logs are enabled")
                                    #Get the result of execution
                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                    print("Waiting for ETHAgent to restart after enabling the logs")
                                    time.sleep(20);
                                    #check whether the process is running or not
                                    query="sh %s/tdk_platform_utility.sh checkProcess notify_comp" %TDK_PATH
                                    print("query:%s" %query)
                                    tdkTestObj = obj2.createTestStep('ExecuteCmd');
                                    tdkTestObj.addParameter("command", query)
                                    expectedresult="SUCCESS";
                                    tdkTestObj.executeTestCase("SUCCESS");
                                    actualresult = tdkTestObj.getResult();
                                    pid = tdkTestObj.getResultDetails().strip().replace("\\n","");
                                    if expectedresult in actualresult and pid:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("TEST STEP 8:Check notify_comp process after enabling the logs");
                                        print("EXPECTED RESULT 8: notify_comp process should be running");
                                        print("ACTUAL RESULT 8: PID of notify_comp %s" %pid);
                                        #Get the result of execution
                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                        #Prmitive test case which associated to this Script
                                        tdkTestObj = obj3.createTestStep('WIFIAgent_SetAttr');

                                        tdkTestObj.addParameter("paramname","Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber");
                                        tdkTestObj.addParameter("accessControlChanged","anybody");
                                        tdkTestObj.addParameter("notification","active");
                                        expectedresult = "SUCCESS"

                                        #Execute the test case in STB
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        details = tdkTestObj.getResultDetails();
                                        if expectedresult in actualresult:
                                            print("TEST STEP 9:Set attribute as active and anybody for Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber")
                                            print("EXPECTED RESULT 9:Should set attribute as active and anybody for Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber");
                                            print("ACTUAL RESULT 9: %s" %details);
                                            #Get the result of execution
                                            print("[TEST EXECUTION RESULT] : SUCCESS");

                                            print("Retrieving the timestamp before disconnecting the LAN client")
                                            tdkTestObj = obj2.createTestStep('ExecuteCmd');
                                            cmd = "cat /rdklogs/logs/NOTIFYLog.txt.0 | grep -i mod=NOTIFY";
                                            tdkTestObj.addParameter("command", cmd);
                                            tdkTestObj.executeTestCase(expectedresult);
                                            actualresult = tdkTestObj.getResult();
                                            details = tdkTestObj.getResultDetails().strip().replace("\\n","");
                                            oldTimestamp = details.split()[0]
                                            if expectedresult in actualresult and oldTimestamp != "":
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print("TEST STEP 10: Get the old timestamp");
                                                print("EXPECTED RESULT 10 :Should get old timestamp")
                                                print("ACTUAL RESULT 10 :old timestamp is %s" %oldTimestamp)
                                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                                print("Disconnect the lan client")
                                                status= bringdownInterface(tdkbE2EUtility.lan_interface,"LAN");
                                                if status == "SUCCESS":
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("TEST STEP 11: Check if lan client is disconnected");
                                                    print("EXPECTED RESULT 11 : LAN client should be disconnected")
                                                    print("ACTUAL RESULT 11 :LAN client is disconnected")
                                                    #Get the result of execution
                                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                                    print("Waiting to reflect the changes in log file")
                                                    time.sleep(500);
                                                    print("Retrieving the timestamp after disconnecting LAN client")
                                                    tdkTestObj = obj2.createTestStep('ExecuteCmd');
                                                    cmd = "cat /rdklogs/logs/NOTIFYLog.txt.0 | grep -i mod=NOTIFY";
                                                    tdkTestObj.addParameter("command", cmd);
                                                    tdkTestObj.executeTestCase(expectedresult);
                                                    actualresult1 = tdkTestObj.getResult();
                                                    details = tdkTestObj.getResultDetails().strip().replace("\\n","");
                                                    disconnectTimestamp = details.split()[0]
                                                    print("Timestamp after disconnecting LAN client: %s" %disconnectTimestamp)
                                                    print("Retrieving the logs in NOTIFYLog.txt.0 after disconnecting the client")
                                                    tdkTestObj = obj2.createTestStep('ExecuteCmd');
                                                    cmd = "cat /rdklogs/logs/NOTIFYLog.txt.0 | grep -i Connected-Client| grep -i %s" %lanMAC;
                                                    tdkTestObj.addParameter("command", cmd);

                                                    tdkTestObj.executeTestCase(expectedresult);
                                                    actualresult2 = tdkTestObj.getResult();
                                                    disconnectLogs = tdkTestObj.getResultDetails().strip().replace("\\n","");
                                                    print("After disconnecting LAN client logs:%s" %disconnectLogs)
                                                    if expectedresult in (actualresult1 and actualresult2) and lanMAC in disconnectLogs and "Offline" in disconnectLogs and oldTimestamp != disconnectTimestamp:
                                                        print("TEST STEP 12: Check disconnected logs are present in logfile");
                                                        print("EXPECTED RESULT 12 : Disconnected logs should be present in logfile")
                                                        print("ACTUAL RESULT 12:Disconnected logs are present")
                                                        #Get the result of execution
                                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                                    else:
                                                        print("TEST STEP 12: Disconnected logs are not present in logfile");
                                                    print("Connect the LAN client")
                                                    status= bringupInterface(tdkbE2EUtility.lan_interface,"LAN");
                                                    if status == "SUCCESS":
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        print("TEST STEP 13: Revert the changes by connecting lan client");
                                                        print("EXPECTED RESULT 13 : LAN client should be connected")
                                                        print("ACTUAL RESULT 13 :LAN client is connected")
                                                        #Get the result of execution
                                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                                        print("Waiting to reflect the changes in log file")
                                                        time.sleep(200);
                                                        print("Retrieving the timestamp after connecting the client")
                                                        tdkTestObj = obj2.createTestStep('ExecuteCmd');
                                                        cmd = "cat /rdklogs/logs/NOTIFYLog.txt.0 | grep -i mod=NOTIFY";
                                                        tdkTestObj.addParameter("command", cmd);
                                                        tdkTestObj.executeTestCase(expectedresult);
                                                        actualresult1 = tdkTestObj.getResult();
                                                        details = tdkTestObj.getResultDetails().strip().replace("\\n","");
                                                        connectTimestamp = details.split()[0]
                                                        print("Timestamp after connecting the client %s" %connectTimestamp)

                                                        print("Retrieving the logs in NOTIFYLog.txt.0 after connecting the client")
                                                        tdkTestObj = obj2.createTestStep('ExecuteCmd');
                                                        cmd = "cat /rdklogs/logs/NOTIFYLog.txt.0 | grep -i Connected-Client| grep -i %s" %lanMAC;
                                                        tdkTestObj.addParameter("command", cmd);

                                                        tdkTestObj.executeTestCase(expectedresult);
                                                        actualresult2 = tdkTestObj.getResult();
                                                        connectLogs = tdkTestObj.getResultDetails().strip().replace("\\n","");
                                                        print("After disconnecting LAN client logs:%s" %connectLogs)
                                                        if expectedresult in (actualresult1 and actualresult2) and lanMAC in connectLogs and "Online" in connectLogs and disconnectTimestamp != connectTimestamp:
                                                            print("TEST STEP 14: Check connected logs are present in logfile");
                                                            print("EXPECTED RESULT 14 : Connected logs should be present in logfile")
                                                            print("ACTUAL RESULT 14:Connected logs are present")
                                                            #Get the result of execution
                                                            print("[TEST EXECUTION RESULT] : SUCCESS");
                                                        else:
                                                            tdkTestObj.setResultStatus("FAILURE");
                                                            print("TEST STEP 14: Connected logs are not present in logfile");
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("TEST STEP 13: Failed to revert the changes by connecting lan client");
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("TEST STEP 11:lan client is not disconnected");
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP 10:Failed to get the old timestamp");
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP 9:Set attribute as for Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber failed")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 8:notify_comp process is not running after enabling the logs");
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 7: Failed to Enable the notifycomp logs");
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 6 : Failed to get the MAC address of lan client")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("TEST STEP 5: checkIpRange:lan ip address is not in DHCP range")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 4: getParameterValue : Failed to get gateway lan ip")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: getLanIPAddress:Failed to get the LAN client IP")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Device is in bridge mode")
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
    obj1.unloadModule("tdkbtr181");
    obj2.unloadModule("sysutil");
    obj3.unloadModule("wifiagent");

else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");