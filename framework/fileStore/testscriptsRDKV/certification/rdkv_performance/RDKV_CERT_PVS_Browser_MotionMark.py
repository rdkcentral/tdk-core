##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2022 RDK Management
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
  <name>RDKV_CERT_PVS_Browser_MotionMark</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getBrowserScore_MotionMark</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate the average fps value obtained from the browser performance using Motion Mark</synopsis>
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
    <test_case_id>RDKV_PERFORMANCE_102</test_case_id>
    <test_objective>The objective of this test is to validate the average fps value obtained from the browser performance using Motion Mark</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. Threshold value of motionmark score
2. motionmark test url</input_parameters>
    <automation_approch>1. As a pre requisite disable all other plugins and enable webkitbrowser plugin.
2. Load the motionmark Browser test URL
3. Get the final score and validate it
4. Revert all values</automation_approch>
    <expected_output>The browser score from motionmark should be in the expected range</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Browser_MotionMark</test_script>
    <skipped>No</skipped>
    <release_version>M97</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
from BrowserPerformanceUtility import *
import BrowserPerformanceUtility
from rdkv_performancelib import *
import rdkv_performancelib
import json
import BrowserPerformanceVariables
from StabilityTestUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Browser_MotionMark')

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

# Execution Summary Variable
Summ_list=[]

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
  app_bundle_name=BrowserPerformanceVariables.motion_app_bundle_name
  app_download_url=BrowserPerformanceVariables.motion_app_download_url
  sub_category_failure = False

  app_name = "com.rdkcentral.motion"
  status = rdkservice_install_launch_app(obj, app_bundle_name, app_name, app_download_url)
  if status == "SUCCESS": 
    browsertest_keypress(obj,app_name,[["9","13"],[]])
    time.sleep(420)
    tdkTestObj = obj.createTestStep('rdkservice_getBrowserScore_MotionMark')
    tdkTestObj.executeTestCase(expectedResult)
    browser_score_dict = json.loads(tdkTestObj.getResultDetails())
    result = tdkTestObj.getResult()
    if browser_score_dict["main_score"] != "Unable to get the browser score" and expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS");
        browser_score = browser_score_dict["main_score"]
        conf_file,result = getConfigFileName(tdkTestObj.realpath)
        result1, motionmark_threshold_value = getDeviceConfigKeyValue(conf_file,"MOTIONMARK_THRESHOLD_VALUE")
        if motionmark_threshold_value != "":
            print("\n Browser score from test: ",browser_score)
            Summ_list.append('Browser score from test: {} '.format(browser_score))
            print("\n Threshold value for browser score:",motionmark_threshold_value)
            Summ_list.append('Threshold value for browser score: {}'.format(motionmark_threshold_value))
            if float(browser_score) > float(motionmark_threshold_value):
                print("\n The browser performance score is high as expected\n")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("\n The browser performance score is lower than expected \n")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("Failed to get the threshold value from config file")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("Failed to get the browser score")

    print("\n Terminating the app")
    tdkTestObj = obj.createTestStep('rdkv_terminate_app');
    tdkTestObj.addParameter("app_id",app_name)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    if result == "SUCCESS":
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print("Unable to terminate the app")
  else:
      print("Failed to launch the app")

  getSummary(Summ_list,obj)
  obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")
