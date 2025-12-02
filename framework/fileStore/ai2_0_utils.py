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
"""
DAC Utilities Module

Common utility functions for DAC (Distributed Application Catalog) based Package Manager tests.
Provides reusable helpers for:
- Fetching DAC configuration and catalog listings
- JSON-RPC calls to Package Manager plugin
- Application download, install, list, launch, and uninstall operations
"""

import json
import requests
from typing import Any, Dict, List, Optional, Tuple

# DAC Configuration
DEFAULT_DAC_CONFIG_URL = "https://dac.config.dev.fireboltconnect.com/configuration/cpe.json"
DEFAULT_JSONRPC_URL = "http://127.0.0.1:9998/jsonrpc"

# Package Manager RPC Methods
PM_DOWNLOAD_METHOD = "org.rdk.PackageManagerRDKEMS.1.download"
PM_INSTALL_METHOD = "org.rdk.PackageManagerRDKEMS.install"
PM_LIST_METHOD = "org.rdk.PackageManagerRDKEMS.1.listPackages"
PM_UNINSTALL_METHOD = "org.rdk.PackageManagerRDKEMS.uninstall"
APP_MANAGER_LAUNCH_METHOD = "org.rdk.AppManager.1.launchApp"


def create_tdk_test_step(tdk_obj, step_name: str, step_description: str = "") -> Any:
    """
    Create a TDK test step for tracking individual operations.
    
    Args:
        tdk_obj: TDK scripting library object
        step_name: Name of the test step (e.g., 'Download_Package', 'Install_App')
        step_description: Optional description for the step
        
    Returns:
        TDK test step object
    """
    tdkTestObj = tdk_obj.createTestStep('RdkService_Test')
    if step_description:
        tdkTestObj.addParameter("description", step_description)
    tdkTestObj.addParameter("step_name", step_name)
    return tdkTestObj


def set_test_step_status(tdkTestObj, status: str, details: str = ""):
    """
    Set TDK test step status with optional details.
    
    Args:
        tdkTestObj: TDK test step object
        status: "SUCCESS" or "FAILURE"
        details: Optional details message
    """
    if details:
        print(f"  [TDK STEP] {status}: {details}")
    tdkTestObj.setResultStatus(status)


def fetch_dac_config(config_url: str = DEFAULT_DAC_CONFIG_URL) -> Tuple[str, str, str]:
    """
    Fetch DAC catalog configuration.
    
    Returns:
        Tuple of (catalog_url, username, password)
    """
    try:
        resp = requests.get(config_url, timeout=30)
        resp.raise_for_status()
        cfg = resp.json()
        
        catalog = cfg['appstore-catalog']
        url_val = catalog['url']
        user_val = catalog['authentication']['user']
        password_val = catalog['authentication']['password']
        
        return url_val, user_val, password_val
    except Exception as e:
        raise Exception(f"Failed to fetch DAC config: {str(e)}")


def list_dac_packages(catalog_url: str, username: str, password: str, 
                      platform_name: str, firmware_ver: str) -> List[Dict[str, Any]]:
    """
    List packages from DAC catalog for given platform and firmware version.
    
    Args:
        catalog_url: Base DAC catalog URL
        username: Authentication username
        password: Authentication password
        platform_name: Platform name (e.g., 'rpi4')
        firmware_ver: Firmware version
    
    Returns:
        List of application dictionaries with id, name, version, etc.
    """
    try:
        url = f"{catalog_url}/apps"
        params = {
            'platformName': platform_name,
            'firmwareVer': firmware_ver
        }
        
        resp = requests.get(url, auth=(username, password), params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        # Handle different response structures
        if isinstance(data, dict):
            if 'applications' in data:
                return data['applications']
            elif 'apps' in data:
                return data['apps']
        elif isinstance(data, list):
            return data
        
        return []
    except Exception as e:
        raise Exception(f"Failed to list DAC packages: {str(e)}")


def get_app_details(catalog_url: str, username: str, password: str,
                    package_id: str, platform_name: str, firmware_ver: str) -> Dict[str, Any]:
    """
    Get detailed information for a specific application.
    
    Returns:
        Dictionary with application details
    """
    try:
        url = f"{catalog_url}/apps/{package_id}"
        params = {
            'platformName': platform_name,
            'firmwareVer': firmware_ver
        }
        
        resp = requests.get(url, auth=(username, password), params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        raise Exception(f"Failed to get app details: {str(e)}")


def build_download_url(catalog_url: str, package_id: str, version: str, 
                       platform_name: str, firmware_ver: str) -> str:
    """
    Build the download URL for a package bundle.
    
    Args:
        catalog_url: Base DAC catalog URL
        package_id: Application package ID
        version: Application version
        platform_name: Platform name
        firmware_ver: Firmware version
    
    Returns:
        Complete download URL for the package bundle
    """
    return f"{catalog_url}/bundles/{package_id}/{version}/{platform_name}/{firmware_ver}"


def jsonrpc_call(method: str, params: Optional[Dict[str, Any]] = None, 
                 url: str = DEFAULT_JSONRPC_URL, request_id: int = 1) -> Dict[str, Any]:
    """
    Make a JSON-RPC call to WPEFramework.
    
    Args:
        method: RPC method name
        params: Method parameters (optional)
        url: JSON-RPC endpoint URL
        request_id: Request ID
    
    Returns:
        Response dictionary
    
    Raises:
        Exception: If RPC call fails or returns error
    """
    payload = {
        'jsonrpc': '2.0',
        'id': request_id,
        'method': method,
    }
    
    if params is not None:
        payload['params'] = params
    
    try:
        resp = requests.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        
        if 'error' in data:
            error_msg = data['error']
            if isinstance(error_msg, dict):
                error_msg = f"Code: {error_msg.get('code')}, Message: {error_msg.get('message')}"
            raise Exception(f"JSON-RPC error for {method}: {error_msg}")
        
        return data
    except requests.exceptions.RequestException as e:
        raise Exception(f"JSON-RPC request failed: {str(e)}")


def download_package(download_url: str, jsonrpc_url: str = DEFAULT_JSONRPC_URL) -> str:
    """
    Download a package using Package Manager.
    
    Args:
        download_url: URL to download package from
        jsonrpc_url: JSON-RPC endpoint
    
    Returns:
        Download ID
    """
    params = {'url': download_url}
    result = jsonrpc_call(PM_DOWNLOAD_METHOD, params, jsonrpc_url, request_id=3)
    
    download_id = result.get('result', {}).get('downloadId')
    if not download_id:
        raise Exception("Download failed: no downloadId returned")
    
    return download_id


def install_package(package_id: str, version: str, file_locator: str,
                   additional_metadata: List[Dict[str, str]],
                   jsonrpc_url: str = DEFAULT_JSONRPC_URL) -> Dict[str, Any]:
    """
    Install a package using Package Manager.
    
    Args:
        package_id: Package identifier
        version: Package version
        file_locator: Path to package file (e.g., /opt/CDL/package2001)
        additional_metadata: List of metadata dicts with 'name' and 'value'
        jsonrpc_url: JSON-RPC endpoint
    
    Returns:
        Installation result
    """
    params = {
        'packageId': package_id,
        'version': version,
        'fileLocator': file_locator,
        'additionalMetadata': additional_metadata
    }
    
    return jsonrpc_call(PM_INSTALL_METHOD, params, jsonrpc_url, request_id=1013)


def list_installed_packages(jsonrpc_url: str = DEFAULT_JSONRPC_URL) -> List[Dict[str, Any]]:
    """
    List installed packages.
    
    Returns:
        List of installed package dictionaries
    """
    result = jsonrpc_call(PM_LIST_METHOD, None, jsonrpc_url, request_id=42)
    
    packages = result.get('result', {})
    if isinstance(packages, dict):
        return packages.get('packages', [])
    elif isinstance(packages, list):
        return packages
    
    return []


def launch_app(app_id: str, jsonrpc_url: str = DEFAULT_JSONRPC_URL) -> Dict[str, Any]:
    """
    Launch an application using App Manager.
    
    Args:
        app_id: Application ID to launch
        jsonrpc_url: JSON-RPC endpoint
    
    Returns:
        Launch result
    """
    params = {'appId': app_id}
    return jsonrpc_call(APP_MANAGER_LAUNCH_METHOD, params, jsonrpc_url, request_id=1015)


def uninstall_package(package_id: str, jsonrpc_url: str = DEFAULT_JSONRPC_URL) -> Dict[str, Any]:
    """
    Uninstall a package using Package Manager.
    
    Args:
        package_id: Package identifier to uninstall
        jsonrpc_url: JSON-RPC endpoint
    
    Returns:
        Uninstall result
    """
    params = {'packageId': package_id}
    return jsonrpc_call(PM_UNINSTALL_METHOD, params, jsonrpc_url, request_id=1014)


def build_additional_metadata(app_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Build additional metadata list from application data.
    
    Args:
        app_data: Application dictionary from DAC catalog
    
    Returns:
        List of metadata dictionaries suitable for install call
    """
    metadata = []
    
    if 'name' in app_data:
        metadata.append({'name': 'appName', 'value': app_data['name']})
    
    if 'category' in app_data:
        metadata.append({'name': 'category', 'value': app_data['category']})
    
    if 'type' in app_data:
        metadata.append({'name': 'type', 'value': app_data['type']})
    
    return metadata


def verify_package_installed(package_id: str, jsonrpc_url: str = DEFAULT_JSONRPC_URL) -> bool:
    """
    Verify if a package is installed.
    
    Args:
        package_id: Package ID to check
        jsonrpc_url: JSON-RPC endpoint
    
    Returns:
        True if package is installed, False otherwise
    """
    try:
        packages = list_installed_packages(jsonrpc_url)
        return any(
            pkg.get('packageId') == package_id or pkg.get('id') == package_id
            for pkg in packages
        )
    except Exception:
        return False


def get_device_info_from_json(json_path: str = "/etc/WPEFramework/plugins/PackageManagerRDKEMS.json") -> Tuple[str, str]:
    """
    Read device platform and firmware information from PackageManager config.
    
    Returns:
        Tuple of (firmware_version, platform_name)
    """
    import os
    
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Config file not found: {json_path}")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    firmware_ver = str(data.get('FirmwareCompatibilityKey', ''))
    platform_name = str(data.get('dacBundlePlatformNameOverride', ''))
    
    if not firmware_ver or not platform_name:
        raise ValueError(f"Required keys missing in {json_path}")
    
    return firmware_ver, platform_name


def check_plugin_status(plugin_name: str, jsonrpc_url: str = DEFAULT_JSONRPC_URL) -> Dict[str, Any]:
    """
    Check the status of a Thunder plugin.
    
    Args:
        plugin_name: Plugin callsign (e.g., 'org.rdk.PackageManagerRDKEMS')
        jsonrpc_url: JSON-RPC endpoint URL
        
    Returns:
        Dict containing plugin status information
    """
    method = f"Controller.1.status@{plugin_name}"
    result = jsonrpc_call(method, {}, jsonrpc_url)
    return result if result else {}


def activate_plugin(plugin_name: str, jsonrpc_url: str = DEFAULT_JSONRPC_URL) -> bool:
    """
    Activate a Thunder plugin.
    
    Args:
        plugin_name: Plugin callsign (e.g., 'org.rdk.PackageManagerRDKEMS')
        jsonrpc_url: JSON-RPC endpoint URL
        
    Returns:
        True if activation successful, False otherwise
    """
    try:
        method = "Controller.1.activate"
        params = {"callsign": plugin_name}
        result = jsonrpc_call(method, params, jsonrpc_url)
        
        # Wait a moment for activation to complete
        import time
        time.sleep(2)
        
        # Verify activation
        status = check_plugin_status(plugin_name, jsonrpc_url)
        return status.get('state') == 'activated'
    except Exception as e:
        print(f"Error activating {plugin_name}: {str(e)}")
        return False


def check_and_activate_ai2_managers(jsonrpc_url: str = DEFAULT_JSONRPC_URL) -> Tuple[bool, List[str]]:
    """
    Check and activate all required AI2.0 Manager plugins.
    
    Order: Storage -> Package -> Download -> Window -> Runtime -> Lifecycle -> App -> Preinstall
    
    Args:
        jsonrpc_url: JSON-RPC endpoint URL
        
    Returns:
        Tuple of (all_activated: bool, failed_plugins: List[str])
    """
    import time
    
    # Plugins in dependency order
    plugins = [
        "org.rdk.StorageManager",
        "org.rdk.PackageManagerRDKEMS",
        "org.rdk.DownloadManager",
        "org.rdk.RDKWindowManager",
        "org.rdk.RuntimeManager",
        "org.rdk.LifecycleManager",
        "org.rdk.AppManager",
        "org.rdk.PreinstallManager"
    ]
    
    failed_plugins = []
    
    print("\n" + "="*80)
    print("PRECONDITION: Checking AI2.0 Manager Plugins")
    print("="*80)
    
    for idx, plugin in enumerate(plugins, 1):
        print(f"\n[{idx}/{len(plugins)}] Checking {plugin}...")
        
        try:
            # Check current status
            status = check_plugin_status(plugin, jsonrpc_url)
            current_state = status.get('state', 'unknown')
            
            print(f"  Current state: {current_state}")
            
            if current_state != 'activated':
                print(f"  Activating {plugin}...")
                success = activate_plugin(plugin, jsonrpc_url)
                
                if success:
                    print(f"  ✓ {plugin} activated successfully")
                else:
                    print(f"  ✗ {plugin} activation failed")
                    failed_plugins.append(plugin)
            else:
                print(f"  ✓ {plugin} already activated")
                
        except Exception as e:
            print(f"  ✗ Error checking {plugin}: {str(e)}")
            failed_plugins.append(plugin)
        
        # Small delay between activations
        if idx < len(plugins):
            time.sleep(1)
    
    # Summary
    print("\n" + "="*80)
    if not failed_plugins:
        print("✅ All AI2.0 Manager plugins are activated")
        print("="*80)
        return True, []
    else:
        print("❌ The following plugins failed to activate:")
        for plugin in failed_plugins:
            print(f"  - {plugin}")
        print("="*80)
        return False, failed_plugins


def delete_downloaded_packages(download_ids: List[str], jsonrpc_url: str = DEFAULT_JSONRPC_URL) -> Dict[str, Any]:
    """
    Delete downloaded package files using DownloadManager.
    
    Args:
        download_ids: List of download IDs to delete
        jsonrpc_url: JSON-RPC endpoint URL
        
    Returns:
        Dict with deletion results
    """
    results = {
        'total': len(download_ids),
        'success': 0,
        'failed': 0,
        'errors': []
    }
    
    print("\n" + "="*80)
    print("POSTCONDITION: Cleaning up downloaded packages")
    print("="*80)
    
    for download_id in download_ids:
        print(f"  Deleting download ID: {download_id}")
        try:
            method = "org.rdk.DownloadManager.1.delete"
            params = {"downloadId": str(download_id)}
            result = jsonrpc_call(method, params, jsonrpc_url)
            
            if result:
                print(f"    ✓ Deleted successfully")
                results['success'] += 1
            else:
                print(f"    ✗ Deletion failed")
                results['failed'] += 1
                results['errors'].append(f"Download ID {download_id}: No result returned")
                
        except Exception as e:
            print(f"    ✗ Error: {str(e)}")
            results['failed'] += 1
            results['errors'].append(f"Download ID {download_id}: {str(e)}")
    
    # Summary
    print(f"\nDeletion Summary:")
    print(f"  Total: {results['total']}")
    print(f"  Success: {results['success']}")
    print(f"  Failed: {results['failed']}")
    print("="*80)
    
    return results


def cleanup_all_test_artifacts(package_ids: List[str], download_ids: Optional[List[str]] = None, 
                                jsonrpc_url: str = DEFAULT_JSONRPC_URL) -> Dict[str, Any]:
    """
    Complete cleanup of all test artifacts including packages and downloads.
    
    Args:
        package_ids: List of package IDs to uninstall
        download_ids: Optional list of download IDs to delete
        jsonrpc_url: JSON-RPC endpoint URL
        
    Returns:
        Dict with cleanup results
    """
    results = {
        'uninstalled': 0,
        'uninstall_failed': 0,
        'deleted': 0,
        'delete_failed': 0,
        'errors': []
    }
    
    print("\n" + "="*80)
    print("POSTCONDITION: Complete Test Cleanup")
    print("="*80)
    
    # Step 1: Uninstall packages
    if package_ids:
        print(f"\nUninstalling {len(package_ids)} packages...")
        for pkg_id in package_ids:
            print(f"  Uninstalling: {pkg_id}")
            try:
                uninstall_package(pkg_id, jsonrpc_url)
                
                # Verify uninstallation
                import time
                time.sleep(2)
                is_installed = verify_package_installed(pkg_id, jsonrpc_url)
                
                if not is_installed:
                    print(f"    ✓ Uninstalled successfully")
                    results['uninstalled'] += 1
                else:
                    print(f"    ✗ Still installed after uninstall")
                    results['uninstall_failed'] += 1
                    results['errors'].append(f"Package {pkg_id}: Still installed")
                    
            except Exception as e:
                print(f"    ✗ Error: {str(e)}")
                results['uninstall_failed'] += 1
                results['errors'].append(f"Package {pkg_id}: {str(e)}")
    
    # Step 2: Delete downloaded files
    if download_ids:
        print(f"\nDeleting {len(download_ids)} downloaded files...")
        delete_results = delete_downloaded_packages(download_ids, jsonrpc_url)
        results['deleted'] = delete_results['success']
        results['delete_failed'] = delete_results['failed']
        results['errors'].extend(delete_results['errors'])
    
    # Summary
    print("\n" + "="*80)
    print("CLEANUP SUMMARY")
    print("="*80)
    print(f"Packages Uninstalled: {results['uninstalled']}/{len(package_ids) if package_ids else 0}")
    print(f"Downloads Deleted: {results['deleted']}/{len(download_ids) if download_ids else 0}")
    
    total_failed = results['uninstall_failed'] + results['delete_failed']
    if total_failed > 0:
        print(f"\n❌ {total_failed} cleanup operations failed")
        if results['errors']:
            print("\nErrors:")
            for error in results['errors'][:5]:  # Show first 5 errors
                print(f"  - {error}")
    else:
        print("\n✅ All cleanup operations completed successfully")
    
    print("="*80)
    
    return results


def configure_test_case_standalone(obj, ip, port, test_case_name):
    """
    Configure TDK test case for standalone execution with all required parameters
    
    Args:
        obj: TDKScriptingLibrary object
        ip: Device IP address
        port: Device port
        test_case_name: Name of the test case
    """
    obj.configureTestCase(
        url="http://localhost:8080/rdk-test-tool",           # url
        path="/tmp/tdk/",                                     # path
        logpath="/tmp/tdk/logs/",                            # logpath
        execId=1,                                            # execId
        execDeviceId=1,                                      # execDeviceId
        execResId=1,                                         # execResId
        deviceIp=ip,                                         # deviceIp
        devicePort=port,                                     # devicePort
        logTransferPort=69,                                  # logTransferPort
        statusPort=8088,                                     # statusPort
        testcaseID=test_case_name,                           # testcaseID
        deviceId=1,                                          # deviceId
        performanceBenchMarkingEnabled="false",             # performanceBenchMarkingEnabled
        performanceSystemDiagnosisEnabled="false",          # performanceSystemDiagnosisEnabled
        scriptSuiteEnabled="false",                         # scriptSuiteEnabled
        executionName=test_case_name                         # executionName
    )
