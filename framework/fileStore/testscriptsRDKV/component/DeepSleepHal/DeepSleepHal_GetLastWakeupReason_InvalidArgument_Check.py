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
  <name>DeepSleepHal_GetLastWakeupReason_InvalidArgument_Check</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>DeepSleepHal_GetLastWakeupReason</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to check the GetLastWakeupReason API with the NULL param for negative case checks.</synopsis>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_DeepSleepHal_03</test_case_id>
    <test_objective>Test script to verify HAL API PLAT_DS_GetLastWakeupReason with the invalid argument</test_objective>
    <test_type>Negative</test_type>
    <test_setup>Video_Accelerator</test_setup>
    <pre_requisite>1.TDK agent should be up and running
2.Initialize DeepSleep management module.
</pre_requisite>
    <api_or_interface_used> PLAT_DS_GetLastWakeupReason(DeepSleep_WakeupReason_t *wakeupReason)</api_or_interface_used>
    <input_parameters>*wakeupReason - pointer variable to retrieve the wakeup reason value</input_parameters>
    <automation_approch>1.Load the deep sleep hal module
2.Initialise the deep sleep module using PLAT_DS_INIT API
3.Invoke PLAT_DS_GetLastWakeupReason API by passing a NULL param.
4.Update test result as SUCCESS/FAILURE if device satisfies expected behavior
5.Unload the module</automation_approch>
    <expected_output>Driver should handle the NULL check and return the correpsonding error.</expected_output>
    <priority>High</priority>
    <test_stub_interface>libdeepsleephalstub.so.0.0.0</test_stub_interface>
    <test_script>DeepSleepHal_GetLastWakeupReason_InvalidArgument_Check</test_script>
    <skipped>No</skipped>
    <release_version>M126</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("deepsleephal","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'DeepSleepHal_GetLastWakeupReason_InvalidArgument_Check');

#Get the result of connection with test component and DUT
loadModuleStatus = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadModuleStatus);

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";

    #Prmitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('DeepSleepHal_GetLastWakeupReason');

    #Adding the corresponding param values
    Is_null_param_check = 1;
    tdkTestObj.addParameter("Is_null_param_check", Is_null_param_check);

    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedResult);

    #Get the result of execution
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("FAILURE");
        print(details)
        print("ACTUAL RESULT: DeepSleepHal_GetLastWakeupReason call getting succeeded eventhough with the NULL params being passed")
        print("[TEST EXECUTION RESULT]: FAILURE\n")
    else:
        tdkTestObj.setResultStatus("SUCCESS");
        print(details)
        print("ACTUAL RESULT: DeepSleepHal_GetLastWakeupReason call failed as expected for invalid argument")
        print("[TEST EXECUTION RESULT]: SUCCESS\n")

    obj.unloadModule("deepsleephal");
else:
    print("Load module failed");
    obj.setLoadModuleStatus("FAILURE");
