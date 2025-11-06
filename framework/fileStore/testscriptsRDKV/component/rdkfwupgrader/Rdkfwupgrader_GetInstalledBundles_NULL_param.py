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
  <name>Rdkfwupgrader_GetInstalledBundles_NULL_param</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkfwupgrader_GetInstalledBundles</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify the behavior when a NULL parameter is passed in the GetInstalledBundles function.</synopsis>
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
    <test_case_id>RDKFWUPGRADE_114</test_case_id>
    <test_objective>To verify the behavior when a NULL parameter is passed in the GetInstalledBundles function.</test_objective>
    <test_type>Negative</test_type>
    <test_setup>Video Accelerator,RPI</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>GetInstalledBundles</api_or_interface_used>
    <input_parameters>pBundles - pointer to a char buffer to store the output string
    szBufSize - the size of the character buffer in argument 1.</input_parameters>
    <automation_approch>1. TM loads the RDK_fwupgradeAgent.
    2. RDK_fwupgradeAgent will invoke GetInstalledBundles API with the NULL param being passed to pBundles param.
    3. TM will verify the output by having a expected output as invalid param and verify.
    4. TM will return SUCCESS or FAILURE based on the result from the above step.</automation_approch>
    <expected_output>API must do proper NULL check and return the corresponding error code without facing any crash</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkfwupgraderstub.so.0.0.0</test_stub_interface>
    <test_script>Rdkfwupgrader_GetInstalledBundles_NULL_param</test_script>
    <skipped></skipped>
    <release_version>M137</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from RdkfwupgraderTestVariables import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkfwupgrader","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Rdkfwupgrader_GetInstalledBundles_NULL_param');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);

if "SUCCESS" in result.upper():
    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('rdkfwupgrader_GetInstalledBundles');
    tdkTestObj.addParameter("null_param", 1);
    tdkTestObj.addParameter("buffer_size", 50);
    tdkTestObj.executeTestCase("SUCCESS");
    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails().strip().replace(r'\n', '\n');

    print("[Expected Result]: FAILURE");
    print("[Actual Result]: %s" %result);
    
    if result == "FAILURE" and "crash" not in details:
        print("SUCCESS : GetInstalledBundles failed as expected for null param")
        tdkTestObj.setResultStatus("SUCCESS")
    elif "crash" in details:
        print("FAILURE : GetInstalledBundles crashes when called with null param")
        tdkTestObj.setResultStatus("FAILURE")
        obj.initiateReboot();
    else:
        print("FAILURE : GetInstalledBundles is success for null param which is not expected")
        tdkTestObj.setResultStatus("FAILURE")

    obj.unloadModule("rdkfwupgrader");
else:
    print ("LOAD MODULE FAILED")
