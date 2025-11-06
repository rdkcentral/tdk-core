##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
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
  <name>Rdkfwupgrader_getJRPCTokenData_NULL_token</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkfwupgrader_getJRPCTokenData</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To try to obtain token from testString via rdkfwupgrader API getJRPCTokenData with NULL token and verify output</synopsis>
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
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKFWUPGRADE_15</test_case_id>
    <test_objective>To try to obtain token from testString via rdkfwupgrader API getJRPCTokenData with NULL token and verify output</test_objective>
    <test_type>Negative</test_type>
    <test_setup>Video Accelerator,RPI</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>getJRPCTokenData</api_or_interface_used>
    <input_parameters>testString</input_parameters>
    <automation_approch>1. TM loads the RDK_fwupgradeAgent via the test agent.
    2. RDK_fwupgradeAgent will invoke getJRPCTokenData API with testString.
    3. TM will verify the output by having a expected output string and cross verify.
    4. TM will return SUCCESS or FAILURE based on the result from the above step.</automation_approch>
    <expected_output>API must FAIL due to NULL token being passed</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkfwupgraderstub.so.0.0.0</test_stub_interface>
    <test_script>Rdkfwupgrader_getJRPCTokenData_NULL_token</test_script>
    <skipped></skipped>
    <release_version>M133</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import sys
from RdkfwupgraderTestVariables import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkfwupgrader","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Rdkfwupgrader_getJRPCTokenData_NULL_token');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);

if "SUCCESS" in result.upper():
    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('rdkfwupgrader_getJRPCTokenData');
    tdkTestObj.addParameter("string", tokenTestString)
    tdkTestObj.addParameter("null_token", 1)
    tdkTestObj.executeTestCase("SUCCESS");
    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails().strip()

    print("\n[RESULT] : %s" %result);
    print("[DETAILS] : %s" %details);

    if result == "FAILURE":
        print ("SUCCESS : Validation success for NULL token");
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        print ("FAILURE : Validation unsuccessfull")
        print ("Expected test Result : getJRPCTokenData must fail due to NULL token")
        print ("Actual test Result : ", details)
        tdkTestObj.setResultStatus("FAILURE")

    obj.unloadModule("rdkfwupgrader");

else:
    print ("LOAD MODULE FAILED")
