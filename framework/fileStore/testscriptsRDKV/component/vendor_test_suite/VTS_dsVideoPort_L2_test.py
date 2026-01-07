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
  <name>VTS_dsVideoPort_L2_test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>setVTSResult</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Execute VTS dsVideoPort L2 testcases</synopsis>
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
    <test_case_id>VTS_Test_06</test_case_id>
    <test_objective>Execute VTS dsVideoPort L2 testcases</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator, RPI</test_setup>
    <pre_requisite>VTS binaries must be installed in DUT</pre_requisite>
    <api_or_interface_used>hal_test</api_or_interface_used>
    <input_parameters>dsVideoPort config yaml</input_parameters>
    <automation_approch>1. TDK TM will start a session into the DUT
    2. TM will start the hal_test binary along with yaml config and fetch the number of testcases.
    3. TM will execute all the testcases iteratively one by one and note down the results.
    4. TM will parse the results and set the script status as SUCCESS/FAILURE.</automation_approch>
    <expected_output>All testcases must succeed without any errors </expected_output>
    <priority>High</priority>
    <test_stub_interface>vendor_test_suitelib</test_stub_interface>
    <test_script>VTS_dsVideoPort_L2_test</test_script>
    <skipped></skipped>
    <release_version>M134</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from VTSTestVariables import * 
from vendor_test_suitelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("vendor_test_suite","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'VTS_dsVideoPort_L2_test');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);

if "SUCCESS" in result.upper():
    tdkTestObj = obj.createTestStep('getDeviceConfigValues')
    tdkTestObj.addParameter("configKey", "SSHParams")
    tdkTestObj.executeTestCase("SUCCESS")
    actualresult = tdkTestObj.getResult();
    ssh_params = tdkTestObj.getResultDetails().strip().split()
    tdkTestObj.setResultStatus("SUCCESS")
    username = ssh_params[0]
    password = ssh_params[1]

    #Set module
    module = "L2 dsVideoPort - Source"
    print("Module : ",module)
    #Set binary name
    binaryName = DeviceSettings_binaryName
    print ("BinaryName : ",binaryName)
    #Set TestCase Config
    binaryConfig = VideoPort_binaryConfig
    print("BinaryConfig : ",binaryConfig)
    #Set Custom List of TestCases
    testCaseList = VideoPort_L2_List
    #Set basepath of test
    basePath = VTS_Binary_basePath + DeviceSettings_basePath
    #SkipTestCaseList
    SkipTestCaseList = VideoPort_L2_SkipTestCaseList
    boxtype = obj.getDeviceBoxType();
    if (boxtype == "RPI-Client"):
        SkipTestCaseList = VideoPort_L2_SkipTestCaseList_RPI

    #Configuring plugin name
    plugin_name = "dsVideoPort L2"

    testList = SetupPreRequisites(str(ip), username, password, basePath, binaryName, binaryConfig, module, True)

    try:
        if testList:
            print("\n####################################################################################")
            print("            PLUGIN NAME :  ",plugin_name)
            print("####################################################################################")

            binaryPath = "cd " + basePath + " ; ./" + binaryName + " -p " + binaryConfig
            print("BinaryPath : ",binaryPath)
            executionSummary = runTest(binaryPath, module, plugin_name, testList, testCaseList, SkipTestCaseList)
    
            executePostRequisites()

            failed_testCases = printTestSummary(executionSummary, plugin_name)
        else:
            print("ERROR : NO TESTS FOUND")
            failed_testCases = "ERROR"
    except:
        failed_testCases = "ERROR"
    
    tdkTestObj = obj.createTestStep('setVTSResult')
    tdkTestObj.addParameter("failed_testCases", failed_testCases)
    tdkTestObj.executeTestCase("SUCCESS")
    status = tdkTestObj.getResultDetails()
    tdkTestObj.setResultStatus(status)

    obj.unloadModule("vendor_test_suite");
else:
    print ("MODULE LOAD FAILURE")
