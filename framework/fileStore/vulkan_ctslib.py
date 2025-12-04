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
import json
import sys
import re
from SSHUtility import *
import SSHUtility
import requests
import time
from datetime import datetime
import os
import subprocess
import inspect
import configparser
from time import sleep
import pexpect
deviceIP=""
SSHConfigValues={}
deviceMAC=""
password=""
user_name=""
sshMethod=""
#---------------------------------------------------------------------------------------
#INITIALIZE THE MODULE
#---------------------------------------------------------------
def init_module (libobj, port, deviceInfo):
    global deviceIP
    global devicePort
    global deviceName
    global deviceMAC
    global deviceType
    global libObj
    deviceIP = libobj.ip;
    devicePort = port
    deviceName = deviceInfo["devicename"]
    deviceType = deviceInfo["boxtype"]
    libObj = libobj
    try:
        deviceMAC = deviceInfo["mac"]
        SSHUtility.deviceMAC = deviceMAC
        SSHUtility.realpath = libobj.realpath
        deviceMAC = deviceMAC.replace(":","")
    except Exception as e:
        print("\nException Occurred while getting MAC \n")
        print(e)
        print("PLEASE UPDATE MAC ADDRESS in DEVICE CONFIGURATION")
        os.exit()
#----------------------------------------------------------------------
# GET DEVICE CONFIGURATION FROM THE DEVICE CONFIG FILE
# Description  : Read the value of device configuration from the <device>.config file
# Parameters   : basePath - a string to specify the path of the TM
#                configKey - a string to specify the configuration whose value needs to be retrieved from the <device>.config file
# Return Value : value of device configuration or error log in case of failure
#----------------------------------------------------------------------
def get_device_config_value (basePath, configKey):
    deviceConfigFile=""
    configValue = ""
    output = ""
    configPath = basePath + "/"   + "fileStore/tdkvRDKServiceConfig"
    deviceNameConfigFile = configPath + "/" + deviceName + ".config"
    deviceTypeConfigFile = configPath + "/" + deviceType + ".config"
    # Check whether device / platform config files required for
    # executing the test are present
    if os.path.exists (deviceNameConfigFile) == True:
        deviceConfigFile = deviceNameConfigFile
    elif os.path.exists (deviceTypeConfigFile) == True:
        deviceConfigFile = deviceTypeConfigFile
    else:
        output = "FAILURE : No Device config file found : " + deviceNameConfigFile + " or " + deviceTypeConfigFile
        print(output)
    try:
        if (len (deviceConfigFile) != 0) and (len (configKey) != 0):
            config = configparser.ConfigParser ()
            config.read (deviceConfigFile)
            deviceConfig = config.sections ()[0]
            configValue =  config.get (deviceConfig, configKey)
            output = configValue
        else:
            output = "FAILURE : DeviceConfig file or key cannot be empty"
            print(output)
    except Exception as e:
        output = "FAILURE : Exception Occurred: [" + inspect.stack()[0][3] + "] " + e.message
        print(output)
    return output

#---------------------------------------------------------------
# GET THE REQUIRED CONFIGURATIONS TO SSH INTO THE DUT
# Description  : To get the required configurations to SSH into the DUT
# Return Value : Returns 'SUCCESS' on successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------
def obtainCredentials():
    config_status = "SUCCESS"
    result = "SUCCESS"
    print("[INFO] Retrieving Configuration values from config file.......")
    configKeyList = ["SSH_METHOD","SSH_USERNAME", "SSH_PASSWORD"]
    global SSHConfigValues
    global password
    global user_name
    global sshMethod
    #Get each configuration from device config file
    for configKey in configKeyList:
        SSHConfigValues[configKey] = get_device_config_value(libObj.realpath,configKey)
        if "FAILURE" not in SSHConfigValues[configKey] and SSHConfigValues[configKey] != "":
            print("SUCCESS: Successfully retrieved %s configuration from device config file" %(configKey))
        else:
            print("FAILURE: Failed to retrieve %s configuration from device config file" %(configKey))
            if SSHConfigValues[configKey] == "":
                print("\n [INFO] Please configure the %s key in the device config file" %(configKey))
                result = "FAILURE"
                break
    if "FAILURE" != result:
        if "directSSH" == SSHConfigValues["SSH_METHOD"]:
            sshMethod = SSHConfigValues["SSH_METHOD"]
            user_name = SSHConfigValues["SSH_USERNAME"]
            if SSHConfigValues["SSH_PASSWORD"] == "None":
                password = ""
            else:
                password = configValues["SSH_PASSWORD"]
        else:
            print("FAILURE: Currently only supports directSSH ssh method")
            config_status = "FAILURE"
    else:
        config_status = "FAILURE"
    if config_status == "SUCCESS":
        return SSHConfigValues
    else:
        return config_status
#-------------------------------------------------------------------
# EXECUTE A COMMAND IN DUT SHELL AND GET THE OUTPUT
# Description  : Execute a command in DUT through ssh_and_execute() from SSHUtility library and get the output
# Parameters   : 1. sshMethod -  string to specify the SSH method to be used
#                2. credentials - a coma ceparated string to specify the parameters for ssh_and_execute() method. Values are retrieved from <device>.config
#                       a. credentials[0] - string to specify the DUT IP
#                       b. credentials[1] - string to specify the username to ssh to DUT
#                       c. credentials[2] - string to specify the password to ssh to DUT
#                3. command - string to specify the command to be executed in DUT
# Return Value : console output of the command executed on DUT
#-------------------------------------------------------------------
def executeCmnd_InDUT (command):
    output = ""
    global SSHConfigValues
    if not SSHConfigValues:
        credentials = obtainCredentials()
    else:
        credentials = SSHConfigValues
    if isinstance(credentials,dict) and credentials.get("SSH_METHOD")== "directSSH":
        user_name = credentials.get("SSH_USERNAME")
        host_name = deviceIP
        sshMethod = credentials.get("SSH_METHOD")
        password = credentials.get("SSH_PASSWORD")
    else:
        #TODO
        print("Secure ssh to CPE")
        pass
    try:
        output = ssh_and_execute (sshMethod, host_name, user_name, password, command)
    except Exception as e:
        print("Exception occured during ssh session")
        print(e)
    return output

#--------------------------------------------------------------------------------------
# RUN VULKAN CTS COMMAND IN DUT
#---------------------------------------------------------------------------------------
def run_vulkan_cts_command(info_filename=None):
    print("\n Vulkan CTS Command Execution in DUT \n")
    # Determine .info argument by parsing the main python script (or VULKAN_INFO env var)

    try:
        main_path = sys.argv[0] if len(sys.argv) > 0 else None
        content = ""
        if main_path and os.path.exists(main_path):
            with open(main_path, "r") as mf:
                content = mf.read()
        else:
            try:
                content = inspect.getsource(__main__)
            except Exception:
                content = ""

        m = re.search(r'["\']([^"\']+\.info)["\']', content)
        if m:
            info_filename = os.path.basename(m.group(1))
        else:
            # fallback: allow explicit env var if main script doesn't contain the value
            env_val = os.environ.get("VULKAN_INFO")
            if env_val:
                info_filename = os.path.basename(env_val)
    except Exception as e:
        print(f"[ERROR] Failed to determine .info argument: {e}")

    if not info_filename:
        print("[FAILURE] Could not determine .info filename from main script or VULKAN_INFO env var")
        return ""

    command = f"cd /tmp/usb/vulkan-cts ; sh run_cts.sh {info_filename}"
    output = executeCmnd_InDUT(command)
    if not output :
        print ("[FAILURE] : No output was obtained from test")
        return ""
    else:
        print ("[SUCCESS] : Output obtained from test")

    return output



#--------------------------------------------------------------------------------------
# GET THE QPA FILE NAME FROM THE INFO FILE
#---------------------------------------------------------------------------------------
def copy_file(qpa_folder_path, result_dir, qpa_file_name):
    print("\n Executing copy file function \n")
    print("Folder path : %s" % qpa_folder_path)
    print("Result directory : %s" % result_dir)
    print("QPA file name : %s" % qpa_file_name)

    file_status = "SUCCESS"
    global deviceIP
    devicePort = 8080

    print("\n Copy QPA file from DUT to TDK Server \n") 

    if not qpa_file_name:
        print(f"[FAILURE] No .qpa file found in {qpa_folder_path}")
        file_status = "FAILURE"

    qpa_file_name_only = os.path.basename(qpa_file_name)
    print(f"[INFO] Using QPA file: {qpa_file_name_only}")

    start_cmd = f"cd {qpa_folder_path} && nohup python3 -m http.server {devicePort} >/dev/null 2>&1 &"
    executeCmnd_InDUT(start_cmd)
    sleep(3)

    download_url = f"http://{deviceIP}:{devicePort}/{qpa_file_name_only}"
    output_path = os.path.join(result_dir, qpa_file_name_only)
    print(f"[INFO] Downloading from {download_url}")

    max_wait_time = 120
    interval = 5
    waited = 0
    success = False
    

    while waited < max_wait_time:
        try:
            result = subprocess.run(["wget", "-O", output_path, download_url],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"[SUCCESS] QPA file downloaded: {output_path}")
                success = True
                break
            else:
                print(f"[INFO] QPA not ready, retrying in {interval}s...")
        except Exception as e:
            print(f"[ERROR] wget failed: {e}")

        sleep(interval)
        waited += interval

    executeCmnd_InDUT("ps -ef | grep 'http.server' | grep -v grep | awk '{print $2}' | xargs kill -9")
    print("[INFO] HTTP server stopped on DUT")

    if not success:
        print(f"[FAILURE] QPA file not found after {max_wait_time}s.")
        file_status = "FAILURE"

    return file_status

#---------------------------------------------------------------------------------------
# GENERATE EXCEL REPORT FROM QPA FILE
#---------------------------------------------------------------------------------------
def report_generation(result_dir):
    excel_status = "SUCCESS"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    excel_output = os.path.join(result_dir, f"vulkan_CTS_{os.path.basename(result_dir).split('.')[0]}_{timestamp}.xlsx")

    print(f"[INFO] Generating Excel report using {result_dir}")
    try:
        # Resolve an absolute path to vulkan_report_generator.py next to this module (fallback to libObj.realpath if available)
        script_path = os.path.join(os.path.dirname(__file__), "vulkan_report_generator.py")
        if not os.path.exists(script_path):
            fallback_base = getattr(globals().get('libObj', object()), 'realpath', '')
            if fallback_base:
                candidate = os.path.join(fallback_base, "vulkan_report_generator.py")
                if os.path.exists(candidate):
                    script_path = candidate

        if not os.path.exists(script_path):
            raise FileNotFoundError(f"vulkan_report_generator.py not found at {script_path}")

        subprocess.run(["python3", script_path, result_dir, excel_output], check=True)
        print(f"[SUCCESS] Excel report generated: {excel_output}")
    except Exception as e:
        print(f"[ERROR] Excel generation failed: {e}")
        excel_status = "FAILURE"
        excel_status = "FAILURE"
    return excel_status

