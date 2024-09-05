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
  <name>DSHal_Get_MISteering_Reboot_Persist</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DSHal_GetMISteering</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To enable or disable the MI Steering status with reboot scenario</synopsis>
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
    <test_case_id>CT_DS_HAL_198</test_case_id>
    <test_objective>To enable or disable the MI Steering status in reboot scenario</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator,RDKTV</test_setup>
    <pre_requisite>1. Initialize IARMBus
2. Connect IARMBus
3. Initialize dsMgr
4. Initialize DSHAL subsystems</pre_requisite>
    <api_or_interface_used>dsGetAudioPort(dsAudioPortType_t type, int index, int *handle)
dsError_t dsGetMS12Capabilities(intptr_t handle, int *capabilities)
dsError_t  dsGetMISteering(intptr_t handle, bool *enabled)
dsError_t  dsSetMISteering(intptr_t handle, bool enabled)</api_or_interface_used>
    <input_parameters>type - Audio port type
index- Audio port index
handle - Audio port handle
capabilities - to get the platform supported MS12 capability feature lists.
enabled - MI Steering enabled(1)/disabled(0) value</input_parameters>
    <automation_approch>1. TM loads the DSHAL agent via the test agent.
2. DSHAL agent will invoke the api dsGetMS12Capabilities to check whether MI Steering feature got supported in platform or not.
3. If feature is supported verify the enabled/disabled value in reboot scenario using dsGetMISteering and dsSetMISteering API.
3. TM checks if the status is correct and return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1.Verify the API call is success
Checkpoint 2 Verify that the status is correct
Checkpoint 3 If MI Steering feature is not supported in source device, then always it should return dsERR_OPERATION_NOT_SUPPORTED</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdshalstub.so.0.0.0</test_stub_interface>
    <test_script>DSHal_Get_MISteering_Reboot_Persist</test_script>
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
dshalObj.configureTestCase(ip,port,'DSHal_Get_MISteering_Reboot_Persist');

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

        # get the platform supported MS12 capabiliites to check whether the MISteering feature is supported or not
        tdkTestObj = dshalObj.createTestStep('DSHal_GetMS12Capabilities');
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult:
            print("dsGetMS12Capabilities API call is getting succeeded");
            tdkTestObj.setResultStatus("SUCCESS");
            if "MI Steering" in details:
                print("MI Steering feature is supported");
                MI_Steering_enabled = 1;
            else:
                print("MI Steering feature is not supported");
                MI_Steering_enabled = 0;
        else:
            print("dsGetMS12Capabilities API call is getting failed");
            print(details);
            tdkTestObj.setResultStatus("FAILURE");

        # get the box type & assign the expected result based on the MI Steering feature enabled
        boxtype = dshalObj.getDeviceBoxType();
        if boxtype in "Video_Accelerator":
            print("Box type: Video accelerator");
            if MI_Steering_enabled == 0:
                expectedResult="FAILURE";
                source_device_failure_handlings = 1;
            else:
                expectedResult="SUCCESS";
                source_device_failure_handlings = 0;
        else:
            expectedResult="SUCCESS";
            print("Box type: RDKTV");
            source_device_failure_handlings = 0;

        print("\nTEST STEP 1 : Get the MISteering value using dsGetMISteering API");
        if source_device_failure_handlings:
            print("EXPECTED OUTPUT : dsGetMISteering API should return dsERR_OPERATION_NOT_SUPPORTED for source device if this feature is not supported");
        else:
            print("EXPECTED OUTPUT : Should get the current MISteering status value");
        #Get the current MI Steering enabled status
        tdkTestObj = dshalObj.createTestStep('DSHal_GetMISteering');
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print("DSHal_GetMISteering expected result: ", expectedResult);
        print("DSHal_GetMISteering actual result: ", actualResult);
        if expectedResult in actualResult:
            # if box type is in STB and MISteering feature is not supported then expected o/p is OP_NOT_SUPPORTED
            if source_device_failure_handlings:
                expectederrorVal = "dsERR_OPERATION_NOT_SUPPORTED";
                print(details);
                if expectederrorVal in details:
                    print("dsGetMISteering API returned an expected value : dsERR_OPERATION_NOT_SUPPORTED");
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    print("dsGetMISteering API returned an error value other than the expected value : dsERR_OPERATION_NOT_SUPPORTED");
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                tdkTestObj.setResultStatus("SUCCESS");
                MISteeringEnabled = tdkTestObj.getResultDetails();
                print("MISteering status retrieved : ", MISteeringEnabled);
                cur_status = MISteeringEnabled;
                print("Test step 2 : to Enable the MISteering & reboot the device");
                #Disable surround decoder status if its enabled
                tdkTestObj = dshalObj.createTestStep('DSHal_SetMISteering');
                tdkTestObj.addParameter("enable",1);
                expectedResult="SUCCESS";
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();

                if expectedResult in actualResult:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("\nTEST STEP 3 : Device will going to reboot")
                    dshalObj.initiateReboot();
                        
                    print("\nTEST STEP 4 : Get the MISteering enabled status using dsGetMISteering API");
                    print("EXPECTED OUTPUT : Should get enabled status as set before reboot using dsGetMISteering API");
                    #Check SurroundDecoderEnabled status
                    tdkTestObj = dshalObj.createTestStep('DSHal_GetMISteering');
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    print("DSHal_GetMISteering result: ", actualResult)
                    if expectedResult in actualResult:
                        enable = int(str(details).split(":",1)[1].strip())
                        if enable:
                            print("MISteering is enabled.");
                            tdkTestObj.setResultStatus("SUCCESS");
                        else:
                            print("MISteering is disabled. But it was enabled before reboot");
                            tdkTestObj.setResultStatus("FAILURE");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print(details);
                        print("Failed to get GetMISteering status");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    details = tdkTestObj.getResultDetails();
                    print(details);
                    print("dsSetMISteering API call getting failed");
                
                #re-assigned the last status after execuing the script
                print("Test step to set the last MISteering enabled status");
                #Disable surround decoder status if its enabled
                tdkTestObj = dshalObj.createTestStep('DSHal_SetMISteering');
                tdkTestObj.addParameter("enable",cur_status);
                expectedResult="SUCCESS";
                tdkTestObj.executeTestCase(expectedResult);
                actualResult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                if expectedResult in actualResult:
                    #Check SurroundDecoderEnabled status
                    tdkTestObj = dshalObj.createTestStep('DSHal_GetMISteering');
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedResult);
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    print("DSHal_GetMISteering result: ", actualResult)
                    if expectedResult in actualResult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        enable = int(str(details).split(":",1)[1].strip())
                        if enable:
                            print("MISteering is enabled.");
                        else:
                            print("MISteering is disabled.");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print(details);
                        print("Failed to get MISteering status");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    details = tdkTestObj.getResultDetails();
                    print(details);
                    print("dsSetMISteering API call getting failed");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            details = tdkTestObj.getResultDetails();
            print(details);
            if source_device_failure_handlings:
                print("ACTUAL RESULT : dsGetMISteering call is success instead of returning dsERR_OPERATION_NOT_SUPPORTED");
            else:
                print("Failed to get MISteering status");
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print("AudioPort handle not retrieved");

    dshalObj.unloadModule("dshal");

else:
    print("Module load failed");
