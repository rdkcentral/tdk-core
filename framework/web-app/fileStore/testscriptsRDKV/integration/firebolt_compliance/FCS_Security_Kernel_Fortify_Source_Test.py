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
  <name>FCS_Security_Kernel_Fortify_Source_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Script to check the CPU load, boot up time, kernel binary size and all</synopsis>
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
    <test_case_id>FCS_Security_27</test_case_id>
    <test_objective>Script to check the CPU load, boot up time, kernel binary size and all</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator, RPI</test_setup>
    <pre_requisite>Security test shell script must be installed in the device</pre_requisite>
    <api_or_interface_used>systemutil</api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>Check the CPU load, boot up time, kernel binary size and all</automation_approch>
    <expected_output>Should return the CPU load memory , boot up time and kernel binary size</expected_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Security_Kernel_Fortify_Source_Test</test_script>
    <skipped>No</skipped>
    <release_version>M129</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# Use tdklib library, which provides a wrapper for TDK testcase script
import tdklib
from tdkvutility import *

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","1")

# IP and Port of box; replace with DUT IP and port while executing script
ip = <ipaddress>  # Replace with DUT IP
port = <port>  # Replace with DUT Port
obj.configureTestCase(ip,port,'FCS_Security_Kernel_Fortify_Source_Test')

# Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS] :  %s" % result)

if "SUCCESS" in result.upper():
    print("\nTEST STEP 1: Measure boot time")
    command = "uptime"  # Change to your boot measurement command
    result, details, tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": command}, True)


    if result and details:
        print(f"Boot time details: {details.strip()}")
        print(details)
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        print("Failed to measure boot time.")
        tdkTestObj.setResultStatus("FAILURE")

    # TEST STEP 2: Measure process load time
    print("\nTEST STEP 2: Measure process load time")
    process_command = "echo Hello, World!"  # Replace with actual process command
    result, details, tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": process_command}, True)

    if result and details:
        print(f"Process load time for '{process_command}': {details}")
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        print("Failed to measure process load time.")
        tdkTestObj.setResultStatus("FAILURE")

    # TEST STEP 3: Monitor CPU and memory load
    print("\nTEST STEP 3: Monitor CPU and memory usage")
    command = "top -b -n 1 | head -n 10"  # Adjust for a single snapshot of CPU/memory
    result, details, tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": command}, True)

    if result and details:
        print("CPU and Memory Usage:")
        print(details)
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        print("Failed to retrieve CPU and memory usage.")
        tdkTestObj.setResultStatus("FAILURE")

    # TEST STEP 4: Check kernel binary size
    print("\nTEST STEP 4: Check kernel binary size")
    kernel_path = "/boot"  
    command = f"du -h {kernel_path}"
    result, details, tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": command}, True)
    if result and details:
        binary_value_str = details.strip()
        binary_value_str = binary_value_str.replace('\\t/boot\\n', '')
        # Check if the size has a suffix and convert accordingly
        if 'M' in binary_value_str:
            binary_value = float(binary_value_str[:-1]) * 1024 * 1024  # Convert MB to bytes
        elif 'K' in binary_value_str:
            binary_value = float(binary_value_str[:-1]) * 1024 # Convert KB to bytes
        elif 'G' in binary_value_str:
            binary_value = float(binary_value_str[:-1]) * 1024 * 1024 * 1024  # Convert GB to bytes
        else:
            binary_value = float(binary_value_str)

        print(f"Kernel binary size in bytes: {binary_value}")
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        print("Failed to retrieve kernel binary size.")
        tdkTestObj.setResultStatus("FAILURE")


else:
    print("Module load failed")

# Unload the module
obj.unloadModule("systemutil")
