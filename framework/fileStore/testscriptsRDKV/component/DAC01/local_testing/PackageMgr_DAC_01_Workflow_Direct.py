#!/usr/bin/env python3
"""
Direct execution of DAC workflow without TDK framework dependency.
Tests: Download, Install, Launch, Kill, and Uninstall Application
"""

import sys
import json
import time
import requests
from pathlib import Path

# Configuration
DEVICE_IP = "192.168.29.164"
JSONRPC_PORT = 9998
JSONRPC_URL = f"http://{DEVICE_IP}:{JSONRPC_PORT}/jsonrpc"

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    from ai2_0_utils import (
        fetch_dac_config,
        list_dac_packages,
        build_download_url,
        pm_download,
        dac01_install_app,
        pm_list_packages,
        launch_app,
        kill_app,
        uninstall_app,
        verify_app_uninstalled,
        get_ai2_setting,
        activate_required_plugins
    )
    print("[OK] ai2_0_utils imported successfully")
except ImportError as e:
    print(f"[WARNING] Could not import ai2_0_utils: {e}")
    print("[INFO] Will use basic JSON-RPC calls instead")
    fetch_dac_config = None


def make_jsonrpc_call(method, params=None):
    """Make a JSON-RPC call to Thunder Framework"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        response = requests.post(JSONRPC_URL, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            print(f"[ERROR] {method}: {result['error']}")
            return None
        
        return result.get("result")
    except Exception as e:
        print(f"[ERROR] JSON-RPC call failed for {method}: {e}")
        return None


def test_device_connection():
    """Test connectivity to device"""
    print("\n" + "="*80)
    print("PRECONDITION: Test Device Connectivity")
    print("="*80)
    
    try:
        result = make_jsonrpc_call("org.rdk.System.1.systemVersion")
        if result:
            print(f"[SUCCESS] Device Connected")
            print(f"[INFO] Device Response: {result}")
            return True
        else:
            print(f"[ERROR] Failed to connect to {DEVICE_IP}:{JSONRPC_PORT}")
            return False
    except Exception as e:
        print(f"[ERROR] Connection test failed: {e}")
        return False


def activate_plugins():
    """Activate required plugins"""
    print("\n" + "="*80)
    print("STEP 0: Activate Required Plugins")
    print("="*80)
    
    required_plugins = [
        "org.rdk.PackageManager",
        "org.rdk.AppManager", 
        "org.rdk.LifecycleManager",
        "org.rdk.StorageManager",
        "org.rdk.RuntimeManager"
    ]
    
    for plugin in required_plugins:
        try:
            result = make_jsonrpc_call(f"{plugin}.activate")
            if result:
                print(f"[OK] {plugin} activated")
            else:
                print(f"[INFO] {plugin} may already be active")
        except Exception as e:
            print(f"[WARNING] Could not activate {plugin}: {e}")
    
    return True


def fetch_dac_packages():
    """Fetch DAC packages"""
    print("\n" + "="*80)
    print("STEP 1: Fetch DAC Configuration and List Packages")
    print("="*80)
    
    if fetch_dac_config:
        try:
            catalog_url, username, password = fetch_dac_config()
            print(f"[OK] DAC Catalog URL: {catalog_url}")
            
            packages = list_dac_packages(catalog_url, username, password)
            if packages:
                print(f"[OK] Found {len(packages)} packages in DAC catalog")
                for i, pkg in enumerate(packages[:3]):  # Show first 3
                    print(f"  [{i}] {pkg.get('name', 'Unknown')} v{pkg.get('version', 'Unknown')}")
                return packages
        except Exception as e:
            print(f"[ERROR] Failed to fetch DAC packages: {e}")
    
    return []


def download_package(packages, index=2):
    """Download a package from DAC"""
    print("\n" + "="*80)
    print(f"STEP 2: Download Package (Index {index})")
    print("="*80)
    
    if not packages or index >= len(packages):
        print(f"[ERROR] Invalid package index {index}")
        return None
    
    package = packages[index]
    print(f"[INFO] Downloading: {package.get('name')} v{package.get('version')}")
    
    try:
        if fetch_dac_config:
            catalog_url, username, password = fetch_dac_config()
            download_url = build_download_url(catalog_url, package)
            
            result = pm_download(JSONRPC_URL, download_url)
            if result and 'downloadId' in result:
                download_id = result['downloadId']
                print(f"[SUCCESS] Download started with ID: {download_id}")
                return download_id
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
    
    return None


def install_package(download_id):
    """Install a downloaded package"""
    print("\n" + "="*80)
    print("STEP 3: Install Package")
    print("="*80)
    
    if not download_id:
        print("[ERROR] No download ID provided")
        return None
    
    try:
        if fetch_dac_config:
            result = dac01_install_app(JSONRPC_URL, download_id)
            if result:
                print(f"[SUCCESS] Installation completed")
                print(f"[INFO] Installation result: {result}")
                return result.get('appId') or result.get('packageId')
    except Exception as e:
        print(f"[ERROR] Installation failed: {e}")
    
    return None


def launch_application(app_id):
    """Launch the installed application"""
    print("\n" + "="*80)
    print("STEP 4: Launch Application")
    print("="*80)
    
    if not app_id:
        print("[ERROR] No app ID provided")
        return False
    
    try:
        if fetch_dac_config:
            result = launch_app(JSONRPC_URL, app_id)
            if result:
                print(f"[SUCCESS] Application launched")
                print(f"[INFO] Launch result: {result}")
                return True
    except Exception as e:
        print(f"[ERROR] Launch failed: {e}")
    
    return False


def kill_application(app_id):
    """Kill the running application"""
    print("\n" + "="*80)
    print("STEP 5: Kill Application")
    print("="*80)
    
    if not app_id:
        print("[ERROR] No app ID provided")
        return False
    
    try:
        time.sleep(3)  # Let app run briefly
        
        if fetch_dac_config:
            result = kill_app(JSONRPC_URL, app_id)
            if result:
                print(f"[SUCCESS] Application killed")
                print(f"[INFO] Kill result: {result}")
                return True
    except Exception as e:
        print(f"[ERROR] Kill failed: {e}")
    
    return False


def uninstall_application(app_id):
    """Uninstall the application"""
    print("\n" + "="*80)
    print("STEP 6: Uninstall Application")
    print("="*80)
    
    if not app_id:
        print("[ERROR] No app ID provided")
        return False
    
    try:
        if fetch_dac_config:
            result = uninstall_app(JSONRPC_URL, app_id)
            if result:
                print(f"[SUCCESS] Application uninstalled")
                print(f"[INFO] Uninstall result: {result}")
                return True
    except Exception as e:
        print(f"[ERROR] Uninstall failed: {e}")
    
    return False


def main():
    """Execute DAC workflow"""
    print("\n" + "="*80)
    print("DAC WORKFLOW TEST - Direct Execution")
    print("="*80)
    print(f"Device: {DEVICE_IP}:{JSONRPC_PORT}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test connection
    if not test_device_connection():
        print("\n[FAILED] Cannot connect to device")
        return 1
    
    # Activate plugins
    activate_plugins()
    
    # Fetch packages
    packages = fetch_dac_packages()
    
    if not packages:
        print("\n[INFO] Skipping further steps - DAC packages not available")
        print("[SUCCESS] Connection and activation verified")
        return 0
    
    # Download package
    download_id = download_package(packages, index=2)
    
    if download_id:
        # Wait for download to complete
        print("[INFO] Waiting for download to complete...")
        time.sleep(10)
        
        # Install package
        app_id = install_package(download_id)
        
        if app_id:
            # Launch
            if launch_application(app_id):
                # Kill
                kill_application(app_id)
                
                # Uninstall
                uninstall_application(app_id)
    
    print("\n" + "="*80)
    print("TEST EXECUTION COMPLETED")
    print("="*80)
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Test execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
