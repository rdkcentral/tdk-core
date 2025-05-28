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
<?xml version="1.0" encoding="UTF-8"?>
<xml>
  <id/>
  <version>2</version>
  <name>E2E_SANITY_RemoteManagement_HTTPS_FromAnyIPToGateway</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Set different HTTPS port and check whether they are accessible from any computer</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Broadband</box_type>
    <box_type>Emulator</box_type>
    <box_type>RPI</box_type>
  <box_type>BPI</box_type></box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_408</test_case_id>
    <test_objective>Set different HTTPS port and check whether they are accessible from any computer</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>"Device.UserInterface.X_CISCO_COM_RemoteAccess.HttpsEnable"
"Device.UserInterface.X_CISCO_COM_RemoteAccess.FromAnyIP"</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save remote access variables
4. Enable HTTPS and enable access from any computer from WAN side and set a random port number to https port
5.  Connect to the WAN client and check whether HTTPS from WAN to WAN ip of GW is success
6.Unload tdkb_e2e module</automation_approch>
    <except_output>HTTPS should be success from WAN to gateway</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_SANITY_RemoteManagement_HTTPS_FromAnyIPToGateway</test_script>
    <skipped>No</skipped>
    <release_version>M59</release_version>
    <remarks>WAN</remarks>
  </test_cases>
  <script_tags>
    <script_tag>BASIC</script_tag>
  </script_tags>
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
obj.configureTestCase(ip,port,'E2E_SANITY_RemoteManagement_HTTPS_FromAnyIPToGateway');

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
        httpsEnable = "Device.UserInterface.X_CISCO_COM_RemoteAccess.HttpsEnable"
        fromAnyIP = "Device.UserInterface.X_CISCO_COM_RemoteAccess.FromAnyIP"
        httpsPort = "Device.UserInterface.X_CISCO_COM_RemoteAccess.HttpsPort"

        #Get the value of parameters that are currently set.
        paramList=[httpsEnable,fromAnyIP,httpsPort]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current status of httpsEnable,httpsPort and fromAnyIP")
            print("EXPECTED RESULT 1: Should retrieve the current status of httpsEnable,httpsPort and fromAnyIP")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            # Set the lanIPAddress,lanSubnetMask,minAddress and maxAddress"
            setValuesList = ['true','true',tdkbE2EUtility.remote_access_https_port];
            print("Parameter values that are set: %s" %setValuesList)


            list1 = [httpsEnable,'true','bool']
            list2 = [fromAnyIP,'true','bool']
            list3 = [httpsPort,tdkbE2EUtility.remote_access_https_port,'unsignedint']

            #Concatenate the lists with the elements separated by pipe
            setParamList= list1 + list2 + list3
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set httpsEnable,https port and fromAnyIP")
                print("EXPECTED RESULT 2: Should set httpsEnable, https port and fromAnyIP");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");

                #Retrieve the values after set and compare
                newParamList=[httpsEnable,fromAnyIP,httpsPort]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current httpsEnable,https port and fromAnyIP")
                    print("EXPECTED RESULT 3: Should retrieve the current httpsEnable,https port and fromAnyIP")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    #Wait for the changes to reflect in client device
                    time.sleep(60);
                    gwHttpsPort = newValues[2];
                    status = wgetToGateway(tdkbE2EUtility.gw_wan_ip, "WGET_HTTPS", tdkbE2EUtility.wan_ip, gwHttpsPort, "WAN")
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS");
                        finalStatus = "SUCCESS";
                        print("SUCCESS: HTTPS from WAN to WAN ip of GW with different https port is success")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("FAILURE: HTTPS from WAN to WAN ip of GW with different https port is blocked")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current httpsEnable,htp port and fromAnyIP")
                    print("EXPECTED RESULT 3: Should retrieve the current httpsEnable, https port and fromAnyIP")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 2: Set httpsEnable, https port and fromAnyIP")
                print("EXPECTED RESULT 2: Should set httpsEnable, https port and fromAnyIP");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");

            #Prepare the list of parameter values to be reverted

            list1 = [httpsEnable,orgValue[0],'bool']
            list2 = [fromAnyIP,orgValue[1],'bool']
            list3 = [httpsPort,orgValue[2],'unsignedint']

            #Concatenate the lists with the elements separated by pipe
            revertParamList = list1 + list2 + list3
            revertParamList = "|".join(map(str, revertParamList))

            #Revert the values to original
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
            if expectedresult in actualresult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 4: Should set the original httpsEnable,https port and fromAnyIP");
                print("ACTUAL RESULT 4: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 4: Should set the original httpsEnable,https port and fromAnyIP");
                print("ACTUAL RESULT 4: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current  httpsEnable,https port and fromAnyIP")
            print("EXPECTED RESULT 1: Should retrieve the current httpsEnable,https port and fromAnyIP")
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