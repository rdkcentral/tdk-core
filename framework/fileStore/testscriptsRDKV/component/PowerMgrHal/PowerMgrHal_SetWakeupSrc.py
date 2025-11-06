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
  <name>PowerMgrHal_SetWakeupSrc</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>PowerMgrHal_SetWakeupSrc</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to validate the wakeup source enablement.</synopsis>
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
    <test_case_id>TC_PowerMgrHal_16</test_case_id>
    <test_objective>Test script to set the wakeupsource type using HAL API PLAT_API_SetWakeupSrc</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator</test_setup>
    <pre_requisite>1.TDK agent should be up and running
2.Initialize CPE Power management module.
</pre_requisite>
    <api_or_interface_used> PLAT_API_SetWakeupSrc( PWRMGR_WakeupSrcType_t srcType, bool  enable );</api_or_interface_used>
    <input_parameters> srcType - input source type value
    enable - pass true or false to set the input srcType</input_parameters>
    <automation_approch>1.Load the PowerMgr Hal module
2.Initialise the powerMgr hal module using PLAT_INIT API
3.Invoke PLAT_API_SetWakeupSrc API with the enable/disable state
4.Update test result as SUCCESS/FAILURE if device satisfies expected behavior
5.Unload the module</automation_approch>
    <expected_output>Should set the corresponding state of the input wakeup source type.</expected_output>
    <priority>High</priority>
    <test_stub_interface>libpwrmgrhalstub.so.0.0.0</test_stub_interface>
    <test_script>PowerMgrHal_SetWakeupSrc</test_script>
    <skipped>No</skipped>
    <release_version>M126</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("pwrmgrhal","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'PowerMgrHal_SetWakeupSrc');

#Get the result of connection with test component and STB
loadModuleStatus = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadModuleStatus);

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";

    #to get the current value of wakeup source type before executing the testcase
    wakeup_src = ['VOICE', 'MOTION DETECT', 'BLE', 'WIFI', 'IR', 'POWER KEY', 'TIMER', 'CEC', 'LAN']
    active_state = []
    for i in wakeup_src:
        tdkTestObj = obj.createTestStep('PowerMgrHal_GetWakeupSrc');
        wakeupsrc = i;
        tdkTestObj.addParameter("wakeupsrc", wakeupsrc);
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            print("Value returned  : ",details)
            enable = int(str(details).split(":",1)[1].split(":")[1].strip())
            active_state.append(enable);
            print("[TEST EXECUTION RESULT] : SUCCESS")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("ACTUAL RESULT  : ",details)
            if details.find("PWRMGR_INVALID_ARGUMENT") != -1:
                active_state.append('Not Supported');
            print("[TEST EXECUTION RESULT] : FAILURE\n");

    print("\nList of wakeup source types and its active states b4 executing script: ");
    print(wakeup_src);
    print(active_state);

    print("\nTEST STEP1 : Enable all the wakeup source types using PLAT_API_SetWakeupSrc")
    print("EXPECTED OUTPUT : Should enable all the wakeup source types as 1")
    #Primitive test case which associated to this Script
    active_state1 = [];
    for i in wakeup_src:
        tdkTestObj = obj.createTestStep('PowerMgrHal_SetWakeupSrc');
        wakeupsrc = i;
        tdkTestObj.addParameter("wakeupsrc", wakeupsrc);
        tdkTestObj.addParameter("Is_wkup_src_enable", 1);
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            print("ACTUAL RESULT  : ", details)
            active_state1.append(1);
            print("[TEST EXECUTION RESULT] : SUCCESS")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("ACTUAL RESULT  : ", details)
            if details.find("PWRMGR_INVALID_ARGUMENT") != -1:
                active_state1.append('Not Supported');
            print("[TEST EXECUTION RESULT] : FAILURE\n")

    print("\nTEST STEP2 : Get the values and verify whether it has updated properly or not using PLAT_API_GetWakeupSrc")
    print("EXPECTED OUTPUT : Should get all the wakeup source types as 1")
    active_state2 = []
    for i in wakeup_src:
        tdkTestObj = obj.createTestStep('PowerMgrHal_GetWakeupSrc');
        wakeupsrc = i;
        tdkTestObj.addParameter("wakeupsrc", wakeupsrc);
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            print("Value returned  : ", details)
            enable = int(str(details).split(":", 1)[1].split(":")[1].strip())
            active_state2.append(enable);
            print("[TEST EXECUTION RESULT] : SUCCESS")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("ACTUAL RESULT  : ", details)
            if details.find("PWRMGR_INVALID_ARGUMENT") != -1:
                active_state2.append('Not Supported');
            print("[TEST EXECUTION RESULT] : FAILURE\n");

    if active_state2 == active_state1:
        tdkTestObj.setResultStatus("SUCCESS");
        print("\nBoth Set & Get values are equal");
        print("[TEST EXECUTION RESULT] : SUCCESS")
    else:
        tdkTestObj.setResultStatus("FAILURE");
        print("\nBoth Set & Get values are not equal");
        print("[TEST EXECUTION RESULT] : FAILURE\n");

    # reverting with the very first values of wakeup source type before executing the testscript
    state_inc = 0;
    for i in wakeup_src:
        tdkTestObj = obj.createTestStep('PowerMgrHal_SetWakeupSrc');
        wakeupsrc = i;
        Is_wkup_src_enable = active_state[state_inc];
        if Is_wkup_src_enable == 'Not Supported':
            print("\nNot supported wakeup source: ", i);
            Is_wkup_src_enable = 0;
        tdkTestObj.addParameter("wakeupsrc", wakeupsrc);
        tdkTestObj.addParameter("Is_wkup_src_enable", Is_wkup_src_enable);
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            print("\nReverted successfully to the default wakeup source type's active status")
            print("ACTUAL RESULT  : ", details)
            print("[TEST EXECUTION RESULT] : SUCCESS")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("ACTUAL RESULT  : ", details)
            print("[TEST EXECUTION RESULT] : FAILURE\n")
        state_inc += 1;

    # to get the reverted value of wakeup source types after executing the testcase for checking
    active_state = [];
    for i in wakeup_src:
        tdkTestObj = obj.createTestStep('PowerMgrHal_GetWakeupSrc');
        wakeupsrc = i;
        tdkTestObj.addParameter("wakeupsrc", wakeupsrc);
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            print("Value returned  : ", details)
            enable = int(str(details).split(":", 1)[1].split(":")[1].strip())
            active_state.append(enable);
            print("[TEST EXECUTION RESULT] : SUCCESS")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("ACTUAL RESULT  : ", details)
            if details.find("PWRMGR_INVALID_ARGUMENT") != -1:
                active_state.append('Not Supported');
            print("[TEST EXECUTION RESULT] : FAILURE\n");

    print("\nList of wakeup source types and its active states after executing script: ");
    print(wakeup_src);
    print(active_state);

    obj.unloadModule("pwrmgrhal");
else:
    print("Load module failed");
    obj.setLoadModuleStatus("FAILURE");
