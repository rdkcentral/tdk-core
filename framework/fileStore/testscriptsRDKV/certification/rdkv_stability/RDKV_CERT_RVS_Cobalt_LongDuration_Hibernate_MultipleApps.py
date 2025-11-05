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
  <version>20</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_RVS_Cobalt_LongDuration_Hibernate_MultipleApps</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateResourceUsage</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test validates the memory usage of multiple apps by putting them in hibernated state for long duration</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>185</execution_time>
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
    <test_case_id>RDKV_STABILITY_73</test_case_id>
    <test_objective>The objective of this test is to validate the memory usage of multiple apps by putting them in hibernated state for long duration</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>wpeframework should be up and running in the device</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Hibernate test duration
Maximum allowed Memory usage</input_parameters>
    <automation_approch>1. As a prerequisite, disable all the other plugins 
   and enable Cobalt only. and validate memory usage
2. Set the cobalt to hibernated state and calculate memory usage
3. Validate if the cobalt can restore after long hibernated state 
4.Launch YouTube tv. and validate memory usage
5. Set the YouTube tv. to hibernated state and calculate memory usage
6. Validate if the YouTube tv can restore after long hibernated state 
6. Revert all values</automation_approch>
    <expected_output>all apps should be successfully restored after long hibernated state and their memory usage must be in expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Cobalt_LongDuration_Hibernate_MultipleApps</test_script>
    <skipped>No</skipped>
    <release_version>M130</release_version>
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
from rdkvmemcrlib import*
import re
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Cobalt_LongDuration_Hibernate_MultipleApps');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

#the time till which apps will stay in hibernated state
test_interval = 3600

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):    
    print("Check Pre conditions")
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    browser_test_url = PerformanceTestVariables.browser_test_url
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated","DeviceInfo":"activated","YouTubeTV":"deactivated"}
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
    test_time_in_mins = int(StabilityTestVariables.hibernate_test_duration)
    test_time_in_millisec = test_time_in_mins * 60 * 1000
    time_limit = int(round(time.time() * 1000)) + test_time_in_millisec    
    completed = True
    while int(round(time.time() * 1000)) < time_limit:        
        cobal_launch_status = launch_cobalt(obj)    
        if cobal_launch_status == "SUCCESS":
           time.sleep(30)
           print("\nPre conditions for the test are set successfully")           
           tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
           tdkTestObj.addParameter("plugin","Cobalt")
           tdkTestObj.executeTestCase(expectedResult)
           result = tdkTestObj.getResult()
           cobalt_status = tdkTestObj.getResultDetails()
           if cobalt_status == 'resumed' and expectedResult in result:
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
                  Cobalt_BeforeHibernate_appusage = result[1].strip()
                  if "SUCCESS" in result:
                      tdkTestObj.setResultStatus("SUCCESS")
                      print("SUCCESS : Memory usage of the cobalt app was successfully retrieved before hibernated state\n")
                  else:
                       completed = False
                       print("\n Error while validating memory usage")
                       tdkTestObj.setResultStatus("FAILURE")
                       break
           print("\n Set the cobalt in Hibernated state by suspending it.")
           suspend_status,start_suspend = suspend_plugin(obj,"Cobalt")
           time.sleep(10)
           if suspend_status == expectedResult:
                print("Checking current cobalt status\n")
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
                       time.sleep(test_interval)               
                       # Check memory usage 
                       print("\n ##### Validating  memory usage #####\n")                       
                       tdkTestObj = obj.createTestStep('memcr_appMemorySize')
                       tdkTestObj.addParameter("processID",processID)
                       tdkTestObj.executeTestCase(expectedResult)
                       result = tdkTestObj.getResultDetails()
                       result = ast.literal_eval(result)
                       result = list(result)
                       print("result:",result)
                       Cobalt_AfterHibernate_appusage = result[1].strip()
                       if "SUCCESS" in result:
                               tdkTestObj.setResultStatus("SUCCESS")
                               print("SUCCESS : Memory usage of the cobalt app was successfully retrieved when cobalt is in hibernated state\n")
                               time.sleep(10)                                                     
                               AfterHibernate_value = getNumericValue(Cobalt_AfterHibernate_appusage)
                               BeforeHibernate_value = getNumericValue(Cobalt_BeforeHibernate_appusage)                               
                               onebytenth_value = float(BeforeHibernate_value)/10
                               print(f"1/10th value of {Cobalt_BeforeHibernate_appusage} is {onebytenth_value}")
                               validation =True
                               if float(AfterHibernate_value) <= onebytenth_value:
                                  tdkTestObj.setResultStatus("SUCCESS")
                                  print("SUCCESS : After hibernating the app, its memory consumption decreased to "+Cobalt_AfterHibernate_appusage+" down from 1/10th of "+Cobalt_BeforeHibernate_appusage+" before suspension\n")
                               else:
                                   validation =False
                                   tdkTestObj.setResultStatus("FAILURE")
                                   print("FAILURE : After hibernating the app, its memory consumption decreased to "+Cobalt_AfterHibernate_appusage+" up from 1/10th of "+Cobalt_BeforeHibernate_appusage+" before suspension\n")
                print("Restoring cobalt app\n")
                restore_status,start_restore =restore_plugin(obj,"Cobalt")
                if restore_status == expectedResult:
                        print("\n Cobalt app restored successfully and launching youtube tv\n")
                        params = '{"callsign":"YouTubeTV"}'
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","org.rdk.RDKShell.1.launch")
                        tdkTestObj.addParameter("value",params)
                        tdkTestObj.executeTestCase(expectedResult)                               
                        result = tdkTestObj.getResult()
                        if result == expectedResult:
                            tdkTestObj.setResultStatus("SUCCESS")
                            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                            tdkTestObj.addParameter("plugin","YouTubeTV")
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            youtube_tv_status = tdkTestObj.getResultDetails()
                            if youtube_tv_status== 'resumed' and expectedResult in result:
                                print("youtube  TV is in resumed state\n")
                                tdkTestObj = obj.createTestStep('memcr_getProcessID')
                                tdkTestObj.addParameter("appname","YouTubeTV")
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResultDetails()
                                result = ast.literal_eval(result)
                                result = list(result)
                                YT_processID = result[1].strip()
                                if "SUCCESS" in result:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print("SUCCESS : ProceesID retrieval successful\n")
                                    tdkTestObj = obj.createTestStep('memcr_appMemorySize')
                                    tdkTestObj.addParameter("processID",YT_processID)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResultDetails()
                                    result = ast.literal_eval(result)
                                    result = list(result)
                                    YoutubeTV_BeforeHibernate_appusage = result[1].strip()
                                    if "SUCCESS" in result:
                                         tdkTestObj.setResultStatus("SUCCESS")
                                         print("SUCCESS : Memory usage of the  youtube tv app was successfully retrieved before hibernated state\n")
                                    else:
                                        completed = False
                                        print("\n Error while validating memory usage")
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                            print("\n Set the youtube tv in Hibernated state by suspending it.")
                            suspend_status,start_suspend = suspend_plugin(obj,"YouTubeTV")
                            time.sleep(10)
                            if  suspend_status==expectedResult:
                                tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                tdkTestObj.addParameter("plugin","YouTubeTV")
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                youtube_tv_status = tdkTestObj.getResultDetails()
                                if youtube_tv_status== 'hibernated' and expectedResult in result:                               
                                     tdkTestObj.setResultStatus("SUCCESS")
                                     print("Youtube TV is in hibernated state\n")
                                     time.sleep(test_interval)
                                     tdkTestObj = obj.createTestStep('memcr_appMemorySize')
                                     tdkTestObj.addParameter("processID",YT_processID)
                                     tdkTestObj.executeTestCase(expectedResult)
                                     result = tdkTestObj.getResultDetails()
                                     result = ast.literal_eval(result)
                                     result = list(result)
                                     YoutubeTV_AfterHibernate_appusage = result[1].strip()
                                     if "SUCCESS" in result:
                                         tdkTestObj.setResultStatus("SUCCESS")
                                         print("SUCCESS : Memory usage of the  youtube tv app was successfully retrieved before hibernated state\n")
                                     else:
                                         completed = False
                                         print("\n Error while validating memory usage")
                                         tdkTestObj.setResultStatus("FAILURE")
                                         break
                                     AfterHibernate_value = getNumericValue(YoutubeTV_AfterHibernate_appusage)
                                     BeforeHibernate_value = getNumericValue(YoutubeTV_BeforeHibernate_appusage)                                     
                                     onebytenth_value = float(BeforeHibernate_value)/10
                                     print(f"1/10th value of {YoutubeTV_BeforeHibernate_appusage} is {onebytenth_value}")
                                     validation =True
                                     if float(AfterHibernate_value) <= onebytenth_value:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print("SUCCESS : After hibernating the app, its memory consumption decreased to "+YoutubeTV_AfterHibernate_appusage+" down from 1/10th of "+YoutubeTV_BeforeHibernate_appusage+" before suspension\n")
                                     else:
                                        validation =False
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print("FAILURE : After hibernating the app, its memory consumption decreased to "+YoutubeTV_AfterHibernate_appusage+" up from 1/10th of "+YoutubeTV_BeforeHibernate_appusage+" before suspension\n")
    if(completed):
          print("\nsuccessfully completed the test in {} minutes".format(test_time_in_mins))         
          tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
          tdkTestObj.executeTestCase(expectedResult)
          status = tdkTestObj.getResult()
          result = tdkTestObj.getResultDetails()
          #Revert the values
          if revert=="YES":
             print("Revert the values before exiting")
             status = set_plugins_status(obj,curr_plugins_status_dict)
             post_condition_status = check_device_state(obj)
             obj.unloadModule("rdkv_stability");
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")
