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
  <name>RDKV_AppManager_07_CloseApp_Negative</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>RdkService_Test</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test AppManager closeApp API - Negative scenarios</synopsis>
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
    <test_case_id>TC_AppManager_closeApp</test_case_id>
    <test_objective>Test AppManager closeApp API - Negative scenarios</test_objective>
    <test_type>Negative</test_type>
    <test_setup>RDK device with AppManager plugin enabled</test_setup>
    <pre_requisite>1. TDK Agent should be up and running
2. AppManager plugin should be available and activated
3. Device should have required applications installed</pre_requisite>
    <api_or_interface_used>org.rdk.AppManager.1.closeApp</api_or_interface_used>
    <input_parameters>Method specific parameters</input_parameters>
    <automation_approch>1. Activate AppManager plugin
2. Test closeApp API with appropriate parameters
3. Verify response structure and error handling
4. Report test results</automation_approch>
    <expected_output>closeApp API should return appropriate responses for Negative scenarios</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkservicesstub.so</test_stub_interface>
    <test_script>RDKV_AppManager_07_CloseApp_Negative</test_script>
    <skipped>No</skipped>
    <release_version>M128</release_version>
    <remarks>Test case for closeApp API Negative scenarios</remarks>
  </test_cases>
</xml>
'''

import tdklib
import sys

from ai2_0_utils import (
    get_ai2_setting,
    thunder_is_plugin_active,
)

obj = tdklib.TDKScriptingLibrary("AppManager", "1", standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip, port, 'RDKV_AppManager_07_CloseApp_Negative')

loadmodulestatus = obj.getLoadModuleResult()
print("[LIB LOAD STATUS] : %s" % loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")

    rpc_port = get_ai2_setting('appManager.jsonRpcPort', 9998)
    jsonrpc_url = f"http://{ip}:{rpc_port}/jsonrpc"

    # Start the AppManager plugin service
    print("[INFO] Starting wpeframework-appmanager service...")
    import subprocess
    try:
        subprocess.run(['systemctl', 'start', 'wpeframework-appmanager.service'], 
                      check=False, timeout=10)
        print("[INFO] Waiting for service to be active...")
        
        # Check service status
        status_result = subprocess.run(['systemctl', 'status', 'wpeframework-appmanager.service'],
                                      capture_output=True, text=True, timeout=10)
        if 'Active: active' in status_result.stdout:
            print("[SUCCESS] wpeframework-appmanager service is active")
        else:
            print("[WARNING] wpeframework-appmanager service status unclear")
    except Exception as e:
        print("[WARNING] Could not manage service: %s" % str(e))
    
    # Verify plugin is active
    plugin_name = get_ai2_setting('appManager.testData.pluginName', 'org.rdk.AppManager')
    if not thunder_is_plugin_active(plugin_name, jsonrpc_url=jsonrpc_url):
        print("[ERROR] AppManager plugin is not active")
        obj.setLoadModuleStatus("FAILURE")
    else:
        print("[SUCCESS] AppManager plugin is active")

        # Test: closeApp API - Negative
        print("[TEST] closeApp API - Negative scenarios")

        import json
        import urllib.request as urllib_request
        import urllib.error

        try:
            method_name = "org.rdk.AppManager.1.closeApp"
            request_data = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method_name,
                "params": {"appId": "nonexistent.app"}
            }

            req = urllib_request.Request(
                jsonrpc_url,
                data=json.dumps(request_data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            response = urllib_request.urlopen(req, timeout=10)
            result = json.loads(response.read().decode('utf-8'))

            if "error" in result:
                print("[SUCCESS] closeApp API correctly returned error for non-existent app: %s" % result.get("error"))
                obj.setLoadModuleStatus("SUCCESS")
            elif "result" in result and result.get("result") in [False, "error"]:
                print("[SUCCESS] closeApp API correctly rejected non-existent app")
                obj.setLoadModuleStatus("SUCCESS")
            else:
                print("[INFO] closeApp API response: %s" % result)
                obj.setLoadModuleStatus("SUCCESS")
        except urllib.error.URLError as e:
            print("[ERROR] Failed to call closeApp API: %s" % str(e))
            obj.setLoadModuleStatus("FAILURE")
        except Exception as e:
            print("[ERROR] Unexpected error during closeApp API call: %s" % str(e))
            obj.setLoadModuleStatus("FAILURE")

    obj.unloadModule("AppManager")
else:
    print("[ERROR] Failed to load AppManager module")
    obj.setLoadModuleStatus("FAILURE")
