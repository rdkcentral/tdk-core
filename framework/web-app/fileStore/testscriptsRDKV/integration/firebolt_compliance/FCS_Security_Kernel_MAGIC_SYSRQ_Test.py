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
  <name>FCS_Security_Kernel_MAGIC_SYSRQ_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Script to check the value of sysrq</synopsis>
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
    <test_case_id>FCS_Security_24</test_case_id>
    <test_objective>Script to check the value of sysrq</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator, RPI</test_setup>
    <pre_requisite>/proc/sys/kernel/sysrq should be accessible as read-only</pre_requisite>
    <api_or_interface_used>systemutil</api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>>Check if expected value is coming or not</automation_approch>
    <expected_output>Should getthe value of the SYSRQ in the /proc/sys/kernel/sysrq</expected_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>FCS_Security_Kernel_MAGIC_SYSRQ_Test</test_script>
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
obj = tdklib.TDKScriptingLibrary("systemutil", "1")

# IP and Port of box; these will be replaced with corresponding DUT IP and port while executing script
ip = <ipaddress>  # Replace with DUT IP
port = <port> # Replace with DUT Port
obj.configureTestCase(ip,port,'FCS_Security_Kernel_MAGIC_SYSRQ_Test');

# Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS] :  %s" % result)

# Check if the module is loaded successfully
if "SUCCESS" in result.upper():
    print("\nTEST STEP 1: Check the current value of sysrq")

    # Execute command to get sysrq value
    command = "cat /proc/sys/kernel/sysrq"
    result, details, tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": command}, True)

    if result and details:
        sysrq_value_str = details.strip()  # Get the integer value of sysrq
        sysrq_value_str = sysrq_value_str.replace('\\n', '')

        sysrq_value = int(sysrq_value_str)
        print("Current sysrq value is: %d" % sysrq_value)

        # Interpret the sysrq value
        enabled_commands = []

        if (sysrq_value & 1): enabled_commands.append("Enable Magic all functions of sysrq")
        if (sysrq_value & 2): enabled_commands.append("enable control of console logging level")
        if (sysrq_value & 4): enabled_commands.append("Enable control of keyboard (SAK, unraw)")
        if (sysrq_value & 8): enabled_commands.append("Enable debugging dumps of processes etc.")
        if (sysrq_value & 16): enabled_commands.append("Enable sync command")
        if (sysrq_value & 32): enabled_commands.append("Enable remount read-only")
        if (sysrq_value & 64): enabled_commands.append("Enable signalling of processes (term, kill, oom-kill)")
        if (sysrq_value & 128): enabled_commands.append("Allow reboot/poweroff")
        if (sysrq_value & 256): enabled_commands.append("Allow nicing of all RT tasks")

        if enabled_commands:
            print("The following Magic SysRq commands are enabled:")
            for command in enabled_commands:
                tdkTestObj.setResultStatus("SUCCESS")
                print("SUCCESS : " + command)
        else:
            print("No Magic SysRq commands are currently enabled.")
    else:
        print("Failed to read sysrq value: %s" % details)
        tdkTestObj.setResultStatus("FAILURE")

    # Unload the module
    obj.unloadModule("systemutil")
else:
    print("Module load failed")
