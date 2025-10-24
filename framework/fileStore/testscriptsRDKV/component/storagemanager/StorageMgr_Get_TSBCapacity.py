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
  <name>StorageMgr_Get_TSBCapacity</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>GetTSBStatus</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to get the capacity of the TSB</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>1</execution_time>
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
    <box_type>RDKTV</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_StorageMgr_03</test_case_id>
    <test_objective>Test Script to get the capacity of the TSB</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator, RDKTV</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>rdkStorage_getTSBCapacity</api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>1.Load storagemanager module.
2.Invoke getTSBCapacity API
3.Should return the capacity of the TSB</automation_approch>
    <expected_output>Should return TSB capacity</expected_output>
    <priority>High</priority>
    <test_stub_interface>libstoragemanagerstub.so.0.0.0</test_stub_interface>
    <test_script></test_script>
    <skipped>No</skipped>
    <release_version>M125</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("storagemanager","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'StorageMgr_Get_TSBCapacity');


#Get the result of connection with test component and DUT
loadModuleStatus = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadModuleStatus);

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";

    print("\nTEST STEP : Get the TSB Status using rdkStorage_getTSBCapacity API")
    print("EXPECTED RESULT : Should return capacity of the TSB")

    tdkTestObj = obj.createTestStep('GetTSBCapacity');
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult and int(details) != 0:
        tdkTestObj.setResultStatus("SUCCESS");
        print("TSB Capacity : ",details)
        print("[TEST EXECUTION RESULT] : SUCCESS\n")
        print("ACTUAL RESULT: StorageMgr_GetTSBCapacity call was success")
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print("TSB Capacity : ",details)
        print("ACTUAL RESULT: StorageMgr_GetTSBCapacity call failed")
        print("[TEST EXECUTION RESULT] : FAILURE\n")

    obj.unloadModule("storagemanager");

else:
    print("Load module failed");
    obj.setLoadModuleStatus("FAILURE");


