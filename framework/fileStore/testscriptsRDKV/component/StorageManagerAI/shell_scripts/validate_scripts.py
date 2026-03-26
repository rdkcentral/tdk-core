#!/usr/bin/env python3
"""
StorageManager Python Scripts Validation
Verifies all Python test scripts are ready for TDK execution
"""

import os
import sys
import re
from pathlib import Path

def check_file_syntax(filepath):
    """Check if Python file has valid syntax"""
    try:
        with open(filepath, 'r') as f:
            code = f.read()
        compile(code, filepath, 'exec')
        return True, "Valid syntax"
    except SyntaxError as e:
        return False, str(e)

def check_tdk_placeholders(filepath):
    """Verify TDK placeholders are present"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    required_patterns = [
        (r'ip\s*=\s*<ipaddress>', 'IP placeholder'),
        (r'port\s*=\s*<port>', 'Port placeholder'),
        (r'from StorageManagerUtils|import StorageManagerUtils', 'StorageManagerUtils import'),
    ]
    
    missing = []
    for pattern, desc in required_patterns:
        if not re.search(pattern, content):
            missing.append(desc)
    
    return len(missing) == 0, missing

def check_required_imports(filepath):
    """Verify required imports are present"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    required_imports = ['tdklib', 'json']
    found_imports = []
    
    for imp in required_imports:
        if f"import {imp}" in content or f"from {imp}" in content:
            found_imports.append(imp)
    
    return len(found_imports) >= 1, found_imports

def check_error_handling(filepath):
    """Verify error handling is implemented"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    patterns = [
        (r'try:', 'try block'),
        (r'except.*:', 'except block'),
        (r'utils\.set_test_case_status', 'status setting'),
    ]
    
    found = []
    for pattern, desc in patterns:
        if re.search(pattern, content):
            found.append(desc)
    
    return len(found) >= 2, found

def main():
    script_dir = Path(__file__).parent / 'framework' / 'fileStore' / 'testscriptsRDKV' / 'component' / 'StorageManagerAI'
    
    if not script_dir.exists():
        # Try current directory
        script_dir = Path('.') / 'framework' / 'fileStore' / 'testscriptsRDKV' / 'component' / 'StorageManagerAI'
    
    if not script_dir.exists():
        print("ERROR: StorageManagerAI directory not found")
        return False
    
    print("=" * 70)
    print("StorageManager Python Scripts Validation")
    print("=" * 70)
    print(f"\nScript Directory: {script_dir}")
    print()
    
    # Find all test Python files
    test_files = sorted([f for f in script_dir.glob('StorageMgr_*.py')])
    utils_file = script_dir / 'StorageManagerUtils.py'
    
    if not test_files:
        print("ERROR: No test files found")
        return False
    
    print(f"Found {len(test_files)} test files and 1 utility file\n")
    
    all_passed = True
    results = []
    
    # Check utility file first
    print("Checking StorageManagerUtils.py...")
    syntax_ok, syntax_msg = check_file_syntax(utils_file)
    if syntax_ok:
        print("  ✓ Syntax: Valid")
    else:
        print(f"  ✗ Syntax: {syntax_msg}")
        all_passed = False
    
    print()
    
    # Check each test file
    for test_file in test_files:
        test_name = test_file.name
        print(f"Checking {test_name}...")
        
        checks = {
            'Syntax': check_file_syntax(test_file),
            'TDK Placeholders': check_tdk_placeholders(test_file),
            'Required Imports': check_required_imports(test_file),
            'Error Handling': check_error_handling(test_file),
        }
        
        for check_name, (passed, details) in checks.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check_name}")
            if not passed:
                if isinstance(details, list):
                    for detail in details:
                        print(f"     - Missing: {detail}")
                else:
                    print(f"     - {details}")
                all_passed = False
        
        results.append((test_name, all([v[0] for v in checks.values()])))
        print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\nTest Files Checked: {passed_count}/{total_count} passed")
    
    if all_passed:
        print("\n✓ All scripts are ready for TDK execution!")
        print("\nNext steps:")
        print("  1. Configure TDK framework with Python environment")
        print("  2. Replace <ipaddress> with actual device IP (e.g., 192.168.29.164)")
        print("  3. Replace <port> with actual JSONRPC port (e.g., 9998)")
        print("  4. Execute test scripts:")
        print("     python StorageMgr_01_ActivatePlugin.py")
        print("     python StorageMgr_02_Clear_AppStorage.py")
        print("     ... etc")
        return True
    else:
        print("\n✗ Some scripts have issues that need to be fixed")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
