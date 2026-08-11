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
obj.configureTestCase(ip,port,'RDKV_CERT_NPVS_FastForward_2x_AV1');

#Set device configurations to default values
checkAVStatus = "no"
timeoutInSeconds = "10"

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
expectedResult="SUCCESS"

if "SUCCESS" in result.upper():
    
    #The test name specifies the test case to be executed from the mediapipeline test suite
    test_name = "test_trickplay"
    #Test url for the stream to be played is retrieved from MediaValidationVariables library
    test_url = MediaValidationVariables.video_src_url_av1

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


    #Retrieve the value of configuration parameter 'NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT' that specifies the video playback timeout in seconds
    tdkTestObj = obj.createTestStep('getDeviceConfigValue')
    tdkTestObj.addParameter("configKey","NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT")
    tdkTestObj.executeTestCase(expectedResult);
    actualresult = tdkTestObj.getResult();
    timeoutConfigValue = tdkTestObj.getResultDetails();

    #If the value of NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT is retrieved correctly and its value is not empty, timeout value should be passed to the test application
    #if the device config value is empty, default timeout(10sec) is passed
    if expectedResult in actualresult.upper() and timeoutConfigValue != "":
        timeoutInSeconds = timeoutConfigValue

    #Construct the trickplay operation string
    #The operations specifies the operation(fastforward/rewind/seek/play/pause) to be executed from the mediapipeline trickplay test
    # Sample operations strings is "operations=fastforward2x:20"
    tdkTestObj = obj.createTestStep('setOperations')
    tdkTestObj.addParameter("operation","fastforward2x")
    tdkTestObj.addParameter("arguments",str(timeoutInSeconds))
    tdkTestObj.executeTestCase(expectedResult);
    setresult = tdkTestObj.getResultDetails();

    tdkTestObj = obj.createTestStep('getOperations')
    tdkTestObj.executeTestCase(expectedResult);
    operations = tdkTestObj.getResultDetails();

    #Sample command = "mediapipelinetests test_trickplay <AV1_STREAM_URL> checkavstatus=yes timeout=20"
    arguments = {"checkavstatus" : checkAVStatus,"operations": operations}

    tdkTestObj = obj.createTestStep('getMediaPipelineTestCommand')
    tdkTestObj.addParameter("arguments",str(arguments))
    tdkTestObj.addParameter("test_name",test_name)
    tdkTestObj.addParameter("test_url",test_url)
    tdkTestObj.executeTestCase(expectedResult);
    command = tdkTestObj.getResultDetails();

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
            print("AV1 Playback using 'playbin' and 'westeros-sink' was successfull")
            print("Mediapipeline test executed successfully")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("AV1 Playback using 'playbin' and 'westeros-sink' failed")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("Mediapipeline test execution failed")

obj.unloadModule("native_playback_validation_suite");
