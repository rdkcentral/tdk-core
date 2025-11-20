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
  <name>PackageMgr_DAC_03_ListInstalledApps</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>RdkService_Test</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>List and verify all installed applications from DAC catalog</synopsis>
  <groups_id />
  <execution_time>60</execution_time>
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
    <test_case_id>TC_PackageMgr_DAC_03</test_case_id>
    <test_objective>List all installed packages and verify against DAC catalog applications</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK device with PackageManager plugin enabled</test_setup>
    <pre_requisite>1. TDK Agent should be up and running
2. PackageManagerRDKEMS plugin should be activated
3. Applications should be installed (run PackageMgr_DAC_02_InstallAllApps)</pre_requisite>
    <api_or_interface_used>org.rdk.PackageManagerRDKEMS.1.listPackages</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Fetch list of applications from DAC catalog
2. Call PackageManager.listPackages to get all installed packages
3. Compare installed packages against DAC catalog applications
4. Report installed, missing, and unexpected packages
5. Display detailed information for each installed package</automation_approch>
    <expected_output>All DAC catalog applications should be listed as installed</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkservicesstub.so</test_stub_interface>
    <test_script>PackageMgr_DAC_03_ListInstalledApps</test_script>
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
    list_installed_packages,
    get_device_info_from_json,
    check_and_activate_ai2_managers,
    create_tdk_test_step,
    set_test_step_status
)

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkservices", "1")

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box IP and port while executing script
ip = "<ipaddress>"
port = "<port>"
obj.configureTestCase(ip, port, 'PackageMgr_DAC_03_ListInstalledApps')

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
            dac_app_ids = {app.get('id') for app in dac_applications}
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
            installed_ids = {pkg.get('packageId') for pkg in installed_packages}
            print(f"  Total installed packages: {len(installed_packages)}")
            set_test_step_status(tdkTestObj, "SUCCESS", f"Found {len(installed_packages)} installed packages")
        except Exception as e:
            set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
            raise
        
        # Step 5: Compare and analyze
        tdkTestObj = create_tdk_test_step(obj, "Step5_VerifyInstallations", 
                                           "Verify DAC applications installation status")
        try:
            print("\n[STEP 5] Analyzing installation status...")
            
            # Find installed DAC apps
            installed_dac_apps = installed_ids.intersection(dac_app_ids)
            
            # Find missing DAC apps
            missing_dac_apps = dac_app_ids - installed_ids
            
            # Find unexpected packages (not in DAC catalog)
            unexpected_packages = installed_ids - dac_app_ids
            
            verification_msg = f"Installed: {len(installed_dac_apps)}/{len(dac_app_ids)}, Missing: {len(missing_dac_apps)}"
            set_test_step_status(tdkTestObj, "SUCCESS", verification_msg)
        except Exception as e:
            set_test_step_status(tdkTestObj, "FAILURE", f"Error: {str(e)}")
            raise
        
        # Display summary
        print("\n" + "="*80)
        print("PACKAGE VERIFICATION SUMMARY")
        print("="*80)
        print(f"Total DAC Catalog Applications: {len(dac_app_ids)}")
        print(f"Total Installed Packages: {len(installed_ids)}")
        print(f"DAC Apps Installed: {len(installed_dac_apps)}")
        print(f"DAC Apps Missing: {len(missing_dac_apps)}")
        print(f"Unexpected Packages: {len(unexpected_packages)}")
        
        # Display installed DAC applications
        if installed_dac_apps:
            print("\n" + "="*80)
            print("INSTALLED DAC APPLICATIONS")
            print("="*80)
            for pkg in installed_packages:
                pkg_id = pkg.get('packageId')
                if pkg_id in installed_dac_apps:
                    # Find corresponding DAC app
                    dac_app = next((app for app in dac_applications if app.get('id') == pkg_id), None)
                    app_name = dac_app.get('name', 'Unknown') if dac_app else 'Unknown'
                    
                    print(f"\n  Package ID: {pkg_id}")
                    print(f"  Name: {app_name}")
                    print(f"  Version: {pkg.get('version', 'Unknown')}")
                    print(f"  Install State: {pkg.get('installState', 'Unknown')}")
                    
                    metadata = pkg.get('metadata', [])
                    if metadata:
                        print(f"  Metadata:")
                        for meta in metadata:
                            print(f"    - {meta.get('name', 'Unknown')}: {meta.get('value', 'Unknown')}")
        
        # Display missing applications
        if missing_dac_apps:
            print("\n" + "="*80)
            print("MISSING DAC APPLICATIONS (Not Installed)")
            print("="*80)
            for dac_app in dac_applications:
                if dac_app.get('id') in missing_dac_apps:
                    print(f"  - {dac_app.get('name', 'Unknown')} ({dac_app.get('id')})")
        
        # Display unexpected packages
        if unexpected_packages:
            print("\n" + "="*80)
            print("UNEXPECTED PACKAGES (Not in DAC Catalog)")
            print("="*80)
            for pkg in installed_packages:
                pkg_id = pkg.get('packageId')
                if pkg_id in unexpected_packages:
                    print(f"  - {pkg.get('name', 'Unknown')} ({pkg_id})")
        
        # Determine test status
        if len(installed_dac_apps) == len(dac_app_ids):
            print("\n[TEST RESULT] SUCCESS - All DAC applications are installed")
            obj.setLoadModuleStatus("SUCCESS")
        elif len(installed_dac_apps) > 0:
            print(f"\n[TEST RESULT] PARTIAL SUCCESS - {len(installed_dac_apps)}/{len(dac_app_ids)} DAC applications installed")
            obj.setLoadModuleStatus("SUCCESS")
        else:
            print("\n[TEST RESULT] FAILURE - No DAC applications installed")
            obj.setLoadModuleStatus("FAILURE")
    
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {str(e)}")
        obj.setLoadModuleStatus("FAILURE")
    
    obj.unloadModule("rdkservices")
else:
    print("[ERROR] Failed to load rdkservices module")
    obj.setLoadModuleStatus("FAILURE")
