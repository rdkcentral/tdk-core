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
import requests
from selenium import webdriver
import os
import websocket
import time
import configparser
import importlib
import re

import WebAudioVariables
import web_socket_util
from web_socket_util import *

deviceIP=""
devicePort=""
deviceName=""
deviceType=""
deviceMac=""
realpath=""
securityEnabled=False
deviceToken=""
expectedResult="SUCCESS"
#METHODS
#---------------------------------------------------------------
#INITIALIZE THE MODULE
#---------------------------------------------------------------
def init_module(libobj,port,deviceInfo):
    global deviceIP
    global devicePort
    global deviceName
    global deviceType
    global libObj
    global realpath
    global deviceMac
    deviceIP = libobj.ip;
    devicePort = port
    deviceName = deviceInfo["devicename"]
    deviceType = deviceInfo["boxtype"]
    libObj = libobj
    try:
        deviceMac = deviceInfo["mac"]
    except Exception as e:
        print("\nException Occurred while getting MAC \n")
        print(e)

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
        print("ERROR!! \nEXCEPTION OCCURRED WHILE EXECUTING CURL COMMANDS!!")
        print("Command : ",data)
        print("Error message received :\n",e);
        response = "EXCEPTION OCCURRED"
    return response,json_response,status

#---------------------------------------------------------------
#EXECUTE CURL REQUESTS
#---------------------------------------------------------------
def execute_step(Data,IsPerformanceSelected="false"):
    status = "SUCCESS"
    global securityEnabled
    try:
        data = '{"jsonrpc": "2.0", "id": 1234567890, '+Data+'}'
        response,json_response,status = postCURLRequest(data,securityEnabled)
        if status == "INVALID TOKEN":
            print("\nAuthorization issue occurred. Update Token & Re-try...")
            global deviceToken
            tokenFile = libObj.realpath + "/" + "fileStore/tdkvRDKServiceConfig/tokenConfig/" + deviceName + ".config"
            if not securityEnabled:
                # Create the Device Token config file and update the token
                token_status,deviceToken = read_token_config(deviceIP,tokenFile)
                if token_status == "SUCCESS":
                    print("\nDevice Security Token obtained successfully")
                else:
                    print("\nFailed to get the device security token")
                securityEnabled = True
            else:
                # Update the token in the device token config file
                token_status,deviceToken  = handleDeviceTokenChange(deviceIP,tokenFile)
            if token_status == "SUCCESS":
                response,json_response,status = postCURLRequest(data,securityEnabled)
            else:
                print("\nFailed to update the token in token config file")
            if status == "INVALID TOKEN":
                token_status,deviceToken  = handleDeviceTokenChange(deviceIP,tokenFile)
                if token_status=="SUCCESS":
                    response,json_response,status = postCURLRequest(data,securityEnabled)
                else:
                    status = "FAILURE"
        if status == "SUCCESS":
            print("\n---------------------------------------------------------------------------------------------------")
            print("Json command : ", data)
            print("\n Response : ", json_response, "\n")
            print("----------------------------------------------------------------------------------------------------\n")
            result = json_response.get("result")
            if result != None and "'success': False" in str(result):
                result = "EXCEPTION OCCURRED"
            if IsPerformanceSelected == "YES":
                time_taken = response.elapsed.total_seconds()
                print("Time taken for",Data,"is :", time_taken)
                return time_taken;
            IsPerformanceSelected = libObj.parentTestCase.performanceBenchMarkingEnabled
            if IsPerformanceSelected == "true":
                conf_file,result_conf = getConfigFileName(libObj.realpath)
                result_time, max_response_time = getDeviceConfigKeyValue(conf_file,"MAX_RESPONSE_TIME")
                time_taken = response.elapsed.total_seconds()
                print("Time Taken for",Data,"is :", time_taken)
                if (float(time_taken) <= 0 or float(time_taken) > float(max_response_time)):
                    print("Device took more than usual to respond.")
                    print("Exiting the script")
                    result = "EXCEPTION OCCURRED"
        else:
            result = response;
        return result;
    except requests.exceptions.RequestException as e:
        print("ERROR!! \nEXCEPTION OCCURRED WHILE EXECUTING CURL COMMANDS!!")
        print("Error message received :\n",e);
        return "EXCEPTION OCCURRED"

#----------------------------------------------------------------------
#GET THE NAME OF DEVICE CONFIG FILE
#----------------------------------------------------------------------
def getConfigFileName(basePath):
    deviceConfigFile=""
    status ="SUCCESS"
    configPath = basePath + "/"   + "fileStore/tdkvRDKServiceConfig"
    deviceNameConfigFile = configPath + "/" + deviceName + ".config"
    deviceTypeConfigFile = configPath + "/" + deviceType + ".config"

    # Check whether device / platform config files required for
    # executing the test are present
    if os.path.exists(deviceNameConfigFile) == True:
        deviceConfigFile = deviceNameConfigFile
        print("[INFO]: Using Device config file: %s" %(deviceNameConfigFile))
    elif os.path.exists(deviceTypeConfigFile) == True:
        deviceConfigFile = deviceTypeConfigFile
        print("[INFO]: Using Device config file: %s" %(deviceTypeConfigFile))
    else:
        status = "FAILURE"
        print("[ERROR]: No Device config file found : %s or %s" %(deviceNameConfigFile,deviceTypeConfigFile))
    return deviceConfigFile,status;

#-------------------------------------------------------------------------
#GET THE VALUES FROM DEVICE CONFIG FILE
#-------------------------------------------------------------------------
def getDeviceConfigKeyValue(deviceConfigFile,key):
    value  = ""
    status = "SUCCESS"
    deviceConfig  = "device.config"
    try:
        # If the key is none object or empty then exception
        # will be thrown
        if key is None or key == "":
            status = "FAILURE"
            print("\nException Occurred: [%s] key is None or empty" %(inspect.stack()[0][3]))
        # Parse the device configuration file and read the
        # data. But if the data is empty it is taken as such
        else:
            config = configparser.ConfigParser()
            config.read(deviceConfigFile)
            value = str(config.get(deviceConfig,key))
    except Exception as e:
        status = "FAILURE"
        print("\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e))

    return status,value

#-----------------------------------------------------------------------------
#PRE-REQUISITE CHECK FOR WEBAUDIO TESTING
#-----------------------------------------------------------------------------
def webaudio_prerequisite(VariableList):
    pre_requsite_status="SUCCESS"
    VariableList = VariableList.split(",")
    #Check all required variable values from WebAudioVariables.py
    for var in VariableList:
        value = getattr(WebAudioVariables, var, None)
        if value is None or value == "":
            print("ERROR: Please configure ", var , "in WebAudioVariables.py file")
            pre_requsite_status="FAILURE"

    return pre_requsite_status

#-----------------------------------------------------------------
#GET PLUGIN STATUS
#-----------------------------------------------------------------
def webaudio_getPluginStatus(plugin):
    data = '"method": "Controller.1.status@'+plugin+'"'
    result = execute_step(data)
    if result != None and result != "EXCEPTION OCCURRED":
        for x in result:
            WebKitStatus=x["state"]
        return WebKitStatus
    else:
        return result;

#----------------------------------------------------------------------------
#CHECK THE STATUS OF RDKSHELL PLUGIN AND ACTIVATE IF NEEDED
#----------------------------------------------------------------------------
def webaudio_rdkshellStatus():
    activated = False
    rdkshell_status = webaudio_getPluginStatus("org.rdk.RDKShell")
    if "activated" == rdkshell_status:
        activated = True
    elif "deactivated" == rdkshell_status:
        set_status = webaudio_setPluginStatus("org.rdk.RDKShell","activate")
        time.sleep(2)
        rdkshell_status = webaudio_getPluginStatus("org.rdk.RDKShell")
        if "activated" in rdkshell_status:
            activated = True
        else:
            print("\n Unable to activate RDKShell plugin")
    else:
        print("\n RDKShell status in DUT:",rdkshell_status)
    return activated

#-----------------------------------------------------------------------------
#LAUNCH PLUGIN INSTANCE IN DEVICE
#-----------------------------------------------------------------------------
def webaudio_setPluginStatus(plugin,status,uri=''):
    data = ''
    rdkshell_activated = webaudio_rdkshellStatus()
    if rdkshell_activated:
        if status in "activate":
            data = '"method":"org.rdk.RDKShell.1.launch", "params":{"callsign": "'+plugin+'", "type":"", "uri":"'+uri+'"}'
        else:
            data = '"method":"org.rdk.RDKShell.1.destroy", "params":{"callsign": "'+plugin+'"}'
        if data !='':
            result = execute_step(data)
        else:
            print ("ERROR : Failed to create the json data to launch the plugin")
            result = "EXCEPTION OCCURRED"
    else:
        print ("ERROR: Failed to activate RDKShell to launch the plugin")
        result = "EXCEPTION OCCURRED"
    return result

#-------------------------------------------------------------------
#GET THE VALUE OF A METHOD
#-------------------------------------------------------------------
def webaudio_getValue(method):
    data = '"method": "'+method+'"'
    result = execute_step(data)
    return result

#------------------------------------------------------------------
#SET VALUE FOR A METHOD
#------------------------------------------------------------------
def webaudio_setValue(method,value):
    data = '"method": "'+method+'","params": '+value
    result = execute_step(data)
    return result

#--------------------------------------------------------------------------------
#CREATE WEBSOCKET CONNECTION TO WEBINSPECT PAGE
#---------------------------------------------------------------------------------
def webaudio_create_socket_connection():

    port = WebAudioVariables.webinspect_port
    webinspect_url ='http://'+deviceIP+':'+port+'/Main.html?ws='+deviceIP+':'+port+'/socket/1/1/WebPage'
    websocket_url = 'ws://'+deviceIP+':'+port+'/socket/1/1/WebPage'
    web_socket_util.deviceToken=''
    result ="SUCCESS"
    # Function to open Chrome browser
    def open_chrome_browser(webinspect_url):
        # Set the display environment variable
        os.environ["PATH"] = WebAudioVariables.chromedriver_path
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(chrome_options=chrome_options) #Opening Chrome
            driver.get(webinspect_url)
        except Exception as error:
            print("Got exception while opening the browser")
            print(error)
            driver = False
            result ="FAILURE"
        return driver


    # Open the browser
    print ("\n Open webinspect page in chrome browser")
    driver = open_chrome_browser(webinspect_url)

    if not driver:
        return "Error: Unable to open the browser"
        result ="FAILURE"
    else:
        print ("SUCCESS: Successfully opened Chrome has opened with the webinspect page\n")

    # Wait for a few seconds to allow the WebSocket connection to establish
    time.sleep(5)

    webkit_console_socket = createEventListener(deviceIP,port,[],"/socket/1/1/WebPage",False)
    # Close the browser
    driver.quit()

    return result, driver, webkit_console_socket

#-----------------------------------------------------------------------------------------
#LAUNCH WEBAUDIO TEST APP IN BROWSER TO START THE TEST
#-----------------------------------------------------------------------------------------
def webaudio_launch_testApp(obj, url,browser):
    result = "FAILURE"
    browser_method = browser+".1.url"

    tdkTestObj = obj.createTestStep('webaudio_setPluginStatus')
    tdkTestObj.addParameter("plugin",browser)
    tdkTestObj.addParameter("status","activate")
    tdkTestObj.addParameter("uri",url)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    if expectedResult in result:
        print("SUCCESS: Launching ",browser, " with ",url, "returned success")
        tdkTestObj.setResultStatus("SUCCESS")

        print("\n Verify the URL in ", browser)
        time.sleep(10)
        tdkTestObj = obj.createTestStep("webaudio_getValue")
        tdkTestObj.addParameter("method",browser_method)
        tdkTestObj.executeTestCase(expectedResult)
        new_url=tdkTestObj.getResultDetails()
        result = tdkTestObj.getResult()
        if expectedResult in result and new_url == url:
            print("SUCCESS: Successfully loaded ",url," in ", browser)
            tdkTestObj.setResultStatus("SUCCESS")
            result = "SUCCESS"
        else:
            print("FAILURE: Failed to load", url , " in ", browser)
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("FAILURE: Failed to launch ", browser , " with ", url)
        tdkTestObj.setResultStatus("FAILURE")
    return result

#-----------------------------------------------------------------------------------------
#TO PRESS KEYS IN UI USING RDKSHELL
#-----------------------------------------------------------------------------------------
def webaudio_keypress(obj,browser,keys):
    result="FAILURE"
    param='['
    index=0
    for key in keys:
        if ":" in key:
            param = param + '{"keyCode": ' + key + ',"modifiers": ['+ key.split(":")[0] +'],"delay":1.0,'+ '"callsign":' +browser+',"client":' + browser+ '}'
        else:
            param = param + '{"keyCode": ' + key + ',"modifiers": [],"delay":1.0,'+ '"callsign":' +browser+',"client":' + browser+ '}'
        if index != (len(keys)-1):
            param = param + ','
        else:
            param = param + ']'
        index +=1

    params = '{"keys":'+ param + '}'
    tdkTestObj = obj.createTestStep('webaudio_setValue')
    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
    tdkTestObj.addParameter("value",params)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    if expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        print("SUCCESS: Navigated through UI and started the test")
        result = "SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("FAILURE : Failed to start the test by navigating through UI")
    return result


#-----------------------------------------------------------------------------------------
#GET LOGS FROM WEBINSPECT PAGE 
#-----------------------------------------------------------------------------------------
def webaudio_getLogs_webinspectpage(obj, url, browser,keys=[]):
    log_message = []
    continue_count = 0

    def string_to_dict(string_data):
        parsed_data = {}
        # Remove unnecessary escape characters
        string_data = string_data.replace('\\"', '"')
        string_data = string_data.replace("{","")
        string_data = string_data.replace("}","")
        string_data = string_data.replace("[","")
        string_data = string_data.replace("]","")
        key_value_pairs = string_data.split(',')
        # Iterate over the key-value pairs
        for pair in key_value_pairs:
            # Split each pair by the first colon to separate key and value
            key, value = pair.split(':', 1)
            key = key.strip('" ')
            key=key.replace("\\", "")
            key=key.replace('"','')
            value = value.strip('" ')
            value = value.replace('\\',"")
            value = value.replace('"','')
            # Add key-value pair to the dictionary
            parsed_data[key] = value
        return parsed_data

    result, driver, webkit_console_socket = webaudio_create_socket_connection()
    if expectedResult in result:
        print("SUCCESS: Successfully established websocket connection to webinspect page of the device")
        time.sleep(30)

        print("\n Launch webaudio test url in ", browser)
        result = webaudio_launch_testApp(obj,url,browser)
        if keys !=[] and expectedResult in result:
            print ("\n Navigate through webaudio test UI and start test ")
            result=webaudio_keypress(obj,browser,keys)
        if expectedResult in result:
            print("\n Get logs from the webinspect page")
            while True:
                if continue_count > 60:
                    print ("FAILURE: Failed to get logs from webinspect page of the device")
                    break;
                if (len(webkit_console_socket.getEventsBuffer())== 0):
                    time.sleep(1)
                    continue_count += 1
                    continue
                console_log = webkit_console_socket.getEventsBuffer().pop(0)
                if "TDK_LOGS" in console_log:
                    log_dict=string_to_dict(console_log)
                    log_message.append(log_dict["text"])
                if "TDK_END" in console_log:
                    break;
    else:
        print ("FAILURE : Failed to establish websocket connection to webinspect page of the device")
        tdkTestObj.setResultStatus("FAILURE")
    driver.quit()
    webkit_console_socket.disconnect()
    return log_message

#-------------------------------------------------------------------
#GET THE SSH DETAILS FROM CONFIGURATION FILE
#-------------------------------------------------------------------
def webaudio_getSSHParams():
    ssh_dict = {}
    print("\n getting ssh params from conf file")
    conf_file,result = getConfigFileName(libObj.realpath)
    if result == "SUCCESS":
        result,ssh_method = getDeviceConfigKeyValue(conf_file,"SSH_METHOD")
        result,user_name = getDeviceConfigKeyValue(conf_file,"SSH_USERNAME")
        result,password = getDeviceConfigKeyValue(conf_file,"SSH_PASSWORD")
        if any(value == "" for value in (ssh_method,user_name,password)):
            print("please configure values before test")
            ssh_dict = {}
        else:
            ssh_dict["ssh_method"] = ssh_method
            if password.upper() == "NONE":
                password = ""
            ssh_dict["credentials"] = deviceIP +","+ user_name +","+ password
    else:
        print("Failed to find the device specific config file")
    ssh_dict = json.dumps(ssh_dict)
    return ssh_dict

#-------------------------------------------------------------------
#GET THE OUTPUT OF A COMMAND EXECUTED
#-------------------------------------------------------------------
def webaudio_getRequiredLog(ssh_method,credentials,command):
    output = ""
    credentials_list = credentials.split(',')
    host_name = credentials_list[0]
    user_name = credentials_list[1]
    password = credentials_list[2]
    lib = importlib.import_module("SSHUtility")
    if ssh_method == "directSSH":
        method = "ssh_and_execute"
    else:
        method = "ssh_and_execute_" + ssh_method
    method_to_call = getattr(lib, method)
    try:
        if ssh_method == "directSSH":
            output = method_to_call(ssh_method,host_name,user_name,password,command)
        else:
            output = method_to_call(host_name,user_name,password,command)
    except Exception as e:
        print("Exception occured during ssh session")
        print(e)
    finally:
        if output == "":
            output = "EXCEPTION"
        return output

#-------------------------------------------------------------------
#GET THE TIMESTAMP FROM THE LOG STRING
#-------------------------------------------------------------------
def getTimeStampFromString(log_string):
    match = re.search(r"(\d{2}:\d{2}:\d{2}\.\d{6})",log_string)
    return match.group(1)

#-------------------------------------------------------------------
#GET THE TIME IN MILLISEC FROM THE STRING
#-------------------------------------------------------------------
def getTimeInMilliSec(time_string):
    microsec_frm_time_string = int(time_string.split(".")[-1])
    time_string = time_string.replace(time_string.split(".")[-1],"")
    time_string = time_string.replace(".",":")
    time_string = time_string + str(microsec_frm_time_string/1000)
    hours, minutes, seconds, millisec = time_string.split(':')
    time_in_millisec = int(hours) * 3600000 + int(minutes) * 60000 + int(seconds)*1000 + float(millisec)
    return time_in_millisec

#------------------------------------------------------------------------------------
#GET LOGS FROM WPEFRAMEWORK LOGS FILE
#------------------------------------------------------------------------------------
def webaudio_getLogs_fromDevicelogs(obj,url,browser,grep_line,keys=[]):
   log_message=""
   print("\n Check for required configurations to ssh to the device") 
   tdkTestObj = obj.createTestStep('webaudio_getSSHParams')
   tdkTestObj.executeTestCase(expectedResult)
   result = tdkTestObj.getResult()
   ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
   if ssh_param_dict != {} and expectedResult in result:
       tdkTestObj.setResultStatus("SUCCESS")
       print("\n Launch webaudio test url in ", browser)
       start_time = str(datetime.utcnow()).split()[1]
       result = webaudio_launch_testApp(obj,url,browser)
       time.sleep(20)
       if keys !=[] and expectedResult in result:
            print ("\n Navigate through webaudio test UI and start test ")
            result=webaudio_keypress(obj,browser,keys)
            time.sleep(60)
       if expectedResult in result:
           time.sleep(10)
           print ("\n Check for the logs in wpeframework logs")
           command = "cat /opt/logs/wpeframework.log | grep -inr 'TDK_LOGS'| grep " + grep_line
           tdkTestObj = obj.createTestStep('webaudio_getRequiredLog')
           tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
           tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
           tdkTestObj.addParameter("command",command)
           tdkTestObj.executeTestCase(expectedResult)
           result = tdkTestObj.getResult()
           output = tdkTestObj.getResultDetails()
           if output != "EXCEPTION" and expectedResult in result:
               log_line = output.split('\n')[1]
               if log_line != "":
                   log_time = getTimeStampFromString(log_line)
                   start_time_millisec = getTimeInMilliSec(start_time)
                   log_line_time_millisec = getTimeInMilliSec(log_time)
                   islogcurrent = log_line_time_millisec - start_time_millisec
                   if float(islogcurrent) >0 :
                       log_message=log_line
                   else:
                       print("FAILURE : Failed to get the logs from wpeframework logs")
                       tdkTestObj.setResultStatus("FAILURE")
               else:
                   print("FAILURE : Failed to get the logs from wpeframework logs ")
                   tdkTestObj.setResultStatus("FAILURE")
           else:
               print("FAILURE : Failed to execute command in the device")
               tdkTestObj.setResultStatus("FAILURE")
       else:
           print("FAILURE: Failed to launch webaudio test url in the device")
           tdkTestObj.setResultStatus("FAILURE")
   else:
       print ("FAILURE: SSH related configurations are missing in device specific config file")
       tdkTestObj.setResultStatus("FAILURE")
   return log_message
