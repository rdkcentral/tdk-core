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
  <name>HdmicecHal_Remove_LogicalAddress</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>HdmicecHal_RemoveLogicalAddress</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>to remove the last added logical address</synopsis>
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
    <test_case_id>TC_HdmicecHal_17</test_case_id>
    <test_objective>Test script to remove the logical address which last acquired</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDKTV</test_setup>
    <pre_requisite>1. TDK Agent should be up and running
    2. Required a setup with CEC enabled TV connection
    3.  HdmiCecOpen should open a CEC driver instance successfully and iarmbus event should be obtained from device ready call back.</pre_requisite>
    <api_or_interface_used>HDMI_CEC_STATUS HdmiCecRemoveLogicalAddress(int handle, int logicalAddresses)
    HDMI_CEC_STATUS HdmiCecGetLogicalAddress(int handle, int *logicalAddress)</api_or_interface_used>
    <input_parameters>handle - driver handle
    logicalAddresses - logical address to be released</input_parameters>
    <automation_approch>1.Load the Hdmicec Hal module
    2. Remove the logical address from the driver using HdmiCecRemoveLogicalAddress API
    3. Get the logical address obtained by the driver using HdmiCecGetLogicalAddress API
    4. Based on the logical address obtained updated the test result as SUCCESS/FAILURE
    5. Unload the module</automation_approch>
    <expected_output>should released the last acquired logical address</expected_output>
    <priority>High</priority>
    <test_stub_interface>libhdmicechalstub.so.0.0.0</test_stub_interface>
    <test_script>HdmicecHal_Remove_LogicalAddress</test_script>
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
obj.configureTestCase(ip,port,'HdmicecHal_Remove_LogicalAddress');
#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";

    # Get the device's current logical address to reasign it once exectuted the testcase
    tdkTestObj = obj.createTestStep('HdmicecHal_GetLogicalAddress');
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    cur_logical_addr = int(str(details).split(":",1)[1].split(",")[1].split(":")[1].strip())
    print("cur_logical_addr %d" %(cur_logical_addr))
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        print("Value Returned : ",details)
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print("Value Returned : ",details)

    # Add new logical address other than the defaul one - 4
    print("\nTEST STEP1 : Add any logical address using HdmiCecAddLogicalAddress API to veriy the remove functionality");
    logical_addr = 9;
    Is_handle_invalid = 0;
    tdkTestObj = obj.createTestStep('HdmicecHal_AddLogicalAddress');
    tdkTestObj.addParameter("logical_addr",logical_addr);
    tdkTestObj.addParameter("Is_handle_invalid",Is_handle_invalid);
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        print("\n",details)
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print("\n",details)

    print("\nTEST STEP2 : Remove the logical address using HdmiCecRemoveLogicalAddress API");
    print("EXPECTED RESULT : Should remove the last added logical address");
    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('HdmicecHal_RemoveLogicalAddress');
    logical_addr = 9;
    print("\nRemoved logical address as %d" %(logical_addr));
    tdkTestObj.addParameter("logical_addr",logical_addr);
    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        print("ACTUAL RESULT  : ",details)
        print("[TEST EXECUTION RESULT] : SUCCESS")
        print("\nTEST STEP3 : Get the logical address using HdmiCecGetLogicalAddress")
        print("EXPECTED OUTPUT : Should get the updated logical address")
        tdkTestObj = obj.createTestStep('HdmicecHal_GetLogicalAddress');
        tdkTestObj.executeTestCase(expectedResult);
        print("After execute testcase")
        actualResult = tdkTestObj.getResult();
        print("actual restlut ", actualResult)
        details = tdkTestObj.getResultDetails();
        print("Get LOG details ", details)
        get_logicalAddress = int(str(details).split(":",1)[1].split(",")[1].split(":")[1].strip())
        if expectedResult in actualResult and get_logicalAddress == cur_logical_addr:
            tdkTestObj.setResultStatus("SUCCESS");
            print("Value Returned : ",details)
            print("ACTUAL RESULT  : Remove logical address operation success")
            print("[TEST EXECUTION RESULT] : SUCCESS")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("Value Returned : ",details)
            print("ACTUAL RESULt: Remove logical address operation failed")
            print("[TEST EXECUTION RESULT]: FAILURE\n")
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print(details)
        print("ACTUAL RESULT: HdmiCecRemoveLogicalAddress call failed")
        print("[TEST EXECUTION RESULT] : FAILURE\n")

    # re-assigned the previous logical address to driver which captured before running the test execution
    logical_addr = cur_logical_addr;
    Is_handle_invalid = 0;
    tdkTestObj = obj.createTestStep('HdmicecHal_AddLogicalAddress');
    tdkTestObj.addParameter("logical_addr",logical_addr);
    tdkTestObj.addParameter("Is_handle_invalid",Is_handle_invalid);
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        print("\n",details)
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print("\n",details)

    obj.unloadModule("hdmicechal");
else:
    print("Load module failed");
    obj.setLoadModuleStatus("FAILURE");
