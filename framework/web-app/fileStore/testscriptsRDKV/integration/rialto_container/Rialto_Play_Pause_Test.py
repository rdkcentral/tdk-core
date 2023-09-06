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
  <name>Rialto_Play_Pause_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>getSSHParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify cobalt play pause operations using rialto source</synopsis>
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
    <box_type>RDKTV</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RIALTO_CONTAINER_03</test_case_id>
    <test_objective>To verify cobalt play pause operations using rialto source</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator, RDKTV</test_setup>
    <pre_requisite>Cobalt dac bundle must be hosted in a server and COBALT_DAC_BUNDLE_PATH configuration must be set</pre_requisite>
    <api_or_interface_used>LISA.1.install,LISA.1.getList, org.rdk.RDKShell.1.launchApplication, org.rdk.RDKShell.1.generateKey, org.rdk.RDKShell.1.setFocus, org.rdk.RDKShell.1.kill</api_or_interface_used>
    <input_parameters>COBALT_DAC_BUNDLE_PATH</input_parameters>
    <automation_approch>1. Install com.rdk.cobalt application from COBALT_DAC_BUNDLE_PATH if not already installed in DUT.
    2. check if application is successfully installed using LISA.1.getList
    3. launch com.rdk.cobalt application using RDKShell API.
    4. setFocus to com.rdk.cobalt.
    5. check if rialto server is running.
    6. using generateKey method press down arrow and OK button to select and play a video.
    7. pause the playback using spacebar key press
    8. verify video playback using PROC validation script configured.
    9. kill the cobalt application</automation_approch>
    <expected_output>Video playback must be proper after launching cobalt application</expected_output>
    <priority>High</priority>
    <test_stub_interface>LISA, RDKShell</test_stub_interface>
    <test_script>Rialto_Play_Pause_Test</test_script>
    <skipped></skipped>
    <release_version>M116</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from time import sleep

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rialto_container","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Rialto_Play_Pause_Test');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;

expectedResult="SUCCESS"

if "SUCCESS" in result.upper():
    tdkTestObj = obj.createTestStep('checkApplicationInstalled');
    tdkTestObj.executeTestCase(expectedResult);
    installed = tdkTestObj.getResultDetails();
    if installed == "FAILURE":
        tdkTestObj.setResultStatus("SUCCESS")
        tdkTestObj = obj.createTestStep('InstallApplication')
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResultDetails();
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
            tdkTestObj = obj.createTestStep('checkApplicationInstalled');
            tdkTestObj.executeTestCase(expectedResult);
            installed = tdkTestObj.getResultDetails();

    launched = "FAILURE"
    if installed == "SUCCESS":
        tdkTestObj.setResultStatus("SUCCESS")
        tdkTestObj = obj.createTestStep('LaunchApplication')
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResultDetails();
        if result == "SUCCESS":
            launched = "SUCCESS"
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Application installation failed"
        tdkTestObj.setResultStatus("FAILURE")

    server_running = "FAILURE"
    if launched == "SUCCESS":
        sleep(10)
        tdkTestObj = obj.createTestStep('executeInDUT')
        #Check if rialto server is being active
        command = "ps -ef | grep  RialtoServer | grep -v grep"
        tdkTestObj.addParameter("command",command)
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResultDetails();
        print result
        if "RialtoServer" in result:
            print "RialtoServer is running as expected"
            server_running = "SUCCESS"
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "RialtoServer is not running"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Application launch failed"
        tdkTestObj.setResultStatus("FAILURE")

    launch_video = "FAILURE"
    if server_running == "SUCCESS":
        tdkTestObj = obj.createTestStep('Press_key')
        #press down arrow
        key=40
        tdkTestObj.addParameter("key_code",key)
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResultDetails();
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
            #press ok
            key=13
            tdkTestObj.addParameter("key_code",key)
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResultDetails();
            if result != "SUCCESS":
                tdkTestObj.setResultStatus("FAILURE")
            else:
                tdkTestObj.setResultStatus("SUCCESS")
                #Wait for Video to Start
                sleep(20)
                #At this point video is playing,pressing "spacebar" to pause the video
                key=32
                tdkTestObj.addParameter("key_code",key)
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResultDetails();
                if result != "SUCCESS":
                    tdkTestObj.setResultStatus("FAILURE")
                else:
                    tdkTestObj.setResultStatus("SUCCESS")
                    launch_video = "SUCCESS"
        else:
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Application launch failed"
        tdkTestObj.setResultStatus("FAILURE")

    if launch_video == "SUCCESS":
        #Wait for Pause
        sleep(2)

        log_verification = False
        tdkTestObj = obj.createTestStep('checkPROC')
        tdkTestObj.addParameter("check_pause","True")
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResultDetails();
        print "AV status result",result
        if "NOT_ENABLED" in result:
            print "PROC_ENTRY validation is disabled , checking wpeframeowrk.log for video validation"
            log_verification = True
        elif "FAILURE" in result:
            print "AV status not proper as proc entry validation failed"
            tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("SUCCESS")

        if log_verification:
            tdkTestObj = obj.createTestStep('executeInDUT')
            #Check if rialto source is being used
            command1 = "journalctl --since \"2 minutes ago\" -x -u wpeframework | awk '/Video/ && /Rialto/'"
            tdkTestObj.addParameter("command",command1)
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResultDetails();
            print result
            if "appsrc" in result:
                print "Video is playing fine"
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "Video is not playing"
                tdkTestObj.setResultStatus("FAILURE")

            command2 = "journalctl --since \"2 minutes ago\" -x -u wpeframework | awk '/Audio/ && /Rialto/'"
            tdkTestObj.addParameter("command",command1)
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResultDetails();
            print result
            if "appsrc" in result:
                print "Audio is playing fine"
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "Audio is not playing"
                tdkTestObj.setResultStatus("FAILURE")

    if launched == "SUCCESS":
        tdkTestObj.setResultStatus("SUCCESS")
        tdkTestObj = obj.createTestStep('KillApplication')
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResultDetails();
        if result == "SUCCESS":
            launched = "SUCCESS"
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            tdkTestObj.setResultStatus("FAILURE")
       
obj.unloadModule("rialto_container");
