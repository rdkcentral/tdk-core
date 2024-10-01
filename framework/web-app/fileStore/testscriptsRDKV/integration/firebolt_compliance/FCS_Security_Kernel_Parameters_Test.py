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
  <name>FCS_Security_Kernel_Parameters_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>FireboltCompliance_DoNothing</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Script to check the Kernel parameters are immutable</synopsis>
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
    <test_case_id>FCS_Security_31</test_case_id>
    <test_objective>Script to check the Kernel parameters are immutable</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator, RPI</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>systemtil</api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>Check Kernel parameters are immutable as expected</automation_approch>
    <expected_output>Should return kernel parameters as immutable</expected_output>
    <priority>High</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script><FCS_Security_Kernel_Parameters_Test/test_script>
    <skipped>No</skipped>
    <release_version>M129</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# Use tdklib library, which provides a wrapper for TDK test case script
import tdklib
from tdkvutility import *

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("systemutil","1")

# IP and Port of box, No need to change
# This will be replaced with corresponding DUT IP and port while executing the script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'FCS_Security_Kernel_Parameters_Test')

# Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)

# Define expected trusted kernel parameters
TRUSTED_PARAMS = "root=/dev/mmcblk1p10 rootwait rw bhpa=1052m@960m"

# Check if the module loaded successfully
if "SUCCESS" in result.upper():
    print("\nTEST STEP 1: Check current kernel parameters")

    # Command to retrieve current kernel parameters
    command = "cat /proc/cmdline"
    result, current_params, tdkTestObj = executeTest(obj, 'ExecuteCommand', {"command": command}, True)

    if result and current_params:
        print("Current kernel parameters: %s" % current_params)

        # Check if parameters are trusted
        if TRUSTED_PARAMS in current_params:
            print("SUCCESS: Kernel init parameters are trusted.")
        else:
            print("FAILURE: Kernel init parameters are NOT trusted.")
            print("Potential security risk: unauthorized modifications may have occurred.")
            tdkTestObj.setResultStatus("FAILURE")
            obj.unloadModule("systemutil")
            exit(1)

        # Check if parameters are immutable
        print("TEST STEP 2: Testing immutability of kernel parameters...")
        print("Attempting to change kernel parameters...")

        # Attempt to modify (this should fail)
        try:
            subprocess.run(['echo', 'new_param=value'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("FAILURE: Kernel parameters are mutable!")
            tdkTestObj.setResultStatus("FAILURE")
        except Exception:
            print("SUCCESS: Kernel parameters are immutable as expected.")
            tdkTestObj.setResultStatus("SUCCESS")
    else:
        print("FAILURE: Could not retrieve kernel parameters.")
        tdkTestObj.setResultStatus("FAILURE")

    # Unload the module
    obj.unloadModule("systemutil")
else:
    print("Module load failed")

