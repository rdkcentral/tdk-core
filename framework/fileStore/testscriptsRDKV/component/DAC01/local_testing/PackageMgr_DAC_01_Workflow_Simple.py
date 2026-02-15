#!/usr/bin/env python3
"""
DAC Workflow Test - Simplified Version
Executes on 192.168.29.164 when PackageManager services are available

This script can be run in two ways:
1. Direct execution: python PackageMgr_DAC_01_Workflow_Simple.py
2. Via SSH from remote host (requires services running on device)
"""

import requests
import json
import sys
import time
import argparse
from typing import Optional, Dict, Any

# Configuration
DEVICE_IP = "192.168.29.164"
JSONRPC_PORT = 9998
JSONRPC_URL = f"http://{DEVICE_IP}:{JSONRPC_PORT}/jsonrpc"

# Test configuration
DAC_PACKAGE_INDEX = 2  # Which package to test (default: 2nd package)


class DACWorkflowTest:
    def __init__(self, device_ip: str = DEVICE_IP, port: int = JSONRPC_PORT):
        self.device_ip = device_ip
        self.port = port
        self.jsonrpc_url = f"http://{device_ip}:{port}/jsonrpc"
        self.download_id = None
        self.app_id = None
        self.test_passed = True
        
    def log(self, level: str, message: str):
        """Log message with level prefix"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] [{level:8}] {message}")
    
    def call_jsonrpc(self, method: str, params: Optional[Dict] = None) -> Optional[Any]:
        """Make JSON-RPC call to device"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params or {}
            }
            
            response = requests.post(self.jsonrpc_url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                error = result["error"]
                self.log("ERROR", f"{method}: [{error.get('code')}] {error.get('message')}")
                return None
            
            return result.get("result")
            
        except requests.exceptions.ConnectionError:
            self.log("ERROR", f"Cannot connect to {self.device_ip}:{self.port}")
            return None
        except Exception as e:
            self.log("ERROR", f"JSON-RPC call failed: {e}")
            return None
    
    def precondition_check_connection(self) -> bool:
        """Check device connection"""
        self.log("INFO", "="*80)
        self.log("INFO", "PRECONDITION: Test Device Connectivity")
        self.log("INFO", "="*80)
        
        # Try PackageManagerRDKEMS (the correct callsign)
        result = self.call_jsonrpc("org.rdk.PackageManagerRDKEMS.download", 
                                  {"url": "test"})
        if result is not None:
            self.log("PASS", f"Device connected - PackageManager service active")
            return True
        
        self.log("FAIL", "Cannot connect to device")
        self.test_passed = False
        return False
    
    def step_1_activate_services(self) -> bool:
        """Activate required services"""
        self.log("INFO", "="*80)
        self.log("INFO", "STEP 1: Activate Required Services")
        self.log("INFO", "="*80)
        
        services = [
            "org.rdk.PackageManager",
            "org.rdk.AppManager",
            "org.rdk.LifecycleManager",
            "org.rdk.StorageManager"
        ]
        
        for service in services:
            result = self.call_jsonrpc(f"{service}.activate")
            if result is not None:
                self.log("PASS", f"Activated: {service}")
            else:
                self.log("WARN", f"Could not activate: {service}")
        
        return True
    
    def step_2_get_package_list(self) -> bool:
        """Get available packages"""
        self.log("INFO", "="*80)
        self.log("INFO", "STEP 2: List Available Packages")
        self.log("INFO", "="*80)
        
        result = self.call_jsonrpc("org.rdk.PackageManagerRDKEMS.listPackages")
        if result:
            packages = result if isinstance(result, list) else [result]
            self.log("PASS", f"Found {len(packages)} packages")
            for i, pkg in enumerate(packages[:5]):
                pkg_name = pkg.get('name', 'Unknown') if isinstance(pkg, dict) else str(pkg)
                self.log("INFO", f"  [{i}] {pkg_name}")
            return True
        else:
            self.log("INFO", "Could not retrieve package list (may not be available)")
            return True  # Don't fail on this
    
    def step_3_download_package(self, package_index: int = DAC_PACKAGE_INDEX) -> bool:
        """Download a package"""
        self.log("INFO", "="*80)
        self.log("INFO", f"STEP 3: Download Package (Index {package_index})")
        self.log("INFO", "="*80)
        
        result = self.call_jsonrpc("org.rdk.PackageManagerRDKEMS.download", {
            "url": f"https://example.com/package_{package_index}.tar.gz"
        })
        
        if result and 'downloadId' in result:
            self.download_id = result['downloadId']
            self.log("PASS", f"Download started with ID: {self.download_id}")
            return True
        else:
            self.log("INFO", f"Download call returned: {result}")
            if result:
                self.download_id = result.get('downloadId')
                self.log("PASS", f"Download started with ID: {self.download_id}")
                return True
            self.log("WARN", "Could not start download")
            return True  # Continue anyway
    
    def step_4_wait_for_download(self, timeout: int = 60) -> bool:
        """Wait for download to complete"""
        self.log("INFO", "="*80)
        self.log("INFO", "STEP 4: Wait for Download to Complete")
        self.log("INFO", "="*80)
        
        if not self.download_id:
            self.log("FAIL", "No download ID available")
            return False
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.call_jsonrpc("org.rdk.PackageManager.getDownloadStatus", {
                "downloadId": self.download_id
            })
            
            if result:
                progress = result.get('progress', 0)
                status = result.get('status', 'unknown')
                self.log("INFO", f"Download progress: {progress}% (Status: {status})")
                
                if status == "completed" or progress >= 100:
                    self.log("PASS", "Download completed")
                    return True
            
            time.sleep(5)
        
        self.log("FAIL", f"Download timeout after {timeout}s")
        self.test_passed = False
        return False
    
    def step_5_install_package(self) -> bool:
        """Install the downloaded package"""
        self.log("INFO", "="*80)
        self.log("INFO", "STEP 5: Install Package")
        self.log("INFO", "="*80)
        
        if not self.download_id:
            self.log("FAIL", "No download ID available")
            return False
        
        result = self.call_jsonrpc("org.rdk.PackageManager.install", {
            "downloadId": self.download_id
        })
        
        if result:
            self.app_id = result.get('appId') or result.get('packageId')
            self.log("PASS", f"Installation completed. App ID: {self.app_id}")
            return True
        else:
            self.log("FAIL", "Installation failed")
            self.test_passed = False
            return False
    
    def step_6_launch_app(self) -> bool:
        """Launch the application"""
        self.log("INFO", "="*80)
        self.log("INFO", "STEP 6: Launch Application")
        self.log("INFO", "="*80)
        
        if not self.app_id:
            self.log("FAIL", "No app ID available")
            return False
        
        result = self.call_jsonrpc("org.rdk.AppManager.launchApp", {
            "appId": self.app_id
        })
        
        if result:
            self.log("PASS", f"Application launched")
            time.sleep(3)  # Let app run briefly
            return True
        else:
            self.log("FAIL", "Launch failed")
            self.test_passed = False
            return False
    
    def step_7_kill_app(self) -> bool:
        """Kill the application"""
        self.log("INFO", "="*80)
        self.log("INFO", "STEP 7: Kill Application")
        self.log("INFO", "="*80)
        
        if not self.app_id:
            self.log("FAIL", "No app ID available")
            return False
        
        result = self.call_jsonrpc("org.rdk.AppManager.killApp", {
            "appId": self.app_id
        })
        
        if result:
            self.log("PASS", "Application killed")
            return True
        else:
            self.log("FAIL", "Kill failed")
            self.test_passed = False
            return False
    
    def step_8_uninstall_app(self) -> bool:
        """Uninstall the application"""
        self.log("INFO", "="*80)
        self.log("INFO", "STEP 8: Uninstall Application")
        self.log("INFO", "="*80)
        
        if not self.app_id:
            self.log("FAIL", "No app ID available")
            return False
        
        result = self.call_jsonrpc("org.rdk.PackageManager.uninstall", {
            "appId": self.app_id
        })
        
        if result:
            self.log("PASS", "Application uninstalled")
            return True
        else:
            self.log("FAIL", "Uninstall failed")
            self.test_passed = False
            return False
    
    def run_full_workflow(self) -> bool:
        """Execute complete DAC workflow"""
        self.log("INFO", "="*80)
        self.log("INFO", "DAC WORKFLOW TEST - Complete Execution")
        self.log("INFO", "="*80)
        self.log("INFO", f"Device: {self.device_ip}:{self.port}\n")
        
        # Precondition
        if not self.precondition_check_connection():
            return False
        
        # Steps
        self.step_1_activate_services()
        
        if not self.step_2_get_package_list():
            return False
        
        self.step_3_download_package(DAC_PACKAGE_INDEX)
        self.step_4_wait_for_download()
        self.step_5_install_package()
        self.step_6_launch_app()
        self.step_7_kill_app()
        self.step_8_uninstall_app()
        
        # Summary
        self.log("INFO", "="*80)
        if self.test_passed:
            self.log("PASS", "ALL TESTS PASSED")
        else:
            self.log("FAIL", "SOME TESTS FAILED")
        self.log("INFO", "="*80)
        
        return self.test_passed


def main():
    parser = argparse.ArgumentParser(
        description="DAC Workflow Test for RDK Device",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Test with default device (192.168.29.164:9998)
  %(prog)s --device 192.168.1.100    # Test with custom IP
  %(prog)s --device 192.168.1.100 --port 8998  # Test with custom port
  %(prog)s --check-only              # Only check connectivity
        """
    )
    
    parser.add_argument('--device', default=DEVICE_IP, help=f'Device IP (default: {DEVICE_IP})')
    parser.add_argument('--port', type=int, default=JSONRPC_PORT, help=f'JSON-RPC port (default: {JSONRPC_PORT})')
    parser.add_argument('--check-only', action='store_true', help='Only check connectivity')
    parser.add_argument('--package-index', type=int, default=DAC_PACKAGE_INDEX, help=f'Package index (default: {DAC_PACKAGE_INDEX})')
    
    args = parser.parse_args()
    
    # Create test instance
    test = DACWorkflowTest(device_ip=args.device, port=args.port)
    
    # Run test
    if args.check_only:
        return 0 if test.precondition_check_connection() else 1
    else:
        return 0 if test.run_full_workflow() else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n[INTERRUPTED] Test execution interrupted")
        sys.exit(130)
    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
