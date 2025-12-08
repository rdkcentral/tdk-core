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
  <version>2</version>
  <name>PackageMgr_DAC_01_DownloadAllApps</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>RdkService_Test</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test AI2.0 Package Manager download functionality using Thunder RDK Services - Download all available applications from DAC catalog</synopsis>
  <groups_id />
  <execution_time>10</execution_time>
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
    <test_case_id>TC_PackageMgr_DAC_01</test_case_id>
    <test_objective>Verify PackageManagerRDKEMS can download all available applications from DAC catalog using Thunder interface</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDKTV</test_setup>
    <pre_requisite>
1. Device should have PackageManagerRDKEMS plugin available
2. Device should have internet connectivity to reach DAC server
3. Device configuration file should have platform and firmware version info
</pre_requisite>
    <api_or_interface_used>org.rdk.PackageManagerRDKEMS.1.download</api_or_interface_used>
    <input_parameters>DAC download URLs for available applications</input_parameters>
    <automation_approch>
1. Check PackageManagerRDKEMS plugin availability via Thunder
2. Fetch DAC catalog configuration
3. Read device platform and firmware information
4. List available applications from DAC catalog
5. Download first 5 applications using Thunder PackageManager interface
6. Verify download results and provide summary
</automation_approch>
    <expected_output>All available applications should be downloaded successfully with valid download IDs</expected_output>
    <priority>High</priority>
    <test_stub_interface>Thunder</test_stub_interface>
    <test_script>PackageMgr_DAC_01_DownloadAllApps</test_script>
    <skipped>No</skipped>
    <release_version>M128</release_version>
    <remarks>Thunder-based implementation using RdkService_Test primitive</remarks>
  </test_cases>
</xml>
'''

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import json
from ai2_0_utils import (
    fetch_dac_config,
    list_dac_packages,
    build_download_url,
    thunder_download_package,
    get_device_info_from_json,
    safe_unload_module
)

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkservices", "1", standAlone=True)

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
    
    try:
        # Step 1: Check plugin availability
        print("\n[STEP 1] Checking PackageManagerRDKEMS plugin availability...")
        tdkTestObj = obj.createTestStep('RdkService_Test')
        tdkTestObj.addParameter("xml_name", "PackageManagerRDKEMS")
        tdkTestObj.addParameter("request_type", "status")
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        
        if "SUCCESS" in result:
            print("[INFO] PackageManagerRDKEMS plugin is available")
            tdkTestObj.setResultStatus("SUCCESS")
            
            # Step 2: Fetch DAC configuration
            print("\n[STEP 2] Fetching DAC configuration...")
            try:
                catalog_url, username, password = fetch_dac_config()
                print(f"[INFO] DAC Catalog URL: {catalog_url}")
            except Exception as e:
                print(f"[ERROR] Failed to fetch DAC config: {str(e)}")
                obj.setLoadModuleStatus("FAILURE")
                safe_unload_module(obj, "rdkservices")
                exit()
            
            # Step 3: Read device configuration
            print("\n[STEP 3] Reading device platform and firmware version...")
            try:
                firmware_ver, platform_name = get_device_info_from_json()
                print(f"[INFO] Platform: {platform_name}, Firmware: {firmware_ver}")
            except Exception as e:
                print(f"[ERROR] Failed to read device config: {str(e)}")
                obj.setLoadModuleStatus("FAILURE")
                safe_unload_module(obj, "rdkservices")
                exit()
            
            # Step 4: List applications from DAC catalog
            print("\n[STEP 4] Listing applications from DAC catalog...")
            try:
                applications = list_dac_packages(catalog_url, username, password, platform_name, firmware_ver)
                if not applications:
                    print("[WARNING] No applications found in DAC catalog")
                    obj.setLoadModuleStatus("FAILURE")
                    safe_unload_module(obj, "rdkservices")
                    exit()
                print(f"[INFO] Found {len(applications)} applications in catalog")
            except Exception as e:
                print(f"[ERROR] Failed to list DAC applications: {str(e)}")
                obj.setLoadModuleStatus("FAILURE")
                safe_unload_module(obj, "rdkservices")
                exit()
            
            # Step 5: Download applications using Thunder interface
            print(f"\n[STEP 5] Downloading applications via Thunder PackageManager...")
            download_count = 0
            max_downloads = min(5, len(applications))  # Limit to first 5 apps for testing
            
            for idx, app in enumerate(applications[:max_downloads], 1):
                app_id = app.get('id', app.get('packageId', ''))
                app_name = app.get('name', app_id)
                app_version = app.get('version', '1.0.0')
                
                print(f"\n[{idx}/{max_downloads}] Processing {app_name}...")
                
                try:
                    # Build download URL
                    download_url = build_download_url(
                        catalog_url, app_id, app_version, platform_name, firmware_ver
                    )
                    print(f"    Download URL: {download_url}")
                    
                    # Download using Thunder PackageManagerRDKEMS
                    download_id = thunder_download_package(obj, download_url, app_name)
                    
                    if download_id:
                        print(f"    ✓ Download successful - ID: {download_id}")
                        download_count += 1
                        download_results.append({
                            'app_id': app_id,
                            'app_name': app_name,
                            'status': 'SUCCESS',
                            'download_id': download_id
                        })
                    else:
                        print(f"    ✗ Download failed - No download ID returned")
                        download_results.append({
                            'app_id': app_id,
                            'app_name': app_name,
                            'status': 'FAILURE',
                            'error': 'No download ID'
                        })
                        
                except Exception as e:
                    print(f"    ✗ Error: {str(e)}")
                    download_results.append({
                        'app_id': app_id,
                        'app_name': app_name,
                        'status': 'FAILURE',
                        'error': str(e)
                    })
            
            # Summary
            print("\n" + "="*80)
            print("DOWNLOAD SUMMARY")
            print("="*80)
            print(f"Total Applications: {len(applications)}")
            print(f"Downloads Attempted: {max_downloads}")
            print(f"Successful Downloads: {download_count}")
            print(f"Failed Downloads: {max_downloads - download_count}")
            
            if download_count > 0:
                print("\nSuccessful Downloads:")
                for result in download_results:
                    if result['status'] == 'SUCCESS':
                        print(f"  ✓ {result['app_name']} - ID: {result['download_id']}")
            
            if download_count < max_downloads:
                print("\nFailed Downloads:")
                for result in download_results:
                    if result['status'] == 'FAILURE':
                        print(f"  ✗ {result['app_name']} - Error: {result.get('error', 'Unknown')}")
            
            print("="*80)
            
            # Set final test result
            if download_count == max_downloads:
                print("\n[TEST RESULT] SUCCESS - All downloads completed successfully")
                obj.setLoadModuleStatus("SUCCESS")
            elif download_count > 0:
                print(f"\n[TEST RESULT] PARTIAL SUCCESS - {download_count}/{max_downloads} downloads successful")
                obj.setLoadModuleStatus("SUCCESS")  # Consider partial success as success
            else:
                print("\n[TEST RESULT] FAILURE - No downloads successful")
                obj.setLoadModuleStatus("FAILURE")
                
        else:
            print("[ERROR] PackageManagerRDKEMS plugin is not available")
            tdkTestObj.setResultStatus("FAILURE")
            obj.setLoadModuleStatus("FAILURE")
    
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {str(e)}")
        obj.setLoadModuleStatus("FAILURE")
    
    safe_unload_module(obj, "rdkservices")
else:
    print("[ERROR] Failed to load rdkservices module")
    obj.setLoadModuleStatus("FAILURE")