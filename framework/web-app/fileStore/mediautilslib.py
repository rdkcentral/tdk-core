#!/usr/bin/python
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
##########################################################################

#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import threading
from SSHUtility import *
from tdklib import *
from time import sleep
import configparser

# Description  : Parse the device config file fields.
#
# Parameters   : obj: Instance of mediautils component library
#
# Return Value : "SUCCESS"/"FAILURE"
#
def getDeviceConfig(obj,configSection,configKey):
    #Get the device name configured in test manager
    deviceDetails = obj.getDeviceDetails()
    deviceName = deviceDetails["devicename"]
    #Get the device configuration file name
    deviceConfig = deviceName + ".config"

    #Get the current directory path
    configFilePath = os.path.dirname(os.path.realpath(__file__))
    configFilePath = configFilePath + "/tdkvDeviceConfig"

    #Parse the device configuration file
    ConfigFile = configFilePath+'/'+deviceConfig

    try :
        configParser = configparser.ConfigParser()
        configParser.read(r'%s' %ConfigFile)
        configValue = configParser.get(configSection, configKey)
        if configKey == "password" and configValue == "None":
            configValue=""
        #print ("%s : %s"%(configKey,configValue))
        return configValue
    except:
        print("deviceConfig file not found")
        if configKey == "user_name":
            return "root"
        elif configKey == "password":
            return ""
        elif configKey == "sshMethod":
            return "directSSH"
        else:
            print("Unable to retrieve " ,configKey)
            return "FAILURE"

# Description  : To ssh the device and entered stream playback command
#
# Parameters   : obj: Instance of mediautils component library
#
# Return Value : "TRUE"/"FALSE"
#
def play(obj,timeout):
    global user_name
    global password
    global sshMethod
    user_name = getDeviceConfig(obj,"sshCredentials-config","user_name")
    password = getDeviceConfig(obj,"sshCredentials-config","password")
    sshMethod = getDeviceConfig(obj,"sshCredentials-config","sshMethod")
    def thread_function(obj,timeout):
        url = getDeviceConfig(obj,"mediautils-config","playback_url")
        if not url:
            print("URL is empty")
            return False
        command  = " tdk_mediapipelinetests test_generic_playback " + url + " checkAudioFPS=no checkFPS=no timeout=" + str(timeout)
        global user_name
        global password
        global sshMethod
        host_name = obj.IP
        output = ssh_and_execute (sshMethod, host_name, user_name, password, command)
        output = output.split("\n")
        for line in output[-3:]:
            print(line)
        print ("Mediaplayback thread terminated")
    thread = threading.Thread(target=thread_function,args=(obj,timeout))
    thread.start()
    print("Mediaplayback thread started")
    sleep(10)
    command  = " pidof tdk_mediapipelinetests "
    host_name = obj.IP
    output = ssh_and_execute (sshMethod, host_name, user_name, password, command)
    if output:
        print ("SUCCESS : Video is still playing")
        return True
    else:
        print ("FAILURE : Video is not playing")
        thread.join()
        return False
