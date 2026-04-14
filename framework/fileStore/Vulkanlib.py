##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#########################################################################

"""
Vulkan Library Module for TDK Testing Framework

This module provides functionality for:
- Vulkan/VkMark benchmark execution on DUT devices
- SSH connection management and command execution
- Display creation using RDKWindowManager or Westeros
- Device configuration management
- Test environment setup and teardown
"""

# Standard library imports
import json
import sys
import re
import requests
import time
import os
import subprocess
import inspect
import configparser
from time import sleep
import pexpect

# Custom imports
from SSHUtility import *
import SSHUtility

# Global variables for device configuration and connection management
deviceIP = ""                      # IP address of the device under test
SSHConfigValues = {}               # SSH configuration parameters from config file
deviceMAC = ""                     # MAC address of the device
password = ""                      # SSH password for device access
user_name = ""                     # SSH username for device access
sshMethod = ""                     # SSH connection method (e.g., 'directSSH')
runtime_dir = "/tmp"               # Runtime directory for Wayland display
wayland_display = "test"           # Wayland display
device_model = "Video_Accelerator" # Device Model
display_created = False            # Flag to track if display has been created
height = 0
width = 0

resolution="1080p"
api="vulkan"

#---------------------------------------------------------------------------------------
# MODULE INITIALIZATION
#---------------------------------------------------------------------------------------
def init_module(libobj, port, deviceInfo):
    """
    Initialize the Vulkan library module with device configuration.
    
    Args:
        libobj: Library object containing device connection information
        port: Port number for device communication
        deviceInfo: Dictionary containing device details (devicename, boxtype, mac)
    
    Returns:
        None
    
    Raises:
        SystemExit: If MAC address is missing or invalid
    """
    global deviceIP, devicePort, deviceName, deviceMAC, deviceType, libObj
    
    # Initialize device connection parameters
    deviceIP = libobj.ip
    devicePort = port
    deviceName = deviceInfo["devicename"]
    deviceType = deviceInfo["boxtype"]
    libObj = libobj
    
    try:
        # Configure MAC address for SSH utility
        deviceMAC = deviceInfo["mac"]
        SSHUtility.deviceMAC = deviceMAC
        SSHUtility.realpath = libobj.realpath
        deviceMAC = deviceMAC.replace(":", "")  # Remove colons from MAC address
        
    except Exception as e:
        print(f"\n[ERROR] Exception occurred while getting MAC address: {e}")
        print("PLEASE UPDATE MAC ADDRESS in DEVICE CONFIGURATION")
        os._exit(1)  # Use os._exit instead of os.exit for cleaner termination

#----------------------------------------------------------------------
# DEVICE CONFIGURATION MANAGEMENT
#----------------------------------------------------------------------
def get_device_config_value(basePath, configKeyList):
    """
    Read configuration values from device-specific configuration file.
    
    This function searches for device configuration files in the following priority:
    1. Device-specific config file: <deviceName>.config
    2. Device-type config file: <deviceType>.config
    
    Args:
        basePath (str): Base path of the test manager
        configKeyList (list or str): Configuration key(s) to retrieve
    
    Returns:
        list or str: Configuration value(s) or failure message
    """
    # Handle backward compatibility for single key
    is_single_key = isinstance(configKeyList, str)
    if is_single_key:
        configKeyList = [configKeyList]
    
    # Construct configuration file paths
    configPath = os.path.join(basePath, "fileStore/tdkvRDKServiceConfig")
    deviceNameConfigFile = os.path.join(configPath, f"{deviceName}.config")
    deviceTypeConfigFile = os.path.join(configPath, f"{deviceType}.config")
    
    # Check for device configuration files in priority order
    if os.path.exists(deviceNameConfigFile):
        deviceConfigFile = deviceNameConfigFile
        print(f"[INFO] Using device-specific config: {deviceNameConfigFile}")
    elif os.path.exists(deviceTypeConfigFile):
        deviceConfigFile = deviceTypeConfigFile
        print(f"[INFO] Using device-type config: {deviceTypeConfigFile}")
    else:
        error_msg = f"FAILURE: No device config file found: {deviceNameConfigFile} or {deviceTypeConfigFile}"
        print(error_msg)
        return error_msg
    
    # Validate input parameters
    if not deviceConfigFile or not configKeyList:
        error_msg = "FAILURE: DeviceConfig file or keylist cannot be empty"
        print(error_msg)
        return error_msg
    
    try:
        # Parse configuration file
        config = configparser.ConfigParser()
        config.read(deviceConfigFile)
        
        if not config.sections():
            error_msg = f"FAILURE: No sections found in config file {deviceConfigFile}"
            print(error_msg)
            return error_msg
        
        deviceConfig = config.sections()[0]
        configKeyValues = []
        
        for configKey in configKeyList:
            try:
                configValue = config.get(deviceConfig, configKey)
                print(f"[INFO] Retrieved {configKey} = {configValue}")
                configKeyValues.append(configValue)
            except configparser.NoOptionError:
                error_msg = f"FAILURE: Configuration key '{configKey}' not found in {deviceConfigFile}"
                print(error_msg)
                return error_msg
        
        # Return single value for backward compatibility
        return configKeyValues[0] if is_single_key else configKeyValues
        
    except Exception as e:
        error_msg = f"FAILURE: Exception occurred in {inspect.stack()[0][3]}: {str(e)}"
        print(error_msg)
        return error_msg


#---------------------------------------------------------------
# SSH CREDENTIAL MANAGEMENT
#---------------------------------------------------------------
def obtain_Credentials():
    """
    Retrieve SSH configuration values from device configuration file.
    
    This function reads SSH connection parameters including method,
    username, and password from the device configuration file.
    
    Returns:
        dict: SSH configuration values on success
        str: "FAILURE" string on failure
    """
    global SSHConfigValues, password, user_name, sshMethod
    
    print("[INFO] Retrieving SSH configuration values from config file...")
    
    # Required SSH configuration keys
    configKeyList = ["SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD"]
    config_status = "SUCCESS"
    
    configKeyValues = get_device_config_value(libObj.realpath, configKeyList)
    
    # Check if configuration retrieval failed
    if isinstance(configKeyValues, str) and "FAILURE" in configKeyValues:
        print("[FAILURE] Failed to retrieve SSH configuration from device config")
        return "FAILURE"

    # Retrieve each configuration value
    for i, configValue in enumerate(configKeyValues):
        configKey = configKeyList[i]
        SSHConfigValues[configKey] = configValue
        
        if "FAILURE" not in configValue and configValue:
            print(f"[SUCCESS] Retrieved {configKey} configuration")
        else:
            print(f"[FAILURE] Failed to retrieve {configKey} configuration")
            if not configValue:
                print(f"[INFO] Please configure the {configKey} key in the device config file")
            config_status = "FAILURE"
            break
    
    # Validate and set SSH parameters
    if config_status == "SUCCESS":
        if SSHConfigValues["SSH_METHOD"] == "directSSH":
            sshMethod = SSHConfigValues["SSH_METHOD"]
            user_name = SSHConfigValues["SSH_USERNAME"]
            # Handle password configuration
            password = "" if SSHConfigValues["SSH_PASSWORD"] == "None" else SSHConfigValues["SSH_PASSWORD"]
            print(f"[INFO] SSH configured for DUT")
        else:
            print("[FAILURE] Currently only supports directSSH method")
            config_status = "FAILURE"
    
    return SSHConfigValues if config_status == "SUCCESS" else "FAILURE"

#-------------------------------------------------------------------
# COMMAND EXECUTION ON DEVICE UNDER TEST (DUT)
#-------------------------------------------------------------------
def execute_Cmnd_InDUT(command):
    """
    Execute a command on the Device Under Test (DUT) via SSH.
    
    This function handles SSH connection setup, command execution,
    and output retrieval from the target device.
    
    Args:
        command (str): Command to execute on the DUT
    
    Returns:
        str: Command output from DUT or empty string on failure
    """
    global SSHConfigValues
    output = ""
    
    # Ensure SSH credentials are available
    if not SSHConfigValues:
        print("[INFO] SSH credentials not cached, obtaining from config...")
        credentials = obtain_Credentials()
    else:
        credentials = SSHConfigValues
    
    # Validate credentials and connection method
    if isinstance(credentials, dict) and credentials.get("SSH_METHOD") == "directSSH":
        user_name = credentials.get("SSH_USERNAME")
        host_name = deviceIP
        ssh_method = credentials.get("SSH_METHOD")
        ssh_password = credentials.get("SSH_PASSWORD")
        
        print(f"[INFO] Executing command on DUT")
        print(command)
        
    else:
        print("[WARNING] Secure SSH to CPE not yet implemented")
        return ""
    
    try:
        # Execute command via SSH utility
        output = ssh_and_execute(ssh_method, host_name, user_name, ssh_password, command)
        
        if output:
            print(f"[INFO] Command executed successfully, output length: {len(output)} characters")
        else:
            print("[WARNING] Command executed but no output received")
            
    except Exception as e:
        print(f"[ERROR] SSH session failed: {str(e)}")
        output = ""
    
    return output

def parse_tiles_stats(output):
    """
    Parse FPS and CPU statistics from tiles_benchmark output.
    
    Args:
        output (str): Command output containing benchmark results
    
    Returns:
        str: "SUCCESS" if parsing successful, "FAILURE" otherwise
    """
    if not output:
        print("FAILURE: No output to parse")
        return "FAILURE"
    
    fps_match = re.search(r"\[VK\]\s*Average FPS\s*([\d\.]+)", output)
    cpu_match = re.search(r"\[VK\]\s*Average CPU\s*([\d\.]+)", output)

    if not fps_match or not cpu_match:
        print("FAILURE: Unable to parse Average FPS or CPU from tiles_benchmark output")
        print(f"[DEBUG] Searching in output: {output[-200:]}...")  # Show last 200 chars
        return "FAILURE"

    try:
        avg_fps = float(fps_match.group(1))
        avg_cpu = float(cpu_match.group(1))
        
        print(f"Average FPS: {avg_fps}")
        print(f"Average CPU: {avg_cpu}%")
        print("SUCCESS: Parsed and validated FPS and CPU usage from tiles_benchmark")
        return "SUCCESS"
    except ValueError as e:
        print(f"FAILURE: Error converting parsed values to float: {e}")
        return "FAILURE"

def parse_motion_stats(output):
    """
    Parse FPS and CPU statistics from motion_benchmark output.
    
    Args:
        output (str): Command output containing benchmark results
    
    Returns:
        str: "SUCCESS" if parsing successful, "FAILURE" otherwise
    """
    if not output:
        print("FAILURE: No output to parse")
        return "FAILURE"
        
    # Get last non-empty line
    lines = [line for line in output.strip().splitlines() if line.strip()]
    if not lines:
        print("FAILURE: No valid lines found in motion_benchmark output")
        return "FAILURE"
        
    last_line = lines[-1]
    print(f"[DEBUG] Parsing last line: {last_line}")

    # Regex for final line format
    match = re.search(r"FPS:\s*([\d\.]+)%\s*CPU End:\s*([\d\.]+)%", last_line)

    if not match:
        print("FAILURE: Unable to parse final FPS or CPU from motion_benchmark output")
        print(f"[DEBUG] Expected format: 'FPS: X.X% CPU End: Y.Y%'")
        return "FAILURE"

    try:
        final_fps = float(match.group(1))
        final_cpu = float(match.group(2))
        
        print(f"Final FPS: {final_fps}%")
        print(f"Final CPU: {final_cpu}%")
        print("SUCCESS: Parsed and validated FPS and CPU usage from motion_benchmark")
        return "SUCCESS"
    except ValueError as e:
        print(f"FAILURE: Error converting parsed values to float: {e}")
        return "FAILURE"

def parse_fps_cpu_stats(output):
    """
    Parse FPS and CPU statistics from multithread or overlay benchmark output.
    
    This function extracts performance metrics from various benchmark tests that report
    Average FPS and Average CPU Usage patterns. It's designed to handle both:
    - Multithread benchmark tests (e.g., vkmultithread, oglmultithread)
    - Overlay benchmark tests (e.g., vkoverlay, gloverlay, overlay_test)
    
    Both test types typically output similar performance metrics in the same format,
    making this parser suitable for multiple benchmark scenarios.
    
    Expected output format:
    - "Average FPS: X.XX" where X.XX is a decimal number
    - "Average CPU Usage: Y.YY%" or "Average CPU: Y.YY%" where Y.YY is a decimal number with % sign
    
    Args:
        output (str): Command output containing benchmark results from multithread or overlay tests
    
    Returns:
        str: "SUCCESS" if parsing successful and metrics found,
             "FAILURE" if parsing fails or output is invalid
    
    Example:
        >>> output = "Test completed. Average FPS: 45.67\\nAverage CPU Usage: 23.45%"
        >>> result = parse_fps_cpu_stats(output)
        Average FPS: 45.67
        Average CPU Usage: 23.45%
        SUCCESS: Parsed multithread benchmark statistics
        >>> print(result)
        SUCCESS
    """
    # Input validation - check for empty or invalid output
    if not output or not isinstance(output, str):
        print("FAILURE: No valid output provided for FPS/CPU stats parsing")
        return "FAILURE"
   
    # Get app name
    if "multithread" in output:
        appname = "multithread"
    else:
        appname = "overlay"

    # Log the parsing attempt for debugging
    print(f"[INFO] Parsing {appname} benchmark statistics...")
    print(f"[DEBUG] Output length: {len(output)} characters")
    
    # Define regex patterns for extracting performance metrics
    # Pattern 1: Average FPS - matches "Average FPS: XX.XX" format
    fps_pattern = r"Average FPS:\s*([\d\.]+)"
    
    # Pattern 2: Average CPU Usage - matches both "Average CPU Usage: XX.XX%" and "Average CPU: XX.XX%" formats
    cpu_pattern = r"Average CPU(?:\s+Usage)?:\s*([\d\.]+)%"
    
    # Search for FPS metrics in the output
    fps_match = re.search(fps_pattern, output, re.IGNORECASE)
    
    # Search for CPU usage metrics in the output
    cpu_match = re.search(cpu_pattern, output, re.IGNORECASE)

    # Validate that both required metrics were found
    if not fps_match or not cpu_match:
        print("FAILURE: Unable to parse required FPS/CPU metrics from multithread/overlay benchmark")
        
        # Provide specific feedback about what was missing
        if not fps_match:
            print("[DEBUG] Missing or invalid Average FPS pattern in output")
            print(f"[DEBUG] Expected pattern: {fps_pattern}")
        
        if not cpu_match:
            print("[DEBUG] Missing or invalid Average CPU pattern in output")
            print(f"[DEBUG] Expected pattern: {cpu_pattern}")
        
        # Show a sample of the output for debugging
        sample_output = output[-300:] if len(output) > 300 else output
        print(f"[DEBUG] Output sample: ...{sample_output}")
        
        return "FAILURE"

    # Extract and validate the numeric values
    try:
        # Parse FPS value and validate it's a positive number
        avg_fps_str = fps_match.group(1)
        avg_fps = float(avg_fps_str)
        
        # Parse CPU usage value and validate it's within reasonable range (0-100%)
        avg_cpu_str = cpu_match.group(1)
        avg_cpu = float(avg_cpu_str)
        
        # Validate FPS is non-negative
        if avg_fps < 0:
            print(f"FAILURE: Invalid FPS value: {avg_fps} (must be non-negative)")
            return "FAILURE"
        
        # Validate CPU usage is within reasonable range
        if avg_cpu < 0 or avg_cpu > 100:
            print(f"WARNING: CPU usage {avg_cpu}% is outside typical range (0-100%)")
        
        # Display the successfully parsed metrics
        print(f"Average FPS: {avg_fps}")
        print(f"Average CPU: {avg_cpu}%")
        print(f"SUCCESS: Parsed and validated {appname} benchmark statistics")
        
        # Optional: Log performance thresholds for analysis
        if avg_fps > 0:
            performance_rating = "High" if avg_fps >= 30 else "Medium" if avg_fps >= 15 else "Low"
            print(f"[INFO] Performance rating: {performance_rating} ({avg_fps} FPS)")
        
        if avg_cpu <= 80:
            efficiency_rating = "Efficient" if avg_cpu <= 50 else "Moderate"
            print(f"[INFO] CPU efficiency: {efficiency_rating} ({avg_cpu}% usage)")
        elif avg_cpu <= 95:
            print(f"[INFO] CPU efficiency: High load ({avg_cpu}% usage)")
        else:
            print(f"[WARNING] CPU efficiency: Critical load ({avg_cpu}% usage)")
        
        return "SUCCESS"
        
    except ValueError as e:
        # Handle cases where extracted values cannot be converted to float
        print(f"FAILURE: Error converting parsed values to numbers: {e}")
        print(f"[DEBUG] FPS string: '{fps_match.group(1) if fps_match else 'N/A'}'")
        print(f"[DEBUG] CPU string: '{cpu_match.group(1) if cpu_match else 'N/A'}'")
        return "FAILURE"
    
    except Exception as e:
        # Handle any other unexpected errors
        print(f"FAILURE: Unexpected error during FPS/CPU stats parsing: {e}")
        return "FAILURE"

#-------------------------------------------------------------------
# DISPLAY MANAGEMENT FUNCTIONS
#-------------------------------------------------------------------
def checkDisplay():
    """
    Check if a Wayland display is already created and available.
    
    Returns:
        bool: True if display exists and is accessible, False otherwise
    """
    global display_created
    
    # JSON-RPC call to check for existing displays
    command = ('curl --header "Content-Type: application/json" '
              '--request POST --data \'{"jsonrpc":"2.0", "id":3, '
              '"method":"org.rdk.RDKWindowManager.1.getApps"}\' '
              'http://127.0.0.1:9998/jsonrpc')
    
    output = execute_Cmnd_InDUT(command)
    if output:
        last_line = output.strip().splitlines()[-1] if output.strip() else ""
        print(f"[INFO] org.rdk.RDKWindowManager.1.getApps result : {last_line}")
        if 'test' in last_line:
            display_created = True
            return True
    else:
        print("[WARNING] No response from RDKWindowManager.getApps")
    return False

def createDisplay():
    """
    Create a Wayland display using RDKWindowManager or fallback to Westeros.
    
    This function first checks if RDKWindowManager is available, and if so,
    creates a display using it. Otherwise, it returns a message indicating
    that RDKWindowManager is not present.
    
    Returns:
        str: "SUCCESS" on successful display creation,
             "FAILURE" on failure,
             "RDKWindowManager not present" if RDKWindowManager is unavailable
    """
    # Check if RDKWindowManager is available
    RDKWindowManager_json = "/etc/WPEFramework/plugins/RDKWindowManager.json"
    
    print(f"[INFO] Checking for RDKWindowManager at {RDKWindowManager_json}")
    command = f"ls -l {RDKWindowManager_json}"
    output = execute_Cmnd_InDUT(command)
    
    if "No such file or directory" in output:
        print("[INFO] RDKWindowManager not available, will use Westeros fallback")
        return "RDKWindowManager not present"

    # Detect runtime directory from WPE Framework service configuration
    print("[INFO] Detecting XDG_RUNTIME_DIR from WPE Framework service...")
    command = "grep XDG_RUNTIME_DIR /lib/systemd/system/wpeframework.service | sed -E 's/.*=//; s/\"//g'"
    output = execute_Cmnd_InDUT(command)
    
    global runtime_dir
    if output.strip():
        runtime_dir = output.strip().splitlines()[-1]
        print(f"[INFO] Detected RUNTIME_DIR: {runtime_dir}")
    else:
        print("[WARNING] Could not detect RUNTIME_DIR, using default: /run")
        runtime_dir = "/run"

    print("\n[PRE-REQUISITE 1] Creating display using RDKWindowManager")

    # Check if display already exists
    if not checkDisplay():
        print("[INFO] Creating new display via RDKWindowManager...")
        
        # JSON-RPC call to create display
        command = ('curl --header "Content-Type: application/json" '
                   '--request POST --data \'{"jsonrpc":"2.0", "id":3, '
                   '"method":"org.rdk.RDKWindowManager.1.createDisplay", '
                   f'"params" : {{"displayParams" : {{ "client": "test", '
                   f'"displayName": "test", "displayWidth": {width}, "displayHeight" : {height}}} }}\' '
                   'http://127.0.0.1:9998/jsonrpc')
        
        output = execute_Cmnd_InDUT(command)
        if output:
            last_line = output.strip().splitlines()[-1] if output.strip() else ""
            print(f"[INFO] org.rdk.RDKWindowManager.1.createDisplay result : {last_line}")
        else:
            print("[WARNING] No response from RDKWindowManager.createDisplay")
            return "FAILURE"
        
        # Check for creation errors
        if 'null' not in last_line or 'ERROR_GENERAL' in last_line:
            print("[FAILURE] Display creation failed - RDKWindowManager error")
            return "FAILURE"
        
        # Verify display was created successfully
        if checkDisplay():
            print("[SUCCESS] Display creation completed successfully")
            return "SUCCESS"
        else:
            print("[FAILURE] Display creation failed - verification failed")
            return "FAILURE"
    else:
        print("[SUCCESS] Display already exists and is accessible")
        return "SUCCESS"

def run_test(command):
    """
    Execute a test command with proper Wayland display environment setup.
    
    Args:
        command (str): Test command to execute
    
    Returns:
        str: "SUCCESS" on completion (currently always returns SUCCESS)
    
    """
    global width
    global height
    global runtime_dir
    global wayland_display
    test_command = f"export XDG_RUNTIME_DIR={runtime_dir}; export WAYLAND_DISPLAY={wayland_display}; {command} "
    if width and height:
        test_command = f"export XDG_RUNTIME_DIR={runtime_dir}; export WAYLAND_DISPLAY={wayland_display}; {command} --width {width} --height {height} "

    global device_model
    # Add Raspberry Pi specific DRM card setting
    if device_model == "RPI":
        print("[INFO] Adding Raspberry Pi DRM card configuration")
        test_command = "export WESTEROS_DRM_CARD=/dev/dri/card1; " + test_command
    
    output = execute_Cmnd_InDUT(test_command)
    
    if not output:
        print("[WARNING] Test execution completed but no output received")
        return "FAILURE"
    
    print(f"[INFO] Test output:\n{output}")
    
    # Parse output based on benchmark type
    if "tiles_benchmark" in command:
        return parse_tiles_stats(output)
    elif "motion_benchmark" in command:
        return parse_motion_stats(output)
    elif "multithread" in command:
        return parse_fps_cpu_stats(output)
    elif "overlay" in command:
        return parse_fps_cpu_stats(output)
    else:
        print(f"[ERROR] Parse function for this test is not implemented, output length: {len(output)} characters")
        return "FAILURE"


def execute_postrequisites():
    """
    Clean up test environment and terminate background processes.
    
    This function performs cleanup operations after test execution,
    including terminating Westeros processes if they were started
    during the test.
    
    Returns:
        str: "SUCCESS" on completion
    """
    global display_created
    
    print("[INFO] Executing post-test cleanup...")
    
    if display_created:
        print("[INFO] Display was managed by RDKWindowManager, no cleanup needed")
        return "SUCCESS"
    else:
        print("[INFO] Terminating Westeros processes...")
        command = "kill -9 `pidof westeros` 2>/dev/null || true"
        output = execute_Cmnd_InDUT(command)
        print("[INFO] Westeros cleanup completed")
        return "SUCCESS"

#-------------------------------------------------------------------
# PREREQUISITE SETUP FOR VULKAN APPS TESTING
#-------------------------------------------------------------------
def set_prerequisites(model, resolution):
    """
    Set up the required environment for VkMark testing.
    
    This function attempts to create a display using RDKWindowManager first.
    If RDKWindowManager is not available, it falls back to starting Westeros
    with appropriate environment variables for the specified device model.
    
    Args:
        model (str): Device model ("RPI" for Raspberry Pi, others for standard setup)
    
    Returns:
        str: "SUCCESS" on successful setup, "FAILURE" on error
    """
    print("[INFO] Setting up prerequisites for Vulkan testing...")

    resolutions = {
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "2160p": (3840, 2160)
    }
    global width
    global height
    global device_model
    width, height = resolutions.get(resolution, (1920, 1080))
    device_model = model
    
    # Attempt to create display using RDKWindowManager
    createDisplay_result = createDisplay()
    
    if str(createDisplay_result) != "RDKWindowManager not present":
        # RDKWindowManager is available
        if createDisplay_result == "SUCCESS":
            print("[SUCCESS] Display setup completed using RDKWindowManager")
            return "SUCCESS"
        else:
            print("[FAILURE] Display creation failed with RDKWindowManager")
            return "FAILURE"
    
    # Fallback to Westeros setup
    print("\n[PRE-REQUISITE 1] Setting up Westeros display environment")
    
    global runtime_dir
    global wayland_display

    wayland_display="main0"
    
    # Construct Westeros startup command with proper environment
    command = f"XDG_RUNTIME_DIR={runtime_dir} WAYLAND_DISPLAY={wayland_display} westeros --renderer libwesteros_render_embedded.so.0.0.0 --display main0 --embedded --animate --window-size {width}x{height} &"
    command = "LD_PRELOAD=/usr/lib/libwesteros_gl.so.0 " + command

    # Add Raspberry Pi specific DRM card setting
    if model == "RPI":
        print("[INFO] Adding Raspberry Pi DRM card configuration")
        command = "WESTEROS_DRM_CARD=/dev/dri/card1 " + command
    
    print(f"[INFO] Starting Westeros with command: {command}")
    output = execute_Cmnd_InDUT(command)
    
    # Note: For background processes, output might be empty
    # The success/failure should be determined differently
    print("[INFO] Westeros startup command executed")
    return "SUCCESS"

#-------------------------------------------------------------------
# PARSE VKCUBE OUTPUT
#-------------------------------------------------------------------
def parse_vkcube_output(output):
    fps_values = []
    cpu_values = []

    # Extract per-frame FPS and CPU
    pattern = r"FPS:\s*([\d.]+)\s*\|\s*CPU:\s*([\d.]+)%"

    for line in output.splitlines():
        match = re.search(pattern, line)
        if match:
            fps = float(match.group(1))
            cpu = float(match.group(2))
            fps_values.append(fps)
            cpu_values.append(cpu)

    # Extract reported averages (optional validation)
    avg_fps_match = re.search(r"[VKCube] Average FPS\s*:\s*([\d.]+)", output)
    avg_cpu_match = re.search(r"[VKCube] Average CPU usage\s*:\s*([\d.]+)%", output)

    # ❌ Validation checks
    if not fps_values or not cpu_values:
        return {"status": "failure", "reason": "No FPS/CPU data found"}

    if len(fps_values) != len(cpu_values):
        return {"status": "failure", "reason": "Mismatch in FPS/CPU samples"}

    # Compute averages
    calc_avg_fps = sum(fps_values) / len(fps_values)
    calc_avg_cpu = sum(cpu_values) / len(cpu_values)

    # If reported averages exist, validate them (tolerance allowed)
    if avg_fps_match:
        reported_fps = float(avg_fps_match.group(1))
        if abs(calc_avg_fps - reported_fps) > 5:  # tolerance
            return {"status": "failure", "reason": "FPS average mismatch"}

    if avg_cpu_match:
        reported_cpu = float(avg_cpu_match.group(1))
        if abs(calc_avg_cpu - reported_cpu) > 5:
            return {"status": "failure", "reason": "CPU average mismatch"}

    # Additional sanity checks
    if calc_avg_fps <= 0 or calc_avg_cpu < 0:
        return {"status": "failure", "reason": "Invalid values"}

    return {
        "status": "success",
        "average_fps": round(calc_avg_fps, 2),
        "average_cpu": round(calc_avg_cpu, 2)
    }

#-------------------------------------------------------------------
# VKMARK BINARY EXECUTION
#-------------------------------------------------------------------
def execute_binary(binary, present_mode):
    """
    Execute Vulkan benchmark binary with specified present mode.
    
    This function constructs and executes the appropriate Vulkan binary command
    based on the display setup (RDKWindowManager vs Westeros) and parses
    the benchmark results.
    
    Args:
        present_mode (str): Vulkan present mode (e.g., 'fifo', 'immediate')
    
    Returns:
        str: "SUCCESS" if benchmark completes and score is extracted,
             "FAILURE" if execution fails or no score is found
    """
    global runtime_dir, display_created, wayland_display
    global width, height
    
    # Validate input
    if not present_mode or not isinstance(present_mode, str):
        print("[ERROR] Invalid present_mode parameter")
        return "FAILURE"
    
    print(f"[INFO] Executing {binary} benchmark in {present_mode} mode...")

    present_mode_enum = { "mailbox" : 1, "fifo" : 2 }

    # Set present_mode for vkcube
    if binary == "vkcube":
        present_mode_key = present_mode
        present_mode = present_mode_enum[present_mode_key]

    # Set duration and enable metric collection in vkcube
    if binary == "vkcube":
        binary = binary + f" --duration 60 --fps --width {width} --height {height}"

    # Add fullscreen mode for vkmark
    if binary == "vkmark":
        binary = binary + " --fullscreen "


    # Construct command based on display setup method
    if display_created:
        # Use RDKWindowManager created display
        command = f"XDG_RUNTIME_DIR={runtime_dir} WAYLAND_DISPLAY={wayland_display} {binary} "
        if "vkcube" in binary:
            command = command + f" --present_mode {present_mode}"
        elif "vkmark" in binary:
            command = command + f" --winsys wayland --present-mode={present_mode}"
        else:
            print("[ERROR] Invalid binary")
            return "FAILURE"
        print("[INFO] Using RDKWindowManager display 'test'")
    else:
        # Use Westeros display - wait for socket creation
        command = (f"while ! ls {runtime_dir}/westeros* 1>/dev/null 2>&1; do sleep 1; done; "
                  f"export XDG_RUNTIME_DIR={runtime_dir}; "
                  f"export WAYLAND_DISPLAY={wayland_display}; "
                  f"{binary} ")
        if "vkcube" in binary:
            command = command + f" --present_mode {present_mode}"
        elif "vkmark" in binary:
            command = command + f" --winsys wayland --present-mode={present_mode}"
        else:
            print("[ERROR] Invalid binary")
            return "FAILURE"
        print("[INFO] Using Westeros display - waiting for socket creation")
    
    print(f"[DEBUG] vulkan binary command: {command}")
    
    # Execute vulkan binary benchmark
    output = execute_Cmnd_InDUT(command)
    
    if not output:
        print("[ERROR] No output received from vulkan binary execution")
        return "FAILURE"
    
    print("[INFO] Vulkan binary execution completed")
    print(f"\n{output}\n")

    if "vkmark" in binary:
        # Parse benchmark score from output
        score_match = re.search(r"vkmark Score:\s*(\d+)", output, re.IGNORECASE)

        # Check for errors or missing score
        if "error" in output.lower() or not score_match:
            print(f"[FAILURE] Unable to obtain VkMark score in {present_mode} mode")
            if "error" in output.lower():
                print("[DEBUG] Error detected in VkMark output")
            else:
                print("[DEBUG] No score pattern found in output")
            return "FAILURE"
    
        # Extract and display score
        score = score_match.group(1)
        print(f"[SUCCESS] VkMark score obtained in {present_mode} mode: {score}")

    if "vkcube" in binary:
        result = parse_vkcube_output(output)
        present_mode = present_mode_key
        try:
            score = result["average_fps"]
            cpu_usage = result["average_cpu"]
            print(f"[SUCCESS] VkCube score obtained in {present_mode} mode: {score}")
        except:
            print("[DEBUG] Error detected in VkCube output")
            return "FAILURE"

    # Format and display results banner
    result_text = f"{present_mode.upper()} SCORE = {score}"
    if "vkcube" in binary:
        result_text = f"{result_text} CPU Usage = {cpu_usage}"
    banner_length = len(result_text) + 4  # Add padding
    
    print("\n" + "=" * banner_length)
    print(f"  {result_text}")
    print("=" * banner_length + "\n")
    
    return "SUCCESS"
