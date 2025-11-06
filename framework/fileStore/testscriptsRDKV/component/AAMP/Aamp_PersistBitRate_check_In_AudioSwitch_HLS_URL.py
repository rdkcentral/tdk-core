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
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Aamp_PersistBitRate_check_In_AudioSwitch_HLS_URL</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Aamp_AampPersistBitRateOverSeek</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to verify the bitrate persistence during audio track switching scenarios on HLS stream</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>true</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Video_Accelerator</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Aamp_90</test_case_id>
    <test_objective>Test script to verify the bitrate persistence during audio track switching scenarios on HLS stream</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator,RPI</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper tuning URLs</pre_requisite>
    <api_or_interface_used>AampTune
AampStop
AampSetVideoBitrate
AampGetVideoBitrate
AampPersistBitRateOverSeek
AampGetAvailableAudioTracks
AampGetAudioTrack
AampSetAudioTrack</api_or_interface_used>
    <input_parameters>HLS URL</input_parameters>
    <automation_approch>1. TM loads the Aamp Agent.
2. Aamp Agent invokes Tune API with HLS URL
3. Aamp Agent invokes GetVideoBitrate API to get the current bitrage
4. Aamp Agent invokes Aamp Stop API
5. Aamp Agent invokes SetVideoBitrates API with a supported different bitrate other than the default one.
6. Aamp Agent invokes PersistBitRateOverSeek API with the argument true to verify the enable persist functionality.
7. Aamp Agent invokes SetAudioTrack to select the next available autio track.
8. Aamp Agent invokes GetVideoBitrate API to check the value whether is it persisted or not. 
9. TM checks the value and returns SUCCESS/FAILURE
10. TM unloads the Aamp Agent</automation_approch>
    <expected_output>Should persist the video bitrate value even after switching to the different audio track</expected_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0</test_stub_interface>
    <test_script>Aamp_PersistBitRate_check_In_AudioSwitch_HLS_URL</test_script>
    <skipped>No</skipped>
    <release_version>M130</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import aampUtilitylib;
from time import sleep;
from tdkvutility import *

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
#Test component to be tested
aampObj = tdklib.TDKScriptingLibrary("aamp","2.0");
aampObj.configureTestCase(ip,port,'Aamp_PersistBitRate_check_In_AudioSwitch_HLS_URL');
#Get the result of connection with test component and STB
aampLoadStatus = aampObj.getLoadModuleResult();
print("AAMP module loading status : %s" %aampLoadStatus) ;
if ("SUCCESS" in aampLoadStatus.upper()):
    aampObj.setLoadModuleStatus("SUCCESS");

    streamType="hlsstream"
    #pattern to be searched for event validation
    pattern="AAMP_EVENT_TUNED"
    #fetch Aamp stream from config file
    tuneURL=aampUtilitylib.getAampTuneURL(streamType);
    #Primitive test case which associated to this Script
    tdkTestObj = aampObj.createTestStep('Aamp_AampTune');
    tdkTestObj.addParameter("URL",tuneURL);
    expectedResult = "SUCCESS";
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    result = tdkTestObj.getResult();
    if result and aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern) == "SUCCESS":
        print("AAMP Tune call is success")
        result,details,tdkTestObj = executeTest(aampObj, 'Aamp_AampGetVideoBitrates', "no parameters", True)
        if result:
            bitrates = details.split(':')[-1].strip(' ').split(' ');
            print(bitrates);
            #result,details = executeTest(aampObj, 'Aamp_AampStop');
            if len(bitrates) <2:
                tdkTestObj.setResultStatus("FAILURE");
                print("Please use a stream which support multiple bitrates")
                result,details = executeTest(aampObj, 'Aamp_AampStop');
            else:
                #Get the current bitrate
                result,details = executeTest(aampObj, 'Aamp_AampGetVideoBitrate');
                rate  = int(details.split(':')[-1]);
                print("Get the current video bitrate ", rate);

                #Set the other bitrate which is avail in the stream other than the above default one.
                set_bitrate = 2800000;
                result,details = executeTest(aampObj, 'Aamp_AampSetVideoBitrate', {"bitRate":int(set_bitrate)});
                print("Set the bitrate ", set_bitrate);
                print(details);

                #Enable PersistBitRateOverSeek functionality
                tdkTestObj = aampObj.createTestStep('Aamp_AampPersistBitRateOverSeek');
                tdkTestObj.addParameter("enable", "true");
                expectedResult = "SUCCESS";
                #Execute the test case in STB
                tdkTestObj.executeTestCase(expectedResult);
                #Get the result of execution
                actualResult = tdkTestObj.getResult();
                print(actualResult);
                details = tdkTestObj.getResultDetails();
                print("Result :", details);
                if expectedResult in actualResult:
                    print("PersistBitRateOverSeek functionality check config value updated successfully.");
                    tdkTestObj.setResultStatus("SUCCESS");

                    #Get the available audio tracks from the current playing HLS stream
                    tdkTestObj = aampObj.createTestStep('Aamp_AampGetAvailableAudioTracks');
                    expectedResult = "SUCCESS";
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedResult);
                    #Get the result of execution
                    actualResult = tdkTestObj.getResult();
                    print(actualResult);
                    details = tdkTestObj.getResultDetails();
                    if expectedResult in actualResult:
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("Result :", details)
                        tracks = details.replace('Avaliable Audio tracks: ','').split(',')
                        numberOfTracks = len(list(set(tracks)))

                        tdkTestObj = aampObj.createTestStep('Aamp_AampGetAudioTrack');
                        expectedResult = "SUCCESS";
                        #Execute the test case in STB
                        tdkTestObj.executeTestCase(expectedResult);
                        #Get the result of execution
                        actualResult = tdkTestObj.getResult();
                        print(actualResult);
                        details = tdkTestObj.getResultDetails();
                        if expectedResult in actualResult:
                            #Set the result status of execution
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("Result :", details)
                            track_index_get = details.replace('TrackIndex:', '').replace('\\n','')
                        else:
                            #Set the result status of execution
                            tdkTestObj.setResultStatus("FAILURE");
                            print(details);

                        TrackRange = list(range(0, numberOfTracks, 1));
                        if numberOfTracks < 2:
                            print("Please use a stream which is having more than one audio tracks");
                            result,details = executeTest(aampObj, 'Aamp_AampStop');
                            tdkTestObj.setResultStatus("FAILURE");
                        else:
                            mutliaudio_stream = True;
                            print("Playing stream is having more than one audio track.")
                            tdkTestObj.setResultStatus("SUCCESS");

                        trackList = list(TrackRange)
                        if mutliaudio_stream:
                            second_track = trackList[1];
                        #Remove Current Audio
                        #trackList.remove(int(track_index_get))

                        #switch to the 2nd audio track & verify whether bitrate value got persisted
                        tdkTestObj = aampObj.createTestStep('Aamp_AampSetAudioTrack');
                        expectedResult = "SUCCESS";
                        #track_index_set = _track
                        tdkTestObj.addParameter("track_index",int(second_track));
                        #Execute the test case in STB
                        tdkTestObj.executeTestCase(expectedResult);
                        #Get the result of execution
                        actualResult = tdkTestObj.getResult();
                        print(actualResult);
                        details = tdkTestObj.getResultDetails();
                        if expectedResult in actualResult:
                            #Set the result status of execution
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("Result :", details)
                            tdkTestObj = aampObj.createTestStep('Aamp_AampGetAudioTrack');
                            expectedResult = "SUCCESS";
                            #Execute the test case in STB
                            tdkTestObj.executeTestCase(expectedResult);
                            #Get the result of execution
                            actualResult = tdkTestObj.getResult();
                            print(actualResult);
                            details = tdkTestObj.getResultDetails();
                            if expectedResult in actualResult:
                                #Set the result status of execution
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("Result :", details)
                                track_index_get = details.replace('TrackIndex:', '').replace('\\n','')
                                if str(second_track) == str(track_index_get):
                                    print("SUCCESS: Audio Track was set successfully")
                                    tdkTestObj.setResultStatus("SUCCESS");
                                else:
                                    print("FAILURE: Audio Track was not successfully set")
                                    tdkTestObj.setResultStatus("FAILURE");
                            else:
                                #Set the result status of execution
                                tdkTestObj.setResultStatus("FAILURE");
                                print(details);
                        else:
                            #Set the result status of execution
                            print("FAILURE: Set Audio Track got failed");
                            tdkTestObj.setResultStatus("FAILURE");
                            print(details);


                        #Get the video Bitrate and check whether it is persisted
                        result,details = executeTest(aampObj, 'Aamp_AampGetVideoBitrate');
                        rate  = int(details.split(':')[-1]);
                        if rate == 0:
                            print("Video bitrate not set to zero ", rate);
                            print("[TEST EXECUTION RESULT] : FAILURE");
                            tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("GetVideo bitrate value from AAMP", rate);
                            if rate == 2800000:
                                print("Video Bitrate value persisted successfully.");
                                print("[TEST EXECUTION RESULT] : SUCCESS");
                                tdkTestObj.setResultStatus("SUCCESS");
                            else:
                                print("Video Bitrate value not persisted.");
                                print("[TEST EXECUTION RESULT] : FAILURE");
                                tdkTestObj.setResultStatus("FAILURE");
                        result,details = executeTest(aampObj, 'Aamp_AampStop');
                else:
                    print("PersistBitRateOverSeek functionality check config value not updated properly");
                    print("[TEST EXECUTION RESULT] : FAILURE");
                    tdkTestObj.setResultStatus("FAILURE");
        else:
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");
            print("Aamp_AampGetVideoBitrates call failed");
        result,details = executeTest(aampObj, 'Aamp_AampStop');
    else:
        print("AAMP Tune call Failed");
        tdkTestObj.setResultStatus("FAILURE");
    #Unload Module
    aampObj.unloadModule("aamp");
else:
    print("Failed to load aamp module");
    aampObj.setLoadModuleStatus("FAILURE");
