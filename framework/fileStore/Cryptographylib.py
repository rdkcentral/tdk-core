##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2024 RDK Management
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
import os
import subprocess
import inspect
import configparser
from time import sleep
import pexpect
import time

ssh_param_dict = {}
securityEnabled=False

#---------------------------------------------------------------
#INITIALIZE THE MODULE
#---------------------------------------------------------------
def init_module (libobj, port, deviceInfo):
    global deviceIP
    global devicePort
    global deviceName
    global deviceType
    global libObj
    deviceIP = libobj.ip;
    devicePort = port
    deviceName = deviceInfo["devicename"]
    deviceType = deviceInfo["boxtype"]
    libObj = libobj
    try:
        deviceMac = deviceInfo["mac"]
        SSHUtility.deviceMAC = deviceMac
        SSHUtility.realpath = libobj.realpath
    except Exception as e:
        print("\nException Occurred while getting MAC \n")
        print(e)

#------------------------------------------------------------------------------
# Function to retreive the device details
#------------------------------------------------------------------------------
def getDeviceDetails(detail):
    if detail == "deviceType":
        return deviceType
    elif detail == "deviceIP":
        return deviceIP
    elif detail == "devicePort":
        return devicePort
    else:
        return deviceName


#-------------------------------------------------------------------
#GET THE SSH DETAILS FROM CONFIGURATION FILE
#-------------------------------------------------------------------
def rdkservice_getSSHParams(realpath,deviceIP):
    ssh_dict = {}
    print("\n getting ssh params from conf file")

    ssh_method = getDeviceConfigValue("SSH_METHOD")
    if not ssh_method:
        ssh_method = "directSSH"
    user_name = getDeviceConfigValue("SSH_USERNAME")
    if not user_name:
        user_name = "root"
    password = getDeviceConfigValue("SSH_PASSWORD")
    if not password:
        password = "None"
    if any(value == "" for value in (ssh_method,user_name,password)):
        print("please configure values before test")
        ssh_dict = {}
    else:
        ssh_dict["ssh_method"] = ssh_method
        if password.upper() == "NONE":
            password = ""
        ssh_dict["credentials"] = deviceIP +","+ user_name +","+ password
    ssh_dict = json.dumps(ssh_dict)
    return ssh_dict

#-------------------------------------------------------------------
# Function to execute the command in the DUT using ssh utility
#-------------------------------------------------------------------
def execute_Cmnd_In_DUT (command,sshMethod="", credentials=""):
    output = ""
    global deviceIP;
    ssh_param = rdkservice_getSSHParams(libObj.realpath,deviceIP)
    global ssh_param_dict
    ssh_param_dict = json.loads(ssh_param)
    if not sshMethod:
        sshMethod = ssh_param_dict["ssh_method"]
        credentials = ssh_param_dict['credentials']
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

######################################################################
#
# Functions
#
######################################################################

#Function to retrieve the device configuration from device config file
def getDeviceConfigValue (configKey):
    try:
        global test_streams_base_path

        result = "SUCCESS"
        #Retrieve the device details(device name) and device type from tdk library
        deviceConfigFile=""
        configValue = ""
        basePath = libObj.realpath
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
            result = "FAILURE"

        #Continue only if the device config file exists
        if (len (deviceConfigFile) != 0):
            configParser = configparser.ConfigParser()
            configParser.read(r'%s' % deviceConfigFile)
            configValue = configParser.get('device.config', configKey)
            '''try:
                test_streams_base_path = configParser.get('device.config',"TEST_STREAMS_BASE_PATH")
            except:
                test_streams_base_path = ""'''
        else:
            print("DeviceConfig file not available")
            result = "FAILURE"
    except Exception as e:
        print("Exception occurred while retrieving device configuration  : " + e)
        result = "FAILURE"
    if configValue == "":
        return result
    return configValue

