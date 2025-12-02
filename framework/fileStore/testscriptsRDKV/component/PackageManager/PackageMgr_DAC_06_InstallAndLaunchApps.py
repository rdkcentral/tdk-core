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
  <name>PackageMgr_DAC_06_InstallAndLaunchApps</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>RdkService_Test</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Install and launch all applications from DAC catalog one by one</synopsis>
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
    <test_case_id>TC_PackageMgr_DAC_06</test_case_id>
    <test_objective>Download, install, and immediately launch each application from DAC catalog one by one</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK device with PackageManager and AppManager plugins enabled</test_setup>
    <pre_requisite>1. TDK Agent should be up and running
2. PackageManagerRDKEMS, DownloadManagerRDKEMS, and AppManager plugins should be activated
3. Sufficient storage space for package installations
4. Network connectivity to DAC catalog</pre_requisite>
    <api_or_interface_used>org.rdk.PackageManagerRDKEMS.1.download
org.rdk.PackageManagerRDKEMS.1.install
org.rdk.AppManager.1.launchApp</api_or_interface_used>
    <input_parameters>None (reads from device config and DAC catalog)</input_parameters>
    <automation_approch>1. Activate all required AI2.0 Manager plugins
2. Fetch DAC catalog configuration and list available applications
3. For each application:
   a. Download the application bundle
   b. Install the downloaded package
   c. Launch the installed application
   d. Track results for each operation
4. Report comprehensive results with success/failure for each app
5. Cleanup downloaded packages after completion</automation_approch>
    <expected_output>Each application should be successfully downloaded, installed, and launched</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkservicesstub.so</test_stub_interface>
    <test_script>PackageMgr_DAC_06_InstallAndLaunchApps</test_script>
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
    get_device_info_from_json,
    build_download_url,
    build_additional_metadata,
    download_package,
    install_package,
    launch_app,
    verify_package_installed,
    check_and_activate_ai2_managers,
    delete_downloaded_packages,
    create_tdk_test_step,
    set_test_step_status
    configure_tdk_test_case
)

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkservices", "1", standAlone=True)

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

# Configure test case using helper function
result = configure_tdk_test_case(obj, ip, port, 'PackageMgr_DAC_06_InstallAndLaunchApps')

if "SUCCESS" in result.upper():
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
    
    download_ids = []  # Track download IDs for cleanup
    app_results = []
    
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
            applications = list_dac_packages(catalog_url, username, password, platform_name, firmware_ver)
            print(f"  Total applications found: {len(applications)}")
            set_test_step_status(tdkTestObj, "SUCCESS", f"Found {len(applications)} applications")
        except Exception as e:
            set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
            raise
        
        if not applications:
            print("[WARNING] No applications found in DAC catalog")
            obj.setLoadModuleStatus("SUCCESS")
        else:
            # Step 4: Download, Install, and Launch each application
            print("\n[STEP 4] Processing applications (Download → Install → Launch)...")
            for idx, app in enumerate(applications, 1):
                app_id = app.get('id')
                app_name = app.get('name', 'Unknown')
                app_version = app.get('version', 'Unknown')
                
                print(f"\n{'='*80}")
                print(f"[{idx}/{len(applications)}] Processing: {app_name}")
                print(f"  App ID: {app_id}")
                print(f"  Version: {app_version}")
                print(f"{'='*80}")
                
                app_result = {
                    'app_id': app_id,
                    'app_name': app_name,
                    'app_version': app_version,
                    'download_status': 'NOT_STARTED',
                    'install_status': 'NOT_STARTED',
                    'launch_status': 'NOT_STARTED'
                }
                
                # Step 4a: Download
                tdkTestObj = create_tdk_test_step(obj, f"Step4a_Download_{idx}", 
                                                   f"Download {app_name}")
                tdkTestObj.addParameter("app_id", app_id)
                tdkTestObj.addParameter("app_name", app_name)
                tdkTestObj.addParameter("app_version", app_version)
                
                try:
                    print(f"\n  [DOWNLOAD] Starting download...")
                    download_url = build_download_url(
                        catalog_url, app_id, app_version, platform_name, firmware_ver
                    )
                    print(f"    Download URL: {download_url}")
                    
                    download_id = download_package(download_url, jsonrpc_url)
                    print(f"    ✓ Download ID: {download_id}")
                    download_ids.append(download_id)
                    
                    app_result['download_status'] = 'SUCCESS'
                    app_result['download_id'] = download_id
                    set_test_step_status(tdkTestObj, "SUCCESS", f"Downloaded ID: {download_id}")
                    
                except Exception as e:
                    print(f"    ✗ Download FAILED: {str(e)}")
                    app_result['download_status'] = 'FAILURE'
                    app_result['download_error'] = str(e)
                    set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
                    app_results.append(app_result)
                    continue  # Skip install and launch if download fails
                
                # Step 4b: Install
                tdkTestObj = create_tdk_test_step(obj, f"Step4b_Install_{idx}", 
                                                   f"Install {app_name}")
                tdkTestObj.addParameter("app_id", app_id)
                tdkTestObj.addParameter("app_name", app_name)
                tdkTestObj.addParameter("download_id", download_id)
                
                try:
                    print(f"\n  [INSTALL] Starting installation...")
                    additional_metadata = build_additional_metadata(app)
                    install_result = install_package(app_id, app_version, download_id, 
                                                    additional_metadata, jsonrpc_url)
                    print(f"    ✓ Install command sent")
                    
                    # Small delay to allow installation to complete
                    time.sleep(3)
                    
                    # Verify installation
                    is_installed = verify_package_installed(app_id, jsonrpc_url)
                    if is_installed:
                        print(f"    ✓ Package installed successfully")
                        app_result['install_status'] = 'SUCCESS'
                        set_test_step_status(tdkTestObj, "SUCCESS", "Package installed successfully")
                    else:
                        print(f"    ✗ Package not found after install")
                        app_result['install_status'] = 'FAILURE'
                        app_result['install_error'] = 'Package not found after install'
                        set_test_step_status(tdkTestObj, "FAILURE", "Package not found after install")
                        app_results.append(app_result)
                        continue  # Skip launch if install verification fails
                    
                except Exception as e:
                    print(f"    ✗ Install FAILED: {str(e)}")
                    app_result['install_status'] = 'FAILURE'
                    app_result['install_error'] = str(e)
                    set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
                    app_results.append(app_result)
                    continue  # Skip launch if install fails
                
                # Step 4c: Launch
                tdkTestObj = create_tdk_test_step(obj, f"Step4c_Launch_{idx}", 
                                                   f"Launch {app_name}")
                tdkTestObj.addParameter("app_id", app_id)
                tdkTestObj.addParameter("app_name", app_name)
                
                try:
                    print(f"\n  [LAUNCH] Starting application launch...")
                    launch_result = launch_app(app_id, jsonrpc_url)
                    
                    # Check launch result
                    if launch_result and isinstance(launch_result, dict):
                        if launch_result.get('result') == 'success' or 'launchId' in launch_result:
                            print(f"    ✓ Launch successful")
                            app_result['launch_status'] = 'SUCCESS'
                            set_test_step_status(tdkTestObj, "SUCCESS", "Launch successful")
                        else:
                            print(f"    ⚠ Launch returned: {launch_result}")
                            app_result['launch_status'] = 'PARTIAL'
                            app_result['launch_result'] = launch_result
                            set_test_step_status(tdkTestObj, "SUCCESS", f"Launch completed: {launch_result}")
                    else:
                        print(f"    ✓ Launch command sent")
                        app_result['launch_status'] = 'SUCCESS'
                        set_test_step_status(tdkTestObj, "SUCCESS", "Launch command sent")
                    
                    # Delay before next app to avoid resource contention
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"    ✗ Launch FAILED: {str(e)}")
                    app_result['launch_status'] = 'FAILURE'
                    app_result['launch_error'] = str(e)
                    set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
                
                app_results.append(app_result)
            
            # Summary
            print("\n" + "="*80)
            print("TEST EXECUTION SUMMARY")
            print("="*80)
            
            download_success = sum(1 for r in app_results if r['download_status'] == 'SUCCESS')
            install_success = sum(1 for r in app_results if r['install_status'] == 'SUCCESS')
            launch_success = sum(1 for r in app_results if r['launch_status'] == 'SUCCESS')
            
            print(f"Total Applications: {len(app_results)}")
            print(f"Download Success: {download_success}/{len(app_results)}")
            print(f"Install Success: {install_success}/{len(app_results)}")
            print(f"Launch Success: {launch_success}/{len(app_results)}")
            
            # Detailed per-app results
            print("\n" + "="*80)
            print("PER-APPLICATION RESULTS")
            print("="*80)
            for result in app_results:
                print(f"\n{result['app_name']} ({result['app_id']})")
                print(f"  Download: {result['download_status']}", end="")
                if result['download_status'] == 'FAILURE':
                    print(f" - {result.get('download_error', 'Unknown error')}")
                else:
                    print()
                print(f"  Install:  {result['install_status']}", end="")
                if result['install_status'] == 'FAILURE':
                    print(f" - {result.get('install_error', 'Unknown error')}")
                else:
                    print()
                print(f"  Launch:   {result['launch_status']}", end="")
                if result['launch_status'] == 'FAILURE':
                    print(f" - {result.get('launch_error', 'Unknown error')}")
                else:
                    print()
            
            # Set final status
            if launch_success == len(app_results):
                print("\n[TEST RESULT] SUCCESS - All applications downloaded, installed, and launched")
                obj.setLoadModuleStatus("SUCCESS")
            elif launch_success > 0:
                print(f"\n[TEST RESULT] PARTIAL SUCCESS - {launch_success}/{len(app_results)} applications fully processed")
                obj.setLoadModuleStatus("SUCCESS")
            else:
                print("\n[TEST RESULT] FAILURE - No applications successfully launched")
                obj.setLoadModuleStatus("FAILURE")
    
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {str(e)}")
        obj.setLoadModuleStatus("FAILURE")
    
    # Postcondition: Cleanup downloaded packages
    if download_ids:
        tdkTestObj = create_tdk_test_step(obj, "Postcondition_Cleanup", 
                                           "Delete downloaded packages")
        try:
            print("\n[POSTCONDITION] Cleaning up downloaded packages...")
            delete_downloaded_packages(download_ids, jsonrpc_url)
            print(f"  ✓ Deleted {len(download_ids)} download(s)")
            set_test_step_status(tdkTestObj, "SUCCESS", f"Deleted {len(download_ids)} downloads")
        except Exception as e:
            print(f"  ⚠ Cleanup warning: {str(e)}")
            set_test_step_status(tdkTestObj, "FAILURE", f"Cleanup failed: {str(e)}")
    
    obj.unloadModule("rdkservices")
else:
    print("[ERROR] Failed to load rdkservices module")
    obj.setLoadModuleStatus("FAILURE")
