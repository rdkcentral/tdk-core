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
  <name>RDKV_CERT_PACS_Cobalt_Hibernate_memory_usage_4K_Video_PlayPause</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getSSHParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test validates the memory usage before and after cobalt is hibernated during 4k video playback</synopsis>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_150</test_case_id>
    <test_objective>The objective of the test is to validate the memory usage before and after cobalt is hibernated during 4k video playback</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite>Wpeframework process should be up and running in the device</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>4k test url</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell
2. Set a 4K video URL using deeplink method.
3. Save current system time and Start playing by generateKey method
4. Using Proc validation and check video started playing
5. Calculate the memory usage
6. Suspend the cobalt app and check it is in hibernated state
7. Now validate the memory usage is decreased by 1/10th of memory utilized when it was in resumed state
8. Restore the cobalt app and validate the video playback is resumed using wpeframework logs
9. Deactivate the Cobalt plugin.</automation_approch>
    <expected_output>memory usage should be less that 1/10 th of memory utilized when cobalt is in resumed state
 and play back should be resumed after restore</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_Hibernate_memory_usage_4K_Video_PlayPause</test_script>
    <skipped>No</skipped>
    <release_version>M130</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import PerformanceTestVariables
from StabilityTestUtility import *
from datetime import datetime
from rdkv_performancelib import *
from rdkvmemcrlib import*
import ast
import re
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_Hibernate_memory_usage_4K_Video_PlayPause');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
#Execution summary variable 
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print ("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print ("Check Pre conditions")
    status = "SUCCESS"
    revert = "NO"
    cobalt_test_url = PerformanceTestVariables.video4K_test_url
    print ("cobalt_test_url:",cobalt_test_url)
    if cobalt_test_url == "":
        print ("\n Please configure the video4K_test_url value\n")
    plugins_list = ["Cobalt","WebKitBrowser"]
    browser_test_url = PerformanceTestVariables.browser_test_url
    if browser_test_url == "":
        print ("\n Please configure the browser_test_url value\n")
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        if plugin_status_needed.get("Cobalt") == "hibernated":
           restore_plugin(obj,"Cobalt")
           time.sleep(5)
        status = set_plugins_status(obj,plugin_status_needed)
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            status = "FAILURE"
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if status == "SUCCESS" and expectedResult in result and ssh_param_dict != {} and cobalt_test_url != "":
        tdkTestObj.setResultStatus("SUCCESS")
        cobal_launch_status = launch_cobalt(obj)
        print ("\nPre conditions for the test are set successfully")
        time.sleep(30)
        if cobal_launch_status == "SUCCESS":
            print ("\n Set the URL : {} using Cobalt deeplink method \n".format(cobalt_test_url))
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","Cobalt.1.deeplink")
            tdkTestObj.addParameter("value",cobalt_test_url)
            tdkTestObj.executeTestCase(expectedResult)
            cobalt_result = tdkTestObj.getResult()
            time.sleep(20)
            if(cobalt_result == expectedResult):
                tdkTestObj.setResultStatus("SUCCESS")
                print ("Clicking OK to play video")
                params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                video_start_time = str(datetime.utcnow()).split()[1]
                tdkTestObj.executeTestCase(expectedResult)
                result1 = tdkTestObj.getResult()
                time.sleep(40)
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result2 = tdkTestObj.getResult()
                time.sleep(50)
                if "SUCCESS" == (result1 and result2):
                    tdkTestObj.setResultStatus("SUCCESS")
                    print ("\n Check video is started \n")
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
                            print ("\n Video started Playing\n")
                            tdkTestObj.setResultStatus("SUCCESS")
                            time.sleep(10)
                            tdkTestObj = obj.createTestStep('memcr_getProcessID')
                            tdkTestObj.addParameter("appname","CobaltImplementation")
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResultDetails()
                            result = ast.literal_eval(result)
                            result = list(result)
                            processID = result[1].strip()
                            if "SUCCESS" in result:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print("SUCCESS : ProceesID retrieval successful\n")
                                tdkTestObj = obj.createTestStep('memcr_appMemorySize')
                                tdkTestObj.addParameter("processID",processID)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResultDetails()
                                result = ast.literal_eval(result)
                                result = list(result)
                                BeforeHibernate_appusage = result[1].strip()
                                if "SUCCESS" in result:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print("SUCCESS : Memory usage of the app was successfully retrieved before hibernate state\n")
                                    time.sleep(10)
                                    print("\n Set the cobalt in Hibernate state by suspending it.")
                                    print("\nSuspend the Cobalt plugin :\n")
                                    launch_status,launch_start_time = launch_plugin(obj,"WebKitBrowser",browser_test_url)
                                    time.sleep(10)
                                    if launch_status == expectedResult:
                                       tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                       tdkTestObj.addParameter("plugin","WebKitBrowser")
                                       tdkTestObj.executeTestCase(expectedResult)
                                       webkit_status = tdkTestObj.getResultDetails()
                                       result = tdkTestObj.getResult()
                                       if webkit_status == 'resumed' and expectedResult in result:
                                          print("\n WebKitBrowser resumed successfully")
                                          time.sleep(10)
                                          print("\n Checking Cobalt current state")
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
                                             tdkTestObj = obj.createTestStep('memcr_appMemorySize')
                                             tdkTestObj.addParameter("processID",processID)
                                             tdkTestObj.executeTestCase(expectedResult)
                                             result = tdkTestObj.getResultDetails()
                                             result = ast.literal_eval(result)
                                             result = list(result)
                                             AfterHibernate_appusage = result[1].strip()
                                             if "SUCCESS" in result:
                                                 tdkTestObj.setResultStatus("SUCCESS")
                                                 print("SUCCESS : Memory usage of the app was successfully retrieved after hibernated state")
                                                 AfterHibernate_value = getNumericValue(AfterHibernate_appusage)
                                                 BeforeHibernate_value = getNumericValue(BeforeHibernate_appusage)
                                                 onebytenth_value = float(BeforeHibernate_value)/10
                                                 print(f"1/10th value of {BeforeHibernate_appusage} is {onebytenth_value}")
                                                 validation =True
                                                 if float(AfterHibernate_value) <= onebytenth_value:
                                                     tdkTestObj.setResultStatus("SUCCESS")
                                                     print("SUCCESS : After hibernating the app, its memory consumption decreased to "+AfterHibernate_appusage+" down from 1/10th of "+BeforeHibernate_appusage+" before suspension\n")
                                                 else:
                                                    validation =False
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    print("FAILURE : After hibernating the app, its memory consumption decreased to "+AfterHibernate_appusage+" up from 1/10th of "+BeforeHibernate_appusage+" before suspension\n")
                                                 restore_status,start_restore =restore_plugin(obj,"Cobalt")
                                                 if restore_status == expectedResult:
                                                      print("\n Cobalt app restored successfully and trying to launch it")
                                                      resume_status,start_resume = launch_plugin(obj,"Cobalt")
                                                      time.sleep(5)
                                                      if resume_status == expectedResult:
                                                           print("\n Cobalt app resumed successfully")
                                                           time.sleep(30)
                                                           print ("\n Check video is resumed \n")
                                                           command = 'cat /opt/logs/wpeframework.log | grep -inr State.*changed.*old.*PAUSED.*new.*PLAYING | tail -1'
                                                           tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                                           tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                                                           tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                                                           tdkTestObj.addParameter("command",command)
                                                           tdkTestObj.executeTestCase(expectedResult)
                                                           result = tdkTestObj.getResult()
                                                           output = tdkTestObj.getResultDetails()
                                                           if output != "EXCEPTION" and expectedResult in result and "old: PAUSED" in output:
                                                              video_resumed_log = output.split('\n')[1]
                                                              video_play_starttime_in_millisec = getTimeInMilliSec(video_start_time)
                                                              video_played_time = getTimeStampFromString(video_resumed_log)
                                                              video_played_time_in_millisec = getTimeInMilliSec(video_played_time)
                                                              if video_played_time_in_millisec > video_play_starttime_in_millisec:
                                                                 print ("\n Video resumed Playing\n")
                                                                 tdkTestObj.setResultStatus("SUCCESS")
                                                              else:
                                                                 print ("\n Video has not resumed after cobalt restore. \n")
                                                                 tdkTestObj.setResultStatus("FAILURE")
                                                           else:
                                                               print ("\n Video play related logs are not available after resume \n")
                                                               tdkTestObj.setResultStatus("FAILURE")
                                                      else:
                                                          print("\n Failed to resume cobalt application")
                                                          tdkTestObj.setResultStatus("FAILURE")

                                                 else:
                                                     print("\n Failed to restore cobalt application")
                                                     tdkTestObj.setResultStatus("FAILURE")

                                             else:
                                                 tdkTestObj.setResultStatus("FAILURE")
                                                 print("FAILURE ; Failed to retrieve memory usage of the app after hibernated state\n")
                                          else:
                                              print("Cobalt is not in Hibernate state\n")
                                              tdkTestObj.setResultStatus("FAILURE")                            
                                              obj.unloadModule("rdkv_performance");
                                       else:
                                           print("webkit browser is not in resumed state.\n")
                                           tdkTestObj.setResultStatus("FAILURE")                             
                                    else:
                                        print("Failed to launch webkitbrowser\n")
                                        tdkTestObj.setResultStatus("FAILURE")

                            else:
                               print("Failed retrieve to ProceesID\n")
                               tdkTestObj.setResultStatus("FAILURE")                                                       
                        else:
                            print ("\n Video  not started playing \n")
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print ("\n Video play related logs are not available \n")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print ("\n Error while executing generateKey method \n")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print ("\n Error while executing deeplink method \n")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print ("\n Error while launching Cobalt \n")
            tdkTestObj.setResultStatus("FAILURE")
        print ("\n Exiting from Cobalt \n")
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin","Cobalt")
        tdkTestObj.addParameter("status","deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print ("Unable to deactivate Cobalt")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print ("\n Preconditions are not met \n")
        tdkTestObj.setResultStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print ("Revert the values before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
    print("#################################TEST SUMMARY######################################\n")   
    if validation ==True:
        print("SUCCESS : After Hibernating the app, its memory consumption decreased to "+AfterHibernate_appusage+" down from 1/10th of "+BeforeHibernate_appusage+" before hibernating\n")
    else:
        print(f"FAILURE: After hibernating the app, its memory consumption decreased  to {AfterHibernate_appusage} kb from {BeforeHibernate_appusage} kb before hibernating but it is not under threshold limit.\n")
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print ("Failed to load module")
