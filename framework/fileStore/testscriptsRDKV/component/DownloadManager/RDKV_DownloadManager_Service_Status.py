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
  <version>1</version>
  <name>RDKV_DownloadManager_Service_Status</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>downloadmanager_statuscheck</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test DownloadManager service status and plugin availability</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks></remarks>
  <skip>false</skip>
  <box_types>
    <box_type>RDKTV</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DOWNLOADMANAGER_002</test_case_id>
    <test_objective>Verify DownloadManager service status and plugin availability</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK</test_setup>
    <pre_requisite>
      1. Thunder framework should be running
      2. DownloadManager plugin should be available
    </pre_requisite>
    <api_or_interface_used>Controller.1.status, org.rdk.DownloadManager</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>
      1. Check Thunder Controller status
      2. Check DownloadManager plugin availability
      3. Verify plugin state and configuration
    </automation_approch>
    <expected_output>DownloadManager plugin should be available and responsive</expected_output>
    <priority>High</priority>
    <test_stub_interface>DownloadManager</test_stub_interface>
    <test_script>RDKV_DownloadManager_Service_Status</test_script>
    <skipped>No</skipped>
    <release_version>M100</release_version>
    <remarks>None</remarks>
  </test_cases>
  <script_tags/>
</xml>
'''

# Import necessary libraries

import tdklib
from ai2_0_utils import (
  safe_unload_module,
  thunder_is_plugin_active,
)

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("DownloadManager", "1", standAlone=True)

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip, port, 'RDKV_DownloadManager_Service_Status')

# Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)

expectedResult = "SUCCESS"
finalStatus = "FAILURE"
finalOutput = ""

if "SUCCESS" in result.upper():
    # Step 1: Check Download Manager active status using device IP JSON-RPC
    print("\n[STEP] Checking Download Manager plugin active status...")
    try:
        if thunder_is_plugin_active("org.rdk.DownloadManager", jsonrpc_url=f"http://{ip}:9998/jsonrpc"):
            print("[SUCCESS] Download Manager plugin is active")
            finalStatus = "SUCCESS"
            finalOutput = "DownloadManager plugin is active and responsive"
        else:
            print("[FAILURE] Download Manager plugin is not active")
            finalStatus = "FAILURE"
            finalOutput = "DownloadManager plugin is not active"
    except Exception as e:
        print(f"[ERROR] Status check failed: {e}")
        finalStatus = "FAILURE"
        finalOutput = f"Error checking plugin status: {str(e)}"
else:
    print("FAILURE : Module Loading Status Failure")
    finalStatus = "FAILURE"
    finalOutput = "Module loading failed"

obj.setLoadModuleStatus(finalStatus)
obj.addTestcaseResult("DownloadManager_StatusCheck", finalStatus, finalOutput)

# unload module
safe_unload_module(obj, "DownloadManager")
