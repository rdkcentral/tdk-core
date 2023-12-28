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
  <name>FOG_MPD_Check_Seek_to_Beginning</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Fog_Do_Nothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Play fog asset and seek to beginning, pipeline must play from beginning</synopsis>
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
    <box_type>Hybrid-1</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
    <box_type>RDKTV</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_FOG_31</test_case_id>
    <test_objective>Play fog asset and seek to beginning , pipeline must play from beginning</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Xg1v4,Video Accelerator, RPI</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper tuning URLs</pre_requisite>
    <api_or_interface_used>Tune</api_or_interface_used>
    <input_parameters>Fog URL</input_parameters>
    <automation_approch>1.TM loads the Aamp Agent and systemutil Agent.
2. Aamp Agent invokes Tune API with Fog URL
3. TM checks if the corresponding tune event is received.
4. Call AampSetrateandSeek with seek as set to beginning point
5. Call AampGetPlaybackPosition and verify if seek is successfull
6. Wait for sometime and call AampGetPlaybackPosition, verify pipeline is in playing state.
7. TM unloads the Aamp Agent and systemutil Agent</automation_approch>
    <expected_output>Checkpoint 1 : Tune event is received
Checkpoint 2.  Seek is successfull</expected_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0
libsystemutilstub.so.0.0.0</test_stub_interface>
    <test_script>FOG_MPD_Check_Seek_to_Beginning</test_script>
    <skipped>No</skipped>
    <release_version>M111</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import aampUtilitylib;
from time import *

streamType = "fogmpdstream";
#fetch Aamp stream from config file
tuneURL=aampUtilitylib.getAampTuneURL(streamType);
#pattern to be searched for event validation
pattern = "AAMP_EVENT_TUNED";
expectedResult = "SUCCESS";

#Test component to be tested
sysObj = tdklib.TDKScriptingLibrary("systemutil","2.0");
aampObj = tdklib.TDKScriptingLibrary("aamp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
sysObj.configureTestCase(ip,port,'FOG_MPD_Check_Seek_to_Beginning');
aampObj.configureTestCase(ip,port,'FOG_MPD_Check_Seek_to_Beginning');

#Get the result of connection with test component and STB
aampLoadStatus = aampObj.getLoadModuleResult();
print("AAMP module loading status : %s" %aampLoadStatus);
sysLoadStatus = sysObj.getLoadModuleResult();
print("SystemUtil module loading status : %s" %sysLoadStatus);

aampObj.setLoadModuleStatus(aampLoadStatus);
sysObj.setLoadModuleStatus(sysLoadStatus);


def exitFromScript():
    aampObj.unloadModule("aamp");
    sysObj.unloadModule("systemutil");
    exit()


if ("SUCCESS" in aampLoadStatus.upper()) and ("SUCCESS" in sysLoadStatus.upper()):

    #Prmitive test case which associated to this Script
    print("\nTEST STEP 1: Check if tune is successfull")
    tdkTestObj = aampObj.createTestStep('Aamp_AampTune');
    tdkTestObj.addParameter("URL",tuneURL);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    #Get the result of execution
    actualResult = tdkTestObj.getResult();

    if expectedResult in actualResult:
        print("AAMP Tune call is success")
        #Search events in Log
        test_step=2
        actualResult=aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern);
        if expectedResult in actualResult:
            print("AAMP Tune event recieved")
            print("[TEST EXECUTION RESULT] : %s" %actualResult);
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS");

            sleep(10)
            print("\nTEST STEP 3:Acquire position before seek")
            tdkTestObj = aampObj.createTestStep('Aamp_AampGetPlaybackPosition');
            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedResult);
            #Get the result of execution
            actualResult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            print("Result :", details);
            if expectedResult not in actualResult:
                print("GetPlaybackPosition failed")
                tdkTestObj.setResultStatus("FAILURE")
                exitFromScript()
            previous_position = (float)(details.split(":")[1])
            print("Initial Position :",previous_position)

            #AampSetRate call
            print("\nTEST STEP 4:Seeking to Beginning")
            tdkTestObj = aampObj.createTestStep('Aamp_AampSetRateAndSeek');
            tdkTestObj.addParameter("rate",1.0);
            tdkTestObj.addParameter("seconds",0.0);
            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedResult);
            #Get the result of execution
            result = tdkTestObj.getResult();
            if expectedResult in result:
                pattern="AAMP_EVENT_BITRATE_CHANGED"
                test_step=5
                #Search events in Log
                result=aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern);
                if expectedResult in result:
                    print("Verified AampSetRate")
                    #Set the result status of execution
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print("AampSetRate failed to speed change")
                    #Set the result status of execution
                    tdkTestObj.setResultStatus("FAILURE")
                    exitFromScript()
            else:
                print("SetRateAndSeek failed")
                tdkTestObj.setResultStatus("FAILURE")
                exitFromScript()

            print("\nTEST STEP 6:Acquire Position after seek")
            tdkTestObj = aampObj.createTestStep('Aamp_AampGetPlaybackPosition');
            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedResult);
            #Get the result of execution
            actualResult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            print("Result :", details);
            if expectedResult not in actualResult:
                print("GetPlaybackPosition failed")
                tdkTestObj.setResultStatus("FAILURE")
                exitFromScript()
            position = (float)(details.split(":")[1])
            print("Position after seek to beg :",position)

            print("Check Position of pipeline after seek is valid or not")
            if (previous_position > position):
                print("SUCCESS : FOG Seek to beginning was successfull");
                tdkTestObj.setResultStatus("SUCCESS")
                print("[TEST EXECUTION RESULT] : %s" %result);
            else:
                print("FAILURE : FOG Seek to beginning was not successfull");
                tdkTestObj.setResultStatus("FAILURE")
                print("[TEST EXECUTION RESULT] : FAILURE");
                exitFromScript()

            sleep(10)
            print("\nTEST STEP 7:Check if playback is fine after seeking")
            tdkTestObj = aampObj.createTestStep('Aamp_AampGetPlaybackPosition');
            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedResult);
            #Get the result of execution
            actualResult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            print("Result :", details);
            if expectedResult not in actualResult:
                print("GetPlaybackPosition failed")
                tdkTestObj.setResultStatus("FAILURE")
                exitFromScript()
            new_position = (float)(details.split(":")[1])
            print("Position after waiting after seek :",new_position)

            if (new_position > position):
                print("SUCCESS : Pipeline is in playing state after seeking");
                tdkTestObj.setResultStatus("SUCCESS")
                print("[TEST EXECUTION RESULT] : %s\n" %result);
            else:
                print("FAILURE : Pipeline is not in playing state after seeking");
                tdkTestObj.setResultStatus("FAILURE")
                print("[TEST EXECUTION RESULT] : FAILURE\n");
                exitFromScript()

        else:
            print("No AAMP tune event received\n")
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");
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
