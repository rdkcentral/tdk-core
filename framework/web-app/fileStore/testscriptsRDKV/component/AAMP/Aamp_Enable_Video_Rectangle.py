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
  <name>Aamp_Enable_Video_Rectangle</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Aamp_AampGetVideoRectangle</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to get and set video display rectangle co-ordinates while EnableVideoRectangle is enabled</synopsis>
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
    <test_case_id>CT_Aamp_73</test_case_id>
    <test_objective>Test script to get and set video display rectangle co-ordinates while EnableVideoRectangle is enabled</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper Live tuning URL</pre_requisite>
    <api_or_interface_used>AampTune
AampSetWesterosConfig
AampStop
AampGetVideoRectangle
AampEnableVideoRectangle
AampSetVideoRectangle</api_or_interface_used>
    <input_parameters>Live URL</input_parameters>
    <automation_approch>1. TM loads the Aamp Agent and systemutil Agent.
2. Aamp Agent invokes SetWesterosConfig to make AAMP use westerossink as video-sink.
3. Aamp Agent invokes Tune API with MPD URL
4. Aamp Agent invokes EnableVideoRectangle API
5. Aamp Agent invokes SetVideoRectangle API with valid co-ordinates
6. Checks if GetVideoRectangle API  returns the co-ordinates set and set SUCCESS/FAILURE
7. TM unloads the Aamp Agent and systemutil Agent.</automation_approch>
    <expected_output>Should set the new video rectangle co-ordinates</expected_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0
libsystemutilstub.so.0.0.0</test_stub_interface>
    <test_script>Aamp_Enable_Video_Rectangle</test_script>
    <skipped>No</skipped>
    <release_version>M113</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import aampUtilitylib;
#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
#Test component to be tested
aampObj = tdklib.TDKScriptingLibrary("aamp","2.0");
sysObj = tdklib.TDKScriptingLibrary("systemutil","2.0");
aampObj.configureTestCase(ip,port,'Aamp_Enable_Video_Rectangle');
sysObj.configureTestCase(ip,port,'Aamp_Enable_Video_Rectangle');
#Get the result of connection with test component and STB
aampLoadStatus = aampObj.getLoadModuleResult();
print "AAMP module loading status : %s" %aampLoadStatus ;
sysLoadStatus = sysObj.getLoadModuleResult();
print "SystemUtil module loading status : %s" %sysLoadStatus ;
if ("SUCCESS" in aampLoadStatus.upper()) and ("SUCCESS" in sysLoadStatus.upper()):
        aampObj.setLoadModuleStatus("SUCCESS");
        sysObj.setLoadModuleStatus("SUCCESS");

        streamType="mpdstream"
        #pattern to be searched for event validation
        pattern="AAMP_EVENT_TUNED"
        #fetch Aamp stream from config file
        tuneURL=aampUtilitylib.getAampTuneURL(streamType);

        tdkTestObj = aampObj.createTestStep('Aamp_AampSetWesterosSinkConfig');
        expectedResult = "SUCCESS";
        tdkTestObj.addParameter("enable","true");
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print details

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
                print "AAMP Tune call is success"
                #Search events in Log
                actualResult=aampUtilitylib.searchAampEvents(sysObj, pattern);
                if expectedResult in actualResult:
                        print "AAMP Tune event recieved"
                        print "[TEST EXECUTION RESULT] : %s" %actualResult;
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("SUCCESS");

                        #GetVideoRectangle must return empty co-ordinates before setting videoRectangle DELIA-45366
                        tdkTestObj = aampObj.createTestStep('Aamp_AampGetVideoRectangle');
                        expectedResult = "FAILURE";
                        #Execute the test case in STB
                        tdkTestObj.executeTestCase(expectedResult);
                        #Get the result of execution
                        actualResult = tdkTestObj.getResult();
                        print actualResult;
                        details = tdkTestObj.getResultDetails();
                        if expectedResult in actualResult:
                            #Set the result status of execution
                            tdkTestObj.setResultStatus("SUCCESS");
                            print "SUCCESS : Empty co-ordinates is returned as expected before setting videoRectangle\n"

                            tdkTestObj = aampObj.createTestStep('Aamp_AampEnableVideoRectangle');
                            expectedResult = "SUCCESS";
                            tdkTestObj.addParameter("enable","true");
                            tdkTestObj.executeTestCase(expectedResult);
                            actualResult = tdkTestObj.getResult();
                            details = tdkTestObj.getResultDetails();
                            print details
                            tdkTestObj = aampObj.createTestStep('Aamp_AampSetVideoRectangle');
                            x=0
                            y=0
                            w=1920
                            h=1080
                            expectedResult = "SUCCESS";
                            tdkTestObj.addParameter("x", x);
                            tdkTestObj.addParameter("y", y);
                            tdkTestObj.addParameter("w", w);
                            tdkTestObj.addParameter("h", h);
                            print "Setting video rectangle co-ordinates in x,y,w,h format : ",x,y,w,h
                            tdkTestObj.executeTestCase(expectedResult);
                            actualResult = tdkTestObj.getResult();
                            print actualResult;
                            details = tdkTestObj.getResultDetails();
                            if expectedResult in actualResult :
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "Result :", details;
                                print "[TEST EXECUTION RESULT] : SUCCESS\n"

                                tdkTestObj = aampObj.createTestStep('Aamp_AampGetVideoRectangle');
                                expectedResult = "SUCCESS";
                                tdkTestObj.executeTestCase(expectedResult);
                                actualResult = tdkTestObj.getResult();
                                print actualResult;
                                details = tdkTestObj.getResultDetails();
                                if details:
                                    x1 = int(str(details).split(":")[1].split(",")[0].strip())
                                    y1 = int(str(details).split(":")[1].split(",")[1].strip())
                                    w1 = int(str(details).split(":")[1].split(",")[2].strip())
                                    h1 = int(str(details).split(":")[1].split(",")[3].strip())
                                if expectedResult in actualResult and (x1 == x and y1 == y and w1 == w and h1 == h):
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print "Result :", details;
                                    print "[TEST EXECUTION RESULT] : SUCCESS\n"

                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print details;
                                    print "[TEST EXECUTION RESULT] : FAILURE\n"
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print details;
                                print "[TEST EXECUTION RESULT] : FAILURE\n"
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print details;
                            print "[TEST EXECUTION RESULT] : FAILURE\n"
                else:
                        print "No AAMP tune event received"
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("FAILURE");
                #AampTuneStop call
                tdkTestObj = aampObj.createTestStep('Aamp_AampStop');
                #Execute the test case in STB
                tdkTestObj.executeTestCase(expectedResult);
                #Get the result of execution
                result = tdkTestObj.getResult();
                if expectedResult in result:
                    print "AAMP Stop Success"
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "AAMP Stop Failure"
                    tdkTestObj.setResultStatus("FAILURE")
        else:
                print "AAMP Tune call Failed"
                print "Error description : ",details
                print "[TEST EXECUTION RESULT] : %s" %actualResult;
                #Set the result status of execution
                tdkTestObj.setResultStatus("FAILURE");
        #Unload Module
        aampObj.unloadModule("aamp");
        sysObj.unloadModule("systemutil");
else:
    print "Failed to load aamp/systemutil module";
    aampObj.setLoadModuleStatus("FAILURE");
    sysObj.setLoadModuleStatus("FAILURE");
