##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
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
  <name>RDKV_CERT_RVS_LightningApp_LaunchURL_StressTest</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateCPULoad</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to stress test by loading URL in LightningApp for 100 times without destroying the application.</synopsis>
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
    <test_case_id>RDKV_STABILITY_80</test_case_id>
    <test_objective>The objective of this test is to stress test by loading URL in LightningApp for 100 times without destroying the application. </test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>test_url_1</input_parameters>
    <automation_approch>1. As a prerequisite disable all plugins and enable LightningApp and DeviceInfo plugins
2. Start a loop upto max_count value and inside the loop:
a) set video_src_url_hls and verify whether it is set successfully
b) repeat this for max_count without destroying the plugin. 
3. Revert the plugins</automation_approch>
    <expected_output>URLs should be set and verified without destroying the plugin and CPU load and memory usage must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_LightningApp_LaunchURL_StressTest</test_script>
    <skipped>No</skipped>
    <release_version>M135</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
 
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import StabilityTestVariables
import json
from StabilityTestUtility import *
from rdkv_performancelib import *

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1", standAlone=True);

# IP and Port of box, No need to change
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>  
port = <port>  
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_LightningApp_LaunchURL_StressTest');

# The device will reboot before starting the stability testing if "pre_req_reboot" is configured as "Yes"
pre_requisite_reboot(obj)

# Get the result of connection with the test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result)

# Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)
expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    print("Check Pre conditions")

    revert = "NO"
    plugins_list = ["LightningApp", "Cobalt", "DeviceInfo"]
    plugin_status_needed = {"LightningApp": "resumed", "Cobalt": "deactivated", "DeviceInfo": "activated"}
    conf_file, status = get_configfile_name(obj)
    status, supported_plugins = getDeviceConfigValue(conf_file, "SUPPORTED_PLUGINS")

    for plugin in plugins_list[:]:
        if plugin not in supported_plugins:
            plugins_list.remove(plugin)
            plugin_status_needed.pop(plugin)

    curr_plugins_status_dict = get_plugins_status(obj, plugins_list)
    time.sleep(10)
    status = "SUCCESS"

    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print("\nError while getting the status of plugins")
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj, plugin_status_needed)
        time.sleep(10)
        new_plugins_status = get_plugins_status(obj, plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"

    test_url = StabilityTestVariables.video_src_url_hls
    max_count = StabilityTestVariables.max_count
    if status == "SUCCESS" and test_url != "":
        print("\nPre conditions for the test are set successfully")
        print("\nGet the URL in LightningApp")

        # Get current URL in LightningApp
        tdkTestObj = obj.createTestStep('rdkservice_getValue')
        tdkTestObj.addParameter("method", "LightningApp.1.url")
        tdkTestObj.executeTestCase(expectedResult)
        current_url = tdkTestObj.getResultDetails()
        result = tdkTestObj.getResult()

        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")

            for count in range(1, max_count):
                result_dict = {}
                print("\nIteration:",count)
                print("\nSetting test URL")
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method", "LightningApp.1.url")
                tdkTestObj.addParameter("value", test_url)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()

                if result == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                    time.sleep(5)
                    print("\nValidate if the URL is set successfully or not")

                    # Verify URL after setting
                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method", "LightningApp.1.url")
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    new_url = tdkTestObj.getResultDetails()

                    if test_url in new_url and expectedResult in result:
                        print(f"URL : {test_url} is set in LightningApp")
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print(f"\nUnable to set URL: {test_url} current URL: {new_url}")
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print(f"\nError while setting the URL: {test_url} current URL: {current_url}")
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            else:
                print(f"\nSuccessfully completed {max_count} iterations\n")

            # Revert the URL back to the initial URL
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method", "LightningApp.1.url")
            tdkTestObj.addParameter("value", current_url)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()

            if result == "SUCCESS":
                print("\nURL is reverted successfully")
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("\nFailed to revert the URL")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("\nUnable to get the current URL loaded in LightningApp")
    else:
        print("\nPre conditions are not met")
        obj.setLoadModuleStatus("FAILURE")

    # Revert the values
    if revert == "YES":
        print("\nRevert the values before exiting")
        status = set_plugins_status(obj, curr_plugins_status_dict)

    # Validate device state after test completion
    post_condition_status = check_device_state(obj)
    obj.unloadModule("rdkv_stability")
else:
    print("Failed to load module")
    obj.setLoadModuleStatus("FAILURE")
