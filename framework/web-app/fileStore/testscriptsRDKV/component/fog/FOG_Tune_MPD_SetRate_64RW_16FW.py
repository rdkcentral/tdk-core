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
  <name>FOG_Tune_MPD_SetRate_64RW_16FW</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Fog_Do_Nothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check if "AAMP_EVENT_SPEED_CHANGED" event is received while invoking setrate with value 16.0 for fog mpd stream</synopsis>
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
    <box_type>IPClient-3</box_type>
    <!--  -->
    <box_type>Hybrid-1</box_type>
    <box_type>Video_Accelerator</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_FOG_17</test_case_id>
    <test_objective>Check if "AAMP_EVENT_SPEED_CHANGED" event is received while invoking setrate with value 16.0 for fog mpd stream</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Xg1v3,Video Accelerator, RPI</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper tuning URLs
Initialize devicesetting manager</pre_requisite>
    <api_or_interface_used>Tune, SetRate</api_or_interface_used>
    <input_parameters>Fog URL</input_parameters>
    <automation_approch>1. TM loads the Aamp Agent and systemutil Agent.
2. Aamp Agent invokes Tune API with Fog mpd URL
3. TM checks if the corresponding event is received.
4. Aamp Agent invokes SetRate API with value -64.0
5. Aamp Agent invokes SetRate API with value 16.0
6. TM checks if event AAMP_EVENT_SPEED_CHANGED is received and returns SUCCESS/FAILURE 
7. TM unloads the Aamp Agent and systemutil Agent.</automation_approch>
    <except_output>Checkpoint 1. Event is received for Fog URL tune
Checkpoint 2. AAMP_EVENT_SPEED_CHANGED event is received</except_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0
libsystemutilstub.so.0.0.0</test_stub_interface>
    <test_script>FOG_Tune_MPD_SetRate_64RW_16FW</test_script>
    <skipped>No</skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
import aampUtilitylib;
from time import sleep;

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
sysObj.configureTestCase(ip,port,'FOG_Tune_MPD_SetRate_64RW_16FW');
aampObj.configureTestCase(ip,port,'FOG_Tune_MPD_SetRate_64RW_16FW');

#Get the result of connection with test component and STB
aampLoadStatus = aampObj.getLoadModuleResult();
print "AAMP module loading status : %s" %aampLoadStatus;
sysLoadStatus = sysObj.getLoadModuleResult();
print "SystemUtil module loading status : %s" %sysLoadStatus;

aampObj.setLoadModuleStatus(aampLoadStatus);
sysObj.setLoadModuleStatus(sysLoadStatus);

if ("SUCCESS" in aampLoadStatus.upper()) and ("SUCCESS" in sysLoadStatus.upper()):
 

	#Prmitive test case which associated to this Script
	tdkTestObj = aampObj.createTestStep('Aamp_AampTune');
	tdkTestObj.addParameter("URL",tuneURL);
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

                        #AampSetRate call
                        tdkTestObj = aampObj.createTestStep('Aamp_AampSetRate');
                        tdkTestObj.addParameter("rate",-64.0);
                        #Execute the test case in STB
                        tdkTestObj.executeTestCase(expectedResult);
                        #Get the result of execution
                        result = tdkTestObj.getResult();
			sleep(120);
                        #AampSetRate call
                        tdkTestObj = aampObj.createTestStep('Aamp_AampSetRate');
                        tdkTestObj.addParameter("rate",16.0);
                        #Execute the test case in STB
                        tdkTestObj.executeTestCase(expectedResult);
                        #Get the result of execution
                        result = tdkTestObj.getResult();
			sleep(20);
                        if expectedResult in result:
                                pattern="AAMP_EVENT_SPEED_CHANGED";
				logName = "/opt/TDK/logs/AgentConsole.log";
				tdkTestObj = sysObj.createTestStep('ExecuteCommand');
                                cmd = "tail -n +`grep -n -m 1 \"AampSetRate Speed is: 16.0\" " + logName + " | cut -f1 -d:` " + logName + " | grep " + pattern + " | grep -v grep" ;
                                print cmd;
                                tdkTestObj.addParameter("command", cmd);
                                tdkTestObj.executeTestCase("SUCCESS");
                                actualresult = tdkTestObj.getResult();
                                details = tdkTestObj.getResultDetails();
				print "OUTPUT:", details;				

                                if pattern in details:
                                        print "SetRate success for FOG Url"
                                        print "[TEST EXECUTION RESULT] : %s" %result;
                                        #Set the result status of execution
                                        tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                        print "SetRate failed for FOG Url"
                                        print "[TEST EXECUTION RESULT] : FAILURE"
                                        #Set the result status of execution
                                        tdkTestObj.setResultStatus("FAILURE")
			else:
				 print "SetRate call failed"
                                 #Set the result status of execution
                                 tdkTestObj.setResultStatus("FAILURE")

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
            		print "No AAMP tune event received"
            		#Set the result status of execution
            		tdkTestObj.setResultStatus("FAILURE");
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

