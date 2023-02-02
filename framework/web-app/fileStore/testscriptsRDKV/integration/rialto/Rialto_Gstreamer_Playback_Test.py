##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2023 RDK Management
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
  <name>Rialto_Gstreamer_Playback_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Rialto_Testing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test gstreamer based playback tests with rialomsevideosink and rialtomseaudiosink</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RIALTO_PLAYBACK_01</test_case_id>
    <test_objective>To test the video playback of various streams through 'playbin', 'rialtomseaudiosink' and 'rialtomsevideosink' gst elements</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI</test_setup>
    <pre_requisite>1.TDK Agent should be up and running in the DUT
2. Test stream url should be updated in the config variable video_src_url_aac, video_src_url_dash_h264, video_src_url_ac3, video_src_url_hevc, video_src_url_vp9, video_src_url_opus, video_src_url_av1, video_src_url_eac3, video_src_url_hls inside RialtoMediaConfig.py library inside filestore
3. CHECK_AV_STATUS configuration should be set as yes/no in the device config file
4. MEDIAPLAYBACK_TIMEOUT configuration should be set to time to wait before checking for AV playback
5. SUPPORTED_CODECS must be filled as device capabilities are read from the same.</pre_requisite>
    <api_or_interface_used>Execute the mediapipelinetests application in DUT</api_or_interface_used>
    <input_parameters>testcasename - "test_rialto_playback", "test_rialto_play_pause"
test_urls - stream urls' from RialtoMediaConfig library
"checkavstatus=yes" - argument to do the video playback verification from SOC side . This argument can be yes/no based on a device configuration(CHECK_AV_STATUS) from Device Config file
timeout - a string to specify the time in seconds for which the videoplayback should be done . This argument is the value of device configuration(MEDIAPLAYBACK_TIMEOUT) from Device Config file</input_parameters>
    <automation_approch>1.Load the systemutil module
2.Retrieve the CHECK_AV_STATUS and MEDIAPLAYBACK_TIMEOUT config values from Device config file.
3.Retrieve the video_src_url variable from RialtoMediaConfig library
4. Construct the mediapipelinetests command based on the retrieved video url, testcasename, CHECK_AV_STATUS deviceconfig value and timeout
5.Execute the command in DUT. During the execution, the DUT will playback av for MEDIAPLAYBACK_TIMEOUT seconds then application exits by closing the pipeline
6.Verify the output from the execute command and check if the strings "Failures: 0" and "Errors: 0", or "failed: 0" exists in the returned output
7.Based on the ExecuteCommand() return value and the output returned from the mediapipelinetests application, TM return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1. Verify the API call is success
Checkpoint 2. Verify that the output returned from mediapipelinetests contains the strings "Failures: 0" and "Errors: 0", or "failed: 0"</expected_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>Rialto_Gstreamer_Playback_Test</test_script>
    <skipped></skipped>
    <release_version>M109</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import RialtoMediaConfig
from rialto_testUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rialto","1");
#Using systemutil library for command execution
sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1")

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Rialto_Gstreamer_Playback_Test');
sysUtilObj.configureTestCase(ip,port,'Rialto_Gstreamer_Playback_Test')

#Set device configurations to default values
checkAVStatus = "no"
timeoutInSeconds = "10"
test_urls={}
test_results={}

#Load the systemutil library
sysutilloadModuleStatus =sysUtilObj.getLoadModuleResult()
print "[System Util LIB LOAD STATUS]  :  %s" %sysutilloadModuleStatus
sysUtilObj.setLoadModuleStatus(sysutilloadModuleStatus)

if "SUCCESS" in sysutilloadModuleStatus.upper():
    expectedResult="SUCCESS"

    print "####################################################################################"
    print "            PLUGIN NAME :  Rialto Gstreamer Test"
    print "####################################################################################"

    setPreRequisite(sysUtilObj);

    #Construct the command with the url and execute the command in DUT
    tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand')

    #The test name specifies the test case to be executed from the mediapipeline test suite
    tests = ["test_rialto_playback","test_rialto_play_pause"]

    totalcases=0
    #Codecs supported by DUT
    actual_result, supported_codecs = getConfigValue (sysUtilObj, 'SUPPORTED_CODECS')
    if "EAC3" in supported_codecs:
        test_urls["EAC3"]=(RialtoMediaConfig.video_src_url_ec3)
        totalcases=totalcases+1
    if "HEVC" in supported_codecs:
        test_urls["HEVC"]=(RialtoMediaConfig.video_src_url_hevc)
        totalcases=totalcases+1
    if "AV1" in supported_codecs:
        test_urls["AV1"]=(RialtoMediaConfig.video_src_url_av1)
        totalcases=totalcases+1
    if "VP9" in supported_codecs:
        test_urls["VP9"]=(RialtoMediaConfig.video_src_url_vp9)
        totalcases=totalcases+1
    if "OPUS" in supported_codecs:
        test_urls["OPUS"]=(RialtoMediaConfig.video_src_url_opus)
        totalcases=totalcases+1
    test_urls["AAC"]=(RialtoMediaConfig.video_src_url_aac)
    test_urls["H264"]=(RialtoMediaConfig.video_src_url_dash_h264)
    test_urls["AC3"]=(RialtoMediaConfig.video_src_url_ac3)
    totalcases=totalcases+3

    print "PLUGIN TEST CASES: ",totalcases

    #Retrieve the value of configuration parameter 'MEDIAPLAYBACK_TIMEOUT' that specifies the video playback timeout in seconds
    actualresult, timeoutConfigValue = getConfigValue (sysUtilObj, 'MEDIAPLAYBACK_TIMEOUT')

    #If the value of MEDIAPLAYBACK_TIMEOUT is retrieved correctly and its value is not empty, timeout value should be passed to the test application
    #if the device config value is empty, default timeout(10sec) is passed
    if expectedResult in actualresult.upper() and timeoutConfigValue != "":
        timeoutInSeconds = timeoutConfigValue

    for test in tests:
        url_iterator = 0
        for test_url in test_urls:
            #To do the AV playback through 'playbin' element, we are using 'mediapipelinetests' test application that is available in TDK along with required parameters
            #Sample command = "mediapipelinetests test_rialto_playback <TEST_STREAM_URL> checkavstatus=yes timeout=20"
            command = getMediaPipelineTestCommand (test, test_urls[test_url], checkavstatus = checkAVStatus, timeout = timeoutInSeconds)

            ExecuteTest(sysUtilObj,test_urls.keys()[url_iterator],test,command)
            url_iterator=url_iterator+1

    ExecutePostRequisite(sysUtilObj)
    #Unload the modules
    sysUtilObj.unloadModule("systemutil")

else:
    print "Module load failed"
