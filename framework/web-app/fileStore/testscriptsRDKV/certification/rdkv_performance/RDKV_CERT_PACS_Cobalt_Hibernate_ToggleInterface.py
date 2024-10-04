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
  <name>RDKV_CERT_PACS_Cobalt_Hibernate_ToggleInterface</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to keep Cobalt in Hibernated state, toggle the network interface and check whether Cobalt persisted in Hibernated state or not.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>20</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_145</test_case_id>
    <test_objective>The objective of this test is to put Cobalt in Hibernated state, toggle the network interface and check whether Hibernated state is persisting or not.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Either the DUT should be already connected and configured with WIFI IP in test manager or WIFI Access point with same IP range is required.
2. Lightning application for ip change detection should be already hosted.
3. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>ip_change_app_url : string
    tm_username : string
    tm_password : string</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell
2. Put cobalt in Hibernated state and check the state of cobalt
3. Check the current network interface and toggle the interface
4.After toggle is successful, check Hibernated state persisted.
 5.Revert the network interface
 6. Close Cobalt</automation_approch>
    <expected_output>Hibernated state persisted even if interface is toggled.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_Hibernate_ToggleInterface</test_script>
    <skipped>No</skipped>
    <release_version>M129</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
from StabilityTestUtility import *
import PerformanceTestVariables
from ip_change_detection_utility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_Hibernate_ToggleInterface')

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
deviceAvailability = "No"
result =obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print("Check Pre conditions")
    status = "SUCCESS"
    revert = "NO"
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url
    plugins_list = ["Cobalt","WebKitBrowser","org.rdk.Network"]
    inverse_dict = {"ETHERNET":"WIFI","WIFI":"ETHERNET"}
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated","org.rdk.Network":"activated"}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print("\n Error while getting the status of plugins")
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        if curr_plugins_status_dict.get("Cobalt") == "hibernated":
           restore_plugin(obj,"Cobalt")
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            print("\n Unable to set status of plugins")
            status = "FAILURE"   
    current_interface,revert_nw = check_current_interface(obj)
    if current_interface != "EMPTY" and status == "SUCCESS":
        new_interface = inverse_dict[current_interface]
        time.sleep(5)
        cobalt_launch_status = launch_cobalt(obj)
        time.sleep(10)
        if cobalt_launch_status in expectedResult:
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
                   print("\nCobalt hibernated Successfully")
                   connect_status, revert_dict, revert_plugin_status,deviceAvailability = connect_to_interface(obj,new_interface)
                   time.sleep(10)
                   if connect_status == "SUCCESS" and deviceAvailability == "Yes":
                      tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                      tdkTestObj.addParameter("plugin","Cobalt")
                      tdkTestObj.executeTestCase(expectedResult)
                      result = tdkTestObj.getResult()
                      cobalt_status = tdkTestObj.getResultDetails()
                      if cobalt_status == 'hibernated' and expectedResult in result:
                          print("\n Cobalt is in hibernated state after toggling the network interface")
                          tdkTestObj.setResultStatus("SUCCESS")
                      else:
                          print("\n Cobalt is not in hibernated state after toggling the network interface")
                          tdkTestObj.setResultStatus("FAILURE")
                                
                   else:
                       print("\n Error while setting interface as :{}".format(new_interface))
                       tdkTestObj.setResultStatus("FAILURE")
                       result_status, revert_dict_new, revert_plugins,deviceAvailability = connect_to_interface(obj, current_interface)
                       if result_status == "SUCCESS" and deviceAvailability == "Yes":
                          print("\n Successfully reverted the interface to: {}".format(current_interface))
                       else:
                          print("\n Error while reverting the interface to: {}".format(current_interface))
                          tdkTestObj.setResultStatus("FAILURE")
                else:
                   print("\n Cobalt is not in Hibernated state ")
                   tdkTestObj.setResultStatus("FAILURE")
            else:
               print("\n Unable to set cobalt in Hibernated state")
               tdkTestObj.setResultStatus("FAILURE")
            #Restore cobalt
            print("\n Restoring  Cobalt from Hibernated state")
            restore_status,start_restore =restore_plugin(obj,"Cobalt")
            if restore_status == expectedResult:
               tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
               tdkTestObj.addParameter("plugin","Cobalt")
               tdkTestObj.executeTestCase(expectedResult)
               result = tdkTestObj.getResult()
               cobalt_status = tdkTestObj.getResultDetails()
               if cobalt_status == 'suspended' and expectedResult in result:
                  print("\nCobalt suspended Successfully\n")
               else:
                   print("\n Cobalt is not in suspended state \n")
                   obj.setLoadModuleStatus("FAILURE")
            else:
                print("\n Unable to restore  Cobalt from Hibernated state \n")
                obj.setLoadModuleStatus("FAILURE")
        else:
            print("\nFailed to lauch Cobalt app")
    else:
        print("\n[Error] Preconditions are not met \n")
        obj.setLoadModuleStatus("FAILURE")
    if deviceAvailability == "Yes":
        if revert == "YES":
            print("\n Revert the values before exiting")
            status = set_plugins_status(obj,curr_plugins_status_dict)
    else:
        print("\n Device went down after change in interface. So reverting the plugins and interface is skipped")
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
