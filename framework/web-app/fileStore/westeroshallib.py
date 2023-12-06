#!/usr/bin/python
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
##########################################################################
import ConfigParser
import os

##################################################################
#
# Method to execute obtain the default display size of the device
#
##################################################################
def getDefaultDisplaySize(westerosObj):

    try :

        #Get the device name configured in test manager
        deviceDetails = westerosObj.getDeviceDetails()
        deviceName = deviceDetails["devicename"]
        #Get the device configuration file name
        deviceConfig = deviceName + ".config"

        #Get the current directory path
        configFilePath = os.path.dirname(os.path.realpath(__file__))
        configFilePath = configFilePath + "/tdkvDeviceConfig"


        #Parse the device configuration file
        westerosConfigFile = configFilePath+'/'+deviceConfig
        #if device specific config file doesn't exist, test for 720p window size
        if not os.path.exists(westerosConfigFile):
            print "Default display Size is 720p"
            return 1280,720

        configParser = ConfigParser.ConfigParser()
        configParser.read(r'%s' % westerosConfigFile)
        display_size = configParser.get('westeros-config', 'displaySize')

        if display_size == "1080p":
            print "Display Size set as 1080p"
            return 1920,1080
        elif display_size == "2160p":
            print "Display Size set as 2160p"
            return 3840,2160
        else:
            return 1280,720

    except Exception, e:
        print e;
        print "Testing for 720p window size"
        return 1280,720
