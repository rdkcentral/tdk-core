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
  <name>FOG_MPD_Check_Pause_Play</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Fog_Do_Nothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check if play after pause resumes from same point</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>20</execution_time>
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
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_FOG_38</test_case_id>
    <test_objective>Check if play after pause resumes from same point</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Xg1v3,Video Accelerator, RPI</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper tuning URLs
Initialize devicesetting manager</pre_requisite>
    <api_or_interface_used>Aamp APIs</api_or_interface_used>
    <input_parameters>Fog URL</input_parameters>
    <automation_approch>1. TM loads the Aamp Agent and systemutil Agent.
2. Aamp Agent invokes Tune API with Fog URL
3. TM checks if the corresponding event is received.
4. TM gets the tsb location from fog.log.
5. TM checks if a folder is created in the tsb location and the folder name is same as the recording id
6. Aamp Agent invokes setRate API to pause and TM verifies if pipeline in paused using Aamp Get Playback Position.
7. Aamp Agent invokes setRate API to play and TM verfies if pipeline plays from the paused point using Aamp Get Playback Position.
8. TM checks invokes Aamp_Stop and returns SUCCESS/FAILURE
9. TM unloads the Aamp Agent and systemutil Agent.</automation_approch>
    <expected_output>Checkpoint 1. Event is received for Fog URL tune
Checkpoint 2. TSB folder name is same as recording id
Checkpoint 3. Pipeline is paused&amp;lt;
Checkpoint 4. Pipeline is playing from pause point</expected_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0
libsystemutilstub.so.0.0.0</test_stub_interface>
    <test_script>FOG_MPD_Check_Pause_Play</test_script>
    <skipped>No</skipped>
    <release_version>M112</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import aampUtilitylib;
from time import sleep;

def FindTSBLocation(obj, fileName, pattern):
        value = "";
        tdkTestObj = obj.createTestStep('ExecuteCommand');
        expectedResult="SUCCESS";
        cmd = "grep " + pattern + " " + fileName + " | cut -d \" \" -f 6 | sed -e 's/\"//g; s/,//g; s/\\r//g' ";
        #cmd = "grep " + pattern + " " + fileName + " | cut -d \":\" -f6";
        print cmd;

        #configre the command
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase(expectedResult);

        actualResult = tdkTestObj.getResult();
        print "Exceution result: ", actualResult;

        if expectedResult in actualResult:
                details = tdkTestObj.getResultDetails();
                value = details.strip("\\n");
                if value != "":
                        print "TSB Location: ", value;
                        tdkTestObj.setResultStatus("SUCCESS");
                else:
                        print "TSB Location not found";
                        tdkTestObj.setResultStatus("FAILURE");
        else:
                tdkTestObj.setResultStatus("FAILURE");
                print "Command execution failed";
        return value;


streamType = "fogmpdstream";
#fetch Aamp stream from config file
tuneURL=aampUtilitylib.getAampTuneURL(streamType);
#pattern to be searched for event validation
pattern = "AAMP_EVENT_TUNED";
expectedResult = "SUCCESS";
fogLog = "/opt/logs/fog.log";
fogConfig = "/etc/fogPrefs.json";
locationPattern = "tsbLocation";

#Test component to be tested
sysObj = tdklib.TDKScriptingLibrary("systemutil","2.0");
aampObj = tdklib.TDKScriptingLibrary("aamp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
sysObj.configureTestCase(ip,port,'FOG_Check_Pause_play');
aampObj.configureTestCase(ip,port,'FOG_Check_Pause_play');

#Get the result of connection with test component and STB
aampLoadStatus = aampObj.getLoadModuleResult();
print "AAMP module loading status : %s" %aampLoadStatus;
sysLoadStatus = sysObj.getLoadModuleResult();
print "SystemUtil module loading status : %s" %sysLoadStatus;

aampObj.setLoadModuleStatus(aampLoadStatus);
sysObj.setLoadModuleStatus(sysLoadStatus);

def exitFromScript():
    aampObj.unloadModule("aamp");
    sysObj.unloadModule("systemutil");
    exit()

if ("SUCCESS" in aampLoadStatus.upper()) and ("SUCCESS" in sysLoadStatus.upper()):

    #Prmitive test case which associated to this Script
    print "\nTEST STEP 1: Check if tune is successfull"
    tdkTestObj = aampObj.createTestStep('Aamp_AampTune');
    tdkTestObj.addParameter("URL",tuneURL);
    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    #Get the result of execution
    actualResult = tdkTestObj.getResult();

    if expectedResult in actualResult:
        print "AAMP Tune call is success"
        #Search events in Log
        test_step=2
        actualResult=aampUtilitylib.searchAampEvents(sysObj, pattern,test_step);
        if expectedResult in actualResult:
            print "AAMP Tune event recieved"
            print "[TEST EXECUTION RESULT] : %s" %actualResult;
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS");

            print "\nTEST STEP 3: Obtain recordingID from fog curl command"
            tsbLocation = FindTSBLocation(sysObj, fogConfig, locationPattern);
            if tsbLocation != "":
                tdkTestObj = sysObj.createTestStep('ExecuteCommand');
                cmd = "curl -L \"http://127.0.0.1:9080/recordings\" | grep recordingId" ;
                print cmd;
                tdkTestObj.addParameter("command", cmd);
                tdkTestObj.executeTestCase("SUCCESS");
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                recId = details.split(":")[1].split("\"")[1].strip("\\");
                print "Recording ID: ",recId;

                print "\nTEST STEP 4: Check if TSB folder is present"
                tdkTestObj = sysObj.createTestStep('ExecuteCommand');
                cmd = "ls " + tsbLocation.rstrip() + "| grep " + recId;
                print cmd;
                tdkTestObj.addParameter("command", cmd);
                tdkTestObj.executeTestCase("SUCCESS");
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                folderName = details.strip("\\n");
                if recId == folderName:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Recording Id and folder name are equal";

                    print "\nTEST STEP 5: Check if TSB data is being loaded"
                    tdkTestObj = sysObj.createTestStep('ExecuteCommand');
                    cmd = "du -sh " + tsbLocation.rstrip() + "//" + folderName;
                    print cmd;
                    tdkTestObj.addParameter("command", cmd);
                    tdkTestObj.executeTestCase("SUCCESS");
                    actualresult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    size = details.split("\\t")[0][:-1];
                    size = float(size.upper().rstrip("\\NMKB"));
                    print "TSB data size:",size;

                    #AampSetRate call
                    print "\nTEST STEP 6 :PAUSE the Pipeline"
                    tdkTestObj = aampObj.createTestStep('Aamp_AampSetRate');
                    tdkTestObj.addParameter("rate",0.0);
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedResult);
                    #Get the result of execution
                    result = tdkTestObj.getResult();
                    sleep(20);
                    if expectedResult in result:
                        pattern="AAMP_EVENT_SPEED_CHANGED"
                        test_step=7
                        #Search events in Log
                        result=aampUtilitylib.searchAampEvents(sysObj, pattern,test_step);
                        if expectedResult in result:
                            print "Verified SetRate for pause"
                            #Set the result status of execution
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print "SetRate for pause failed for FOG Url"
                            print "[TEST EXECUTION RESULT] : FAILURE"
                            #Set the result status of execution
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "SetRate call for PAUSE failed"
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("FAILURE")
                        exitFromScript()

                    print "\nTEST STEP 8:Acquire Position after pause"
                    tdkTestObj = aampObj.createTestStep('Aamp_AampGetPlaybackPosition');
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedResult);
                    #Get the result of execution
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    print "Result :", details;
                    if expectedResult not in actualResult:
                        print "GetPlaybackPosition failed"
                        tdkTestObj.setResultStatus("FAILURE")
                        exitFromScript()
                    previous_position = (float)(details.split(":")[1])
                    print "Position after pause call :",previous_position

                    print "\nWait for sometime to check if pipeline is paused"
                    sleep(10)
                    print "\nTEST STEP 8:Check if pipeline paused "
                    tdkTestObj = aampObj.createTestStep('Aamp_AampGetPlaybackPosition');
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedResult);
                    #Get the result of execution
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    print "Result :", details;
                    if expectedResult not in actualResult:
                        print "GetPlaybackPosition failed"
                        tdkTestObj.setResultStatus("FAILURE")
                        exitFromScript()
                    new_position = (float)(details.split(":")[1])
                    print "Position after waiting after seek :",new_position

                    if (new_position == previous_position):
                        print "SUCCESS : Pipeline is in paused state";
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print "FAILURE : Pipeline is not in paused state";
                        tdkTestObj.setResultStatus("FAILURE")
                        print "[TEST EXECUTION RESULT] : FAILURE";
                        exitFromScript()

                    #AampSetRate call
                    print "\nTEST STEP 9 : Set Pipeline to playing state"
                    tdkTestObj = aampObj.createTestStep('Aamp_AampSetRate');
                    tdkTestObj.addParameter("rate",1.0);
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedResult);
                    #Get the result of execution
                    result = tdkTestObj.getResult();
                    if expectedResult in result:
                        print "SetRate call for PLAY is successfull"
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print "SetRate call for PLAY failed"
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("FAILURE")
                        exitFromScript()

                    print "\nWait for sometime to check if pipeline is in playing state"
                    sleep(10)
                    print "\nTEST STEP 10:Check if pipeline is playing"
                    tdkTestObj = aampObj.createTestStep('Aamp_AampGetPlaybackPosition');
                    #Execute the test case in STB
                    tdkTestObj.executeTestCase(expectedResult);
                    #Get the result of execution
                    actualResult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    print "Result :", details;
                    if expectedResult not in actualResult:
                        print "GetPlaybackPosition failed"
                        tdkTestObj.setResultStatus("FAILURE")
                        exitFromScript()
                    position = (float)(details.split(":")[1])
                    print "Position after waiting after seek :",position

                    if (position - new_position) > 10:
                        print "SUCCESS : Pipeline is in playing";
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print "FAILURE : Pipeline is not playing";
                        tdkTestObj.setResultStatus("FAILURE")
                        print "[TEST EXECUTION RESULT] : FAILURE";
                        exitFromScript()

                    print "\nTEST STEP 11: Invoke Aamp Stop to stop tuning"
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
                    tdkTestObj.setResultStatus("FAILURE");
                    print "Recording Id and folder name are not equal";

            else:
                print "TSB data is not loaded"
                #Set the result status of execution
                tdkTestObj.setResultStatus("FAILURE");

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