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
  <name>Aamp_GetPlaybackPosition_Live_URL</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Aamp_AampGetPlaybackPosition</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to get the current playback position for Live stream</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <box_type>Hybrid-1</box_type>
    <box_type>Video_Accelerator</box_type>
    <!--  -->
    <box_type>IPClient-3</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Aamp_57</test_case_id>
    <test_objective>To get the current playback position</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper tuning URLs</pre_requisite>
    <api_or_interface_used>AampTune
AampStop
AampGetPlaybackPosition</api_or_interface_used>
    <input_parameters>Live URL</input_parameters>
    <automation_approch>1. TM loads the Aamp Agent and systemutil Agent.
2. Aamp Agent invokes Tune API with Live URL
3. Aamp Agent invokes GetPlaybackPosition API
4. TM checks if API returns a non empty value and returns SUCCESS/FAILURE
5. TM unloads the Aamp Agent and systemutil Agent.</automation_approch>
    <expected_output>Should get the valid value</expected_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0
libsystemutilstub.so.0.0.0</test_stub_interface>
    <test_script>Aamp_GetPlaybackPosition_Live_URL</test_script>
    <skipped>No</skipped>
    <release_version>M78</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import aampUtilitylib;
from time import sleep;
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
#Test component to be tested
aampObj = tdklib.TDKScriptingLibrary("aamp","2.0");
sysObj = tdklib.TDKScriptingLibrary("systemutil","2.0");
aampObj.configureTestCase(ip,port,'Aamp_GetPlaybackPosition_Live_URL');
sysObj.configureTestCase(ip,port,'Aamp_GetPlaybackPosition_Live_URL');
#Get the result of connection with test component and STB
aampLoadStatus = aampObj.getLoadModuleResult();
print("AAMP module loading status : %s" %aampLoadStatus) ;
sysLoadStatus = sysObj.getLoadModuleResult();
print("SystemUtil module loading status : %s" %sysLoadStatus) ;

if ("SUCCESS" in aampLoadStatus.upper()) and ("SUCCESS" in sysLoadStatus.upper()):
    aampObj.setLoadModuleStatus("SUCCESS");
    sysObj.setLoadModuleStatus("SUCCESS");

    streamType="livestream"
    #pattern to be searched for event validation
    pattern="AAMP_EVENT_TUNED"
    #fetch Aamp stream from config file
    tuneURL=aampUtilitylib.getAampTuneURL(streamType);

    #Prmitive test case which associated to this Script
    tdkTestObj = aampObj.createTestStep('Aamp_AampTune');
    tdkTestObj.addParameter("URL",tuneURL);
    expectedResult = "SUCCESS";
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    #Get the result of execution
    actualResult = tdkTestObj.getResult();
    if expectedResult in actualResult:
        print("AAMP Tune call is success")
        #Search events in Log
        actualResult=aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern);
        if expectedResult in actualResult:
            print("AAMP Tune event recieved")
            print("[TEST EXECUTION RESULT] : %s" %actualResult);
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS");

            sleep(10);
            tdkTestObj = aampObj.createTestStep('Aamp_AampGetPlaybackPosition');
            expectedResult = "SUCCESS";
            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedResult);
            #Get the result of execution
            actualResult = tdkTestObj.getResult();
            print(actualResult);
            details = tdkTestObj.getResultDetails();
            print("Result :", details);
            if expectedResult in actualResult:
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS");
                position1  = float(details.rstrip(" ").split(':')[-1]);
                print("First value: ", position1);
                sleep(5);
                tdkTestObj = aampObj.createTestStep('Aamp_AampGetPlaybackPosition');
                expectedResult = "SUCCESS";
                #Execute the test case in STB
                tdkTestObj.executeTestCase(expectedResult);
                #Get the result of execution
                actualResult = tdkTestObj.getResult();
                print(actualResult);
                details = tdkTestObj.getResultDetails();
                print("Result :", details);

                if expectedResult in actualResult:
                    position2  = float(details.rstrip(" ").split(':')[-1]);
                    print("Second value: ", position2);
                    diff = position2 - position1;
                    print("Difference in position: ", diff);
                    if diff >= 5.0:
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("Playback position retrieved is valid for Live stream");
                    else:
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("FAILURE");
                        print("Playback position retrieved is not valid for Live stream");
                else:
                    #Set the result status of execution
                    tdkTestObj.setResultStatus("FAILURE");
                    print("Playback position not retrieved");
            else:
                #Set the result status of execution
                tdkTestObj.setResultStatus("FAILURE");
                print("Playback position not retrieved for Live stream");

        else:
            print("No AAMP tune event received");
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");
        #AampTuneStop call
        tdkTestObj = aampObj.createTestStep('Aamp_AampStop');
        #Execute the test case in STB
        tdkTestObj.executeTestCase(expectedResult);
        #Get the result of execution
        result = tdkTestObj.getResult();
        if expectedResult in result:
            print("AAMP Stop Success")
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print("AAMP Stop Failure")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("AAMP Tune call Failed")
        print("[TEST EXECUTION RESULT] : %s" %actualResult);
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
    #Unload Module
    aampObj.unloadModule("aamp");
    sysObj.unloadModule("systemutil");
else:
    print("Failed to load aamp/systemutil module");
    aampObj.setLoadModuleStatus("FAILURE");
    sysObj.setLoadModuleStatus("FAILURE");
