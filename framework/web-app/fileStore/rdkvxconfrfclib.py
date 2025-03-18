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
import json
import time
import os
import subprocess
import inspect
import configparser
from time import sleep
import pexpect
import tdklib

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
def rfc_getDeviceConfig (basePath, configKey):
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
def rfc_obtainCredentials():
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
        rfc_getDeviceConfig(libObj.realpath,configKey)
        configValues[configKey] = rfc_getDeviceConfig(libObj.realpath,configKey)
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
def rfc_executeInDUT (sshMethod, credentials, command):
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

#---------------------------------------------------------------
# Validate the RFC URL
#---------------------------------------------------------------
def rfc_urlvalidate(basePath, configKey):
    rfc_urlvalidatestatus="SUCCESS"
    configValue = rfc_getDeviceConfig (basePath, configKey)
    if "FAILURE" not in configValue:
        if len(configValue) == 0:
            output = "[INFO] - Please configure the xconf server URL in device config file"
            print(output)
            rfc_urlvalidatestatus="FAILURE"
        else:
            config_status=rfc_obtainCredentials()
            if "FAILURE" not in config_status:
                credentials = deviceIP + ',' + user_name + ',' + password
                #validate the given URl by CURL command under DUT
                command="curl -is "+configValue+" | head -n 1"
                print("Executing Command : %s" %command)
                result=rfc_executeInDUT (sshMethod, credentials, command)
                result=result.split("\n")
                result=str(result[1])
                if "200" in result:
                    output = configValue
                    print("SUCCESS : Configured xconf server URL : "+output+" accessed by the device")
                else:
                    output = configValue
                    output = "FAILURE : Please configure accessible xconf server URL : "+output
                    print(output)
                    rfc_urlvalidatestatus="FAILURE"
            else:
                output="FAILURE : Failed to get the device credentials"
                print(output)
                rfc_urlvalidatestatus="FAILURE"
    else:
        output="FAILURE : Failed to get the XCONF server URL"
        print(output)
        rfc_urlvalidatestatus="FAILURE"
    return rfc_urlvalidatestatus,output

#---------------------------------------------------------------
# Form FEATURE NAME
#---------------------------------------------------------------
def rfc_formfeaturename(feature_name):
    formfeaturenamestatus="SUCCESS"
    deviceMACstatus=rfc_getmacaddress()
    if "FAILURE" not in deviceMACstatus:
        feature_name = "TDKV_RFC_"+feature_name+"_"+deviceMAC
    else:
        formfeaturenamestatus="FAILURE"
    return formfeaturenamestatus,feature_name

#---------------------------------------------------------------
# GET DEVICE MAC ADDRESS
#---------------------------------------------------------------
def rfc_getmacaddress():
    getmacaddressstatus="SUCCESS"
    config_status=rfc_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #get the MAC address from device
        command="ifconfig | awk '/eth0/ {print $5}'"
        print("Executing Command : %s" %command)
        #execute in DUT function
        global deviceMAC
        deviceMAC=rfc_executeInDUT (sshMethod, credentials, command)
        deviceMAC=deviceMAC.split("\n")
        deviceMAC=deviceMAC[1]
        deviceMAC=deviceMAC.strip()
        if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$",str(deviceMAC).lower()):
            print("\nSUCCESS : Successfully get the MAC address")
        else:
            print("\nFAILURE : Failed to get the MAC address")
            getmacaddressstatus="FAILURE"
    else:
        print("\nFAILURE : Failed to get the device credentials")
        getmacaddressstatus="FAILURE"
    return getmacaddressstatus

#-----------------------------------------------------------------
# CHECK RFC PARAMETER STATUS
#-----------------------------------------------------------------
def rfc_datamodelcheck(rfcparameter):
    config_status=rfc_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #check rfc parameter status
        command="tr181 -d "+str(rfcparameter)
        print("Executing Command : %s" %command)
        #execute in DUT function
        result=rfc_executeInDUT (sshMethod, credentials, command)
        result=str(result).split("\n")[2]
        result=result.strip()
        print(result)
    else:
        print("\nFAILURE : Failed to get the device credentials")
        result="FAILURE"
    return result

#---------------------------------------------------------------
# INITIALIZE FEATURE AND FEATURE RULE CREATION OR UPDATE
#---------------------------------------------------------------
def rfc_initializefeatures(feature_name,xconfdomainname,rfcparameter,expectedvalue):
    initializefeaturestatus="SUCCESS"
    global feature_id
    global feature_rule_id
    deviceMACstatus=rfc_getmacaddress()
    if "FAILURE" not in deviceMACstatus:
        config_status=rfc_obtainCredentials()
        if "FAILURE" not in config_status:
            credentials = deviceIP + ',' + user_name + ',' + password
            #check feature already present or not
            command='curl -sX  GET '+"'"+xconfdomainname+'feature/filtered?APPLICATION_TYPE=stb&NAME='+feature_name+"'"+' -H "Content-Type: application/json" -H "Accept: application/json" | cut -d "," -f 1 | cut -d ":" -f 2'
            print("Executing Command : %s" %command)
            #execute in DUT function
            result=rfc_executeInDUT (sshMethod, credentials, command)
            result=str(result).split("\n")
            result=str(result[1])
            feature_id=result.replace('"','').strip()
            if "[]" not in feature_id:
                print("Feature is already present")
                print(feature_name+" "+"feature retrieved successfully")
                #check feature rule already present or not
                command='curl -sX  GET '+"'"+xconfdomainname+'featurerule/filtered?APPLICATION_TYPE=stb&NAME='+feature_name+"'"+' -H "Content-Type: application/json" -H "Accept: application/json" | cut -d "," -f 1 | cut -d ":" -f 2'
                print("Executing Command : %s" %command)
                #execute in DUT function
                result=rfc_executeInDUT (sshMethod, credentials, command)
                result=str(result).split("\n")
                result=str(result[1])
                feature_rule_id=result.replace('"','').strip()
                if "[]" not in feature_rule_id:
                    print("Feature rule is already present")
                    print(feature_name+" "+"feature rule retrieved successfully")
                    #Update feature
                    command='curl -sX POST '+xconfdomainname+'feature/importAll -H "Content-Type: application/json" -H "Accept: application/json" -d \'[{"id":"'+feature_id+'","name":"'+feature_name+'","effectiveImmediate":true,"enable":true,"whitelisted":false,"configData":{"tr181.'+rfcparameter+'":"'+expectedvalue+'"},"whitelistProperty":{},"applicationType":"stb","featureInstance":"'+feature_name+'"}]\''
                    print("Executing Command : %s" %command)
                    #execute in DUT function
                    result=rfc_executeInDUT (sshMethod, credentials, command)
                    if "IMPORTED" in result:
                        print("\nSUCCESS : Feature updated successfully")
                        feature_rule_id=feature_rule_id.strip()
                        #Update feature rule
                        command='curl -sX POST '+xconfdomainname+'featurerule/importAll -H "Content-Type: application/json" -H "Accept: application/json" -d \'[{"id":"'+feature_rule_id+'","name":"'+feature_name+'","rule":{"negated":false,"compoundParts":[{"negated":false,"condition":{"freeArg":{"type":"STRING","name":"estbIP"},"operation":"IS","fixedArg":{"bean":{"value":{"java.lang.String":"'+deviceIP+'"}}}},"compoundParts":[]},{"negated":false,"relation":"OR","condition":{"freeArg":{"type":"STRING","name":"estbMacAddress"},"operation":"IS","fixedArg":{"bean":{"value":{"java.lang.String":"'+deviceMAC+'"}}}},"compoundParts":[]}]},"priority":4,"featureIds":["'+feature_id+'"],"applicationType":"stb"}]\''
                        print("Executing Command : %s" %command)
                        #execute in DUT function
                        result=rfc_executeInDUT (sshMethod, credentials, command)
                        if "IMPORTED" in result:
                            print("\nSUCCESS : Feature rule updated successfully")
                        else:
                            print("\nFAILURE : Failed to update feature rule")
                            initializefeaturestatus="FAILURE"
                    else:
                        print("\nFAILURE : Failed to update feature")
                        initializefeaturestatus="FAILURE"
                else:
                    print("Feature rule is not present")
                    print("\nFAILURE : "+feature_name+" "+"failed to retrieve feature rule")
                    initializefeaturestatus="FAILURE"
            else:
                print(feature_name+" : "+"Creating the feature please wait....")
                #Create feature
                command='curl -sX POST '+xconfdomainname+'feature -H "Content-Type: application/json" -H "Accept: application/json" -d \'{"name":"'+feature_name+'","effectiveImmediate":true,"enable":true,"whitelisted":false,"configData":{"tr181.'+rfcparameter+'":"'+expectedvalue+'"},"whitelistProperty":{},"applicationType":"stb","featureInstance":"'+feature_name+'"}\''
                print("Executing Command : %s" %command)
                #execute in DUT function
                result=rfc_executeInDUT (sshMethod, credentials, command)
                result=str(result).split("\n")
                result= str(result[1])
                feature_id=json.loads(result)
                feature_id=feature_id["id"]
                if len(feature_id)!=0:
                    print(feature_name+" : feature created Successfully")
                    #Create feature rule
                    print(feature_name+" : "+"Creating the feature rule please wait....")
                    command='curl -sX POST '+xconfdomainname+'featurerule -H "Content-Type: application/json" -H "Accept: application/json" -d \'{"name":"'+feature_name+'","rule":{"negated":false,"compoundParts":[{"negated":false,"condition":{"freeArg":{"type":"STRING","name":"estbIP"},"operation":"IS","fixedArg":{"bean":{"value":{"java.lang.String":"'+deviceIP+'"}}}},"compoundParts":[]},{"negated":false,"relation":"OR","condition":{"freeArg":{"type":"STRING","name":"estbMacAddress"},"operation":"IS","fixedArg":{"bean":{"value":{"java.lang.String":"'+deviceMAC+'"}}}},"compoundParts":[]}]},"priority":4,"featureIds":["'+feature_id+'"],"applicationType":"stb"}\''
                    print("Executing Command : %s" %command)
                    #execute in DUT function
                    result=rfc_executeInDUT (sshMethod, credentials, command)
                    result=str(result).split("\n")
                    result= str(result[1])
                    feature_rule_id=json.loads(result)
                    feature_rule_id=feature_rule_id["id"]
                    if len(feature_rule_id)!=0:
                        print(feature_name+" : feature rule successfully created")
                    else:
                        print("\nFAILURE : Failed to create feature rule")
                        initializefeaturestatus="FAILURE"
                else:
                    print("\nFAILURE : Failed to create feature")
                    initializefeaturestatus="FAILURE"
        else:
            print("\nFAILURE : Failed to get the device credentials")
            initializefeaturestatus="FAILURE"
    else:
        initializefeaturestatus="FAILURE"
    return initializefeaturestatus

#---------------------------------------------------------------------
# CHECK WHEATHER THE GIVEN FEATURE AND FEATURE RULE GETTING CORRECT OR NOT
#---------------------------------------------------------------------
def rfc_checkconfiguredata(xconfdomainname,rfcparameter,expectedvalue,feature_name):
    checkconfiguredatastatus="SUCCESS"
    deviceMACstatus=rfc_getmacaddress()
    if "FAILURE" not in deviceMACstatus:
        config_status=rfc_obtainCredentials()
        if "FAILURE" not in config_status:
            credentials = deviceIP + ',' + user_name + ',' + password
            command="curl -si '"+xconfdomainname+"featureControl/getSettings?estbMacAddress="+deviceMAC+"&estbIP="+deviceIP+"'"
            print("Executing Command : %s" %command)
            #execute in DUT function
            result=rfc_executeInDUT (sshMethod, credentials, command)
            reaesc = re.compile(r'\x1b[^m]*m')
            result = reaesc.sub('',result)
            if feature_name in result and rfcparameter in result:
                print(result)
                print("\nSUCCESS : Getting RFC settings from the xconf server matches with the configure data")
            else:
                print(result)
                print("\nFAILURE : Getting RFC settings from the xconf server does not match with with configure data")
                checkconfiguredatastatus="FAILURE"
        else:
            print("\nFAILURE : Failed to get the device credentials")
            checkconfiguredatastatus="FAILURE"
    else:
        checkconfiguredatastatus="FAILURE"
    return checkconfiguredatastatus

#---------------------------------------------------------------
# CHECK XCONF SERVER SETTING APPLIED OR NOT IN DUT
#---------------------------------------------------------------
def rfc_check_setornot_configdata(rfcparameter,expectedvalue):
    config_status=rfc_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #check rfc parameter status
        command="tr181 -d "+str(rfcparameter)
        print("Executing Command : %s" %command)
        #execute in DUT function
        result=rfc_executeInDUT (sshMethod, credentials, command)
        result=str(result).split("\n")
        result=str(result[2])
        if expectedvalue in result:
            print(result)
            print("\nSUCCESS : "+rfcparameter+" successfully set to "+expectedvalue)
        else:
            print(result)
            print("\nFAILURE : "+rfcparameter+" failed to set "+expectedvalue)
            result="FAILURE"
    else:
        print("\nFAILURE : Failed to get the device credentials")
        result="FAILURE"
    return result

#---------------------------------------------------------------
# DELETE THE FEATURE
#---------------------------------------------------------------
def rfc_deletefeature(xconfdomainname):
    deletefeaturestatus="SUCCESS"
    config_status=rfc_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        print("\nInitialized deleting the feature")
        command="curl -i -sX DELETE "+xconfdomainname+"feature/"+feature_id
        print("Executing Command : %s" %command)
        #execute in DUT function
        result=rfc_executeInDUT (sshMethod, credentials, command)
        reaesc = re.compile(r'\x1b[^m]*m')
        result = reaesc.sub('',result)
        result = result.strip()
        if "204" in result:
            print(result)
            print("\nSUCCESS : Deleted the feature successfully")
        else:
            print(result)
            print("\nFAILURE : Failed to delete the feature")
            deletefeaturestatus="FAILURE"
    else:
        print("\nFAILURE : Failed to get the device credentials")
        deletefeaturestatus="FAILURE"
    return  deletefeaturestatus

#---------------------------------------------------------------
# DELETE THE FEATURE RULE
#---------------------------------------------------------------
def rfc_deletefeaturerule(xconfdomainname):
    deletefeaturerulestatus="SUCCESS"
    config_status=rfc_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        print("\nInitialized deleting the feature rule")
        command="curl -i -sX DELETE "+xconfdomainname+"featurerule/"+feature_rule_id
        print("Executing Command : %s" %command)
        #execute in DUT function
        result=rfc_executeInDUT (sshMethod, credentials, command)
        reaesc = re.compile(r'\x1b[^m]*m')
        result = reaesc.sub('',result)
        result = result.strip()
        if "204" in result:
            print(result)
            print("\nSUCCESS : Deleted the feature rule successfully")
        else:
            print(result)
            print("\nFAILURE : Failed to delete the feature rule")
            deletefeaturerulestatus="FAILURE"
    else:
        print("\nFAILURE : Failed to get the device credentials")
        deletefeaturerulestatus="FAILURE"
    return deletefeaturerulestatus

#---------------------------------------------------------------
# CHECK for THE PRESENCE OF the PARTNERID3 FILE
#---------------------------------------------------------------
def rfc_datfilechecker():
    datfilecheckerstatus="SUCCESS"
    config_status=rfc_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #check whether partnerid3 dat file is present or not
        command="[ -f /opt/www/authService/partnerId3.dat ] && echo 1 || echo 0"
        print("Executing Command : %s" %command)
        #execute in DUT function
        result=rfc_executeInDUT (sshMethod, credentials, command)
        result = str(result).split("\n")
        result = int(result[1])
        if result == 1:
            print("\nSUCCESS : partnerId3.dat file is available")
            #check if the string "community" exists in /opt/www/authService/partnerId3.dat
            command="grep -q 'community' /opt/www/authService/partnerId3.dat && echo 1 || echo 0"
            print("Executing Command : %s" %command)
            #execute in DUT function
            result=rfc_executeInDUT (sshMethod, credentials, command)
            result = str(result).split("\n")
            result = int(result[1])
            if result == 1:
                print("\nSUCCESS : String 'community' exists in /opt/www/authService/partnerId3.dat")
            else:
                print(result)
                print("\nFAILURE : String 'community' does not exist in /opt/www/authService/partnerId3.dat")
                datfilecheckerstatus="FAILURE"
        else:
            print(result)
            print("\nFAILURE :  partnerId3.dat file is not available")
            datfilecheckerstatus="FAILURE"
    else:
        print("\nFAILURE : Failed to get the device credentials")
        datfilecheckerstatus="FAILURE"
    return datfilecheckerstatus

#---------------------------------------------------------------
# CHECK for THE PRESENCE OF the PARTNERS_DEFAULTS JSON FILE
#---------------------------------------------------------------
def rfc_partnersdefaultschecker():
    partnersdefaultscheckerstatus="SUCCESS"
    config_status=rfc_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #check whether partners_defaults.json file is present or not
        command="[ -f /etc/partners_defaults.json ] && echo 1 || echo 0"
        print("Executing Command : %s" %command)
        #execute in DUT function
        result=rfc_executeInDUT (sshMethod, credentials, command)
        result = str(result).split("\n")
        result = int(result[1])
        if result == 1:
            print("\nSUCCESS : partners_defaults.json file is available")
            #check if the xconf domain URL exists in /etc/partners_defaults.json
            command="sed -n '/community/,/}/p' /etc/partners_defaults.json | grep -q '"+'"Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Bootstrap.XconfUrl" *: *"https://xconf.rdkcentral.com:19092"'+"' /etc/partners_defaults.json && echo 1 || echo 0"
            print("Executing Command : %s" %command)
            #execute in DUT function
            result=rfc_executeInDUT (sshMethod, credentials, command)
            result = str(result).split("\n")
            result = int(result[1])
            if result == 1:
                print("\nSUCCESS : Xconf domain URL exists in /etc/partners_defaults.json")
            else:
                print(result)
                print("\nFAILURE : Xconf domain URL does not exist in /etc/partners_defaults.json")
                partnersdefaultscheckerstatus="FAILURE"
        else:
            print(result)
            print("\nFAILURE : partners_defaults.json file is not available")
            partnersdefaultscheckerstatus="FAILURE"
    else:
        print("\nFAILURE : Failed to get the device credentials")
        partnersdefaultscheckerstatus="FAILURE"
    return partnersdefaultscheckerstatus

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
def rfc_getValue(method):
    data = '"method": "'+method+'"'
    result = execute_step(data)
    return result

#------------------------------------------------------------------
# SET VALUE FOR A METHOD
#------------------------------------------------------------------
def rfc_setValue(method,value):
    data = '"method": "'+method+'","params": '+value
    result = execute_step(data)
    return result

#-----------------------------------------------------------------
# GET PLUGIN STATUS
#-----------------------------------------------------------------
def rfc_getPluginStatus(plugin):
    data = '"method": "Controller.1.status@'+plugin+'"'
    result = execute_step(data)
    if result != None:
        for x in result:
            PluginStatus=x["state"]
        return PluginStatus
    else:
        return result

#------------------------------------------------------------------
# ENABLE MAINTENANCEMANAGER PLUGIN
#------------------------------------------------------------------
def rfc_enable_maintenance_manager(method,params):
    enable_maintenance_manager_status="SUCCESS"
    #check the plugin status
    status = rfc_getPluginStatus(method)
    #If the plugin status is deactivated, it needs to be activated
    if status == "deactivated":
        print("\nPlugin is currently deactivated and needs to be activated")
        print("[INFO] Activating "+method+" plugin")
        time.sleep(3)
        status = rfc_setValue("Controller.1.activate",params)
        time.sleep(3)
        status = rfc_getPluginStatus(method)
        #check the plugin status
        if status == "activated":
            print("SUCCESS : "+method+" plugin in activated state")
        else:
            print("FAILURE : Unable to activate "+method+"\n")
            enable_maintenance_manager_status="FAILURE"
    elif status == "activated":
        print("SUCCESS : "+method+" plugin in activated state")
    else:
        print("FAILURE : Plugin is missing or in an undefined state\n")
        enable_maintenance_manager_status="FAILURE"
    return enable_maintenance_manager_status

#------------------------------------------------------------------
# DISABLE AND ENABLE MAINTENANCEMANAGER PLUGIN
#------------------------------------------------------------------
def rfc_disable_enable_maintenance_manager(method,params):
    disable_enable_maintenance_manager_status="SUCCESS"
    #check the plugin status
    status = rfc_getPluginStatus(method)
    #If the plugin status is activated, it needs to be deactivated and then reactivated
    if status == "activated":
        #Deactivate the plugin
        print("\nPlugin is currently activated and needs to be deactivated and then activated")
        print("[INFO] Deactivating "+method+" plugin")
        time.sleep(3)
        status = rfc_setValue("Controller.1.deactivate",params)
        time.sleep(3)
        status = rfc_getPluginStatus(method)
        #check the plugin status
        if status == "deactivated":
            print("SUCCESS : "+method+" plugin in deactivated state\n")
            #Activate the plugin
            print("\n[INFO] Activating "+method+" plugin")
            time.sleep(3)
            status = rfc_setValue("Controller.1.activate",params)
            time.sleep(3)
            status = rfc_getPluginStatus(method)
            #check the plugin status
            if status == "activated":
                print("SUCCESS : "+method+" plugin in activated state\n")
            else:
                print("FAILURE : Unable to activate "+method+"\n")
                disable_enable_maintenance_manager_status="FAILURE"
        else:
            print("FAILURE : Unable to deactivate "+method+"\n")
            disable_enable_maintenance_manager_status="FAILURE"
    else:
        print("FAILURE : Plugin is missing or in an undefined state\n")
        disable_enable_maintenance_manager_status="FAILURE"
    return disable_enable_maintenance_manager_status
