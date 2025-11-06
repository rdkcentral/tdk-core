##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2023 RDK Management
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
  <name>HWPerformance_glmark2</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SystemUtilAgent_ExecuteBinary</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To obtain the glmark2 using wayland-glesv2 backend by rendering various scenes on the renderer</synopsis>
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
    <box_type>RPI-HYB</box_type>
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
    <test_case_id>TC_HWPerformance_11</test_case_id>
    <test_objective>To obtain the glmark2 using wayland-glesv2 backend by rendering various scenes on the renderer</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Video Accelerator</test_setup>
    <pre_requisite>glmark2 tool must be installed in DUT</pre_requisite>
    <api_or_interface_used>systemutil, glmark2</api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>1. Setup the  graphics test environment using tdk start up file.
    2. Graphics test environment includes stopping wpeframework and starting westeros renderer
    3. Execute glmark2-es2-wayland test binary in DUT
    4. Obtain glmark2 score</automation_approch>
    <expected_output>glmark2 score must be obtained</expected_output>
    <priority>Medium</priority>
    <test_stub_interface>systemutil</test_stub_interface>
    <test_script>HWPerformance_glmark2</test_script>
    <skipped></skipped>
    <release_version>M110</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1");
sysUtilObj.configureTestCase(ip,port,'HWPerformance_glmark2');
sysUtilLoadStatus = sysUtilObj.getLoadModuleResult();
print("System module loading status : %s" %sysUtilLoadStatus);
#Set the module loading status
sysUtilObj.setLoadModuleStatus(sysUtilLoadStatus);

if "SUCCESS" in sysUtilLoadStatus.upper():
    expectedResult="SUCCESS"
    tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand');
    cmd = "command -v glmark2-es2-wayland"
    print(cmd);
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase("SUCCESS");
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails()

    if details:
        print("glmark2 is installed in device\nProceeding with the testcase")
        print("\nTEST STEP NAME: Setup graphics testing environment")
        command = "touch graphics_test; ls graphics_test"
        tdkTestObj.addParameter("command", command)
        tdkTestObj.executeTestCase(expectedResult)
        output = tdkTestObj.getResultDetails()
        if expectedResult in actualresult.upper() and "graphics_test" in output :
            print("Rebooting the device.......")
            sysUtilObj.initiateReboot();

        print("\nTEST STEP NAME: Check if westeros renderer is running")
        cmd = "ps -ef | grep \"westeros --renderer\" | grep -v grep"
        tdkTestObj.addParameter("command", cmd)
        tdkTestObj.executeTestCase(expectedResult)
        output = tdkTestObj.getResultDetails()
        if expectedResult in actualresult.upper() and not output:
            print("westeros renderer is not running\nExiting from testcase")
            tdkTestObj.setResultStatus("FAILURE");

        else:
            print("\nTEST STEP NAME : Run glmark2 test")
            cmd = "glmark2-es2-wayland > glmark2_exec_log ; cat glmark2_exec_log"
            tdkTestObj.addParameter("command", cmd);
            tdkTestObj.executeTestCase("SUCCESS");
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails()
            if "glmark2 Score" in details:
                filepath = tdkTestObj.transferLogs("glmark2_exec_log", "false" );
                try:
                    data = open(filepath,'r');
                    message = data.read()
                    print("\n************** glmark2  Execution Log - Begin**********\n")
                    print(message)
                    print("\n************** glmark2  Execution - End*************\n")
                    data.close()
                    tdkTestObj.setResultStatus("SUCCESS");
                except IOError:
                    print("ERROR : Unable to open execution log file")
                    tdkTestObj.setResultStatus("FAILURE");
            else:
                print("glmark2 score is not obtained")
                tdkTestObj.setResultStatus("FAILURE");

        print("\nTEST STEP NAME: Restore default Environment")
        cmd = "rm graphics_test"
        tdkTestObj.addParameter("command", cmd)
        tdkTestObj.executeTestCase(expectedResult)
        sysUtilObj.initiateReboot();

    else:
        print("glmark2 is not installed in DUT")
        tdkTestObj.setResultStatus("FAILURE");

    sysUtilObj.unloadModule("systemutil");
else:
    print("Module load failed")
