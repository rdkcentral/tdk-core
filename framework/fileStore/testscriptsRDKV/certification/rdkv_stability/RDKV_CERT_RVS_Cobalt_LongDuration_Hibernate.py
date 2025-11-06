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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_RVS_Cobalt_LongDuration_Hibernate</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateResourceUsage</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test validates long duration Hibernated state of Cobalt app for a given amount of time</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>120</execution_time>
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
    <test_case_id>RDKV_STABILITY_71</test_case_id>
    <test_objective>The objective of this test is to do the stability testing by placing Cobalt in hibernated state for a given amount of time and get the cpu load.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. Time upto which the cobalt should be in hibernated state
2. Maximum allowed CPU load
3. Maximum allowed Memory usage</input_parameters>
    <automation_approch>1. As a prerequisite, disable all the other plugins 
   and enable Cobalt only.
2. Set the cobalt to hibernated state
3. Validate if the cobalt can restore after long hibernated state.
4. Validate CPU load
5. Validate memory usage
6. Revert all values</automation_approch>
    <expected_output>The cobalt should be in Hibernated state for the given time and should be successfully restored </expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Cobalt_LongDuration_Hibernate</test_script>
    <skipped>No</skipped>
    <release_version>M129</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from BrowserPerformanceUtility import *
import BrowserPerformanceUtility
from rdkv_performancelib import *
import rdkv_performancelib
import StabilityTestVariables
from StabilityTestUtility import *
from SSHUtility import *
import ast
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Cobalt_LongDuration_Hibernate');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}{}_{}_{}_CPUMemoryInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
cpu_mem_info_dict = {}
test_interval = 300

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):  
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url;  
    print("Check Pre conditions")
    if cobalt_test_url == "":
        print("\n Please configure the cobalt_test_url value\n")
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"resumed","DeviceInfo":"activated"}
    conf_file, status = get_configfile_name(obj);
    status,supported_plugins = getDeviceConfigValue(conf_file,"SUPPORTED_PLUGINS")
    for plugin in plugins_list[:]:
        if plugin not in supported_plugins:
            plugins_list.remove(plugin)
            plugin_status_needed.pop(plugin)
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    status = "SUCCESS"
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        status = "FAILURE"
        print("\n Error while getting status of plugins")
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        if curr_plugins_status_dict.get("Cobalt") == "hibernated":
          restore_plugin(obj,"Cobalt")
          time.sleep(5)
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    cobal_launch_status = launch_cobalt(obj)    
    validation_dict = get_validation_params(obj)
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if status == "SUCCESS" and cobal_launch_status == "SUCCESS" and validation_dict != {} and cobalt_test_url != "" and ssh_param_dict != {}:
        time.sleep(30)
        print("\nPre conditions for the test are set successfully")
        print("\n Set the cobalt in Hibernate state by suspending it.")
        print("\nSuspend the Cobalt plugin :\n")
        params = '{"callsign":"Cobalt"}'
        tdkTestObj = obj.createTestStep('rdkservice_setValue')
        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.suspend")
        tdkTestObj.addParameter("value",params)
        tdkTestObj.executeTestCase(expectedResult)
        time.sleep(5)
        result = tdkTestObj.getResult()
        if result == expectedResult:
            tdkTestObj.setResultStatus("SUCCESS")
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","Cobalt")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            cobalt_status = tdkTestObj.getResultDetails()
            if cobalt_status == 'hibernated' and expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(5)
                print("\nCobalt is in hibernated state")
                #Validating Resource usage 
                test_time_in_mins = int(StabilityTestVariables.cobalt_hibernate_test_duration)
                test_time_in_millisec = test_time_in_mins * 60 * 1000
                time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
                iteration = 0
                completed = True
                while int(round(time.time() * 1000)) < time_limit:                   
                   # Check Cobalt's state every 15 minutes 
                   if (iteration % 4) == 0: 
                       print("\n Validating the cobalt Hibernate state ")
                       tdkTestObj.setResultStatus("SUCCESS")
                       tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                       tdkTestObj.addParameter("plugin","Cobalt")
                       tdkTestObj.executeTestCase(expectedResult)
                       result = tdkTestObj.getResult()
                       cobalt_status = tdkTestObj.getResultDetails()                                  
                       if cobalt_status != 'hibernated':
                            # If Cobalt is not in hibernation, fail the test case and break the loop
                            print("\n cobalt exited from Hibernate state")
                            tdkTestObj.setResultStatus("FAILURE")
                            completed = False
                            break                   
                   iteration += 1                   
                   time.sleep(test_interval)
                if completed:
                   print("\nsuccessfully completed the {} times in {} minutes".format(iteration,test_time_in_mins))
                   print("Cobalt remained in hibernated state for the configured time and trying to restore the app\n")
                   restore_status,start_restore =restore_plugin(obj,"Cobalt")
                   if restore_status == expectedResult:
                        time.sleep(10)
                        tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                        tdkTestObj.addParameter("plugin","Cobalt")
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        cobalt_status = tdkTestObj.getResultDetails()
                        if cobalt_status == 'suspended' and expectedResult in result:
                             print("\nCobalt suspended Successfully\n")
                             tdkTestObj.setResultStatus("SUCCESS")                   
                             cobal_launch_status = launch_cobalt(obj)
                             time.sleep(5)
                             if cobal_launch_status  == expectedResult:
                                 print("\nCobalt Launched Successfully\n")
                                 print("\n Set the URL : {} using Cobalt deeplink method \n".format(cobalt_test_url))
                                 tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                 tdkTestObj.addParameter("method","Cobalt.1.deeplink")
                                 tdkTestObj.addParameter("value",cobalt_test_url)
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
                                   video_start_time = str(datetime.now()).split()[1]
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
                                            pause_start_time = str(datetime.now()).split()[1]
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
                                                      play_start_time = str(datetime.now()).split()[1]
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
                      print("\nFailed to restore Cobalt from  hibernated state .")   
            else:
                print("\n Cobalt in not in  Hibernated state.")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("\n Failed to Hiberante the cobalt app")
            tdkTestObj.setResultStatus("FAILURE")    
        print("\n Exit from Cobalt \n")
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
        print("Pre conditions are not met")
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print("Revert the values before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict)
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")
