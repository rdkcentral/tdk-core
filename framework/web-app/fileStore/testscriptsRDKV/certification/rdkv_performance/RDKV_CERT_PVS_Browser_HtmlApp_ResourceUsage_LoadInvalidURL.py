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
  <version>10</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Browser_HtmlApp_ResourceUsage_LoadInvalidURL</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate the resource usage after loading Invalid URL in HtmlApp and check whether Html App is stable, and no crash is observed.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_142</test_case_id>
    <test_objective>The objective of this test is to validate the resource usage after loading InvalidURL in HtmlApp and check whether Html App is stable, and no crash is observed.</test_objective>
    <test_type>Negative</test_type>
    <test_setup>RPI,Video_Accelarator</test_setup>
    <pre_requisite>1. wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>html_page_url: string</input_parameters>
    <automation_approch>1. Launch HtmlApp using RDKShell
2. Set a Invalid URL in HtmlApp using HtmlApp.1.url method.
3. Validate the resource usage by DeviceInfo.1.systeminfo method
4. Check for crashes
5. Revert the status of HtmlApp.</automation_approch>
    <expected_output>Current URL should not be changed due to loading of Invalid URL and resource usage must be within the expected limit and no crashes should be observed.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Browser_HtmlApp_ResourceUsage_LoadInvalidURL</test_script>
    <skipped>No</skipped>
    <release_version>M123</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Browser_HtmlApp_ResourceUsage_LoadInvalidURL')
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result)
expectedResult = "SUCCESS"
if expectedResult in result.upper():    
    browser_invalid_test_url = PerformanceTestVariables.browser_invalid_test_url
    print("\n Check Pre conditions")
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status = "SUCCESS"
    plugins_list = ["HtmlApp","Cobalt","WebKitBrowser"]
    plugin_status_needed = {"HtmlApp":"deactivated","Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    url_to_grep = browser_invalid_test_url.replace('https://', '')
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
        launch_status,launch_start_time = launch_plugin(obj,"HtmlApp")
        if launch_status == expectedResult:
            time.sleep(10)
            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","HtmlApp")
            tdkTestObj.executeTestCase(expectedResult)
            htmlapp_status = tdkTestObj.getResultDetails()
            result = tdkTestObj.getResult()
            if htmlapp_status == 'resumed' and expectedResult in result:
                print("\n HtmlApp resumed successfully")
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(10)
                tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                tdkTestObj.addParameter("realpath",obj.realpath)
                tdkTestObj.addParameter("deviceIP",obj.IP)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                if browser_invalid_test_url != "" and ssh_param_dict != {}:
                    tdkTestObj.setResultStatus("SUCCESS")
                    time.sleep(10)
                    print("\nPre conditions for the test are set successfully");
                    print("\nGet the URL in HtmlApp")
                    tdkTestObj = obj.createTestStep('rdkservice_getValue');
                    tdkTestObj.addParameter("method","HtmlApp.1.url");
                    tdkTestObj.executeTestCase(expectedResult);
                    current_url = tdkTestObj.getResultDetails();
                    result = tdkTestObj.getResult()
                    if current_url != None and expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("Current URL:",current_url)
                        print("\n Setting the test URL")
                        Execution_start_time = str(datetime.utcnow()).split()[1]
                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                        tdkTestObj.addParameter("method","HtmlApp.1.url")
                        tdkTestObj.addParameter("value",browser_invalid_test_url)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResult()
                        time.sleep(10)
                        if expectedResult in result:
                            tdkTestObj.setResultStatus("SUCCESS")
                            command = 'cat /opt/logs/wpeframework.log | grep -inr "Failed to load resource" | grep -nr ' + url_to_grep + ' | tail -1'
                            print("COMMAND : %s" %(command))
                            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                            tdkTestObj.addParameter("command",command)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            output = tdkTestObj.getResultDetails()
                            if output != "EXCEPTION" and "Failed to load resource" in output and url_to_grep in output:
                                print("\n Invalid URL is not loaded in HtmlApp \n")
                                command = 'cat /opt/logs/wpeframework.log | grep -inr crash'
                                print("COMMAND : %s" %(command))
                                #Primitive test case which associated to this Script
                                tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog');
                                #Add the parameters to ssh to the DUT and execute the command
                                tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                                tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                                tdkTestObj.addParameter("command",command)
                                #Execute the test case in DUT
                                tdkTestObj.executeTestCase(expectedResult);
                                result = tdkTestObj.getResult()
                                output = tdkTestObj.getResultDetails()                                
                                print(output)
                                output = tdkTestObj.getResultDetails().replace(r'\n', '\n');
                                output = output[output.find('\n')]
                                time.sleep(10)
                                if "crash" in output :
                                     crash_time = getTimeStampFromString(output)
                                     crash_status=(True if Execution_start_time < crash_time  else False)
                                     print(Execution_start_time)
                                else:
                                     crash_status=False
                                     
                                if not crash_status :
                                    print("Crash is not observed while loading invalid URL in HtmlApp")
                                    print("\n Validate the status of HtmlApp plugin :\n")
                                    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                    tdkTestObj.addParameter("plugin","HtmlApp")
                                    #Execute the test case in DUT
                                    tdkTestObj.executeTestCase(expectedResult);
                                    output = tdkTestObj.getResultDetails()
                                    if output != 'deactivated':
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print("\nGet the URL in HtmlApp")
                                        tdkTestObj = obj.createTestStep('rdkservice_getValue');
                                        tdkTestObj.addParameter("method","HtmlApp.1.url");
                                        tdkTestObj.executeTestCase(expectedResult);
                                        present_url = tdkTestObj.getResultDetails();
                                        result = tdkTestObj.getResult()
                                        if current_url == present_url and expectedResult in result:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print("\nCurrent url persisted after loading invalidURL")
                                            print("\n Validating resource usage:")
                                            tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                                            tdkTestObj.executeTestCase(expectedResult)
                                            resource_usage = tdkTestObj.getResultDetails()
                                            result = tdkTestObj.getResult()
                                            if expectedResult in result and resource_usage != "ERROR":
                                                print("\n Resource usage is within the expected limit")
                                                tdkTestObj.setResultStatus("SUCCESS")
                                            else:
                                                print("\n Error while validating resource usage")
                                                tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            print("\Current url did not persist")
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print("Html App got deactivated automatically while loading an invalid URL")
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print("Crash observed")
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print("\n Exception occured while getting crash logs \n")
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("\n 'Failed to load resource' related logs are not available \n")
                            tdkTestObj.setResultStatus("FAILURE")

                    else:
                        print("\nUnable to set URL in HtmlApp")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("\nFailed to get the URL in HtmlApp")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("\n Error while resuming HtmlApp, current status: ",htmlapp_status)
                tdkTestObj.setResultStatus("FAILURE")

            #Deactivate plugin
            print("\n Exiting from HtmlApp")
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
