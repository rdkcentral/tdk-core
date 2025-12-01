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

import tdklib
import json
import ast
import sys
import re
from SSHUtility import *
import SSHUtility
import requests
import time
import os
import inspect
import configparser

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

#----------------------------------------------------------------------
# GET DEVICE CONFIGURATION FROM THE DEVICE CONFIG FILE
# Description  : Read the value of device configuration from the <device>.config file
# Parameters   : basePath - a string to specify the path of the TM
#                configKey - a string to specify the configuration whose value needs to be retrieved from the <device>.config file
# Return Value : value of device configuration or error log in case of failure
#----------------------------------------------------------------------
def memcr_getDeviceConfig (basePath, configKey):
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
def memcr_obtainCredentials():
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
        memcr_getDeviceConfig(libObj.realpath,configKey)
        configValues[configKey] = memcr_getDeviceConfig(libObj.realpath,configKey)
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
def memcr_executeInDUT (sshMethod, credentials, command):
    output = ""
    if sshMethod == "directSSH":
        credentialsList = credentials.split(',')
        host_name = credentialsList[0]
        user_name = credentialsList[1]
        password = credentialsList[2]
    else:
        print("Secure ssh to CPE")
        pass
    try:
        output = ssh_and_execute (sshMethod, host_name, user_name, password, command)
    except Exception as e:
        print("Exception occured during ssh session")
        print(e)
    return output

#---------------------------------------------------------------
# EXECUTE CURL REQUESTS
# Description  : Execute curl request in DUT
# Parameters   : Data - a string which contains actual curl request
# Return Value : contains response of the curl request sent
#---------------------------------------------------------------
def execute_step(Data):
    data = '{"jsonrpc": "2.0", "id": 1, '+Data+'}'
    headers = {'content-type': 'text/plain;',}
    url = 'http://'+str(deviceIP)+':'+str(devicePort)+'/jsonrpc'
    try:
        response = requests.post(url, headers=headers, data=data, timeout=30)
        json_response = json.loads(response.content)
        print("---------------------------------------------------------------------------------------------------")
        print("Json command : ", data)
        print("\n Response : ", json_response)
        print("----------------------------------------------------------------------------------------------------")
        result = json_response.get("result")
    except requests.exceptions.RequestException as e:
        print("---------------------------------------------------------------------------------------------------")
        print("Json command : ", data)
        print("Error Message Received : ",e)
        print("---------------------------------------------------------------------------------------------------")
        sys.exit()
    return result

#-------------------------------------------------------------------
# GET THE VALUE OF A METHOD
#-------------------------------------------------------------------
def memcr_getValue(method):
    data = '"method": "'+method+'"'
    result = execute_step(data)
    return result

#------------------------------------------------------------------
# SET VALUE FOR A METHOD
#------------------------------------------------------------------
def memcr_setValue(method,value):
    data = '"method": "'+method+'","params": '+value
    result = execute_step(data)
    return result

#-----------------------------------------------------------------
# GET PLUGIN STATUS
#-----------------------------------------------------------------
def memcr_getPluginStatus(plugin):
    data = '"method": "Controller.1.status@'+plugin+'"'
    result = execute_step(data)
    if result != None:
        for x in result:
            PluginStatus=x["state"]
        return PluginStatus
    else:
        return result

#------------------------------------------------------------------
# CHECK DEVICE STATUS
#------------------------------------------------------------------
def memcr_getTestDeviceStatus():
    try:
        data = '{"jsonrpc":"2.0","id":"2","method": "Controller.1.status@Controller"}'
        headers = {'content-type': 'text/plain;'}
        url = 'http://' + str(deviceIP) + ':' + str(devicePort) + '/jsonrpc'
        response = requests.post(url, headers=headers, data=data, timeout=3)
        if response.status_code == 200:
            jsonResponse = json.loads(response.content,strict=False)
            return "FREE"
        else:
            return "NOT_FOUND"
    except Exception as e:
        return "NOT_FOUND"

#------------------------------------------------------------------
# CHECK PLUGIN STATUS
#------------------------------------------------------------------
def memcr_checkPluginStatus(method,params):
    checkpluginstatus = "SUCCESS"
    status = memcr_getPluginStatus(method)
    if status != "activated":
        print("[INFO] Activating "+method+" plugin")
        status = memcr_setValue("Controller.1.activate",params)
        status = memcr_getPluginStatus(method)
    if status == "activated":
        print("SUCCESS : "+method+" plugin in activated state\n")
    else:
        print("FAILURE: Unable to activate "+method+"\n")
        checkpluginstatus = "FAILURE"
    return checkpluginstatus

#------------------------------------------------------------------
# REBOOT THE DEVICE
#------------------------------------------------------------------
def memcr_rebootDevice(waitTime):
    rebootdevicestatus = "SUCCESS"
    status = memcr_getPluginStatus("org.rdk.System")
    timeout = time.time() + 30*5
    deviceStatus = "DOWN"
    if status != "activated":
        print("[INFO] Activating System plugin for rebooting the device")
        params = '{"callsign":"org.rdk.System"}'
        status = memcr_setValue("Controller.1.activate",params)
        status = memcr_getPluginStatus("org.rdk.System")
    if status == "activated":
        print("[INFO] System plugin is activated")
        data = '"method": "org.rdk.System.1.reboot","params": {"rebootReason": "TDK_TESTING"}'
        result = execute_step(data)
        result = result.get("success")
        if str(result).lower() == "true":
            print("\n[INFO] Waiting for the device to come up...")
            time.sleep(waitTime)
            while True:
                status = memcr_getTestDeviceStatus()
                if status == "FREE":
                    deviceStatus = "UP"
                    break;
                elif time.time() > timeout:
                    deviceStatus = "DOWN"
                    print("[INFO] Device is not coming up even after 2.5 mins")
                    break;
                time.sleep(5)
            if deviceStatus == "UP":
                print("[INFO] Device is UP")
            else:
                print("[INFO] Device is DOWN")
                rebootdevicestatus = "FAILURE"
        else:
            print(result)
            rebootdevicestatus = "FAILURE"
    else:
        print("FAILURE: Unable to activate System plugin")
        rebootdevicestatus = "FAILURE"
    return rebootdevicestatus

#-----------------------------------------------------------------
# GET THE TR181 PARAMETER VALUE
#-----------------------------------------------------------------
def memcr_getTR181Value(basePath,configKey):
    getTR181Valuestatus = "SUCCESS"
    configValue = memcr_getDeviceConfig (basePath, configKey)
    if len(configValue) == 0:
        print("FAILURE : Please configure the "+configKey+" in device config file\n")
        getTR181Valuestatus = "FAILURE"
    else:
        print("SUCCESS : Successfully retrieved "+configKey+" in device config file\n")
    return configValue,getTR181Valuestatus

#---------------------------------------------------------------
# ENABLE THE REQUIRED DATA MODEL IN THE DUT
# Description  : To enable the required data model in the DUT
# Parameters   : datamodel - Data model list which needs to be enabled
# Return Value : Returns 'SUCCESS' on successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------
def memcr_datamodelcheck(datamodel):
    datamodelcheck_status = "SUCCESS"
    rebootFlag = 0
    global default_state
    status = memcr_obtainCredentials()
    if "FAILURE" not in status:
        credentials = deviceIP + ',' + user_name + ',' + password
        command =  'tr181 -d '+str(datamodel)
        print("COMMAND : %s" %(command))
        output = memcr_executeInDUT(sshMethod,credentials,command)
        if "FAILURE" not in output:
            output = str(output).split("\n")[1]
            print(output)
            if "true" in output.lower():
                print('SUCCESS: '+datamodel+' parameter is already enabled\n')
            elif "false" in output.lower() or "empty" in output.lower():
                default_state = "FAILURE"
                command =  'tr181 -d -s -t boolean -v true '+datamodel
                print("COMMAND : %s" %(command))
                enableStatus = memcr_executeInDUT(sshMethod,credentials,command)
                enableStatus = enableStatus.strip()
                if "set operation success" in enableStatus.lower():
                    rebootFlag = 1
                    print('SUCCESS: Successfully set the '+datamodel+' parameter\n')
                else:
                    print(enableStatus)
                    print('FAILURE: Could not able to set the '+datamodel+' parameter\n')
                    datamodelcheck_status = "FAILURE"
            else:
                print(output)
                print('FAILURE: Failed to retrieve '+datamodel+' enabled status\n')
                datamodelcheck_status = "FAILURE"
        else:
            print('FAILURE: Error while executing the command\n')
            datamodelcheck_status = "FAILURE"
        
        if "FAILURE" not in datamodelcheck_status and rebootFlag == 1:
            print('[INFO] Rebooting the Device................')
            status = memcr_rebootDevice(60)
            if "SUCCESS" in status:
                command =  'tr181 -d '+datamodel
                print("COMMAND : %s" %(command))
                enableStatus = memcr_executeInDUT(sshMethod,credentials,command)
                enableStatus = str(enableStatus).split("\n")[1]
                if "true" in enableStatus.lower():
                    print(enableStatus)
                    print('SUCCESS: Successfully enabled the '+datamodel+' parameter\n')
                else:
                    print(enableStatus)
                    print('FAILURE: '+datamodel+' parameter not enabled\n')
                    datamodelcheck_status = "FAILURE"
            else:
                print('FAILURE: Error while rebooting the device\n')
                datamodelcheck_status = "FAILURE"
    else:
        print('FAILURE: Failed to retrieve required configurations\n')
        datamodelcheck_status = "FAILURE"
    return datamodelcheck_status

#-----------------------------------------------------------------
# CHECK THE MEMCR STATUS
#-----------------------------------------------------------------
def memcr_statuscheck():
    memcrstatus="SUCCESS"
    config_status=memcr_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #check parodus status
        command="systemctl status memcr | grep running"
        print("Executing Command : %s" %command)
        #execute in DUT function
        result = memcr_executeInDUT(sshMethod, credentials, command)
        result = result.split("\n")
        result=str(result[1])
        if "active (running)" in result:
            print(result)
            print("SUCCESS : Successfully get the memcr status\n")
        else:
            print(result)
            print("FAILURE : Memcr Process is not running\n")
            memcrstatus="FAILURE"
    else:
        print("FAILURE : Failed to get the device credentials\n")
        memcrstatus="FAILURE"
    return memcrstatus

#-----------------------------------------------------------------
# GET THE MEMORY USAGE OF APPLICATIONS
#-----------------------------------------------------------------
def memcr_appMemorySize(processID):
    output = 0
    appmemorysizestatus="SUCCESS"
    config_status = memcr_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #get the memory usage of app
        command = "cd /proc/"+processID+"; grep -i 'VmRSS' status | awk '{print $2$3}'"
        print("Executing Command : %s" %command)
        #execute in DUT function
        output = memcr_executeInDUT (sshMethod, credentials, command)
        output = output.split("\n")
        output = output[1]
        # Regular expression to match a number followed by optional unit
        if re.match(r'(\d+)([a-zA-Z]*)$',output.strip()):
            print("Memory Usage of app : "+output)
        else:
            print("FAILURE : Failed to get the memory usage\n")
            appmemorysizestatus="FAILURE"
    else:
        print("FAILURE : Failed to get the device credentials\n")
        appmemorysizestatus="FAILURE"
    return appmemorysizestatus,output

#-----------------------------------------------------------------
# GET THE PROCESS ID OF APPLICATIONS
#-----------------------------------------------------------------
def memcr_getProcessID(appname):
    output = 0
    getprocessidstatus="SUCCESS"
    config_status = memcr_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #get the processID of app
        command = "ps -aux | grep 'WPEProcess' | grep '"+appname+"' | awk \'NR==1 {print $2}\'"
        print("Executing Command : %s" %command)
        #execute in DUT function
        output = memcr_executeInDUT (sshMethod, credentials, command)
        output = output.split("\n")
        output = output[1]
        if int(output) > 0:
            print("Process ID : "+output)
        else:
            print("FAILURE : Invalid proccessID\n")
            getprocessidstatus="FAILURE"
    else:
        print("FAILURE : Failed to get the device credentials\n")
        getprocessidstatus="FAILURE"
    return getprocessidstatus,output

#-----------------------------------------------------------------
# CHECK IF THE IMAGE IS PRESENT OR NOT
#-----------------------------------------------------------------
def memcr_checkImgFile(filepath,processID,checkfile):
    checkimagefilestatus="SUCCESS"
    config_status = memcr_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #get the processID of app
        command = "ls "+filepath+"/pages-"+processID+".img > /dev/null 2>&1 && echo 1 || echo 0"
        print("Executing Command : %s" %command)
        #execute in DUT function
        output = memcr_executeInDUT (sshMethod, credentials, command)
        output = output.split("\n")
        output = output[1]
        if checkfile == "nonemptyfilecheck":
            if int(output) == 1:
                print("SUCCESS : Compressed app image file is present\n")
            else:
                print(output)
                print("FAILURE : Compressed app image file is not present\n")
                checkimagefilestatus="FAILURE"
        else:
            if int(output) == 0:
                print("SUCCESS : Compressed app image file is not present\n")
            else:
                print(output)
                print("FAILURE : Compressed app image file is present\n")
                checkimagefilestatus="FAILURE"
    else:
        print("FAILURE : Failed to get the device credentials\n")
        checkimagefilestatus="FAILURE"
    return checkimagefilestatus

#-----------------------------------------------------------------
# CHECK APPHIBERNATE RFC PARAMETER VALUE
#-----------------------------------------------------------------
def memcr_checkAppHibernateRFC(datamodel):
    checkAppHibernateRFC = "SUCCESS"
    status = memcr_obtainCredentials()
    if "FAILURE" not in status:
        credentials = deviceIP + ',' + user_name + ',' + password
        command =  'tr181 -d '+str(datamodel)
        print("COMMAND : %s" %(command))
        output = memcr_executeInDUT(sshMethod,credentials,command)
        output = str(output).split("\n")[1]
        print(output)
        if "true" in output.lower():
            print('SUCCESS: '+datamodel+' parameter is enabled\n')
        else:
            print('FAILURE : '+datamodel+' parameter is disabled\n')
            checkAppHibernateRFC = "FAILURE"
    else:
        print('FAILURE : Failed to get the device credentials\n')
        checkAppHibernateRFC = "FAILURE"
    return checkAppHibernateRFC

#---------------------------------------------------------------
# RESTART WPEFRAMEWORK SERVICE
#---------------------------------------------------------------
def memcr_restart_wpeframework_service():
    wpeframework_servicestatus = "SUCCESS"
    status = memcr_obtainCredentials()
    if "FAILURE" not in status:
        credentials = deviceIP + ',' + user_name + ',' + password
        command = 'systemctl restart wpeframework 2>/dev/null ; sleep 25s ; systemctl status wpeframework 2>/dev/null | grep active  | cut -d ";" -f 2 | cut -d " " -f 2'
        print("COMMAND : %s" %(command))
        output = memcr_executeInDUT(sshMethod,credentials,command)
        output = str(output).split("\n")[1]
        output = output.replace("s","").strip()
        if 25 <= int(output) <= 30:
            print("SUCCESS : Successfully restarted wpeframework service with the delay of "+output+" seconds\n")
        else:
            print("FAILURE : Failed to restart wpeframework service with the delay of "+output+" seconds\n")
            wpeframework_servicestatus = "FAILURE"
    else:
        print("FAILURE : Failed to get the device credentials\n")
        wpeframework_servicestatus = "FAILURE"
    return wpeframework_servicestatus

#----------------------------------------------------------------------
# VALIDATE WPEFRAMEWORK LOGS DURING HIBERNATE AND RESTORE OPERATIONS
#----------------------------------------------------------------------
def memcr_logValidation(log_Occurrences):
    logValidation_status = "SUCCESS"
    status = memcr_obtainCredentials()
    if "FAILURE" not in status:
        credentials = deviceIP + ',' + user_name + ',' + password
        command = 'journalctl --since "1 min ago" -x -u wpeframework | grep -inr "'+log_Occurrences+'"'
        print("COMMAND : %s" %(command))
        output = memcr_executeInDUT(sshMethod,credentials,command)
        output = str(output).split("\n")[1]
        if len(output) and log_Occurrences in output:
            print(output)
            print("SUCCESS : Log entry found\n")
        else:
            print(output)
            print("FAILURE : Log entry not found\n")
            logValidation_status = "FAILURE"
    else:
        print("FAILURE : Failed to get the device credentials\n")
        logValidation_status = "FAILURE"
    return logValidation_status

#----------------------------------------------------------------------
# LAUNCH THE APP
#----------------------------------------------------------------------
def memcr_launchapp(obj, value):
    try:
        method = "org.rdk.RDKShell.1.launch"
        expectedResult = "SUCCESS"
        tdkTestObj = obj.createTestStep('memcr_setValue')
        tdkTestObj.addParameter("method", method)
        tdkTestObj.addParameter("value", value)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResultDetails()
        result = ast.literal_eval(str(result))
        appstate = result["launchType"]
        success = str(result["success"])
        return appstate, success
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
