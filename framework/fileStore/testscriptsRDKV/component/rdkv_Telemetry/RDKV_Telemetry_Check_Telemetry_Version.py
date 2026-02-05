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
  <name>RDKV_Telemetry_Check_Telemetry_Version</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>telemetry_deviceconfig_value</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To verify the telemetry version in DUT</synopsis>
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
    <test_case_id>rdkv_Telemetry_03</test_case_id>
    <test_objective>To verify the telemetry version in DUT</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator, RPI</test_setup>
    <pre_requisite>SSH_METHOD, SSH_USERNAME  and SSH_PASSWORD  must be configured in device config file</pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>1. Obtain telemetry version  using Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.Version via tr181 utility</automation_approch>
    <expected_output>1. Verify Telemetry.Version is as expected.</expected_output>
    <priority>High</priority>
    <test_stub_interface></test_stub_interface>
    <test_script>RDKV_Telemetry_Check_Telemetry_Version</test_script>
    <skipped>No</skipped>
    <release_version>M140</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_telemetry","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Telemetry_Check_Telemetry_Version');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);

if "SUCCESS" in result.upper():
    print("\n[TEST STEP 1] : Check if lighttpd is running")
    tdkTestObj = obj.createTestStep('telemetry_executeCmdInDUT');
    command = "tr181 Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.Version"
    tdkTestObj.addParameter("command", command)
    tdkTestObj.executeTestCase("SUCCESS");
    details = tdkTestObj.getResultDetails()
    print("\n ", details)
    if "2.0" in details:
        print("\nExpected Telemetry version is running in device")
        print("\n[TEST STEP RESULT] : SUCCESS\n");
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        print("Telemetry version is not as expected in device")
        print("\n[TEST STEP RESULT] : FAILURE\n")
        tdkTestObj.setResultStatus("FAILURE");

obj.unloadModule("rdkv_telemetry");
