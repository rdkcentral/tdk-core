#!/usr/bin/env python3
"""
AppManager Test Framework Compliance Validation Script
Validates all test files for TDK Enterprise Service framework compliance
"""

import os
import re
from pathlib import Path

def validate_file(filepath):
    """Validate a single test file for compliance"""
    compliance_issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check 1: Proper primitive_test_name (not RdkService_Test)
        if 'RdkService_Test' in content:
            compliance_issues.append("❌ Still has generic RdkService_Test primitive name")
        elif not re.search(r'<primitive_test_name>AppManager_\w+</primitive_test_name>', content):
            compliance_issues.append("❌ Missing or malformed AppManager primitive_test_name")
        else:
            compliance_issues.append("✓ Proper primitive_test_name")
        
        # Check 2: No ai2_0_utils imports
        if 'ai2_0_utils' in content:
            compliance_issues.append("❌ Still has ai2_0_utils imports")
        else:
            compliance_issues.append("✓ No ai2_0_utils imports")
        
        # Check 3: Uses createTestStep pattern
        if 'createTestStep(' in content:
            compliance_issues.append("✓ Uses createTestStep()")
        else:
            compliance_issues.append("❌ Missing createTestStep() call")
        
        # Check 4: Uses addParameter pattern
        if 'addParameter(' in content:
            compliance_issues.append("✓ Uses addParameter()")
        else:
            compliance_issues.append("❌ Missing addParameter() calls")
        
        # Check 5: Uses executeTestCase pattern
        if 'executeTestCase(' in content:
            compliance_issues.append("✓ Uses executeTestCase()")
        else:
            compliance_issues.append("❌ Missing executeTestCase() call")
        
        # Check 6: Uses obj.unloadModule (not safe_unload_module)
        if 'safe_unload_module(' in content:
            compliance_issues.append("❌ Still uses safe_unload_module()")
        elif 'obj.unloadModule(' in content:
            compliance_issues.append("✓ Uses obj.unloadModule()")
        else:
            compliance_issues.append("❌ Missing obj.unloadModule()")
        
        #  Check 7: No undefined get_ai2_setting calls
        if 'get_ai2_setting(' in content:
            compliance_issues.append("❌ Still has get_ai2_setting() calls")
        else:
            compliance_issues.append("✓ No get_ai2_setting() calls")
        
        # Check 8: No undefined thunder_is_plugin_active calls
        if 'thunder_is_plugin_active(' in content:
            compliance_issues.append("❌ Still has thunder_is_plugin_active() calls")
        else:
            compliance_issues.append("✓ No thunder_is_plugin_active() calls")
        
        # Check if compliant (no ❌ issues)
        is_compliant = all(not issue.startswith("❌") for issue in compliance_issues)
        
        return is_compliant, compliance_issues
    
    except Exception as e:
        return False, [f"❌ Error reading file: {str(e)}"]

def main():
    """Main validation function"""
    base_dir = r"d:\Project\TDK\testCodeRepo\tdk-core\framework\fileStore\testscriptsRDKV\component\AppManager"
    
    # Find all test files
    test_files = sorted([f for f in os.listdir(base_dir) if f.startswith('RDKV_AppManager_') and f.endswith('.py')])
    
    compliant_count = 0
    total_count = len(test_files)
    
    print("AppManager Test Framework Compliance Validation")
    print("=" * 70)
    
    for filename in test_files:
        filepath = os.path.join(base_dir, filename)
        is_compliant, issues = validate_file(filepath)
        
        status = "✓ COMPLIANT" if is_compliant else "✗ NON-COMPLIANT"
        print(f"\n{status}: {filename}")
        if not is_compliant:
            for issue in issues:
                print(f"  {issue}")
        
        if is_compliant:
            compliant_count += 1
    
    # Summary
    print(f"\n{'=' * 70}")
    print(f"Summary: {compliant_count}/{total_count} files are fully compliant")
    print(f"Compliance Rate: {100 * compliant_count / total_count:.1f}%")
    
    if compliant_count == total_count:
        print("✓✓✓ ALL FILES ARE COMPLIANT WITH TDK ENTERPRISE SERVICE FRAMEWORK ✓✓✓")

if __name__ == "__main__":
    main()
