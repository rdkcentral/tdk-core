##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2023 RDK Management
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
import ConfigParser
from time import sleep
import pexpect
import time
from SecurityTokenUtility import *
from ip_change_detection_utility import *
import importlib

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
       print "\nException Occurred while getting MAC \n"
       print e

#------------------------------------------------------------------------------
# Function to retreive the config values set in the corresponding config file
#------------------------------------------------------------------------------
def getDeviceConfig (configKey):
    deviceConfigFile=""
    configValue = ""
    output = ""
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
        print output
    try:
        if (len (deviceConfigFile) != 0) and (len (configKey) != 0):
            config = ConfigParser.ConfigParser ()
            config.read (deviceConfigFile)
            deviceConfig = config.sections ()[0]
            configValue =  config.get (deviceConfig, configKey)
            output = configValue
        else:
            output = "FAILURE : DeviceConfig file or key cannot be empty"
            print output
    except Exception as e:
        output = "FAILURE : Exception Occurred: [" + inspect.stack()[0][3] + "] " + e.message
        print output
    return output

#-------------------------------------------------------------------
# Function to execute the command in the DUT using ssh utility
#-------------------------------------------------------------------
def executeInDUT (command,sshMethod="", credentials=""):
    output = ""
    rdkv_performancelib.deviceName = deviceName
    rdkv_performancelib.deviceType = deviceType
    ssh_param = rdkv_performancelib.rdkservice_getSSHParams(libObj.realpath,deviceIP)
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
        print "Secure ssh to CPE"
        pass
    try:
        output = ssh_and_execute (sshMethod, host_name, user_name, password, command)
    except Exception as e:
        print "Exception occured during ssh session"
        print e
    return output

#---------------------------------------------------------------
#POST CURL REQUEST USING PYTHON REQUESTS
#---------------------------------------------------------------
def postCURLRequest(data,securityEnabled):
    status = "SUCCESS"
    json_response={}
    if securityEnabled:
        Bearer = 'Bearer ' + deviceToken
        headers = {'content-type': 'text/plain;',"Authorization":Bearer}
    else:
        headers = {'content-type': 'text/plain;',}
    url = 'http://'+str(deviceIP)+':'+str(devicePort)+'/jsonrpc'
    try:
        response = requests.post(url, headers=headers, data=data, timeout=20)
        json_response = json.loads(response.content)
        if json_response.get("error") != None and "Missing or invalid token" in json_response.get("error").get("message"):
            status = "INVALID TOKEN"
    except requests.exceptions.RequestException as e:
        status = "FAILURE"
        print "ERROR!! \nEXCEPTION OCCURRED WHILE EXECUTING CURL COMMANDS!!"
        print "Command : ",data
        print "Error message received :\n",e;
        response = "EXCEPTION OCCURRED"
    return response,json_response,status

#---------------------------------------------------------------
#EXECUTE CURL REQUESTS
#---------------------------------------------------------------
def execute_step(Data):
    status = "SUCCESS"
    global securityEnabled
    try:
        data = '{"jsonrpc": "2.0", "id": 1234567890, '+Data+'}'
        response,json_response,status = postCURLRequest(data,securityEnabled)
        if status == "INVALID TOKEN":
           print "\nAuthorization issue occurred. Update Token & Re-try..."
           global deviceToken
           tokenFile = libObj.realpath + "/" + "fileStore/tdkvRDKServiceConfig/tokenConfig/" + deviceName + ".config"
           if not securityEnabled:
               # Create the Device Token config file and update the token
               token_status,deviceToken = read_token_config(deviceIP,tokenFile)
               if token_status == "SUCCESS":
                   print "Device Security Token obtained successfully"
               else:
                   print "Failed to get the device security token"
               securityEnabled = True
           else:
               # Update the token in the device token config file
               token_status,deviceToken  = handleDeviceTokenChange(deviceIP,tokenFile)
           if token_status == "SUCCESS":
               response,json_response,status = postCURLRequest(data,securityEnabled)
           else:
               print "Failed to update the token in token config file"
           if status == "INVALID TOKEN":
               token_status,deviceToken  = handleDeviceTokenChange(deviceIP,tokenFile)
               if token_status == "SUCCESS":
                   response,json_response,status = postCURLRequest(data,securityEnabled)
               else:
                   status = "FAILURE"
        web_socket_util.deviceToken = deviceToken
        if status == "SUCCESS":
            print "\n---------------------------------------------------------------------------------------------------"
            print "Json command : ", data
            print "\n Response : ", json_response, "\n"
            print "----------------------------------------------------------------------------------------------------\n"
            result = json_response.get("result")
            if result != None and "'success': False" in str(result):
                result = "EXCEPTION OCCURRED"

        else:
            result = response;
        return result;
    except requests.exceptions.RequestException as e:
        print "ERROR!! \nEXCEPTION OCCURRED WHILE EXECUTING CURL COMMANDS!!"
        print "Error message received :\n",e;
        return "EXCEPTION OCCURRED"

#--------------------------------------------------------------------------
# Function to check if cobalt application is already installed in the DUT
#--------------------------------------------------------------------------
def checkApplicationInstalled():
    method = "LISA.1.getList"
    params ='{}'
    result = executeCurlCommand(method,params);
    print "getList Result",result

    installed = "FAILURE"
    cobalt_app_id = getDeviceConfig ('COBALT_APP_ID')
    if cobalt_app_id in str(result):
        print "Application is installed"
        print "Proceeding to launching"
        installed="SUCCESS"
    else:
        print "Application is not installed"
        print "Proceeding to install application"
        
    return installed

#-------------------------------------------------------------------
# Function to execute the curl command
#-------------------------------------------------------------------
def executeCurlCommand(method,value):
    data = '"method": "'+method+'","params": '+value
    result = execute_step(data)
    return result

#-------------------------------------------------------------------
# Function to install cobalt dac bundle hosted in the server
#-------------------------------------------------------------------
def InstallApplication():
    method = "LISA.1.install"
    cobalt_app_id = getDeviceConfig ('COBALT_APP_ID')
    params ='{"id":"' + cobalt_app_id + '","url":"'
    cobalt_bundle = getDeviceConfig ('COBALT_DAC_BUNDLE_PATH')
    params  = params + cobalt_bundle
    params = params + '","version":"1.0.0","appName":"' + cobalt_app_id + '","type":"dac","category":"category"}'
    result = executeCurlCommand(method,params);
    print "LISA install result",result
    status="FAILURE"
    if result.isnumeric():
        #tdkTestObj.setResultStatus("SUCCESS")
        status="SUCCESS"
        application_wait_timeout = getDeviceConfig ('APPLICATION_INSTALLATION_TIMEOUT')
        time.sleep(float(application_wait_timeout))
    else:
        print "LISA installation failed"
        #tdkTestObj.setResultStatus("FAILURE")
    return status

#-------------------------------------------------------------------
# Function to launch cobalt application and set it to Front
#-------------------------------------------------------------------
def LaunchApplication():
    cobalt_app_id = getDeviceConfig ('COBALT_APP_ID')
    print "Launching %s application"%(cobalt_app_id)
    method = "org.rdk.RDKShell.1.launchApplication"
    params ='{"client":"' + cobalt_app_id + '","mimeType":"application/dac.native","uri":"' + cobalt_app_id +';1.0.0"}'
    result = executeCurlCommand(method,params);
    print "launchApplication Result",result

    if "True" in str(result):
        print "Get Clients of RDKShell to verify if cobalt is launched"
        method = "org.rdk.RDKShell.1.getClients"
        result = executeCurlCommand(method,params);
        print "getClients Result",result

        if "True" in str(result) and cobalt_app_id in str(result):
            print "Cobalt is successfully launched"
            print "SetFocus of cobalt to front"
            method = "org.rdk.RDKShell.1.setFocus"
            params = '{"client":"' + cobalt_app_id + '"}'
            result = executeCurlCommand(method,params);
            print "setFocus result",result

            if "True" in str(result):
                print "Cobalt set to front successfully"

            else:
                print "Unable to set cobalt to front"
                return "FAILURE"

        else:
            print "Cobalt was not obtained as RDKShell Clients"
            return "FAILURE"

    else:
        print "Cobalt laucnh failure"
        return "FAILURE"

    return "SUCCESS"

#-------------------------------------------------------------------
# Function to press keys simulating play/pause operations
#-------------------------------------------------------------------
def Press_key(key_code):
    method = "org.rdk.RDKShell.1.generateKey"
    params = '{"keys":[{"keyCode": '
    params = params + str(key_code) +',"modifiers": [],"delay":1.0}]}}'
    result = executeCurlCommand(method,params);
    print "RDKShell generate key",result
    status="FAILURE"
    if "True" in str(result):
        status="SUCCESS"
    else:
        print "RDKShell generate key failed"
    return status

#-------------------------------------------------------------------
# Function to kill the cobalt application after testing
#-------------------------------------------------------------------
def KillApplication():
    method = "org.rdk.RDKShell.1.kill"
    cobalt_app_id = getDeviceConfig ('COBALT_APP_ID')
    params ='{"client":"' + cobalt_app_id + '"}'
    result = executeCurlCommand(method,params);
    print "Kill Application result",result
    status="FAILURE"
    if "True" in str(result):
        status="SUCCESS"
    else:
        print "Cobalt kill application failed"
    return status

#-------------------------------------------------------------------
# Function to check required pattern in proc entry file
#-------------------------------------------------------------------
def checkProcEntry(sshMethod,credentials,validation_script,mode):
    result = "FAILURE"
    validation_script = validation_script.split('.py')[0]
    try:
        lib = importlib.import_module(validation_script)
        method = "check_video_status"
        method_to_call = getattr(lib, method)
        result = method_to_call(sshMethod,credentials,mode)
    except Exception as e:
        print e;
        print "[ERROR]: Failed to import video validation script file, please check the configuration"
        result = "FAILURE"
    finally:
        return result

#-------------------------------------------------------------------
# Function to read the proc validation parameters from device config file
#-------------------------------------------------------------------
def checkPROC(check_pause):
    proc_check = getDeviceConfig ('RIALTO_PROC_VALIDATION')
    if "YES" in proc_check:
        rdkv_performancelib.deviceName = deviceName
        rdkv_performancelib.deviceType = deviceType
        ssh_param = rdkv_performancelib.rdkservice_getSSHParams(libObj.realpath,deviceIP)
        ssh_param_dict = json.loads(ssh_param)
        sshMethod = ssh_param_dict["ssh_method"]
        credentials = ssh_param_dict['credentials']
        validation_script = getDeviceConfig ('VIDEO_VALIDATION_SCRIPT_FILE')
        proc_file_path = libObj.realpath + "/"   + "fileStore/" + validation_script
        print "proc validation file: ",proc_file_path
        if not os.path.exists(proc_file_path) :
            print " PROC entry file is missing from fileStore "
            return "FAILURE"
        mode = getDeviceConfig ('PROC_CHECK_MODE')
        if check_pause == "True":
             mode = mode + "-paused"
        av_status = checkProcEntry(sshMethod,credentials,validation_script,mode)
        return av_status
    else:
        print "PROC Entry validation is disabled"
        return "NOT_ENABLED"

def ChangeContainerStatus(operation):
    if operation == "pause":
        method = "org.rdk.OCIContainer.pauseContainer"
    elif operation == "resume":
        method = "org.rdk.OCIContainer.resumeContainer"
    else:
        return "FAILURE"
    cobalt_app_id = getDeviceConfig ('COBALT_APP_ID')
    params =' { "containerId": "' + cobalt_app_id + '" } }'
    result = executeCurlCommand(method,params);
    print "Container status change result",result
    status="FAILURE"
    if "True" in str(result):
        status="SUCCESS"
    else:
        print "Container status change failed"
    return status
