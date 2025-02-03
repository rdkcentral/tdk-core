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
  <name>Rdkfwupgrader_mergeLists_NULL_list</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkfwupgrader_mergeLists</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To merge two metaDataList with passing NULL list via rdkfwupgrader API mergeLists and verify output</synopsis>
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
    <test_case_id>RDKFWUPGRADE_22</test_case_id>
    <test_objective>To merge two metaDataList with passing NULL list via rdkfwupgrader API mergeLists and verify output</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator,RPI</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>mergeLists</api_or_interface_used>
    <input_parameters>testString</input_parameters>
    <automation_approch>1. TM loads the RDK_fwupgradeAgent via the test agent.
    2. RDK_fwupgradeAgent will invoke mergeLists API with test metaDataLists.
    3. Three iteration of testing will be done :
         i) Setting list-1 as NULL
         ii) Setting list-2 as NULL
         iii) Setting both lists as NULL
    4. TM will verify the output by having a expected output list and cross verify.
    5. TM will return SUCCESS or FAILURE based on the result from the above step.</automation_approch>
    <expected_output>API must return merged list as expected</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkfwupgraderstub.so.0.0.0</test_stub_interface>
    <test_script>Rdkfwupgrader_mergeLists_NULL_list</test_script>
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
obj.configureTestCase(ip,port,'Rdkfwupgrader_mergeLists_NULL_list');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);

if "SUCCESS" in result.upper():
    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('rdkfwupgrader_mergeLists');
    for i in range(0,3):
        if i == 0:
            print("Setting list 1 as NULL")
            tdkTestObj.addParameter("null_list1", 1);
            tdkTestObj.addParameter("null_list2", 0);
            list1 = ""
        elif i == 1:
            print("Setting list 2 as NULL")
            tdkTestObj.addParameter("null_list1", 0);
            tdkTestObj.addParameter("null_list2", 1);
            list2 = ""
        else:
            print("Setting both lists as NULL")
            tdkTestObj.addParameter("null_list1", 1);
            tdkTestObj.addParameter("null_list2", 1);
            list1 = ""
            list2 = ""
        tdkTestObj.addParameter("list1", list1)
        tdkTestObj.addParameter("list2", list2)
        tdkTestObj.executeTestCase("SUCCESS");
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails().strip().replace(r'\n', '\n')

        print("\n[RESULT] : %s" %result);
        print("[DETAILS] : \n%s" %details);

        mergedList = list1 + " " + list2
        mergedList = mergedList.split()

        if set(details.splitlines())  == set(mergedList):
            print("SUCCESS : mergeLists returns expected result")
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print("FAILURE : mergeLists not returning expected result")
            print("Expected Result : ", str(set(mergedList)))
            print("Actual Result : ", str(set(details.splitlines())))
            tdkTestObj.setResultStatus("FAILURE")
    obj.unloadModule("rdkfwupgrader");

else:
    print ("LOAD MODULE FAILED")
