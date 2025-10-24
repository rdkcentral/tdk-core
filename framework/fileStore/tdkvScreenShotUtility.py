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
from screenCaptureUtility import *
from tdklib import *
from tdkStandAlonelib import *
import os

#######################################################################################################
#
# Method to obtain config value from device config file
#
#  obj          : object obtained from TDKScriptingLibrary in TDK Test Script
#  configKey    : key for which config value must be fetched for from device config value
#######################################################################################################
def getConfig(obj,configKey):
    deviceDetails = obj.getDeviceDetails()
    deviceName = deviceDetails["devicename"]
    deviceType = deviceDetails["boxtype"]
    deviceConfigFile=""
    configValue = ""
    basePath = obj.realpath
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
        #Retrieve the value of config key from device config file
        configValue = configParser.get('device.config', configKey)
    else:
        print("DeviceConfig file not available")
        result = "FAILURE"
    if configValue == "":
        return result
    return configValue

#######################################################################################################
#
# Wrapper for screenCaptureUtlity - getSnapShot for TDK Test Scripts
# Method obtains the "SCREEN_CAPTURE_MECHANISM" from device config file
#        fetches device IP and sets the image name and destination path
#
#  obj     : object obtained from TDKScriptingLibrary in TDK Test Script
#######################################################################################################
def getScreenShot(obj):
    base_path = '{}{}_{}_{}'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
    DUT_IP=obj.IP
    deviceDetails = obj.getDeviceDetails()
    obj.ip=obj.IP
    ThunderPort_details = getThunderPortDetails(obj) 
    thunderPort = ThunderPort_details["thunderPort"]
    setThunderPort(thunderPort)
    device_name = deviceDetails["devicename"]
    try:
        screenCaptureMechanism = getConfig(obj,"SCREEN_CAPTURE_MECHANISM")
        print("Got screenCapture Mechanism as ", screenCaptureMechanism)
    except:
        screenCaptureMechanism = "RDKSHELL"

    screenCaptureMechanism = screenCaptureMechanism.lower()
    if screenCaptureMechanism == "rdkshell":
        image_name = base_path + "_" + device_name
        result = getSnapShot(screenCaptureMechanism,DUT_IP,base_path,image_name)
    elif screenCaptureMechanism == "screencaptureservice":
        image_name = '{}_{}_{}_{}'.format(str(obj.execID),str(obj.execDevId),str(obj.resultId),str(device_name))
        cgi_server_url = getConfig(obj,"SC_UPLOAD_URL")
        result = getSnapShot(screenCaptureMechanism,DUT_IP,cgi_server_url,image_name)
        result = '{}{}'.format(obj.logpath,result)
    else:
        print ("FAILURE  :Unsupported Screen Capture Mechanism")
        result =  "FAILURE"

    if not os.path.exists(result):
        result = "FAILURE"
    print("Result from tdkvScreenShotUtility - ",result)
    return result


