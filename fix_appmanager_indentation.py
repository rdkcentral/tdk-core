#!/usr/bin/env python3
"""
Fix AppManager Service Name Indentation
Corrects the indentation issue from the previous refactoring
"""

import os
import re
from pathlib import Path

# Directory containing the AppManager test files
test_dir = r"D:\Project\TDK\testCodeRepo\tdk-core\framework\fileStore\testscriptsRDKV\component\AppManager"

def fix_service_name_indentation(filepath):
    """Fix service name indentation in a single AppManager test file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the malformed indentation
        # Replace the broken format with the correct one
        pattern = r"service_name = get_ai2_setting\('APPMANAGER_SERVICE_NAME', 'wpeframework-appmanager\.service'\)\n    subprocess\.run\(\['systemctl', 'start', service_name\]"
        replacement = """service_name = get_ai2_setting('APPMANAGER_SERVICE_NAME', 'wpeframework-appmanager.service')
        subprocess.run(['systemctl', 'start', service_name]"""
        
        content = re.sub(pattern, replacement, content)
        
        # Also remove the hardcoded service name from the later status check
        pattern2 = r"status_result = subprocess\.run\(\['systemctl', 'status', 'wpeframework-appmanager\.service'\]"
        replacement2 = "status_result = subprocess.run(['systemctl', 'status', service_name]"
        
        content = re.sub(pattern2, replacement2, content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"[ERROR] Failed to process {filepath}: {str(e)}")
        return False

def main():
    """Fix indentation in all AppManager test files"""
    test_files = sorted(Path(test_dir).glob("RDKV_AppManager_*.py"))
    
    print(f"Fixing indentation in {len(test_files)} AppManager test files...\n")
    
    fixed_count = 0
    
    for test_file in test_files:
        if fix_service_name_indentation(str(test_file)):
            fixed_count += 1
            print(f"✓ {test_file.name}")
    
    print(f"\n{'='*70}")
    print(f"Indentation Fix Complete: {fixed_count} files updated")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
