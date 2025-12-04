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
DEFAULT_JSONRPC_URL = "http://127.0.0.1:9998/jsonrpc"  # For legacy compatibility

# Timeout constants
socket_timeout = 10
http_timeout = 30

# Thunder-based testing - no direct JSON-RPC needed


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


def fetch_dac_config(config_url: str = DEFAULT_DAC_CONFIG_URL, timeout: int = 30) -> Tuple[str, str, str]:
    """
    Fetch DAC catalog configuration.
    
    Returns:
        Tuple of (catalog_url, username, password)
    """
    try:
        resp = requests.get(config_url, timeout=timeout)
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
                      platform_name: str, firmware_ver: str, timeout: int = 30) -> List[Dict[str, Any]]:
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
                    package_id: str, platform_name: str, firmware_ver: str, timeout: int = 30) -> Dict[str, Any]:
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
                 url: str = DEFAULT_JSONRPC_URL, request_id: int = 1, timeout: int = 60) -> Dict[str, Any]:
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
        resp = requests.post(url, json=payload, timeout=timeout)
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



def get_device_info_from_json(json_path: str = None) -> Tuple[str, str]:
    """
    Read device platform and firmware information from PackageManager config.
    
    Returns:
        Tuple of (firmware_version, platform_name)
    """
    import os
    
    # Determine default config path if not provided
    if json_path is None:
        # Try common locations for PackageManager config
        possible_paths = [
            "/etc/WPEFramework/plugins/PackageManagerRDKEMS.json",
            "/opt/WPEFramework/share/WPEFramework/PackageManagerRDKEMS.json",
            "./PackageManagerRDKEMS.json"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                json_path = path
                break
        
        if json_path is None:
            raise FileNotFoundError(f"Config file not found in any of these locations: {possible_paths}")
    
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Config file not found: {json_path}")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    firmware_ver = str(data.get('FirmwareCompatibilityKey', ''))
    platform_name = str(data.get('dacBundlePlatformNameOverride', ''))
    
    if not firmware_ver or not platform_name:
        raise ValueError(f"Required keys missing in {json_path}")
    
    return firmware_ver, platform_name


def check_and_activate_ai2_managers(jsonrpc_url: str = DEFAULT_JSONRPC_URL, 
                                    required_only: bool = True, activation_delay: int = 1) -> Tuple[bool, List[str]]:
    """
    Check and activate AI2.0 Manager plugins. Handle missing plugins gracefully.
    
    Args:
        jsonrpc_url: JSON-RPC endpoint URL
        required_only: If True, only check plugins that are actually needed
        
    Returns:
        Tuple of (all_available_activated: bool, failed_plugins: List[str])
    """
    import time
    
    # Start with core plugins that are likely to exist
    core_plugins = [
        "org.rdk.PackageManagerRDKEMS", 
        "org.rdk.AppManager"
    ]
    
    # Extended list for full AI2.0 stack (when available)
    all_plugins = [
        "org.rdk.StorageManager",
        "org.rdk.PackageManagerRDKEMS",
        "org.rdk.DownloadManager", 
        "org.rdk.RDKWindowManager",
        "org.rdk.RuntimeManager",
        "org.rdk.LifecycleManager",
        "org.rdk.AppManager",
        "org.rdk.PreinstallManager"
    ]
    
    plugins_to_check = core_plugins if required_only else all_plugins
    
    available_plugins = []
    failed_plugins = []
    missing_plugins = []
    
    print("\n" + "="*80)
    print("PRECONDITION: Checking AI2.0 Manager Plugins")
    print("="*80)
    
    # Legacy mode warning - JSON-RPC functions not available
    print("\n⚠ Legacy compatibility mode - plugin status checking requires Thunder interface")
    print("Recommend using check_and_activate_ai2_managers_thunder() for full functionality")
    
    # First pass: Check which plugins exist
    print("\n🔍 Discovering available plugins...")
    for plugin in plugins_to_check:
        try:
            # Legacy mode - plugin status checking not available without JSON-RPC functions
            print(f"  ⚠ {plugin} - Status check not available in legacy mode")
            missing_plugins.append(plugin)
        except Exception:
            missing_plugins.append(plugin)
            print(f"  ⚠ {plugin} - Not available")
    
    if not available_plugins:
        print("\n❌ No AI2.0 manager plugins found on this device")
        print("This may be expected if running on devices without AI2.0 stack")
        print("="*80)
        return False, plugins_to_check
    
    # Second pass: Activate available plugins (legacy mode limitation)
    print(f"\n🚀 Plugin activation not available in legacy mode...")
    for idx, plugin in enumerate(available_plugins, 1):
        print(f"\n[{idx}/{len(available_plugins)}] {plugin}...")
        
        try:
            # Legacy mode - plugin activation not available without JSON-RPC functions
            print(f"  ⚠ {plugin} - Plugin control not available in legacy mode")
            failed_plugins.append(plugin)
                
        except Exception as e:
            print(f"  ✗ Error with {plugin}: {str(e)}")
            failed_plugins.append(plugin)
        
        # Small delay between checks
        if idx < len(available_plugins):
            time.sleep(activation_delay)
    
    # Summary
    print("\n" + "="*80)
    activated_count = len(available_plugins) - len(failed_plugins)
    
    if missing_plugins:
        print("📋 Plugin Status Summary:")
        print(f"  Available: {len(available_plugins)}")
        print(f"  Missing: {len(missing_plugins)}")
        print(f"  Activated: {activated_count}")
        print(f"  Failed: {len(failed_plugins)}")
        
        if missing_plugins:
            print(f"\n⚠ Missing plugins (not available on device):")
            for plugin in missing_plugins:
                print(f"    - {plugin}")
    
    if not failed_plugins and available_plugins:
        print("✅ All available AI2.0 Manager plugins are activated")
        print("="*80)
        return True, []
    elif failed_plugins:
        print("❌ The following available plugins failed to activate:")
        for plugin in failed_plugins:
            print(f"    - {plugin}")
        print("="*80)
        return False, failed_plugins
    else:
        print("⚠ No plugins could be activated")
        print("="*80)
        return False, available_plugins


def safe_unload_module(obj, module_name: str) -> None:
    """
    Safely unload a TDK module with error handling.
    
    Args:
        obj: TDK library object
        module_name: Module name to unload
    """
    try:
        print(f"Unloading Module : {module_name}")
        obj.unloadModule(module_name)
        print("Unload Module Status : Success")
    except AttributeError as e:
        if "'NoneType' object has no attribute 'close'" in str(e):
            print("Unload Module Status : Success (connection already closed)")
        else:
            print(f"Unload Module Status : Error - {str(e)}")
    except Exception as e:
        print(f"Unload Module Status : Error - {str(e)}")


def test_tdk_agent_connectivity(ip: str, port: int = 8087) -> bool:
    """
    Test connectivity to TDK Agent without requiring execution IDs.
    
    Args:
        ip: Device IP address
        port: TDK Agent port
        
    Returns:
        True if TDK Agent is accessible, False otherwise
    """
    import socket
    import requests
    
    print(f"Testing TDK Agent connectivity at {ip}:{port}...")
    
    # Test 1: Socket connectivity
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(socket_timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            print(f"[PASS] Socket connection successful to {ip}:{port}")
        else:
            print(f"[FAIL] Socket connection failed to {ip}:{port}")
            return False
    except Exception as e:
        print(f"[FAIL] Socket test failed: {str(e)}")
        return False
    
    # Test 2: HTTP connectivity (basic TDK Agent endpoint)
    try:
        base_url = f"http://{ip}:{port}"
        response = requests.get(f"{base_url}/", timeout=http_timeout)
        print(f"[PASS] HTTP connection successful - Status: {response.status_code}")
        print(f"[INFO] TDK Agent URL: {base_url}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"[FAIL] HTTP connection failed - TDK Agent not responding at {base_url}")
        return False
    except requests.exceptions.Timeout:
        print(f"[FAIL] HTTP connection timeout - TDK Agent slow/unresponsive at {base_url}")
        return False
    except Exception as e:
        print(f"[FAIL] HTTP test failed: {str(e)}")
        return False


# Thunder-based functions for TDK integration
def create_tdk_test_step(tdk_obj, step_name: str, step_description: str = "") -> Any:
    """
    Create a TDK test step for Thunder-based testing.
    
    Args:
        tdk_obj: TDK scripting library object
        step_name: Name of the test step (e.g., 'Download_Package', 'Install_App')
        step_description: Optional description for the step
        
    Returns:
        TDK test step object configured for RdkService_Test
    """
    tdkTestObj = tdk_obj.createTestStep('RdkService_Test')
    if step_description:
        print(f"[TDK STEP] {step_name}: {step_description}")
    return tdkTestObj


def set_test_step_status(tdkTestObj, status: str, details: str = ""):
    """
    Set TDK test step status with optional details for Thunder-based tests.
    
    Args:
        tdkTestObj: TDK test step object
        status: "SUCCESS" or "FAILURE"
        details: Optional details message
    """
    if details:
        print(f"  [TDK RESULT] {status}: {details}")
    tdkTestObj.setResultStatus(status)


def check_thunder_plugin_status(tdk_obj, plugin_name: str) -> bool:
    """
    Check Thunder plugin status using TDK RdkService_Test.
    
    Args:
        tdk_obj: TDK scripting library object
        plugin_name: Plugin name (e.g., 'PackageManagerRDKEMS')
        
    Returns:
        True if plugin is available and active, False otherwise
    """
    try:
        tdkTestObj = tdk_obj.createTestStep('RdkService_Test')
        tdkTestObj.addParameter("xml_name", plugin_name)
        tdkTestObj.addParameter("request_type", "status")
        tdkTestObj.executeTestCase("SUCCESS")
        result = tdkTestObj.getResult()
        
        if "SUCCESS" in result:
            tdkTestObj.setResultStatus("SUCCESS")
            return True
        else:
            tdkTestObj.setResultStatus("FAILURE")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to check plugin status for {plugin_name}: {str(e)}")
        return False


def check_and_activate_ai2_managers(tdk_obj=None, jsonrpc_url: str = None, required_only: bool = True) -> Tuple[bool, List[str]]:
    """
    Check AI2.0 Manager plugins. Supports both Thunder and JSON-RPC modes.
    
    Args:
        tdk_obj: TDK scripting library object (for Thunder mode)
        jsonrpc_url: JSON-RPC endpoint (for direct mode) 
        required_only: If True, only check core plugins
        
    Returns:
        Tuple of (all_available_activated: bool, failed_plugins: List[str])
    """
    if tdk_obj is not None:
        # Thunder mode via TDK
        return check_and_activate_ai2_managers_thunder(tdk_obj, required_only)
    elif jsonrpc_url is not None:
        # Direct JSON-RPC mode (legacy)
        return check_and_activate_ai2_managers_jsonrpc(jsonrpc_url, required_only)
    else:
        raise ValueError("Either tdk_obj or jsonrpc_url must be provided")


def check_and_activate_ai2_managers_thunder(tdk_obj, required_only: bool = True) -> Tuple[bool, List[str]]:
    """
    Check AI2.0 Manager plugins using Thunder interface via TDK.
    
    Args:
        tdk_obj: TDK scripting library object
        required_only: If True, only check core plugins
        
    Returns:
        Tuple of (all_available_activated: bool, failed_plugins: List[str])
    """
    # Core plugins that are essential for AI2.0
    core_plugins = [
        "PackageManagerRDKEMS", 
        "AppManager"
    ]
    
    # Extended list for full AI2.0 stack
    all_plugins = [
        "StorageManager",
        "PackageManagerRDKEMS",
        "DownloadManager", 
        "RDKWindowManager",
        "RuntimeManager",
        "LifecycleManager",
        "AppManager",
        "PreinstallManager"
    ]
    
    plugins_to_check = core_plugins if required_only else all_plugins
    
    available_plugins = []
    failed_plugins = []
    
    print("\n" + "="*80)
    print("PRECONDITION: Checking AI2.0 Manager Plugins via Thunder")
    print("="*80)
    
    # Check which plugins are available via Thunder
    print(f"\n🔍 Discovering available plugins...")
    for plugin in plugins_to_check:
        print(f"  Checking {plugin}...")
        
        if check_thunder_plugin_status(tdk_obj, plugin):
            available_plugins.append(plugin)
            print(f"  ✓ {plugin} - Available and active")
        else:
            failed_plugins.append(plugin)
            print(f"  ✗ {plugin} - Not available or inactive")
    
    # Summary
    print("\n" + "="*80)
    
    print("📋 Plugin Status Summary:")
    print(f"  Available: {len(available_plugins)}")
    print(f"  Missing: {len(failed_plugins)}")
    
    if failed_plugins:
        print(f"\n⚠ Missing/Inactive plugins:")
        for plugin in failed_plugins:
            print(f"    - {plugin}")
    
    if available_plugins:
        print("✅ Available plugins:")
        for plugin in available_plugins:
            print(f"    - {plugin}")
        print("="*80)
        return True, []
    else:
        print("❌ No AI2.0 plugins available")
        print("="*80)
        return False, failed_plugins


def check_and_activate_ai2_managers_jsonrpc(jsonrpc_url: str = DEFAULT_JSONRPC_URL, 
                                           required_only: bool = True) -> Tuple[bool, List[str]]:
    """
    Check and activate AI2.0 Manager plugins using direct JSON-RPC. Handle missing plugins gracefully.
    
    Args:
        jsonrpc_url: JSON-RPC endpoint URL
        required_only: If True, only check plugins that are actually needed
        
    Returns:
        Tuple of (all_available_activated: bool, failed_plugins: List[str])
    """
    import time
    
    # Start with core plugins that are likely to exist
    core_plugins = [
        "org.rdk.PackageManagerRDKEMS", 
        "org.rdk.AppManager"
    ]
    
    # Extended list for full AI2.0 stack (when available)
    all_plugins = [
        "org.rdk.StorageManager",
        "org.rdk.PackageManagerRDKEMS",
        "org.rdk.DownloadManager", 
        "org.rdk.RDKWindowManager",
        "org.rdk.RuntimeManager",
        "org.rdk.LifecycleManager",
        "org.rdk.AppManager",
        "org.rdk.PreinstallManager"
    ]
    
    plugins_to_check = core_plugins if required_only else all_plugins
    
    available_plugins = []
    failed_plugins = []
    missing_plugins = []
    
    print("\n" + "="*80)
    print("PRECONDITION: Checking AI2.0 Manager Plugins")
    print("="*80)
    
    # Legacy mode warning - JSON-RPC functions not available  
    print("\n⚠ JSON-RPC mode not fully implemented - missing JSON-RPC helper functions")
    print("Recommend using check_and_activate_ai2_managers_thunder() for full functionality")
    
    # First pass: Check which plugins exist
    print("\n🔍 Discovering available plugins...")
    for plugin in plugins_to_check:
        try:
            # JSON-RPC mode - plugin status checking not available without helper functions
            print(f"  ⚠ {plugin} - Status check not available in JSON-RPC mode")
            missing_plugins.append(plugin)
        except Exception:
            missing_plugins.append(plugin)
            print(f"  ⚠ {plugin} - Not available")
    
    if not available_plugins:
        print("\n❌ No AI2.0 manager plugins found on this device")
        print("This may be expected if running on devices without AI2.0 stack")
        print("="*80)
        return False, plugins_to_check
    
    # Second pass: Activate available plugins (JSON-RPC mode limitation)
    print(f"\n🚀 Plugin activation not available in JSON-RPC mode...")
    for idx, plugin in enumerate(available_plugins, 1):
        print(f"\n[{idx}/{len(available_plugins)}] {plugin}...")
        
        try:
            # JSON-RPC mode - plugin activation not available without helper functions
            print(f"  ⚠ {plugin} - Plugin control not available in JSON-RPC mode") 
            failed_plugins.append(plugin)
                
        except Exception as e:
            print(f"  ✗ Error with {plugin}: {str(e)}")
            failed_plugins.append(plugin)
        
        # Small delay between checks
        if idx < len(available_plugins):
            time.sleep(1)
    
    # Summary
    print("\n" + "="*80)
    activated_count = len(available_plugins) - len(failed_plugins)
    
    if missing_plugins:
        print("📋 Plugin Status Summary:")
        print(f"  Available: {len(available_plugins)}")
        print(f"  Missing: {len(missing_plugins)}")
        print(f"  Activated: {activated_count}")
        print(f"  Failed: {len(failed_plugins)}")
        
        if missing_plugins:
            print(f"\n⚠ Missing plugins (not available on device):")
            for plugin in missing_plugins:
                print(f"    - {plugin}")
    
    if not failed_plugins and available_plugins:
        print("✅ All available AI2.0 Manager plugins are activated")
        print("="*80)
        return True, []
    elif failed_plugins:
        print("❌ The following available plugins failed to activate:")
        for plugin in failed_plugins:
            print(f"    - {plugin}")
        print("="*80)
        return False, failed_plugins
    else:
        print("⚠ No plugins could be activated")
        print("="*80)
        return False, available_plugins


def thunder_download_package(tdk_obj, download_url: str, app_name: str = "") -> Optional[str]:
    """
    Download a package using Thunder PackageManagerRDKEMS via TDK.
    
    Args:
        tdk_obj: TDK scripting library object
        download_url: URL to download package from
        app_name: Application name for logging
        
    Returns:
        Download ID if successful, None if failed
    """
    import json
    
    try:
        tdkTestObj = tdk_obj.createTestStep('RdkService_Test')
        tdkTestObj.addParameter("xml_name", "PackageManagerRDKEMS")
        tdkTestObj.addParameter("request_type", "download")
        tdkTestObj.addParameter("params", json.dumps({"url": download_url}))
        tdkTestObj.executeTestCase("SUCCESS")
        result = tdkTestObj.getResult()
        
        if "SUCCESS" in result:
            result_details = tdkTestObj.getResultDetails()
            try:
                response_data = json.loads(result_details)
                download_id = response_data.get('result', {}).get('downloadId')
                
                if download_id:
                    print(f"    ✓ Download successful - ID: {download_id}")
                    tdkTestObj.setResultStatus("SUCCESS")
                    return download_id
                else:
                    print(f"    ✗ Download failed - No download ID returned")
                    tdkTestObj.setResultStatus("FAILURE")
                    return None
            except json.JSONDecodeError:
                print(f"    ✗ Download failed - Invalid response format")
                tdkTestObj.setResultStatus("FAILURE")
                return None
        else:
            print(f"    ✗ Download failed - Thunder execution failed")
            tdkTestObj.setResultStatus("FAILURE")
            return None
            
    except Exception as e:
        print(f"    ✗ Download error: {str(e)}")
        return None


def thunder_install_package(tdk_obj, app_id: str, version: str, download_id: str, 
                           additional_metadata: Dict[str, Any] = None, app_name: str = "") -> bool:
    """
    Install a downloaded package using Thunder PackageManagerRDKEMS via TDK.
    
    Args:
        tdk_obj: TDK scripting library object
        app_id: Application ID
        version: Application version
        download_id: Download ID from download operation
        additional_metadata: Additional metadata for installation
        app_name: Application name for logging
        
    Returns:
        True if successful, False if failed
    """
    import json
    
    try:
        install_params = {
            "appId": app_id,
            "version": version,
            "downloadId": download_id
        }
        
        if additional_metadata:
            install_params["additionalMetadata"] = additional_metadata
        
        tdkTestObj = tdk_obj.createTestStep('RdkService_Test')
        tdkTestObj.addParameter("xml_name", "PackageManagerRDKEMS")
        tdkTestObj.addParameter("request_type", "install")
        tdkTestObj.addParameter("params", json.dumps(install_params))
        tdkTestObj.executeTestCase("SUCCESS")
        result = tdkTestObj.getResult()
        
        if "SUCCESS" in result:
            result_details = tdkTestObj.getResultDetails()
            try:
                response_data = json.loads(result_details)
                if response_data.get('success', False):
                    print(f"    ✓ Install successful for {app_name or app_id}")
                    tdkTestObj.setResultStatus("SUCCESS")
                    return True
                else:
                    error_msg = response_data.get('error', 'Unknown install error')
                    print(f"    ✗ Install failed for {app_name or app_id}: {error_msg}")
                    tdkTestObj.setResultStatus("FAILURE")
                    return False
            except json.JSONDecodeError:
                print(f"    ✗ Install failed for {app_name or app_id} - Invalid response format")
                tdkTestObj.setResultStatus("FAILURE")
                return False
        else:
            print(f"    ✗ Install failed for {app_name or app_id} - Thunder execution failed")
            tdkTestObj.setResultStatus("FAILURE")
            return False
            
    except Exception as e:
        print(f"    ✗ Install error for {app_name or app_id}: {str(e)}")
        return False


def thunder_uninstall_package(tdk_obj, app_id: str, app_name: str = "") -> bool:
    """
    Uninstall a package using Thunder PackageManagerRDKEMS via TDK.
    
    Args:
        tdk_obj: TDK scripting library object
        app_id: Application ID to uninstall
        app_name: Application name for logging
        
    Returns:
        True if successful, False if failed
    """
    import json
    
    try:
        tdkTestObj = tdk_obj.createTestStep('RdkService_Test')
        tdkTestObj.addParameter("xml_name", "PackageManagerRDKEMS")
        tdkTestObj.addParameter("request_type", "uninstall")
        tdkTestObj.addParameter("params", json.dumps({"appId": app_id}))
        tdkTestObj.executeTestCase("SUCCESS")
        result = tdkTestObj.getResult()
        
        if "SUCCESS" in result:
            result_details = tdkTestObj.getResultDetails()
            try:
                response_data = json.loads(result_details)
                if response_data.get('success', False):
                    print(f"    ✓ Uninstall successful for {app_name or app_id}")
                    tdkTestObj.setResultStatus("SUCCESS")
                    return True
                else:
                    error_msg = response_data.get('error', 'Unknown uninstall error')
                    print(f"    ✗ Uninstall failed for {app_name or app_id}: {error_msg}")
                    tdkTestObj.setResultStatus("FAILURE")
                    return False
            except json.JSONDecodeError:
                print(f"    ✗ Uninstall failed for {app_name or app_id} - Invalid response format")
                tdkTestObj.setResultStatus("FAILURE")
                return False
        else:
            print(f"    ✗ Uninstall failed for {app_name or app_id} - Thunder execution failed")
            tdkTestObj.setResultStatus("FAILURE")
            return False
            
    except Exception as e:
        print(f"    ✗ Uninstall error for {app_name or app_id}: {str(e)}")
        return False
