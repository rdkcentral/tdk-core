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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Aamp_Disable_4K_Playback</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Aamp_AampSetDisable4K</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to disable 4K video playback</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>4</execution_time>
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
    <box_type>RDKTV</box_type>
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
    <test_case_id>CT_Aamp_83</test_case_id>
    <test_objective>Test script to disable 4K video playback</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper 4K tuning URL</pre_requisite>
    <api_or_interface_used>AampTune
AampSetDisable4K
AampStop</api_or_interface_used>
    <input_parameters>4K URL</input_parameters>
    <automation_approch>1. TM loads the Aamp Agent.
2. Aamp Agent invokes SetDisable4K to make AAMP not switch to 2160p.
3. Aamp Agent invokes Tune API with MPD URL
4. Aamp Agent retrieves the bitrate  details from the player.
5. Aamp Agent checks if video is playing at expected resolution.
7. TM unloads the Aamp Agent.</automation_approch>
    <expected_output>Should play with resolution below 4K</expected_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0</test_stub_interface>
    <test_script>Aamp_Disable_4K_Playback</test_script>
    <skipped>No</skipped>
    <release_version>M120</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import aampUtilitylib;
from time import *
import re

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
#Test component to be tested
aampObj = tdklib.TDKScriptingLibrary("aamp","2.0");
aampObj.configureTestCase(ip,port,'Aamp_Disable_4K_Playback');
#Get the result of connection with test component and STB
aampLoadStatus = aampObj.getLoadModuleResult();
print("AAMP module loading status : %s" %aampLoadStatus) ;
if ("SUCCESS" in aampLoadStatus.upper()):
    aampObj.setLoadModuleStatus("SUCCESS");

    streamType="uhdstream"
    #pattern to be searched for event validation
    pattern="AAMP_EVENT_TUNED"
    #fetch Aamp stream from config file
    tuneURL=aampUtilitylib.getAampTuneURL(streamType);

    tdkTestObj = aampObj.createTestStep('Aamp_AampSetDisable4K');
    expectedResult = "SUCCESS";
    tdkTestObj.addParameter("disable4K","true");
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    print(details)

    #Prmitive test case which associated to this Script
    tdkTestObj = aampObj.createTestStep('Aamp_AampTune');
    tdkTestObj.addParameter("URL",tuneURL);
    expectedResult = "SUCCESS";
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    #Get the result of execution
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        print("AAMP Tune call is success")
        #Search events in Log
        actualResult=aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern);
        if expectedResult in actualResult:
            print("AAMP Tune event recieved")
            print("[TEST EXECUTION RESULT] : %s" %actualResult);
            tdkTestObj.setResultStatus("SUCCESS");

            sleep(20);
            tdkTestObj = aampObj.createTestStep('Aamp_AampGetBitrateDetails');
            tdkTestObj.executeTestCase(expectedResult);
            details = tdkTestObj.getResultDetails();
            pattern = r"Width: (\d+), Height: (\d+)"
            match = re.search(pattern, details)
            if match:
                width = int(match.group(1))
                height = int(match.group(2))
                print("Width:", width)
                print("Height:", height)
                if height != 2160:
                    print("SUCCESS : Playback is not happening at 4K as expected");
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print("FAILURE : Playback is happening at 4K which is not expected");
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("FAILURE : Unable to obtain bitrate details");
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("No AAMP tune event received")
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
        print("Error description : ",details)
        print("[TEST EXECUTION RESULT] : %s" %actualResult);
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
    #Unload Module
    aampObj.unloadModule("aamp");
else:
    print("Failed to load aamp module");
    aampObj.setLoadModuleStatus("FAILURE");
