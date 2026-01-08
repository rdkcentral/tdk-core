#!/usr/bin/env python3
"""
VTS Configuration File
Contains all configuration parameters for the VTS test framework.
"""

import os

# ============= BASE PATH CONFIGURATION =============
# Set the base path for all VTS operations
BASE_PATH = os.getcwd() + "rdk-halif-test-device_settings"

#========== REPO DETAILS ========================

REPO_URL = "https://github.com/rdkcentral/rdk-halif-test-device_settings.git"
REPO_DIR = "rdk-halif-test-device_settings"
CHECKOUT_VER = "6.0.0"

# ============= DEVICE CONFIGURATION =============
# Rack Configuration Parameters
#Update device ip below inside quotes
DEVICE_IP = ""
#Update device SoC inside quotes ex : "Amlogic", "Realtek" , "Broadcom"
DEVICE_PLATFORM = ""
DEVICE_DESCRIPTION = "xxx"
SSH_USERNAME = "root"
SSH_PASSWORD = ""
SSH_PORT = 22
LOG_DIRECTORY = "./logs"

# Device Configuration Parameters  
#Update device SoC inside quotes ex : "Amlogic", "Realtek" , "Broadcom"
CPE_PLATFORM = ""
CPE_MODEL = "test"
#Update device SoC inside quotes ex : "amlogic", "realtek", "broadcom"
SOC_VENDOR = ""
TARGET_DIRECTORY ="/VTS_Package/"
PROFILE_PATH = "../../../../profiles/source/Source_HostSettings.yaml"

# ============= FILE PATHS (RELATIVE TO BASE_PATH) =============
# Virtual Environment
VENV_SCRIPT = os.path.join(BASE_PATH, "host", "activate_venv.sh")

# Test Directories
TARGET_DIR = os.path.join(BASE_PATH, "host", "tests", "L3_TestCases", "dsHost")

# Configuration Files
RACK_CONFIG_PATH = os.path.join(BASE_PATH, "host", "tests", "configs", "example_rack_config.yml")
DEVICE_CONFIG_PATH = os.path.join(BASE_PATH, "host", "tests", "configs", "deviceConfig.yml")

# SCP Skip Configuration
UTBASEUTILS_PATH = os.path.join(BASE_PATH, "host", "tests", "raft", "framework", "plugins", "ut_raft", "utBaseUtils.py")

# Adding command in start function
UTSUITENAVIGATOR_PATH = os.path.join(BASE_PATH, "host", "tests", "raft", "framework", "plugins", "ut_raft", "utSuiteNavigator.py")

# ============= TEST CONFIGURATION =============
# Test Script Configuration
TEST_SCRIPT = "dsHost_test1_VerifyTemperature.py"
RACK_CONFIG_ARG = "../../configs/example_rack_config.yml"
DEVICE_CONFIG_ARG = "../../configs/deviceConfig.yml"

#Update stream server hosting streams
STREAM_DOWNLOAD_PATH = ""
# Log Configuration
LOG_FILE = "menu.log"

# ============= ADVANCED CONFIGURATION =============
# Terminal Configuration
TERMINAL_BUFFER_SIZE = 1024
SELECT_TIMEOUT = 0.1

# YAML Configuration
YAML_INDENT = 4
YAML_DEFAULT_FLOW_STYLE = False

# ============= HELPER FUNCTIONS =============
def get_full_path(relative_path):
    """
    Get full path relative to BASE_PATH
    
    Args:
        relative_path (str): Path relative to BASE_PATH
        
    Returns:
        str: Full absolute path
    """
    return os.path.join(BASE_PATH, relative_path)

def validate_paths():
    """
    Validate that all critical paths exist
    
    Returns:
        dict: Dictionary with path validation results
    """
    paths_to_check = {
        'BASE_PATH': BASE_PATH,
        'VENV_SCRIPT': VENV_SCRIPT,
        'TARGET_DIR': TARGET_DIR,
        'UTBASEUTILS_PATH': UTBASEUTILS_PATH,
        'UTSUITENAVIGATOR_PATH': UTSUITENAVIGATOR_PATH
    }
    
    results = {}
    for name, path in paths_to_check.items():
        results[name] = os.path.exists(path)
    
    return results

def print_config():
    """Print current configuration for debugging"""
    print("\n" + "="*60)
    print("VTS CONFIGURATION")
    print("="*60)
    print(f"Base Path: {BASE_PATH}")
    print(f"Device IP: {DEVICE_IP}")
    print(f"Platform: {DEVICE_PLATFORM}")
    print(f"SSH User: {SSH_USERNAME}")
    print(f"Target Dir: {TARGET_DIR}")
    print(f"VENV Script: {VENV_SCRIPT}")
    print("="*60)
    
    # Show path validation
    validation = validate_paths()
    print("Path Validation:")
    for path_name, exists in validation.items():
        status = "✓" if exists else "✗"
        print(f"  {status} {path_name}: {exists}")
    print("="*60)

# ============= ENVIRONMENT-SPECIFIC OVERRIDES =============
# You can override any configuration based on environment variables
# Example: Override device IP from environment
if os.environ.get('VTS_DEVICE_IP'):
    DEVICE_IP = os.environ.get('VTS_DEVICE_IP')

if os.environ.get('VTS_BASE_PATH'):
    BASE_PATH = os.environ.get('VTS_BASE_PATH')
    # Recalculate all paths if base path changes
    VENV_SCRIPT = os.path.join(BASE_PATH, "host", "activate_venv.sh")
    TARGET_DIR = os.path.join(BASE_PATH, "host", "tests", "L3_TestCases", "dsHost")
    RACK_CONFIG_PATH = os.path.join(BASE_PATH, "host", "tests", "configs", "example_rack_config.yml")
    DEVICE_CONFIG_PATH = os.path.join(BASE_PATH, "host", "tests", "configs", "deviceConfig.yml")
    UTBASEUTILS_PATH = os.path.join(BASE_PATH, "host", "tests", "raft", "framework", "plugins", "ut_raft", "utBaseUtils.py")
    UTSUITENAVIGATOR_PATH = os.path.join(BASE_PATH, "host", "tests", "raft", "framework", "plugins", "ut_raft", "utSuiteNavigator.py")


if __name__ == "__main__":
    print_config()
