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
#---------------------------------------------------------------
def telemetry_obtainCredentials():
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
#-------------------------------------------------------------------
def execute_CmndInDUT (command):
    output = ""
    global SSHConfigValues
    if not SSHConfigValues:
        credentials = telemetry_obtainCredentials()
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

#------------------------------------------------------------------
# GET THE TELEMETRY URL FROM DEVICE CONFIG FILE
#------------------------------------------------------------------
def telemetry_deviceconfig_value(basePath, configKey):
    telemetry_deviceconfig_value_status="SUCCESS"
    configValue = get_device_config_value(basePath, configKey)
    if "FAILURE" not in configValue:
        if len(configValue) == 0:
            output = "[INFO] - Please configure the Telemetry server URL in device config file"
            print(output)
            telemetry_deviceconfig_value_status="FAILURE"
        else:
            output = "[INFO] - Telemetry server URL is configured device config file"
            print(output)
            telemetry_url = configValue
            print("\nConfigured Telemetry url : " + telemetry_url)
    else:
        output="FAILURE : Failed to get the Telemetry server URL"
        print(output)
        telemetry_deviceconfig_value_status="FAILURE"
    return telemetry_deviceconfig_value_status,telemetry_url

#-----------------------------------------------------------------
# CHECK RFC PARAMETER STATUS
#-----------------------------------------------------------------
def telemetry_datamodelcheck(rfcparameter):
    config_status=telemetry_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #check rfc parameter status
        command="tr181 -d "+str(rfcparameter)
        print("Executing Command : %s" %command)
        #execute in DUT function
        result=execute_CmndInDUT (sshMethod, credentials, command)
        result=str(result).split("\n")[2]
        result=result.strip()
        print(result)
    else:
        print("\nFAILURE : Failed to get the device credentials")
        result="FAILURE"
    return result

#------------------------------------------------------------------
# SETTING THE PRE-REQUISITES FOR TELEMETRY CASES
#------------------------------------------------------------------
def setPreRequisites():
    print("\n[PRE-REQUISITE 1] : Setting DCM properties")
    dcmProperties = """# DCM properties file
# Log server details
LOG_SERVER=xconf.rdkcentral.com
# Log upload server details
DCM_LOG_SERVER=http://52.0.158.162:8080/telemetry-collector/rdkv-collector
DCM_LOG_SERVER_URL=https://xconf.rdkcentral.com:19092/loguploader/getT2Settings
# SCP server details
DCM_SCP_SERVER=xconf.rdkcentral.com
# LA server details
DCM_LA_SERVER_URL=http://52.0.158.162:8080/telemetry-collector/rdkv-collector"""
    command = "echo '" + dcmProperties + "' > /etc/dcm.properties"
    execute_CmndInDUT (command)
    print("\n[PRE-REQUISITE 1 RESULT] :DCM properties successfully set")

    print("\n[PRE-REQUISITE 2] : Setting Telemetry Version")
    command  = "tr181 -s -t string -v 2.0.1 Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.Version"
    execute_CmndInDUT (command)
    print("Verifying if Telemetry Version is set")
    command = "tr181 -d Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.Version"
    output = execute_CmndInDUT (command)
    print(output)
    if " 2.0.1" not in output:
        print("FAILURE : Telemetry Version is not successfully set")
        return "FAILURE"
    print("\n[PRE-REQUISITE 2 RESULT] : Telemetry Version is successfully set")

    print("\n[PRE-REQUISITE 3] : Setting Telemetry Config URL")
    command = "tr181 -s -t string -v https://xconf.rdkcentral.com:19092/loguploader/getT2Settings Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.ConfigURL"
    execute_CmndInDUT (command)
    print("Verify if config URL is successfully set")
    command = "tr181 Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.ConfigURL"
    output = execute_CmndInDUT (command)
    print(output)
    if "https://xconf.rdkcentral.com:19092/loguploader/getT2Settings" not in output:
        print("FAILURE : Telemetry.ConfigURL not successfully set")
        return "FAILURE"
    print("\n[PRE-REQUISITE 3 RESULT] : Telemetry.ConfigURL is successfully set")
    return "SUCCESS"

#------------------------------------------------------------------
# Form RBUS CLI COMMAND
#------------------------------------------------------------------
def form_rbuscli_command(param_name, profile_name, description, name):
    payload = {
    "profiles": [
        {
            "name": profile_name,
            "hash": "hash1",
            "value": {
                "Name": profile_name,
                "Description": description,
                "Version": "1",
                "Protocol": "HTTP",
                "EncodingType": "JSON",
                "ReportingInterval": 60,
                "TimeReference": "0001-01-01T00:00:00Z",
                "Parameter": [
                    {
                        "type": "dataModel",
                        "name": name,
                        "reference": param_name
                    }
                ],
                "HTTP": {
                    "URL": "http://52.0.158.162:8080/telemetry-collector/rdkv-collector",
                    "Compression": "None",
                    "Method": "POST",
                    "RequestURIParameter": [
                        {"Name": "deviceId", "Reference": "Device.DeviceInfo.MACAddress"},
                        {"Name": "reportName", "Reference": "Profile.Name"}
                    ]
                },
                "JSONEncoding": {
                    "ReportFormat": "NameValuePair",
                    "ReportTimestamp": "Unix-Epoch"
                }
            }
        }
    ]
    }

    json_str = json.dumps(payload)
    cmd = "rbuscli setvalues Device.X_RDKCENTRAL-COM_T2.ReportProfiles string '" + json_str + "'"
    return cmd
