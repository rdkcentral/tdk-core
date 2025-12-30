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
PROFILE_PATH = "../../../../profiles/source/Source_AudioSettings.yaml"

# ============= FILE PATHS (RELATIVE TO BASE_PATH) =============
# Virtual Environment
VENV_SCRIPT = os.path.join(BASE_PATH, "host", "activate_venv.sh")

# Test Directories
TARGET_DIR = os.path.join(BASE_PATH, "host", "tests", "L3_TestCases", "dsAudio")

# Configuration Files
RACK_CONFIG_PATH = os.path.join(BASE_PATH, "host", "tests", "configs", "example_rack_config.yml")
DEVICE_CONFIG_PATH = os.path.join(BASE_PATH, "host", "tests", "configs", "deviceConfig.yml")

# SCP Skip Configuration
UTBASEUTILS_PATH = os.path.join(BASE_PATH, "host", "tests", "raft", "framework", "plugins", "ut_raft", "utBaseUtils.py")

# Adding command in start function
UTSUITENAVIGATOR_PATH = os.path.join(BASE_PATH, "host", "tests", "raft", "framework", "plugins", "ut_raft", "utSuiteNavigator.py")

# Optional: stop on first failure (default is continue)
STOP_ON_FAILURE = True  # set False to run all regardless of failures

# ============= TEST CONFIGURATION =============
# Test Script Configuration
TEST_SCRIPT = [
    "dsAudio_test01_EnableDisableAndVerifyAudioPortStatus.py",
    "dsAudio_test02_PortConnectionStatus.py",
    "dsAudio_test03_MS12AudioCompression.py",
    "dsAudio_test04_MS12DialogueEnhancer.py",
    "dsAudio_test05_MS12DolbyVolume.py",
    "dsAudio_test06_MS12IntelligentEqualizer.py",
    "dsAudio_test07_MS12Volumeleveller.py",
    "dsAudio_test08_MS12BassEnhancer.py",
    "dsAudio_test09_MS12SurroundDecoder.py",
    "dsAudio_test10_MS12DRCMode.py",
    "dsAudio_test11_MS12SurroundVirtualizer.py",
    "dsAudio_test12_MS12MISteering.py",
    "dsAudio_test13_MS12GraphicEqualizer.py",
    "dsAudio_test14_MS12LEConfig.py",
    "dsAudio_test15_ARCPort.py",
    "dsAudio_test16_ARCSAD.py",
    "dsAudio_test17_OutputMode.py",
    "dsAudio_test18_AudioLevel.py",
    "dsAudio_test19_SpeakerAudioGain.py",
    "dsAudio_test20_MuteUnMute.py",
    "dsAudio_test21_AudioDelay.py",
    "dsAudio_test22_AudioFormat.py",
    "dsAudio_test23_AssociateMix.py",
    "dsAudio_test24_PrimarySecondaryLanguage.py",
    "dsAudio_test25_AudioMix.py",
    "dsAudio_test26_MS12AudioProfiles.py",
]
RACK_CONFIG_ARG = "../../configs/example_rack_config.yml"
DEVICE_CONFIG_ARG = "../../configs/deviceConfig.yml"

#============== utPlayerConfig location==========================
UTPLAYERCONFIG_FILE = "utPlayerConfig.yml"
UTPLAYERCONFIG_PATH = os.path.join(BASE_PATH, "host","tests","raft","framework","plugins","ut_raft","configs", UTPLAYERCONFIG_FILE)

#=====================STREAM====================================
#Update stream server hosting streams
STREAM_DOWNLOAD_PATH = ""

# Optional per-module toggle (defaults to True if omitted)
DOWNLOAD_STREAMS = True

# Keep downloaded streams on the device after tests (do NOT delete in testCleanAssets)
PRESERVE_STREAMS = True

# ================== STREAM RENAME RULES ===========================

STREAM_RENAME_MAP = {
    "multi_tone.ac3": "music_8k_stereo.ac3",
}
STREAM_RENAME_RULES = []

#==================================================================

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
    TARGET_DIR = os.path.join(BASE_PATH, "host", "tests", "L3_TestCases", "dsAudio")
    RACK_CONFIG_PATH = os.path.join(BASE_PATH, "host", "tests", "configs", "example_rack_config.yml")
    DEVICE_CONFIG_PATH = os.path.join(BASE_PATH, "host", "tests", "configs", "deviceConfig.yml")
    UTBASEUTILS_PATH = os.path.join(BASE_PATH, "host", "tests", "raft", "framework", "plugins", "ut_raft", "utBaseUtils.py")
    UTSUITENAVIGATOR_PATH = os.path.join(BASE_PATH, "host", "tests", "raft", "framework", "plugins", "ut_raft", "utSuiteNavigator.py")


if __name__ == "__main__":
    print_config()
