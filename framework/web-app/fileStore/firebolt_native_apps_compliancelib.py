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
import json
import sys
import re
from SSHUtility import *
import SSHUtility
import requests
import os
import subprocess
import inspect
import configparser
from time import sleep
import pexpect
import time
import MediaValidationVariables

ssh_param_dict = {}
securityEnabled=False
# Global variable to store the operations string and use_aamp configuration
operations = ""
use_aamp_for_hls = ""
use_aamp_for_dash = ""
check_pts = ""
check_fps = ""
use_audioSink = ""
use_autoVideoSink_for_fpsdisplaysink = ""
check_audio_fps = ""
test_streams_base_path =""
validateFullPlayback = ""
use_appsrc = ""
start_westeros = ""
create_display = ""

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

#------------------------------------------------------------------------------
# Function to retreive the device details
#------------------------------------------------------------------------------
def getDeviceDetails(detail):
    if detail == "deviceType":
        return deviceType
    elif detail == "deviceIP":
        return deviceIP
    elif detail == "devicePort":
        return devicePort
    else:
        return deviceName


#-------------------------------------------------------------------
#GET THE SSH DETAILS FROM CONFIGURATION FILE
#-------------------------------------------------------------------
def rdkservice_getSSHParams(realpath,deviceIP):
    ssh_dict = {}
    print("\n getting ssh params from conf file")

    ssh_method = getDeviceConfigValue("SSH_METHOD")
    if not ssh_method:
        ssh_method = "directSSH"
    user_name = getDeviceConfigValue("SSH_USERNAME")
    if not user_name:
        user_name = "root"
    password = getDeviceConfigValue("SSH_PASSWORD")
    if not password:
        password = "None"
    if any(value == "" for value in (ssh_method,user_name,password)):
        print("please configure values before test")
        ssh_dict = {}
    else:
        ssh_dict["ssh_method"] = ssh_method
        if password.upper() == "NONE":
            password = ""
            ssh_dict["credentials"] = deviceIP +","+ user_name +","+ password
    ssh_dict = json.dumps(ssh_dict)
    return ssh_dict

#-------------------------------------------------------------------
# Function to execute the command in the DUT using ssh utility
#-------------------------------------------------------------------
def executeCmndInDUT (command,sshMethod="", credentials=""):
    output = ""
    global deviceIP;
    ssh_param = rdkservice_getSSHParams(libObj.realpath,deviceIP)
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
        print("Secure ssh to CPE")
        pass
    try:
        output = ssh_and_execute (sshMethod, host_name, user_name, password, command)
    except Exception as e:
        print("Exception occured during ssh session")
        print(e)
    return output

######################################################################
#
# Functions
#
######################################################################

#Function to retrieve the device configuration from device config file
def getDeviceConfigValue (configKey):
    try:
        global use_aamp_for_hls
        global check_pts
        global check_fps
        global use_audioSink
        global use_autoVideoSink_for_fpsdisplaysink
        global check_audio_fps
        global test_streams_base_path
        global avsync_enabled
        global validateFullPlayback
        global use_appsrc
        global start_westeros
        global create_display

        result = "SUCCESS"
        #Retrieve the device details(device name) and device type from tdk library
        deviceConfigFile=""
        configValue = ""
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
            print(output)
            result = "FAILURE"

        #Continue only if the device config file exists
        if (len (deviceConfigFile) != 0):
            configParser = configparser.ConfigParser()
            configParser.read(r'%s' % deviceConfigFile)
            #Retrieve the value of config key from device config file
            configValue = configParser.get('device.config', configKey)
            try:
                use_aamp_for_hls = configParser.get('device.config',"FIREBOLT_COMPLIANCE_USE_AAMP_FOR_HLS")
            except:
                use_aamp_for_hls = "no"
            try:
                use_aamp_for_dash = configParser.get('device.config',"FIREBOLT_COMPLIANCE_USE_AAMP_FOR_DASH")
            except:
                use_aamp_for_dash = "no"
            try:
                check_pts = configParser.get('device.config',"FIREBOLT_COMPLIANCE_CHECK_PTS")
            except:
                check_pts = "yes"
            try:
                check_fps = configParser.get('device.config',"FIREBOLT_COMPLIANCE_CHECK_FPS")
            except:
                check_fps = "yes"
            try:
                use_audioSink = configParser.get('device.config',"FIREBOLT_COMPLIANCE_USE_AUDIO_SINK")
            except:
                use_audioSink = ""
            try:
                use_autoVideoSink_for_fpsdisplaysink = configParser.get('device.config',"FIREBOLT_COMPLIANCE_USE_AUTOVIDEO_FOR_FPSDISPLAYSINK")
            except:
                use_autoVideoSink_for_fpsdisplaysink = "no"
            try:
                check_audio_fps = configParser.get('device.config',"FIREBOLT_COMPLIANCE_CHECK_AUDIO")
            except:
                check_audio_fps = "no"
            try:
                test_streams_base_path = configParser.get('device.config',"TEST_STREAMS_BASE_PATH")
            except:
                test_streams_base_path = ""
            try:
                validateFullPlayback = configParser.get('device.config',"FIREBOLT_COMPLIANCE_VALIDATE_FULL_PLAYBACK")
            except:
                validateFullPlayback = "no"
            try:
                use_appsrc = configParser.get('device.config',"FIREBOLT_COMPLIANCE_USE_APPSRC")
            except:
                use_appsrc = "no"
            try:
                checkAVStatus = configParser.get('device.config',"FIREBOLT_COMPLIANCE_CHECK_AV_STATUS")
            except:
                checkAVStatus = "no"
            try:
                start_westeros = configParser.get('device.config',"FIREBOLT_COMPLIANCE_START_WESTEROS")
            except:
                start_westeros = "no"
            try:
                create_display = configParser.get('device.config',"FIREBOLT_COMPLIANCE_CREATE_RDKSHELL_DISPLAY")
            except:
                create_display = "no"
        else:
            print("DeviceConfig file not available")
            result = "FAILURE"
    except Exception as e:
        print("Exception occurred while retrieving device configuration  : " + e)
        result = "FAILURE"
    if configValue == "":
        return result
    return configValue


# Function to construct the trickplay operations string from operation, timeout/duration and seek argument values
# Individual operation with arguments(timeout, position etc) should be passed as input (eg: setOperations (seek, 10, 20)
# Separate operations(eg: play:10,pause:10)  should be added by calling the setOperations() separatley
# (eg: setOperations (play, 10) , setOperations (pause, 10) etc)
# For repeating the previous trickplay operations give operation argument as "repeat", followed by the number of operations to be repeated and the repeat count (eg: setOperations (repeat, 1, 2)- for repeating last operation 2 times or setOperations (repeat, 2, 6)- for repeating last 2 operations 6 times etc)
def setOperations (operation, arguments):
    try:
        global operations
        arguments = arguments.split(",")
        #if the repeat operation command is recieved, the previous operations should be repeated the number of times provided as the second argument to repeat
        #Repeat operation will not proceed if there are no previous operations in the string
        if operations and operation == "repeat":
            #The first argument to repeat is the number of previous operation that needs to be repeated
            numberOfOperations = arguments[0]
            #From the operations string, extract the last 'numberOfOperations' number of operations
            #since individual operations are seperated by ',', split the operations string to a list of strings
            splitList = [idx for idx, ch in enumerate(operations) if ch == ',']
            #If there are enough operations to be repeated, select the last 'numberOfOperations' number of operations
            if (len(splitList) > (numberOfOperations - 1)):
                splitIndex = splitList [-numberOfOperations]
                operationsToBeRepeated = operations[splitIndex+1:]
            else:
                operationsToBeRepeated = operations
                for indx in range (0, arguments[1]):
                    operations += "," + operationsToBeRepeated
        elif operation != "repeat":
            if operations != "":
                operations += ","
            operations += operation
            #Add all the arguments
            for argument in arguments:
                operations += ":" + str(float(argument))
        #If there are no operations to be repeated, then repeat command is invalid
        else:
            raise Exception("There are no operations to be repeated")
    except Exception as e:
        print(("Exception occurred while updating the operations string  : " , e))

# Function to retrieve the saved trickplay operation string
def getOperations ():
    return str(operations)

#Function to construct the mediapipelinetest command to be executed in the DUT
def getMediaPipelineTestCommand (test_name, test_url, arguments):
    if test_streams_base_path:
        if not MediaValidationVariables.test_streams_base_path:
            test_url = test_streams_base_path + test_url
        else: 
            test_url = test_url.replace(MediaValidationVariables.test_streams_base_path,test_streams_base_path);
    #First construct the command with mandatory arguments
    command = "tdk_mediapipelinetests " + test_name + " " + test_url
    #For trickplay scenrios use another app instead
    if "trickplay" in test_name:
        command = "tdk_mediapipelinetests_trickplay" + " " + test_url
        if "latency" in test_name.lower():
            command += " checkLatency "
    #Based on the test, the arguments can vary, parse through the variabled arguments
    #and add the available variables
    arguments = arguments.replace("'",'"')
    argList = json.loads(arguments)
    for name, value in list(argList.items ()):
        command += " " + name + "=" + value
    #Feature to disable  video-pts check
    if (check_pts == "no"):
        command = command + " checkPTS=no "
    #Feature to disable video-fps check
    if (check_fps == "no") and "fps" not in command.lower():
        command = command + " checkFPS=no "
    #Use audioSink
    if (use_audioSink):
        command = command + " audioSink=" + use_audioSink;
    #Check Audio fps
    if (check_audio_fps == "no"):
        command = command + " checkAudioFPS=no ";
    #Validate playback to milliseconds
    if (validateFullPlayback == "yes"):
        command = command + " validateFullPlayback ";
    #Use appsrc in pipeline
    if (use_appsrc == "yes"):
        command = command  + " use_appsrc ";
    #Feature to modify hls url to aamp url based on configuration
    if (use_aamp_for_hls == "yes") or (use_aamp_for_dash == "yes"):
        testUrl_list = test_url.split();
        url_list = set()
        #Check if HLS URL is present in command
        for url in testUrl_list:
            if url.endswith(".m3u8") and (use_aamp_for_hls == "yes"):
                url_list.add(url);
                hls_url = True
            elif url.endswith(".mpd") and (use_aamp_for_dash == "yes"):
                url_list.add(url);
                dash_url = True
        if url_list:
            if "trickplay" in test_name:
                url_list.clear()
                if hls_url:
                    url_list.add(MediaValidationVariables.video_src_url_hls_h264_iframe);
                    command = command.replace(test_url,MediaValidationVariables.video_src_url_hls_h264_iframe)
                elif dash_url:
                    url_list.add(MediaValidationVariables.video_src_url_dash_h264_iframe);
                    command = command.replace(test_url,MediaValidationVariables.video_src_url_dash_h264_iframe)
            for url in url_list:
                #Change hls generic url to aamp url
                url_updated = url.replace("https","aamps",1).replace("http","aamp",1);
                command = command.replace(url,url_updated);
    if (start_westeros == "yes"):
        command = command + " startWesteros=yes ";
    elif (create_display == "yes"):
        command = command + " createDisplay=yes";
    return command

#Function to check mediapipeline test execution status from output string
#Returns 'SUCCESS'/'FAILURE' based on the analysis of the output string
def checkMediaPipelineTestStatus (outputString):
    #If the output string returned from 'mediapipelinetests' contains strings "Failures: 0" and "Errors: 0"  or it contains string "failed: 0", then the test suite executed successfully otherwise the test failed
    passStringList = ["Failures: 0", "Errors: 0"]
    passString = "failed: 0"

    if ((all (token in outputString for token in passStringList)) or (passString in outputString)):
        result = "SUCCESS"
    else:
        result = "FAILURE"

    if "No such testcase is present in app" in outputString:
        print("App present in DUT doesnot have such test. Please update the app\n")
        result = "FAILURE"

    return result

# Function to check the latency value
#Returns 'SUCCESS'/'FAILURE' based on the latency obtained
def parseLatency(latencyThreshold,output):
    latency_string = [line for line in output.splitlines() if "Time measured" in line]
    if not latency_string:
        print("Unable to retrieve latency")
        return "FAILURE"
    latency_string = str(latency_string[0])
    latency = latency_string.split()[2]
    if int(latency) < int(latencyThreshold):
        print("Latency:",latency)
        print("Latency retrieved was optimal")
        return "SUCCESS"
    else:
        print("Latency retrieved was not optimal")
        print("Expected Latency :",latencyThreshold)
        print("Actual Latency:",latency)
        return "FAILURE"

#Function to check the codec in audio change
#Returns 'SUCCESS'/'FAILURE' based on the analysis of the output string
def checkifCodecPlayed(codec):
    logFile = " /opt/TDK/audio_change_log "
    if "e-ac-3" in  codec:
        codec_search = '"e-ac-3\|e-ac3\|eac-3"'
    else:
        codec_search = codec
    command = " grep -inr " + codec_search + logFile
    output = executeCmndInDUT(command)
    if output:
        print("%s played successfully"%codec)
        return "SUCCESS"
    else:
        print("%s audio playback failed"%codec)
        return "FAILURE"

#Function to check the Language played
#Returns 'SUCCESS'/'FAILURE' based on the analysis of the output string
def checkifLanguagePlayed(language):
    logFile = " /opt/TDK/audio_change_log "
    command = " grep -inr " + language + logFile
    output = executeCmndInDUT(command)
    if output:
        print("%s played successfully"%language)
        return "SUCCESS"
    else:
        print("%s audio playback failed"%language)
        return "FAILURE"

#Function to verify the output of graphics test execution
#Returns 'SUCCESS'/'FAILURE' based on the error pattern corresponding to the test app
def ParseGraphicsOutput(graphics_output,test_app):
    #Remove wpeframework.service related prints from log
    formatted_output = [line for line in graphics_output.splitlines() if "wpeframework.service" not in line]
    output = '\n'.join(formatted_output)
    print(output)
    print ("*" * 80)
    #If test application is Waymetric, obtain speed indices
    if test_app == "Waymetric":
        if "Waymetric Package is not installed" in output:
            print ("FAILURE: Waymetric not installed in DUT")
            print ("*" * 80)
            return "FAILURE"
        waymetric_report = " cat /tmp/waymetric-report.txt "
        output = executeCmndInDUT(waymetric_report)
        speed_indices = [line for line in output.splitlines() if "speed index" in line]
        if not speed_indices:
            print ("FAILURE: Unable to obtain speed index\nExecution Failed")
            print ("*" * 80)
            return "FAILURE"
        else:
            print (speed_indices)
            print ("SUCCESS: Waymetric execution was successfull")
            print ("*" * 80)
            return "SUCCESS"
    #Check if app exited gracefully without any crash
    if ("Exiting from the test app" not in output) and ("westeros_test: exit" not in output):
        print ("FAILURE: Test Application was not exited gracefully")
        print ("*" * 80)
        return "FAILURE"
    #If test application is Westeros_TDKTestApp , validate error statements
    if test_app == "Westeros_TDKTestApp":
        #ignore "error opening device: /dev/input/event0" as output
        if "error" in output and "error opening device" not in output:
            print ("FAILURE: ERROR observed in execution")
            print ("*" * 80)
            return "FAILURE"
        else:
            print ("SUCCESS: WesterosTDKTestApp execution was successfull")
            print ("*" * 80)
            return "SUCCESS"
    #Check if all APIs are validated successfully
    #13 APIs must be validated for EssosTDKTestApp
    validation_success = output.count("VALIDATION SUCCESS");
    if validation_success == 13:
        print ("SUCCESS : All Essos APIs validated successfully")
        print ("*" * 80)
        return "SUCCESS"
    else:
        print ("FAILURE: VALIDATION ERROR observed")
        print ("*" * 80)
        validation_error_strings = [line for line in output.splitlines() if "VALIDATION ERROR" in line]
        print("ERROR Observed:")
        for matched_line in validation_error_strings:
             print(matched_line)
        return "FAILURE"

#Function to validate latency of the test operation
#Returns 'SUCCESS'/'FAILURE' based on the latency obtained from the output string compared with latencyThreshold
def DurationParse(duration_to_be_verified,output):
    duration_pattern = re.compile(r'Duration: (\d+:\d+\.\d+)')
    match = duration_pattern.search(output)
    if match:
        duration = match.group(1)
        print("Duration : ",duration)
        minutes, seconds = list(map(float, duration.split(':')))
        total_minutes = minutes * 60 + seconds
        if total_minutes >= duration_to_be_verified:
            print("SUCCESS : Duration verified successfully\nExpected Duration :%s"%(duration_to_be_verified))
            return "SUCCESS"
        else:
            print("FAILURE : Duration is less than %d minutes."%(duration_to_be_verified))
            return "FAILURE"
    else:
        print("FAILURE : Unable to Verify Duration")
        return "FAILURE"
