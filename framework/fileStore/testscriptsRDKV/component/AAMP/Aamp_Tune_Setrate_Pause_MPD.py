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
  <name>Aamp_Tune_Setrate_Pause_MPD</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Aamp_AampTune</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check pause for mpd stream</synopsis>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Aamp_28</test_case_id>
    <test_objective>Check pause for mpd stream</test_objective>
    <test_type>Positive</test_type>
    <test_setup>XG1v3</test_setup>
    <pre_requisite>configure Aamp_Tune_Config.ini with proper tuning URLs
Initialize devicesetting manager</pre_requisite>
    <api_or_interface_used>AampTune
AampSetrate</api_or_interface_used>
    <input_parameters>Valid URL from Aamp_Tune_Config.ini</input_parameters>
    <automation_approch>1. TM loads the Aamp_Agent and systemutil_Agent via the test agent.
2.Parse the stream from Aamp_Tune_Config.ini
3.Call AampTune
4.Sleep for sometime
5.Call AampSetrate
6.Call the ExecuteCmd with desired pattern for Log comparison
7.Set the script status as per the Log comparison</automation_approch>
    <except_output>Speed should be changed</except_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub.so.0.0.0
libsystemutilstub.so.0.0.0</test_stub_interface>
    <test_script>Aamp_Tune_Setrate_Pause_MPD</test_script>
    <skipped>No</skipped>
    <release_version>M66</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import aampUtilitylib;
from time import sleep;

streamType="mpdstream"
expectedResult="SUCCESS"
#pattern to be searched for event validation
pattern="AAMP_EVENT_TUNED"

#Test component to be tested
aampObj = tdklib.TDKScriptingLibrary("aamp","2.0");
sysObj = tdklib.TDKScriptingLibrary("systemutil","2.0");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

aampObj.configureTestCase(ip,port,'Aamp_Tune_Setrate_Pause_MPD');
sysObj.configureTestCase(ip,port,'Aamp_Tune_Setrate_Pause_MPD');

#Get the result of connection with test component and STB
aampLoadStatus = aampObj.getLoadModuleResult();
print("AAMP module loading status : %s" %aampLoadStatus);
sysLoadStatus = sysObj.getLoadModuleResult();
print("SystemUtil module loading status : %s" %sysLoadStatus);

aampObj.setLoadModuleStatus(aampLoadStatus);
sysObj.setLoadModuleStatus(sysLoadStatus);

if ("SUCCESS" in aampLoadStatus.upper()) and ("SUCCESS" in sysLoadStatus.upper()):

    #fetch Aamp stream from config file
    tuneURL=aampUtilitylib.getAampTuneURL(streamType);
    #Prmitive test case which associated to this Script
    tdkTestObj = aampObj.createTestStep('Aamp_AampTune');
    tdkTestObj.addParameter("URL",tuneURL);

    #Execute the test case in STB
    tdkTestObj.executeTestCase(expectedResult);
    #Get the result of execution
    result = tdkTestObj.getResult();
    if expectedResult in result:
        print("AAMP Tune is success")
        #Search events in Log
        result=aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern);
        if expectedResult in result:
            print("AAMP Tune events are verified")
            print("[TEST EXECUTION RESULT] : %s" %result);
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS");

            #AampSetRate call
            tdkTestObj = aampObj.createTestStep('Aamp_AampSetRate');
            tdkTestObj.addParameter("rate",0.0);
            #Execute the test case in STB
            tdkTestObj.executeTestCase(expectedResult);
            #Get the result of execution
            result = tdkTestObj.getResult();
            sleep(10);
            if expectedResult in result:
                pattern="AAMP_EVENT_SPEED_CHANGED"
                #Search events in Log
                result=aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern);
                if expectedResult in result:
                    print("Pause success")
                    print("[TEST EXECUTION RESULT] : SUCCESS");
                    #Set the result status of execution
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print("Pause failed")
                    print("[TEST EXECUTION RESULT] : FAILURE")
                    #Set the result status of execution
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("SetRate call failed")
                #Set the result status of execution
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("No AAMP events are received")
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");

        expectedResult = "SUCCESS";
        #AampTuneStop call
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
        print("AAMP Tune is Failure")
        print("[TEST EXECUTION RESULT] : %s" %result);
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");

    #Unload Module
    aampObj.unloadModule("aamp");
    sysObj.unloadModule("systemutil");
else:
    print("Failed to load aamp/systemutil module");
