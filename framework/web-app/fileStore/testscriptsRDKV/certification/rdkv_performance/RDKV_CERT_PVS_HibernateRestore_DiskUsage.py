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
  <name>RDKV_CERT_PVS_HibernateRestore_DiskUsage</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test validates the disk usage when cobalt is in hibernated state and after cobalt is restored</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_151</test_case_id>
    <test_objective>This test objective is to validate the disk usage of the /dev/root partition when cobalt is in hibernated state and after cobalt is restored</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Put the cobalt in hibernated state
2. Execute the df -h command in DUT and find the output.
3. From the command output strip the disk usage of the required partition and verify whether it is greater than 90%
4. Restore the app from Hibernated state and validate disk usage again</automation_approch>
    <expected_output>Disk usage of the partition must be less than 90%</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_HibernateRestore_DiskUsage</test_script>
    <skipped>No</skipped>
    <release_version>M130</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import json
from rdkv_performancelib import *
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_HibernateRestore_DiskUsage');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    max_mem_limit = 90.0
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
        print("\nPre conditions for the test are set successfully")
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
                print("\nCobalt hibernated successfully and trying to get disk usage")
                #Get the disk usage when cobalt is in hibernated state 
                tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                tdkTestObj.addParameter("realpath",obj.realpath)
                tdkTestObj.addParameter("deviceIP",obj.IP)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                print("\n Get the partition name from Device Config file \n")
                conf_file,result = getConfigFileName(obj.realpath)
                partition_result, partition = getDeviceConfigKeyValue(conf_file,"DISK_PARTITION")
                if ssh_param_dict != {} and expectedResult in result and partition != "" :
                   tdkTestObj.setResultStatus("SUCCESS")
                   #command to get the disk usage  output
                   command = 'df -h | grep "'+ partition +'" | awk' + " '{print $5}'"
                   tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                   tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                   tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                   tdkTestObj.addParameter("command",command)
                   tdkTestObj.executeTestCase(expectedResult)
                   result = tdkTestObj.getResult()
                   output = tdkTestObj.getResultDetails()                   
                   if output != "EXCEPTION" and expectedResult in result:
                      print("Checking DiskUsage of {} \n".format(partition))
                      disk_space_usage_hibernate = float(output.split('\n')[1].replace("%",""))
                      if disk_space_usage_hibernate >= max_mem_limit :
                          print("[Error] {} has higher diskusage  when cobalt is in hibernated state: {}% \n".format(partition,disk_space_usage_hibernate))
                          tdkTestObj.setResultStatus("FAILURE")
                      else:
                         print("{} has diskusage: {}%  when cobalt is in hibernated state \n".format(partition,disk_space_usage_hibernate))
                         tdkTestObj.setResultStatus("SUCCESS")
                         print("Restoring the cobalt from hibernated state")
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
                               #Get the disk usage after cobalt is restored from hibernated state.
                               tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                               tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                               tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                               tdkTestObj.addParameter("command",command)
                               tdkTestObj.executeTestCase(expectedResult)
                               result = tdkTestObj.getResult()
                               output = tdkTestObj.getResultDetails()
                               if output != "EXCEPTION" and expectedResult in result:
                                  print("Checking DiskUsage of {} when cobalt is restored from hibernated state\n".format(partition))
                                  disk_space_usage_restore = float(output.split('\n')[1].replace("%",""))
                                  if disk_space_usage_restore >= max_mem_limit :
                                     print("[Error] {} has higher diskusage when cobalt is restored from hibernated state: {}% \n".format(partition,disk_space_usage_restore))
                                     tdkTestObj.setResultStatus("FAILURE")
                                  else:
                                      print("{} has diskusage: {}% when cobalt is restored from hibernated state\n".format(partition,disk_space_usage_restore))
                                      tdkTestObj.setResultStatus("SUCCESS")
                               else:
                                   print("Error occurred during SSH, please check ssh details in configuration file")
                                   tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print("\n Cobalt is not in suspended state, current Cobalt Status: ",cobalt_status)
                                tdkTestObj.setResultStatus("FAILURE")                        
                         else:
                             print("\n Unable to restore Cobalt plugin ")
                             obj.setLoadModuleStatus("FAILURE")                              
                   else:
                       print("Error occurred during SSH, please check ssh details in configuration file")
                       tdkTestObj.setResultStatus("FAILURE")  
                else:
                    print("Please configure the SSH details in configuration file")
                    obj.setLoadModuleStatus("FAILURE")
                    obj.unloadModule("rdkv_performance");
            else:
                print("\n Unable to set Cobalt plugin to Hibernate state")
                obj.setLoadModuleStatus("FAILURE")        
        else:
           print("\n Cobalt is not in suspended state, current Cobalt Status: ",cobalt_status)
           tdkTestObj.setResultStatus("FAILURE")   
    else:
        print("Failed to execute pre conditions successfully.")
        obj.setLoadModuleStatus("FAILURE")
        obj.unloadModule("rdkv_performance");
    print("\n========================TEST SUMMARY==============================\n")
    print("{} has diskusage: {}%  when cobalt is in hibernated state \n".format(partition,disk_space_usage_hibernate))
    print("{} has diskusage: {}% when cobalt is restored from hibernated state\n".format(partition,disk_space_usage_restore))
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")
