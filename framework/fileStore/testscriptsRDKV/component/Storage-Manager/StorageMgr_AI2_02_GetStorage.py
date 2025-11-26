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
  <name>StorageMgr_AI2_02_GetStorage</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>RdkService_Test</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Get storage information for applications using Storage Manager getStorage API</synopsis>
  <groups_id />
  <execution_time>120</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks></remarks>
  <skip>false</skip>
  <box_types>
    <box_type>RDKTV</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_StorageMgr_AI2_02</test_case_id>
    <test_objective>Get storage information for applications using Storage Manager</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK device with Storage Manager plugin enabled</test_setup>
    <pre_requisite>1. TDK Agent should be up and running
2. Storage Manager plugin should be activated</pre_requisite>
    <api_or_interface_used>org.rdk.StorageManager.getStorage</api_or_interface_used>
    <input_parameters>appId, userId, groupId</input_parameters>
    <automation_approch>1. Activate Storage Manager plugin
2. Create storage for test applications
3. Get storage information for created apps
4. Verify path, size, and used space are returned
5. Cleanup created storage</automation_approch>
    <expected_output>Storage information should be retrieved successfully</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkservicesstub.so</test_stub_interface>
    <test_script>StorageMgr_AI2_02_GetStorage</test_script>
    <skipped>No</skipped>
    <release_version>M100</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
from ai2_0_utils import (
    check_and_activate_ai2_managers,
    create_tdk_test_step,
    set_test_step_status,
    jsonrpc_call,
    fetch_dac_config,
    list_dac_packages,
    get_device_info_from_json
)

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkservices", "1", standAlone=True)

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip, port, 'StorageMgr_AI2_02_GetStorage')

# Get the result of connection with test component and DUT
loadmodulestatus = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedResult = "SUCCESS"
    
    test_results = []
    created_apps = []  # Track created storage for cleanup
    
    try:
        # PRECONDITION: Check and activate Storage Manager
        jsonrpc_url = f"http://{ip}:9998/jsonrpc"
        
        tdkTestObj = create_tdk_test_step(obj, "Precondition_Check", "Activate Storage Manager plugin")
        print("\n" + "="*80)
        print("PRECONDITION: Checking Storage Manager Plugin")
        print("="*80)
        
        # Check if Storage Manager is activated
        try:
            status_result = jsonrpc_call("Controller.1.status@org.rdk.StorageManager", {}, jsonrpc_url)
            current_state = status_result.get('result', [{}])[0].get('state', 'unknown')
            print(f"Storage Manager state: {current_state}")
            
            if current_state != 'activated':
                print("Activating Storage Manager...")
                activate_result = jsonrpc_call("Controller.1.activate", {"callsign": "org.rdk.StorageManager"}, jsonrpc_url)
                import time
                time.sleep(2)
                print("✓ Storage Manager activated")
            else:
                print("✓ Storage Manager already activated")
            
            set_test_step_status(tdkTestObj, "SUCCESS", "Storage Manager is active")
        except Exception as e:
            print(f"✗ Error with Storage Manager: {str(e)}")
            set_test_step_status(tdkTestObj, "FAILURE", f"Storage Manager activation failed: {str(e)}")
            raise
        
        # STEP 1: Fetch DAC applications
        print("\n" + "="*80)
        print("STEP 1: Fetching Applications from DAC")
        print("="*80)
        
        # Get device info and fetch DAC apps
        try:
            firmware_ver, platform_name = get_device_info_from_json()
            print(f"Device Info: Platform={platform_name}, Firmware={firmware_ver}")
        except Exception as e:
            firmware_ver = "1.0.0"
            platform_name = "rpi4"
        
        catalog_url, username, password = fetch_dac_config()
        dac_apps = list_dac_packages(catalog_url, username, password, platform_name, firmware_ver)
        
        if not dac_apps:
            raise Exception("No DAC applications available")
        
        # Select first 2 apps for testing
        test_apps = []
        for idx, app in enumerate(dac_apps[:2]):
            app_id = app.get('id', app.get('appId', ''))
            size = app.get('size', 15360)
            if isinstance(size, str):
                size = 15360
            test_apps.append({
                'appId': app_id,
                'size': size,
                'userId': 1000 + idx,
                'groupId': 1000 + idx,
                'name': app.get('name', app_id)
            })
        
        print(f"Selected {len(test_apps)} applications for testing")
        
        # STEP 2: Create storage for applications
        print("\n" + "="*80)
        print("STEP 2: Creating Storage for Applications")
        print("="*80)
        
        for idx, app_data in enumerate(test_apps, 1):
            app_id = app_data['appId']
            size = app_data['size']
            app_name = app_data['name']
            
            print(f"\n[{idx}/{len(test_apps)}] Creating storage for {app_name} ({app_id})...")
            
            try:
                params = {'appId': app_id, 'size': size}
                result = jsonrpc_call("org.rdk.StorageManager.createStorage", params, jsonrpc_url)
                path = result.get('result', {}).get('path', '')
                
                if path:
                    print(f"  ✓ Storage created at: {path}")
                    created_apps.append(app_id)
                else:
                    print(f"  ✗ Storage creation failed")
                    
            except Exception as e:
                print(f"  ✗ Exception: {str(e)}")
        
        import time
        time.sleep(2)  # Wait for storage to be ready
        
        # STEP 3: Get storage information
        print("\n" + "="*80)
        print("STEP 3: Getting Storage Information")
        print("="*80)
        
        for idx, app_data in enumerate(test_apps, 1):
            app_id = app_data['appId']
            user_id = app_data['userId']
            group_id = app_data['groupId']
            
            print(f"\n[{idx}/{len(test_apps)}] Getting storage for {app_id}...")
            
            tdkTestObj = create_tdk_test_step(obj, f"GetStorage_{app_id}", f"Get storage info for {app_id}")
            
            try:
                # Call getStorage
                params = {
                    'appId': app_id,
                    'userId': user_id,
                    'groupId': group_id
                }
                
                result = jsonrpc_call("org.rdk.StorageManager.getStorage", params, jsonrpc_url)
                
                # Extract response
                response = result.get('result', {})
                path = response.get('path', '')
                size = response.get('size', 0)
                used = response.get('used', 0)
                
                print(f"  Response:")
                print(f"    Path: {path}")
                print(f"    Size: {size} KB")
                print(f"    Used: {used} KB")
                
                # Verify success
                if path and size > 0:
                    print(f"  ✓ Storage info retrieved successfully")
                    test_results.append({
                        'appId': app_id,
                        'status': 'SUCCESS',
                        'path': path,
                        'size': size,
                        'used': used
                    })
                    set_test_step_status(tdkTestObj, "SUCCESS", f"Storage info retrieved: path={path}, size={size}KB, used={used}KB")
                else:
                    print(f"  ✗ Storage info retrieval failed")
                    test_results.append({
                        'appId': app_id,
                        'status': 'FAILURE',
                        'error': 'Invalid response'
                    })
                    set_test_step_status(tdkTestObj, "FAILURE", "getStorage returned invalid data")
                    
            except Exception as e:
                print(f"  ✗ Exception: {str(e)}")
                test_results.append({
                    'appId': app_id,
                    'status': 'FAILURE',
                    'error': str(e)
                })
                set_test_step_status(tdkTestObj, "FAILURE", f"Exception: {str(e)}")
        
        # POSTCONDITION: Cleanup created storage
        print("\n" + "="*80)
        print("POSTCONDITION: Cleaning up created storage")
        print("="*80)
        
        for app_id in created_apps:
            print(f"  Deleting storage for {app_id}...")
            try:
                delete_result = jsonrpc_call("org.rdk.StorageManager.deleteStorage", {'appId': app_id}, jsonrpc_url)
                error = delete_result.get('result', {}).get('error', '')
                if not error:
                    print(f"    ✓ Deleted successfully")
                else:
                    print(f"    ✗ Delete failed: {error}")
            except Exception as e:
                print(f"    ✗ Delete error: {str(e)}")
        
        # Summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        success_count = sum(1 for r in test_results if r['status'] == 'SUCCESS')
        failure_count = sum(1 for r in test_results if r['status'] == 'FAILURE')
        
        print(f"Total Tests: {len(test_results)}")
        print(f"Success: {success_count}")
        print(f"Failure: {failure_count}")
        
        if failure_count == 0:
            print("\n✅ ALL TESTS PASSED")
            obj.setLoadModuleStatus("SUCCESS")
        else:
            print("\n❌ SOME TESTS FAILED")
            obj.setLoadModuleStatus("FAILURE")
        
        print("="*80)
        
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {str(e)}")
        obj.setLoadModuleStatus("FAILURE")
        
        # Attempt cleanup even on failure
        if created_apps:
            print("\nAttempting cleanup...")
            for app_id in created_apps:
                try:
                    jsonrpc_call("org.rdk.StorageManager.deleteStorage", {'appId': app_id}, jsonrpc_url)
                except:
                    pass
    
    obj.unloadModule("rdkservices")
else:
    print("Failed to load rdkservices module")
    obj.setLoadModuleStatus("FAILURE")
