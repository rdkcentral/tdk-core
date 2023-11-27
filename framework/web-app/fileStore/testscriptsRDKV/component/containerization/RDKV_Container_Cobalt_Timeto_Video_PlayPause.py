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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_Container_Cobalt_Timeto_Video_PlayPause</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>containerization_launchApplication</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Start playback in youtube then calculate time to play and pause video</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>Containerization_13</test_case_id>
    <test_objective>Start playback in youtube then calculate time to play and pause video</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator,RDKTV</test_setup>
    <pre_requisite>1. Configure the values SSH Method (variable $SSH_METHOD), DUT username (variable $SSH_USERNAME)and password of the DUT (variable $SSH_PASSWORD)  available in fileStore/device.config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>COBALT_DETAILS=</input_parameters>
    <automation_approch>"1.  After start on the device, ensure that Dobby is running
2. Enable datamodel values
3. Reboot the device or restart WPEFramework service
4. Verify datamodel values
5. Launch Cobalt
6. Verify that Cobalt is running in container mode
7. Check wpeframework.log
8. Start playback
9.Pause Video
10. Calculate time to pause and play from wpeframework.log
</automation_approch>
    <expected_output>Time to video play and pause must be within threshold limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>containerization</test_stub_interface>
    <test_script>RDKV_Container_Cobalt_Timeto_Video_PlayPause</test_script>
    <skipped>No</skipped>
    <release_version>M111</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from containerizationlib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("containerization","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Container_Cobalt_Timeto_Video_PlayPause');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Retrieving Configuration values from config file......."
    configKeyList = ["SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD", "COBALT_DETAILS", "COBALT_PLAYBACK_URL_CONTAINER", "COBALT_PAUSE_TIME_THRESHOLD_VALUE_CONTAINER", "COBALT_PLAY_TIME_THRESHOLD_VALUE_CONTAINER", "THRESHOLD_OFFSET_IN_CONTAINER"]
    configValues = {}
    #Get each configuration from device config file
    for configKey in configKeyList:
        tdkTestObj = obj.createTestStep('containerization_getDeviceConfig')
        tdkTestObj.addParameter("basePath",obj.realpath)
        tdkTestObj.addParameter("configKey",configKey)
        tdkTestObj.executeTestCase("SUCCESS")
        configValues[configKey] = tdkTestObj.getResultDetails()
        if "FAILURE" not in configValues[configKey] and configValues[configKey] != "":
            print "SUCCESS: Successfully retrieved %s configuration from device config file" %(configKey)
        else:
            print "FAILURE: Failed to retrieve %s configuration from device config file" %(configKey)
            if configValues[configKey] == "":
                print "\n [INFO] Please configure the %s key in the device config file" %(configKey)
                result = "FAILURE"
                break
    if "FAILURE" != result:
        if "directSSH" == configValues["SSH_METHOD"]:
            ssh_method = configValues["SSH_METHOD"]
            user_name = configValues["SSH_USERNAME"]
            cobalt_details = configValues["COBALT_DETAILS"]
            cobalt_playback_url = configValues["COBALT_PLAYBACK_URL_CONTAINER"]
            cobalt_pause_threshold = configValues["COBALT_PAUSE_TIME_THRESHOLD_VALUE_CONTAINER"]
            cobalt_play_threshold = configValues["COBALT_PLAY_TIME_THRESHOLD_VALUE_CONTAINER"]
            offset = configValues["THRESHOLD_OFFSET_IN_CONTAINER"]
            if configValues["SSH_PASSWORD"] == "None":
                password = ""
            else:
                password = configValues["SSH_PASSWORD"]
        else:
            print "FAILURE: Currently only supports directSSH ssh method"
            config_status = "FAILURE"
    else:
        config_status = "FAILURE"

    credentials = obj.IP + ',' + configValues["SSH_USERNAME"] + ',' + configValues["SSH_PASSWORD"]
    print "\nTo Ensure Dobby service is running"
    command = 'systemctl status dobby | grep active | grep -v inactive'
    print "COMMAND : %s" %(command)

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('containerization_executeInDUT');
    #Add the parameters to ssh to the DUT and execute the command
    tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
    tdkTestObj.addParameter("credentials", credentials);
    tdkTestObj.addParameter("command", command);

    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedResult);
    result = tdkTestObj.getResult()

    #Get the result of execution
    output = tdkTestObj.getResultDetails();
    if "Active: active" in output and expectedResult in result:
        print "Dobby is running %s" %(output)
        #To enable datamodel
        datamodel=["Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Dobby.Cobalt.Enable"]
        tdkTestObj = obj.createTestStep('containerization_setPreRequisites')
        tdkTestObj.addParameter("datamodel",datamodel)
        tdkTestObj.executeTestCase(expectedResult)
        actualresult= tdkTestObj.getResultDetails()
        if expectedResult in actualresult.upper():
            tdkTestObj.setResultStatus("SUCCESS")
            time.sleep(15)
            print "Launch Cobalt"
            tdkTestObj = obj.createTestStep('containerization_launchApplication')
            tdkTestObj.addParameter("launch",cobalt_details)
            tdkTestObj.executeTestCase(expectedResult)
            actualresult = tdkTestObj.getResultDetails()
            if expectedResult in actualresult.upper():
                tdkTestObj.setResultStatus("SUCCESS")
                print "Check container is running"
                tdkTestObj = obj.createTestStep('containerization_checkContainerRunningState')
                tdkTestObj.addParameter("callsign",cobalt_details)
                tdkTestObj.executeTestCase(expectedResult)
                actualresult = tdkTestObj.getResultDetails()
                if expectedResult in actualresult.upper():
                    tdkTestObj.setResultStatus("SUCCESS")
                    #Check for Container launch logs
                    command = 'cat /opt/logs/wpeframework.log | grep "launching cobalt in container mode"'
                    print "COMMAND : %s" %(command)
                    #Primitive test case which associated to this Script
                    tdkTestObj = obj.createTestStep('containerization_executeInDUT');
                    #Add the parameters to ssh to the DUT and execute the command
                    tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                    tdkTestObj.addParameter("credentials", credentials);
                    tdkTestObj.addParameter("command", command);

                    #Execute the test case in DUT
                    tdkTestObj.executeTestCase(expectedResult);
                    output = tdkTestObj.getResultDetails()
                    if "launching cobalt in container mode" in output:
                        print "Cobalt launched successfully in container mode"
                        print "\n Set the URL : {} using Cobalt deeplink method"
                        tdkTestObj = obj.createTestStep('containerization_setValue')
                        tdkTestObj.addParameter("method","Cobalt.1.deeplink")
                        tdkTestObj.addParameter("value",cobalt_playback_url)
                        tdkTestObj.executeTestCase(expectedResult)
                        cobalt_result = tdkTestObj.getResult()
                        time.sleep(10)
                        if(cobalt_result in expectedResult):
                            tdkTestObj.setResultStatus("SUCCESS")
                            print "Clicking OK to play video"
                            params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                            tdkTestObj = obj.createTestStep('containerization_setValue')
                            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                            tdkTestObj.addParameter("value",params)
                            video_start_time = str(datetime.utcnow()).split()[1]
                            tdkTestObj.executeTestCase(expectedResult)
                            result1 = tdkTestObj.getResult()
                            time.sleep(50)
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                            tdkTestObj.addParameter("value",params)
                            tdkTestObj.executeTestCase(expectedResult)
                            result2 = tdkTestObj.getResult()
                            time.sleep(50)
                            if "SUCCESS" == (result1 and result2):
                                print "\n Check video is started \n"
                                command = 'cat /opt/logs/dobby.log | grep -inr State.*changed.*old.*PAUSED.*new.*PLAYING | tail -1'
                                tdkTestObj = obj.createTestStep('containerization_executeInDUT');
                                #Add the parameters to ssh to the DUT and execute the command
                                tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                                tdkTestObj.addParameter("credentials", credentials);
                                tdkTestObj.addParameter("command", command);
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                output = tdkTestObj.getResultDetails()
                                if output != "EXCEPTION" and expectedResult in result and "old: PAUSED" in output:
                                    video_playing_log = output.split('\n')[1]
                                    video_play_starttime_in_millisec = getTimeInMilliSec(video_start_time)
                                    video_played_time = getTimeStampFromString(video_playing_log)
                                    video_played_time_in_millisec = getTimeInMilliSec(video_played_time)
                                    if video_played_time_in_millisec > video_play_starttime_in_millisec:
                                        print "\n Video started Playing\n"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        time.sleep(10)
                                        print "\n Pausing Video \n"
                                        params = '{"keys":[ {"keyCode": 32,"modifiers": [],"delay":1.0}]}'
                                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                                        tdkTestObj.addParameter("value",params)
                                        pause_start_time = str(datetime.utcnow()).split()[1]
                                        tdkTestObj.executeTestCase(expectedResult)
                                        result = tdkTestObj.getResult()
                                        if result == "SUCCESS":
                                            time.sleep(20)
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print "\n Check video is paused \n"
                                            command = 'cat /opt/logs/dobby.log | grep -inr State.*changed.*old.*PLAYING.*new.*PAUSED | tail -1'
                                            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                            tdkTestObj.addParameter("ssh_method",configValues["SSH_METHOD"])
                                            tdkTestObj.addParameter("credentials", credentials)
                                            tdkTestObj.addParameter("command",command)
                                            tdkTestObj.executeTestCase(expectedResult)
                                            result = tdkTestObj.getResult()
                                            output = tdkTestObj.getResultDetails()
                                            if output != "EXCEPTION" and expectedResult in result and "old: PLAYING" in output:
                                                pause_log = output.split('\n')[1]
                                                pause_starttime_in_millisec = getTimeInMilliSec(pause_start_time)
                                                video_pausedtime = getTimeStampFromString(pause_log)
                                                video_pausedtime_in_millisec = getTimeInMilliSec(video_pausedtime)
                                                time_for_video_pause = video_pausedtime_in_millisec - pause_starttime_in_millisec
                                                if video_pausedtime_in_millisec > pause_starttime_in_millisec:
                                                    print "\n Video is paused \n"
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    #Play video
                                                    print "\n Play video \n"
                                                    params = '{"keys":[ {"keyCode": 32,"modifiers": [],"delay":1.0}]}'
                                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                                                    tdkTestObj.addParameter("value",params)
                                                    play_start_time = str(datetime.utcnow()).split()[1]
                                                    tdkTestObj.executeTestCase(expectedResult)
                                                    result = tdkTestObj.getResult()
                                                    if result == "SUCCESS":
                                                        print "\n Check video is playing \n"
                                                        time.sleep(20)
                                                        command = 'cat /opt/logs/dobby.log | grep -inr State.*changed.*old.*PAUSED.*new.*PLAYING | tail -1'
                                                        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                                        tdkTestObj.addParameter("ssh_method",configValues["SSH_METHOD"])
                                                        tdkTestObj.addParameter("credentials",credentials)
                                                        tdkTestObj.addParameter("command",command)
                                                        tdkTestObj.executeTestCase(expectedResult)
                                                        result = tdkTestObj.getResult()
                                                        output = tdkTestObj.getResultDetails()
                                                        if output != "EXCEPTION" and expectedResult in result and "old: PAUSED" in output:
                                                            playing_log = output.split('\n')[1]
                                                            play_starttime_in_millisec = getTimeInMilliSec(play_start_time)
                                                            video_playedtime = getTimeStampFromString(playing_log)
                                                            print "\n Played time",video_playedtime
                                                            video_playedtime_in_millisec = getTimeInMilliSec(video_playedtime)
                                                            time_for_video_play = video_playedtime_in_millisec - play_starttime_in_millisec
                                                            #Get threshold values from device config file
                                                            conf_file,file_status = getConfigFileName(obj.realpath)
                                                            result1,cobalt_pause_threshold = getDeviceConfigKeyValue(conf_file,"COBALT_PAUSE_TIME_THRESHOLD_VALUE_CONTAINER")
                                                            result2,cobalt_play_threshold = getDeviceConfigKeyValue(conf_file,"COBALT_PLAY_TIME_THRESHOLD_VALUE_CONTAINER")
                                                            offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET_IN_CONTAINER")
                                                            if all(value != "" for value in (cobalt_pause_threshold,cobalt_play_threshold,offset)):
                                                                print "\n play initiated at {} ".format(play_start_time)
                                                                print "\n play happend at {} ".format(video_playedtime)
                                                                print "\n Time taken for play operation: {} milliseconds \n".format(time_for_video_play)
                                                                print "\n Threshold value for time taken for play operation : {} ms".format(cobalt_play_threshold)
                                                                if 0 < int(time_for_video_play) < (int(cobalt_play_threshold) + int(offset)):
                                                                    print "\n Time taken for play operation is within the expected limit"
                                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                                else:
                                                                    print "\n Time taken for play operation is not within the expected limit"
                                                                    tdkTestObj.setResultStatus("FAILURE")
                                                                print "\n pause initiated at {} ".format(pause_start_time)
                                                                print "\n pause happend at {} (UTC)".format(video_pausedtime)
                                                                print "\n Time taken for pause operation: {} milleseconds \n".format(time_for_video_pause)
                                                                print "\n Threshold value for time taken for pause operation : {} ms".format(cobalt_pause_threshold)
                                                                if 0 < int(time_for_video_pause) < (int(cobalt_pause_threshold) + int(offset)):
                                                                    print "\n Time taken for pause operation is within the expected limit \n"
                                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                                else:
                                                                    print "\n Time taken for pause operation is not within the expected limit \n"
                                                                    tdkTestObj.setResultStatus("FAILURE")
                                                            else:
                                                                print "\n Please configure the threshold values in device config file \n"
                                                                tdkTestObj.setResultStatus("FAILURE")
                                                        else:
                                                            print "\n Video play related logs are not available"
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                    else:
                                                        print "\n Error while executing generateKey method \n"
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                else:
                                                    print "\n Video pause related logs are not available \n"
                                                    tdkTestObj.setResultStatus("FAILURE")
                                            else:
                                                print "\n Video pause related logs are not available"
                                                tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            print "\n Error while executing generateKey method \n"
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print "\n Video is not started playing \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "Video play related logs not available"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "Generate key method failed"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "Unable to launch the url"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "Unable to get the required logs"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "Cobalt is not running in container mode"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "Failed to launch Cobalt"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "Failed to enable data model value"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Dobby service is not running"
        tdkTestObj.setResultStatus("FAILURE")

tdkTestObj = obj.createTestStep('containerization_setPostRequisites')
tdkTestObj.addParameter("datamodel",datamodel)
tdkTestObj.executeTestCase(expectedResult)
actualresult = tdkTestObj.getResultDetails()
if expectedResult in actualresult.upper():
    tdkTestObj.setResultStatus("SUCCESS")
else:
    print "Set Post Requisites Failed"
    tdkTestObj.setResultStatus("FAILURE")

obj.unloadModule("containerization");
