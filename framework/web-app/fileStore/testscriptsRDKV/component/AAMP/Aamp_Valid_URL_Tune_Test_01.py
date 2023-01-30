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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>3</version>
  <name>Aamp_Valid_URL_Tune_Test_01</name>
  <primitive_test_id/>
  <primitive_test_name>Aamp_AampTune</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>test Aamp tune with Valid URL</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_AAMP_01</test_case_id>
    <test_objective>test aamp tune api with valid url</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Xg1v3</test_setup>
    <pre_requisite>Valid URL should be updated in the Aamp_Tune_Config.ini.</pre_requisite>
    <api_or_interface_used>gst_init(NULL,NULL)
Tune(Tune_URL.c_str())</api_or_interface_used>
    <input_parameters>Valid URL</input_parameters>
    <automation_approch>1. TM loads the aamp agent via the test agent.
2. Aamp agent will invoke the gst_init for the gst plugins initialization
3. Aamp agent will invoke the Tune api with valid URL from Aamp_Tune_Config.ini</automation_approch>
    <except_output>Tune happened suucssefully</except_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so</test_stub_interface>
    <test_script>Aamp_Valid_URL_Tune_Test_01</test_script>
    <skipped>No</skipped>
    <release_version>M57</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import aampUtilitylib;
stream_Type="hlsstream"
Expected_Result="SUCCESS"

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("aamp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Aamp_Valid_URL_Tune_Test_01');

#Get the result of connection with test component and STB
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

#fetch Aamp stream from config file
tune_URL=aampUtilitylib.getAampTuneURL(stream_Type);
#Prmitive test case which associated to this Script
tdkTestObj = obj.createTestStep('Aamp_AampTune');
tdkTestObj.addParameter("URL",tune_URL);

#Execute the test case in STB
tdkTestObj.executeTestCase(Expected_Result);

#Get the result of execution
result = tdkTestObj.getResult();

if Expected_Result in result:
	print "AAMP Tune is success"
	print "[TEST EXECUTION RESULT] : %s" %result;
	#Set the result status of execution
	tdkTestObj.setResultStatus("SUCCESS");
   
        #AampTuneStop call
        tdkTestObj = obj.createTestStep('Aamp_AampStop');
        #Execute the test case in STB
        tdkTestObj.executeTestCase(Expected_Result);
        #Get the result of execution
        result = tdkTestObj.getResult();
        if Expected_Result in result:
            print "AAMP Stop Success"
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "AAMP Stop Failure"
            tdkTestObj.setResultStatus("FAILURE")
else:
	print "AAMP Tune is Failure"
	print "[TEST EXECUTION RESULT] : %s" %result;
	#Set the result status of execution
	tdkTestObj.setResultStatus("FAILURE");

#Unload Module
obj.unloadModule("aamp");
