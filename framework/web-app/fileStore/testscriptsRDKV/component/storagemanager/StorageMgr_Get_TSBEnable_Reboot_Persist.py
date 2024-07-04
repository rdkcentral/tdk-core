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
  <name>StorageMgr_Get_TSBEnable_Reboot_Persist</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SetTSBEnabled</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test Script to check whether TSB is enable or not after reboot</synopsis>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_StorageMgr_10</test_case_id>
    <test_objective>Test Script to check whether TSB is enable or not after reboot</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator, RDKTV</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>isTSBEnabled,setTSBEnabled</api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>1.Load storagemanager module.
2.Invoke setTSBEnabled Api and set it as disable
3.Invoke isTSBEnabled API and check whether its disabled or not 
4.After that device will goin for reboot
5.After the reboot again invoke the isTSBEnabled API and verify TSB is Enabled or not</automation_approch>
    <expected_output>Should return TSB as enabled after reboot</expected_output>
    <priority></priority>
    <test_stub_interface>libstoragemanagerstub.so.0.0.0</test_stub_interface>
    <test_script>StorageMgr_Get_TSBEnable_Reboot_Persist</test_script>
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
isEnabled=0;
obj.configureTestCase(ip,port,'StorageMgr_Get_TSBEnable_Reboot_Persist');

#Get the result of connection with test component and DUT
loadModuleStatus = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadModuleStatus);

if "SUCCESS" in loadModuleStatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedResult="SUCCESS";


    tdkTestObj = obj.createTestStep('SetTSBEnabled');
    print("\nSet TSB as %d" %(isEnabled));
    tdkTestObj.addParameter("isEnabled",isEnabled);
    tdkTestObj.executeTestCase(expectedResult);
    actualResult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();

    if expectedResult in actualResult:
        tdkTestObj.setResultStatus("SUCCESS");
        print("\nTEST STEP : Setting TSB disabled or not using rdkStorage_setTSBEnabled API ")
        print("EXPECTED OUTPUT : Should get TSB as disabled")

        tdkTestObj = obj.createTestStep('IsTSBEnabled');
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        print("Is TSB Enabled = ",details)

        if expectedResult in actualResult and "false" in details:
            tdkTestObj.setResultStatus("SUCCESS");
            print("ACTUAL RESULT : Setting TSB as disable was success")
            obj.initiateReboot();
            
            tdkTestObj.executeTestCase(expectedResult);
            actualResult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            print("Is TSB Enabled = ",details)

            if expectedResult in actualResult and "true" in details:
                tdkTestObj.setResultStatus("SUCCESS");
                print("ACTUAL RESULT : TSB is enabled after reboot was success")
                print("[TEST EXECUTION RESULT] : SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("ACTUAL RESULt: TSB enable was failed after reboot")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("ACTUAL RESULt: TSB disable was failed")
    else:
            tdkTestObj.setResultStatus("FAILURE");
            print("Value Returned : ",details)
            print("ACTUAL RESULt: Setting TSB as enable was failed")
            print("[TEST EXECUTION RESULT]: FAILURE\n")

    obj.unloadModule("storagemanager");

else:
    print("Load module failed");
    obj.setLoadModuleStatus("FAILURE");


