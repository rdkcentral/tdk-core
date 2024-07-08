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
  <name>E2E_BridgeMode_CheckLocalIPConfigDisabled_OnReboot</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>When the gateway is in bridge mode check whether the local ip configuration is disabled and check if on reboot also this persists</synopsis>
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
    <box_type>Emulator</box_type>
    <!--  -->
    <box_type>RPI</box_type>

  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_482</test_case_id>
    <test_objective>When the gateway is in bridge mode check whether the local ip configuration is disabled and check if on reboot also this persists</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>1.Ccsp Components in DUT should be in a running state that includes component under test Cable Modem
2.TDK Agent should be in running state or invoke it through StartTdk.sh script</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode
Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress
Device.DHCPv4.Server.Pool.1.MinAddress
Device.DHCPv4.Server.Pool.1.MaxAddress</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Get the current LanMode and save it
3. Get the current local IP configuration and save it.
4. Set the Lanmode as bridge mode
5. Try to change the local IP configuration. Operation should fail
6. Reboot the gateway
7. Again try to change local ip config. Set operation should fail
8. Revert the Lanmode and local ip config to its initial values
9. Unload tdkb_e2e module</automation_approch>
    <except_output>When device is in bridge local ip configuration option should be disabled this behavior should persist on reboot</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_BridgeMode_CheckLocalIPConfigDisabled_OnReboot</test_script>
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
obj1 = tdklib.TDKScriptingLibrary("tdkbtr181","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_BridgeMode_CheckLocalIPConfigDisabled_OnReboot');
obj1.configureTestCase(ip,port,'E2E_BridgeMode_CheckLocalIPConfigDisabled_OnReboot');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
loadmodulestatus1 =obj1.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus1) ;

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS");
    obj1.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

        #Assign the parameters names to a variable
        ipAddress = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
        minAddress = "Device.DHCPv4.Server.Pool.1.MinAddress"
        maxAddress = "Device.DHCPv4.Server.Pool.1.MaxAddress"
        lanMode = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode"

        #Get the value of the parameters that are currently set.
        paramList=[ipAddress , minAddress, maxAddress, lanMode]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current value of Lan Ipaddress, minaddress, maxaddress, lanMode")
            print("EXPECTED RESULT 1: Should retrieve the current value of Lan Ipaddress, minaddress, maxaddress,lanMode")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            if orgValue[0]=="10.0.0.1" :
                newIp = "172.16.0.1"
                newMin = "172.16.0.2"
                newMax = "172.16.0.253"
            else:
                newIp = "10.0.0.1"
                newMin = "10.0.0.2"
                newMax = "10.0.0.253"

            status = setLanModeAndVerify(obj,'bridge-static')

            if expectedresult in status:

                setValuesList = [newIp,newMin,newMax];
                print("LAN parameter values that are set: %s" %setValuesList)

                list1 = [ipAddress, newIp,'string']
                list2 = [minAddress, newMin,'string']
                list3 = [maxAddress, newMax,'string']

                #Concatenate the lists with the elements separated by pipe
                setParamList = list1 + list2 + list3
                setParamList = "|".join(map(str, setParamList))

                #try to edit local ip config when device is in bridge mode
                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                if expectedresult not in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 2: Try to change local ip configuration")
                    print("EXPECTED RESULT 2: local ip configuration should be disabled")
                    print("SUCCESS: Local ip configuration is disabled in bridge mode")

                    #rebooting the device
                    obj1.initiateReboot();
                    sleep(300);

                     #try to edit local ip config when  bridge mode is disabled
                    tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                    if expectedresult not in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TEST STEP 3: Try to change local ip configuration after reboot")
                        print("EXPECTED RESULT 3: local ip configuration should be disabled even after reboot");
                        print("ACTUAL RESULT 3: %s" %details);
                        print("[TEST EXECUTION RESULT] : SUCCESS");

                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print("TEST STEP 3: Try to change local ip configuration after reboot")
                        print("EXPECTED RESULT 3: local ip configuration should be disabled even after reboot")
                        print("ACTUAL RESULT 3: %s" %details);
                        print("[TEST EXECUTION RESULT] : FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("FAILURE: Local ip configuration is not disabled in bridge mode")
            else:
                print("Failed to set bridge mode")

            #Prepare the list of parameter values to be reverted
            list1 = [ipAddress,orgValue[0],'string']
            list2 = [minAddress,orgValue[1],'string']
            list3 = [maxAddress,orgValue[2],'string']
            list4 = [lanMode,orgValue[3],'string']

            #Concatenate the lists with the elements separated by pipe
            revertParamList = list1 + list2 + list3 + list4
            revertParamList = "|".join(map(str, revertParamList))

            #Revert the values to original
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
            sleep(90);
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 4: Should set the original lanip,min and max addresses, lanMode")
                print("ACTUAL RESULT 4: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 4: Should set the original lanip,min and max addresses, lanMode")
                print("ACTUAL RESULT 4: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current lanip,min and max addresses, lanMode")
            print("EXPECTED RESULT 1: Should retrieve the current lanip,min and max addresses, lanMode")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : FAILURE");
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        obj.setLoadModuleStatus("FAILURE");
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup();
    obj.unloadModule("tdkb_e2e");
    obj1.unloadModule("tdkbtr181");

else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    obj1.setLoadModuleStatus("FAILURE");
    print("Module loading failed");
