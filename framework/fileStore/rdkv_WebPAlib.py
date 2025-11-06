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

deviceMAC=""
password=""
user_name=""
sshMethod=""
#---------------------------------------------------------------
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
def webpa_obtainCredentials():
    config_status = "SUCCESS"
    result = "SUCCESS"
    print("[INFO] Retrieving Configuration values from config file.......")
    configKeyList = ["SSH_METHOD","SSH_USERNAME", "SSH_PASSWORD"]
    configValues = {}
    global password
    global user_name
    global sshMethod
    #Get each configuration from device config file
    for configKey in configKeyList:
        configValues[configKey] = get_device_config_value(libObj.realpath,configKey)
        if "FAILURE" not in configValues[configKey] and configValues[configKey] != "":
            print("SUCCESS: Successfully retrieved %s configuration from device config file" %(configKey))
        else:
            print("FAILURE: Failed to retrieve %s configuration from device config file" %(configKey))
            if configValues[configKey] == "":
                print("\n [INFO] Please configure the %s key in the device config file" %(configKey))
                result = "FAILURE"
                break
    if "FAILURE" != result:
        if "directSSH" == configValues["SSH_METHOD"]:
            sshMethod = configValues["SSH_METHOD"]
            user_name = configValues["SSH_USERNAME"]
            if configValues["SSH_PASSWORD"] == "None":
                password = ""
            else:
                password = configValues["SSH_PASSWORD"]
        else:
            print("FAILURE: Currently only supports directSSH ssh method")
            config_status = "FAILURE"
    else:
        config_status = "FAILURE"
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
def execute_CmndInDUT (sshMethod, credentials, command):
    output = ""
    if sshMethod == "directSSH":
        credentialsList = credentials.split(',')
        host_name = credentialsList[0]
        user_name = credentialsList[1]
        password = credentialsList[2]
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

################################################################################################
#     Parodus Service check
################################################################################################

def webpa_parodusstatuscheck():
    parodusstatus="SUCCESS"
    config_status=webpa_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #check parodus status
        command="systemctl status parodus | grep running"
        print("Executing Command : %s" %command)
        #execute in DUT function
        result=execute_CmndInDUT(sshMethod, credentials, command)
        result=result.split("\n")
        print(result)
        result=str(result[1])
        if "active (running)" in result:
            print(result)
            print("\nSUCCESS : Successfully get the parodus status")
        else:
            print(result)
            print("\nFAILURE : Parodus Process not running")
            parodusstatus="FAILURE"
    else:
        print("\nFAILURE : Failed to get the device credentials")
        parodusstatus="FAILURE"
    return parodusstatus

################################################################################################
#        GET Device config
################################################################################################

def webpa_deviceconfig_value(basePath, configKey, configKey2):
    webpa_deviceconfig_value_status="SUCCESS"
    configValue = get_device_config_value(basePath, configKey)
    if "FAILURE" not in configValue:
        if len(configValue) == 0:
            output = "[INFO] - Please configure the WEBPA server URL in device config file"
            print(output)
            webpa_deviceconfig_value_status="FAILURE"
        else:
            output = "[INFO] - WEBPA server URL is configured device config file"
            print(output)
            webpa_url = configValue
            print("\nConfigured WebPA url : " + webpa_url)
            
            configValue = get_device_config_value(basePath, configKey2)
            if "FAILURE" not in configValue:
                if len(configValue) == 0:
                    output = "[INFO] - Please configure the AUTH_TOKEN in device config file"
                    print(output)
                    webpa_deviceconfig_value_status="FAILURE"
                else:
                    output = "[INFO] - AUTH_TOKEN is configured device config file"
                    print(output)
                    Auth_Key = configValue
                    print("\n Authorization Token : " + Auth_Key)
            else:
                output="FAILURE : Failed to get the Authorizationn token"
                print(output)
                webpa_deviceconfig_value_status="FAILURE"

    else:
        output="FAILURE : Failed to get the WEBPA server URL"
        print(output)
        webpa_deviceconfig_value_status="FAILURE"
    return webpa_deviceconfig_value_status,webpa_url,Auth_Key


#---------------------------------------------------------------
# WEBPA GET
#---------------------------------------------------------------
def webpa_get(paramName,WEBPA_URL,AUTH_TOKEN):
    webpa_getstatus="SUCCESS"
    global deviceMAC
    global password
    global user_name
    global sshMethod
    if sshMethod and user_name:
        config_status = "SUCCESS"
    else:
        config_status = "FAILURE"
    deviceMACstatus = "SUCCESS"
    if "FAILURE" not in deviceMACstatus:
        if config_status != "SUCCESS":
            config_status=webpa_obtainCredentials()
        if "FAILURE" not in config_status:            
            credentials = deviceIP + ',' + user_name + ',' + password
            WEBPA_URL = WEBPA_URL.strip()
            AUTH_TOKEN = AUTH_TOKEN.strip()
            command = "curl -X GET '"+WEBPA_URL+"/api/v2/device/mac:"+deviceMAC+"/config?names="+paramName+"'"+" -H 'authorization:"+AUTH_TOKEN+"'"
            print("\nExecuting Command : %s" %command)
            #execute in DUT function
            result=execute_CmndInDUT (sshMethod, credentials, command)
            result=str(result).split("\n")
            result=str(result[1])
            print("\nGet Response : ", result)
            data = json.loads(result)

            data_type_field =0

            value_field = data["parameters"][0]["value"].strip('"')

            print("Value : ", value_field)

            if value_field == "" or value_field == "EMPTY":
                print("\nFAILURE : Value field is empty\n")
                webpa_getstatus="FAILURE"
            else:
                data_type_field = data["parameters"][0]["dataType"]
                print("Data Type : ", data_type_field)
                print("\nSUCCESS : Value feild is not empty\n")

        else:
            print("\nFAILURE : Failed to get the device credentials")
            webpa_getstatus="FAILURE"
    else:
         webpa_getstatus="FAILURE"
    
    return webpa_getstatus,value_field,data_type_field


#---------------------------------------------------------------
# WEBPA SET
#---------------------------------------------------------------
def webpa_set(paramName,testValue,WEBPA_URL,AUTH_TOKEN,dataType):
    global deviceMAC
    global password
    global user_name
    global sshMethod
    if sshMethod and user_name:
        config_status = "SUCCESS"
    else:
        config_status = "FAILURE"
    deviceMACstatus = "SUCCESS"
    webpa_setstatus="SUCCESS"

    if "FAILURE" not in deviceMACstatus:
        if config_status != "SUCCESS":
            config_status=webpa_obtainCredentials()
        if "FAILURE" not in config_status:
            credentials = deviceIP + ',' + user_name + ',' + password
            WEBPA_URL = WEBPA_URL.strip()
            AUTH_TOKEN = AUTH_TOKEN.strip()
            command = "curl -X PATCH "+WEBPA_URL+"/api/v2/device/mac:"+deviceMAC+"/config -d '{"+'"parameters":[{"dataType":' + str(dataType) + ', "name":"'+paramName+'",  "value": "'+testValue+'"}]}'+"' -H 'authorization:"+AUTH_TOKEN+"'"
            print("Executing Command : %s\n" %command)
            #execute in DUT function
            result=execute_CmndInDUT (sshMethod, credentials, command)
            result=str(result).split("\n")
            result=str(result[1])
            print("\nSet Response : ", result)
        else:
            print("\nFAILURE : Failed to get the device credentials")
            webpa_setstatus="FAILURE"
    else:
         webpa_setstatus="FAILURE"

    return webpa_setstatus

#---------------------------------------------------------------
# WEBPA validation
#---------------------------------------------------------------
def webpa_validate_set(paramName, testValue, WEBPA_URL, AUTH_TOKEN):
    validation_status = "FAILURE"
    print(f"\n[INFO] Validating if '{paramName}' was set to '{testValue}'")

    global deviceMAC
    global password
    global user_name
    global sshMethod
    if sshMethod and user_name:
        config_status = "SUCCESS"
    else:
        config_status = "FAILURE"
    deviceMACstatus = "SUCCESS"
    if "FAILURE" not in deviceMACstatus:
        if config_status != "SUCCESS":
            config_status=webpa_obtainCredentials()
        if "FAILURE" not in config_status:
            credentials = deviceIP + ',' + user_name + ',' + password
            WEBPA_URL = WEBPA_URL.strip()
            AUTH_TOKEN = AUTH_TOKEN.strip()
            command = f"curl -X GET '{WEBPA_URL}/api/v2/device/mac:{deviceMAC}/config?names={paramName}' -H 'authorization:{AUTH_TOKEN}'"
            print(f"\nExecuting Command: {command}")
            result = execute_CmndInDUT(sshMethod, credentials, command)
            result = str(result).split("\n")[1]
            data = json.loads(result)

            actual_value = data["parameters"][0]["value"].strip('"')

            if actual_value == testValue:
                print(f"[SUCCESS] Parameter '{paramName}' is correctly set to '{testValue}'")
                validation_status = "SUCCESS"
            else:
                print(f"[FAILURE] Mismatch! Expected: '{testValue}', Got: '{actual_value}'")
        else:
            print("[FAILURE] Failed to obtain WebPA credentials")
    else:
        print("[FAILURE] Failed to get MAC address")

    return validation_status



#---------------------------------------------------------------
# Integer Check Function
#---------------------------------------------------------------
def integer_check (value, threshold_value=None):
    str_val = str(value.strip())
    print ("Value obtained : ", str_val)
    if not str_val.isdigit():
        print(f"[FAILURE] Value contains Alphabets or non-numeric characters")
        return "FAILURE"
    str_val = int(value)
    if str_val < 0:
        print(f"[FAILURE] Value is in negative")
        return "FAILURE"
    if threshold_value is not None:
        threshold_value = int(threshold_value)
        print("Threshold value provided: ", threshold_value)
        if str_val <= threshold_value:
            print("[SUCCESS] Value is less than the threshold value")
            return "SUCCESS"
        else:
            print("[FAILURE] Value is greater than the threshold value")
            return "FAILURE"
    else:
        print("Integer value validated successfully")
        return "SUCCESS"

#----------------------------------------------------------------------------------------------
