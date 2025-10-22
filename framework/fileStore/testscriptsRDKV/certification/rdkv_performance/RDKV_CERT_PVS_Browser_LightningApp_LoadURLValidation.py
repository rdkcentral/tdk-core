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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Browser_LightningApp_LoadURLValidation</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getBrowserURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this script is to validate if the URL is getting loaded correctly in Lightning App using API response and webinspect page.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_138</test_case_id>
    <test_objective>The objective of this script is to validate if the URL is getting loaded correctly in Lightning App using API response and webinspect page.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Launch Lightning app
2. Load any url through LightningApp.1.url
3. Validate whether the url launched is same as the url displayed in webinspect page</automation_approch>
    <expected_output>The url displayed in webinspect page should be same as the url launched in Lightning app</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Browser_LightningApp_LoadURLValidation</test_script>
    <skipped>No</skipped>
    <release_version>M111</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import PerformanceTestVariables
from BrowserPerformanceUtility import *
from StabilityTestUtility import *
import rdkv_performancelib
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Browser_LightningApp_LoadURLValidation')
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result)
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    event_listener = None
    lightning_app_webinspect_port = PerformanceTestVariables.lightning_app_webinspect_port
    browser_test_url = PerformanceTestVariables.browser_test_url
    conf_file, status = get_configfile_name(obj);
    print("\n Check Pre conditions")
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status = "SUCCESS"
    plugins_list = ["LightningApp","Cobalt","WebKitBrowser"]
    plugin_status_needed = {"LightningApp":"deactivated","Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    status,supported_plugins = getDeviceConfigValue(conf_file,"SUPPORTED_PLUGINS")
    for plugin in plugins_list[:]:
        if plugin not in supported_plugins:
            plugins_list.remove(plugin)
            plugin_status_needed.pop(plugin)
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print("\n Error while getting the status of plugins")
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            print("\n Unable to deactivate plugins")
            status = "FAILURE"
    if status == "SUCCESS":
        print("\nPre conditions for the test are set successfully")
        launch_status,launch_start_time = launch_plugin(obj,"LightningApp")
        if launch_status == expectedResult:
            time.sleep(10)
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","LightningApp")
            tdkTestObj.executeTestCase(expectedResult)
            lightningapp_status = tdkTestObj.getResultDetails()
            result = tdkTestObj.getResult()
            if lightningapp_status == 'resumed' and expectedResult in result:
                print("\n LightningApp resumed successfully")
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(10)
                print("\n Set test URL")
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","LightningApp.1.url")
                tdkTestObj.addParameter("value",browser_test_url)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                time.sleep(10)
                if expectedResult in result:
                    print("\nValidate if the URL is set successfully or not")
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method","LightningApp.1.url")
                    tdkTestObj.executeTestCase(expectedResult)
                    new_url = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                    if browser_test_url in new_url and expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("\n URL(",new_url,") is set successfully")
                        time.sleep(20)
                        tdkTestObj = obj.createTestStep('rdkservice_getBrowserURL')
                        tdkTestObj.addParameter("webinspect_port",lightning_app_webinspect_port)
                        tdkTestObj.executeTestCase(expectedResult)
                        target_URL = tdkTestObj.getResultDetails()
                        result = tdkTestObj.getResult()
                        if expectedResult in result:
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("Validate whether the url launched in Lightning App and url loaded in webinspect page are same")
                            if new_url == target_URL:
                                print("The url launched in Lightning App: {} is same as the url in webinspect page: {}".format(new_url,target_URL))
                            else:
                                print("The url launched in Lightning App: {} is not the same url in webinspect page: {}".format(new_url,target_URL))
                                tdkTestObj.setResultStatus("FAILURE");
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("Error in getting the url from webinpect page")
                    else:
                        print("\nFailed to load the URL, current url:",new_url)
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("\n Failed to set the URL")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("\n Error while resuming LightningApp, current status: ",lightningapp_status)
                tdkTestObj.setResultStatus("FAILURE")
            #Deactivate plugin
            print("\n Exiting from LightningApp")
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
        print("\nPre conditions are not met")
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print("\n Revert the values before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
