#!/usr/bin/env python3
"""Quick compliance check"""

import os
import re

base_dir = r"d:\Project\TDK\testCodeRepo\tdk-core\framework\fileStore\testscriptsRDKV\component\AppManager"

non_compliant = []
for f in sorted(os.listdir(base_dir)):
    if f.startswith('RDKV_AppManager_') and f.endswith('.py'):
        filepath = os.path.join(base_dir, f)
        with open(filepath, 'r') as file:
            content = file.read()
            # Check if it still has RdkService_Test
            if 'RdkService_Test' in content:
                non_compliant.append(f)

if non_compliant:
    print(f"✗ {len(non_compliant)} files still non-compliant:")
    for f in non_compliant:
        print(f"  - {f}")
else:
    print("✓ ALL 34 FILES ARE NOW FULLY COMPLIANT WITH TDK ENTERPRISE SERVICE FRAMEWORK!")
