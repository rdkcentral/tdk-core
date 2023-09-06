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
  <name>FOG_MPD_Resolution_1080p</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Fog_Do_Nothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Validate resolution in FOG with respect to set resolution to 1080p</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <box_type>Video_Accelerator</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
    <!--  -->
    <!--  -->
    <!--  -->
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_FOG_28</test_case_id>
    <test_objective>Validate resolution in FOG with respect to set resolution to 1080p</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Xg1v3,Video Accelerator, RPI</test_setup>
    <pre_requisite>1.configure Aamp_Tune_Config.ini with proper tuning URLs
2.Initialize devicesetting manager
3.display device should be connected</pre_requisite>
    <api_or_interface_used>Tune</api_or_interface_used>
    <input_parameters>Fog URL</input_parameters>
    <automation_approch>1. TM loads the Device_Settings_Agent via the test agent.
2.Device_Settings_Agent will get the list resolution supported by a given port.
3.Device_Settings_Agent will get the default resolution supported by a given port.
4.Device_Settings_Agent will get the status of display connection.
5.Device_Settings_Agent will get the display resolution.
6. Device_Settings_Agent will set the new display resolution.
7. Device_Settings_Agent will check for the new display resolution and will return SUCCESS or FAILURE based on the result.
8 TM loads the Aamp Agent and systemutil Agent.
9. Aamp Agent invokes Tune API with Fog URL
10. TM checks if the corresponding event is received.
11. TM gets the OriginalUrl from the recording details using curl command
12. TM checks if OriginalUrl is same as that in the  tune url and returns SUCCESS/FAILURE 
13. TM unloads the Aamp Agent and systemutil Agent</automation_approch>
    <expected_output>Checkpoint 1 : Resolution is set as expected
Checkpoint 2.  Retrieved resolution is as expected</expected_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0
libsystemutilstub.so.0.0.0</test_stub_interface>
    <test_script>FOG_MPD_Resolution_1080p</test_script>
    <skipped>No</skipped>
    <release_version>M110</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import aampUtilitylib;

streamType = "fogmpdstream";
#fetch Aamp stream from config file
tuneURL=aampUtilitylib.getAampTuneURL(streamType);
#pattern to be searched for event validation
pattern = "AAMP_EVENT_TUNED";
expectedResult = "SUCCESS";

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("devicesettings","1.2");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'FOG_MPD_Resolution_1080p');

resolution_set = "False"

loadmodulestatus =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %loadmodulestatus ;
if "SUCCESS" in loadmodulestatus.upper():
        #Set the module loading status
        obj.setLoadModuleStatus("SUCCESS");

        #calling Device Settings - initialize API
        tdkTestObj = obj.createTestStep('DS_ManagerInitialize');
        expectedresult="SUCCESS"
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        #Check for SUCCESS/FAILURE return value of DS_ManagerInitialize
        if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print "SUCCESS :Application successfully initialized with Device Settings library";
                #calling DS_IsDisplayConnectedStatus function to check for display connection status
                tdkTestObj = obj.createTestStep('DS_IsDisplayConnectedStatus');
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                displaydetails = tdkTestObj.getResultDetails();
                #Check for SUCCESS/FAILURE return value of DS_IsDisplayConnectedStatus
                if (expectedresult in actualresult) and ("TRUE" in displaydetails):
                    tdkTestObj.setResultStatus("SUCCESS");
                    #calling DS_Resolution get list of supported resolutions and the default resolution
                    tdkTestObj = obj.createTestStep('DS_Resolution');
                    tdkTestObj.addParameter("port_name","HDMI0");
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    resolutiondetails = tdkTestObj.getResultDetails();
                    #Check for SUCCESS/FAILURE return value of DS_Resolution
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully gets the list of supported and default resolutions";
                        print "%s" %resolutiondetails;
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE :Failed to get the list of supported resolutions";
                    #calling DS_SetResolution to set and get the display resolution as 1080p60    
                    resolution="1080p60";
                    print "Resolution value set to:%s" %resolution;
                    if resolution in resolutiondetails:
                        tdkTestObj = obj.createTestStep('DS_SetResolution');
                        tdkTestObj.addParameter("resolution",resolution);
                        tdkTestObj.addParameter("port_name","HDMI0");
                        expectedresult="SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult);
                        actualresult = tdkTestObj.getResult();
                        resolutiondetails = tdkTestObj.getResultDetails();
                        #Check for SUCCESS/FAILURE return value of DS_SetResolution
                        if expectedresult in actualresult:
                                print "SUCCESS:set and get resolution Success";
                                print "getresolution %s" %resolutiondetails;
                                #comparing the resolution before and after setting
                                if resolution in resolutiondetails :
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print "SUCCESS: Both the resolutions are same";
                                        resolution_set = "True"
                                else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print "FAILURE: Both the resolutions are not same";
                        else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print "FAILURE:set and get resolution fails";
                    else:
                        print "FAILURE:Requested resolution are not supported by this device";
                        tdkTestObj.setResultStatus("FAILURE");
                    #calling DS_ManagerDeInitialize to DeInitialize API
                    tdkTestObj = obj.createTestStep('DS_ManagerDeInitialize');
                    expectedresult="SUCCESS"
                    tdkTestObj.executeTestCase(expectedresult);
                    actualresult = tdkTestObj.getResult();
                    #Check for SUCCESS/FAILURE return value of DS_ManagerDeInitialize
                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print "SUCCESS :Application successfully DeInitialized the DeviceSetting library";
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print "FAILURE: Deinitalize failed" ;
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "FAILURE:Connection Failed";  
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "FAILURE: Device Setting Initialize failed";
        print "[TEST EXECUTION RESULT] : %s" %actualresult;
        #Unload the deviceSettings module
        obj.unloadModule("devicesettings");
else:
        print"Load module failed";
        #Set the module loading status
        obj.setLoadModuleStatus("FAILURE"); 

if resolution_set == "True":
        #Test component to be tested
        sysObj = tdklib.TDKScriptingLibrary("systemutil","2.0");
        aampObj = tdklib.TDKScriptingLibrary("aamp","2.0");

        sysObj.configureTestCase(ip,port,'FOG_MPD_Resolution_1080p');
        aampObj.configureTestCase(ip,port,'FOG_MPD_Resolution_1080p');

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
			actualResult=aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern);
			if expectedResult in actualResult:
				print "AAMP Tune event recieved"
				print "[TEST EXECUTION RESULT] : %s" %actualResult;
				#Set the result status of execution
				tdkTestObj.setResultStatus("SUCCESS");
                           
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
			
                                aampObj.unloadModule("aamp");
				#Get the recorded url from curl command
				tdkTestObj = sysObj.createTestStep('ExecuteCommand');
                                cmd = "grep 'tvHeight\|tvWidth' /opt/TDK/logs/AgentConsole.log"
				print cmd;
				tdkTestObj.addParameter("command", cmd);
				tdkTestObj.executeTestCase("SUCCESS");
				actualresult = tdkTestObj.getResult();
				details = tdkTestObj.getResultDetails();
				print "Result ",details;
				if details != "":
					tdkTestObj.setResultStatus("SUCCESS");
					print "Details retrieved";
                                        tvHeight = (details.split('tvHeight:',2)[1].split(',',2)[0])
				        tvWidth = (details.split('tvWidth:',2)[1].split(' ',2)[0])
					if tvHeight == "1080":
						tdkTestObj.setResultStatus("SUCCESS");
						print "\nResolution obtained as expected tvHeight : %s tvWidth %s"%(tvHeight,tvWidth);
					else:
						tdkTestObj.setResultStatus("FAILURE");
						print "\nResolution is wrong , got resolution as  tvHeight : %s tvWidth %s"%(tvHeight,tvWidth);
				else:
					tdkTestObj.setResultStatus("FAILURE");
					print "Details not retrieved";

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
		sysObj.unloadModule("systemutil");
	else:
		print "Failed to load aamp/systemutil/devicesettings module";

