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
  <name>Aamp_SetSlowMotionRate_HLS</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>Aamp_AampSetRate</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>SetSlowMotion Playback Rate on HLS stream and verify the same</synopsis>
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
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <box_type>Hybrid-1</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_Aamp_79</test_case_id>
    <test_objective>SetSlowMotion Playback Rate on HLS stream and verify the same</test_objective>
    <test_type>Positive</test_type>
    <test_setup>X1, Video Accelerator, RPI</test_setup>
    <pre_requisite>HLS stream must be populated in Aamp_Tune_config.ini</pre_requisite>
    <api_or_interface_used>SetRate</api_or_interface_used>
    <input_parameters>HLS stream</input_parameters>
    <automation_approch>1.Tune AAMP with HLS url.
2. Verify TUNED event is captured.
3. Invoke SetRate API with rate set as 0.5.
4. Verify SPEED_CHANGED event is captured.
5. Verify if playback rate is set as expected by periodically querying playback position.
6. Invoke AAMP steop to gracefully exit from the player.</automation_approch>
    <expected_output>Playback must be happening at 0.5x speed</expected_output>
    <priority>High</priority>
    <test_stub_interface>libaampstub</test_stub_interface>
    <test_script>Aamp_SetSlowMotionRate_HLS</test_script>
    <skipped></skipped>
    <release_version>M114</release_version>
    <remarks></remarks>
  </test_cases>
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

aampobj.configureTestCase(ip,port,'Aamp_SetSlowMotionRate_HLS');
sysobj.configureTestCase(ip,port,'Aamp_SetSlowMotionRate_HLS');

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
        print "AAMP Tune call is success"
        #Search events in Log
        result=aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern);
        if Expected_Result in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print "AAMP Tune events are verified"

            rate = 0.5
            tdkTestObj = aampobj.createTestStep('Aamp_AampSetRate');
            tdkTestObj.addParameter("rate",rate);
            #Execute the test case in STB
            tdkTestObj.executeTestCase(Expected_Result);
            #Get the result of execution
            result = tdkTestObj.getResult();
            if Expected_Result in result:
                pattern="AAMP_EVENT_SPEED_CHANGED"
                #Search events in Log
                result=aampUtilitylib.SearchAampPlayerEvents(tdkTestObj,pattern);
                if Expected_Result in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print "Verified AampSetRate happened with rate: %s"%rate;

                    #Check if playback rate is set as expected
                    aampUtilitylib.CheckPlayBackRate(aampobj,rate) 

                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print "AampSetRate Events not verified with rate :%s"%rate;
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "No AAMP events are received"

        #AampTuneStop call
        tdkTestObj = aampobj.createTestStep('Aamp_AampStop');
        #Execute the test case in STB
        tdkTestObj.executeTestCase(Expected_Result);
        #Get the result of execution
        result = tdkTestObj.getResult();
        if Expected_Result in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print "AAMP Stop Success"
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print "AAMP Stop Failure"
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print "AAMP Tune is Failure"

    #Unload Module
    aampobj.unloadModule("aamp");
    sysobj.unloadModule("systemutil");

