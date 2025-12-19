##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>PackageMgr_DAC_01_DownloadAllApps</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>RdkService_Test</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test AI2.0 Package Manager download functionality using Thunder RDK Services - Download all available applications from DAC catalog</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>RDKTV</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_PackageMgr_DAC_01</test_case_id>
    <test_objective>Verify PackageManagerRDKEMS can download all available applications from DAC catalog using Thunder interface</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator and RPI</test_setup>
    <pre_requisite>1. Device should have PackageManagerRDKEMS plugin available
2. Device should have internet connectivity to reach DAC server
3. Device configuration file should have platform and firmware version info</pre_requisite>
    <api_or_interface_used>org.rdk.PackageManagerRDKEMS.1.download</api_or_interface_used>
    <input_parameters>DAC download URLs for available applications</input_parameters>
    <automation_approch>1. Check PackageManagerRDKEMS plugin availability via Thunder
2. Fetch DAC catalog configuration
3. Read device platform and firmware information
4. List available applications from DAC catalog
5. Download first 5 applications using Thunder PackageManager interface
6. Verify download results and provide summary</automation_approch>
    <expected_output>All available applications should be downloaded successfully with valid download IDs</expected_output>
    <priority>High</priority>
    <test_stub_interface>Nil</test_stub_interface>
    <test_script>PackageMgr_DAC_01_DownloadAllApps</test_script>
    <skipped>Nil</skipped>
    <release_version>M128</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
from ai2_0_utils import (
    fetch_dac_config,
    list_dac_packages,
    build_download_url,
    pm_download,
    get_device_info_from_json,
    safe_unload_module,
    thunder_is_plugin_active,
    get_ai2_setting,
    ensure_plugin_active,
)

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("PackageManager", "1", standAlone=True)

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box IP and port while executing script
print ("Configuring the IP and Port of the device")
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'PackageMgr_DAC_01_DownloadAllApps');

# Get the result of connection with test component and DUT
loadmodulestatus = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedResult = "SUCCESS"
    
    download_results = []
    
    try:
        # Step 1: Verify PackageManagerRDKEMS is active via status check (no direct activation)
        print("\n[STEP 1] Checking PackageManagerRDKEMS plugin active status...")
        # Use device IP for Thunder JSON-RPC endpoint with port from config (default 9998)
        rpc_port = get_ai2_setting('packageManager.jsonRpcPort', 9998)
        jsonrpc_url = f"http://{ip}:{rpc_port}/jsonrpc"
        if thunder_is_plugin_active("org.rdk.PackageManagerRDKEMS", jsonrpc_url=jsonrpc_url):
            print("[INFO] PackageManagerRDKEMS plugin is active")
        else:
            print("[INFO] Plugin inactive. Attempting activation via utils...")
            if ensure_plugin_active(obj, "org.rdk.PackageManagerRDKEMS", jsonrpc_url=jsonrpc_url):
                print("[SUCCESS] PackageManagerRDKEMS plugin activated")
            else:
                print("[ERROR] PackageManagerRDKEMS plugin is not active and activation failed")
                obj.setLoadModuleStatus("FAILURE")
                safe_unload_module(obj, "PackageManager")
                exit()

        # Step 2: Fetch DAC configuration
        print("\n[STEP 2] Fetching DAC configuration...")
        try:
            catalog_url, username, password = fetch_dac_config()
            print(f"[INFO] DAC Catalog URL: {catalog_url}")
        except Exception as e:
            print(f"[ERROR] Failed to fetch DAC config: {str(e)}")
            obj.setLoadModuleStatus("FAILURE")
            safe_unload_module(obj, "PackageManager")
            exit()
            
        # Step 3: Read device configuration
        print("\n[STEP 3] Reading device platform and firmware version...")
        try:
            firmware_ver, platform_name = get_device_info_from_json()
            print(f"[INFO] Platform: {platform_name}, Firmware: {firmware_ver}")
        except Exception as e:
            print(f"[ERROR] Failed to read device config: {str(e)}")
            obj.setLoadModuleStatus("FAILURE")
            safe_unload_module(obj, "PackageManager")
            exit()
            
        # Step 4: List applications from DAC catalog
        print("\n[STEP 4] Listing applications from DAC catalog...")
        try:
            applications = list_dac_packages(catalog_url, username, password, platform_name, firmware_ver)
            if not applications:
                print("[WARNING] No applications found in DAC catalog")
                obj.setLoadModuleStatus("FAILURE")
                safe_unload_module(obj, "PackageManager")
                exit()
            print(f"[INFO] Found {len(applications)} applications in catalog")
            try:
                names = [app.get('name') or app.get('id') or app.get('packageId') or 'unknown' for app in applications]
                print("[INFO] Applications:")
                for n in names:
                    print(f"  - {n}")
            except Exception:
                pass
        except Exception as e:
            print(f"[ERROR] Failed to list DAC applications: {str(e)}")
            obj.setLoadModuleStatus("FAILURE")
            safe_unload_module(obj, "PackageManager")
            exit()
            
        # Step 5: Download applications using Thunder interface
        print(f"\n[STEP 5] Downloading applications via Thunder PackageManager...")
        download_count = 0
        max_downloads_cfg = get_ai2_setting('packageManager.maxDownloads', 5)
        max_downloads = min(int(max_downloads_cfg), len(applications))
        prefer_jsonrpc = bool(get_ai2_setting('packageManager.preferJsonRpc', True))
        
        for idx, app in enumerate(applications[:max_downloads], 1):
                app_id = app.get('id', app.get('packageId', ''))
                app_name = app.get('name', app_id)
                default_ver = get_ai2_setting('packageManager.defaultAppVersion', '1.0.0')
                app_version = app.get('version', default_ver)
                
                print(f"\n[{idx}/{max_downloads}] Processing {app_name}...")
                
                try:
                    # Build download URL
                    download_url = build_download_url(
                        catalog_url, app_id, app_version, platform_name, firmware_ver
                    )
                    print(f"    Download URL: {download_url}")

                    # Simple helper drives preferJsonRpc + fallback
                    download_id = pm_download(obj, ip, download_url, app_name)
                    
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
        else:
            print(f"\n[TEST RESULT] FAILURE - {download_count}/{max_downloads} downloads successful")
            obj.setLoadModuleStatus("FAILURE")
                
        # End of main try
    
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {str(e)}")
        obj.setLoadModuleStatus("FAILURE")
    
    safe_unload_module(obj, "PackageManager")
else:
    print("[ERROR] Failed to load PackageManager module")
    obj.setLoadModuleStatus("FAILURE")