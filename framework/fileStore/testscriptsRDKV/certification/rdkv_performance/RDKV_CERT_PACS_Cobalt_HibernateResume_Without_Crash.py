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
  <name>RDKV_CERT_PACS_Cobalt_HibernateResume_Without_Crash</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getSSHParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test validates if any crash is observed during the hibernate and restore process of cobalt application</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_152</test_case_id>
    <test_objective>The objective of this test is to validate if any crash is observed during the hibernate and restore process of cobalt application</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Launch the cobalt application using Rdkshell
2.Now suspend the application 
3. Verify any crash is observed during Hibernated state
4.Now restore the application and check for any crash
5. Now resume the application and check for any crash</automation_approch>
    <expected_output>No crash must be observed during the execution process</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_HibernateResume_Without_Crash</test_script>
    <skipped>No</skipped>
    <release_version>M130</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import rdkv_performancelib
from rdkv_performancelib import *
from datetime import datetime
from StabilityTestUtility import *
from web_socket_util import *
import PerformanceTestVariables
import json

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_HibernateResume_Without_Crash');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Execution summary variable
Summ_list=[]

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print("Check Pre conditions")
    event_listener = None
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    crash_Validation = False
    plugins_list = ["Cobalt"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"Cobalt":"resumed"}
    print("curr_plugins_status_dict:",curr_plugins_status_dict)
    if curr_plugins_status_dict != plugin_status_needed:
        if plugin_status_needed.get("Cobalt") == "hibernated":
           restore_plugin(obj,"Cobalt")
        revert = "YES"
        time.sleep(5)
        status = set_plugins_status(obj,plugin_status_needed)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict != plugin_status_needed:
            status = "FAILURE"
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if status == "SUCCESS"  and ssh_param_dict != {} :           
        time.sleep(30)
        print("\nPre conditions for the test are set successfully")
        hibernated_time = restored_time = ""
        suspend_status,start_suspend = suspend_plugin(obj,"Cobalt")
        if suspend_status == expectedResult:
            time.sleep(10)
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","Cobalt")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            cobalt_status = tdkTestObj.getResultDetails()
            print("Checking for any crash during cobalt suspend\n")
            command = 'cat /opt/logs/wpeframework.log | grep -inr crash'
            print("COMMAND : %s" %(command))            
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
            if ("crash" or "CRASH" or "Crash") in output:
                print("Crash observed during cobalt suspend\n")
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
                    print("Crash is observed during cobalt suspend and plugin is deactivated")
                    tdkTestObj.setResultStatus("FAILURE")
                    crash_Validation = True
                    obj.unloadModule("rdkv_performance");
                    
            else:
                 print("No crash observed during cobalt suspend")
                 tdkTestObj.setResultStatus("SUCCESS")
            if cobalt_status == 'hibernated' and expectedResult in result and crash_Validation ==False:
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(5)
                print("\nCobalt hibernated Successfully and trying to restore the app\n")
                restore_status,start_restore =restore_plugin(obj,"Cobalt")
                print("Checking for any crash while restoring the cobalt app\n")
                command = 'cat /opt/logs/wpeframework.log | grep -inr crash'
                print("COMMAND : %s" %(command))            
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
                if ("crash" or "CRASH" or "Crash") in output:
                    print("Crash observed during cobalt restore")
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
                        print("Crash is observed during cobalt restore and plugin is deactivated")
                        tdkTestObj.setResultStatus("FAILURE")
                        crash_Validation = True
                        obj.unloadModule("rdkv_performance");                        
                else:
                    print("No crash observed during cobalt restore")
                    tdkTestObj.setResultStatus("SUCCESS")
                if restore_status == expectedResult and crash_Validation ==False :
                   tdkTestObj.setResultStatus("SUCCESS")
                   time.sleep(10)
                   tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                   tdkTestObj.addParameter("plugin","Cobalt")
                   tdkTestObj.executeTestCase(expectedResult)
                   result = tdkTestObj.getResult()
                   cobalt_status = tdkTestObj.getResultDetails()
                   if cobalt_status == 'suspended' and expectedResult in result:
                      print("\nCobalt suspended Successfully\n")
                      tdkTestObj.setResultStatus("SUCCESS")
                      resume_status,start_resume = launch_plugin(obj,"Cobalt")
                      print("Checking for any crash while resuming the cobalt app\n")
                      command = 'cat /opt/logs/wpeframework.log | grep -inr crash'
                      print("COMMAND : %s" %(command))            
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
                      if ("crash" or "CRASH" or "Crash") in output:
                         print("Crash observed during cobalt resume")
                         print("\n Validate the status of cobalt plugin to confirm the crash:\n")
                         tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                         tdkTestObj.addParameter("plugin","Cobalt")
                         #Execute the test case in DUT                         
                         tdkTestObj.executeTestCase(expectedResult);
                         output = tdkTestObj.getResultDetails()
                         if output != 'deactivated':
                            print("Crash is not observed and plugin is still active")
                            tdkTestObj.setResultStatus("SUCCESS")
                         else:
                             print("Crash is observed during cobalt resume and plugin is deactivated")
                             tdkTestObj.setResultStatus("FAILURE")
                             crash_Validation = True
                             obj.unloadModule("rdkv_performance");
                             
                      else:
                          print("No crash observed during cobalt resume")
                          tdkTestObj.setResultStatus("SUCCESS")
                      if resume_status == expectedResult and crash_Validation ==False:
                         time.sleep(10)
                         tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                         tdkTestObj.addParameter("plugin","Cobalt")
                         tdkTestObj.executeTestCase(expectedResult)
                         cobalt_status = tdkTestObj.getResultDetails()
                         result = tdkTestObj.getResult()
                         if cobalt_status == 'resumed' and expectedResult in result:
                            print("\nCobalt resumed Successfully\n")
                            tdkTestObj.setResultStatus("SUCCESS")
                            time.sleep(30)                            
                           
                         else:
                            print("\n Cobalt is not in resumed state, current cobalt Status: ",cobalt_status)
                            tdkTestObj.setResultStatus("FAILURE")
                      else:
                         print("\n Unable to set cobalt plugin to resumed state \n")
                         tdkTestObj.setResultStatus("FAILURE")
                   else:
                      print("\n Cobalt is not in suspended state, current cobalt Status: ",cobalt_status)
                      tdkTestObj.setResultStatus("FAILURE")
                else:
                   print("\n Unable to restore cobalt plugin ")
                   obj.setLoadModuleStatus("FAILURE")
        
            else:
                print("\n Unable to set cobalt plugin to hibernate state")
                obj.setLoadModuleStatus("FAILURE")
            time.sleep(30)
    else:
        print("\n Pre conditions are not met \n")
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print("Revert the values before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");    
    print("################TEST SUMMARY################\n")
    if crash_Validation == False:
        print("No crash is observed during the execution\n")
    else:
        print("Crash observed during execution\n")

else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")
