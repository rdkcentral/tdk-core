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
  <name>DSHal_Get_AudioLevel_Reboot_Persist</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_GetAudioLevel</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify the set and get Audio level value in reboot scenario</synopsis>
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
    <box_type>RDKTV</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DS_HAL_203</test_case_id>
    <test_objective>To verify the set and get Audio level in reboot scenario</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator,RDKTV</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetAudioPort(dsAudioPortType_t type, int index, int *handle)
dsError_t  dsSetAudioLevel(intptr_t handle, float level)
dsError_t  dsGetAudioLevel(intptr_t handle, float *level)</api_or_interface_used>
    <input_parameters>type - Audio port type
index- Audio port index
handle - Audio port handle
level - returns the current audio vol level of speaker and headphone which connected in sink devices</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2 . DSHAL agent will invoke the api dsGetAudioLevel and dsSetAudioLevel to set/get audio vol level and verify the persistence in reboot case too.
3. TM checks if the status is correct and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success
Checkpoint 2 Verify that the volume level is same after reboot
Checkpoint 3 If the connected boxtype is video_accelerator then always should return dsERR_OPERATION_NOT_SUPPORTED</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_Get_AudioLevel_Reboot_Persist</test_script>
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
dshalObj.configureTestCase(ip,port,'DSHal_Get_AudioLevel_Reboot_Persist');

#Get the result of connection with test component and STB
dshalloadModuleStatus = dshalObj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %dshalloadModuleStatus);

dshalObj.setLoadModuleStatus(dshalloadModuleStatus);
boxtype = dshalObj.getDeviceBoxType();

if "SUCCESS" in dshalloadModuleStatus.upper():
    expectedResult="SUCCESS";
    #Primitive test case which associated to this Script
    tdkTestObj = dshalObj.createTestStep('DSHal_GetAudioPort');
    if boxtype in "Video_Accelerator":
        audiotype = "HDMI";
    else:
        audiotype = "SPEAKER";
    tdkTestObj.addParameter("portType", audioPortType[audiotype]);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    print("DSHal_GetAudioPort result: ", actualResult)
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        details = tdkTestObj.getResultDetails();
        print(details);

        # get the box type & assign the expected result based on the Graphic equalizer feature enabled
        if boxtype in "Video_Accelerator":
            print("Box type: Video accelerator");
            expectedResult="FAILURE";
            source_device_failure_handlings = 1;
        else:
            expectedResult="SUCCESS";
            print("Box type: RDKTV");
            source_device_failure_handlings = 0;

        print("\nTEST STEP 1 : Get the current audio volume level of an audio port speaker using dsGetAudioLevel API");
        if source_device_failure_handlings:
            print("EXPECTED OUTPUT : dsGetAudioLevel API should return dsERR_OPERATION_NOT_SUPPORTED always for source device");
        else:
            print("EXPECTED OUTPUT : Should get the current audio volume level");
        #Get the current MI Steering enabled status
        tdkTestObj = dshalObj.createTestStep('DSHal_GetAudioLevel');
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print("DSHal_GetAudioLevel expected result: ", expectedResult);
        print("DSHal_GetAudioLevel actual result: ", actualResult)
        if expectedResult in actualResult:
            # if box type is in STB then expected o/p is OP_NOT_SUPPORTED always
            if source_device_failure_handlings:
                expectederrorVal = "dsERR_OPERATION_NOT_SUPPORTED";
                print(details);
                if expectederrorVal in details:
                    print("dsGetAudioLevel API returned an expected value : dsERR_OPERATION_NOT_SUPPORTED");
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    print("dsGetAudioLevel API returned an error value other than the expected value : dsERR_OPERATION_NOT_SUPPORTED");
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                tdkTestObj.setResultStatus("SUCCESS");
                details = tdkTestObj.getResultDetails();
                #mode = int(str(details).split(":",1)[1].strip());
                mode = float(str(details).split(":",1)[1].strip());
                print("Audio volume level retrieved : ", mode);
                cur_status = mode;
                print("TEST STEP 2 : To set the audio volume level as 50 & reboot the device");
                print("EXPECTED OUTPUT : Should set the audio volume level as 50");
                #Disable surround decoder status if its enabled
                tdkTestObj = dshalObj.createTestStep('DSHal_SetAudioLevel');
                tdkTestObj.addParameter("audiolevel",50);
                expectedResult="SUCCESS";
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();

                if expectedResult in actualResult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("\nTEST STEP 3 : Device will going to reboot")
                    dshalObj.initiateReboot();
                        
                    print("\nTEST STEP 4 : Get the audio volume level using dsGetAudioLevel API");
                    print("EXPECTED OUTPUT : Should get value as set before reboot using dsSetAudioLevel API");
                    #Check SurroundDecoderEnabled status
                    tdkTestObj = dshalObj.createTestStep('DSHal_GetAudioLevel');
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    print("DSHal_GetAudioLevel actual result: ", actualResult)
                    if expectedResult in actualResult:
                        #mode = int(str(details).split(":",1)[1].strip());
                        mode = float(str(details).split(":",1)[1].strip());
                        print("Audio volume level retrieved : ", mode);
                        if mode == 50:
                            print("Received the correct audio volume level which set before reboot.");
                            tdkTestObj.setResultStatus("SUCCESS");
                        else:
                            print("Received the incorrect audio volume level which it wasn't set before reboot");
                            tdkTestObj.setResultStatus("FAILURE");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print(details);
                        print("Failed to get AudioLevel");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    details = tdkTestObj.getResultDetails();
                    print(details);
                    print("dsSetAudioLevel API call getting failed");
                
                #re-assigned the last status after execuing the script
                print("Test step to set/retain the last audio dB level");
                #Disable surround decoder status if its enabled
                tdkTestObj = dshalObj.createTestStep('DSHal_SetAudioLevel');
                tdkTestObj.addParameter("audiolevel",cur_status);
                expectedResult="SUCCESS";
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                if expectedResult in actualResult:
                    #Check SurroundDecoderEnabled status
                    tdkTestObj = dshalObj.createTestStep('DSHal_GetAudioLevel');
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    print("DSHal_GetAudioLevel actual result: ", actualResult)
                    if expectedResult in actualResult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        #mode = int(str(details).split(":",1)[1].strip());
                        mode = float(str(details).split(":",1)[1].strip());
                        print("Audio volume level retrieved : ", mode);
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print(details);
                        print("Failed to get AudioLevel");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    details = tdkTestObj.getResultDetails();
                    print(details);
                    print("dsSetAudioLevel API call getting failed");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            details = tdkTestObj.getResultDetails();
            print(details);
            if source_device_failure_handlings:
                print("ACTUAL RESULT : dsGetAudioLevel call is success instead of returning dsERR_OPERATION_NOT_SUPPORTED");
            else:
                print("Failed to get AudioLevel");
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print("AudioPort handle not retrieved");

    dshalObj.unloadModule("dshal");

else:
    print("Module load failed");
