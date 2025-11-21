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
  <name>PackageMgr_DAC_01_DownloadAllApps</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>RdkService_Test</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Download all applications from DAC catalog using Package Manager download API</synopsis>
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
    <test_case_id>TC_PackageMgr_DAC_01</test_case_id>
    <test_objective>Download all applications from DAC catalog for the device platform</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK device with PackageManager plugin enabled</test_setup>
    <pre_requisite>1. TDK Agent should be up and running
2. PackageManagerRDKEMS plugin should be activated
3. Network connectivity to DAC catalog
4. Device should have PackageManagerRDKEMS.json with platform configuration</pre_requisite>
    <api_or_interface_used>org.rdk.PackageManagerRDKEMS.1.download</api_or_interface_used>
    <input_parameters>None (reads from DAC config and device config)</input_parameters>
    <automation_approch>1. Fetch DAC catalog configuration from config endpoint
2. Read device platform and firmware version from PackageManagerRDKEMS.json
3. List all available applications from DAC catalog
4. For each application, download using PackageManager.download API
5. Verify download ID is returned for each application
6. Report success/failure for each download</automation_approch>
    <expected_output>Each application should return a valid downloadId</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkservicesstub.so</test_stub_interface>
    <test_script>PackageMgr_DAC_01_DownloadAllApps</test_script>
    <skipped>No</skipped>
    <release_version>M100</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dac_utils import (
    fetch_dac_config,
    list_dac_packages,
    build_download_url,
    download_package,
    get_device_info_from_json,
    check_and_activate_ai2_managers,
    delete_downloaded_packages,
    create_tdk_test_step,
    set_test_step_status
)

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkservices", "1")

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip, port, 'PackageMgr_DAC_01_DownloadAllApps')

# Get the result of connection with test component and DUT
loadmodulestatus = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedResult = "SUCCESS"
    
    download_results = []
    download_ids = []  # Track download IDs for cleanup
    
    try:
        # PRECONDITION: Check and activate AI2.0 Manager plugins
        jsonrpc_url = f"http://{ip}:9998/jsonrpc"
        
        tdkTestObj = create_tdk_test_step(obj, "Precondition_Check", "Activate AI2.0 Manager plugins")
        all_activated, failed_plugins = check_and_activate_ai2_managers(jsonrpc_url)
        
        if not all_activated:
            print(f"\n[ERROR] Required plugins not activated: {', '.join(failed_plugins)}")
            print("[TEST RESULT] FAILURE - Precondition check failed")
            set_test_step_status(tdkTestObj, "FAILURE", f"Plugins not activated: {', '.join(failed_plugins)}")
            obj.setLoadModuleStatus("FAILURE")
            obj.unloadModule("rdkservices")
            exit()
        
        set_test_step_status(tdkTestObj, "SUCCESS", "All AI2.0 Manager plugins activated")
        
        # Step 1: Fetch DAC configuration
        print("\n[STEP 1] Fetching DAC configuration...")
        tdkTestObj = create_tdk_test_step(obj, "Fetch_DAC_Config", "Fetch DAC catalog configuration")
        
        catalog_url, username, password = fetch_dac_config()
        print(f"  Catalog URL: {catalog_url}")
        print(f"  Username: {username}")
        
        set_test_step_status(tdkTestObj, "SUCCESS", f"DAC config fetched: {catalog_url}")
        
        # Step 2: Get device platform info
        print("\n[STEP 2] Reading device platform configuration...")
        tdkTestObj = create_tdk_test_step(obj, "Read_Device_Config", "Read platform and firmware version")
        
        firmware_ver, platform_name = get_device_info_from_json()
        print(f"  Platform: {platform_name}")
        print(f"  Firmware Version: {firmware_ver}")
        
        set_test_step_status(tdkTestObj, "SUCCESS", f"Platform: {platform_name}, Firmware: {firmware_ver}")
        
        # Step 3: List all applications from DAC catalog
        print("\n[STEP 3] Listing applications from DAC catalog...")
        tdkTestObj = create_tdk_test_step(obj, "List_DAC_Applications", f"List apps for {platform_name}")
        
        applications = list_dac_packages(catalog_url, username, password, platform_name, firmware_ver)
        print(f"  Total applications found: {len(applications)}")
        
        if not applications:
            print("[ERROR] No applications found in DAC catalog")
            set_test_step_status(tdkTestObj, "FAILURE", "No applications in catalog")
            obj.setLoadModuleStatus("FAILURE")
        else:
            set_test_step_status(tdkTestObj, "SUCCESS", f"Found {len(applications)} applications")
            
            # Step 4: Download each application
            print("\n[STEP 4] Downloading applications...")
            for idx, app in enumerate(applications, 1):
                app_id = app.get('id', 'Unknown')
                app_name = app.get('name', 'Unknown')
                app_version = app.get('version', '1.0.0')
                
                print(f"\n  [{idx}/{len(applications)}] {app_name} (ID: {app_id}, Version: {app_version})")
                
                # Create TDK test step for this download
                tdkTestObj = create_tdk_test_step(obj, f"Download_{idx}", f"Download {app_name}")
                tdkTestObj.addParameter("app_id", app_id)
                tdkTestObj.addParameter("app_version", app_version)
                
                try:
                    # Build download URL
                    download_url = build_download_url(
                        catalog_url, app_id, app_version, platform_name, firmware_ver
                    )
                    print(f"    Download URL: {download_url}")
                    
                    # Download package
                    download_id = download_package(download_url, jsonrpc_url)
                    print(f"    ✓ Download ID: {download_id}")
                    
                    download_ids.append(download_id)  # Track for cleanup
                    
                    download_results.append({
                        'app_id': app_id,
                        'app_name': app_name,
                        'status': 'SUCCESS',
                        'download_id': download_id
                    })
                    
                    # Report SUCCESS to TDK
                    set_test_step_status(tdkTestObj, "SUCCESS", f"Downloaded ID: {download_id}")
                    
                except Exception as e:
                    print(f"    ✗ Download FAILED: {str(e)}")
                    download_results.append({
                        'app_id': app_id,
                        'app_name': app_name,
                        'status': 'FAILURE',
                        'error': str(e)
                    })
                    
                    # Report FAILURE to TDK
                    set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
            
            # Summary
            print("\n" + "="*80)
            print("DOWNLOAD SUMMARY")
            print("="*80)
            
            success_count = sum(1 for r in download_results if r['status'] == 'SUCCESS')
            failure_count = len(download_results) - success_count
            
            print(f"Total Applications: {len(download_results)}")
            print(f"Successful Downloads: {success_count}")
            print(f"Failed Downloads: {failure_count}")
            
            # Detailed results
            if failure_count > 0:
                print("\nFailed Applications:")
                for result in download_results:
                    if result['status'] == 'FAILURE':
                        print(f"  - {result['app_name']} ({result['app_id']}): {result.get('error', 'Unknown error')}")
            
            # Set final status
            if success_count == len(download_results):
                print("\n[TEST RESULT] SUCCESS - All applications downloaded successfully")
                obj.setLoadModuleStatus("SUCCESS")
            elif success_count > 0:
                print("\n[TEST RESULT] PARTIAL SUCCESS - Some applications downloaded")
                obj.setLoadModuleStatus("SUCCESS")
            else:
                print("\n[TEST RESULT] FAILURE - No applications downloaded")
                obj.setLoadModuleStatus("FAILURE")
            
                # POSTCONDITION: Cleanup downloaded packages
                if download_ids:
                    tdkTestObj = create_tdk_test_step(obj, "Cleanup_Downloads", "Delete downloaded packages")
                    try:
                        delete_downloaded_packages(download_ids, jsonrpc_url)
                        set_test_step_status(tdkTestObj, "SUCCESS", f"Deleted {len(download_ids)} downloads")
                    except Exception as cleanup_error:
                        set_test_step_status(tdkTestObj, "FAILURE", f"Cleanup error: {str(cleanup_error)}")
    
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {str(e)}")
        obj.setLoadModuleStatus("FAILURE")
        
        # Cleanup on error
        if download_ids:
            try:
                delete_downloaded_packages(download_ids, jsonrpc_url)
            except:
                pass
    
    obj.unloadModule("rdkservices")
else:
    print("[ERROR] Failed to load rdkservices module")
    obj.setLoadModuleStatus("FAILURE")
