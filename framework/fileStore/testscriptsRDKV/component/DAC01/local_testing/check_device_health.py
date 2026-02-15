#!/usr/bin/env python3
"""
Simple Device Health Check and Service Activation
"""

import requests
import json
import time

DEVICE_IP = "192.168.29.164"
JSONRPC_PORT = 9998
JSONRPC_URL = f"http://{DEVICE_IP}:{JSONRPC_PORT}/jsonrpc"


def make_jsonrpc_call(method, params=None):
    """Make a JSON-RPC call to Thunder Framework"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        print(f"[CALL] {method}")
        response = requests.post(JSONRPC_URL, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            error = result["error"]
            print(f"  [ERROR] Code {error.get('code')}: {error.get('message')}")
            return None
        
        return result.get("result")
    except requests.exceptions.ConnectionError:
        print(f"  [ERROR] Cannot connect to {DEVICE_IP}:{JSONRPC_PORT}")
        return None
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None


def main():
    print("\n" + "="*80)
    print("DEVICE HEALTH CHECK & SERVICE ACTIVATION")
    print("="*80)
    print(f"Target: {DEVICE_IP}:{JSONRPC_PORT}\n")
    
    # Try to get system version
    print("Step 1: Checking basic connectivity...")
    result = make_jsonrpc_call("org.rdk.System.1.systemVersion")
    if result:
        print(f"  [OK] SystemVersion: {result}\n")
    else:
        print("  [INFO] System service not active - attempting activation...\n")
        
        # Try to activate System
        result = make_jsonrpc_call("org.rdk.System.1.activate")
        if result is not None:
            print(f"  [OK] System activated: {result}\n")
            time.sleep(2)
            
            # Try again
            result = make_jsonrpc_call("org.rdk.System.1.systemVersion")
            if result:
                print(f"  [OK] SystemVersion: {result}\n")
    
    # List available services
    print("Step 2: Discovering available services...")
    result = make_jsonrpc_call("org.rdk.System.1.getServices")
    if result:
        if isinstance(result, list):
            services = result
        elif isinstance(result, dict) and 'services' in result:
            services = result['services']
        else:
            services = [result]
        
        print(f"  [OK] Found {len(services)} services:")
        for service in sorted(services)[:15]:
            if isinstance(service, dict):
                print(f"    - {service.get('callsign', 'Unknown')}")
            else:
                print(f"    - {service}")
    
    # Check PackageManager status
    print("\nStep 3: Checking PackageManager status...")
    result = make_jsonrpc_call("org.rdk.PackageManager.getPackageList")
    if result:
        print(f"  [OK] PackageManager is active\n")
    else:
        print("  [INFO] PackageManager may need activation")
        result = make_jsonrpc_call("org.rdk.PackageManager.activate")
        print(f"  [INFO] Activation attempt: {result}\n")
    
    print("="*80)
    print("CHECK COMPLETE")
    print("="*80)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FATAL] {e}")
        import traceback
        traceback.print_exc()
