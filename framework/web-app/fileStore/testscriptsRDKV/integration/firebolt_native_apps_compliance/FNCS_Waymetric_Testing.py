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
  <name>FNCS_Waymetric_Testing</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>executeCmndInDUT</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To execute waymetric application for measuring the impact of Wayland (Display Server) as compared to rendering directly with EGL on graphics performance</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
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
  <rdk_versions />
  <test_cases>
    <test_case_id>FNCS_GRAPHICS_04</test_case_id>
    <test_objective>To execute waymetric application for measuring the impact of Wayland (Display Server) as compared to rendering directly with EGL on graphics performance</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK TV,Video Accelerator, RPI</test_setup>
    <pre_requisite>waymetric binary should be available in the device</pre_requisite>
    <api_or_interface_used>Execute the waymetric application in DUT</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1.Execute the RunGraphicsTDK.sh script which executes "waymetric" application in DUT.
2.Verify application is executed successfully, obtain the speed indices from the waymetric test report.
3.Upon successfull retriving all speed indices, TM will set the execution as SUCCESS.</automation_approch>
    <expected_output>speed indices must be successfully obtained</expected_output>
    <priority>High</priority>
    <test_stub_interface>waymetric</test_stub_interface>
    <test_script>FNCS_Waymetric_Testing</test_script>
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
obj.configureTestCase(ip,port,'FNCS_Waymetric_Testing');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
expectedResult="SUCCESS"

if "SUCCESS" in result.upper():

    tdkTestObj = obj.createTestStep('executeCmndInDUT')
    command = "cd /opt/TDK ; sh RunGraphicsTDKTest.sh Waymetric"
    print("Executing command in DUT: ", command)
    tdkTestObj.addParameter("command",command)
    tdkTestObj.executeTestCase(expectedResult);

    output = tdkTestObj.getResultDetails()
    if not output:
        print ("FAILURE : No output was obtained from test")
        tdkTestObj.setResultStatus("FAILURE")
    else:
        tdkTestObj.setResultStatus("SUCCESS")

        tdkTestObj = obj.createTestStep('ParseGraphicsOutput')
        tdkTestObj.addParameter("graphics_output",output)
        tdkTestObj.addParameter("test_app","Waymetric")
        tdkTestObj.executeTestCase(expectedResult);
        output = tdkTestObj.getResultDetails()
        tdkTestObj.setResultStatus(output)

obj.unloadModule("firebolt_native_apps_compliance");
