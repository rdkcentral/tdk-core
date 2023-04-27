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
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_Container_Cobalt_TimeTo_PlayNextVideo</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>containerization_launchApplication</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate the time taken to start a new video after playing a given video in Cobalt.</synopsis>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>Containerization_15</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to start a new video after playing a given video in Cobalt.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Configure the values SSH Method (variable $SSH_METHOD), DUT username (variable $SSH_USERNAME)and password of the DUT (variable $SSH_PASSWORD)  available in fileStore/device.config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>COBALT_DETAILS</input_parameters>
    <automation_approch>1. After start on the device, ensure that Dobby is running
2. Enable datamodel values
3. Reboot the device or restart WPEFramework service
4. Verify datamodel values
5. Launch Cobalt
6. Verify that Cobalt is running in container mode
7. Check wpeframework.log
8. Set video URL using deeplink method.
9. Click OK to start video playback.
10. Validate video playback using decoder logs
11. Click down arrow key 2 times and then press ok to select the new video.
12. Check gstplayer state change logs in wpeframework log to get the next video start time.
13. Validate the time taken to play the new video.</automation_approch>
    <expected_output>Time taken should be within the expected limit.</expected_output>
    <priority>High</priority>
    <test_stub_interface>containerization</test_stub_interface>
    <test_script>RDKV_Container_LifecycleManagement_Cobalt</test_script>
    <skipped>No</skipped>
    <release_version>M112</release_version>
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
obj.configureTestCase(ip,port,'RDKV_Container_Cobalt_TimeTo_PlayNextVideo');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Retrieving Configuration values from config file......."
    configKeyList = ["SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD", "COBALT_DETAILS","COBALT_PLAYBACK_URL","COBALT_PLAY_TIME_THRESHOLD_VALUE","THRESHOLD_OFFSET"]
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
            cobalt_playback_url = configValues["COBALT_PLAYBACK_URL"]
            cobalt_play_threshold = configValues["COBALT_PLAY_TIME_THRESHOLD_VALUE"]
            offset = configValues["THRESHOLD_OFFSET"]
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
    #tdkTestObj.addParameter("sshMethod", ssh_method);
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
            print "Launch Cobalt"
            tdkTestObj = obj.createTestStep('containerization_launchApplication')
            #tdkTestObj.addParameter("launch",cobalt_details)
            tdkTestObj.addParameter("launch",configValues["COBALT_DETAILS"])
            tdkTestObj.executeTestCase(expectedResult)
            actualresult = tdkTestObj.getResultDetails()
            if expectedResult == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
                print "Check container is running"
                tdkTestObj = obj.createTestStep('containerization_checkContainerRunningState')
                tdkTestObj.addParameter("callsign",cobalt_details)
                tdkTestObj.executeTestCase(expectedResult)
                actualresult = tdkTestObj.getResultDetails()
                if expectedResult in actualresult.upper():
                    tdkTestObj.setResultStatus("SUCCESS")
                    #Check for Container launch logs
                    command = 'cat /opt/logs/wpeframework.log | grep "launching Cobalt in container mode"'
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
                    if "launching Cobalt in container mode" in output:
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
                            tdkTestObj.executeTestCase(expectedResult)
                            time.sleep(10)
                            keycode_list = ['40', '40', '13']
                            print "\n Play next video"
                            for keycode in keycode_list:
                                params = '{"keys":[ {"keyCode": ' + keycode + ',"modifiers": [],"delay":1.0}]}'
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                                tdkTestObj.addParameter("value",params)
                                if keycode == '13':
                                    play_start_time = str(datetime.utcnow()).split()[1]
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                if expectedResult in result:
                                    print "\n Sending keycode : {} using generateKey".format(keycode)
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "\n Error while executing generateKey method with keycode: {}".format(keycode)
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            else:
                                time.sleep(25)
                                print "\n Check the logs from DUT"
                                command = 'cat /opt/logs/wpeframework.log | grep -inr State.*changed.*old.*PAUSED.*new.*PLAYING | tail -1'
                                tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                                tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                                tdkTestObj.addParameter("command",command)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                output = tdkTestObj.getResultDetails()
                                if output != "EXCEPTION" and expectedResult in result and "old: PAUSED" in output:
                                    playing_log = output.split('\n')[1]
                                    print "\n Playing log  :",playing_log
                                    play_starttime_in_millisec = getTimeInMilliSec(play_start_time)
                                    video_playedtime = getTimeStampFromString(playing_log)
                                    video_playedtime_in_millisec = getTimeInMilliSec(video_playedtime)
                                    time_for_video_play = video_playedtime_in_millisec - play_starttime_in_millisec
                                    #Get threshold values from device config file
                                    conf_file,file_status = getConfigFileName(obj.realpath)
                                    result2,cobalt_play_threshold = getDeviceConfigKeyValue(conf_file,"COBALT_PLAY_NEXT_VIDEO_TIME_THRESHOLD_VALUE")
                                    offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                    Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                                    if all(value != "" for value in (cobalt_play_threshold,offset)):
                                        print "\n Play initiated at {}".format(play_start_time)
                                        Summ_list.append('Play initiated at :{}'.format(play_start_time))
                                        print "\n Play happend at {}".format(video_playedtime)
                                        Summ_list.append('Play happend at :{}'.format(video_playedtime))
                                        print "\n Time taken for play operation: {} milliseconds \n".format(time_for_video_play)
                                        Summ_list.append('Time taken for play operation :{}ms'.format(time_for_video_play))
                                        print "\n Threshold value for Time taken for playing next video: {} milliseconds \n".format(cobalt_play_threshold)
                                        if 0 < int(time_for_video_play) < (int(cobalt_play_threshold) + int(offset)):
                                            print "\n Time taken for play operation is within the expected limit"
                                            tdkTestObj.setResultStatus("SUCCESS")
                                        else:
                                            print "\n Time taken for play operation is not within the expected limit"
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print "\n Please configure the threshold values in device config file"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "Unable to get the required logs from DUT"
                                    tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "Error in launching Cobalt in container mode"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "Unable to get the required logs to validate whether cobalt is launched in container mode"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "Error in checking the container running state"
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
