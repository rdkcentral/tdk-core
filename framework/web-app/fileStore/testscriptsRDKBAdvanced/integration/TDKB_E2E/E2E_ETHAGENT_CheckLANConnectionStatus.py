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
  <name>E2E_ETHAGENT_CheckLANConnectionStatus</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To disconnect  and connect lan client and check if it is updated in  ETHAGENTLog.txt.0</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>20</execution_time>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_518</test_case_id>
    <test_objective>To disconnect  and connect lan client and check if it is updated in  ETHAGENTLog.txt.0</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,RPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.Hosts.X_CISCO_COM_ConnectedDeviceNumber</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. import selenium module
3. Get the lan mode and check if the device is in router mode
4. Get the lan client ip and get the current lan ip address dhcp range
5. Check the lan client ip is in dhcp range
6. Get the MAC Address of lan IP
7. Enable ethagent logs
8. Check if ETHAgent process is running after enabling the logs
9. Get the logs before bringing down lan client
10.Bring down the lan client
11.Check if the logs are updated in ETHAGENTLog.txt.0 with timestamp
12.Bring up the lan client
13.Check if the logs are updated in ETHAGENTLog.txt.0
14. unload module</automation_approch>
    <except_output>After connecting and disconnecting lan client logs should be updated in Check if the logs are updated in ETHAGENTLog.txt.0</except_output>
    <priority>High</priority>
    <test_stub_interface>None</test_stub_interface>
    <test_script>E2E_ETHAGENT_CheckLANConnectionStatus</test_script>
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

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_ETHAGENT_CheckLANConnectionStatus');
obj1.configureTestCase(ip,port,'E2E_ETHAGENT_CheckLANConnectionStatus');
obj2.configureTestCase(ip,port,'E2E_ETHAGENT_CheckLANConnectionStatus');

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
                            macAddress = lanMAC.upper()
                            if macAddress:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("TEST STEP 6 : Get the MAC address of lan client")
                                print("MAC retrieved is %s" %macAddress)
                                tdkTestObj = obj1.createTestStep('TDKB_TR181Stub_Set');
                                tdkTestObj.addParameter("ParamName","Device.LogAgent.X_RDKCENTRAL-COM_EthAgent_LoggerEnable");
                                tdkTestObj.addParameter("ParamValue","true");
                                tdkTestObj.addParameter("Type","boolean");
                                #Execute the test case in DUT
                                tdkTestObj.executeTestCase(expectedresult);
                                actualresult = tdkTestObj.getResult();
                                details = tdkTestObj.getResultDetails();
                                #Set the result status of execution
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("TEST STEP 7: Enable the ETHAgent logs");
                                print("EXPECTED RESULT 7 : Should enable the ETHAgent logs")
                                print("ACTUAL RESULT 7:ETHAgent logs are enabled")
                                #Get the result of execution
                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                print("Waiting for ETHAgent to restart after enabling the logs")
                                time.sleep(60);
                                #check whether the process is running or not
                                query="sh %s/tdk_platform_utility.sh checkProcess CcspEthAgent" %TDK_PATH
                                print("query:%s" %query)
                                tdkTestObj = obj2.createTestStep('ExecuteCmd');
                                tdkTestObj.addParameter("command", query)
                                expectedresult="SUCCESS";
                                tdkTestObj.executeTestCase("SUCCESS");
                                actualresult = tdkTestObj.getResult();
                                pid = tdkTestObj.getResultDetails().strip().replace("\\n","");
                                if expectedresult in actualresult and pid:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print("TEST STEP 8:Check CcspEthAgent process after enabling the logs");
                                    print("EXPECTED RESULT 8: CcspEthAgent process should be running");
                                    print("ACTUAL RESULT 8: PID of CcspEthAgent %s" %pid);
                                    #Get the result of execution
                                    print("[TEST EXECUTION RESULT] : SUCCESS");
                                    tdkTestObj = obj2.createTestStep('ExecuteCmd');
                                    cmd = "tail -1 n /rdklogs/logs/ETHAGENTLog.txt.0";
                                    tdkTestObj.addParameter("command",cmd);
                                    tdkTestObj.executeTestCase(expectedresult);
                                    actualresult = tdkTestObj.getResult();
                                    orglogs = tdkTestObj.getResultDetails();
                                    print("Initial EthAgentLog:%s" %orglogs)
                                    oldTimestamp = orglogs.split()[0]
                                    print("Disconnect the lan client")
                                    status= bringdownInterface(tdkbE2EUtility.lan_interface,"LAN");
                                    if status == "SUCCESS":
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("TEST STEP 9: Check if lan client is disconnected");
                                        print("EXPECTED RESULT 9 : LAN client should be disconnected")
                                        print("ACTUAL RESULT 9 :LAN client is disconnected")
                                        #Get the result of execution
                                        print("[TEST EXECUTION RESULT] : SUCCESS");
                                        print("Waiting to reflect the changes in log file")
                                        time.sleep(550);
                                        tdkTestObj = obj2.createTestStep('ExecuteCmd');
                                        cmd = "tail -1 n /rdklogs/logs/ETHAGENTLog.txt.0";
                                        tdkTestObj.addParameter("command",cmd);
                                        tdkTestObj.executeTestCase(expectedresult);
                                        actualresult = tdkTestObj.getResult();
                                        disconnectedlogs = tdkTestObj.getResultDetails();
                                        print("Log after LAN Disconnect:%s" %disconnectedlogs)
                                        newTimestamp = disconnectedlogs.split()[0]
                                        if macAddress in disconnectedlogs and "Disconnected" in disconnectedlogs and oldTimestamp != newTimestamp:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("TEST STEP 10: Check if disconnected logs are present");
                                            print("EXPECTED RESULT 10: Disconnected logs should be present")
                                            print("ACTUAL RESULT 10:Disconnected logs are present")
                                            #Get the result of execution
                                            print("[TEST EXECUTION RESULT] : SUCCESS");
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP 10: disconnected logs are not present");
                                        status= bringupInterface(tdkbE2EUtility.lan_interface,"LAN");
                                        if status == "SUCCESS":
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print("TEST STEP 11: Check if lan client is connected");
                                            print("EXPECTED RESULT 11 : LAN client should be connected")
                                            print("ACTUAL RESULT 11 :LAN client is connected")
                                            #Get the result of execution
                                            print("[TEST EXECUTION RESULT] : SUCCESS");
                                            print("Waiting to reflect the changes in log file")
                                            time.sleep(200);
                                            tdkTestObj = obj2.createTestStep('ExecuteCmd');
                                            cmd = "tail -1 n /rdklogs/logs/ETHAGENTLog.txt.0";
                                            tdkTestObj.addParameter("command",cmd);
                                            tdkTestObj.executeTestCase(expectedresult);
                                            actualresult = tdkTestObj.getResult();
                                            connectlogs = tdkTestObj.getResultDetails();
                                            print("Log after LAN Connect:%s" %connectlogs)
                                            newConnectTimestamp = connectlogs.split()[0]
                                            if macAddress in connectlogs and "Connected" in connectlogs and newTimestamp != newConnectTimestamp:
                                                tdkTestObj.setResultStatus("SUCCESS");
                                                print("TEST STEP 12: Check if connected logs are present");
                                                print("EXPECTED RESULT 12: connected logs should be present")
                                                print("ACTUAL RESULT 12:connected logs are present")
                                                #Get the result of execution
                                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP 12: Check if connected logs are present");
                                                print("EXPECTED RESULT 12: connected logs should be present")
                                                print("ACTUAL RESULT 12:connected logs are not present")
                                                #Get the result of execution
                                                print("[TEST EXECUTION RESULT] : FAILURE");
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP 11: Failed to bring up the lan interface");
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 9: Disconnected logs are not present in ethagent log file");
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 8:CCSPETHAgent is not running after enabling the logs");
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 6:Failed to get MAC Address")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("TEST STEP 5:checkIpRange:lan ip address is not in DHCP range")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 4:getParameterValue : Failed to get gateway lan ip")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3:getLanIPAddress:Failed to get the LAN client IP")
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

else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");