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
  <name>FCS_Security_Kernel_Physical_Space_Access_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test if access for kernel physical filesystem and address space access is removed from the system</synopsis>
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
    <test_case_id>FCS_Security_30</test_case_id>
    <test_objective>Test if access for kernel physical filesystem and address space access is removed from the system</test_objective>
    <test_type>Video_Accelerator</test_type>
    <test_setup>Video Accelerator, RPI</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>systemutil</api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>Check if kernel address space access is removed by verifying "mem" file is not present in /dev or /proc directories.</automation_approch>
    <expected_output>kcore or mem files must not be present in /proc/ or /dev directories</expected_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Security_Kernel_Physical_Space_Access_Test</test_script>
    <skipped>No</skipped>
    <release_version>M129</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library, which provides a wrapper for tdk testcase script
import tdklib
from tdkvutility import *

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","1")

# IP and Port of box, No need to change,
# This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'FCS_Security_Kernel_Physical_Space_Access_Test')

# Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)

# Path to be extracted
filePath = "/tmp"
# Shell Script path
shellScript = "SecurityTestTDK.sh "
# Test option
testOption = "check_DEVMEM_CONFIG "

# Test component to be tested
if "SUCCESS" in result.upper():
    # Step 1: Check if access to the physical address space of kernel is removed
    print("\nTEST STEP 1: Check if access to the physical address space of kernel is removed")
    print("\nEXPECTED OUTPUT: /proc/mem or /dev/mem files must not be present")
    result, details, tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": "find /dev -iname mem"}, True)

    if details:
        print("FAILURE: mem file is present")
        print("This provides access to the physical address space of the operating system kernel, excluding memory that is associated with an I/O device.\nSupport for /dev/mem MUST be removed.")
        tdkTestObj.setResultStatus("FAILURE")
    else:
        print("SUCCESS: mem file is not present")
        tdkTestObj.setResultStatus("SUCCESS")

    # Step 2: Check if /proc/config.gz is present
    print("\nTEST STEP 2: Check if /proc/config.gz is present")
    result, details, tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": "ls /proc/config.gz"}, True)
    if result and details:
        print("SUCCESS: Kernel config file (/proc/config.gz) is present")

        # Check if parsing shell script is present
        command = "ls " + shellScript
        result, details, tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": command}, True)

        if not details:
            print("FAILURE: Parsing shell script %s is not present in DUT" % (shellScript))
            tdkTestObj.setResultStatus("FAILURE")
        else:
            # Execute shell script to check the required configurations
            print("TEST STEP 3: Check if required kernel configurations for /dev/mem are set correctly")
            command = "sh " + shellScript + testOption + filePath
            result, details, tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": command}, True)

            if "Extracted config file could not be found" in details:
                print(details)
                tdkTestObj.setResultStatus("FAILURE")
            elif details:

                # Expected configs and their status
                configs_to_check = {
                    "CONFIG_DEVMEM": "not set",
                    "CONFIG_STRICT_DEVMEM": "enabled",
                    "CONFIG_IO_STRICT_DEVMEM": "enabled",
                    "CONFIG_DEVKMEM": "not set"
                }

                # Extract and parse the shell script output
                output_lines = details.splitlines()
                test_failed = False

                # Loop through the configurations and check their status
                for config, expected_status in configs_to_check.items():
                    found_line = next((line for line in output_lines if config in line), None)

                    if not found_line:
                        print(f"{config} not found in the output")
                        test_failed = True
                    elif expected_status in found_line:
                        print(f"{config} is {expected_status} as expected.")
                    else:
                        print(f"{config} is not {expected_status}.")
                        test_failed = True

                # Set final result status based on the checks
                if test_failed:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("Configurations are not configured as expected")
                else:
                    print("All Configurations are configured as expected")
                    tdkTestObj.setResultStatus("SUCCESS")

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
             
