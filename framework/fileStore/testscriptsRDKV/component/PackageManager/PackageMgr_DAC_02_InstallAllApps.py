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
  <name>PackageMgr_DAC_02_InstallAllApps</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>RdkService_Test</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Install all applications from DAC catalog using Package Manager install API</synopsis>
  <groups_id />
  <execution_time>600</execution_time>
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
    <test_case_id>TC_PackageMgr_DAC_02</test_case_id>
    <test_objective>Install all applications from DAC catalog after downloading</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK device with PackageManager plugin enabled</test_setup>
    <pre_requisite>1. Thunder interface should be available
2. PackageManagerRDKEMS plugin should be available
3. Applications should be downloaded first (run PackageMgr_DAC_01_DownloadAllApps)
4. Sufficient storage space available</pre_requisite>
    <api_or_interface_used>org.rdk.PackageManagerRDKEMS.1.install</api_or_interface_used>
    <input_parameters>packageId, version, fileLocator, additionalMetadata</input_parameters>
    <automation_approch>1. Fetch DAC catalog configuration and list applications
2. Download all applications from catalog
3. For each downloaded application, install using PackageManager.install API
4. Provide file locator based on download ID (/opt/CDL/package{downloadId})
5. Include additional metadata (appName, category, type)
6. Verify installation success for each application</automation_approch>
    <expected_output>Each application should install successfully</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkservicesstub.so</test_stub_interface>
    <test_script>PackageMgr_DAC_02_InstallAllApps</test_script>
    <skipped>No</skipped>
    <release_version>M100</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import time

from ai2_0_utils import (
    fetch_dac_config,
    list_dac_packages,
    build_download_url,
    thunder_download_package,
    thunder_install_package,
    build_additional_metadata,
    get_device_info_from_json,
    check_and_activate_ai2_managers_thunder,
    create_tdk_test_step,
    set_test_step_status,
    configure_tdk_test_case,
    safe_unload_module
)

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkservices", "1", standAlone=True)

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

# Configure test case using helper function
configure_tdk_test_case(obj, ip, port, 'PackageMgr_DAC_02_InstallAllApps')

# Get the result of connection with test component and DUT
loadmodulestatus = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedResult = "SUCCESS"
    
    install_results = []
    installed_package_ids = []  # Track installed packages for cleanup
    download_ids = []  # Track download IDs for cleanup
    
    try:
        # PRECONDITION: Check and activate AI2.0 Manager plugins
        all_activated, failed_plugins = check_and_activate_ai2_managers_thunder(obj, required_only=False)
        
        # Check if essential plugins are available (PackageManagerRDKEMS is required)
        essential_failed = [p for p in failed_plugins if 'PackageManagerRDKEMS' in p]
        
        if essential_failed:
            print(f"\n[ERROR] Essential plugin not available: {', '.join(essential_failed)}")
            print("[TEST RESULT] SKIPPED - Essential plugin not available on this device")
            obj.setLoadModuleStatus("FAILURE")
            safe_unload_module(obj, "rdkservices")
            exit()
        
        # Step 1: Fetch DAC configuration
        print("\n[STEP 1] Fetching DAC configuration...")
        catalog_url, username, password = fetch_dac_config()
        print(f"  Catalog URL: {catalog_url}")
        
        # Step 2: Get device platform info
        print("\n[STEP 2] Reading device platform configuration...")
        firmware_ver, platform_name = get_device_info_from_json()
        print(f"  Platform: {platform_name}")
        print(f"  Firmware Version: {firmware_ver}")
        
        # Step 3: List all applications from DAC catalog
        print("\n[STEP 3] Listing applications from DAC catalog...")
        applications = list_dac_packages(catalog_url, username, password, platform_name, firmware_ver)
        print(f"  Total applications found: {len(applications)}")
        
        if not applications:
            print("[ERROR] No applications found in DAC catalog")
            obj.setLoadModuleStatus("FAILURE")
        else:
            # Step 4: Download and install each application
            print("\n[STEP 4] Downloading and installing applications...")
            for idx, app in enumerate(applications, 1):
                app_id = app.get('id', 'Unknown')
                app_name = app.get('name', 'Unknown')
                app_version = app.get('version', '1.0.0')
                
                print(f"\n  [{idx}/{len(applications)}] {app_name} (ID: {app_id}, Version: {app_version})")
                
                # Create TDK test step for this install
                tdkTestObj = create_tdk_test_step(obj, f"Install_{idx}", f"Install {app_name}")
                tdkTestObj.addParameter("app_id", app_id)
                tdkTestObj.addParameter("app_version", app_version)
                
                try:
                    # Download package
                    download_url = build_download_url(
                        catalog_url, app_id, app_version, platform_name, firmware_ver
                    )
                    print(f"    Downloading from: {download_url}")
                    
                    download_id = thunder_download_package(obj, download_url, app_name)
                    print(f"    ✓ Download ID: {download_id}")
                    
                    download_ids.append(download_id)  # Track for cleanup
                    
                    # Prepare install parameters
                    file_locator = f"/opt/CDL/package{download_id}"
                    additional_metadata = build_additional_metadata(app)
                    
                    print(f"    Installing from: {file_locator}")
                    
                    # Install package
                    install_result = thunder_install_package(
                        obj, app_id, app_version, download_id, 
                        additional_metadata, app_name
                    )
                    
                    print(f"    ✓ Installation successful")
                    
                    installed_package_ids.append(app_id)  # Track for cleanup
                    
                    install_results.append({
                        'app_id': app_id,
                        'app_name': app_name,
                        'status': 'SUCCESS',
                        'download_id': download_id
                    })
                    
                    # Report SUCCESS to TDK
                    set_test_step_status(tdkTestObj, "SUCCESS", f"Installed successfully")
                    
                    # Small delay between installations
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"    ✗ Installation FAILED: {str(e)}")
                    install_results.append({
                        'app_id': app_id,
                        'app_name': app_name,
                        'status': 'FAILURE',
                        'error': str(e)
                    })
                    
                    # Report FAILURE to TDK
                    set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
            
            # Summary
            print("\n" + "="*80)
            print("INSTALLATION SUMMARY")
            print("="*80)
            
            success_count = sum(1 for r in install_results if r['status'] == 'SUCCESS')
            failure_count = len(install_results) - success_count
            
            print(f"Total Applications: {len(install_results)}")
            print(f"Successful Installations: {success_count}")
            print(f"Failed Installations: {failure_count}")
            
            # Detailed results
            if failure_count > 0:
                print("\nFailed Applications:")
                for result in install_results:
                    if result['status'] == 'FAILURE':
                        print(f"  - {result['app_name']} ({result['app_id']}): {result.get('error', 'Unknown error')}")
            
            # Set final status
            if success_count == len(install_results):
                print("\n[TEST RESULT] SUCCESS - All applications installed successfully")
                obj.setLoadModuleStatus("SUCCESS")
            elif success_count > 0:
                print("\n[TEST RESULT] PARTIAL SUCCESS - Some applications installed")
                obj.setLoadModuleStatus("SUCCESS")
            else:
                print("\n[TEST RESULT] FAILURE - No applications installed")
                obj.setLoadModuleStatus("FAILURE")
            
            # POSTCONDITION: Test artifacts cleanup not needed for Thunder interface
            print("\n[TEST CLEANUP] Thunder interface - no cleanup required")
    
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {str(e)}")
        obj.setLoadModuleStatus("FAILURE")
        
        # Thunder interface - no cleanup needed
    
    safe_unload_module(obj, "rdkservices")
else:
    print("[ERROR] Failed to load rdkservices module")
    obj.setLoadModuleStatus("FAILURE")
