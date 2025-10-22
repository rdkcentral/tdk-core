##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2024 RDK Management
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
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PACS_Cobalt_PlayPause_Hibernate_Restore</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate Cobalt Play Pause after restoring from Hibernated state</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_149</test_case_id>
    <test_objective>The objective of this test is to validate cobalt Play Pause after restoring from hibernated state</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url:string</input_parameters>
    <automation_approch>1. As a pre requisite, disable all the other plugins and enable Cobalt only.
2.Suspend the cobalt and check the satus of the cobalt if its in hibernated state
3.Restore the cobalt to suspend state.
4.Launch the cobalt using deeplink method using cobalt url configured
5. Validate if the video is playing using proc entries.
6. Generate key press corresponding to space key which will pause the video and wait 10 seconds.
7. Validate if the video is paused using proc entries.
8. Generate key press corresponding to space key which will play the video.
9. Validate if the video is playing using proc entries.
10. Revert all values.</automation_approch>
    <expected_output>Once the cobalt is restored from hibernated state ,video must pause after pressing space key and it should continue to play after space key is pressed again.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_PlayPause_Hibernate_Restore</test_script>
    <skipped>No</skipped>
    <release_version>M129</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from rdkv_performancelib import *
import rdkv_performancelib
import PerformanceTestVariables
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_PlayPause_Hibernate_Restore');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url;
    print("Check Pre conditions")
    if cobalt_test_url == "":
        print("\n Please configure the cobalt_test_url value\n")
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated"}
    if curr_plugins_status_dict != plugin_status_needed:
        if curr_plugins_status_dict.get("Cobalt") == "hibernated":
           restore_plugin(obj,"Cobalt")
           time.sleep(5)
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
    cobalt_launch_status = launch_cobalt(obj)    
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if status == "SUCCESS" and cobalt_launch_status == "SUCCESS" and cobalt_test_url != "" and ssh_param_dict != {}  :
        print("\nPre conditions for the test are set successfully")
        time.sleep(30)
        suspend_status,start_suspend = suspend_plugin(obj,"Cobalt")
        if suspend_status == expectedResult:
            time.sleep(10)
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","Cobalt")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            cobalt_status = tdkTestObj.getResultDetails()
            if cobalt_status == 'hibernated' and expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(5)
                print("\nCobalt hibernated successfully and trying to restore the app\n")
                restore_status,start_restore =restore_plugin(obj,"Cobalt")
                if restore_status == expectedResult:
                   tdkTestObj.setResultStatus("SUCCESS")
                   time.sleep(10)
                   tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                   tdkTestObj.addParameter("plugin","Cobalt")
                   tdkTestObj.executeTestCase(expectedResult)
                   result = tdkTestObj.getResult()
                   cobalt_status = tdkTestObj.getResultDetails()
                   if cobalt_status == 'suspended' and expectedResult in result:
                      print("\nCobalt suspended successfully\n")
                      tdkTestObj.setResultStatus("SUCCESS")                   
                      cobalt_launch_status = launch_cobalt(obj)
                      time.sleep(5)
                      if cobalt_launch_status  == expectedResult:
                          print("\nCobalt launched successfully\n")              
                          print("\n Set the URL : {} using Cobalt deeplink method \n".format(cobalt_test_url))
                          tdkTestObj = obj.createTestStep('rdkservice_setValue')
                          tdkTestObj.addParameter("method","Cobalt.1.deeplink")
                          tdkTestObj.addParameter("value",cobalt_test_url)
                          video_start_time = str(datetime.now()).split()[1][:-3]
                          tdkTestObj.executeTestCase(expectedResult)
                          cobalt_result = tdkTestObj.getResult()
                          time.sleep(10)
                          if(cobalt_result == expectedResult):
                                   tdkTestObj.setResultStatus("SUCCESS")
                                   print("Clicking OK to play video")
                                   params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                                   tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                   tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                                   tdkTestObj.addParameter("value",params)                                   
                                   tdkTestObj.executeTestCase(expectedResult)
                                   result1 = tdkTestObj.getResult()
                                   time.sleep(40)
                                   #Skip if Ad is playing by pressing OK
                                   params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                                   tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                   tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                                   tdkTestObj.addParameter("value",params)
                                   tdkTestObj.executeTestCase(expectedResult)
                                   result2 = tdkTestObj.getResult()
                                   time.sleep(50)
                                   if "SUCCESS" == (result1 and result2):
                                      print("\n Check video is started \n")
                                      command = 'cat /opt/logs/wpeframework.log | grep -inr State.*changed.*old.*PAUSED.*new.*PLAYING | tail -1'
                                      tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                      tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                                      tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                                      tdkTestObj.addParameter("command",command)
                                      tdkTestObj.executeTestCase(expectedResult)
                                      result = tdkTestObj.getResult()
                                      output = tdkTestObj.getResultDetails()
                                      if output != "EXCEPTION" and expectedResult in result and "old: PAUSED" in output:
                                         video_playing_log = output.split('\n')[1]
                                         video_play_starttime_in_millisec = getTimeInMilliSec(video_start_time)
                                         video_played_time = getTimeStampFromString(video_playing_log)
                                         video_played_time_in_millisec = getTimeInMilliSec(video_played_time)
                                         if video_played_time_in_millisec > video_play_starttime_in_millisec:
                                            print("\n Video started Playing\n")
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            time.sleep(10)
                                            print("\n Pausing Video \n")
                                            params = '{"keys":[ {"keyCode": 32,"modifiers": [],"delay":1.0}]}'
                                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                                            tdkTestObj.addParameter("value",params)
                                            pause_start_time = str(datetime.now()).split()[1][:-3]
                                            tdkTestObj.executeTestCase(expectedResult)
                                            result = tdkTestObj.getResult()
                                            if result == "SUCCESS":
                                               time.sleep(20)
                                               tdkTestObj.setResultStatus("SUCCESS")
                                               print("\n Check video is paused \n")
                                               command = 'cat /opt/logs/wpeframework.log | grep -inr State.*changed.*old.*PLAYING.*new.*PAUSED | tail -1'
                                               tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                               tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                                               tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
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
                                                      print("\n Video is paused \n")
                                                      tdkTestObj.setResultStatus("SUCCESS")
                                                      #Play video
                                                      print("\n Play video \n")
                                                      params = '{"keys":[ {"keyCode": 32,"modifiers": [],"delay":1.0}]}'
                                                      tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                                      tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                                                      tdkTestObj.addParameter("value",params)
                                                      play_start_time = str(datetime.now()).split()[1][:-3]
                                                      tdkTestObj.executeTestCase(expectedResult)
                                                      result = tdkTestObj.getResult()
                                                      if result == "SUCCESS":
                                                          print("\n Check video is playing \n")
                                                          time.sleep(20)
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
                                                             play_starttime_in_millisec = getTimeInMilliSec(play_start_time)
                                                             video_playedtime = getTimeStampFromString(playing_log)
                                                             print("\n Played time",video_playedtime)
                                                             video_playedtime_in_millisec = getTimeInMilliSec(video_playedtime)
                                                             if video_played_time_in_millisec > video_play_starttime_in_millisec:
                                                                print("\n Video started Playing\n")
                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                             else:
                                                                 print("\n Video is not Playing\n")
                                                                 tdkTestObj.setResultStatus("FAILURE")
                                                                 exit()
                                                          else:
                                                              print("\n Video play related logs are not available")
                                                              tdkTestObj.setResultStatus("FAILURE")
                                                      else:
                                                          print("\n Error while executing generateKey method \n")
                                                          tdkTestObj.setResultStatus("FAILURE")
                                                  else:
                                                     print("\n Video is not paused  \n")
                                                     tdkTestObj.setResultStatus("FAILURE")
                                               else:
                                                  print("\n Video pause related logs are not available")
                                                  tdkTestObj.setResultStatus("FAILURE")
                                  
                                         else:
                                            print("\n Video is not started playing \n")
                                            tdkTestObj.setResultStatus("FAILURE")
                                      else:
                                          print("\n Video play related logs are not available \n")
                                          tdkTestObj.setResultStatus("FAILURE")
                                   else:
                                       print("\n Error while executing generateKey method \n")
                                       tdkTestObj.setResultStatus("FAILURE")
                          else:
                             print("Unable to load the cobalt_test_url")
                             tdkTestObj.setResultStatus("FAILURE")
                      else:
                         print("\n Failed to launch Cobalt  ")
                         tdkTestObj.setResultStatus("FAILURE")
                   else:
                       print("\n Failed to Suspend Cobalt App") 
                       tdkTestObj.setResultStatus("FAILURE")     
                else:
                    print("\n Failed to restore cobalt from Hibernated state")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("\n Failed to hibernate cobalt app")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("\n Failed to Suspend Cobalt App") 
            tdkTestObj.setResultStatus("FAILURE")   
        print("\n Exiting from Cobalt \n")
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin","Cobalt")
        tdkTestObj.addParameter("status","deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print("Unable to deactivate Cobalt")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("\n Preconditions are not met \n")
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print("Revert the values before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")