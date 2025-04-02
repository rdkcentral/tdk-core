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
  <name>Rdkfwupgrader_GetModelNum</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkfwupgrader_GetModelNum</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify the retrieval of the model number of the device</synopsis>
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
    <test_case_id>RDKFWUPGRADE_64</test_case_id>
    <test_objective>To verify the retrieval of the model number of the device</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator,RPI</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>GetModelNum</api_or_interface_used>
    <input_parameters>pModelNum - pointer to a char buffer to store the output string.
    szBufSize - the size of the character buffer in argument 1.</input_parameters>
    <automation_approch>1. TM loads the RDK_fwupgradeAgent.
    2. RDK_fwupgradeAgent will invoke GetModelNum API with the valid buffer size along with pointer variable to hold the model number of the device.
    3. TM will verify the output by having a expected output string and cross verify.
    4. TM will return SUCCESS or FAILURE based on the result from the above step.</automation_approch>
    <expected_output>API must return OsClass of the device</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkfwupgraderstub.so.0.0.0</test_stub_interface>
    <test_script>Rdkfwupgrader_GetModelNum</test_script>
    <skipped></skipped>
    <release_version>M135</release_version>
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
obj.configureTestCase(ip,port,'Rdkfwupgrader_GetModelNum');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);

if "SUCCESS" in result.upper():
    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('rdkfwupgrader_GetModelNum');
    tdkTestObj.addParameter("buffer_size", 25);
    tdkTestObj.executeTestCase("SUCCESS");
    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails().strip().replace(r'\n', '\n');

    print("[RESULT] : %s" %result);
    print("[DETAILS] : \n%s" %details);
    
    if result == "SUCCESS":
        if not details:
            print("Retrieved empty model number field. Should return the proper model number of the device.");
            tdkTestObj.setResultStatus("FAILURE");
        else:
            print("Successfully returns the device's model number");
            tdkTestObj.setResultStatus("SUCCESS");
    else:
        print ("FAILURE : GetModelNum failed");
        tdkTestObj.setResultStatus("FAILURE");

    obj.unloadModule("rdkfwupgrader");
else:
    print ("LOAD MODULE FAILED")
