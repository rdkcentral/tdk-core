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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>FOG_StopFogCli_Check_TSBSize_Increasing</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Fog_Do_Nothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check if data size is growing inside tsb location after stopping fogcli</synopsis>
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
    <box_type>RDKTV</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_FOG_12</test_case_id>
    <test_objective>Check if data size is growing inside tsb location after stopping fogcli</test_objective>
    <test_type>Negative</test_type>
    <test_setup>Xg1v3,Video Accelerator, RPI</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper tuning URLs
Initialize devicesetting manager</pre_requisite>
    <api_or_interface_used>Tune</api_or_interface_used>
    <input_parameters>Fog URL</input_parameters>
    <automation_approch>1. TM loads the Aamp Agent and systemutil Agent.
2. Aamp Agent invokes Tune API with Fog URL
3. TM checks if the corresponding event is received.
4. TM gets the tsb location from fog.log.
5. Aamp Agent stops fogcli
6. TM checks if the data size is increasing inside tsb location and returns FAILURE/SUCCESS
7. TM unloads the Aamp Agent and systemutil Agent.</automation_approch>
    <except_output>Checkpoint 1. Event is received for Fog URL tune
Checkpoint 2. TSB folder name is same as recording id
Checkpoint 3.  Data size is increasing inside tsb location</except_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0
libsystemutilstub.so.0.0.0</test_stub_interface>
    <test_script>FOG_StopFogCli_Check_TSBSize_Increasing</test_script>
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

def FindTSBLocation(obj, fileName, pattern):
    value = "";
    tdkTestObj = obj.createTestStep('ExecuteCommand');
    expectedResult="SUCCESS";
    cmd = "grep " + pattern + " " + fileName + " | cut -d \":\" -f6";
    print(cmd);

    #configre the command
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase(expectedResult);

    actualResult = tdkTestObj.getResult();
    print("Exceution result: ", actualResult);

    if expectedResult in actualResult:
        details = tdkTestObj.getResultDetails();
        value = details.strip("\\n");
        if value != "":
            print("TSB Location: ", value);
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            print("TSB Location not found");
            tdkTestObj.setResultStatus("FAILURE");
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print("Command execution failed");
    return value;


streamType = "fogstream";
#fetch Aamp stream from config file
tuneURL=aampUtilitylib.getAampTuneURL(streamType);
#pattern to be searched for event validation
pattern = "AAMP_EVENT_TUNED";
expectedResult = "SUCCESS";
fogLog = "/opt/logs/fog.log";
locationPattern = "\"TSB storage-path\"";

#Test component to be tested
sysObj = tdklib.TDKScriptingLibrary("systemutil","2.0");
aampObj = tdklib.TDKScriptingLibrary("aamp","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
sysObj.configureTestCase(ip,port,'FOG_StopFogCli_Check_TSBSize_Increasing');
aampObj.configureTestCase(ip,port,'FOG_StopFogCli_Check_TSBSize_Increasing');

#Get the result of connection with test component and STB
aampLoadStatus = aampObj.getLoadModuleResult();
print("AAMP module loading status : %s" %aampLoadStatus);
sysLoadStatus = sysObj.getLoadModuleResult();
print("SystemUtil module loading status : %s" %sysLoadStatus);


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
        print("AAMP Tune call is success")
        #Search events in Log
        actualResult=aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern);
        if expectedResult in actualResult:
            print("AAMP Tune event recieved")
            print("[TEST EXECUTION RESULT] : %s" %actualResult);
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS");

            tsbLocation = FindTSBLocation(sysObj, fogLog, locationPattern);
            if tsbLocation != "":
                tdkTestObj = sysObj.createTestStep('ExecuteCommand');
                cmd = "curl -L \"http://127.0.0.1:9080/recordings\" | grep recordingId" ;
                print(cmd);
                tdkTestObj.addParameter("command", cmd);
                tdkTestObj.executeTestCase("SUCCESS");
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                recId = details.split(":")[1].split("\"")[1].strip("\\");

                print(recId);

                tdkTestObj = sysObj.createTestStep('ExecuteCommand');
                cmd = "ls " + tsbLocation.rstrip() + "| grep " + recId;
                print(cmd);
                tdkTestObj.addParameter("command", cmd);
                tdkTestObj.executeTestCase("SUCCESS");
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();
                folderName = details.strip("\\n");
                if recId == folderName:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("Recording Id and folder name are equal");

                    tdkTestObj = sysObj.createTestStep('ExecuteCommand');
                    cmd = "systemctl stop fog";
                    print(cmd);
                    tdkTestObj.addParameter("command", cmd);
                    tdkTestObj.executeTestCase("SUCCESS");
                    actualresult = tdkTestObj.getResult();

                    tdkTestObj = sysObj.createTestStep('ExecuteCommand');
                    cmd = "du -sh " + tsbLocation.rstrip() + "//" + folderName;
                    print(cmd);
                    tdkTestObj.addParameter("command", cmd);
                    tdkTestObj.executeTestCase("SUCCESS");
                    actualresult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    size1 = details.split("\\t")[0][:-1];
                    size1 = float(size1.upper().rstrip("\\NMKB"));
                    print(size1);

                    sleep(50);
                    tdkTestObj = sysObj.createTestStep('ExecuteCommand');
                    cmd = "du -sh " + tsbLocation.rstrip() + "//" + folderName;
                    print(cmd);
                    tdkTestObj.addParameter("command", cmd);
                    tdkTestObj.executeTestCase("SUCCESS");
                    actualresult = tdkTestObj.getResult();
                    details = tdkTestObj.getResultDetails();
                    size2 = details.split("\\t")[0][:-1];
                    size2 = float(size2.upper().rstrip("\\NMKB"));
                    print(size2);

                    if size1 == size2:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TSB size is not increasing");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TSB size is increasing");

                    tdkTestObj = sysObj.createTestStep('ExecuteCommand');
                    cmd = "systemctl start fog";
                    print(cmd);
                    tdkTestObj.addParameter("command", cmd);
                    tdkTestObj.executeTestCase("SUCCESS");
                    actualresult = tdkTestObj.getResult();
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("Recording Id and folder name are not equal");

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
            print("No AAMP tune event received")
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print("AAMP Tune call Failed")
        print("[TEST EXECUTION RESULT] : %s" %actualResult);
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");

    #Unload Module
    aampObj.unloadModule("aamp");
    sysObj.unloadModule("systemutil");
else:
    print("Failed to load aamp/systemutil module");
