#!/usr/bin/env python3
"""
AppManager Test Refactoring Script
Updates all AppManager test files to use configuration values from Video_Accelerator.config
"""

import os
import re
from pathlib import Path

# Directory containing the AppManager test files
test_dir = r"D:\Project\TDK\testCodeRepo\tdk-core\framework\fileStore\testscriptsRDKV\component\AppManager"

# Mapping of old/new configuration keys and old hardcoded defaults to new keys
replacements = [
    {
        'old_pattern': r"rpc_port = get_ai2_setting\('appManager\.jsonRpcPort', 9998\)",
        'new_string': "rpc_port = get_ai2_setting('APPMANAGER_JSONRPC_PORT', 9998)",
        'description': 'Update AppManager JSON RPC Port configuration key'
    },
    {
        'old_pattern': r"plugin_name = get_ai2_setting\('appManager\.testData\.pluginName', 'org\.rdk\.AppManager'\)",
        'new_string': "plugin_name = get_ai2_setting('APPMANAGER_PLUGIN_NAME', 'org.rdk.AppManager')",
        'description': 'Update AppManager Plugin Name configuration key'
    },
    {
        'old_pattern': r"app_id = get_ai2_setting\('appManager\.testData\.appId', 'com\.rdk\.app\.cobalt25_rpi4'\)",
        'new_string': "app_id = get_ai2_setting('APPMANAGER_TEST_APP_ID', 'com.rdk.app.cobalt25_rpi4')",
        'description': 'Update AppManager Test App ID configuration key'
    },
    {
        'old_pattern': r"get_ai2_setting\('appManager\.jsonRpcPort', 9998\)",
        'new_string': "get_ai2_setting('APPMANAGER_JSONRPC_PORT', 9998)",
        'description': 'Update any remaining AppManager JSON RPC Port references'
    },
    {
        'old_pattern': r"subprocess\.run\(\['systemctl', 'start', 'wpeframework-appmanager\.service'\]",
        'new_string': "service_name = get_ai2_setting('APPMANAGER_SERVICE_NAME', 'wpeframework-appmanager.service')\n    subprocess.run(['systemctl', 'start', service_name]",
        'description': 'Use config for service name'
    }
]

def update_file(filepath):
    """Update a single AppManager test file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # Apply replacements
        for replacement in replacements:
            pattern = replacement['old_pattern']
            new_string = replacement['new_string']
            
            if re.search(pattern, content):
                content = re.sub(pattern, new_string, content)
                changes_made.append(replacement['description'])
        
        # Only write if changes were made
        if changes_made and content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes_made
        
        return False, []
    
    except Exception as e:
        print(f"[ERROR] Failed to process {filepath}: {str(e)}")
        return False, []

def main():
    """Update all AppManager test files"""
    test_files = sorted(Path(test_dir).glob("RDKV_AppManager_*.py"))
    
    print(f"Found {len(test_files)} AppManager test files")
    print(f"Starting refactoring...\n")
    
    updated_count = 0
    failed_count = 0
    
    for test_file in test_files:
        success, changes = update_file(str(test_file))
        if success:
            updated_count += 1
            print(f"✓ {test_file.name}")
            for change in changes:
                print(f"  - {change}")
        else:
            if changes:  # Only count as error if there was an exception
                failed_count += 1
    
    print(f"\n{'='*70}")
    print(f"Refactoring Complete:")
    print(f"  • Updated: {updated_count} files")
    print(f"  • Failed: {failed_count} files")
    print(f"  • Total: {len(test_files)} files")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
