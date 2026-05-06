##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2026 RDK Management
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
import os
import sys
import configparser
import inspect
import SSHUtility
from SSHUtility import *
from web_socket_util import *

deviceToken = ""

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
# Parameters   : configkeylist  - a list to specify the configuration whose value needs to be retrieved from the <device>.config file
# Return Value : value of device configuration or error log in case of failure
#----------------------------------------------------------------------
def appmanagers_getdeviceconfig(configkeylist):
    configvalues = {}
    deviceconfigfile = ""
    configvalue = ""
    output = ""
    getdeviceconfig_status = "SUCCESS"
    print("[INFO] Retrieving Configuration values from config file")

    # Define config file paths
    configpath = libObj.realpath + "/" + "fileStore/tdkvRDKServiceConfig"
    devicenameconfigfile = configpath + "/" + deviceName + ".config"
    devicetypeconfigfile = configpath + "/" + deviceType + ".config"

    # Check which config file exists
    if os.path.exists(devicenameconfigfile) == True:
        deviceconfigfile = devicenameconfigfile
    elif os.path.exists(devicetypeconfigfile) == True:
        deviceconfigfile = devicetypeconfigfile
    else:
        output = "FAILURE : No Device config file found : " + devicenameconfigfile + " or " + devicetypeconfigfile
        print(output)
        getdeviceconfig_status = "FAILURE"
        return configvalues, getdeviceconfig_status

    # Get each configuration from device config file
    for configkey in configkeylist:
        try:
            if (len(deviceconfigfile) != 0) and (len(configkey) != 0):
                config = configparser.ConfigParser()
                config.read(deviceconfigfile)
                deviceConfig = config.sections()[0]
                configvalue = config.get(deviceConfig, configkey)
                configvalues[configkey] = configvalue
                if "FAILURE" not in configvalues[configkey] and configvalues[configkey] != "":
                    print("SUCCESS: Successfully retrieved %s configuration from device config file" % (configkey))
                else:
                    print("FAILURE: Failed to retrieve %s configuration from device config file" % (configkey))
                    getdeviceconfig_status = "FAILURE"
                    break
            else:
                output = "FAILURE : Device Config file or key cannot be empty"
                print(output)
                break
        except Exception as e:
            output = "FAILURE : Exception Occurred: [" + inspect.stack()[0][3] + "] " + str(e)
            print(output)
            break

    # Print all retrieved config key values
    print("\n[INFO] Retrieved configuration values")
    for key, value in configvalues.items():
        if value != "":
            print(f"{key} : {value}")
        else:
            print(f"{key} : Please configure the {key} key in the device config file")
    
    if getdeviceconfig_status != "FAILURE" and "SSH_USERNAME" in configvalues and "SSH_PASSWORD" in configvalues and "SSH_METHOD" in configvalues:
        global password
        global user_name
        global sshMethod
        if "directSSH" == configvalues["SSH_METHOD"]:
            sshMethod = configvalues["SSH_METHOD"]
            user_name = configvalues["SSH_USERNAME"]
            if configvalues["SSH_PASSWORD"] == "None":
                password = ""
            else:
                password = configvalues["SSH_PASSWORD"]
        else:
            print("FAILURE: Currently only supports directSSH ssh method")
            getdeviceconfig_status = "FAILURE"

    return configvalues, getdeviceconfig_status

#-------------------------------------------------------------------
# EXECUTE A COMMAND IN DUT SHELL AND GET THE OUTPUT
#-------------------------------------------------------------------
def appmanagers_executeInDUT(command):
    output = ""
    try:
        output = ssh_and_execute(sshMethod, deviceIP, user_name, password, command)
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
def execute_step(data):
    data = '{"jsonrpc": "2.0", "id": 1, '+data+'}'
    headers = {'content-type': 'text/plain;',}
    url = 'http://'+str(deviceIP)+':'+str(devicePort)+'/jsonrpc'
    try:
        response = requests.post(url, headers=headers, data=data, timeout=30)
        json_response = json.loads(response.content)
        print("---------------------------------------------------------------------------------------------------")
        print("Json command : ", data)
        print("\nResponse : ", json_response)
        print("----------------------------------------------------------------------------------------------------")
        result = json_response
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
def appmanagers_getvalue(method):
    data = '"method": "'+method+'"'
    result = execute_step(data)
    return result

#------------------------------------------------------------------
# SET VALUE FOR A METHOD
#------------------------------------------------------------------
def appmanagers_setvalue(method,value):
    data = '"method": "'+method+'","params": '+value
    result = execute_step(data)
    return result

#-----------------------------------------------------------------
# GET PLUGIN STATUS
#-----------------------------------------------------------------
def appmanagers_getpluginstatus(plugin):
    data = '"method": "Controller.1.status@'+plugin+'"'
    result = execute_step(data)
    result = result.get("result")
    if result != None:
        for x in result:
            PluginStatus=x["state"]
        return PluginStatus
    else:
        return result

#------------------------------------------------------------------
# CHECK PLUGIN STATUS
#------------------------------------------------------------------
def appmanagers_checkpluginstatus(pluginlist):
    checkpluginstatus = "SUCCESS"
    print("[INFO] Checking and Activating plugins if not in activated state\n")
    for plugin in pluginlist:
        params = '{"callsign": "'+plugin+'"}'
        status = appmanagers_getpluginstatus(plugin)
        if status == "deactivated":
            print(f"[INFO] Activating {plugin} plugin")
            status = appmanagers_setvalue("Controller.1.activate", params)
            status = appmanagers_getpluginstatus(plugin)
            if status == "activated":
                print(f"SUCCESS : {plugin} plugin in {status} state\n")
            else:
                print(f"FAILURE: {plugin} plugin in {status} state\n")
                checkpluginstatus = "FAILURE"
                break
        elif status == "activated":
            print(f"SUCCESS : {plugin} plugin already in {status} state\n")
        else:
            print(f"FAILURE : {plugin} plugin in {status} state\n")
            checkpluginstatus = "FAILURE"
            break
    return checkpluginstatus

#------------------------------------------------------------------
# WAIT FOR EVENT
#------------------------------------------------------------------
def wait_for_event(event_listener,max_wait=60, initial_delay=10):
    time.sleep(initial_delay)
    continue_count = 0
    while continue_count <= max_wait:
        events = event_listener.getEventsBuffer()
        if len(events) == 0:
            continue_count += 1
            time.sleep(1)
            continue
        print("\nReceived Events ....")
        print("---------------------------------------------------------------------------------------------------")
        print(events)
        print("---------------------------------------------------------------------------------------------------")
        return events
    
    print(f"\n[INFO] : No events received within {max_wait} seconds")
    return events