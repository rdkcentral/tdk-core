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
import PerformanceTestVariables
from rdkv_performancelib import *

excluded_process_list = PerformanceTestVariables.excluded_process_list
graphical_plugins_list = PerformanceTestVariables.graphical_plugins_list
default_state = "SUCCESS"
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
def containerization_executeInDUT (sshMethod, credentials, command):
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
#-------------------------------------------------------------------
#GET THE SSH DETAILS FROM CONFIGURATION FILE
#-------------------------------------------------------------------
def containerization_getSSHParams(realpath,deviceIP):
    ssh_dict = {}
    print "\n getting ssh params from conf file"
    conf_file,result = getConfigFileName(realpath)
    if result == "SUCCESS":
        result,ssh_method = getDeviceConfigKeyValue(conf_file,"SSH_METHOD")
        result,user_name = getDeviceConfigKeyValue(conf_file,"SSH_USERNAME")
        result,password = getDeviceConfigKeyValue(conf_file,"SSH_PASSWORD")
        if any(value == "" for value in (ssh_method,user_name,password)):
            print "please configure values before test"
            ssh_dict = {}
        else:
            ssh_dict["ssh_method"] = ssh_method
            if password.upper() == "NONE":
                password = ""
            ssh_dict["credentials"] = deviceIP +","+ user_name +","+ password
    else:
        print "Failed to find the device specific config file"
    ssh_dict = json.dumps(ssh_dict)
    return ssh_dict

#-------------------------------------------------------------------
#VALIDATE PROC ENTRY TO FIND WHETHER PLAYBACK IS HAPPENING
#-------------------------------------------------------------------
def containerization_validateProcEntry(sshmethod,credentials,video_validation_script):
    result = "SUCCESS"
    video_validation_script = video_validation_script.split('.py')[0]
    try:
        lib = importlib.import_module(video_validation_script)
        method = "check_video_status"
        method_to_call = getattr(lib, method)
        result = method_to_call(sshmethod,credentials)
    except Exception as e:
        print "\n ERROR OCCURRED WHILE IMPORTING THE VIDEO VALIDATION SCRIPT FILE, PLEASE CHECK THE CONFIGURATION \n"
        result = "FAILURE"
    finally:
        return result

#---------------------------------------------------------------
# EXECUTE A COMMAND IN TM AND GET THE OUTPUT
# Description  : Execute a command in the Test Manager and get the output back
# Parameters   : command - a string to specify the
# Return Value : console output of the 'command' in case of successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------
def containerization_executeInTM (command):
    outdata = ""
    try:
        if "" == command:
            outdata = "FAILURE"
            print "[ERROR]: Command to be executed cannot be empty"
        else:
            print "[INFO] Going to execute %s..." %(command)
            outdata = subprocess.check_output (command, shell=True)
    except:
        outdata = "FAILURE"
        print "#TDK_@error-ERROR : Unable to execute %s successfully" %(command)
    return outdata
#----------------------------------------------------------------------
# GET DEVICE CONFIGURATION FROM THE DEVICE CONFIG FILE
# Description  : Read the value of device configuration from the <device>.config file
# Parameters   : basePath - a string to specify the path of the TM
#                configKey - a string to specify the configuration whose value needs to be retrieved from the <device>.config file
# Return Value : value of device configuration or error log in case of failure
#----------------------------------------------------------------------
def containerization_getDeviceConfig (basePath, configKey):
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
    return output;
#------------------------------------------------------------------
# REBOOT THE DEVICE
#------------------------------------------------------------------
def containerization_rebootDevice(waitTime):
    status = containerization_getPluginStatus("org.rdk.System")
    timeout = time.time() + 30*5
    deviceStatus = "DOWN"
    if status != "activated":
        print "[INFO] Activating System plugin for rebooting the device"
        params = '{"callsign":"org.rdk.System"}'
        status = containerization_setValue("Controller.1.activate",params)
        status = containerization_getPluginStatus("org.rdk.System")
    if status == "activated":
        print "[INFO] System plugin is activated"
        data = '"method": "org.rdk.System.1.reboot","params": {"rebootReason": "TDK_TESTING"}'
        result = execute_step(data)
        if result != "EXCEPTION OCCURRED":
            print "\n[INFO] Waiting for the device to come up..."
            time.sleep(waitTime)
            while True:
                status = containerization_getTestDeviceStatus()
                if status == "FREE":
                    deviceStatus = "UP"
                    break;
                elif time.time() > timeout:
                    deviceStatus = "DOWN"
                    print "[INFO] Device is not coming up even after 2.5 mins"
                    break;
                time.sleep(5)
            if deviceStatus == "UP":
                print "[INFO] Device is UP"
                return "SUCCESS"
            else:
                return "FAILURE"
        else:
            return result
    else:
        print "FAILURE: Unable to activate System plugin"
        return "EXCEPTION OCCURED"

#------------------------------------------------------------------
# Check Device Status
#------------------------------------------------------------------
def containerization_getTestDeviceStatus():
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
#---------------------------------------------------------------
# EXECUTE CURL REQUESTS
# Description  : Execute curl request in DUT
# Parameters   : Data - a string which contains actual curl request
# Return Value : contains response of the curl request sent
#---------------------------------------------------------------
def execute_step(Data):
    data = '{"jsonrpc": "2.0", "id": 1234567890, '+Data+'}'
    headers = {'content-type': 'text/plain;',}
    url = 'http://'+str(deviceIP)+':'+str(devicePort)+'/jsonrpc'
    try:
        response = requests.post(url, headers=headers, data=data, timeout=20)
        json_response = json.loads(response.content)
        print "\n---------------------------------------------------------------------------------------------------"
        print "Json command : ", data
        print "\n Response : ", json_response, "\n"
        print "----------------------------------------------------------------------------------------------------\n"
        result = json_response.get("result")
        if result != None and "'success': False" in str(result):
            result = "EXCEPTION OCCURRED"
        return result;
    except requests.exceptions.RequestException as e:
        print "ERROR!! \nEXCEPTION OCCURRED WHILE EXECUTING CURL COMMANDS!!"
        print "Error message received :\n",e;
        return "EXCEPTION OCCURRED"
#-------------------------------------------------------------------
# GET THE VALUE OF A METHOD
#-------------------------------------------------------------------
def containerization_getValue(method):
    data = '"method": "'+method+'"'
    result = execute_step(data)
    return result
#------------------------------------------------------------------
# SET VALUE FOR A METHOD
#------------------------------------------------------------------
def containerization_setValue(method,value):
    data = '"method": "'+method+'","params": '+value
    result = execute_step(data)
    return result
#-----------------------------------------------------------------
# GET PLUGIN STATUS
#-----------------------------------------------------------------
def containerization_getPluginStatus(plugin):
    data = '"method": "Controller.1.status@'+plugin+'"'
    result = execute_step(data)
    if result != None and result != "EXCEPTION OCCURRED":
        for x in result:
            PluginStatus=x["state"]
        return PluginStatus
    else:
        return result;

#------------------------------------------------------------------
#SET PLUGIN STATUS
#------------------------------------------------------------------
def containerization_setPluginStatus(plugin,status,uri=''):
    data = ''
    if plugin in graphical_plugins_list:
        rdkshell_activated = check_status_of_rdkshell()
        if rdkshell_activated:
            if status in "activate":
                data = '"method":"org.rdk.RDKShell.1.launch", "params":{"callsign": "'+plugin+'", "type":"", "uri":"'+uri+'"}'
            else:
                data = '"method":"org.rdk.RDKShell.1.destroy", "params":{"callsign": "'+plugin+'"}'
    else:
        data = '"method": "Controller.1.'+status+'", "params": {"callsign": "'+plugin+'"}'
    if data != '':
        result = execute_step(data)
    else:
        result = "EXCEPTION OCCURRED"
    return result

#-------------------------------------------------------------------
#CHECK THE STATUS OF RDKSHELL PLUGIN AND ACTIVATE IF NEEDED
#-------------------------------------------------------------------
def check_status_of_rdkshell():
    activated = False
    rdkshell_status = containerization_getPluginStatus("org.rdk.RDKShell")
    if "activated" == rdkshell_status:
        activated = True
    elif "deactivated" == rdkshell_status:
        set_status = containerization_setPluginStatus("org.rdk.RDKShell","activate")
        time.sleep(2)
        rdkshell_status = containerization_getPluginStatus("org.rdk.RDKShell")
        if "activated" in rdkshell_status:
            activated = True
        else:
            print "\n Unable to activate RDKShell plugin"
    else:
        print "\n RDKShell status in DUT:",rdkshell_status
    return activated

#---------------------------------------------------------------
# GET THE REQUIRED CONFIGURATIONS TO SSH INTO THE DUT
# Description  : To get the required configurations to SSH into the DUT
# Return Value : Returns 'SUCCESS' on successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------
def containerization_obtainCredentials():
    config_status = "SUCCESS"
    result = "SUCCESS"
    print "[INFO] Retrieving Configuration values from config file......."
    configKeyList = ["SSH_METHOD","SSH_USERNAME", "SSH_PASSWORD"]
    configValues = {}
    global password
    global user_name
    global ssh_method
    #Get each configuration from device config file
    for configKey in configKeyList:
        containerization_getDeviceConfig(libObj.realpath,configKey)
        configValues[configKey] = containerization_getDeviceConfig(libObj.realpath,configKey)
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
            ssh_method = configValues["SSH_METHOD"]
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
#---------------------------------------------------------------
# COPY THE DOBBY SECURITY TOOL IN THE DUT
# Description  : copy the dobby security tool in the DUT
# Parameters   : 1.fileName - Name of the dobby security tool file
#                2.hostname - ip address of the DUT
#                3.username - username of the DUT
#                4.destPath - destination path to copy the dobby security tool
# Return Value : console output of the 'command' in case of successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------
def containerization_copyToolToDUT(fileName,hostname,username,password,destPath):
    try:
        outdata = "SUCCESS"
        command_to_scp = 'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ' + fileName + ' ' + username + '@' + hostname + ':' + destPath
        child = pexpect.spawn(command_to_scp)
        r=child.expect (['password:',pexpect.EOF])
        if r==0:
           child.sendline ('password')
           child.expect(pexpect.EOF)
        child.close()
    except Exception as e:
        print "[ERROR] basePath\nSCP failed"
        print e
        outdata = "FAILURE"
    return outdata
#---------------------------------------------------------------
# CLONE THE DOBBY SECURITY TOOL IN THE TM AND COPY THE TAR FILE TO DUT
# Description  : clone the dobby security tool in the TM and copy the security tool in the DUT
# Parameters   : basePath - basepath, To clone the dobby security tool
# Return Value : Returns 'SUCCESS' on successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------
def containerization_cloneDobby(basePath):
    clone_dobby_status = "SUCCESS"
    #Obatin credentials for DUT
    config_status = containerization_obtainCredentials()
    if "FAILURE" not in config_status:
        #Check if dobby test tool is downloaded  in TM
        command = '[ -d '+basePath+'/fileStore/dobby-security-tool ] && echo 1 || echo 0'
        output = containerization_executeInTM(command)
        if int(output) == 0 or "FAILURE" in output:
            #gitclone and obtain dobby security directory in fileStore
            command = "cd " + basePath + "/fileStore;git clone https://github.com/rdkcentral/dobby-security-tool.git"
            output = containerization_executeInTM(command)
            sleep(2);
            command = '[ -d '+basePath+'/fileStore/dobby-security-tool ] && echo 1 || echo 0'
            output = containerization_executeInTM(command)
        #if Dobby  is successfully downloaded in fileStore
        if "FAILURE" not in output and int(output) == 1:
            print "SUCCESS: Dobby is installed in TM\n"
            #Create tar ball to run in DUT
            #Command = remove existing result files ; make directory for dobby result files ; tar the whole dobby directory ; check whether tar file is created by ls command
            print "[INFO] Creating tar ball to run in DUT"
            command = "rm -rf " + basePath + "/fileStore/dobby-security-tool/files ; mkdir -p " + basePath + "/fileStore/dobby-security-tool/files; cd " + basePath + "/fileStore/;tar czfP dobby-security-tool/files/dobby-security-tool-remote.tar.gz --exclude=/dobby-security-tool/files/dobby-security-tool-remote.tar.gz dobby-security-tool; ls dobby-security-tool/files"
            result = containerization_executeInTM(command)
            if "FAILURE" not in result and "dobby-security-tool-remote.tar.gz" in result:
                print "SUCCESS: Tar ball was created successfully\n"
                #Copy dobby tool tar ball into DUT
                fileToTransfer = basePath + "/fileStore/dobby-security-tool/files/dobby-security-tool-remote.tar.gz"
                destPath = "/home/root"
                result = containerization_copyToolToDUT(fileToTransfer,deviceIP,user_name,password,destPath)
                if "FAILURE" in result:
                    print "FAILURE: Could not copy the files to the DUT"
                    clone_dobby_status = "FAILURE"
                else:
                    credentials = deviceIP + ',' + user_name + ',' + password
                    command = '[ -f /home/root/dobby-security-tool-remote.tar.gz ] && echo 1 || echo 0'
                    result = containerization_executeInDUT(ssh_method,credentials,command)
            else:
                print "FAILURE: Error while creating the Tar ball"
                clone_dobby_status = "FAILURE"
            if "FAILURE" in result:
                print "FAILURE: Could not copy the tar file to the DUT"
                clone_dobby_status = "FAILURE"
            elif int(str(result).split("\n")[1]) == 1:
                print "SUCCESS: Dobby security tool tar ball has been copied to DUT in as /home/root/dobby-security-tool-remote.tar.gz successfully\n"
                #Untar the dobby tar ball
                #Command = untar dobby tar ball;
                print "\n[INFO] Untaring Dobby security tool in DUT...."
                command = "cd /home/root; tar xzf dobby-security-tool-remote.tar.gz; [ -d /home/root/dobby-security-tool ] && echo 1 || echo 0"
                #SSH and execute command
                result = containerization_executeInDUT(ssh_method,credentials,command)
                if int(str(result).split("\n")[1]) == 1:
                    print "SUCCESS: Dobby test tool moved to DUT"
                else:
                    print "FAILURE: Could not untar the file in the DUT"
                    clone_dobby_status = "FAILURE"
            else:
                print "FAILURE: Could not copy the tar file to the DUT"
                clone_dobby_status = "FAILURE"
        else:
            print "FAILURE: Error Cloning the file in the TM"
            clone_dobby_status = "FAILURE"
    else:
        clone_dobby_status = "FAILURE"
    return clone_dobby_status
#---------------------------------------------------------------
# ENABLE THE REQUIRED DATA MODEL IN THE DUT
# Description  : To enable the required data model in the DUT
# Parameters   : datamodel - Data model list which needs to be enabled
# Return Value : Returns 'SUCCESS' on successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------
def containerization_setPreRequisites(datamodel):
    pre_requisite_status = "SUCCESS"
    rebootFlag = 0
    global default_state
    status = containerization_obtainCredentials()
    if "FAILURE" not in status:
        credentials = deviceIP + ',' + user_name + ',' + password
        for datamodels in datamodel:
            command =  'tr181 -d/ '+str(datamodels)
            print "COMMAND : %s" %(command)
            output = containerization_executeInDUT(ssh_method,credentials,command)
            if "FAILURE" not in output:
                output = str(output).split("\n")[1]
                if "true" in output.lower():
                    print 'SUCCESS: The '+datamodels+' parameter is already enabled'
                elif "false" in output.lower() or "empty" in output.lower():
                    default_state = "FAILURE"
                    command =  'tr181 -d -s -t boolean -v true '+datamodels
                    print "COMMAND : %s" %(command)
                    enableStatus = containerization_executeInDUT(ssh_method,credentials,command)
                    enableStatus = enableStatus.strip()
                    if "set operation success" in enableStatus.lower():
                        rebootFlag = 1
                        print 'SUCCESS: Successfully set the '+datamodels+' parameter'
                    else:
                        print 'FAILURE: Could not able to set the '+datamodels+' parameter'
                        pre_requisite_status = "FAILURE"
                else:
                    print 'FAILURE: Failed to retrieve '+datamodels+' enabled status'
                    pre_requisite_status = "FAILURE"
            else:
                print 'FAILURE: Error while executing the command'
                pre_requisite_status = "FAILURE"


        if "FAILURE" not in pre_requisite_status and rebootFlag == 1:
            print '[INFO] Rebooting the Device................'
            status = containerization_rebootDevice(60)
            if "SUCCESS" in status:
                for datamodels in datamodel:
                    command =  'tr181 -d '+datamodels
                    print "COMMAND : %s" %(command)
                    enableStatus = containerization_executeInDUT(ssh_method,credentials,command)
                    enableStatus = str(enableStatus).split("\n")[1]
                    if "true" in enableStatus.lower():
                        print 'SUCCESS: Successfully enabled the '+datamodels+' parameter'
                    else:
                        print 'FAILURE: '+datamodels+' parameter not enabled'
                        pre_requisite_status = "FAILURE"
            else:
                print 'FAILURE: Error while rebooting the device'
                pre_requisite_status = "FAILURE"

    else:
        print 'FAILURE: Failed to retrieve required configurations'
        pre_requisite_status = "FAILURE"
    return pre_requisite_status

#---------------------------------------------------------------
# LAUNCH THE REQUIRED APPLICATION IN THE DUT USING RDKSHELL PLUGIN
# Description  : To launch the required application
# Parameters   : launch - The callsign and URI of the application
# Return Value : Returns 'SUCCESS' on successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------
def containerization_launchApplication(launch):
     launch_status = "SUCCESS"
     result=[]
     state = containerization_getPluginStatus("org.rdk.RDKShell")
     if state == "deactivated":
         print "[INFO] RDKShell plugin is deactivated"
         print "[INFO] Activating RDKShell plugin"
         params = '{"callsign":"org.rdk.RDKShell"}'
         status = containerization_setValue("Controller.1.activate",params)
         state = containerization_getPluginStatus("org.rdk.RDKShell")
	 start_launch = ""
     if state == "activated":
         print 'SUCCESS: RDKShell Plugin in Activated State'
         launch = launch.split(",")
         for test in launch:
                callsign,uri=test.split("-")
                if str(callsign).lower() == "cobalt":
                    params = '{"callsign": "'+callsign+'","type":"'+callsign+'","visible":true,"configuration": {"url":"'+uri+'"}}'
                else:
                    params = '{"callsign": "'+callsign+'","type":"'+callsign+'","uri":"'+uri+'","visible":true}'
		start_launch = str(datetime.utcnow()).split()[1]
                status = containerization_setValue("org.rdk.RDKShell.1.launch",params)
                if "EXCEPTION OCCURRED" not in status:
                        status = json.dumps(status)
                        status = json.loads(status)
                        if str(status.get("launchType")) == "resume" or str(status.get("launchType")) == "activate" and  str(status.get("success")) == "True":
                                print 'SUCCESS: Successfully Launched the '+callsign+' Application'
                        else:
                                launch_status = "FAILURE"
                                print 'FAILURE: Issue Launching the '+callsign+' Application'
                else:
                        launch_status = "FAILURE"
                        print 'FAILURE: Issue Launching the '+callsign+' Application'
                result.append(launch_status)
         if "FAILURE" not in result:
            launch_status = "SUCCESS"
            return launch_status,start_launch
         else:
            launch_status = "FAILURE"
            return launch_status
     else:
          launch_status = "FAILURE"
          print "FAILURE: RDKShell is not in activated state"
     return launch_status,start_launch
#-------------------------------------------------------------------
# SUSPEND THE REQUIRED APPLICATION IN THE DUT USING RDKSHELL PLUGIN
# Description  : To suspend the required application
# Parameters   : plugin - The plugin which should be suspended
# Return Value : Returns 'SUCCESS' on successful execution or "FAILURE" in case of failure
#-------------------------------------------------------------------
def containerization_suspend_plugin(obj,plugin):
    status = expectedResult = "SUCCESS"
    print "\n Suspending {} \n".format(plugin)
    params = '{"callsign":"'+plugin+'"}'
    tdkTestObj = obj.createTestStep('containerization_setValue')
    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.suspend")
    tdkTestObj.addParameter("value",params)
    start_suspend = str(datetime.utcnow()).split()[1]
    tdkTestObj.executeTestCase(expectedResult);
    result = tdkTestObj.getResult();
    if result == "SUCCESS":
        print "\n Suspended {} plugin \n".format(plugin)
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        print "\n Unable to Suspend {} plugin \n".format(plugin)
        tdkTestObj.setResultStatus("FAILURE")
        status = "FAILURE"
    return status,start_suspend
#---------------------------------------------------------------
# CHECK REQUIRED CONTAINER IS RUNNING IN DUT
# Description  : To check the required container is running in the DUT
# Parameters   : callsign - container name
# Return Value : Returns 'SUCCESS' on successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------
def containerization_checkContainerRunningState(callsign):
    container_status = "SUCCESS"
    result=[]
    status = containerization_obtainCredentials()
    if "FAILURE" not in status:
        credentials = deviceIP + ',' + user_name + ',' + password
        command =  'DobbyTool list'
        print "COMMAND : %s" %(command)
        output = containerization_executeInDUT(ssh_method,credentials,command)
        print (output)
        callsign = callsign.split(",")
        for container in callsign:
            container,uri = container.split("-")
            if "running" in output.lower() and container.lower() in output.lower():
                print 'SUCCESS: '+container+' container is running'
            else:
                print 'FAILURE: '+container+' container is not running'
                container_status = "FAILURE"

    else:
        print 'FAILURE: Failed to retrieve the required configuration'
        container_status = "FAILURE"
    return container_status
#---------------------------------------------------------------
# DISABLE THE REQUIRED DATA MODEL IN THE DUT
# Description  : To disable the required data model in the DUT
# Parameters   : datamodel - Data model list which needs to be disabled
# Return Value : Returns 'SUCCESS' on successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------

def containerization_setPostRequisites(datamodel):
    post_requisite_status = "SUCCESS"
    result=[]
    rebootFlag = 0
    global default_state
    status = containerization_obtainCredentials()
    if "FAILURE" not in status:
        credentials = deviceIP + ',' + user_name + ',' + password
        for datamodels in datamodel:
            command =  'tr181 -d '+str(datamodels)
            print "COMMAND : %s" %(command)
            output = containerization_executeInDUT(ssh_method,credentials,command)
            if "FAILURE" not in output:
                output = str(output).split("\n")[1]
                if "false" in output.lower():
                    print 'SUCCESS: The '+datamodels+' parameter is in disabled state'
                elif "true" in output.lower() or "empty" in output.lower():
                    print 'going to execute logic'
                    if default_state == "SUCCESS":
		       print ' parameter is in enabled state '
                    else:   
                        command =  'tr181 -d -s -t boolean -v false '+datamodels
                        print "COMMAND : %s" %(command)
                        enableStatus = containerization_executeInDUT(ssh_method,credentials,command)
                        enableStatus = enableStatus.strip()
                        print "enableStatus : %s" %(enableStatus)
                        if "set operation success" in enableStatus.lower():
                           rebootFlag = 1
                           print 'SUCCESS: Successfully set the '+datamodels+' parameter'
                        else:
                            print 'FAILURE: Could not able to set the '+datamodels+' parameter'
                            post_requisite_status = "FAILURE"
                else:
                    print 'FAILURE: Failed to retrieve '+datamodels+' enabled status'
                    post_requisite_status = "FAILURE"
            else:
                print 'FAILURE: Error while executing the command'
                post_requisite_status = "FAILURE"

        if "FAILURE" not in post_requisite_status and rebootFlag == 1:
            print '[INFO] Rebooting the Device................'
            status = containerization_rebootDevice(60)
            if "SUCCESS" in status:
                for datamodels in datamodel:
                    command =  'tr181 -d '+datamodels
                    print "COMMAND : %s" %(command)
                    enableStatus = containerization_executeInDUT(ssh_method,credentials,command)
                    enableStatus = str(enableStatus).split("\n")[1]
                    if "false" in enableStatus.lower():
                        print 'SUCCESS: Successfully disabled the '+datamodels+' parameter'
                    else:
                        print 'FAILURE: '+datamodels+' parameter not disabled'
                        post_requisite_status = "FAILURE"
            else:
                print 'FAILURE: Error while rebooting the device'
                post_requisite_status = "FAILURE"

    else:
        print 'FAILURE: Failed to retrieve required configurations'
        post_requisite_status = "FAILURE"
    return post_requisite_status
#---------------------------------------------------------------
# EXECUTE THE DOBBY SECURITY TOOL TESTS
# Description  : To execute the dobby tool tests in the DUT
# Parameters   : containername - Container name to perform tests in the container
#                testCases - Testcase details
# Return Value : Returns 'SUCCESS' on successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------
def containerization_executeDobbyTest(containername,testCases):
    dobby_test_status= "SUCCESS"
    dobbyToolResult={}
    status = containerization_obtainCredentials()
    if "FAILURE" not in status:
        credentials = deviceIP + ',' + user_name + ',' + password
        containername = containername.split(",")
        for container in containername:
            callsign,uri = container.split("-")
            command = 'cd dobby-security-tool/; ./dobby_security.sh -c '+callsign
            print "COMMAND : %s" %(command)
            result = containerization_executeInDUT(ssh_method,credentials,command)
            reaesc = re.compile(r'\x1b[^m]*m')
            result = reaesc.sub('',result)
            dobbyToolResult[callsign] = result

        for test in testCases:
            key,testName,value = test.split("-")
            testName = str(testName).strip()
            print "#==============================================================================#"
            print "TEST CASE NAME   : ",testName
            print "TEST CASE ID   : DOBBY_%s"%(key)
            print "#==============================================================================#"
            key=float(key)
            containerAppResults=[]
            for app in containername:
                app,uri = app.split("-")
                testResult=dobbyToolResult[app]
                testResult=str(testResult).splitlines()
                for line in testResult:
                    if value in line:
                        execStatus = 1
                        testStatus=line.split()[0]
                        testStatus=testStatus.replace('[','').replace(']','')
                        testDesc=line.replace('-','').replace(value,'').replace('   ','').replace(testStatus,'').replace('[','').replace(']','')
                        print "TEST STEP NAME   : ",testName,"_",app
                        count= key + 0.10
                        count=round(count,2)
                        print "TEST STEP ID   :",count
                        key = count
                        if("WARN" in testStatus or "PASS" in testStatus):
                            testStatus="SUCCESS"
                            print "TEST STEP STATUS   :",testStatus
                        else:
                            testStatus="FAILURE"
                            print "TEST STEP STATUS   :",testStatus
                        print "#---------------------------------- Result ------------------------------------#"
                        print line,"\n"
                        containerAppResults.append(testStatus)
                        break

            if "FAILURE" not in containerAppResults:
                finalTestStatus = "SUCCESS"
                print "\n##--------- [TEST EXECUTION STATUS] : %s ----------##\n\n"%(finalTestStatus)
            else:
                finalTestStatus = "FAILURE"
                dobby_test_status = "FAILURE"
                print "\n##--------- [TEST EXECUTION STATUS] : %s ----------##\n\n"%(finalTestStatus)

            if execStatus == 1:
                execStatus = 0
            elif execStatus == 0:
                dobby_test_status = "FAILURE"
    else:
        print 'FAILURE: Failed to retrieve the required configuration'
        dobby_test_status = "FAILURE"
    return dobby_test_status

#---------------------------------------------------------------
# TO CHECK THE DOBBY VERSION
# Description  : To check the dobby and crun versions are up-to date
# Parameters   : testCase - Testcase details
# Return Value : Returns 'SUCCESS' on successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------
def containerization_checkDobbyVersion(testCase):
    dobby_version_status="SUCCESS"
    dobbyVersion=['DOBBY_DAEMON_VERSION','DOBBY_CRUN_VERSION']
    dobbyVersionList=["DobbyDaemon --version","crun --version"]
    versionsvalue=[]
    result=[]
    key,testName = testCase.split("-")
    testName = str(testName).strip()
    print "#==============================================================================#"
    print "TEST CASE NAME   : ",testName
    print "TEST CASE ID   : DOBBY_%s"%(key)
    print "#==============================================================================#"
    config_status = containerization_obtainCredentials()
    if "FAILURE" not in config_status:
        credentials = deviceIP + ',' + user_name + ',' + password
        for version in dobbyVersion:
            containerization_getDeviceConfig(libObj.realpath,version)
            value = containerization_getDeviceConfig(libObj.realpath,version)
            if "FAILURE" not in versionsvalue and versionsvalue != "":
                print "SUCCESS: Successfully retrieved %s configuration from device config file" %(version)
                versionsvalue.append(value)
            else:
                print "FAILURE: Failed to retrieve %s configuration from device config file" %(version)
                dobby_version_status="FAILURE"
                break
        if "FAILURE" != dobby_version_status:
            print "\n[INFO] Configured DobbyDaemon version :%s"%(versionsvalue[0])
            print "[INFO] Configured Crun version :%s"%(versionsvalue[1])
            #To get the current DobbyDaemon version
            command = dobbyVersionList[0]
            print "COMMAND : %s" %(command)
            output = containerization_executeInDUT(ssh_method,credentials,command)
            if not output:
                print "FAILURE: Failed to execute %s" %(command)
                dobby_version_status="FAILURE"
            else:   
                output = output.split('\n',1)[-1]
                currentDobbyVersion = output.split("-")[0].split(":")[1].strip()
                print "[INFO] Current DobbyDaemon version :%s"%(currentDobbyVersion)      

            #To get the current Crun version
            command = dobbyVersionList[1]
            print "COMMAND : %s" %(command)
            output = containerization_executeInDUT(ssh_method,credentials,command)
            if not output:
                print "FAILURE: Failed to execute %s" %(command)
                dobby_version_status="FAILURE"
            else:
                currentCrunVersion = output.split("\n")[1].split("crun version")[1].strip() 
                print "[INFO] Current Crun version :%s"%(currentCrunVersion)
            if "FAILURE" != dobby_version_status and str(versionsvalue[0]).lower() == str(currentDobbyVersion).lower() and str(versionsvalue[1]).lower() == str(currentCrunVersion).lower():
                print "[PASS] 1.2.2 - Dobby Daemon and Crun versions are up to date"
                print "\n##--------- [TEST EXECUTION STATUS] : %s ----------##\n\n"%(dobby_version_status)
            else:
                dobby_version_status="FAILURE"
                print "[FAIL] 1.2.2 - Dobby Daemon and Crun versions are not up to date"
                print "\n##--------- [TEST EXECUTION STATUS] : %s ----------##\n\n"%(dobby_version_status)
        else:
            dobby_version_status="FAILURE"
            print "FAILURE: Failed to retrieve required configuration from device config file"
            print "\n##--------- [TEST EXECUTION STATUS] : %s ----------##\n\n"%(dobby_version_status)
    else:
        dobby_version_status="FAILURE"
        print "FAILURE: Failed to retrieve required configuration from device config file"
    return dobby_version_status

#---------------------------------------------------------------
# TO CHECK THE DEV LOOP PARTITION STATUS
# Description  : To check the dev loop partition status
# Parameters   : testCase - Testcase details
# Return Value : Returns 'SUCCESS' on successful execution or "FAILURE" in case of failure
#---------------------------------------------------------------
def containerization_checkDevLoopPartition(testCase):
    check_partition_status="SUCCESS"
    containerAppResults = []
    partitionStatus = containerization_getDeviceConfig(libObj.realpath,"DOBBY_DEV_LOOP_PARTITION_STATUS")
    if len (partitionStatus) != 0:
        containernames = partitionStatus.split(",")
        key,testName = testCase.split("-")
        testName = str(testName).strip()
        print "#==============================================================================#"
        print "TEST CASE NAME   : ",testName
        print "TEST CASE ID   : DOBBY_%s"%(key)
        print "#==============================================================================#"
        config_status = containerization_obtainCredentials()
        if "FAILURE" not in config_status:
          credentials = deviceIP + ',' + user_name + ',' + password  
          for container in containernames:
            container,partitionStatus = container.split("-")
            #command = 'ps -ef | awk \/'+container+'\/ && \/DobbyInit\/ | grep -v awk | '
            command = 'ps -ef | grep '+container+' | grep DobbyInit | awk \'NR==1 {print $2}\''
            print "COMMAND : %s" %(command)
            DobbyInit_PID = containerization_executeInDUT(ssh_method,credentials,command)
            DobbyInit_PID = DobbyInit_PID.split('\n',1)[-1]
            if DobbyInit_PID:
                command = 'cat /proc/'+DobbyInit_PID+'/mountinfo | grep /dev/loop'
                print "COMMAND : %s" %(command)
                output = containerization_executeInDUT(ssh_method,credentials,command)
                print "TEST STEP NAME   : ",testName,"_",container
                key = float(key)
                count = key + 0.10
                count = round(count,2)
                print "TEST STEP ID   :",count
                if  partitionStatus.lower() == "yes":
                    if '/dev/loop' in output.lower():
                        line = "[PASS] 5.5.1 Partition is present in the device"
                        testStatus="SUCCESS"
                        print "TEST STEP STATUS   :",testStatus
                    else:
                        line = "[FAIL] 5.5.1 partition is not present in the device"
                        check_partition_status="FAILURE"
                        testStatus="FAILURE"
                        print "TEST STEP STATUS   :",testStatus
                elif partitionStatus.lower() == "no":
                    if '/dev/loop' not in output.lower():
                        line = "[PASS] 5.5.1 Partition is not present in the device"
                        testStatus="SUCCESS"
                        print "TEST STEP STATUS   :",testStatus
                    else:
                        line = "[FAIL] 5.5.1 Partition is present in the device but configured as not present"
                        check_partition_status="FAILURE"
                        testStatus="FAILURE"
                        print "TEST STEP STATUS   :",testStatus
                print "#---------------------------------- Result ------------------------------------#"
                print line,"\n"
                containerAppResults.append(testStatus)        
            else:
                print "FAILURE: Failed to retrieve the process ID"
                testStatus = "FAILURE"
                check_partition_status="FAILURE"
                containerAppResults.append(testStatus)

          if "FAILURE" not in containerAppResults:
              finalTestStatus = "SUCCESS"
              print "\n##--------- [TEST EXECUTION STATUS] : %s ----------##\n\n"%(finalTestStatus)
          else:
              finalTestStatus = "FAILURE"
              dobby_test_status = "FAILURE"
              print "\n##--------- [TEST EXECUTION STATUS] : %s ----------##\n\n"%(finalTestStatus)    
        else:
            print "FAILURE: Failed to retrieve the process ID"
            check_partition_status="FAILURE"
    else:
        "FAILURE : %s key should not be empty"%(partitionStatus)   
        check_partition_status="FAILURE"
    return check_partition_status            


#------------------------------------------------------------------
# Calculate Resource Usage
#------------------------------------------------------------------
def containerization_validateResourceUsage():
    resource_usage = ""
    high_cpu = False
    high_memory = False
    data = '"method": "DeviceInfo.1.systeminfo"'
    result = execute_step(data)
    if result != "EXCEPTION OCCURRED":
        cpuload = result["cpuload"]
        if float(cpuload) > float(90):
            high_cpu = True
            high_resource = "CPU"
            #Command to get the top 5 processes with high CPU usage
            command = 'top -o %CPU -bn 1 -w 512 | grep "^ " | awk \'{ printf("%s:%s,\\n",$12, $9); }\' | head -n 6 | tail -n +2 | tr -d \'\\n \''
            print "\n CPU load is high : {}".format(float(cpuload))
        else:
            print "\n CPU load : {}".format(float(cpuload))
        totalram = result["totalram"]
        freeram = result["freeram"]
        memory_usage = round(float(totalram-freeram)/float(totalram)* 100,2)
        if memory_usage > float(90):
            high_memory = True
            high_resource = "MEM"
            #Command to get the top 5 processes with high MEM usage
            command = 'top -o %MEM -bn 1 -w 512 | grep "^ " | awk \'{ printf("%s:%s,\\n",$12, $10); }\' | head -n 6 | tail -n +2 | tr -d \'\\n \''
            print "\n Memory usage is high: {}".format(memory_usage)
        else:
            print "\n Memory usage : {}".format(memory_usage)
        if high_cpu and high_memory:
            high_resource = "CPU and MEM"
            command = 'top -bn 1 -w 512 | grep "^ " | awk \'{ printf("%s : [cpu-%s][mem-%s],\\n",$12, $10, $9); }\' | head -n 6 | tail -n +2 | tr -d \'\\n \''
        if high_cpu or high_memory:
            resource_usage = "ERROR"
            #List top 5 processes with high resource usage
            print "COMMAND : %s" %(command)
            output = containerization_executeInDUT(ssh_method,credentials,command)
            print "\n<b>Top 5 process with high {} usage:</b>\n".format(high_resource)
            output = output.split("\n")[1]
            print '\n\n'.join(output.split(","))
        else:
            resource_usage = cpuload +","+str(memory_usage)
        return resource_usage
    else:
        return result

#-------------------------------------------------------------------
#VALIDATE VIDEO PLAYBACK IN PREMIUM APPS
#-------------------------------------------------------------------
def containerization_validateVideoPlayback(sshmethod,credentials,video_validation_script):
    result = "SUCCESS"
    video_validation_script = video_validation_script.split('.py')[0]
    try:
        lib = importlib.import_module(video_validation_script)
        method = "check_video_status"
        method_to_call = getattr(lib, method)
        result = method_to_call(sshmethod,credentials)
    except Exception as e:
        print "\n ERROR OCCURRED WHILE IMPORTING THE VIDEO VALIDATION SCRIPT FILE, PLEASE CHECK THE CONFIGURATION \n"
        result = "FAILURE"
    finally:
        return result

#-------------------------------------------------------------------
#REMOVE UNWANTED PROCESSES FROM ZORDER AND RETURN UPDATED ZORDER
#-------------------------------------------------------------------
def exclude_from_zorder(zorder):
   new_zorder = [ element for element in zorder if element not in excluded_process_list ] 
   return new_zorder

#--------------------------------------------------------------------
#EXECUTE COMPLETE LIFECYCLE METHODS OF A PLUGIN
#--------------------------------------------------------------------
def containerization_executeLifeCycle(plugin,operations,validation_details):
    result = "FAILURE"
    #Dictionary to store the method and parameter to be passed for that method
    suspend_resume_dict = {"suspend":{"method":"org.rdk.RDKShell.1.suspend","param":'{"callsign":"'+plugin+'"}'},"resume":{"method":"org.rdk.RDKShell.1.launch","param":'{"callsign":"'+plugin+'", "type":"", "uri":""}'}}
    #Dictionary to store the expected values for suspend and resume operations
    expected_status_dict = {"suspend":["suspended"],"resume":["activated","resumed"]}
    #Parameter used for move to front and move to back
    param_val = '{"client": "'+plugin+'"}'
    #Dictionary to store the index values to be checked in move to back and front operations
    check_zorder_dict = {"moveToBack":-1,"moveToFront":0}
    status = containerization_validatePluginFunctionality(plugin,operations,validation_details)
    sys.stdout.flush()
    if status == "SUCCESS":
        #Suspend and resume operations
        for operation in ["suspend","resume"]:
            method = suspend_resume_dict[operation]["method"]
            value = suspend_resume_dict[operation]["param"]
            operation_status = containerization_setValue(method,value)
            if operation_status != "EXCEPTION OCCURRED":
                time.sleep(5)
                curr_status = containerization_getPluginStatus(plugin)
                sys.stdout.flush()
                if curr_status in expected_status_dict[operation]:
                    print "\n Successfully set {} plugin to {} status".format(plugin,curr_status)
                else:
                    print "\n Error while setting {} plugin to {} status, current status: {}".format(plugin,operation,curr_status)
                    break
            else:
                print "\n Error while setting {} plugin to {}".format(plugin,operation)
                break
        #On successfull completion of the loop for suspend and resume, below block will get executed
        else:
            print "\n Successfully completed suspend and resume for {} plugin".format(plugin)
            #Do move to front and back operations
            for move_to_method in ["moveToBack","moveToFront"]:
                move_to_status = containerization_setValue("org.rdk.RDKShell.1."+move_to_method,param_val)
                if move_to_status != "EXCEPTION OCCURRED":
                    time.sleep(5)
                    zorder_result = containerization_getValue("org.rdk.RDKShell.1.getZOrder")
                    sys.stdout.flush()
                    if zorder_result != "EXCEPTION OCCURRED":
                        print zorder_result
                        zorder = zorder_result["clients"]
                        zorder = exclude_from_zorder(zorder)
                        if zorder[check_zorder_dict[move_to_method]].lower() == plugin.lower():
                            print "\n {} operation is success ".format(move_to_method)
                        else:
                            print "\n Error while doing {} operation ".format(move_to_method)
                            break
                    else:
                        print "\n Error while getting the zorder"
                        break
                else:
                    print "\n Error while doing {} operation ".format(move_to_method)
                    break
            else:
                print "\n Successfully completed move to back and move to front for the {} plugin".format(plugin)
                result = "SUCCESS"
    else:
        print "\n Error occurred while lauching and checking the plugin functionality"
    #Destroy the plugin
    print "\n Deactivate {} plugin".format(plugin)
    status = containerization_setPluginStatus(plugin,"deactivate")
    if status != "EXCEPTION OCCURRED":
        #Get the status
        time.sleep(10)
        plugin_status = containerization_getPluginStatus(plugin)
        if plugin_status != 'deactivated':
            print "\n {} plugin is not in deactivated state, current status:{}".format(plugin,plugin_status)
            result = "FAILURE"
        else:
            print "\n Successfully deactivated {} plugin".format(plugin)
    else:
        print "\n Error while deactivating {} plugin".format(plugin)
        result = "FAILURE"
    return result

#-------------------------------------------------------------------
#VALIDATE PLUGIN FUNCTIONALITY
#The function will launch the plugin and validate the functionality
#of the plugin. eg: launch Cobalt, set video URL and validate video
#playback
#-------------------------------------------------------------------
def containerization_validatePluginFunctionality(plugin,operations,validation_details):
    result = "FAILURE"
    operations = json.loads(operations)
    validation_details = json.loads(validation_details)
    movedToFront = False
    #Activate plugin
    print "\n Activating plugin : {}".format(plugin)
    if plugin == "ResidentApp":
        status = containerization_setPluginStatus(plugin,"activate",validation_details[1])
    else:
        status = containerization_setPluginStatus(plugin,"activate")
    time.sleep(5)
    #Check status
    if status != "EXCEPTION OCCURRED":
        curr_status = containerization_getPluginStatus(plugin)
        time.sleep(10)
        if curr_status in ("activated","resumed"):
            zorder_result = containerization_getValue("org.rdk.RDKShell.1.getZOrder")
            if zorder_result != "EXCEPTION OCCURRED":
                zorder = zorder_result["clients"]
                zorder = exclude_from_zorder(zorder)
                if plugin.lower() in zorder:
                    if zorder[0].lower() != plugin.lower():
                        param = '{"client": "'+plugin+'"}'
                        movetofront_result = containerization_setValue("org.rdk.RDKShell.1.moveToFront",param)
                        if movetofront_result != "EXCEPTION OCCURRED":
                            movedToFront = True
                    else:
                        movedToFront = True
                else:
                    print "\n {} is not present in the zorder: {}".format(plugin,zorder)
                if movedToFront:
                    for operation in operations:
                        method = [plugin_method for plugin_method in operation][0]
                        value = [operation[plugin_method] for plugin_method in operation][0]
                        response = containerization_setValue(method,value)
                        sys.stdout.flush()
                        if response == "EXCEPTION OCCURRED":
                            print "\n Error while executing {} method".format(method)
                            break
                        time.sleep(20)
                    else:
                        print "\n Successfully completed launching and setting the operations for {} plugin".format(plugin)
                        validation_check = validation_details[0]
                        if validation_check == "video_validation":
                            time.sleep(20)
                            sshmethod = validation_details[1]
                            credentials = validation_details[2]
                            video_validation_script = validation_details[3]
                            video_status =  containerization_validateVideoPlayback(sshmethod,credentials,video_validation_script)
                            sys.stdout.flush()
                            if video_status != "SUCCESS":
                                print "\n Video is not playing"
                                return result
                            else:
                                print "\n Video is playing"
                                result = "SUCCESS"
                        elif validation_check == "no_validation":
                            print "\n Validation is not needed, proceeding the test"
                            result = "SUCCESS"
                        else:
                            method = validation_check
                            expected_value = validation_details[1]
                            value = containerization_getValue(method)
                            if value not in ("EXCEPTION OCCURRED", None) and expected_value in value:
                                print "\n The value:{} set for {} plugin".format(value,plugin)
                                result = "SUCCESS"
                            else:
                                print "\n Expected Value is not present, Current value: {}".format(value)
                                return result
                else:
                    print "\n Error while moving {} plugin to front ".format(plugin)
            else:
                print "\n Error while getting the zorder result"
        else:
            print "\n Plugin is not activated, current status: {}".format(curr_status)
    else:
        print "\n Error while activating the plugin"
    return result

#------------------------------------------------------------------
#SET PLUGIN STATUS
#------------------------------------------------------------------
def containerization_setPluginStatus(plugin,status,uri=''):
    data = ''
    if plugin:
            #if rdkshell_activated:
            if status in "activate":
                data = '"method":"org.rdk.RDKShell.1.launch", "params":{"callsign": "'+plugin+'", "type":"", "uri":"'+uri+'"}'
            else:
                data = '"method":"org.rdk.RDKShell.1.destroy", "params":{"callsign": "'+plugin+'"}'
    else:
        data = '"method": "Controller.1.'+status+'", "params": {"callsign": "'+plugin+'"}'
    if data != '':
        result = execute_step(data)
    else:
        result = "EXCEPTION OCCURRED"
    return result

