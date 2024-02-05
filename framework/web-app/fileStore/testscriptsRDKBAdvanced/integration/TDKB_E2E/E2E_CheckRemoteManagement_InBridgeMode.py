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
  <version>10</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_CheckRemoteManagement_InBridgeMode</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>When gateway is in bridge mode check if remote management is working as expected</synopsis>
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


  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_484</test_case_id>
    <test_objective>When gateway is in bridge mode check if remote management is working as expected</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>A WAN client should be configured for testing</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.UserInterface.X_CISCO_COM_RemoteAccess.HttpEnable
Device.UserInterface.X_CISCO_COM_RemoteAccess.FromAnyIP
Device.UserInterface.X_CISCO_COM_RemoteAccess.HttpPort
Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save remote access variables and current lanMode
3. Enable remote access from any computer from WAN side via HTTP
4. Enable bridge  mode
5. From a WAN machine check if Gateway's WAN ip is accessible or not
6. Revert  lanMode to its original value
7. Revert remote access variables to its original value
8. Unload tdkb_e2e module</automation_approch>
    <except_output>Remote access should work properly even when gateway is in bridge mode</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_CheckRemoteManagement_InBridgeMode</test_script>
    <skipped>No</skipped>
    <release_version>M64</release_version>
    <remarks>WAN</remarks>
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
obj.configureTestCase(ip,port,'E2E_CheckRemoteManagement_InBridgeMode');

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
        httpEnable = "Device.UserInterface.X_CISCO_COM_RemoteAccess.HttpEnable"
        fromAnyIP = "Device.UserInterface.X_CISCO_COM_RemoteAccess.FromAnyIP"
        httpPort = "Device.UserInterface.X_CISCO_COM_RemoteAccess.HttpPort"
        lanMode = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanMode"

        #Get the value of parameters that are currently set.
        paramList=[httpEnable,fromAnyIP,httpPort,lanMode]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current status of httpEnable,httpPort,fromAnyIP,lanMode")
            print("EXPECTED RESULT 1: Should retrieve the current status of httpEnable,httpPort ,fromAnyIP,lanMode")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            # Set the httpEnable,fromAnyIP
            setValuesList = ['true','true'];
            print("Parameter values that are set: %s" %setValuesList)

            list1 = [httpEnable,'true','bool']
            list2 = [fromAnyIP,'true','bool']

            #Concatenate the lists with the elements separated by pipe
            setParamList= list1 + list2
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set httpEnable, fromAnyIP")
                print("EXPECTED RESULT 2: Should set httpEnable, fromAnyIP");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
                time.sleep(60);

                #Retrieve the values after set and compare
                newParamList=[httpEnable,fromAnyIP]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current httpEnable, fromAnyIP")
                    print("EXPECTED RESULT 3: Should retrieve the current httpEnable, fromAnyIP")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    #set the lanmode as bridge and verify
                    status = setLanModeAndVerify(obj,'bridge-static')

                    if expectedresult in status:
                        gwHttpPort = orgValue[2];
                        print("TEST STEP 4: Check if Remote access to WAN ip of GW is success")
                        print("EXPECTED RESULT 4: Remote access to WAN ip of GW should be success")
                        status = wgetToGateway(tdkbE2EUtility.gw_wan_ip, "WGET_HTTP", tdkbE2EUtility.wan_ip, gwHttpPort, "WAN")
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS");
                            finalStatus = "SUCCESS";
                            print("ACTUAL RESULT 4: SUCCESS")
                            print("SUCCESS: Remote access to WAN ip of GW is success")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("ACTUAL RESULT 4: FAILURE")
                            print("FAILURE: Remote access to WAN ip of GW is blocked")
                        #revert the LanMode to its original value
                        status = setLanModeAndVerify(obj,orgValue[3])
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("Failed to set bridge mode")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current httpEnable and fromAnyIP")
                    print("EXPECTED RESULT 3: Should retrieve the current httpEnable, fromAnyIP, lanMode")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Set httpEnable and fromAnyIP")
                print("EXPECTED RESULT 2: Should set httpEnable, fromAnyIP");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");

            #Prepare the list of parameter values to be reverted

            list1 = [httpEnable,orgValue[0],'bool']
            list2 = [fromAnyIP,orgValue[1],'bool']

            #Concatenate the lists with the elements separated by pipe
            revertParamList = list1 + list2
            revertParamList = "|".join(map(str, revertParamList))

            #Revert the values to original
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
            if expectedresult in actualresult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 4: Should set the original httpEnable, fromAnyIP");
                print("ACTUAL RESULT 4: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 4: Should set the original httpEnable, fromAnyIP");
                print("ACTUAL RESULT 4: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current  httpEnable and fromAnyIP")
            print("EXPECTED RESULT 1: Should retrieve the current httpEnable, fromAnyIP, lanMode")
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