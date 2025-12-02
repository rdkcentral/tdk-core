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
  <name>PackageMgr_DAC_05_UninstallAllApps</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>RdkService_Test</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Uninstall all applications from DAC catalog using Package Manager uninstall API</synopsis>
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
    <test_case_id>TC_PackageMgr_DAC_05</test_case_id>
    <test_objective>Uninstall all applications from DAC catalog and verify cleanup</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK device with PackageManager plugin enabled</test_setup>
    <pre_requisite>1. TDK Agent should be up and running
2. PackageManagerRDKEMS plugin should be activated
3. Applications should be installed (run PackageMgr_DAC_02_InstallAllApps)</pre_requisite>
    <api_or_interface_used>org.rdk.PackageManagerRDKEMS.1.uninstall</api_or_interface_used>
    <input_parameters>packageId</input_parameters>
    <automation_approch>1. List all installed packages from DAC catalog
2. For each installed DAC application, uninstall using PackageManager.uninstall
3. Verify package is removed from installed list
4. Report uninstall success/failure for each application
5. Verify final state - no DAC packages should remain</automation_approch>
    <expected_output>All DAC applications should be uninstalled successfully</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkservicesstub.so</test_stub_interface>
    <test_script>PackageMgr_DAC_05_UninstallAllApps</test_script>
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
    uninstall_package,
    verify_package_installed,
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
configure_test_case_standalone(obj, ip, port, 'PackageMgr_DAC_05_UninstallAllApps')

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
    
    uninstall_results = []
    
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
            print("[WARNING] No DAC applications installed to uninstall")
            obj.setLoadModuleStatus("SUCCESS")
        else:
            # Step 5: Uninstall each application
            print("\n[STEP 5] Uninstalling applications...")
            for idx, pkg in enumerate(dac_installed, 1):
                app_id = pkg.get('packageId')
                dac_app = dac_app_dict.get(app_id, {})
                app_name = dac_app.get('name', 'Unknown')
                
                # Create TDK test step for each uninstall
                tdkTestObj = create_tdk_test_step(obj, f"Step5_Uninstall_{idx}", 
                                                   f"Uninstall {app_name}")
                tdkTestObj.addParameter("app_id", app_id)
                tdkTestObj.addParameter("app_name", app_name)
                
                print(f"\n  [{idx}/{len(dac_installed)}] {app_name} (ID: {app_id})")
                
                try:
                    # Uninstall application
                    uninstall_result = uninstall_package(app_id, jsonrpc_url)
                    print(f"    ✓ Uninstall command sent")
                    
                    # Small delay to allow uninstall to complete
                    time.sleep(2)
                    
                    # Verify package is no longer installed
                    is_still_installed = verify_package_installed(app_id, jsonrpc_url)
                    
                    if not is_still_installed:
                        print(f"    ✓ Package removed successfully")
                        uninstall_results.append({
                            'app_id': app_id,
                            'app_name': app_name,
                            'status': 'SUCCESS'
                        })
                        set_test_step_status(tdkTestObj, "SUCCESS", "Package removed successfully")
                    else:
                        print(f"    ✗ Package still present after uninstall")
                        uninstall_results.append({
                            'app_id': app_id,
                            'app_name': app_name,
                            'status': 'FAILURE',
                            'error': 'Package still present after uninstall'
                        })
                        set_test_step_status(tdkTestObj, "FAILURE", "Package still present after uninstall")
                    
                except Exception as e:
                    print(f"    ✗ Uninstall FAILED: {str(e)}")
                    uninstall_results.append({
                        'app_id': app_id,
                        'app_name': app_name,
                        'status': 'FAILURE',
                        'error': str(e)
                    })
                    set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
            
            # Step 6: Final verification
            tdkTestObj = create_tdk_test_step(obj, "Step6_FinalVerification", 
                                               "Verify all DAC packages removed")
            try:
                print("\n[STEP 6] Final verification...")
                final_installed = list_installed_packages(jsonrpc_url)
                remaining_dac = [pkg for pkg in final_installed if pkg.get('packageId') in dac_app_dict]
                
                print(f"  Remaining DAC applications: {len(remaining_dac)}")
                if remaining_dac:
                    print("  WARNING: The following DAC applications are still installed:")
                    for pkg in remaining_dac:
                        app_id = pkg.get('packageId')
                        dac_app = dac_app_dict.get(app_id, {})
                        print(f"    - {dac_app.get('name', 'Unknown')} ({app_id})")
                    set_test_step_status(tdkTestObj, "FAILURE", f"{len(remaining_dac)} packages still remain")
                else:
                    set_test_step_status(tdkTestObj, "SUCCESS", "All DAC packages removed")
            except Exception as e:
                set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
                raise
            
            # Summary
            print("\n" + "="*80)
            print("UNINSTALL SUMMARY")
            print("="*80)
            
            success_count = sum(1 for r in uninstall_results if r['status'] == 'SUCCESS')
            failure_count = len(uninstall_results) - success_count
            
            print(f"Total Applications: {len(uninstall_results)}")
            print(f"Successful Uninstalls: {success_count}")
            print(f"Failed Uninstalls: {failure_count}")
            print(f"Remaining DAC Packages: {len(remaining_dac)}")
            
            # Detailed results
            if failure_count > 0:
                print("\nFailed Uninstalls:")
                for result in uninstall_results:
                    if result['status'] == 'FAILURE':
                        print(f"  - {result['app_name']} ({result['app_id']}): {result.get('error', 'Unknown error')}")
            
            # Set final status
            if success_count == len(uninstall_results) and len(remaining_dac) == 0:
                print("\n[TEST RESULT] SUCCESS - All applications uninstalled successfully")
                obj.setLoadModuleStatus("SUCCESS")
            elif success_count > 0:
                print("\n[TEST RESULT] PARTIAL SUCCESS - Some applications uninstalled")
                obj.setLoadModuleStatus("SUCCESS")
            else:
                print("\n[TEST RESULT] FAILURE - No applications uninstalled")
                obj.setLoadModuleStatus("FAILURE")
    
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {str(e)}")
        obj.setLoadModuleStatus("FAILURE")
    
    obj.unloadModule("rdkservices")
else:
    print("[ERROR] Failed to load rdkservices module")
    obj.setLoadModuleStatus("FAILURE")
