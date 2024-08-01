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
  <name>DSHal_GetAudioFormat</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_GetAudioFormat</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to check the current audio format.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <test_case_id>CT_DS_HAL_177</test_case_id>
    <test_objective>Test script to get the audio format of the current playback</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator</test_setup>
    <pre_requisite> 1.Initialize IARMBus
2.Connect IARMBus
3.Initialize dsMgr
4.Initialize DSHAL subsystems
5.Stop dsMgr.service</pre_requisite>
    <api_or_interface_used> dsError_t  dsGetAudioFormat(intptr_t handle, dsAudioFormat_t *audioFormat)</api_or_interface_used>
    <input_parameters> handle - audio port handle
audioFormat - address of the value to get the current audio format</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via test agent.
2. DSHAL agent will invoke the api dsGetAudioPort to get the handle
3. Invoke the dsGetAudioFormat api to get the current playing content audio format.
4. TM checks if the audioformat retrieved and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>1. Verify the API call is success
2. verify that handle is received
3. verify the current audio format got received successfully</expected_output>
    <priority >High</priority>
    <test_stub_interface >libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_GetAudioFormat</test_script>
    <skipped>No</skipped>
    <release_version>M127</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
import time;
from mediautilslib import *;
from dshalUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("dshal","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DSHal_GetAudioFormat');

#Get the result of connection with test component and STB
dshalloadModuleStatus = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %dshalloadModuleStatus);

obj.setLoadModuleStatus(dshalloadModuleStatus);

playtimeout=60;

if "SUCCESS" in dshalloadModuleStatus.upper():
    tdkTestObj = obj.createTestStep('DSHal_GetAudioPort');
    result = play(obj,playtimeout);
    expectedResult="SUCCESS";
    print("Test Step1: Stream playback");
    print("Expected result: Should trigger playback successfully");
    if result:
        print("DSHal_ExecuteCmd call is successful and playback triggered");
        
        tdkTestObj.addParameter("portType", audioPortType["HDMI"]);
        # Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        print("DSHal_GetAudioPort result: ", actualResult)
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            details = tdkTestObj.getResultDetails();
            print(details);

        print("Test Step2: Retrieve the current audio format");
        print("Expected result: Should return the current playback audio format");
        tdkTestObj = obj.createTestStep('DSHal_GetAudioFormat');
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        print("Expected result: ", expectedResult);
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult:
            print(details);
            print("ACTUAL RESULT : dsGetAudioFormat call is success");
            tdkTestObj.setResultStatus("SUCCESS");
            print("[TEST EXECUTION RESULT] : SUCCESS");
        else:
            print("Value returned : ",details);
            print("ACTUAL RESULT : dsGetAudioFormat call is failed");
            tdkTestObj.setResultStatus("FAILURE");
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        print("DSHal_ExecuteCmd call unsuccessful and playback not triggered");
        tdkTestObj.setResultStatus("FAILURE");

    obj.unloadModule("dshal");
else:
    print("Module load failed");
