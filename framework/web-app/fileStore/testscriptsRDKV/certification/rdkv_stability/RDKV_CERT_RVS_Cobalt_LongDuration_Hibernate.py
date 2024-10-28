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
    <test_case_id>RDKV_STABILITY_71/test_case_id>
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
    print("Check Pre conditions")
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    status = "SUCCESS"
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"deactivated","DeviceInfo":"activated"}
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
    if status == "SUCCESS" and cobal_launch_status == "SUCCESS":
        time.sleep(30)
        print("\nPre conditions for the test are set successfully")
        print("\n Set the cobalt in Hibernated state by suspending it.")
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
                test_time_in_mins = int(StabilityTestVariables.hibernate_test_duration)
                test_time_in_millisec = test_time_in_mins * 60 * 1000
                time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
                iteration = 0
                completed = True
                while int(round(time.time() * 1000)) < time_limit:
                   # Check Cobalt's state every 15 minutes 
                   if (iteration % 4) == 0: 
                       print("\n Checking Cobalt Hibernated state.")
                       tdkTestObj.setResultStatus("SUCCESS")
                       tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                       tdkTestObj.addParameter("plugin","Cobalt")
                       tdkTestObj.executeTestCase(expectedResult)
                       result = tdkTestObj.getResult()
                       cobalt_status = tdkTestObj.getResultDetails()                                  
                       if cobalt_status != 'hibernated':
                            # If Cobalt is not in hibernated state, stop the test case and break the loop
                            tdkTestObj.setResultStatus("FAILURE")
                            completed = False
                            break
                   iteration += 1
                   # Check resource usage after each iteration
                   print("\n ##### Validating CPU load and memory usage #####\n")
                   print("Iteration : ", iteration)
                   tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
                   tdkTestObj.executeTestCase(expectedResult)
                   status = tdkTestObj.getResult()
                   result = tdkTestObj.getResultDetails()
                   if expectedResult in status and result != "ERROR":
                       tdkTestObj.setResultStatus("SUCCESS")
                       cpuload = result.split(',')[0]
                       memory_usage = result.split(',')[1]
                       result_dict = {}
                       result_dict["iteration"] = iteration
                       result_dict["cpu_load"] = float(cpuload)
                       result_dict["memory_usage"] = float(memory_usage)
                       result_dict_list.append(result_dict)
                   else:
                      completed = False
                      print("\n Error while validating Resource usage")
                      tdkTestObj.setResultStatus("FAILURE")
                      break
                   time.sleep(test_interval)
                if completed:
                   print("Cobalt remained in hibernated state for the configured time")
                   print("\nsuccessfully completed the {} times in {} minutes".format(iteration,test_time_in_mins))
                cpu_mem_info_dict["cpuMemoryDetails"] = result_dict_list
                json.dump(cpu_mem_info_dict,json_file)
                json_file.close()
            else:
                print("\n Cobalt is not in  hibernated state.")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("\n Failed to hibernate the cobalt app")
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
