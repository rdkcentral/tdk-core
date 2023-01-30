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
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Aamp_Valid_Multi_Tune_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Aamp_AampTune</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Tune to multiple test URL one after another as given in the config file</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>30</execution_time>
  <!--  -->
  <long_duration>true</long_duration>
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
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Aamp_29</test_case_id>
    <test_objective>Tune to multiple test streams and check if tuning is happening properly</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1v3</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper tuning URLs</pre_requisite>
    <api_or_interface_used>AampTune</api_or_interface_used>
    <input_parameters>Valid URL from Aamp_Tune_Config.ini</input_parameters>
    <automation_approch>1. TM loads the Aamp_Agent via the test agent.
2.Parse the list of streams from Aamp_Tune_Config.ini
3.Call AampTune
4.Sleep for sometime
5.Set the script status as per the Log comparison
6. Repeat test step 2,3,4 and 5 for all the listed URLS in the config file 
</automation_approch>
    <expected_output>Aamp tune should be success</expected_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0</test_stub_interface>
    <test_script>Aamp_Valid_Multi_Tune_Test</test_script>
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
import time
Expected_Result="SUCCESS"

#Test component to be tested
aampobj = tdklib.TDKScriptingLibrary("aamp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip =<ipaddress>
port = <port>

aampobj.configureTestCase(ip,port,'Aamp_Valid_Multi_Tune_Test');

#Get the result of connection with test component and STB
aamp_status  =aampobj.getLoadModuleResult();
print "[LIB LOAD STATUS]:aamp is %s " %(aamp_status);
if ("SUCCESS" in aamp_status.upper()):

	aampobj.setLoadModuleStatus("SUCCESS");
    
	#fetch Aamp stream from config file
	URLCount=aampUtilitylib.getIPStreamsCounts();
	print "Total number of streams configured in Config file: %d" %URLCount
	if URLCount > 0 :
		for index in range(1, URLCount+1):
		  	tune_URL=aampUtilitylib.getURLFromMultiStreamIndex(index);
			
			print "----------------Execution START For index:%d --------------" %index
			print "URL retrived from config file: %s" %tune_URL
			if "Failure" not in tune_URL:
				#Prmitive test case which associated to this Script
				tdkTestObj = aampobj.createTestStep('Aamp_AampTune');
				tdkTestObj.addParameter("URL",tune_URL);
		
				#Execute the test case in STB
				tdkTestObj.executeTestCase(Expected_Result);
				#Get the result of execution
				result = tdkTestObj.getResult();
			        details= tdkTestObj.getResultDetails();
		        	print "Details: %s" %details;
				if Expected_Result in result:
					print "AAMP Tune is success"
		        	  	time.sleep(2);
					tdkTestObj.setResultStatus("SUCCESS");
					#AampTuneStop call
			                tdkTestObj = aampobj.createTestStep('Aamp_AampStop');
			                #Execute the test case in STB
			                tdkTestObj.executeTestCase(Expected_Result);
			                #Get the result of execution
			                result = tdkTestObj.getResult();
			                if Expected_Result in result:
						print "Verified AampStop"
						print "[TEST EXECUTION RESULT] : %s" %result;
						#Set the result status of execution
						tdkTestObj.setResultStatus("SUCCESS")
						print "----------------Execution END For index:%d --------------" %index
					else:
						print "AampStop Failed"
						print "[TEST EXECUTION RESULT] : %s" %result;
						#Set the result status of execution
						tdkTestObj.setResultStatus("FAILURE")
						print "----------------Execution END For index:%d --------------" %index
				else:
					print "AAMP Tune is Failure"
					print "[TEST EXECUTION RESULT] : %s" %result;
					#Set the result status of execution
					tdkTestObj.setResultStatus("FAILURE");
					print "----------------Execution END For index:%d -------------" %index
		  	else:
				print "URL is not Valid at given instance: %d" %index
				tdkTestObj.setResultStatus("FAILURE");
				print "----------------Execution END For index:%d --------------" %index
	else:
		print "Not even single URL confiured in config file"         
		tdkTestObj.setResultStatus("FAILURE");
	#Unload Module
	aampobj.unloadModule("aamp");
else:
    print "Failed to load aamp module";
    aampobj.setLoadModuleStatus("FAILURE");
