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
  <name>HdmicecHal_Add_LogicalAddress_InvalidArgument_Check</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>HdmicecHal_Add_LogicalAddress_InvalidArgument_Check</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>to verify with the invalid logical address</synopsis>
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
    <box_type>RDKTV</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_HdmicecHal_18</test_case_id>
    <test_objective>Test script to validate with the invalid logical address</test_objective>
    <test_type>negative</test_type>
    <test_setup>RDKTV</test_setup>
    <pre_requisite>1. TDK Agent should be up and running
    2. Required a setup with CEC enabled TV connection
3.  HdmiCecOpen should open a CEC driver instance successfully and iarmbus event should be obtained from device ready call back.</pre_requisite>
    <api_or_interface_used>HDMI_CEC_STATUS HdmiCecAddLogicalAddress(int handle, int logicalAddresses)</api_or_interface_used>
    <input_parameters>handle - driver handle
    logicalAddresses - logical address to be acquired</input_parameters>
    <automation_approch>1.Load the Hdmicec Hal module
    2. Add the invalid logical address to the driver using HdmiCecAddLogicalAddress API
    3. Based on the return value updated the test result as SUCCESS/FAILURE
    4. Unload the module</automation_approch>
    <expected_output>Should return the invalid argument</expected_output>
    <priority>High</priority>
    <test_stub_interface>libhdmicechalstub.so.0.0.0</test_stub_interface>
    <test_script>HdmicecHal_Add_LogicalAddress_InvalidArgument_Check</test_script>
    <skipped>no</skipped>
    <release_version>M125</release_version>
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
obj.configureTestCase(ip,port,'HdmicecHal_Add_LogicalAddress_InvalidArgument_Check');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);

if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";
    print("\nTEST STEP : Send an invalid logical address to the HdmiCecAddLogicalAddress API");
    print("EXEPECTED RESULT : Getting invalid argument error from driver");
    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('HdmicecHal_AddLogicalAddress');
    logical_addr = 16;
    tdkTestObj.addParameter("logical_addr",logical_addr);
    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("FAILURE");
        print("ACTUAL RESULT  : ",details);
        print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        tdkTestObj.setResultStatus("SUCCESS");
        print(details)
        print("ACTUAL RESULT: HdmiCecAddLogicalAddress call failed due to invalid logical address");
        print("[TEST EXECUTION RESULT] : SUCCESS\n");

    obj.unloadModule("hdmicechal");
else:
    print("Load module failed");
    obj.setLoadModuleStatus("FAILURE");
