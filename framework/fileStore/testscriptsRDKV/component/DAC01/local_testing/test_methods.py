#!/usr/bin/env python3
"""Test available methods on PackageManager"""

import requests
import json

url = 'http://192.168.29.164:9998/jsonrpc'

methods_to_try = [
    'org.rdk.PackageManager.download',
    'PackageManager.download',
    'org.rdk.PackageManagerRDKEMS.download',
    'PackageManagerRDKEMS.1.download',
    'org.rdk.PackageManager.getPackages',
    'org.rdk.PackageManagerRDKEMS.getPackages',
]

print("\nTesting available methods:\n")

for method in methods_to_try:
    payload = {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': {}}
    try:
        resp = requests.post(url, json=payload, timeout=5)
        result = resp.json()
        if 'error' in result:
            code = result["error"].get("code")
            msg = result["error"].get("message")
            print(f'{method:50} [{code:6}] {msg}')
        else:
            print(f'{method:50} [OK] Result: {str(result.get("result"))[:40]}')
    except Exception as e:
        print(f'{method:50} [CONN] Error: {str(e)[:40]}')

print("\n")
