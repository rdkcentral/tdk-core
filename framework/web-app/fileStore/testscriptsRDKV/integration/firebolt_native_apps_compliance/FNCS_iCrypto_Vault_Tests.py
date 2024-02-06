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
  <name>FNCS_iCrypto_Vault_Tests</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>executeCmndInDUT</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test to execute the iCrypto Vault Import/Export Operation and Set/Get operations and verify the results</synopsis>
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
    <test_case_id>FNCS_ICRYPTO_02</test_case_id>
    <test_objective>Test to execute the iCrypto Vault Import/Export Operation and Set/Get operations and verify the results</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK TV,Video Accelerator, RPI</test_setup>
    <pre_requisite>The iCrypto interface test binary should be available in the device</pre_requisite>
    <api_or_interface_used>Execute the cgfacetests application in DUT</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Execute the Vault Interface tests in DUT. During the execution, the DUT will execute all the tests available in iCrypto interface tests suite.
2.During the execution, the DUT will Import a test_Vector and the id returned by Import will be used to Export the data and the verification based on Import Input and Export Output.
3.Vault Set/Get operation performs a similar operation with test_Vector  being passed to vault_Set and the id being used to retrieve the test_Vector back using vault_Get.
4.Verify the output from the execute command and check if the string "0 FAILED" exists in the returned output
5.Based on the ExecuteCommand() return value and the output returned from the Vault tests of "cgfacetests" application, TM return SUCCESS/FAILURE status.</automation_approch>
    <expected_output>Checkpoint 1. Verify the API call is success
Checkpoint 2. Verify that the output of Vault Tests returned from cgfacetests contains the strings "TOTAL:" and "0 FAILED"</expected_output>
    <priority>High</priority>
    <test_stub_interface>firebolt_compliance_native_apps</test_stub_interface>
    <test_script>FNCS_iCrypto_Vault_Tests</test_script>
    <skipped>No</skipped>
    <release_version>M121</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("firebolt_native_apps_compliance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'FNCS_iCrypto_Vault_Tests');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
expectedResult="SUCCESS"
failed = False;

if "SUCCESS" in result.upper():
    tdkTestObj = obj.createTestStep('executeCmndInDUT')
    testModule = "Vault"
    #Define Module Tests
    Tests = {"Vault":[" Vault::ImportExport", " Vault::SetGet"]}
    test_Names = Tests[testModule]
    if len(test_Names) > 1:
        test_Name_End = str(test_Names[-1]);
    else:
        test_Name_End = str(test_Names[0])
    test_Name_First = str(test_Names[0]);


    command = "cgfacetests | awk '/" + test_Name_First + "/,/" + test_Name_End + " -/'"
    tdkTestObj.addParameter("command",command)
    tdkTestObj.executeTestCase(expectedResult);

    output = tdkTestObj.getResultDetails()
    print("OUTPUT: ...\n", output)

    if "command not found" in output:
        print ("FAILURE : Test application not installed in DUT")
        tdkTestObj.setResultStatus("FAILURE")
        failed = True

    test_result_string = [line for line in output.splitlines() if "PASSED" in line]
    for line in test_result_string:
        if "0 FAILED" not in line and not failed:
            print ("FAILURE : Observed failures in Vault test execution");
            tdkTestObj.setResultStatus("FAILURE")
    if not failed:
        print ("SUCCESS : Vault test execution was successfull, no failures observed")
        tdkTestObj.setResultStatus("SUCCESS")

obj.unloadModule("firebolt_native_apps_compliance");

