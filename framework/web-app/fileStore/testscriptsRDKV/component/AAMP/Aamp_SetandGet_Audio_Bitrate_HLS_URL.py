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
  <version>9</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Aamp_SetandGet_Audio_Bitrate_HLS_URL</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Aamp_AampGetAudioBitrate</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to set and get the audio bitrate with supported values</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>true</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks>Audio Bitrate information is available only for DASH stream , not for HLS Streams</remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>true</skip>
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
    <test_case_id>CT_Aamp_65</test_case_id>
    <test_objective>Test Script to set and get the audio bitrate with supported values</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1V3,XI3</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper tuning URLs</pre_requisite>
    <api_or_interface_used>AampTune
AampStop
AampSetAudioBitrate
AampGetAudioBitrate</api_or_interface_used>
    <input_parameters>HLS URL</input_parameters>
    <automation_approch>1. TM loads the Aamp Agent and systemutil Agent.
2. Aamp Agent invokes Tune API with HLS URL
3. Aamp Agent invokes GetAudioBitrates API
4. Aamp Agent invokes SetAudioBitrates API with all supported bitrates
5. Aamp Agent invokes GetAudioBitrates API to get the current bitrate
6. TM checks if the value is set and returns SUCCESS/FAILURE
7. TM unloads the Aamp Agent and systemutil Agent.</automation_approch>
    <expected_output>Should set the audio bitrate value</expected_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0
libsystemutilstub.so.0.0.0</test_stub_interface>
    <test_script>Aamp_SetandGet_Audio_Bitrate_HLS_URL</test_script>
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
aampObj.configureTestCase(ip,port,'Aamp_SetandGet_Audio_Bitrate_HLS_URL');
sysObj.configureTestCase(ip,port,'Aamp_SetandGet_Audio_Bitrate_HLS_URL');
#Get the result of connection with test component and STB
aampLoadStatus = aampObj.getLoadModuleResult();
print "AAMP module loading status : %s" %aampLoadStatus ;
sysLoadStatus = sysObj.getLoadModuleResult();
print "SystemUtil module loading status : %s" %sysLoadStatus ;
if ("SUCCESS" in aampLoadStatus.upper()) and ("SUCCESS" in sysLoadStatus.upper()):
	aampObj.setLoadModuleStatus("SUCCESS");
	sysObj.setLoadModuleStatus("SUCCESS");
    
	streamType="hlsstream"
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
		print "AAMP Tune call is success"
		#Search events in Log	
		actualResult=aampUtilitylib.searchAampEvents(sysObj, pattern);
		if expectedResult in actualResult:
			print "AAMP Tune event recieved"
			print "[TEST EXECUTION RESULT] : %s" %actualResult;
			#Set the result status of execution
			tdkTestObj.setResultStatus("SUCCESS");

                        tdkTestObj = aampObj.createTestStep('Aamp_AampGetAudioBitrates');
                        expectedResult = "SUCCESS";
                        #Execute the test case in STB
                        tdkTestObj.executeTestCase(expectedResult);
                        #Get the result of execution
                        actualResult = tdkTestObj.getResult();
                        print actualResult;
                        details = tdkTestObj.getResultDetails();
			print details;
                        if expectedResult in actualResult:
				bitrates = details.split(':')[-1].strip(' ').split(' ');
				print bitrates;
				for rate in bitrates:
		                        tdkTestObj = aampObj.createTestStep('Aamp_AampSetAudioBitrate');
					tdkTestObj.addParameter("bitRate", int(rate));
		                        expectedResult = "SUCCESS";
					print "Trying to set audio bitrate to ", rate;
                		        #Execute the test case in STB
		                        tdkTestObj.executeTestCase(expectedResult);
                		        #Get the result of execution
		 		        actualResult = tdkTestObj.getResult();
		                        print actualResult;
                		        details = tdkTestObj.getResultDetails();
					sleep(10);

		                        if expectedResult in actualResult:
                        			tdkTestObj = aampObj.createTestStep('Aamp_AampGetAudioBitrate');
			                        expectedResult = "SUCCESS";
                        			#Execute the test case in STB
			                        tdkTestObj.executeTestCase(expectedResult);
                        			#Get the result of execution
			                        actualResult = tdkTestObj.getResult();
                        			print actualResult;
			                        details = tdkTestObj.getResultDetails();
						print details;
						print rate;
						if expectedResult in actualResult and rate in details:
							#Set the result status of execution
			                                tdkTestObj.setResultStatus("SUCCESS");
                        			        print "Audio bitrate set to ", rate;
			                        else:
                        			        #Set the result status of execution
			                                tdkTestObj.setResultStatus("FAILURE");
                        			        print "Audio bitrate not set to ", rate;
					else:
						 #Set the result status of execution
                                                 tdkTestObj.setResultStatus("FAILURE");
                                                 print "Aamp_AampSetAudioBitrate call failed";
			else:
				 #Set the result status of execution
                                 tdkTestObj.setResultStatus("FAILURE");
                                 print "Aamp_AampGetAudioBitrates call failed";
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
