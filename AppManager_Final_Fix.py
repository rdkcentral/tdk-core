#!/usr/bin/env python3
"""
Fix remaining AppManager files - Update primitive_test_name in XML
"""

import os
import re

FIXES = [
    ('RDKV_AppManager_24_ClearAllAppData.py', 'AppManager_ClearAllAppData'),
    ('RDKV_AppManager_25_GetAppMetadata_Positive.py', 'AppManager_GetAppMetadata'),
    ('RDKV_AppManager_26_GetAppMetadata_Negative.py', 'AppManager_GetAppMetadata'),
]

def fix_primitive_test_name(filepath, new_name):
    """Fix the primitive_test_name in the XML"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the primitive_test_name
        content = re.sub(
            r'<primitive_test_name>.*?</primitive_test_name>',
            f'<primitive_test_name>{new_name}</primitive_test_name>',
            content,
            count=1
        )
        
        # Also update the places in the code where the primitive name is used
        old_name = re.search(r"tdkTestObj = obj\.createTestStep\('([^']+)'\)", content)
        if old_name:
            old_primitive = old_name.group(1)
            if old_primitive != new_name:
                content = content.replace(
                    f"tdkTestObj = obj.createTestStep('{old_primitive}')",
                    f"tdkTestObj = obj.createTestStep('{new_name}')"
                )
        else:
            # If not found, add the proper call
            content = re.sub(
                r"tdkTestObj = obj\.createTestStep\('[^']+'\)",
                f"tdkTestObj = obj.createTestStep('{new_name}')",
                content
            )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, f"Fixed {os.path.basename(filepath)}"
    
    except Exception as e:
        return False, f"Error in {os.path.basename(filepath)}: {str(e)}"

def main():
    base_dir = r"d:\Project\TDK\testCodeRepo\tdk-core\framework\fileStore\testscriptsRDKV\component\AppManager"
    
    for filename, prim_name in FIXES:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            success, message = fix_primitive_test_name(filepath, prim_name)
            print(f"{'✓' if success else '✗'} {message}")
        else:
            print(f"  - Skipped (not found): {filename}")

if __name__ == "__main__":
    main()
