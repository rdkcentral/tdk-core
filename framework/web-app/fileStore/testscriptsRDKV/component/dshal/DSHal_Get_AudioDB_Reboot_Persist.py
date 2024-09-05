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
  <name>DSHal_Get_AudioDB_Reboot_Persist</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_GetAudioDB</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify the set and get Audio dB value in reboot scenario</synopsis>
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
    <test_case_id>CT_DS_HAL_202</test_case_id>
    <test_objective>To verify the set and get Audio dB value in reboot scenario</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator,RDKTV</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetAudioPort(dsAudioPortType_t type, int index, int *handle)
dsError_t  dsGetAudioDB(intptr_t handle, fload *audiodB)
dsError_t  dsSetAudioDB(intptr_t handle, fload audiodB)</api_or_interface_used>
    <input_parameters>type - Audio port type
index- Audio port index
handle - Audio port handle
audiodB - audio dB level to set and get</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2 . DSHAL agent will invoke the api dsGetAudioDB and dsSetAudioDB to get and set the audio dB level and verify the same in reboot.
3. TM checks if the status is correct and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success
Checkpoint 2 Verify that the status is correct<
Checkpoint 3 If boxtype is video_accelerator then always it should return dsERR_OPERATION_NOT_SUPPORTED/expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_Get_AudioDB_Reboot_Persist</test_script>
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
dshalObj.configureTestCase(ip,port,'DSHal_Get_AudioDB_Reboot_Persist');

#Get the result of connection with test component and STB
dshalloadModuleStatus = dshalObj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %dshalloadModuleStatus);

dshalObj.setLoadModuleStatus(dshalloadModuleStatus);

if "SUCCESS" in dshalloadModuleStatus.upper():
    expectedResult="SUCCESS";
    #Primitive test case which associated to this Script
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

        # get the box type & assign the expected result
        boxtype = dshalObj.getDeviceBoxType();
        if boxtype in "Video_Accelerator":
            print("Box type: Video accelerator");
            expectedResult="FAILURE";
            source_device_failure_handlings = 1;
        else:
            expectedResult="SUCCESS";
            print("Box type: RDKTV");
            source_device_failure_handlings = 0;

        print("\nTEST STEP 1 : Get the current audio dB value of an audio port using dsGetAudioDB API");
        if source_device_failure_handlings:
            print("EXPECTED OUTPUT : dsGetAudioDB API should return dsERR_OPERATION_NOT_SUPPORTED always for source device");
        else:
            print("EXPECTED OUTPUT : Should get the current audio dB value");
        #Get the current MI Steering enabled status
        tdkTestObj = dshalObj.createTestStep('DSHal_GetAudioDB');
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print("DSHal_GetAudioDB expected result: ", expectedResult);
        print("DSHal_GetAudioDB actual result: ", actualResult)
        if expectedResult in actualResult:
            # if box type is in STB then expected o/p is OP_NOT_SUPPORTED always
            if source_device_failure_handlings:
                expectederrorVal = "dsERR_OPERATION_NOT_SUPPORTED";
                print(details);
                if expectederrorVal in details:
                    print("dsGetAudioDB API returned an expected value : dsERR_OPERATION_NOT_SUPPORTED");
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    print("dsGetAudioDB API returned an error value other than the expected value : dsERR_OPERATION_NOT_SUPPORTED");
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                tdkTestObj.setResultStatus("SUCCESS");
                details = tdkTestObj.getResultDetails();
                mode = float(str(details).split(":",1)[1].strip());
                print("Audio dB level retrieved : ", mode);
                cur_status = mode;
                print("TEST STEP 2 : To set the audio dB value as 10 & reboot the device");
                print("EXPECTED OUTPUT : Should set the audio gain value as 10");
                #Set AudiodB value as 10
                tdkTestObj = dshalObj.createTestStep('DSHal_SetAudioDB');
                tdkTestObj.addParameter("audiodBlevel",10);
                expectedResult="SUCCESS";
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();

                if expectedResult in actualResult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("\nTEST STEP 3 : Device will going to reboot")
                    dshalObj.initiateReboot();
                        
                    print("\nTEST STEP 4 : Get the audio dB level using dsGetAudioDB API");
                    print("EXPECTED OUTPUT : Should get value as set before reboot using dsSetAudioDB API");
                    #Check SurroundDecoderEnabled status
                    tdkTestObj = dshalObj.createTestStep('DSHal_GetAudioDB');
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    print("DSHal_GetAudioDB actual result: ", actualResult)
                    if expectedResult in actualResult:
                        mode = float(str(details).split(":",1)[1].strip());
                        print("Audio dB level retrieved : ", mode);
                        if mode == 10:
                            print("Received the correct audio dB level which set before reboot.");
                            tdkTestObj.setResultStatus("SUCCESS");
                        else:
                            print("Received the incorrect audio dB level which it wasn't set before reboot");
                            tdkTestObj.setResultStatus("FAILURE");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print(details);
                        print("Failed to get GetAudioDB");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    details = tdkTestObj.getResultDetails();
                    print(details);
                    print("dsSetAudioDB API call getting failed");
                
                #re-assigned the last status after execuing the script
                print("Test step to set/retain the last audio dB level");
                #Disable surround decoder status if its enabled
                tdkTestObj = dshalObj.createTestStep('DSHal_SetAudioDB');
                tdkTestObj.addParameter("audiodBlevel",cur_status);
                expectedResult="SUCCESS";
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                if expectedResult in actualResult:
                    #Check SurroundDecoderEnabled status
                    tdkTestObj = dshalObj.createTestStep('DSHal_GetAudioDB');
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    print("DSHal_GetAudioDB actual result: ", actualResult)
                    if expectedResult in actualResult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        mode = float(str(details).split(":",1)[1].strip());
                        print("Audio dB level retrieved : ", mode);
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print(details);
                        print("Failed to get audio dB level");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    details = tdkTestObj.getResultDetails();
                    print(details);
                    print("dsSetAudioDB API call getting failed");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            details = tdkTestObj.getResultDetails();
            print(details);
            if source_device_failure_handlings:
                print("ACTUAL RESULT : dsGetAudioDB call is success instead of returning dsERR_OPERATION_NOT_SUPPORTED");
            else:
                print("Failed to get audio dB level");
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print("AudioPort handle not retrieved");

    dshalObj.unloadModule("dshal");

else:
    print("Module load failed");
