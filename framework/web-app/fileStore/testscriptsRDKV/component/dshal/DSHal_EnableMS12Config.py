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
  <name>DSHal_EnableMS12Config</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_EnableMS12Config</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to enable MS12 config features.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
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
    <box_type>RDKTV</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_181</test_case_id>
    <test_objective>Test script to check the return value of EnableMS12Config HAL API to ensure really it got deprecated in HAL implementation</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDKTV,Video_Accelerator</test_setup>
    <pre_requisite> 1.Initialize IARMBus
2.Connect IARMBus
3.Initialize dsMgr
4.Initialize DSHAL subsystems
5.Stop dsMgr.service</pre_requisite>
    <api_or_interface_used>dsError_t dsEnableMS12Config(intptr_t handle, dsMS12FEATURE_t feature,const bool enable);</api_or_interface_used>
    <input_parameters> handle - audio port handle
feature - MS12 config feature enum values
bool - enable or disable the given input feature</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via test agent.
2. DSHAL agent will invoke the api dsGetAudioPort to get the handle
3. Invoke the dsEnableMS12Config api to set the the supported audio formats.
4. TM checks the retrieved status of the HAL api and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>1. Verify the API call is success
2. verify that handle is received
3. verify the API returned operation not supported as defined in the HAL spec since this feature got deprecated</expected_output>
    <priority >High</priority>
    <test_stub_interface >libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_EnableMS12Config</test_script>
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
obj.configureTestCase(ip,port,'DSHal_EnableMS12Config');

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

    expectedResult="FAILURE";
    print("Test Step2: To enable DAPV2 MS12 feature using dsEnableMS12Config API");
    print("Expected output: Should get operation not supported since this functionality is deprecated as per HAL spec");
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('DSHal_EnableMS12Config');
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    print("Expected result: ", expectedResult);
    print("Actual result: ", actualResult);
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        expectederrorVal = "dsERR_OPERATION_NOT_SUPPORTED";
        print(details);
        if expectederrorVal in details:
            printk("EnableMS12Config API returned an expected value : dsERR_OPERATION_NOT_SUPPORTED");
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            printk("EnableMS12Config API returned an error value other than the expected value : dsERR_OPERATION_NOT_SUPPORTED");
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print(details);
        print("EnableMS12 config is not returning an expected error value");
        tdkTestObj.setResultStatus("FAILURE");

    obj.unloadModule("dshal");
else:
    print("Module load failed");
