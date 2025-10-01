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
# Description  : Execute a command in DUT through ssh_and_execute() from SSHUtility library and get the output
# Parameters   : 1. sshMethod -  string to specify the SSH method to be used
#                2. credentials - a coma ceparated string to specify the parameters for ssh_and_execute() method. Values are retrieved from <device>.config
#                       a. credentials[0] - string to specify the DUT IP
#                       b. credentials[1] - string to specify the username to ssh to DUT
#                       c. credentials[2] - string to specify the password to ssh to DUT
#                3. command - string to specify the command to be executed in DUT
# Return Value : console output of the command executed on DUT
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
# Description  : Read the TELEMETRY URL from the <device>.config file
# Parameters   : basePath - a string to specify the path of the TM
#                configKey - a string to specify the configuration whose value needs to be retrieved from the <device>.config file
# Return Value : TELEMETRY URL or error log in case of failure
#------------------------------------------------------------------
def telemetry_deviceconfig_value(basePath, configKey):
    telemetry_deviceconfig_value_status="SUCCESS"
    Telemetry_Collector_URL = ""
    dummy_url = False
    configValue = get_device_config_value(basePath, configKey)
    if "FAILURE" not in configValue:
        if not configValue.strip():
            output = "[INFO] Telemetry Collector URL is not configured, Configuring the dummy URL"
            Telemetry_Collector_URL = "http:///test.dummy.telemertry.com"
            print(output)
            print("\nDummy Collector URL : " + Telemetry_Collector_URL)
            dummy_url = True
        else:
            output = "[INFO] - Telemetry server URL is configured device config file"
            print(output)
            Telemetry_Collector_URL = configValue
            print("\nConfigured Telemetry Collector url : " + Telemetry_Collector_URL)
            dummy_url = False
    else:
        output="FAILURE : Failed to get the Telemetry server URL"
        print(output)
        telemetry_deviceconfig_value_status="FAILURE"
    print("Vale : " + telemetry_deviceconfig_value_status)
    print("Vale1 : " + Telemetry_Collector_URL)
    print("Vale2 : " + str(dummy_url))
    return f"({telemetry_deviceconfig_value_status}, {Telemetry_Collector_URL}, {dummy_url})"

#-----------------------------------------------------------------
# CHECK RFC PARAMETER STATUS
# Description  : To check the parameter status
# Return Value : Returns 'SUCCESS' on successful execution or "FAILURE" in case of failure 
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
# Description  : To set the Pre requisties before validating Telemetry cases
# Return value : Returns 'SUCCESS' on successfully pre-requisties set or "FAILURE" in case of failure
#------------------------------------------------------------------
def setPreRequisites(Telemetry_Collector_URL):
    Telemetry_Collector_URL = Telemetry_Collector_URL.strip().replace("\n", "").replace("\t", "")
    print("\n[PRE-REQUISITE 1] : Setting DCM properties")
    dcmProperties = f"""# DCM properties file
# Log server details
LOG_SERVER=xconf.rdkcentral.com
# Log upload server details
DCM_LOG_SERVER={Telemetry_Collector_URL}
DCM_LOG_SERVER_URL=https://xconf.rdkcentral.com:19092/loguploader/getT2Settings
# SCP server details
DCM_SCP_SERVER=xconf.rdkcentral.com
# LA server details
DCM_LA_SERVER_URL={Telemetry_Collector_URL}"""
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

    print("\n[PRE-REQUISITE 3] : Getting Telemetry Config URL")
    command = "tr181 Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.ConfigURL"
    output = execute_CmndInDUT (command)
    print("\nTelemetry Config URL : \n", output)

    if not output:
        print("\n[PRE-REQUISITE 3 RESULT] : Unable to retrive the Telemetry Config URL from DUT\n")
        return "FAILURE"
    else:
        print("\n[PRE-REQUISITE 3 RESULT] : Telemetry Config URL was retrived successfully\n")
        return "SUCCESS"

#------------------------------------------------------------------
# Form RBUS CLI COMMAND
# Description : TO form the rbuscli command to set the profile
# Return Value : Return "SUCCESS" on profile set was success or "FAILURE" on failure
#------------------------------------------------------------------
def form_rbuscli_command(param_name, Telemetry_Collector_URL, profile_name, description, name):

    form_rbuscli_command_status="SUCCESS"
    Telemetry_Collector_URL = Telemetry_Collector_URL.strip().replace("\n", "").replace("\t", "")
    #print("URL : ", Telemetry_Collector_URL)
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
                    "URL":Telemetry_Collector_URL,
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


#------------------------------------------------------------------
# Form RBUS CLI Event COMMAND 
# Description : TO form the rbuscli command to set the profile and event
# Return Value : Return "SUCCESS" on profile and event set was success or "FAILURE" on failure
#------------------------------------------------------------------
def form_rbuscli_event_command(event_name, Telemetry_Collector_URL, profile_name, description, component_name):

    form_rbuscli_command_status="SUCCESS"
    Telemetry_Collector_URL = Telemetry_Collector_URL.strip().replace("\n", "").replace("\t", "")
    payloads = {
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
                        "type": "event",
                        "eventName": event_name
                        "component": component_name
                        "use": "absolute"
                    }
                ],
                "HTTP": {
                    "URL":Telemetry_Collector_URL,
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

    json_str = json.dumps(payloads)
    cmd = "rbuscli setvalues Device.X_RDKCENTRAL-COM_T2.ReportProfiles string '" + json_str + "'"
    return cmd
