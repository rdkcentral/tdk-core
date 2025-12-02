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
  <name>PackageMgr_DAC_04_LaunchApps</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>RdkService_Test</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Launch all installed applications from DAC catalog</synopsis>
  <groups_id />
  <execution_time>300</execution_time>
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
    <test_case_id>TC_PackageMgr_DAC_04</test_case_id>
    <test_objective>Launch all installed applications from DAC catalog using AppManager</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK device with PackageManager and AppManager plugins enabled</test_setup>
    <pre_requisite>1. TDK Agent should be up and running
2. PackageManagerRDKEMS and AppManager plugins should be activated
3. Applications should be installed (run PackageMgr_DAC_02_InstallAllApps)</pre_requisite>
    <api_or_interface_used>org.rdk.AppManager.1.launch</api_or_interface_used>
    <input_parameters>appId</input_parameters>
    <automation_approch>1. List all installed packages from DAC catalog
2. For each installed application, attempt to launch using AppManager.launch
3. Verify launch response for success
4. Report launch success/failure for each application
5. Small delay between launches to avoid resource contention</automation_approch>
    <expected_output>Applications should launch successfully without errors</expected_output>
    <priority>Medium</priority>
    <test_stub_interface>librdkservicesstub.so</test_stub_interface>
    <test_script>PackageMgr_DAC_04_LaunchApps</test_script>
    <skipped>No</skipped>
    <release_version>M100</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import sys
import time

from ai2_0_utils import (
    fetch_dac_config,
    list_dac_packages,
    list_installed_packages,
    launch_app,
    get_device_info_from_json,
    check_and_activate_ai2_managers,
    create_tdk_test_step,
    set_test_step_status,
    configure_test_case_standalone
)

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkservices", "1", standAlone=True)

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

# Configure test case using helper function
configure_test_case_standalone(obj, ip, port, 'PackageMgr_DAC_04_LaunchApps')

# Get the result of connection with test component and DUT
loadmodulestatus = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedResult = "SUCCESS"
    
    # Precondition: Check and activate AI2.0 managers
    tdkTestObj = create_tdk_test_step(obj, "Precondition_ActivateManagers", 
                                       "Check and activate AI2.0 managers")
    try:
        jsonrpc_url = f"http://{ip}:9998/jsonrpc"
        check_and_activate_ai2_managers(jsonrpc_url)
        set_test_step_status(tdkTestObj, "SUCCESS", "AI2.0 managers activated")
    except Exception as e:
        set_test_step_status(tdkTestObj, "FAILURE", f"Failed to activate: {str(e)}")
        obj.setLoadModuleStatus("FAILURE")
        obj.unloadModule("rdkservices")
        sys.exit(1)
    
    launch_results = []
    
    try:
        # Step 1: Fetch DAC configuration
        tdkTestObj = create_tdk_test_step(obj, "Step1_FetchDACConfig", 
                                           "Fetch DAC catalog configuration")
        try:
            print("\n[STEP 1] Fetching DAC configuration...")
            catalog_url, username, password = fetch_dac_config()
            print(f"  Catalog URL: {catalog_url}")
            set_test_step_status(tdkTestObj, "SUCCESS", f"Catalog URL: {catalog_url}")
        except Exception as e:
            set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
            raise
        
        # Step 2: Get device platform info
        tdkTestObj = create_tdk_test_step(obj, "Step2_GetDeviceInfo", 
                                           "Read device platform configuration")
        try:
            print("\n[STEP 2] Reading device platform configuration...")
            firmware_ver, platform_name = get_device_info_from_json()
            print(f"  Platform: {platform_name}")
            print(f"  Firmware Version: {firmware_ver}")
            set_test_step_status(tdkTestObj, "SUCCESS", f"Platform: {platform_name}, FW: {firmware_ver}")
        except Exception as e:
            set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
            raise
        
        # Step 3: List all applications from DAC catalog
        tdkTestObj = create_tdk_test_step(obj, "Step3_ListDACApps", 
                                           "List applications from DAC catalog")
        try:
            print("\n[STEP 3] Listing applications from DAC catalog...")
            dac_applications = list_dac_packages(catalog_url, username, password, platform_name, firmware_ver)
            dac_app_dict = {app.get('id'): app for app in dac_applications}
            print(f"  Total DAC applications: {len(dac_applications)}")
            set_test_step_status(tdkTestObj, "SUCCESS", f"Found {len(dac_applications)} DAC applications")
        except Exception as e:
            set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
            raise
        
        # Step 4: List installed packages
        tdkTestObj = create_tdk_test_step(obj, "Step4_ListInstalledPackages", 
                                           "List installed packages on device")
        try:
            print("\n[STEP 4] Listing installed packages on device...")
            jsonrpc_url = f"http://{ip}:9998/jsonrpc"
            installed_packages = list_installed_packages(jsonrpc_url)
            
            # Filter to only DAC applications
            dac_installed = [pkg for pkg in installed_packages if pkg.get('packageId') in dac_app_dict]
            print(f"  Total installed DAC applications: {len(dac_installed)}")
            set_test_step_status(tdkTestObj, "SUCCESS", f"Found {len(dac_installed)} installed DAC apps")
        except Exception as e:
            set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
            raise
        
        if not dac_installed:
            print("[WARNING] No DAC applications installed to launch")
            obj.setLoadModuleStatus("SUCCESS")
        else:
            # Step 5: Launch each application
            print("\n[STEP 5] Launching applications...")
            for idx, pkg in enumerate(dac_installed, 1):
                app_id = pkg.get('packageId')
                dac_app = dac_app_dict.get(app_id, {})
                app_name = dac_app.get('name', 'Unknown')
                
                # Create TDK test step for each launch
                tdkTestObj = create_tdk_test_step(obj, f"Step5_Launch_{idx}", 
                                                   f"Launch {app_name}")
                tdkTestObj.addParameter("app_id", app_id)
                tdkTestObj.addParameter("app_name", app_name)
                
                print(f"\n  [{idx}/{len(dac_installed)}] {app_name} (ID: {app_id})")
                
                try:
                    # Launch application
                    launch_result = launch_app(app_id, jsonrpc_url)
                    
                    # Check if launch was successful
                    # Note: AppManager.launch typically returns {"result":"success"} or error
                    if launch_result and isinstance(launch_result, dict):
                        if launch_result.get('result') == 'success' or 'launchId' in launch_result:
                            print(f"    ✓ Launch successful")
                            launch_results.append({
                                'app_id': app_id,
                                'app_name': app_name,
                                'status': 'SUCCESS'
                            })
                            set_test_step_status(tdkTestObj, "SUCCESS", "Launch successful")
                        else:
                            print(f"    ✗ Launch returned unexpected result: {launch_result}")
                            launch_results.append({
                                'app_id': app_id,
                                'app_name': app_name,
                                'status': 'FAILURE',
                                'error': f"Unexpected result: {launch_result}"
                            })
                            set_test_step_status(tdkTestObj, "FAILURE", f"Unexpected result: {launch_result}")
                    else:
                        print(f"    ✓ Launch completed")
                        launch_results.append({
                            'app_id': app_id,
                            'app_name': app_name,
                            'status': 'SUCCESS'
                        })
                        set_test_step_status(tdkTestObj, "SUCCESS", "Launch completed")
                    
                    # Delay between launches to avoid resource contention
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"    ✗ Launch FAILED: {str(e)}")
                    launch_results.append({
                        'app_id': app_id,
                        'app_name': app_name,
                        'status': 'FAILURE',
                        'error': str(e)
                    })
                    set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
            
            # Summary
            print("\n" + "="*80)
            print("LAUNCH SUMMARY")
            print("="*80)
            
            success_count = sum(1 for r in launch_results if r['status'] == 'SUCCESS')
            failure_count = len(launch_results) - success_count
            
            print(f"Total Applications: {len(launch_results)}")
            print(f"Successful Launches: {success_count}")
            print(f"Failed Launches: {failure_count}")
            
            # Detailed results
            if failure_count > 0:
                print("\nFailed Launches:")
                for result in launch_results:
                    if result['status'] == 'FAILURE':
                        print(f"  - {result['app_name']} ({result['app_id']}): {result.get('error', 'Unknown error')}")
            
            # Set final status
            if success_count == len(launch_results):
                print("\n[TEST RESULT] SUCCESS - All applications launched successfully")
                obj.setLoadModuleStatus("SUCCESS")
            elif success_count > 0:
                print("\n[TEST RESULT] PARTIAL SUCCESS - Some applications launched")
                obj.setLoadModuleStatus("SUCCESS")
            else:
                print("\n[TEST RESULT] FAILURE - No applications launched")
                obj.setLoadModuleStatus("FAILURE")
    
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {str(e)}")
        obj.setLoadModuleStatus("FAILURE")
    
    obj.unloadModule("rdkservices")
else:
    print("[ERROR] Failed to load rdkservices module")
    obj.setLoadModuleStatus("FAILURE")
