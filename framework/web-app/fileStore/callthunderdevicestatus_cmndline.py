##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2019 RDK Management
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
###########################################################################
import sys
import requests
import json
import configparser
import os
import subprocess
from SSHUtility import *
import SSHUtility
import re
import importlib


#----------------------------------------------------------------------------------
# EXECUTE A COMMAND IN THE SPECIFIED VM AND GET THE OUTPUT
# Return Value : console output of the command executed in specified VM
#----------------------------------------------------------------------------------
def executeCommandInVM():
    output = ""
    status = True

    #remote_sshkey is an ssh key that should be available in the TM /opt location. This is used to ssh from docker to the host machine for VA devices.
    #The same key can be used to ssh to any other VM to execute the command there.
    #Please ensure to keep the public key remote_sshkey.pub in the authorized_keys file in the remote VM

    #pid_command is to check if the port is already open in the VM
    pid_command = "ssh -i /opt/remote_sshkey " +revportvm_username+"@"+deviceIP+ " \"sudo ss -sltnpe  | grep 0.0.0.0: | grep "+devicePort+" |  cut -d',' -f2 | cut -d'=' -f2\""
    kill_command = "ssh -i /opt/remote_sshkey " +revportvm_username+"@"+deviceIP+ " \"kill PID \""

    try:
        output = subprocess.check_output(pid_command, shell=True, stderr=subprocess.STDOUT)
        output = output.decode()

        #To extract the actual output value from the warning messages from the jump servers
        if "measures." in output:
            output=output.split('.')[-1].strip()
        if output != "":
            kill_command = kill_command.replace("PID", output.strip())
            output = subprocess.check_output(kill_command, shell=True, stderr=subprocess.STDOUT)
            output = output.decode()
    except subprocess.CalledProcessError as e:
       output = e.output.decode()
       print(e)
       status = False
    except Exception as e:
        print(e)
        status = False
    return status

#-------------------------------------------------------------------
# RETRIEVE THE CURRENT STATUS OF THE DUT
# Description  : Sends an RDK service request to retrieve the current status of the DUT (Device Under Test)
# Return Value : Returns the status of the DUT
#-------------------------------------------------------------------
def check_device_status():
    data = '{"jsonrpc":"2.0","id":"3","method": "Controller.1.status@Controller"}'
    headers = {'content-type': 'text/plain;',}
    url = 'http://'+deviceIP+':'+devicePort+'/jsonrpc'
    try:
       response = requests.post(url, headers=headers, data=data, timeout=10)
       request_successful = True
    except Exception as e:
       response = None
       request_successful = False
    return response,request_successful

#-------------------------------------------------------------------
#GET THE VALUE OF GIVEN KEY FROM DEVICE SPECIFIC CONFIG FILE
#Description  : Get the config file name and fetch the values of given keys from the file
#Parameter    : conf_var_list -> A list of key to fetch the values from config file
#Return Value : Returns the status and a dictionary of config keys and values
#-------------------------------------------------------------------
def get_config_value(conf_var_list):
    configValues = {}
    configStatus = True
    try:
        config = configparser.ConfigParser()
        current_directory = os.path.dirname(os.path.abspath(__file__))
        device_config_file = os.path.join(current_directory,"tdkvRDKServiceConfig" ,sys.argv[3])
        if os.path.exists(device_config_file) == True:
            for configKey in conf_var_list:
                config.read(device_config_file)
                if config.has_option('device.config',configKey):
                    configValues[configKey] = str(config.get("device.config",configKey))
                    if configValues[configKey] == "":
                        configStatus = False
                        break
                else:
                    configStatus = False
                    break
        else:
            configStatus = False
    except Exception as e:
        configStatus = False
    return configStatus,configValues


#------------------------------------------------------------------------
#TO EXECUTE A GIVEN COMMAND IN THE DEVICE
#Parameter    : A dictionary of config keys and values
#               command to execute in the device
#Return Value : Status and the output response from the device
#------------------------------------------------------------------------
def ssh_execute_cmd_DUT(configValues,command):
    output=""
    status=True
    try:
        ssh_method= configValues["SSH_METHOD"]
        username=configValues["SSH_USERNAME"]
        password = configValues["SSH_PASSWORD"]
        #if ssh_method is not directSSH, please ensure to keep the correct ssh implementation in SSHUtility file
        #if ssh_method is configured as jumpserver, SSHUtility should have a function called ssh_and_execute_jumpserver(command,mac)
        lib = importlib.import_module("SSHUtility")
        if ssh_method == "directSSH":
            method = "ssh_and_execute"
        else:
            method = "ssh_and_execute_" + ssh_method
        method_to_call = getattr(lib, method)

        if ssh_method == "directSSH":
            output= ssh_and_execute (ssh_method,hostName,username,password,command)
        else:
            ssh_util = configValues["SSH_UTIL"]
            mac = sys.argv[4]
            output = method_to_call(command,mac,ssh_util)
    except Exception as e:
        print(e)
        status=False
    return status,output

#-------------------------------------------------
#SCRIPT STARTS HERE
#-------------------------------------------------
if ( (len(sys.argv)) < 4):
    print("Usage : python " + sys.argv[0] + " <Device_IP_Address> <Thunder_Port> <Device Specific Config file> MACAddress")
    print("eg    : python " + sys.argv[0] + " <Valid DUT IP Address> 9998 <Device Specific Config file MACAddress>")
    exit()
else:
    deviceIP = hostName = sys.argv[1]
    devicePort = sys.argv[2]
    if int(devicePort) != 9998:
        conf_status,conf_values=get_config_value(["EXECUTION_DEVICE_TYPE","REV_PORT_GW_SERVER_IP","REV_PORT_GW_USERNAME"])
        if conf_status:
            execution_device_type=conf_values["EXECUTION_DEVICE_TYPE"]
            deviceIP = conf_values["REV_PORT_GW_SERVER_IP"]
            revportvm_username = conf_values["REV_PORT_GW_USERNAME"]
        else:
            print("NOT_FOUND")

    #Check the device status
    response,request_successful = check_device_status()

    if request_successful and response is not None and response.status_code == 200:
        print("FREE")
    elif int(devicePort) != 9998 and conf_status:
        #Check if the devicePort is open in the VM.
        #If open kill that process from the VM
        status = executeCommandInVM()
        if status:
            configKeyList = ["SSH_METHOD","SSH_USERNAME","SSH_PASSWORD","PRIVATE_KEY_FILE_PATH","SSH_UTIL"]
            conf_status,configValues=get_config_value(configKeyList)
            if conf_status:
                private_key=configValues["PRIVATE_KEY_FILE_PATH"]
                command= f'ls {configValues["PRIVATE_KEY_FILE_PATH"]}'

                #Check if the private key is present inside device
                commandStatus,output = ssh_execute_cmd_DUT(configValues, command)
                if commandStatus and configValues["PRIVATE_KEY_FILE_PATH"] in output:
                    #Form ssh tunnel command
                    if execution_device_type== 'VA':
                        command=f'ssh -y -fN -i {private_key} -R {devicePort}:0.0.0.0:9998 -N {revportvm_username}@{deviceIP}'
                    else:
                        command=f"ssh -y -fN -i {private_key} -R {devicePort}:0.0.0.0:9998 -N -l {revportvm_username} -p 9090 {deviceIP}"

                    #Execute ssh tunnel command inside the device
                    commandStatus,output = ssh_execute_cmd_DUT(configValues, command)

                    #Check the device status
                    response,request_successful = check_device_status()
                    if request_successful and response is not None and response.status_code == 200:
                        print("FREE")
                    else:
                        print("NOT FOUND")
                else:
                    print("NOT FOUND")
            else:
                print("NOT FOUND")
        else:
            print("NOT FOUND")
