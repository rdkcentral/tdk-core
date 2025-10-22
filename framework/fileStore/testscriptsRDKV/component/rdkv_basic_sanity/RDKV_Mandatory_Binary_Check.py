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
  <name>RDKV_Mandatory_Binary_Check</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_basic_sanity_executeInDUT</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Script to check the mandatory binaries are present</synopsis>
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
    <box_type>RDKTV</box_type>
    <!--  -->
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
    <test_case_id>RDKV_Basic_Sanity_14</test_case_id>
    <test_objective>Script to check the mandatory binaries are present</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator, RPI-Client, RDKTV</test_setup>
    <pre_requisite>1. Ensure the shell script and config file is present in the device</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>The files given in the configuration files should be present in the given location</automation_approch>
    <expected_output>All mandatory binaries should be present</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_basic_sanity</test_stub_interface>
    <test_script>RDKV_Mandatory_Binary_Check</test_script>
    <skipped>No</skipped>
    <release_version>M128</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested

obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True);
obj.configureTestCase(ip,port,'RDKV_Mandatory_Binary_Check');
LoadStatus = obj.getLoadModuleResult();
print("System module loading status : %s" %LoadStatus);
#Set the module loading status
obj.setLoadModuleStatus(LoadStatus);

if ("SUCCESS" in LoadStatus.upper()):
    tdkTestObj = obj.createTestStep('rdkv_basic_sanity_executeInDUT')
    command = "cd /opt/TDK; sh system_file_check.sh binary_check"
    print("Executor Command : %s" %command)
    tdkTestObj.addParameter("command",command)
    tdkTestObj.addParameter("fetch_SSH_params",True)
    tdkTestObj.executeTestCase("SUCCESS");
    result = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails().replace(r'\n', '\n');

    print("Details : %s" %details)
    if "RESULT : SUCCESS" in details:
        tdkTestObj.setResultStatus(result);
    else:
        tdkTestObj.setResultStatus("FAILURE");
    print("\n[TEST EXECUTION RESULT] :  %s\n" %result)

else:
    print("System Module Loading Status:FAILURE")

#Unload rdkv_basic_sanity module
obj.unloadModule("rdkv_basic_sanity");
