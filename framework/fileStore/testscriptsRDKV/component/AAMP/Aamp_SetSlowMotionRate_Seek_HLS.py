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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Aamp_SetSlowMotionRate_Seek_HLS</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Aamp_AampGetPlaybackPosition</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify media pipeline is seekable at slowMotion playback rate</synopsis>
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
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Aamp_80</test_case_id>
    <test_objective>Verify media pipeline is seekable at slowMotion playback rate</test_objective>
    <test_type>Positive</test_type>
    <test_setup>X1, Video Accelerator, RPI</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>SetRateAndSeek</api_or_interface_used>
    <input_parameters>HLS stream</input_parameters>
    <automation_approch>1.Invoke Tune API with HLS url.
2. Verify if TUNED event is captured.
3. GetPlayPosition of the pipeline and set the seekPosition value accordingly.
4. Invoke SetRateAndSeek with rate set as 0.5 and seekPosition calculated in the former step.
5. Verify if BITRATE_CHANGED event is captured.
6. Verify if pipeline is seeked properly.
7. Verify if playback rate is set properly.
8. Invoke Aamp Stop to exit gracefully from the player.</automation_approch>
    <expected_output>Pipeline must be seeked to expected point and playabck rate also must be set properly</expected_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub</test_stub_interface>
    <test_script>Aamp_SetSlowMotionRate_Seek_HLS</test_script>
    <skipped></skipped>
    <release_version>M114</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import aampUtilitylib;
from time import *

stream_Type="hlsstream"
Expected_Result="SUCCESS"

#pattern to be searched for event validation
pattern="AAMP_EVENT_TUNED"

#Test component to be tested
aampobj = tdklib.TDKScriptingLibrary("aamp","2.0");
sysobj = tdklib.TDKScriptingLibrary("systemutil","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

aampobj.configureTestCase(ip,port,'Aamp_SetSlowMotionRate_Seek_HLS.py');
sysobj.configureTestCase(ip,port,'\Aamp_SetSlowMotionRate_Seek_HLS');

#Get the result of connection with test component and STB
aamp_status  =aampobj.getLoadModuleResult();
sysutil_status = sysobj.getLoadModuleResult();
print("[LIB LOAD STATUS]:aamp is %s and systemutil is %s" %(aamp_status,sysutil_status));

if ("SUCCESS" in aamp_status.upper()) and ("SUCCESS" in sysutil_status.upper()):
    aampobj.setLoadModuleStatus("SUCCESS");
    sysobj.setLoadModuleStatus("SUCCESS");

    #fetch Aamp stream from config file
    tune_URL=aampUtilitylib.getAampTuneURL(stream_Type);
    #Prmitive test case which associated to this Script
    tdkTestObj = aampobj.createTestStep('Aamp_AampTune');
    tdkTestObj.addParameter("URL",tune_URL);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(Expected_Result);
    #Get the result of execution
    result = tdkTestObj.getResult();
    if Expected_Result in result:
        print("AAMP Tune call is success")
        #Search events in Log
        result=aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern);
        if Expected_Result in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print("AAMP Tune events are verified")

            tdkTestObj = aampobj.createTestStep('Aamp_AampGetPlaybackPosition');
            #Execute the test case in STB
            tdkTestObj.executeTestCase(Expected_Result);
            #Get the result of execution
            result = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            print("Result :", details);
            if Expected_Result in result:
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS");
                initial_position  = float(details.rstrip(" ").split(':')[-1]);
                print("Initial play position : ", initial_position);

                playbackspeed = 0.5
                if ( initial_position > 15 ):
                    seekposition = initial_position - 15
                else:
                    seekposition = 25
                #seekposition = initial_position + 30
                print("SeekPosition : ",seekposition)
                tdkTestObj = aampobj.createTestStep('Aamp_AampSetRateAndSeek');
                tdkTestObj.addParameter("rate",playbackspeed);
                tdkTestObj.addParameter("seconds",int(seekposition));
                #Execute the test case in STB
                tdkTestObj.executeTestCase(Expected_Result);
                #Get the result of execution
                result = tdkTestObj.getResult();
                if Expected_Result in result:
                    pattern="AAMP_EVENT_BITRATE_CHANGED"
                    #Search events in Log
                    result=aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern);
                    if Expected_Result in result:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print("Verified AampSetRate")

                        tdkTestObj = aampobj.createTestStep('Aamp_AampGetPlaybackPosition');
                        #Execute the test case in STB
                        tdkTestObj.executeTestCase(Expected_Result);
                        #Get the result of execution
                        result = tdkTestObj.getResult();
                        details = tdkTestObj.getResultDetails();
                        print("Result :", details);
                        if Expected_Result in result:
                            #Set the result status of execution
                            position_seeked  = float(details.rstrip(" ").split(':')[-1]);
                            print("After seeking playback position : ", position_seeked);
                            if position_seeked >= seekposition:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print("Seek position success")

                                #Check if playback rate is playing as expected
                                aampUtilitylib.CheckPlayBackRate(aampobj,playbackspeed);

                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print("Seek position failure")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("Playback position not retrieved");
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("AampSetRate failed to speed change")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("Playback position not retrieved");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("No AAMP events are received")

        #AampTuneStop call
        tdkTestObj = aampobj.createTestStep('Aamp_AampStop');
        #Execute the test case in STB
        tdkTestObj.executeTestCase(Expected_Result);
        #Get the result of execution
        result = tdkTestObj.getResult();
        if Expected_Result in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print("AAMP Stop Success")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("AAMP Stop Failure")
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print("AAMP Tune is Failure")

    #Unload Module
    aampobj.unloadModule("aamp");
    sysobj.unloadModule("systemutil");

else:
    print("Failed to load aamp/systemutil module");
    aampobj.setLoadModuleStatus("FAILURE");
    sysobj.setLoadModuleStatus("FAILURE");
