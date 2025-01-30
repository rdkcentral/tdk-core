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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PACS_Cobalt_HibernateRestore_Load_lnvalidURL</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The test validates if any crash is observed when cobalt is resumed from hibernated state with invalid url.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_153</test_case_id>
    <test_objective>The test validates if any crash is observed when cobalt is resumed from hibernated state with invalid url.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Launch cobalt
2.Hibernate cobalt app
3.Restore the cobalt app
4.Resume the cobalt app using deep link method with an invalid url
5.check for any crash</automation_approch>
    <expected_output>No crash should be observed during execution</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_HibernateRestore_Load_lnvalidURL</test_script>
    <skipped>No</skipped>
    <release_version>M130</release_version>
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
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_HibernateRestore_Load_lnvalidURL');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    cobalt_test_invalid_url = PerformanceTestVariables.cobalt_test_invalid_url;
    print("Check Pre conditions")
    if cobalt_test_invalid_url == "":
        print("\n Please configure the cobalt_test_invalid_url value\n")
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt"]
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated"}
    conf_file, status = get_configfile_name(obj);
    status,supported_plugins = getDeviceConfigValue(conf_file,"SUPPORTED_PLUGINS")
    for plugin in plugins_list[:]:
        if plugin not in supported_plugins:
            plugins_list.remove(plugin)
            plugin_status_needed.pop(plugin)
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    if curr_plugins_status_dict != plugin_status_needed:
        if curr_plugins_status_dict.get("Cobalt") == "hibernated":
           restore_plugin(obj,"Cobalt")
           time.sleep(5)
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
    cobal_launch_status = launch_cobalt(obj)
    validation_dict = get_validation_params(obj)
    if status == "SUCCESS" and cobal_launch_status == "SUCCESS" and validation_dict != {} and cobalt_test_invalid_url != "":
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
                      cobal_launch_status = launch_cobalt(obj)
                      time.sleep(5)
                      tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                      tdkTestObj.addParameter("realpath",obj.realpath)
                      tdkTestObj.addParameter("deviceIP",obj.IP)
                      tdkTestObj.executeTestCase(expectedResult)
                      result = tdkTestObj.getResult()
                      ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                      if cobal_launch_status  == expectedResult and ssh_param_dict != {} and cobalt_test_invalid_url != "":
                          print("\nCobalt launched successfully\n")              
                          print("\n Set the URL : {} using Cobalt deeplink method \n".format(cobalt_test_invalid_url))
                          tdkTestObj = obj.createTestStep('rdkservice_setValue')
                          tdkTestObj.addParameter("method","Cobalt.1.deeplink")
                          tdkTestObj.addParameter("value",cobalt_test_invalid_url)
                          tdkTestObj.executeTestCase(expectedResult)
                          cobalt_result = tdkTestObj.getResult()
                          output = tdkTestObj.getResultDetails()
                          print("output:",output)
                          time.sleep(10)
                          if(cobalt_result == expectedResult):
                              tdkTestObj.setResultStatus("SUCCESS")
                              command = 'cat /opt/logs/wpeframework.log | grep -inr crash'
                              print("COMMAND : %s" %(command))
                              #Primitive test case which associated to this Script
                              tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog');
                              #Add the parameters to ssh to the DUT and execute the command
                              tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                              tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                              tdkTestObj.addParameter("command",command)
                              #Execute the test case in DUT
                              tdkTestObj.executeTestCase(expectedResult);
                              output = tdkTestObj.getResultDetails()
                              output = tdkTestObj.getResultDetails().replace(r'\n', '\n');
                              output = output[output.find('\n')]
                              time.sleep(10)
                              if ("crash" or "CRASH" or "Crash") in output:
                                  print("Crash observed")
                                  print("\n Validate the status of Cobalt plugin to confirm the crash:\n")
                                  tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                  tdkTestObj.addParameter("plugin","Cobalt")
                                  #Execute the test case in DUT
                                  tdkTestObj.executeTestCase(expectedResult);
                                  output = tdkTestObj.getResultDetails()
                                  if output != 'deactivated':
                                     print("Crash is not observed and plugin is still active")
                                     tdkTestObj.setResultStatus("SUCCESS")
                                  else:
                                     print("Crash is observed and plugin is deactivated")
                                     tdkTestObj.setResultStatus("FAILURE")
                              else:
                                 print("No crash Observed")
                                 tdkTestObj.setResultStatus("SUCCESS")                                   
                          else:
                             print("Unable to load the cobalt_test_invalid_url")
                             tdkTestObj.setResultStatus("FAILURE")
                      else:
                         print("\n Failed to launch cobalt  ")
                         tdkTestObj.setResultStatus("FAILURE")
                   else:
                       print("\n Failed to Suspend cobalt App") 
                       tdkTestObj.setResultStatus("FAILURE")     
                else:
                    print("\n Failed to restore cobalt from hibernated state")
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
