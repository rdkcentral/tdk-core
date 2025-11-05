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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DSHal_GetAudioCapabilities_NullParam_Check</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_GetAudioCapabilities</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to validate audio capabilities HAL api by passing null param.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>1</execution_time>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_178</test_case_id>
    <test_objective>Test script to validate the Getaudiocapabilities API by passing null param</test_objective>
    <test_type>Negative</test_type>
    <test_setup>Video_Accelerator</test_setup>
    <pre_requisite> 1.Initialize IARMBus
2.Connect IARMBus
3.Initialize dsMgr
4.Initialize DSHAL subsystems
5.Stop dsMgr.service</pre_requisite>
    <api_or_interface_used> dsError_t dsGetAudioCapabilities(intptr_t handle, int *capabilities)</api_or_interface_used>
    <input_parameters> handle - audio port handle
capabilities - address of the value to get the audio capabilities</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via test agent.
2. DSHAL agent will invoke the api dsGetAudioPort to get the handle
3. Invoke the dsGetAudioCapabilities api by passing a null param to the capabilities arguments.
4. TM checks if the dsGetAudioCapabilities returned a corresponding error code retrieved and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>1. Verify the API call is success
2. verify that handle is received
3. verify the dsGetAudioCapabilities API got returned a proper error statement</expected_output>
    <priority >High</priority>
    <test_stub_interface >libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_GetAudioCapabilities_NullParam_Check</test_script>
    <skipped>No</skipped>
    <release_version>M127</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from dshalUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("dshal","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DSHal_GetAudioCapabilities_NullParam_Check');

#Get the result of connection with test component and STB
dshalloadModuleStatus = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %dshalloadModuleStatus);

obj.setLoadModuleStatus(dshalloadModuleStatus);

if "SUCCESS" in dshalloadModuleStatus.upper():
    print("Test Step1: To get the audioport handle");
    print("Expected output: Should get the valid handle");
    expectedResult = "SUCCESS";
    # Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('DSHal_GetAudioPort');
    tdkTestObj.addParameter("portType", audioPortType["HDMI"]);
    # Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    print("DSHal_GetAudioPort result: ", actualResult)

    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        details = tdkTestObj.getResultDetails();
        print(details);

    print("Test Step2: To validate the GetAudioCapabilities HAL API by passing null param");
    print("Expected output: Should get the proper error code without facing any crashes");
    expectedResult="FAILURE";
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('DSHal_GetAudioCapabilities');
    tdkTestObj.addParameter("Isnullparamcheck",1);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    print("Expected result: ", expectedResult);
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        print(details);
        print("ACTUAL RESULT : dsGetAudioCapabilities call is failed due to null param being passed");
        tdkTestObj.setResultStatus("SUCCESS");
        print("[TEST EXECUTION RESULT] : SUCCESS");
    else:
        print("Value returned : ", details);
        print("ACTUAL RESULT : dsGetAudioCapabilities call is success eventhough null param being passed");
        tdkTestObj.setResultStatus("FAILURE");
        print("[TEST EXECUTION RESULT] : FAILURE");

    obj.unloadModule("dshal");
else:
    print("Module load failed");
