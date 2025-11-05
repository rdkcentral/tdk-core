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
  <name>Rdkfwupgrader_mergeLists_duplicate_elements</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkfwupgrader_mergeLists</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To merge two metaDataList with duplicate elements via rdkfwupgrader API mergeLists and verify output</synopsis>
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
    <test_case_id>RDKFWUPGRADE_23</test_case_id>
    <test_objective>To merge two metaDataList with duplicate elements via rdkfwupgrader API mergeLists and verify output</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator,RPI</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>mergeLists</api_or_interface_used>
    <input_parameters>testString</input_parameters>
    <automation_approch>1. TM loads the RDK_fwupgradeAgent via the test agent.
    2. RDK_fwupgradeAgent will invoke mergeLists API with test metaDataLists - both list1 and list2 will be the same lists.
    3. TM will verify the output by having a expected output list and cross verify.
    4. TM will return SUCCESS or FAILURE based on the result from the above step.</automation_approch>
    <expected_output>API must return merged list as expected</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkfwupgraderstub.so.0.0.0</test_stub_interface>
    <test_script>Rdkfwupgrader_mergeLists_duplicate_elements</test_script>
    <skipped></skipped>
    <release_version>M133</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import sys
from collections import Counter

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkfwupgrader","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Rdkfwupgrader_mergeLists_duplicate_elements');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);

def find_and_print_duplicates(input_list):
    counter = Counter(input_list)
    # Find duplicates
    duplicates = [item for item, count in counter.items() if count > 1]
    if duplicates:
        print("\nERROR : Duplicates found:", duplicates)
        return True
    else:
        print("No duplicates found")
        return False

if "SUCCESS" in result.upper():
    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('rdkfwupgrader_mergeLists');
    #Send same list twice
    List1 = " ca-store-update-bundle_package.json ca-store-update-bundle_2.0_package.json "
    List2 = " ca-store-update-bundle_package.json lxyupdate-bundle_package.json"
    tdkTestObj.addParameter("list1", List1)
    tdkTestObj.addParameter("list2", List2)
    tdkTestObj.executeTestCase("SUCCESS");
    #Get the result of execution
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails().strip().replace(r'\n', '\n')

    print("\nInput List 1 : \n%s" %str(List1.split()))
    print("\nInput List 2 : \n%s" %str(List2.split()))
    print("\nMERGED List : \n%s" %str(details.splitlines()))

    mergedList = list(set((List1 + List2).split()))

    if set(details.splitlines())  == set(mergedList) and len(mergedList) == len(details.splitlines()):
        print("SUCCESS : mergeLists returns expected result")
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        find_and_print_duplicates(details.splitlines())
        print("\nFAILURE : mergeLists not returning expected result")
        tdkTestObj.setResultStatus("FAILURE")
    obj.unloadModule("rdkfwupgrader");

else:
    print ("LOAD MODULE FAILED")
