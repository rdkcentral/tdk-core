#!/usr/bin/env python3
"""
Activate services and run DAC workflow test
"""

import requests
import json
import time
import sys

DEVICE_IP = "192.168.29.164"
JSONRPC_PORT = 9998
JSONRPC_URL = f"http://{DEVICE_IP}:{JSONRPC_PORT}/jsonrpc"


def make_jsonrpc_call(method, params=None):
    """Make a JSON-RPC call"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        response = requests.post(JSONRPC_URL, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            error = result["error"]
            return None, f"[{error.get('code')}] {error.get('message')}"
        
        return result.get("result"), None
        
    except Exception as e:
        return None, str(e)


def main():
    print("\n" + "="*80)
    print("DAC WORKFLOW - Service Activation and Test")
    print("="*80)
    print(f"Device: {DEVICE_IP}:{JSONRPC_PORT}\n")
    
    # Activate StorageManager
    print("Step 1: Activating StorageManager...")
    result, error = make_jsonrpc_call("Controller.1.activate", 
                                      {"callsign": "org.rdk.StorageManager"})
    if error:
        print(f"  [WARNING] {error}")
    else:
        print(f"  [OK] StorageManager activation: {result}")
    
    time.sleep(1)
    
    # Activate PackageManager
    print("\nStep 2: Activating PackageManager...")
    result, error = make_jsonrpc_call("Controller.1.activate",
                                      {"callsign": "org.rdk.PackageManagerRDKEMS"})
    if error:
        print(f"  [WARNING] {error}")
    else:
        print(f"  [OK] PackageManager activation: {result}")
    
    time.sleep(1)
    
    # Check status
    print("\nStep 3: Checking service status...")
    result, error = make_jsonrpc_call("org.rdk.PackageManagerRDKEMS.getPackageList")
    if error:
        print(f"  [ERROR] PackageManager: {error}")
    else:
        print(f"  [OK] PackageManager responding")
        if isinstance(result, list):
            print(f"      Found {len(result)} packages")
    
    # Try to get storage
    print("\nStep 4: Checking StorageManager...")
    result, error = make_jsonrpc_call("org.rdk.StorageManager.getStorageDetails")
    if error:
        print(f"  [ERROR] StorageManager: {error}")
    else:
        print(f"  [OK] StorageManager responding")
        print(f"      Details: {result}")
    
    print("\n" + "="*80)
    print("ACTIVATION COMPLETE")
    print("="*80)
    print("\nNow try running the DAC workflow test:")
    print("  python PackageMgr_DAC_01_Workflow_Simple.py")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
