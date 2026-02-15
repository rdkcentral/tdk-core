#!/usr/bin/env python3
"""
AppManager Test Framework Conversion Script - Phase 2
Converts complete test logic from direct-API to TDK framework pattern
"""

import os
import re
from pathlib import Path

# Mapping of test files to primitive test names
TEST_MAPPINGS = {
    '01_Activate': 'AppManager_Activate',
    '02_LaunchApp_Positive': 'AppManager_LaunchApp',
    '03_LaunchApp_Negative': 'AppManager_LaunchApp',
    '04_PreloadApp_Positive': 'AppManager_PreloadApp',
    '05_PreloadApp_Negative': 'AppManager_PreloadApp',
    '06_CloseApp_Positive': 'AppManager_CloseApp',
    '07_CloseApp_Negative': 'AppManager_CloseApp',
    '08_TerminateApp_Positive': 'AppManager_TerminateApp',
    '09_TerminateApp_Negative': 'AppManager_TerminateApp',
    '10_KillApp_Positive': 'AppManager_KillApp',
    '11_KillApp_Negative': 'AppManager_KillApp',
    '12_IsInstalled_Positive': 'AppManager_IsInstalled',
    '13_IsInstalled_Negative': 'AppManager_IsInstalled',
    '14_GetInstalledApps': 'AppManager_GetInstalledApps',
    '15_GetLoadedApps': 'AppManager_GetLoadedApps',
    '16_SendIntent_Positive': 'AppManager_SendIntent',
    '17_SendIntent_Negative': 'AppManager_SendIntent',
    '18_StartSystemApp_Positive': 'AppManager_StartSystemApp',
    '19_StartSystemApp_Negative': 'AppManager_StartSystemApp',
    '20_StopSystemApp_Positive': 'AppManager_StopSystemApp',
    '21_StopSystemApp_Negative': 'AppManager_StopSystemApp',
    '22_ClearAppData_Positive': 'AppManager_ClearAppData',
    '23_ClearAppData_Negative': 'AppManager_ClearAppData',
    '27_GetAppProperty_Positive': 'AppManager_GetAppProperty',
    '28_GetAppProperty_Negative': 'AppManager_GetAppProperty',
    '29_SetAppProperty_Positive': 'AppManager_SetAppProperty',
    '30_SetAppProperty_Negative': 'AppManager_SetAppProperty',
    '31_GetMaxRunningApps': 'AppManager_GetMaxRunningApps',
    '32_GetMaxHibernatedApps': 'AppManager_GetMaxHibernatedApps',
    '33_GetMaxHibernatedFlashUsage': 'AppManager_GetMaxHibernatedFlashUsage',
    '34_GetMaxInactiveRamUsage': 'AppManager_GetMaxInactiveRamUsage',
}

def clean_and_replace_test_logic(content, primitive_name):
    """Replace all the old test logic with proper TDK framework pattern"""
    
    # Pattern 1: Remove undefined function calls and replace entire try block
    # Match from "try:" to "safe_unload_module" and replace completely
    
    try_block_pattern = r'    try:\s*rpc_port = get_ai2_setting\(.*?\)\s*jsonrpc_url = f".*?"\s*plugin_name = get_ai2_setting\(.*?\)\s*if not thunder_is_plugin_active\(.*?\):\s*print\("\[ERROR\] AppManager plugin is not active"\)\s*obj\.setLoadModuleStatus\("FAILURE"\)\s*else:\s*print\("\[SUCCESS\] AppManager plugin is active"\)\s*# Test:.*?\n.*?print\(".*?\[TEST\].*?scenarios"\).*?# TODO:.*?print\(".*?\[INFO\] Test implementation pending.*?"\)\s*obj\.setLoadModuleStatus\("SUCCESS"\)\s*except Exception as e:\s*print\(f"\[ERROR\] Test execution failed:.*?\)\s*obj\.setLoadModuleStatus\("FAILURE"\)\s*safe_unload_module\(obj, "AppManager"\)'
    
    # Safer pattern - just look for the try block more carefully
    # Pattern to match the try-except-safe_unload block
    try_pattern = r'try:\s*rpc_port = get_ai2_setting.*?safe_unload_module\(obj, "AppManager"\)'
    
    replacement = f'''try:
        # Test using TDK framework's createTestStep pattern
        print("\\n[TEST] AppManager API Test via TDK Framework")
        
        # Use TDK framework's createTestStep
        tdkTestObj = obj.createTestStep('{primitive_name}')
        
        # Add relevant parameters based on test type
        # Parameters will be specific to each test method
        tdkTestObj.addParameter("testType", "positive")
        
        # Execute test case using TDK framework
        tdkTestObj.executeTestCase(expectedResult)
        
        # Get result details from framework
        result = tdkTestObj.getResultDetails()
        
        if result and "SUCCESS" in str(result):
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"  [PASS] Test execution successful: {result}")
            obj.setLoadModuleStatus("SUCCESS")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"  [FAIL] Test execution failed: {result}")
            obj.setLoadModuleStatus("FAILURE")

    except Exception as e:
        print(f"[ERROR] Test execution failed: {{str(e)}}")
        obj.setLoadModuleStatus("FAILURE")

    obj.unloadModule("AppManager")'''
    
    # Use a more aggressive regex with DOTALL flag
    content = re.sub(
        try_pattern,
        replacement,
        content,
        flags=re.DOTALL,
        count=1
    )
    
    return content

def clean_remaining_artifacts(content):
    """Clean up any remaining undefined function calls"""
    # Remove any remaining get_ai2_setting, thunder_is_plugin_active, safe_unload_module calls
    content = re.sub(r'.*?get_ai2_setting\(.*?\).*?\n', '', content)
    content = re.sub(r'.*?thunder_is_plugin_active\(.*?\).*?\n', '', content)
    content = re.sub(r'.*?if not thunder_is_plugin_active.*?\n', '', content)
    content = re.sub(r'.*?print\("\[SUCCESS\] AppManager plugin is active"\).*?\n', '', content)
    content = re.sub(r'.*?print\("\[ERROR\] AppManager plugin is not active"\).*?\n', '', content)
    content = re.sub(r'.*?safe_unload_module.*?\n', '', content)
    content = re.sub(r'.*?jsonrpc_url = .*?\n', '', content)
    content = re.sub(r'.*?plugin_name = .*?\n', '', content)
    
    # Remove empty else blocks that may have been left behind
    content = re.sub(r'else:\s*\n\s*print\(""\)\s*', '', content)
    
    # Clean up extra blank lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    return content

def convert_file_phase2(filepath, primitive_name):
    """Convert a single AppManager test file - Phase 2"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Step 1: Clean and replace test logic
        content = clean_and_replace_test_logic(content, primitive_name)
        
        # Step 2: Clean remaining artifacts
        content = clean_remaining_artifacts(content)
        
        # Step 3: Ensure unloadModule is present
        if 'obj.unloadModule("AppManager")' not in content:
            # Add it before the final else block
            content = re.sub(
                r'(obj\.setLoadModuleStatus\("FAILURE"\))\n\nelse:',
                r'\1\n\n    obj.unloadModule("AppManager")\nelse:',
                content
            )
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, f"Phase 2: {os.path.basename(filepath)}"
    
    except Exception as e:
        return False, f"Phase 2 Error in {os.path.basename(filepath)}: {str(e)}"

def main():
    """Main conversion function for Phase 2"""
    base_dir = r"d:\Project\TDK\testCodeRepo\tdk-core\framework\fileStore\testscriptsRDKV\component\AppManager"
    
    results = []
    for test_key, prim_name in TEST_MAPPINGS.items():
        filename = f"RDKV_AppManager_{test_key}.py"
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            success, message = convert_file_phase2(filepath, prim_name)
            results.append((success, message))
            print(f"{'✓' if success else '✗'} {message}")
        else:
            print(f"  - Skipped (not found): {filename}")
    
    # Summary
    successful = sum(1 for s, _ in results if s)
    total = len([r for r in results if r])
    print(f"\n✓ Phase 2 Completed: {successful}/{total} files updated")

if __name__ == "__main__":
    main()
