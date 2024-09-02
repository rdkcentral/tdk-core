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
  <name>DSHal_GetMS12AudioProfileList</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_GetMS12AudioProfileList</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to get the platform supported MS12 audio profiles.</synopsis>
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
    <box_type>Video_Accelerator</box_type>
    <box_type>RDKTV</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_195</test_case_id>
    <test_objective >Test script to get the platform supported MS12 audio profiles</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator,RDKTV</test_setup>
    <pre_requisite> 1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems
5. Stop dsMgr.service</pre_requisite>
    <api_or_interface_used>dsError_t  dsGetMS12AudioProfileList(intptr_t handle, dsMS12AudioProfileList_t* profiles)</api_or_interface_used>
    <input_parameters> handle - audio port handle
profiles - return the list of supported audio profiles.</input_parameters>
    <automation_approch >1. TM loads the DSHAL agent via test agent.
2. DSHAL agent will invoke the api dsGetAudioPort to get the handle
3. Invoke the dsGetMS12AudioProfileList api to get the supported audio profiles.
4. TM checks if the supported audio profiles retrieved sucessfully and return SUCCESS/FAILURE status based on that</automation_approch>
    <expected_output>1. Verify the API call is success
2. verify that handle is received
3. verify the supported audio profiles got received successfully or not
4. If execution is on source device then dsGetMS12AudioProfileList api should return dsERR_OPERATION_NOT_SUPPORTED</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_GetMS12AudioProfileList</test_script>
    <skipped>No</skipped>
    <release_version>M128</release_version>
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
obj.configureTestCase(ip,port,'DSHal_GetMS12AudioProfileList');

#Get the result of connection with test component and STB
dshalloadModuleStatus = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %dshalloadModuleStatus);

obj.setLoadModuleStatus(dshalloadModuleStatus);

if "SUCCESS" in dshalloadModuleStatus.upper():
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

        # get the box type & assign the expected result
        boxtype = obj.getDeviceBoxType();
        if boxtype in "Video_Accelerator":
            print("Box type: Video accelerator");
            expectedResult="FAILURE";
            source_device_failure_handlings = 1;
        else:
            expectedResult="SUCCESS";
            print("Box type: RDKTV");
            source_device_failure_handlings = 0;

        print("\nTEST STEP 1 : Get the current audio profiles using dsGetMS12AudioProfileList API");
        if source_device_failure_handlings:
            print("EXPECTED OUTPUT : dsGetMS12AudioProfileList API should return dsERR_OPERATION_NOT_SUPPORTED always for source device");
        else:
            print("EXPECTED OUTPUT : Should get the current audio profile");

        #Prmitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('DSHal_GetMS12AudioProfileList');
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        print("Expected result: ", expectedResult);
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult:
            # if box type is in STB then expected o/p is OP_NOT_SUPPORTED
            if source_device_failure_handlings:
                expectederrorVal = "dsERR_OPERATION_NOT_SUPPORTED";
                print(details);
                if expectederrorVal in details:
                    print("GetMS12AudioProfileList API returned an expected value : dsERR_OPERATION_NOT_SUPPORTED");
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    print("GetMS12AudioProfileList API returned an error value other than the expected value : dsERR_OPERATION_NOT_SUPPORTED");
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                print(details);
                print("ACTUAL RESULT  : dsGetMS12AudioProfileList call is success");
                tdkTestObj.setResultStatus("SUCCESS");
        else:
            print(details);
            if source_device_failure_handlings:
                print("ACTUAL RESULT : dsGetMS12AudioProfileList call is success instead of returning dsERR_OPERATION_NOT_SUPPORTED");
            else:
                print("ACTUAL RESULT  : dsGetMS12AudioProfileList call failed")
            tdkTestObj.setResultStatus("FAILURE");
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print("AudioPort handle not retrieved");

    obj.unloadModule("dshal");
else:
    print("Module load failed");
