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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>DSHal_EnableSurroundDecoder</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_EnableSurroundDecoder</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To enable or disable the audio surround decoder status</synopsis>
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
    <test_case_id>CT_DS_HAL_185</test_case_id>
    <test_objective>To enable or disable the audio surround decoder status</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator,RDKTV</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetAudioPort(dsAudioPortType_t type, int index, int *handle)
dsError_t  dsEnableSurroundDecoder(intptr_t handle, bool enabled)
dsError_t  dsIsSurroundDecoderEnabled(intptr_t handle, bool *enabled)
dsError_t dsGetMS12Capabilities(intptr_t handle, int *capabilities)</api_or_interface_used>
    <input_parameters>type - Audio port type
index- Audio port index
handle - Audio port handle
enabled - Surround Decoder enabled(1)/disabled(0) value
capabilities - to get the platform supported MS12 capabaility fields</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2 . DSHAL agent will invoke the api dsIsSurroundDecoderEnabled and dsEnableSurroundDecoder to get/set surround devcoder status.
3. TM checks if the status is correct and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success
Checkpoint 2 Verify that the status is correct
Checkpoint 3 If surround decoder feature is not supported in source device then API should return always dsERR_OPERATION_NOT_SUPPORTED</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_EnableSurroundDecoder</test_script>
    <skipped>No</skipped>
    <release_version>M128</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from dshalUtility import *;

#Test component to be tested
dshalObj = tdklib.TDKScriptingLibrary("dshal","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
dshalObj.configureTestCase(ip,port,'DSHal_EnableSurroundDecoder');

#Get the result of connection with test component and STB
dshalloadModuleStatus = dshalObj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %dshalloadModuleStatus);

dshalObj.setLoadModuleStatus(dshalloadModuleStatus);

if "SUCCESS" in dshalloadModuleStatus.upper():
    expectedResult="SUCCESS";
    #Prmitive test case which associated to this Script
    tdkTestObj = dshalObj.createTestStep('DSHal_GetAudioPort');
    tdkTestObj.addParameter("portType", audioPortType["HDMI"]);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    print("DSHal_GetAudioPort result: ", actualResult)
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        details = tdkTestObj.getResultDetails();
        print(details);

        # get the platform supported MS12 capabiliites to check whether the surround decoder is supported or not
        tdkTestObj = dshalObj.createTestStep('DSHal_GetMS12Capabilities');
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult:
            print("dsGetMS12Capabilities API call is getting succeeded");
            tdkTestObj.setResultStatus("SUCCESS");
            if "Surround Decoder" in details:
                print("Surround Decoder feature is supported");
                surround_enabled = 1;
            else:
                print("Surround Decoder feature is not supported");
                surround_enabled = 0;
        else:
            print("dsGetMS12Capabilities API call is getting failed");
            print(details);
            tdkTestObj.setResultStatus("FAILURE");

        # get the box type & assign the expected result based on the surround decoder feature enabled
        boxtype = dshalObj.getDeviceBoxType();
        if boxtype in "Video_Accelerator":
            print("Box type: Video accelerator");
            if surround_enabled == 0:
                expectedResult="FAILURE";
                source_device_failure_handlings = 1;
            else:
                expectedResult="SUCCESS";
                source_device_failure_handlings = 0;
        else:
            expectedResult="SUCCESS";
            print("Box type: RDKTV");
            source_device_failure_handlings = 0;

        print("\nTEST STEP 1 : Get the surround decoder enable status using dsIsSurroundDecoderEnabled API");
        if source_device_failure_handlings:
            print("EXPECTED OUTPUT : dsIsSurroundDecoderEnabled API should return dsERR_OPERATION_NOT_SUPPORTED for source device if this feature is not supported");
        else:
            print("EXPECTED OUTPUT : Should get the current surround decoder enabled status");

        #Check SurroundDecoderEnabled status
        tdkTestObj = dshalObj.createTestStep('DSHal_IsSurroundDecoderEnabled');
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print("DSHal_IsSurroundDecoderEnabled expected result: ", expectedResult);
        print("DSHal_IsSurroundDecoderEnabled actual result: ", actualResult);
        if expectedResult in actualResult:
            # if box type is in STB then expected o/p is OP_NOT_SUPPORTED
            if source_device_failure_handlings:
                expectederrorVal = "dsERR_OPERATION_NOT_SUPPORTED";
                print(details);
                if expectederrorVal in details:
                    print("IsSurroundDecoderEnabled API returned an expected value : dsERR_OPERATION_NOT_SUPPORTED");
                    tdkTestObj.setResultStatus("SUCCESS");
                    tdkTestObj = dshalObj.createTestStep('DSHal_EnableSurroundDecoder');
                    tdkTestObj.addParameter("enable",1);
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    if expectederrorVal in details:
                        print("EnableSurroundDecoder API returned an expected value : dsERR_OPERATION_NOT_SUPPORTED");
                        tdkTestObj.setResultStatus("SUCCESS");
                    else:
                        print("EnableSurroundDecoder API returned an error value other than the expected value : dsERR_OPERATION_NOT_SUPPORTED");
                        tdkTestObj.setResultStatus("FAILURE");
                else:
                    print("IsSurroundDecoderEnabled API returned an error value other than the expected value : dsERR_OPERATION_NOT_SUPPORTED");
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                tdkTestObj.setResultStatus("SUCCESS");
                IsSurroundDecoderEnabled = tdkTestObj.getResultDetails();
                print("SurroundDecoderEnabled status retrieved : ", IsSurroundDecoderEnabled);
                cur_status = IsSurroundDecoderEnabled;
                if details:
                    print("SurroundDecoder is Enabled.. Test step to disable the Surround decoder");
                    #Disable surround decoder status if its enabled
                    tdkTestObj = dshalObj.createTestStep('DSHal_EnableSurroundDecoder');
                    tdkTestObj.addParameter("enable",0);
                    expectedResult="SUCCESS";
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    if expectedResult in actualResult:
                         #Check SurroundDecoderEnabled status
                         tdkTestObj = dshalObj.createTestStep('DSHal_IsSurroundDecoderEnabled');
                         #Execute the test case in STB
                         tdkTestObj.executeTestCase(expectedResult);
                         actualResult = tdkTestObj.getResult();
                         details = tdkTestObj.getResultDetails();
                         print("DSHal_IsSurroundDecoderEnabled result: ", actualResult)
                         if expectedResult in actualResult:
                             if details:
                                 print("Surround decoder is not disabled.");
                                 tdkTestObj.setResultStatus("FAILURE");
                             else:
                                 print("Surround decoder is disabled successfully");
                                 tdkTestObj.setResultStatus("SUCCESS");
                         else:
                             tdkTestObj.setResultStatus("FAILURE");
                             details = tdkTestObj.getResultDetails();
                             print(details);
                             print("Failed to get SurroundDecoderEnabled status");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print(details);
                        print("EnableSurroundDecoder API call getting failed");
                else:
                    print("SurroundDecoder is Disabled.. Test step to enable the Surround decoder");
                    #Disable surround decoder status if its enabled
                    tdkTestObj = dshalObj.createTestStep('DSHal_EnableSurroundDecoder');
                    tdkTestObj.addParameter("enable",1);
                    expectedResult="SUCCESS";
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    if expectedResult in actualResult:
                        #Check SurroundDecoderEnabled status
                        tdkTestObj = dshalObj.createTestStep('DSHal_IsSurroundDecoderEnabled');
                        #Execute the test case in STB
                        tdkTestObj.executeTestCase(expectedResult);
                        actualResult = tdkTestObj.getResult();
                        details = tdkTestObj.getResultDetails();
                        print("DSHal_IsSurroundDecoderEnabled result: ", actualResult)
                        if expectedResult in actualResult:
                            if details:
                                print("Surround decoder is enabled succesfully.");
                                tdkTestObj.setResultStatus("SUCCESS");
                            else:
                                print("Surround decoder is not enabled.");
                                tdkTestObj.setResultStatus("FAILURE");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            details = tdkTestObj.getResultDetails();
                            print(details);
                            print("Failed to get SurroundDecoderEnabled status");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print(details);
                        print("EnableSurroundDecoder API call getting failed");
                #re-assigned the last status after execuing the script
                print("Test step to set the last Surround decoder status");
                #Disable surround decoder status if its enabled
                tdkTestObj = dshalObj.createTestStep('DSHal_EnableSurroundDecoder');
                tdkTestObj.addParameter("enable",cur_status);
                expectedResult="SUCCESS";
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                if expectedResult in actualResult:
                    #Check SurroundDecoderEnabled status
                    tdkTestObj = dshalObj.createTestStep('DSHal_IsSurroundDecoderEnabled');
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    print("DSHal_IsSurroundDecoderEnabled result: ", actualResult)
                    if expectedResult in actualResult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        if details:
                            print("Surround decoder is enabled.");
                        else:
                            print("Surround decoder is disabled.");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print(details);
                        print("Failed to get SurroundDecoderEnabled status");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    details = tdkTestObj.getResultDetails();
                    print(details);
                    print("EnableSurroundDecoder API call getting failed");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            details = tdkTestObj.getResultDetails();
            print(details);
            if source_device_failure_handlings:
                print("ACTUAL RESULT : dsIsSurroundDecoderEnabled call is success instead of returning dsERR_OPERATION_NOT_SUPPORTED");
            else:
                print("Failed to get SurroundDecoderEnabled status");
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print("AudioPort handle not retrieved");

    dshalObj.unloadModule("dshal");

else:
    print("Module load failed");
