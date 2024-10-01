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
  <name>FCS_Security_Check_Kernel_KALLSYMS</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Check all the configurations for KALLSYMS are enabled or not</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <box_type>Video_Accelerator</box_type>
    <box_type>RPI-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>FCS_Security_20</test_case_id>
    <test_objective>Check all the configurations for KALLSYMS are enabled or not</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator, RPI</test_setup>
    <pre_requisite>Security test shell script must be installed in the device</pre_requisite>
    <api_or_interface_used>systemutil</api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>Check if expected KALLYSMS configurations are enabled by extracting the /proc/config.gz file.</automation_approch>
    <expected_output>Expected KALLYSMS configurations must be enabled</expected_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Security_Check_Kernel_KALLSYMS</test_script>
    <skipped>No</skipped>
    <release_version>M129</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# Use tdklib library, which provides a wrapper for TDK test case script
import tdklib
import os
from tdkvutility import *

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","1")

# IP and Port of box, No need to change
# This will be replaced with corresponding DUT IP and port while executing the script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'FCS_Security_Check_Kernel_KALLSYMS')

# Get the result of connection with the test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)

#Path to be extracted
filePath = "/tmp"
#Shell Script path
shellScript = "SecurityTestTDK.sh "

testOption = "CHECK_KALLSYMS " 
# Assuming your shell script accepts this option

if "SUCCESS" in result.upper():
    print("\nTEST STEP 1: Check if /proc/config.gz is present")
    result, details, tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": "ls /proc/config.gz"}, True)

    if result and details:
        print("SUCCESS: Kernel config file (/proc/config.gz) is present")

        # Execute shell script to check CONFIG_KALLSYMS status
        command = "sh SecurityTestTDK.sh CHECK_KALLSYMS /tmp"
        result, details, tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": command}, True)

        if not details:
            print(f"Parsing shell script {shellScript} is not present in DUT")
            tdkTestObj.setResultStatus("FAILURE")
        else:
            # Execute shell script
            print("TEST STEP 2: Check if expected KALLSYMS configuration is enabled or not")
            command = f"sh {shellScript} {testOption} {filePath}"
            result, details, tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": command}, True)

            if "Extracted config file could not be found" in details:
                print(details)
                tdkTestObj.setResultStatus("FAILURE")
            elif details:
                # Check if any config is enabled
                config_found = False
                for line in details.splitlines():
                    if "is enabled" in line:
                        print(f"{line}.")
                        print("KALLSYMS Config is enabled as expected")
                        tdkTestObj.setResultStatus("SUCCESS")
                        config_found = True
                        break  # Exit after the first enabled config is found
                    if not config_found:
                        print("KALLSYMS Config is disabled")
                        tdkTestObj.setResultStatus("FAILURE")
            else:
                print("No output from the shell script execution.")
                tdkTestObj.setResultStatus("FAILURE")

    else:
        print("FAILURE: Kernel config file (/proc/config.gz) is not present")
        tdkTestObj.setResultStatus("FAILURE")

    # Unload the module
    obj.unloadModule("systemutil")

else:
    print("Module load failed")


