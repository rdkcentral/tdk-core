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
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import MediaValidationVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("native_playback_validation_suite","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'NPVS_Appsrc_Video_Underflow_Signal_H264');

#Set device configurations to default values
checkAVStatus = "no"

#Threshold value for appsrc
threshold = "2796910"
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
expectedResult="SUCCESS"

if "SUCCESS" in result.upper():
    
    #The test name specifies the test case to be executed from the mediapipeline test suite
    test_name = "test_appsrc_video_underflow_signal"
    #Test url for the stream to be played is retrieved from MediaValidationVariables library
    test_url = MediaValidationVariables.video_src_url_mp4_30fps

    #Retrieve the value of configuration parameter 'NATIVE_PLAYBACK_CHECK_AV_STATUS' that specifies whether SOC level playback verification check should be done or not
    tdkTestObj = obj.createTestStep('getDeviceConfigValue')
    tdkTestObj.addParameter("configKey","NATIVE_PLAYBACK_CHECK_AV_STATUS")
    tdkTestObj.executeTestCase(expectedResult);
    actualresult = tdkTestObj.getResult();
    check_av_status_flag = tdkTestObj.getResultDetails();
    #If the value of NATIVE_PLAYBACK_CHECK_AV_STATUS is retrieved correctly and its value is "yes", argument to check the SOC level AV status should be passed to test application
    if expectedResult in actualresult.upper() and check_av_status_flag == "yes":
        print("Video Decoder proc check is added")
        checkAVStatus = check_av_status_flag

    #Sample command = "mediapipelinetests test_generic_playback <Appsrc_Video_Underflow_Signal_H264_STREAM_URL> checkavstatus=yes timeout=20"
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

obj.unloadModule("native_playback_validation_suite");
