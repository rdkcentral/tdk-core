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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_CM_VerifyCMStatus</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify whether the Operational status of Wireless Gateway got through TR-181 Parameter (Device.X_CISCO_COM_CableModem.CMStatus) matches with the actual status of WG. (value: OPERATIONAL)</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>30</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
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
    <test_case_id>TC_TDKB_E2E_191</test_case_id>
    <test_objective>Verify whether the Operational status of Wireless Gateway got through TR-69 Parameter (Device.X_CISCO_COM_CableModem.CMStatus) matches with the actual status of WG. (value: OPERATIONAL)</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband</test_setup>
    <pre_requisite>CMAgent should be up and running in the DUT</pre_requisite>
    <api_or_interface_used>tdkb_e2e_Get</api_or_interface_used>
    <input_parameters>Device.X_CISCO_COM_CableModem.CMStatus</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get the current CM status and check whether the CM status is returned as OPERATIONAL
3. Connect to the LAN client and check the IP address of the LAN client.
4. Check whether the LAN client is able to ping to Gateway IP when CM Status is Operational
5. Unload tdkb_e2e module</automation_approch>
    <except_output>LAN client should be able to ping to Gateway IP when CM Status is Operational</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_CM_VerifyCMStatus</test_script>
    <skipped>No</skipped>
    <release_version>M53</release_version>
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

obj.configureTestCase(ip,port,'E2E_CM_VerifyCMStatus');

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

        #Get the current CM Status
        param = "Device.X_CISCO_COM_CableModem.CMStatus"
        tdkTestObj,status,cmStatus = getParameterValue(obj,param)

        if expectedresult in status and cmStatus == "OPERATIONAL":
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current CM Status")
            print("EXPECTED RESULT 1: Should retrieve the current CM Status")
            print("ACTUAL RESULT 1: %s" %cmStatus);
            print("[TEST EXECUTION RESULT] : %s" %status);

            #Connect to LAN client and obtain its IP
            print("TEST STEP 2: Get the IP address of the lan client after connecting to it")
            lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
            if lanIP:
                tdkTestObj.setResultStatus("SUCCESS");
                print("LAN Client IP Address: %s" %lanIP)

                print("TEST STEP 3: Get the current LAN IP address of the Gateway")
                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                tdkTestObj,status,gatewayIP = getParameterValue(obj,param)
                print("Gateway IP Address: %s" %gatewayIP);

                if expectedresult in status and gatewayIP:
                    tdkTestObj.setResultStatus("SUCCESS");

                    print("TEST STEP 4:Check whether the LAN client is able to ping to Gateway IP when CM Status is Operational")
                    status = verifyNetworkConnectivity(gatewayIP, "PING", lanIP, gatewayIP,"LAN")
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("Ping to Gateway IP from LAN Client: SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 4: Failed to Ping to Gateway IP from LAN Client")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Failed to get the LAN IP address of the Gateway")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Failed to get the IP address of the LAN client")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current CM Status")
            print("EXPECTED RESULT 1: Should retrieve the current CM Status")
            print("ACTUAL RESULT 1: %s" %cmStatus);
            print("[TEST EXECUTION RESULT] : %s" %status);
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