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
import ConfigParser
from time import sleep
import pexpect

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
        print output
        #print "[ERROR]: No Device config file found : %s or %s" %(deviceNameConfigFile,deviceTypeConfigFile)
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

#---------------------------------------------------------------
# GET THE REQUIRED CONFIGURATIONS TO SSH INTO THE DUT
# Description  : To get the required configurations to SSH into the DUT
# Return Value : Returns 'SUCCESS' on successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------
def rfc_obtainCredentials():
    config_status = "SUCCESS"
    result = "SUCCESS"
    print "[INFO] Retrieving Configuration values from config file......."
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
            print "SUCCESS: Successfully retrieved %s configuration from device config file" %(configKey)
        else:
            print "FAILURE: Failed to retrieve %s configuration from device config file" %(configKey)
            if configValues[configKey] == "":
                print "\n [INFO] Please configure the %s key in the device config file" %(configKey)
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
            print "FAILURE: Currently only supports directSSH ssh method"
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
        print "Secure ssh to CPE"
        pass
    try:
        output = ssh_and_execute (sshMethod, host_name, user_name, password, command)
    except Exception as e:
        print "Exception occured during ssh session"
        print e
    return output

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
        print "Executing Command : %s" %command
        global deviceMAC
        #execute in DUT function
        deviceMAC=rfc_executeInDUT (sshMethod, credentials, command)
        deviceMAC=deviceMAC.split("\n")
        deviceMAC=deviceMAC[1]
        deviceMAC=deviceMAC.strip()
        if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$",str(deviceMAC).lower()):
            print "\nSUCCESS : Successfully get the MAC address"
        else:
            print "\nFAILURE : Failed to get the MAC address"
            getmacaddressstatus="FAILURE"
    else:
        print "\nFAILURE : Failed to get the device credentials"
        getmacaddressstatus="FAILURE"
    return getmacaddressstatus

#-----------------------------------------------------------------
# UPDATE THE RFC FILE BY XCONF URL
#-----------------------------------------------------------------
def rfc_updateserverurl(RFC_XCONF_URL):
    updatefilestatus="SUCCESS"
    config_status=rfc_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #check whether the rfc file updated or not
        command="grep -q "+RFC_XCONF_URL+" /etc/rfc.properties  && echo 1 || echo 0"
        print "Executing Command : %s" %command
        #execute in DUT function
        result=rfc_executeInDUT (sshMethod, credentials, command)
        result = str(result).split("\n")
        print result
        if int(result[1]) == 1:
            print "\nAlready RFC file have updated xconf url"
        else:
            print "\nRFC file not updated with xconfurl..Updating Xconfurl with RFC file Please wait....."
            modify_url=RFC_XCONF_URL.replace("/","\\/")
            command= "sed -i 's/^RFC_CONFIG_SERVER_URL=.*/RFC_CONFIG_SERVER_URL="+modify_url+"/' /etc/rfc.properties ; grep -q "+RFC_XCONF_URL+" /etc/rfc.properties && echo 1 || echo 0"
            print "Executing Command : %s" %command
            #execute in DUT function
            result=rfc_executeInDUT (sshMethod, credentials, command)
            result = str(result).split("\n")
            print result
            if int(result[1]) == 1:
                print "\nSUCCESS : Successfully updated xconfurl in RFC file"
            else:
                print "\nFAILURE: Failed to update the xconfurl in RFC file"
                updatefilestatus="FAILURE"
    else:
        print "\nFAILURE : Failed to get the device credentials"
        updatefilestatus="FAILURE"
    return updatefilestatus

#-----------------------------------------------------------------
# CHECK THE PARODUS STATUS
#-----------------------------------------------------------------
def rfc_parodusstatuscheck():
    parodusstatus="SUCCESS"
    config_status=rfc_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #check parodus status
        command="systemctl status parodus | grep running"
        print "Executing Command : %s" %command
        #execute in DUT function
        result=rfc_executeInDUT (sshMethod, credentials, command)
        result=result.split("\n")
        print result
        result=str(result[1])
        if "active (running)" in result:
            print result
            print "\nSUCCESS : Successfully get the parodus status"
        else:
            print result
            print "\nFAILURE : Parodus Process not running"
            parodusstatus="FAILURE"
    else:
        print "\nFAILURE : Failed to get the device credentials"
        parodusstatus="FAILURE"
    return parodusstatus

#-----------------------------------------------------------------
# CHECK RFC PARAMETER STATUS
#-----------------------------------------------------------------
def rfc_datamodelcheck(rfcparameter):
    config_status=rfc_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #check rfc parameter status
        command="tr181 -d "+str(rfcparameter)
        print "Executing Command : %s" %command
        #execute in DUT function
        result=rfc_executeInDUT (sshMethod, credentials, command)
        result=str(result).split("\n")[2]
        result=result.strip()
        print result
    else:
        print "\nFAILURE : Failed to get the device credentials"
        result="FAILURE"
    return result

#---------------------------------------------------------------
# INITIALIZE FEATURE AND FEATURE RULE CREATION OR UPDATE
#---------------------------------------------------------------
def rfc_initializefeatures(feature_name,xconfdomainname,rfcparameter,expectedvalue):
    initializefeaturestatus="SUCCESS"
    global feature_id
    deviceMACstatus=rfc_getmacaddress()
    if "FAILURE" not in deviceMACstatus:
        config_status=rfc_obtainCredentials()
        if "FAILURE" not in config_status:
            credentials = deviceIP + ',' + user_name + ',' + password
            #check feature already present or not
            command='curl -sX  GET '+"'"+xconfdomainname+'feature/filtered?APPLICATION_TYPE=stb&NAME='+feature_name+"'"+' -H "Content-Type: application/json" -H "Accept: application/json" | cut -d "," -f 1 | cut -d ":" -f 2'
            print "Executing Command : %s" %command
            #execute in DUT function
            result=rfc_executeInDUT (sshMethod, credentials, command)
            result=str(result).split("\n")
            result=str(result[1])
            if "[]" not in result:
                 feature_id=result.replace('"','').strip()
                 print "SUCCESS : "+feature_name+" "+"feature retrieved successfully"
                 #check feature rule already present or not
                 command='curl -sX  GET '+"'"+xconfdomainname+'featurerule/filtered?APPLICATION_TYPE=stb&NAME='+feature_name+"'"+' -H "Content-Type: application/json" -H "Accept: application/json" | cut -d "," -f 1 | cut -d ":" -f 2'
                 print "Executing Command : %s" %command
                 #execute in DUT function
                 result=rfc_executeInDUT (sshMethod, credentials, command)
                 result=str(result).split("\n")
                 result=str(result[1])
                 feature_rule_id=result.replace('"','').strip()
                 if result:
                     print "SUCCESS : "+feature_name+" "+"feature rule retrieved successfully"
                     #Update feature
                     command='curl -sX POST '+xconfdomainname+'feature/importAll -H "Content-Type: application/json" -H "Accept: application/json" -d \'[{"id":"'+feature_id+'","name":"'+feature_name+'","effectiveImmediate":true,"enable":true,"whitelisted":false,"configData":{"tr181.'+rfcparameter+'":"'+expectedvalue+'"},"whitelistProperty":{},"applicationType":"stb","featureInstance":"'+feature_name+'"}]\''
                     print "Executing Command : %s" %command
                     #execute in DUT function
                     result=rfc_executeInDUT (sshMethod, credentials, command)
                     if "IMPORTED" in result:
                         print "Successfully updated feature"
                         feature_rule_id=feature_rule_id.strip()
                         #Update feature rule
                         command='curl -sX POST '+xconfdomainname+'featurerule/importAll -H "Content-Type: application/json" -H "Accept: application/json" -d \'[{"id":"'+feature_rule_id+'","name":"'+feature_name+'","rule":{"negated":false,"compoundParts":[{"negated":false,"condition":{"freeArg":{"type":"STRING","name":"estbIP"},"operation":"IS","fixedArg":{"bean":{"value":{"java.lang.String":"'+deviceIP+'"}}}},"compoundParts":[]},{"negated":false,"relation":"OR","condition":{"freeArg":{"type":"STRING","name":"estbMacAddress"},"operation":"IS","fixedArg":{"bean":{"value":{"java.lang.String":"'+deviceMAC+'"}}}},"compoundParts":[]}]},"priority":4,"featureIds":["'+feature_id+'"],"applicationType":"stb"}]\''
                         print "Executing Command : %s" %command
                         #execute in DUT function
                         result=rfc_executeInDUT (sshMethod, credentials, command)
                         print result
                         if "IMPORTED" in result:
                             print "Successfully updated featurerule"
                         else:
                             print "Failed to update feature rule"
                             initializefeaturestatus="FAILURE"
                     else:
                         print "Failed to update feature"
                         initializefeaturestatus="FAILURE"
                 else:
                        print "Failed to retreive specific feature rule"
                        initializefeaturestatus="FAILURE"
            else:
                print feature_name+" : "+"feature already not present.Creating this feature please wait...."
                #Create feature
                command='curl -sX POST '+xconfdomainname+'feature -H "Content-Type: application/json" -H "Accept: application/json" -d \'{"name":"'+feature_name+'","effectiveImmediate":true,"enable":true,"whitelisted":false,"configData":{"tr181.'+rfcparameter+'":"'+expectedvalue+'"},"whitelistProperty":{},"applicationType":"stb","featureInstance":"'+feature_name+'"}\''
                print "Executing Command : %s" %command
                #execute in DUT function
                result=rfc_executeInDUT (sshMethod, credentials, command)
                if "id" in result:
                    result=str(result).split("\n")
                    result= str(result[1])
                    feature_id=json.loads(result)
                    feature_id=feature_id["id"]
                    print feature_name+" : feature created Successfully"
                    #Create feature rule
                    command='curl -sX POST '+xconfdomainname+'featurerule -H "Content-Type: application/json" -H "Accept: application/json" -d \'{"name":"'+feature_name+'","rule":{"negated":false,"compoundParts":[{"negated":false,"condition":{"freeArg":{"type":"STRING","name":"estbIP"},"operation":"IS","fixedArg":{"bean":{"value":{"java.lang.String":"'+deviceIP+'"}}}},"compoundParts":[]},{"negated":false,"relation":"OR","condition":{"freeArg":{"type":"STRING","name":"estbMacAddress"},"operation":"IS","fixedArg":{"bean":{"value":{"java.lang.String":"'+deviceMAC+'"}}}},"compoundParts":[]}]},"priority":4,"featureIds":["'+feature_id+'"],"applicationType":"stb"}\''
                    print "Executing Command : %s" %command
                    #execute in DUT function
                    result=rfc_executeInDUT (sshMethod, credentials, command)
                    if "id" in result:
                        print "Feature rule successfully created"
                    else:
                        print "Failed to create feature rule"
                        initializefeaturestatus="FAILURE"
                else:
                    print "Failed to create feature"
                    initializefeaturestatus="FAILURE"
        else:
            print "\nFAILURE : Failed to get the device credentials"
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
            print "Executing Command : %s" %command
            #execute in DUT function
            result=rfc_executeInDUT (sshMethod, credentials, command)
            reaesc = re.compile(r'\x1b[^m]*m')
            result = reaesc.sub('',result)
            if feature_name in result and rfcparameter in result and expectedvalue in result:
                print result
                print "\nSUccess : Retrieved RFC details match with configure data"
            else:
                print result
                print "\nFAILURE : Retrieved RFC details not match with configure data"
                checkconfiguredatastatus="FAILURE"
        else:
            print "\nFAILURE : Failed to get the device credentials"
            checkconfiguredatastatus="FAILURE"
    else:
        checkconfiguredatastatus="FAILURE"
    return checkconfiguredatastatus

#---------------------------------------------------------------
# RESTART RFC CONFIG SERVICE
#---------------------------------------------------------------
def rfc_restartservice():
    restartrfcstatus="SUCCESS"
    config_status=rfc_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #restart rfc services
        command='systemctl restart rfc-config ; sleep 5s ; systemctl status rfc-config | grep active  | cut -d ";" -f 2 | cut -d " " -f 2'
        print "Executing Command : %s" %command
        #execute in DUT function
        result=rfc_executeInDUT (sshMethod, credentials, command)
        result=result.split("\n")
	result=result[1]
	result=result.replace("s","").strip()
        if int(result) <= 7:
            print result
            print "\nSUCCESS : Successfully restarted RFC service"
        else:
            print result
            print "\nFAILURE : Failed to restart RFC service"
            restartrfcstatus="FAILURE"
    else:
        print "\nFAILURE : Failed to get the device credentials"
        restartrfcstatus="FAILURE"
    return restartrfcstatus

#---------------------------------------------------------------
# CHECK XCONF SERVER SETTING APPLIED OR NOT IN DUT
#---------------------------------------------------------------
def rfc_check_setornot_configdata(rfcparameter,expectedvalue):
    config_status=rfc_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        #check rfc parameter status
        command="tr181 -d "+str(rfcparameter)
        print "Executing Command : %s" %command
        #execute in DUT function
        result=rfc_executeInDUT (sshMethod, credentials, command)
        result=str(result).split("\n")
	result=str(result[2])
        if expectedvalue in result:
            print result
            print "\nSUCCESS : "+rfcparameter+" successfully set to "+expectedvalue
        else:
            print result
            print "\nFAILURE : "+rfcparameter+" failed to set "+expectedvalue
            result="FAILURE"
    else:
        print "\nFAILURE : Failed to get the device credentials"
        result="FAILURE"
    return result

#----------------------------------------------------------------------------------------------
# IF XCONF SERVER SETTING APPLIED SUCCESSFULLY THEN ROLLBACK THE RFC PARAMETER TO ACTUALVALUE
#----------------------------------------------------------------------------------------------
def rfc_rollbackdatamodelvalue(rfcparameter,actualvalue,xconfdomainname,feature_name):
    revertrfcstatus="SUCCESS"
    config_status=rfc_obtainCredentials()
    if "FAILURE" not in config_status:
        if len(actualvalue) == 0:
            actualvalue="false"
        credentials = deviceIP + ',' + user_name + ',' + password
        #rollback the rfc parameter
        command="tr181 -s -v "+actualvalue+" "+rfcparameter+" "+"&& echo 1 || echo 0"
        print "Executing Command : %s" %command
        #execute in DUT function
        result=rfc_executeInDUT (sshMethod, credentials, command)
        result = str(result).split("\n")
        if int(result[1]) == 1:
            print "SUCCESS : Set command for "+rfcparameter+" executed successfully"
            command="tr181 -d "+str(rfcparameter)
            print "Executing Command : %s" %command
            #execute in DUT function
            result=rfc_executeInDUT (sshMethod, credentials, command)
            result=str(result).split("\n")
            result=str(result[2])
            if actualvalue in result:
                print result
                print "\nSUCCESS : Rollback the RFC parameter successfully"

                print "\nSetting the dummy RFC parameter value"
                #set the dummy RFC parameter value
                command='curl -sX POST '+xconfdomainname+'feature/importAll -H "Content-Type: application/json" -H "Accept: application/json" -d \'[{"id":"'+feature_id+'","name":"'+feature_name+'","effectiveImmediate":true,"enable":true,"whitelisted":false,"configData":{"Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature":"null"},"whitelistProperty":{},"applicationType":"stb","featureInstance":"'+feature_name+'"}]\''
                print "Executing Command : %s" %command
                #execute in DUT function
                result=rfc_executeInDUT (sshMethod, credentials, command)
                if "IMPORTED" in result:
                    print "\nSUCCESS : Successfully updated dummy RFC parameter Value"
                else:
                    print "\nFAILURE : Updating dummy RFC parameter value failed"
                    revertrfcstatus="FAILURE"
            else:
                print result
                print "\nFAILURE : Rollback the RFC parameter failed"
                revertrfcstatus="FAILURE"
        else:
            print "\nFAILURE : Set command for "+rfcparameter+" execution  failed"
            revertrfcstatus="FAILURE"
    else:
        print "\nFAILURE : Failed to get the device credentials"
        revertrfcstatus="FAILURE"
    return revertrfcstatus
