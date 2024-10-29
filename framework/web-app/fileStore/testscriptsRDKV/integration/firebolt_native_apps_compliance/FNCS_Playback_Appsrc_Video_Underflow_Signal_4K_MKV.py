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
  <name>FNCS_Playback_Appsrc_Video_Underflow_Signal_4K_MKV</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>getDeviceConfigValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify if underflow signal is captured by westerossink after reaching the amount of buffers pushed by "appsrc" element to pipeline created via "playbin" and "westerossink" gst elements</synopsis>
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
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>FNCS_PLAYBACK_300</test_case_id>
    <test_objective>To verify if underflow signal is captured by westerossink after reaching the amount of buffers pushed by "appsrc" element to pipeline created via "playbin" and "westerossink" gst elements</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK TV,Video Accelerator</test_setup>
    <pre_requisite>1.tdk_mediapipelinetests application should be installed in the DUT
2. Test stream url for an Appsrc_Video_Underflow_Signal_4k_MKV stream should be updated in the config variable video_src_url_4k_av1_mkv inside MediaValidationVariables.py library inside filestore
3. FIREBOLT_COMPLIANCE_CHECK_AV_STATUS configuration should be set as yes/no in the device config file
4. FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK configuration should be set as yes/no in the device config file for advanced playback validation
5. FIREBOLT_COMPLIANCE_CHECK_PTS configuration should be set as yes/no in the device config file for validating video pts
6. FIREBOLT_COMPLIANCE_CHECK_FPS configuration should be set as yes/no in the device config file for validating video frames</pre_requisite>
    <api_or_interface_used>gstreamer-1.0</api_or_interface_used>
    <input_parameters>testcasename - "test_appsrc_video_underflow_signal"
test_url - Appsrc_Video_Underflow_Signal_4k_MKV url from MediaValidationVariables library (MediaValidationVariables.video_src_url_h264_30fps)
"checkavstatus=yes" - argument to do the video playback verification from SOC side . This argument can be yes/no based on a device configuration(FIREBOLT_COMPLIANCE_CHECK_AV_STATUS) from Device Config file
"checkFPS=yes" argument to get the video frames. This argument can be yes/no based on a device configuration(FIREBOLT_COMPLIANCE_CHECK_FPS)
"checkAudioFPS=yes" - argument to get the audio frames. This argument can be yes/no based on a device configuration(FIREBOLT_COMPLIANCE_CHECK_AUDIO)
"checkPTS=yes" - argument to get the video PTS . This argument can be yes/no based on a device configuration(FIREBOLT_COMPLIANCE_CHECK_PTS)
"validateFullPlayback" - argument for advanced playback validation . This argument can be yes/no based on a device configuration(FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK)
underflow_threshold - this is the amount of bytes pushed via "appsrc" into pipeline to trigger video underflow</input_parameters>
    <automation_approch>1.Initiate SSH connection to execute command remotely.
2.Retrieve the FIREBOLT_COMPLIANCE_CHECK_AV_STATUS, FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK,FIREBOLT_COMPLIANCE_CHECK_PTS,FIREBOLT_COMPLIANCE_CHECK_FPS, FIREBOLT_COMPLIANCE_CHECK_AUDIO config values from Device config file.
3.Retrieve the video_src_url_4k_av1_mkv variable from MediaValidationVariables library
4.Construct the tdk_mediapipelinetests command based on the retrieved video url, testcasename and configurations
5.Execute the command in DUT. During the execution, the DUT will playback with the above configuration set in pre_requisites then application exits by closing the pipeline
6.Appsrc will be set with the threshold and only that amount of buffers will be sent to playbin, playbin will be set to PLAYING state subsequently.
7.An underflow signal will be triggered upon reaching the end of the buffers sent to appsrc. Verify that underflow signal is captured by westerossink and exit the testcase.
8.Verify the output from the execute command and check if the strings "Failures: 0" and "Errors: 0", or "failed: 0" exists in the returned output.
9.Based on the ExecuteCommand() return value and the output returned from the tdk_mediapipelinetests application, TM return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>1. Verify the API call is success
Checkpoint 2. Verify that the output returned from tdk_mediapipelinetests contains the strings "Failures: 0" and "Errors: 0", or "failed: 0"</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdk_mediapipelinetests</test_stub_interface>
    <test_script>FNCS_Playback_Appsrc_Video_Underflow_Signal_4K_MKV</test_script>
    <skipped>No</skipped>
    <release_version>M130</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import MediaValidationVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("firebolt_native_apps_compliance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'FNCS_Playback_Appsrc_Video_Underflow_Signal_4K_MKV');

#Set device configurations to default values
checkAVStatus = "no"

#Threshold value for appsrc
threshold = "38940939"
#Get the result of connection with test component in DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
expectedResult="SUCCESS"

if "SUCCESS" in result.upper():
    
    #The test name specifies the test case to be executed from the mediapipeline test suite
    test_name = "test_appsrc_video_underflow_signal"
    #Test url for the stream to be played is retrieved from MediaValidationVariables library
    test_url = MediaValidationVariables.video_src_url_4k_av1_mkv

    #Retrieve the value of configuration parameter 'FIREBOLT_COMPLIANCE_CHECK_AV_STATUS' that specifies whether SOC level playback verification check should be done or not
    tdkTestObj = obj.createTestStep('getDeviceConfigValue')
    tdkTestObj.addParameter("configKey","FIREBOLT_COMPLIANCE_CHECK_AV_STATUS")
    tdkTestObj.executeTestCase(expectedResult);
    actualresult = tdkTestObj.getResult();
    check_av_status_flag = tdkTestObj.getResultDetails();
    #If the value of FIREBOLT_COMPLIANCE_CHECK_AV_STATUS is retrieved correctly and its value is "yes", argument to check the SOC level AV status should be passed to test application
    if expectedResult in actualresult.upper() and check_av_status_flag == "yes":
        print("Video Decoder proc check is added")
        checkAVStatus = check_av_status_flag

    #Sample command = "tdk_mediapipelinetests test_appsrc_video_underflow_signal <Appsrc_Video_Underflow_Signal_MKV_STREAM_URL> checkavstatus=yes timeout=20"
    arguments = {"checkavstatus" : checkAVStatus}

    tdkTestObj = obj.createTestStep('getMediaPipelineTestCommand')
    tdkTestObj.addParameter("arguments",str(arguments))
    tdkTestObj.addParameter("test_name",test_name)
    tdkTestObj.addParameter("test_url",test_url)
    tdkTestObj.executeTestCase(expectedResult);
    command = tdkTestObj.getResultDetails();

    #Set underflow threshold for appsrc
    command = command + " underflow_threshold="
    command = command + threshold + " "

    #Remove use_appsrc from command as this test definitely uses appsrc
    command = command.replace("use_appsrc", "")
    print("Executing command in DUT: ", command)

    tdkTestObj = obj.createTestStep('executeCmndInDUT') 
    tdkTestObj.addParameter("command",command)
    tdkTestObj.executeTestCase(expectedResult);

    output = tdkTestObj.getResultDetails().replace(r'\n', '\n'); output = output[output.find('\n'):]
    print("OUTPUT: ...\n", output)
    #Check if the command executed successfully
    if expectedResult in actualresult.upper() and output:
        #Check the output string returned from 'mediapipelinetests' to verify if the test suite executed successfully
        tdkTestObj = obj.createTestStep('checkMediaPipelineTestStatus')
        tdkTestObj.addParameter("outputString",output)
        tdkTestObj.executeTestCase(expectedResult);
        executionStatus = tdkTestObj.getResultDetails()

        if expectedResult in executionStatus:
            tdkTestObj.setResultStatus("SUCCESS")
            print("SUCCESS : Received underflow signal upon reaching end of buffers pushed by appsrc")
            print("Mediapipeline test executed successfully")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            if "Failed to receive buffer underflow signal" in output:
                print("FAILURE : Failed to receive underflow signal after reaching end of buffers pushed by appsrc")
            else:
                print("Mediapipeline test execution failed")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("Mediapipeline test execution failed")

obj.unloadModule("firebolt_native_apps_compliance");
