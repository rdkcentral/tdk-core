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
  <version>9</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PACS_Cobalt_ResourceUsage_Hibernate_State</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to put Cobalt in hibernated state and get memory usage</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_146</test_case_id>
    <test_objective>The objective of this test is to place Cobalt in Hibernated state  and get CPU load and memory usage</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>Wpeframework process should be up and running in the device</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell.
2.  Change Cobalt state to Hibernated state by launching Webkit browser
3. Validate memory usage before and after the the cobalt is hibernated 
4. Revert the plugin status</automation_approch>
    <expected_output>CPU load and memory usage should be within the expected range</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_ResourceUsage_Hibernate_State</test_script>
    <skipped>No</skipped>
    <release_version>M129</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import json
from StabilityTestUtility import *
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
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_ResourceUsage_Hibernate_State');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
AfterHibernate_appusage =None
if expectedResult in result.upper() :
    status = "SUCCESS"
    plugins_list = ["Cobalt","WebKitBrowser","DeviceInfo"]
    browser_test_url = PerformanceTestVariables.browser_test_url
    print("\n Check Pre conditions")
    revert ="NO"
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated","DeviceInfo":"activated"}
    conf_file, status = get_configfile_name(obj);
    status,supported_plugins = getDeviceConfigValue(conf_file,"SUPPORTED_PLUGINS")
    for plugin in plugins_list[:]:
        if plugin not in supported_plugins:
            plugins_list.remove(plugin)
            plugin_status_needed.pop(plugin)
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
       revert = "YES"
       if curr_plugins_status_dict.get("Cobalt") == "hibernated":
          restore_plugin(obj,"Cobalt")
       status = set_plugins_status(obj,plugin_status_needed)
       time.sleep(10)
       plugins_status_dict = get_plugins_status(obj,plugins_list)
       if plugins_status_dict != plugin_status_needed:
          status = "FAILURE"
    if status == "SUCCESS" :
        print("\nPre conditions for the test are set successfully")
        cobal_launch_status = launch_cobalt(obj)
        time.sleep(10)
        if cobal_launch_status == "SUCCESS":
             print("\n Cobalt is launched \n ")             
             tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
             tdkTestObj.addParameter("plugin","Cobalt")
             tdkTestObj.executeTestCase(expectedResult)
             result = tdkTestObj.getResult()
             cobalt_status = tdkTestObj.getResultDetails()
             if cobalt_status == 'resumed' and expectedResult in result:
                     tdkTestObj.setResultStatus("SUCCESS")
                     time.sleep(5)
                     print("\nCobalt is in resumed state")
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
                             print("SUCCESS : Memory usage of the app was successfully retrieved before hibernated state\n")
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
                                   print("\n Checking Cobalt current state")
                                   time.sleep(10)
                                   tdkTestObj.setResultStatus("SUCCESS")
                                   tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                   tdkTestObj.addParameter("plugin","Cobalt")
                                   tdkTestObj.executeTestCase(expectedResult)
                                   result = tdkTestObj.getResult()
                                   cobalt_status = tdkTestObj.getResultDetails()
                                   time.sleep(10)
                                   if cobalt_status == 'hibernated' and expectedResult in result:
                                      tdkTestObj.setResultStatus("SUCCESS")
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
                                             print(f"SUCCESS: After hibernating the app, its memory consumption decreased to {AfterHibernate_appusage} kb from {BeforeHibernate_appusage} kb before hibernating.\n")
                                          else:
                                              tdkTestObj.setResultStatus("FAILURE")
                                              validation =False
                                              print(f"FAILURE: After hibernating the app, its memory consumption decreased  to {AfterHibernate_appusage} kb from {BeforeHibernate_appusage} kb before hibernating ,but it is not under threshold limit.\n")
                                          restore_status,start_restore =restore_plugin(obj,"Cobalt")
                                          if restore_status == expectedResult:
                                             print("\n Cobalt app restored successfully and trying to launch it")
                                             resume_status,start_resume = launch_plugin(obj,"Cobalt")
                                             if resume_status == expectedResult:
                                                print("\n Cobalt app resumed successfully")
                                                tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                                tdkTestObj.addParameter("plugin","WebKitBrowser")
                                                tdkTestObj.executeTestCase(expectedResult)
                                                result = tdkTestObj.getResult()
                                                webkit_status = tdkTestObj.getResultDetails()
                                                print("Webkitbrowser current state is :",webkit_status)
                                             else:
                                                print("\n Failed to resume cobalt application")
                                          else:
                                              print("\n Failed to restore cobalt application")
                                      else:
                                          tdkTestObj.setResultStatus("FAILURE")
                                          print("FAILURE ; Failed to retrieve memory usage of the app after hibernated state\n")
                              
                                   else:
                                       print("Cobalt is not in hibernated state")
                                       tdkTestObj.setResultStatus("FAILURE")                            
                                       obj.unloadModule("rdkv_performance");
                                else:
                                   print("\nWebkitbrowser is not in resumed state")
                                   tdkTestObj.setResultStatus("FAILURE")                            
                             else:
                                 print(" Failed to launch webkit browser")
                                 tdkTestObj.setResultStatus("FAILURE")
                         else:
                             tdkTestObj.setResultStatus("FAILURE")
                             print("FAILURE ; Failed to retrieve memory usage of the app before hibernated state\n")
                           
             else:
                print("Cobalt is not in resumed state")
                tdkTestObj.setResultStatus("FAILURE")
        else:
           print("Failed to Launch cobalt app")
           tdkTestObj.setResultStatus("FAILURE")
    else:
       print("Failed to set Preconditions")
       tdkTestObj.setResultStatus("FAILURE")
    if revert=="YES":
        print("\n Revert the values before exiting \n")
        status = set_plugins_status(obj,curr_plugins_status_dict)
    print("\n Execution Summary")
    if validation ==True:
        print("\n**************************************************")
        print(f"SUCCESS: After hibernating the app, its memory consumption decreased to {AfterHibernate_appusage} kb from {BeforeHibernate_appusage} kb before hibernating.\n")
    else:
        print(f"FAILURE: After hibernating the app, its memory consumption decreased  to {AfterHibernate_appusage} kb from {BeforeHibernate_appusage} kb before hibernating but it is not under threshold limit.\n")
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")
