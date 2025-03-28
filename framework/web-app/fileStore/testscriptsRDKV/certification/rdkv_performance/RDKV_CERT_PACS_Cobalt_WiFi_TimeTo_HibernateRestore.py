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
  <name>RDKV_CERT_PACS_Cobalt_WiFi_TimeTo_HibernateRestore</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate the time taken to Hibernate and restore Cobalt after connecting to Wifi.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_147</test_case_id>
    <test_objective>The objective of this test is to validate time taken to Hibernate and restore Cobalt after connecting to WiFi</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Either the DUT should be already connected and configured with WiFi IP in test manager or WiFi Access point with same IP range is required.
2. Lightning application should be already hosted.
3. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Check the current active interface of DUT and if it is already WIFI then follow steps 3 to 9
2. a) If current active interface is ETHERNET, enable the WIFI interface.
b) Connect to SSID
c) Launch Lightning app for detecting IP change in WebKitBrowser
d) Set WIFI as default interface.
e) Suspend Cobalt  and Check whether it goes in to Hibernate state
3. Restore Cobalt and check whether it enters suspend state
4. Revert all values and default interface</automation_approch>
    <expected_output>Interface should be set as WiFi if it was ETHERNET.
Cobalt should be Hibernated and restored with in Threshold limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_WiFi_TimeTo_HibernateRestore</test_script>
    <skipped>No</skipped>
    <release_version>M129</release_version>
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
from ip_change_detection_utility import *
from web_socket_util import *
import PerformanceTestVariables
import json

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_WiFi_TimeTo_HibernateRestore');

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
    revert_plugins_dict = {}
    revert_if  = revert_device_info = revert_plugins = "NO"
    #Check current interface
    current_interface,revert_nw = check_current_interface(obj)
    if revert_nw == "YES":
        revert_plugins_dict = {"org.rdk.NetworkManager":"deactivated"}
    if current_interface == "EMPTY":
        status = "FAILURE"
    elif current_interface == "eth0":
        revert_if = "YES"
        wifi_connect_status,plugins_status_dict,revert_plugins,deviceAvailability = switch_to_wifi(obj)
        if revert_plugins == "YES":
            revert_plugins_dict.update(plugins_status_dict)
        if wifi_connect_status == "FAILURE":
            status = "FAILURE"
    else:
        print("\n Current interface is WIFI \n")
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
                      print("\nCobalt suspended successfully\n")
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
                            print("\nCobalt resumed successfully\n")
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
                                       print("\n Time taken to Hibernate Cobalt Plugin: " + str(time_taken_for_hibernate) + "(ms)")
                                       Summ_list.append('Time taken to Hibernate Cobalt Plugin :{}ms'.format(time_taken_for_hibernate))
                                       print("\n Threshold value for time taken to Hibernate Cobalt plugin: " + str(hibernate_threshold) + "(ms)")
                                       print("\n Validate the time taken for Hibernating the plugin \n")
                                       if 0 < time_taken_for_hibernate < (int(hibernate_threshold) + int(offset)) :
                                           print("\n Time taken for Hibernating Cobalt plugin is within the expected range \n")
                                           tdkTestObj.setResultStatus("SUCCESS")
                                       else:
                                           print("\n Time taken for Hibernating Cobalt plugin not within the expected range \n")
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
                            print("\n Cobalt is not in resumed state, current Cobalt Status: ",cobalt_status)
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
                print("\n Cobalt is not in hibernated state, current Cobalt Status: ",cobalt_status)
                tdkTestObj.setResultStatus("FAILURE")
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
