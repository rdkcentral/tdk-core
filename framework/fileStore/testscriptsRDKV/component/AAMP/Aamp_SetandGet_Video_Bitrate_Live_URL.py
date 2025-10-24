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
  <version>7</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Aamp_SetandGet_Video_Bitrate_Live_URL</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Aamp_AampGetVideoBitrate</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to set and get the video bitrate with supported values</synopsis>
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
    <test_case_id>CT_Aamp_60</test_case_id>
    <test_objective>Test Script to set and get the video bitrate with supported values</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper tuning URLs</pre_requisite>
    <api_or_interface_used>AampTune
AampStop
AampSetVideoBitrate
AampGetVideoBitrate</api_or_interface_used>
    <input_parameters>Live URL</input_parameters>
    <automation_approch>1. TM loads the Aamp Agent and systemutil Agent.
2. Aamp Agent invokes Tune API with Live URL
3. Aamp Agent invokes GetVideoBitrates API
4. Aamp Agent invokes Aamp Stop API
5. Aamp Agent invokes SetVideoBitrates API with a supported bitrate
6. Aamp Agent invokes Tune API with Live URL
7. Aamp Agent invokes GetVideoBitrates API to get the current bitrate
8. TM checks if the value is set and returns SUCCESS/FAILURE
9. Aamp Agent invokes Aamp Stop API
10. The steps 5,6,7,8,9 is done in a loop for all the supported bitrates
11. TM unloads the Aamp Agent and systemutil Agent.</automation_approch>
    <expected_output>Should set the video bitrate value</expected_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0
libsystemutilstub.so.0.0.0</test_stub_interface>
    <test_script>Aamp_SetandGet_Video_Bitrate_Live_URL</test_script>
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
from tdkvutility import *

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
#Test component to be tested
aampObj = tdklib.TDKScriptingLibrary("aamp","2.0");
sysObj = tdklib.TDKScriptingLibrary("systemutil","2.0");
aampObj.configureTestCase(ip,port,'Aamp_SetandGet_Video_Bitrate_Live_URL');
sysObj.configureTestCase(ip,port,'Aamp_SetandGet_Video_Bitrate_Live_URL');
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
    result = tdkTestObj.getResult();
    if result and aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern) == "SUCCESS":
        print("AAMP Tune call is success")
        result,details,tdkTestObj = executeTest(aampObj, 'Aamp_AampGetVideoBitrates', "no parameters", True)
        if result:
            bitrates = details.split(':')[-1].strip(' ').split(' ');
            print(bitrates);
            result,details = executeTest(aampObj, 'Aamp_AampStop');
            if len(bitrates) <2:
                tdkTestObj.setResultStatus("FAILURE");
                print("Please use a stream which support multiple bitrates")

            else:
                for rate in bitrates:
                    print("Setting Video Bitrate to :",rate);
                    result,details = executeTest(aampObj, 'Aamp_AampSetVideoBitrate', {"bitRate":int(rate)});
                    sleep(5);
                    if result:
                        result,details = executeTest(aampObj, 'Aamp_AampTune', {"URL":tuneURL});
                        if result:
                            result,details = executeTest(aampObj, 'Aamp_AampGetVideoBitrate');
                            if result:
                                print("Video bitrate set to ", rate);
                            else:
                                print("Video bitrate not set to ", rate);
                            result,details = executeTest(aampObj, 'Aamp_AampStop');
                        else:
                            print("AAMP Tune call Failed")
                    else:
                        print("Aamp_AampSetVideoBitrate call failed");
        else:
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");
            print("Aamp_AampGetVideoBitrates call failed");
        result,details = executeTest(aampObj, 'Aamp_AampStop');
    else:
        print("AAMP Tune call Failed")
    #Unload Module
    aampObj.unloadModule("aamp");
    sysObj.unloadModule("systemutil");
else:
    print("Failed to load aamp/systemutil module");
    aampObj.setLoadModuleStatus("FAILURE");
    sysObj.setLoadModuleStatus("FAILURE");
