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
import json
import time
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
def obtain_Credentials():
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
def execute_Cmnd_InDUT (command):
    print("ENetering to execute_Cmnd_InDUT")
    output = ""
    global SSHConfigValues
    if not SSHConfigValues:
        credentials = obtain_Credentials()
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
        print("Entering to command")
        output = ssh_and_execute (sshMethod, host_name, user_name, password, command)
        print("executing the details ",output)
    except Exception as e:
        print("Exception occured during ssh session")
        print(e)
    return output

#-------------------------------------------------------------------
# Setting the Export Values as PRE-REQUISITES For vkmark
#-------------------------------------------------------------------
def set_prerequisites():
    print("\n[PRE-REQUISITE 1] : Setting environment variables and starting Westeros display")

    # Step 1: Start Westeros in background

    #command = "XDG_RUNTIME_DIR=/run WAYLAND_DISPLAY=main0 WESTEROS_GL_GRAPHICS_MAX_SIZE=1280x1024 LD_PRELOAD=/usr/lib/libwesteros_gl.so.0.0.0 westeros --renderer /usr/lib/libwesteros_render_gl.so.0 --display=main0 --window-size 1280x1024 > /tmp/westeros.log 2>&1 & while ! ls /run/westeros* 1>/dev/null 2>&1; do sleep 1; done; export XDG_RUNTIME_DIR=/run; export WAYLAND_DISPLAY=$(ls /run/westeros* | head -n1); vkmark --winsys-dir /usr/lib/vkmark/ --data-dir /usr/share/vkmark/ --winsys wayland --present-mode=fifo"

    command = "XDG_RUNTIME_DIR=/run WAYLAND_DISPLAY=main0 WESTEROS_GL_GRAPHICS_MAX_SIZE=1280x1024 LD_PRELOAD=/usr/lib/libwesteros_gl.so.0.0.0 westeros --renderer /usr/lib/libwesteros_render_gl.so.0 --display=main0 --window-size 1280x1024 > /tmp/westeros.log 2>&1 &"

    #execute_Cmnd_InDUT(command)

    print("[INFO] Westeros display started successfully")

    output = execute_Cmnd_InDUT(command)

    if output:
        print(f"[PRE-REQUISITE 1 RESULT] : Environment variables set successfully\n")
        return "SUCCESS"
    else:
        print("[PRE-REQUISITE 1 RESULT] : Failed to set environment variables")
        return "FAILURE"

#-------------------------------------------------------------------
# Binary Execution
#-------------------------------------------------------------------
def execute_binary():
    command = "while ! ls /run/westeros* 1>/dev/null 2>&1; do sleep 1; done; export XDG_RUNTIME_DIR=/run; export WAYLAND_DISPLAY=$(ls /run/westeros* | head -n1); vkmark --winsys-dir /usr/lib/vkmark/ --data-dir /usr/share/vkmark/ --winsys wayland --present-mode=fifo"

    print("[INFO] Executing VKMARK benchmark...")

    output = execute_Cmnd_InDUT(command)
    if not output :
        print("[ERROR] No output received from vkmark execution")
        return ""

    print("[INFO] VKMARK execution completed successfully")
    return output
