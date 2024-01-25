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
  <name>RDKV_CERT_PVS_Browser_WebKit_LoadURLValidation</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getBrowserURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this script is to validate if the URL is getting loaded correctly in WebKit using API response and webinspect page.</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_136</test_case_id>
    <test_objective>The objective of this script is to validate if the URL is getting loaded correctly in WebKit using API response and webinspect page.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Launch webkit browser
2. Load any url through WebKitBrowser.1.url
3. Validate whether the url launched is same as the url displayed in webinspect page</automation_approch>
    <expected_output>The url displayed in webinspect page should be same as the url launched in webkit browser</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Browser_WebKit_LoadURLValidation</test_script>
    <skipped>No</skipped>
    <release_version>M111</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import PerformanceTestVariables
from BrowserPerformanceUtility import *
from StabilityTestUtility import *
import rdkv_performancelib
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Browser_WebKit_LoadURLValidation');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    webinspect_port = PerformanceTestVariables.webinspect_port
    browser_test_url = PerformanceTestVariables.browser_test_url
    print("Check Pre conditions")
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status,curr_webkit_status,curr_cobalt_status = check_pre_requisites(obj)
    print("Current values \nWebKitBrowser:%s\nCobalt:%s"%(curr_webkit_status,curr_cobalt_status));
    if status == "FAILURE":
        if "FAILURE" not in (curr_webkit_status,curr_cobalt_status):
            set_status=set_pre_requisites(obj)
            #Need to revert the values since we are changing plugin status
            revert="YES"
            if set_status == "SUCCESS":
                status,webkit_status,cobalt_status = check_pre_requisites(obj)
            else:
                status = "FAILURE"
    time.sleep(10)
    if status == "SUCCESS" and browser_test_url != "":
        time.sleep(10)
        print("\nPre conditions for the test are set successfully");
        print("\nGet the URL in WebKitBrowser")
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            print("Current URL:",current_url)
            print("\nSet Browser test URL")
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
            tdkTestObj.addParameter("value",browser_test_url);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                print("\nValidate if the URL is set successfully or not")
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                tdkTestObj.executeTestCase(expectedResult);
                new_url = tdkTestObj.getResultDetails();
                result = tdkTestObj.getResult()
                if browser_test_url in new_url and expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("\n URL(",new_url,") is set successfully")
                    time.sleep(30)
                    tdkTestObj = obj.createTestStep('rdkservice_getBrowserURL')
                    tdkTestObj.addParameter("webinspect_port",webinspect_port)
                    tdkTestObj.executeTestCase(expectedResult)
                    target_URL = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                    if expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("Validate whether the url launched in webkit browser and url loaded in webinspect page are same")
                        if new_url == target_URL:
                            print("The url launched in webkit browser: {} is same as the url in webinspect page: {}".format(new_url,target_URL))
                        else:
                            print("The url launched in webkit browser: {} is not the same url in webinspect page: {}".format(new_url,target_URL))
                            tdkTestObj.setResultStatus("FAILURE");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("Error in getting the url from webinpect page")
                else:
                    print("\nFailed to load the URL ",browser_test_url)
                    print("current url:",new_url)
                    tdkTestObj.setResultStatus("FAILURE");
        #Set the URL back to previous
        tdkTestObj = obj.createTestStep('rdkservice_setValue');
        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
        tdkTestObj.addParameter("value",current_url);
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult();
        if result == "SUCCESS":
            print("\nURL is reverted successfully")
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            print("\nFailed to revert the URL")
            tdkTestObj.setResultStatus("FAILURE");
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print("\nPre conditons are not met")
    time.sleep(5)
    #Revert the values
    if revert=="YES":
        print("\nRevert the values before exiting")
        status = revert_value(curr_webkit_status,curr_cobalt_status,obj);
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")
