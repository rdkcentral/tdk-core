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
  <name>RDKV_CERT_PVS_Functional_Devcie_MaxResponseTime</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getSSHParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this script is to calculate the max response time it takes to get details from the device.</synopsis>
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
    <box_type>RDKTV</box_type>
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
    <test_objective>The objective of this script is to calculate the max response time it takes to get details from the device.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Video Accelerator</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>None</automation_approch>
    <expected_output>The time taken for api to respond should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_Devcie_MaxResponseTime</test_script>
    <skipped>No</skipped>
    <release_version>M116</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from datetime import datetime
import PerformanceTestVariables
from StabilityTestUtility import *
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_Device_MaxResponseTime');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result)
expectedResult = "SUCCESS"
response_time = []
method = PerformanceTestVariables.method
if expectedResult in result.upper():
    count = 0
    for i in range(5):
        tdkTestObj = obj.createTestStep('rdkservice_getMaxResponseTime')
        tdkTestObj.addParameter("method",method)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        time = tdkTestObj.getResultDetails()
        if expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            time = float(time)
            response_time.append(time)
            count = count + 1
        else:
            print("Error in getting the resposne time")
            tdkTestObj.setResultStatus("FAILURE")
            break
    if expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        print("\nCalculate the average time taken for get the resposne from device")
        conf_file,result = getConfigFileName(tdkTestObj.realpath)
        result, max_response_time = getDeviceConfigKeyValue(conf_file,"MAX_RESPONSE_TIME")
        average_timeTaken = sum (response_time)/len(response_time)
        print("\n Average time taken for 5 iterations: ",average_timeTaken)
        print("\n Threshold value for maximum response time: ",max_response_time)
        if (float(average_timeTaken) <= 0 or float(average_timeTaken) > float(max_response_time)):
            print("\nDevice took more than usual to respond.")
            tdkTestObj.setResultStatus("FAILURE")
        else:
            print("\nDevice responded within the expected time")
            tdkTestObj.setResultStatus("SUCCESS")
    else:
        print("\nFailed to validate the response time for 5 times")
        tdkTestObj.setResultStatus("FAILURE")
    obj.unloadModule("rdkv_performance");
else:
    print("Set Post Requisites Failed")
    tdkTestObj.setResultStatus("FAILURE")
