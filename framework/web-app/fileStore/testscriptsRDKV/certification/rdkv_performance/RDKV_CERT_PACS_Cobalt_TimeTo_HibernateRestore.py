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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>4</version>
  <name>RDKV_CERT_PACS_Cobalt_TimeTo_HibernateRestore</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to hibernate and restore cobalt.</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_148</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to hibernate and restore cobalt.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
2. Time in Test Manager and DUT should be in sync with UTC</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.COBALT_HIBERNATE_TIME_THRESHOLD_VALUE 
2.COBALT_RESTORE_TIME_THRESHOLD_VALUE</input_parameters>
    <automation_approch>1.Launch Cobalt using RDKShell
2.Save current system time and suspend the cobalt
3.check cobalt state and and get time from Hibernate event
4.Save current system time and restore the cobalt and parse time from restore event</automation_approch>
    <expected_output>The time taken to Hibernate and restore must be within the expected limits</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_TimeTo_HibernateRestore</test_script>
    <skipped>No</skipped>
    <release_version>M129</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
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
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_TimeTo_HibernateRestore');

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
    plugins_list = ["Cobalt"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    plugin_status_needed = {"Cobalt":"resumed"}
    print("curr_plugins_status_dict:",curr_plugins_status_dict)
    if curr_plugins_status_dict != plugin_status_needed:
        if curr_plugins_status_dict.get("Cobalt") == "hibernated":
           restore_plugin(obj,"Cobalt")
        revert = "YES"
        time.sleep(5)
        status = set_plugins_status(obj,plugin_status_needed)
        plugins_status_dict = get_plugins_status(obj,plugins_list)
        if plugins_status_dict != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        time.sleep(10)
        thunder_port = rdkv_performancelib.devicePort
        event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 7,"method": "org.rdk.RDKShell.1.register","params": {"event": "onHibernated", "id": "client.events.1" }}','{"jsonrpc": "2.0","id": 8,"method": "org.rdk.RDKShell.1.register","params": {"event": "onRestored", "id": "client.events.1" }}'],"/jsonrpc",False)
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
                      print("\nCobalt suspended Successfully\n")
                      tdkTestObj.setResultStatus("SUCCESS")
                      resume_status,start_resume = launch_plugin(obj,"Cobalt")
                      if resume_status == expectedResult:
                         time.sleep(10)
                         tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                         tdkTestObj.addParameter("plugin","Cobalt")
                         tdkTestObj.executeTestCase(expectedResult)
                         cobalt_status = tdkTestObj.getResultDetails()
                         result = tdkTestObj.getResult()
                         if cobalt_status == 'resumed' and expectedResult in result:
                            print("\nCobalt restored successfully\n")
                            tdkTestObj.setResultStatus("SUCCESS")
                            time.sleep(30)
                            if (len(event_listener.getEventsBuffer())!= 0):
                               for event_log in event_listener.getEventsBuffer():
                                   json_msg = json.loads(event_log.split('$$$')[1])
                                   if json_msg["params"]["success"] is True:
                                       if "onHibernated" in json_msg["method"] and not hibernated_time:
                                           hibernated_time = event_log.split('$$$')[0]
                                           print("hibernated_time",hibernated_time)
                                       elif "onRestored" in json_msg["method"] and not restored_time:
                                          restored_time = event_log.split('$$$')[0]
                               if hibernated_time and restored_time:
                                   conf_file,file_status = getConfigFileName(obj.realpath)
                                   hibernate_config_status,hibernate_threshold = getDeviceConfigKeyValue(conf_file,"COBALT_HIBERNATE_TIME_THRESHOLD_VALUE")
                                   Summ_list.append('COBALT_HIBERNATE_TIME_THRESHOLD_VALUE :{}ms'.format(hibernate_threshold))
                                   restore_config_status,restore_threshold = getDeviceConfigKeyValue(conf_file,"COBALT_RESTORE_TIME_THRESHOLD_VALUE")
                                   Summ_list.append('COBALT_RESTORE_TIME_THRESHOLD_VALUE :{}ms'.format(restore_threshold))
                                   offset_status,offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                   Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                                   if all(value != "" for value in (hibernate_threshold,restore_threshold,offset)):
                                       start_hibernate_in_millisec = getTimeInMilliSec(start_suspend)
                                       hibernated_time_in_millisec = getTimeInMilliSec(hibernated_time)
                                       print("\n hibernate initiated at: " +start_suspend + "(UTC)")
                                       Summ_list.append('hibernate initiated at :{}'.format(start_suspend))
                                       print("\n hibernated at : "+hibernated_time+ "(UTC)")
                                       Summ_list.append('hibernated_time at :{}'.format(hibernated_time))
                                       time_taken_for_hibernate = hibernated_time_in_millisec - start_hibernate_in_millisec
                                       print("\n Time taken to hibernate cobalt plugin: " + str(time_taken_for_hibernate) + "(ms)")
                                       Summ_list.append('Time taken to hibernate cobalt plugin :{}ms'.format(time_taken_for_hibernate))
                                       print("\n Threshold value for time taken to hibernate cobalt plugin: " + str(hibernate_threshold) + "(ms)")
                                       print("\n Validate the time taken for hibernating the plugin \n")
                                       if 0 < time_taken_for_hibernate < (int(hibernate_threshold) + int(offset)) :
                                           print("\n Time taken for hibernating cobalt plugin is within the expected range \n")
                                           tdkTestObj.setResultStatus("SUCCESS")
                                       else:
                                           print("\n Time taken for hibernating cobalt plugin not within the expected range \n")
                                           tdkTestObj.setResultStatus("FAILURE")
                                       start_restore_in_millisec = getTimeInMilliSec(start_restore)
                                       restore_time_in_millisec =  getTimeInMilliSec(restored_time)
                                       print("\n Restore initiated at: " + start_restore + "(UTC)")
                                       Summ_list.append('Restore initiated at :{}'.format(start_restore))
                                       print("\n Restored at: " + restored_time + "(UTC)")
                                       Summ_list.append('Restored at :{}'.format(restored_time))
                                       time_taken_for_restore = restore_time_in_millisec - start_restore_in_millisec
                                       print("\n Time taken to Restore Cobalt Plugin: " + str(time_taken_for_restore) + "(ms)")
                                       Summ_list.append('Time taken to Restore Cobalt Plugin :{}ms'.format(time_taken_for_restore))
                                       print("\n Threshold value for time taken to restore Cobalt plugin: " + str(restore_threshold) + "(ms)")
                                       print("\n Validate the time taken for restoring the plugin \n")
                                       if 0 < time_taken_for_restore < (int(restore_threshold) + int(offset)) :
                                           print("\n Time taken for restoring Cobalt plugin is within the expected range \n")
                                           tdkTestObj.setResultStatus("SUCCESS")
                                       else:
                                           print("\n Time taken for restoring Cobalt plugin is not within the expected range \n")
                                           tdkTestObj.setResultStatus("FAILURE")
                                   else:
                                      print("\n Threshold values are not configured in Device configuration file \n")
                                      tdkTestObj.setResultStatus("FAILURE")
                               else:
                                   print("\n Hibernate and restore related events are not available \n")
                                   tdkTestObj.setResultStatus("FAILURE")
                            else:
                               print("\n State change events are not triggered \n")
                               tdkTestObj.setResultStatus("FAILURE")
                         else:
                            print("\n Cobalt is not in restored state, current Cobalt Status: ",cobalt_status)
                            tdkTestObj.setResultStatus("FAILURE")
                      else:
                         print("\n Unable to set Cobalt plugin to resumed state \n")
                         tdkTestObj.setResultStatus("FAILURE")
                   else:
                      print("\n Cobalt is not in Suspended state, current Cobalt Status: ",cobalt_status)
                      tdkTestObj.setResultStatus("FAILURE")
                else:
                   print("\n Unable to restore Cobalt plugin ")
                   obj.setLoadModuleStatus("FAILURE")
        
            else:
                print("\n Unable to set Cobalt plugin to Hibernate state")
                obj.setLoadModuleStatus("FAILURE")
            event_listener.disconnect()
            time.sleep(30)
    else:
        print("\n Pre conditions are not met \n")
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print("Revert the values before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list,obj)
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")
