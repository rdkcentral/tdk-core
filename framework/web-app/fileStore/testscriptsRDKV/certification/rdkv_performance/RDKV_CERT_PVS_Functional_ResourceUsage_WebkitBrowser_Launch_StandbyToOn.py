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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Functional_ResourceUsage_WebkitBrowser_Launch_StandbyToOn</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to calculate the resource usage during WebKitBrowser launch in standby mode to ON</synopsis>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_144</test_case_id>
    <test_objective>The objective of this test is to calculate the resource usage during WebKitBrowser launch in standby mode to ON.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be running in DUT.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. As a prerequisite enable System plugin disable WebKit and html plugins.
2. Get the current power state.
3. Get the preferred standby mode and if it is not LIGHT_SLEEP set it to LIGHT_SLEEP.
4. Set the power state to STANDBY
5. Set the power state to ON and launch WebKitBrowser
6. Calculate the resource usage.
7. Revert values</automation_approch>
    <expected_output>Device's power state should be changed.
Resource usage should be within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_ResourceUsage_WebkitBrowser_Launch_StandbyToOn</test_script>
    <skipped>No</skipped>
    <release_version>M115</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
 # use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from StabilityTestUtility import *
import PerformanceTestVariables
from web_socket_util import *
import json
import rdkv_performancelib
from rdkv_performancelib import *
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_ResourceUsage_WebkitBrowser_Launch_StandbyToOn');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Check Pre conditions"
    continue_count = 0
    event_listener = None
    power_state = ""
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["LightningApp","Cobalt","WebKitBrowser"]
    plugin_status_needed = {"LightningApp":"deactivated","Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    status = "SUCCESS"
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print "\n Error while getting the status of plugins"
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            print "\n Unable to deactivate plugins"
            status = "FAILURE"
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if status == "SUCCESS" and expectedResult in result and ssh_param_dict != {}:
        time.sleep(10)
        print "\nPre conditions for the test are set successfully"
        print "\n Get the current StandByMode of the device:"
        print "\n Invoke org.rdk.System.1.getPreferredStandbyMode \n"
        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult');
        tdkTestObj.addParameter("method","org.rdk.System.1.getPreferredStandbyMode");
        tdkTestObj.addParameter("reqValue","preferredStandbyMode")
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult();
        preferred_standby = tdkTestObj.getResultDetails()
        if expectedResult in result and preferred_standby != "LIGHT_SLEEP":
            tdkTestObj.setResultStatus("SUCCESS")
            print "\n Set standby mode as LIGHT_SLEEP \n"
            params = '{"standbyMode":"LIGHT_SLEEP"}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","org.rdk.System.1.setPreferredStandbyMode");
            tdkTestObj.addParameter("value",params)
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                print "\n SetPreferredStandbyMode is success \n"
                tdkTestObj.setResultStatus("SUCCESS")
                print "\n Invoke org.rdk.System.1.getPreferredStandbyMode \n"
                tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult');
                tdkTestObj.addParameter("method","org.rdk.System.1.getPreferredStandbyMode");
                tdkTestObj.addParameter("reqValue","preferredStandbyMode")
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult();
                preferred_standby = tdkTestObj.getResultDetails()
                if expectedResult in result and preferred_standby == "LIGHT_SLEEP":
                    print "\n Preferred standby mode is LIGHT_SLEEP \n"
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print "\n Error in setting up the stand by mode as LIGHT_SLEEP"
                    tdkTestObj.setResultStatus("FAILURE")
        if expectedResult in result and preferred_standby == "LIGHT_SLEEP":
            print "Check the current power state"
            tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
            tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
            tdkTestObj.addParameter("reqValue","powerState")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            current_power_state = tdkTestObj.getResultDetails()
            if expectedResult in result and current_power_state != "STANDBY":
                print "\n The current power state is: ",current_power_state
                print "\n Set the current power state mode to StandBy"
                params = '{"powerState":"STANDBY", "standbyReason":"APIUnitTest"}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.System.1.setPowerState")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if expectedResult in result:
                    print "\n Get the current power state: \n"
                    tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                    tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
                    tdkTestObj.addParameter("reqValue","powerState")
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    current_power_state = tdkTestObj.getResultDetails()
                else:
                    print "\n Error in setting up the power state to standby"
                    tdkTestObj.setResultStatus("FAILURE")        
            if expectedResult in result and current_power_state == "STANDBY":
                    print "\n Current power state : \n",current_power_state
                    print "\n Set the current power state mode to ON"
                    params = '{"powerState":"ON", "standbyReason":"APIUnitTest"}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.System.1.setPowerState")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if expectedResult in result:
                        print "\n Get the current power state: \n"
                        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                        tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
                        tdkTestObj.addParameter("reqValue","powerState")
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        current_power_state = tdkTestObj.getResultDetails()
                        if expectedResult in result and current_power_state == "ON":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print "\n Current power state : \n",current_power_state
                            tdkTestObj.setResultStatus("SUCCESS")
                            WebKitBrowser_launch_status,launch_time = launch_plugin(obj,"WebKitBrowser")
                            time.sleep(10)
                            if WebKitBrowser_launch_status == "SUCCESS":
                                time.sleep(5)
                                tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                tdkTestObj.addParameter("plugin","WebKitBrowser")
                                tdkTestObj.executeTestCase(expectedResult)
                                WebKitBrowser_status = tdkTestObj.getResultDetails()
                                result = tdkTestObj.getResult()
                                if WebKitBrowser_status == 'resumed' and expectedResult in result:
                                    print "\n WebKitBrowser resumed successfully"
                                    print "\n Validating resource usage:"
                                    tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                                    tdkTestObj.executeTestCase(expectedResult)
                                    resource_usage = tdkTestObj.getResultDetails()
                                    result = tdkTestObj.getResult()
                                    if expectedResult in result and resource_usage != "ERROR":
                                        print "\n Resource usage is within the expected limit"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "\n Error while validating resource usage"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Error while checking WebKitBrowser status, current status: ",WebKitBrowser_status
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error while launching WebKitBrowser"
                                obj.setLoadModuleStatus("FAILURE")
                        else:
                            print "\n Error in getting the current power state"
                            obj.setLoadModuleStatus("FAILURE")
                    else:
                        print "\n Error in setting up the current power state to ON"
                        obj.setLoadModuleStatus("FAILURE")
            else:
                print "\n Error in setting up the current power state to StandBy"
                obj.setLoadModuleStatus("FAILURE")
            #Deactivate plugin
            print "\n Exiting from WebKitBrowser"
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
            tdkTestObj.addParameter("plugin","WebKitBrowser")
            tdkTestObj.addParameter("status","deactivate")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if result == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "Unable to deactivate WebKitBrowser"
                tdkTestObj.setResultStatus("FAILURE")        
        else:
            print "\n Error in setting up the pre-condition"
            obj.setLoadModuleStatus("FAILURE")
        #Revert the values
        if revert=="YES":
            print "\n Revert the values before exiting"
            status = set_plugins_status(obj,curr_plugins_status_dict)
        obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print "Failed to load module"
