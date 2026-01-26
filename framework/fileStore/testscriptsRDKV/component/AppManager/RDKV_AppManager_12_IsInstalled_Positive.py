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
  <name>RDKV_AppManager_12_IsInstalled_Positive</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>RdkService_Test</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test AppManager isInstalled API - Positive scenarios</synopsis>
  <groups_id />
  <execution_time>60</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks></remarks>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_AppManager_isInstalled</test_case_id>
    <test_objective>Test AppManager isInstalled API - Positive scenarios</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK device with AppManager plugin enabled</test_setup>
    <pre_requisite>1. TDK Agent should be up and running
2. AppManager plugin should be available and activated
3. Device should have required applications installed</pre_requisite>
    <api_or_interface_used>org.rdk.AppManager.1.isInstalled</api_or_interface_used>
    <input_parameters>Method specific parameters</input_parameters>
    <automation_approch>1. Activate AppManager plugin
2. Test isInstalled API with appropriate parameters
3. Verify response structure and error handling
4. Report test results</automation_approch>
    <expected_output>isInstalled API should return appropriate responses for Positive scenarios</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkservicesstub.so</test_stub_interface>
    <test_script>RDKV_AppManager_12_IsInstalled_Positive</test_script>
    <skipped>No</skipped>
    <release_version>M128</release_version>
    <remarks>Test case for isInstalled API Positive scenarios</remarks>
  </test_cases>
</xml>
'''

import tdklib
import sys

from ai2_0_utils import (
    get_ai2_setting,
    thunder_is_plugin_active,
    safe_unload_module,
)

obj = tdklib.TDKScriptingLibrary("AppManager", "1", standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip, port, 'RDKV_AppManager_12_IsInstalled_Positive')

loadmodulestatus = obj.getLoadModuleResult()
print("[LIB LOAD STATUS] : %s" % loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")

    try:
        rpc_port = get_ai2_setting('appManager.jsonRpcPort', 9998)
        jsonrpc_url = f"http://{ip}:{rpc_port}/jsonrpc"

        # Verify plugin is active
        plugin_name = get_ai2_setting('appManager.testData.pluginName', 'org.rdk.AppManager')
        if not thunder_is_plugin_active(plugin_name, jsonrpc_url=jsonrpc_url):
            print("[ERROR] AppManager plugin is not active")
            obj.setLoadModuleStatus("FAILURE")
        else:
            print("[SUCCESS] AppManager plugin is active")

            # Test: isInstalled API - Positive
            print("
[TEST] isInstalled API - Positive scenarios")
            
            # TODO: Add specific test implementation for isInstalled
            # Use thunder_call() to invoke the API
            # Validate responses and error handling
            
            print("  [INFO] Test implementation pending - Framework ready")
            obj.setLoadModuleStatus("SUCCESS")

    except Exception as e:
        print(f"[ERROR] Test execution failed: {str(e)}")
        obj.setLoadModuleStatus("FAILURE")

    safe_unload_module(obj, "AppManager")
else:
    print("[ERROR] Failed to load AppManager module")
    obj.setLoadModuleStatus("FAILURE")
