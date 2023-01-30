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
  <version>2</version>
  <name>Aamp_Tune_Setrate_Seek_16FW_22</name>
  <primitive_test_id/>
  <primitive_test_name>Aamp_AampSetRateAndSeek</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Set playback rate and seek</synopsis>
  <groups_id/>
  <execution_time>3</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>true</advanced_script>
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
    <test_case_id>CT_Aamp_22</test_case_id>
    <test_objective>Set playback rate and seek</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Xg1v3</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper tuning URLs</pre_requisite>
    <api_or_interface_used>AampTune
AampSetrateandSeek</api_or_interface_used>
    <input_parameters>Valid URL from Aamp_Tune_Config.ini</input_parameters>
    <automation_approch>1. TM loads the Aamp_Agent and systemutil_Agent via the test agent.
2.Parse the stream from Aamp_Tune_Config.ini
3.Call AampTune
4.Sleep for sometime
5.Call AampSetrateandSeek
6.Call the ExecuteCmd with desired pattern for Log comparison
7.Set the script status as per the Log comparison</automation_approch>
    <except_output>Speed and rate should be changed</except_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0
libsystemutilstub.so.0.0.0</test_stub_interface>
    <test_script>Aamp_Tune_Setrate_Seek_16FW_22</test_script>
    <skipped>No</skipped>
    <release_version>M63_02</release_version>
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
#pattern to be searched for event validation
pattern="AAMP_EVENT_TUNED"

#Test component to be tested
aampobj = tdklib.TDKScriptingLibrary("aamp","2.0");
sysobj = tdklib.TDKScriptingLibrary("systemutil","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

aampobj.configureTestCase(ip,port,'Aamp_Tune_Setrate_Seek_16FW_22');
sysobj.configureTestCase(ip,port,'Aamp_Tune_Setrate_Seek_16FW_22');

#Get the result of connection with test component and STB
aamp_status  =aampobj.getLoadModuleResult();
sysutil_status = sysobj.getLoadModuleResult();
print "[LIB LOAD STATUS]:aamp is %s and systemutil is %s" %(aamp_status,sysutil_status);
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
		print "AAMP Tune is success"
		#Search events in Log	
		result=aampUtilitylib.searchAampEvents(sysobj, pattern);
		if Expected_Result in result:
			print "AAMP Tune events are verified"
			print "[TEST EXECUTION RESULT] : %s" %result;
			#Set the result status of execution
			tdkTestObj.setResultStatus("SUCCESS");
			
			#AampSetRate call
			tdkTestObj = aampobj.createTestStep('Aamp_AampSetRateAndSeek');
			tdkTestObj.addParameter("rate",16.0);
			tdkTestObj.addParameter("seconds",10.0);
		        #Execute the test case in STB
		        tdkTestObj.executeTestCase(Expected_Result);
		        #Get the result of execution
		        result = tdkTestObj.getResult();
	        	if Expected_Result in result:
				pattern="AAMP_EVENT_BITRATE_CHANGED"
		                #Search events in Log
		                result=aampUtilitylib.searchAampEvents(sysobj, pattern);
				if Expected_Result in result:
		                        print "Verified AampSetRate"
		                        print "[TEST EXECUTION RESULT] : %s" %result;
        		                #Set the result status of execution
                		        tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                        print "AampSetRate failed to speed change"
                                        print "[TEST EXECUTION RESULT] : FAILURE"
                                        #Set the result status of execution
                                        tdkTestObj.setResultStatus("FAILURE")

		else:
			print "No AAMP events are received"
                	#Set the result status of execution
	                tdkTestObj.setResultStatus("FAILURE");

                #AampTuneStop call
                tdkTestObj = aampobj.createTestStep('Aamp_AampStop');
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
	aampobj.unloadModule("aamp");
	sysobj.unloadModule("systemutil");
else:
    print "Failed to load aamp/systemutil module";
    aampobj.setLoadModuleStatus("FAILURE");
    sysobj.setLoadModuleStatus("FAILURE");
