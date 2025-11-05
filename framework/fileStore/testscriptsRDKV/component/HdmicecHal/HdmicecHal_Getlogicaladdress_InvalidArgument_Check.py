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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>HdmicecHal_Getlogicaladdress_InvalidArgument_Check</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>HdmicecHal_GetLogicalAddress</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>to verify the GetLogicalAddress HAL API by passing an invalid params.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
   <test_cases>
    <test_case_id>TC_HdmicecHal_23</test_case_id>
    <test_objective>Test script to validate with the invalid NULL param</test_objective>
    <test_type>negative</test_type>
    <test_setup>Video_Accelerator</test_setup>
    <pre_requisite>1. TDK Agent should be up and running
    2. Required a setup with CEC enabled TV connection
3.  HdmiCecOpen should open a CEC driver instance successfully and iarmbus event should be obtained from device ready call back.</pre_requisite>
    <api_or_interface_used>HdmiCecGetLogicalAddress(int handle, int *logicalAddresses)</api_or_interface_used>
    <input_parameters>handle - driver handle
    logicalAddresses - passing NULL param to validate</input_parameters>
    <automation_approch>1.Load the Hdmicec Hal module
    2. Add the invalid NULL param to the driver using HdmiCecGetLogicalAddress API
    3. Based on the return value updated the test result as SUCCESS/FAILURE
    4. Unload the module</automation_approch>
    <expected_output>Driver should return the invalid argument</expected_output>
    <priority>High</priority>
    <test_stub_interface>libhdmicechalstub.so.0.0.0</test_stub_interface>
    <test_script>HdmicecHal_Getlogicaladdress_InvalidArgument_Check</test_script>
    <skipped>no</skipped>
    <release_version>M126</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("hdmicechal","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'HdmicecHal_Getlogicaladdress_InvalidArgument_Check');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadModuleStatus);

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";

    print("\nTEST STEP : Verify the HdmiCecGetLogicalAddress API by passing NULL to the logical address param")
    print("EXPECTED RESULT : Should get the invalid argument from the driver")
    tdkTestObj = obj.createTestStep('HdmicecHal_GetLogicalAddress');
    Is_null_param_check = 1;
    tdkTestObj.addParameter("Is_null_param_check", Is_null_param_check);
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("FAILURE");
        print("Value Returned: ", details)
    else:
        tdkTestObj.setResultStatus("SUCCESS");
        print(details)
        print("ACTUAL RESULT: HdmiCecGetLogicalAddress call failed due to invalid arg")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")

    obj.unloadModule("hdmicechal");
else:
    print("Load module failed");
    obj.setLoadModuleStatus("FAILURE");
