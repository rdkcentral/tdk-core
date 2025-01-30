##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2023 RDK Management
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
  <name>RDKV_CERT_PVS_Functional_Check_LowRAMWarning</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this script is to check whether the events onDeviceLowRamWarning and onDeviceCriticallyLowRamWarning are triggered when multiple plugins are launched and destroyed in the device.</synopsis>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
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
    <test_case_id>RDKV_PERFORMANCE_140</test_case_id>
    <test_objective>The objective of this script is to check whether the events onDeviceLowRamWarning and onDeviceCriticallyLowRamWarning are triggered when multiple plugins are launched and destroyed in the device. </test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Set the memory monitor to 'True' in the device
2. Launch Cobalt and destroy cobalt
3. Launch HTML app and destroy HTML app
4. Launch Lightning app and destroy Lightning app
5. Check if the events onDeviceLowRamWarning and onDeviceCriticallyLowRamWarning are triggered. </automation_approch>
    <expected_output>The events onDeviceLowRamWarning and onDeviceCriticallyLowRamWarning should not be triggered when multiple apps are launched and destroyed in the device. </expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_Check_LowRAMWarning</test_script>
    <skipped>No</skipped>
    <release_version>M111</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import PerformanceTestVariables
from StabilityTestUtility import *
from web_socket_util import *
import rdkv_performancelib
from rdkv_performancelib import *
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_Check_LowRAMWarning');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
#Execution summary variable
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print("Check Pre conditions")
    event_listener = None
    status = "SUCCESS"
    revert = "NO"
    plugins_list = ["Cobalt","HtmlApp","LightningApp"]
    plugin_status_needed = {"Cobalt":"deactivated","HtmlApp":"deactivated","LightningApp":"deactivated"}
    conf_file, status = get_configfile_name(obj);
    status,supported_plugins = getDeviceConfigValue(conf_file,"SUPPORTED_PLUGINS")
    for plugin in plugins_list[:]:
        if plugin not in supported_plugins:
            plugins_list.remove(plugin)
            plugin_status_needed.pop(plugin)
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
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
    if status == "SUCCESS" and expectedResult in result and ssh_param_dict != {}:
        print("\nPre conditions for the test are set successfully")
        print("\n Set the Memory status are 'True' \n")
        params = '{"enable":"True"}'
        tdkTestObj = obj.createTestStep('rdkservice_setValue');
        tdkTestObj.addParameter("method","org.rdk.RDKShell.setMemoryMonitor");
        tdkTestObj.addParameter("value",params)
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult();
        if expectedResult in result:
            thunder_port = rdkv_performancelib.devicePort
            event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 6,"method": "org.rdk.RDKShell.1.register","params": {"event": "onDeviceCriticallyLowRamWarning", "id": "client.events.1" }}'],"/jsonrpc",False)
            event_listener = createEventListener(ip,thunder_port,['{"jsonrpc": "2.0","id": 6,"method": "org.rdk.RDKShell.1.register","params": {"event": "onDeviceLowRamWarning", "id": "client.events.1" }}'],"/jsonrpc",False)
            time.sleep(5)
            launch_status,launch_start_time = launch_plugin(obj,"Cobalt")
            if launch_status == expectedResult:
                time.sleep(5)
                tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                tdkTestObj.addParameter("plugin","Cobalt")
                tdkTestObj.executeTestCase(expectedResult)
                cobalt_status = tdkTestObj.getResultDetails()
                result = tdkTestObj.getResult()
                if cobalt_status == 'resumed' and expectedResult in result:
                    print("\nCobalt Resumed Successfully\n")
                    print("\n launch HtmlApp")
                    launch_status,launch_start_time = launch_plugin(obj,"HtmlApp")
                    if launch_status == expectedResult:
                        time.sleep(5)
                        tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                        tdkTestObj.addParameter("plugin","HtmlApp")
                        tdkTestObj.executeTestCase(expectedResult)
                        htmlapp_status = tdkTestObj.getResultDetails()
                        result = tdkTestObj.getResult()
                        if htmlapp_status == 'resumed' and expectedResult in result:
                            print("\n HtmlApp resumed successfully")
                            time.sleep(10)
                            print("\n Launching Lightning app")
                            launch_status,launch_start_time = launch_plugin(obj,"LightningApp")
                            if launch_status == expectedResult:
                                time.sleep(5)
                                tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                tdkTestObj.addParameter("plugin","LightningApp")
                                tdkTestObj.executeTestCase(expectedResult)
                                lightningapp_status = tdkTestObj.getResultDetails()
                                result = tdkTestObj.getResult()
                                if lightningapp_status == 'resumed' and expectedResult in result:
                                    print("\n LightningApp resumed successfully")
                                    continue_count = 0
                                    while True:
                                        if (continue_count > 120):
                                            print("\n The events onDeviceLowRamWarning and onDeviceCriticallyLowRamWarning are not triggered")
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            break
                                        if (len(event_listener.getEventsBuffer())== 0):
                                            continue_count += 1
                                            time.sleep(1)
                                            continue
                                        event_log = event_listener.getEventsBuffer().pop(0)
                                        print("\n Triggered event: ",event_log,"\n")
                                        if ("onDeviceLowRamWarning" in str(event_log)):
                                            print("\n Event onDeviceLowRamWarning is triggered")
                                            tdkTestObj.setResultStatus("FAILURE")
                                        elif ("onDeviceCriticallyLowRamWarning" in str(event_log)):
                                            print("\n Event onDeviceCriticallyLowRamWarning is triggered")
                                            tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            print("\n Error in validating the events from event log")
                                            tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print("\n Error while getting the status of Lightning app")
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print("\n Error while launching Lightning app")
                                tdkTestObj.setResultStatus("FAILURE")
                            print("\n Exiting from Lightning App \n")
                            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                            tdkTestObj.addParameter("plugin","LightningApp")
                            tdkTestObj.addParameter("status","deactivate")
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            if result == "SUCCESS":
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print("Unable to deactivate LightningApp")
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("Error while getting the status of HTML plugin")
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print("\n Error while launching HTML App")
                        tdkTestObj.setResultStatus("FAILURE")
                    print("\n Exiting from HtmlApp \n")
                    tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                    tdkTestObj.addParameter("plugin","HtmlApp")
                    tdkTestObj.addParameter("status","deactivate")
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("Unable to deactivate HtmlApp")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("\n Error while getting the status of Cobalt plugin")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("\n Error while launching Cobalt plugin")
                tdkTestObj.setResultStatus("FAILURE")
            print("\n Exiting from HtmlApp \n")
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
            tdkTestObj.addParameter("plugin","HtmlApp")
            tdkTestObj.addParameter("status","deactivate")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if result == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("Unable to deactivate HtmlApp")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("\n Error while setting up the memory status as 'True'")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("Error in setting up the pre conditions")
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list,obj)
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")
