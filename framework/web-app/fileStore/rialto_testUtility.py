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
import tdklib;
import os
import ConfigParser

prerequisite_done=False
testCase=1
check_fps = ""
ignore_warnings = ""
use_autoVideoSink_for_fpsdisplaysink = ""
rialto_env_file="${TDK_PATH}/rialto_test"

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
        print "App present in DUT doesnot have such test. Please update the app\n"
        result = "FAILURE"

    return result

#Function to set the pre-requisites for rialto gstreamer testing environment
def setPreRequisite(obj):
    global prerequisite_done
    expectedResult="SUCCESS"
    if not prerequisite_done:
        print "\n\n#---------------------------- Plugin Pre-requisite ----------------------------#"
        print "Pre Requisite : Setup Rialto Environment\nPre Requisite No : 1"

    print "TEST STEP NAME   :  Check Rialto Server Manager running"
    command = "ps -ef | grep -inr RialtoServerManagerSim | grep -v grep"
    print "Executing command in DUT: ", command
    tdkTestObj = obj.createTestStep('ExecuteCommand');
    tdkTestObj.addParameter("command", command)
    tdkTestObj.executeTestCase(expectedResult)
    actualresult = tdkTestObj.getResult()
    output = tdkTestObj.getResultDetails()
    if expectedResult in actualresult.upper() and "RialtoServerManagerSim" not in output :
        if prerequisite_done:
            print  "Unable to set prerequsities"
            Status="FAILURE"
        else:
            print "RialtoServerManagerSim is not running\n\nTEST STEP NAME: Setup environment for Rialto"
            command = "touch %s; ls %s"%(rialto_env_file,rialto_env_file)
            tdkTestObj.addParameter("command", command)
            tdkTestObj.executeTestCase(expectedResult)
            output = tdkTestObj.getResultDetails()
            if expectedResult in actualresult.upper() and "rialto_test" in output :
                print "Rebooting the device......."
                obj.initiateReboot();
                prerequisite_done=True
                setPreRequisite(obj)
                return
            else:
                print "Unable to write in TDK_PATH"
                Status="FAILURE"
    else:
        print "RialtoServerManagerSim is runnning\nRialto Test Setup Environment Completed Successfully"
        Status="SUCCESS"
    tdkTestObj.setResultStatus(Status);
    print "TEST STEP STATUS :",Status
    print "#--------- [Pre-requisite Status] : %s ----------#"%(Status)
    print "Plugin Pre-requisite Status: %s \n\n"%(Status)
    if Status == "FAILURE":
        print "Pre-Requisites FAILED\n\n"
        exit

#Function to reset the environment for rialto gstreamer testing to default environment
def ExecutePostRequisite(obj):
    expectedResult="SUCCESS"
    print "\n#---------------------------- Plugin Post-requisite ----------------------------#\n"
    print "Post Requisite : Restore Default environment in DUT\nPost Requisite No : 1\n\nTEST STEP NAME   :  Restore Default environment"
    tdkTestObj = obj.createTestStep('ExecuteCommand');
    command = "rm %s; ls %s"%(rialto_env_file,rialto_env_file)
    tdkTestObj.addParameter("command", command)
    tdkTestObj.executeTestCase(expectedResult)
    actualresult = tdkTestObj.getResult()
    output = tdkTestObj.getResultDetails()
    if expectedResult in actualresult.upper() and "rialto_test" not in output :
        print "Rebooting the device......."
        obj.initiateReboot();
        Status="SUCCESS"
    else:
        print "Unable to delete rialto_test environment file"
        Status="FAILURE"
    tdkTestObj.setResultStatus(Status);
    print "TEST STEP STATUS :",Status
    print "#--------- [Post-requisite Status] : %s  ----------#"%(Status)
    print "Plugin Post-requisite Status:",Status

#Function to execute the testcase passed as argument
def ExecuteTest(obj,streamType,test,command):
    expectedResult="SUCCESS"
    global testCase
    if "rialto_playback" in test:
        description = "Validate generic playback for %s codec"%(streamType)
        test="Generic Playback Test"
    elif "rialto_play_pause" in test:
        description = "Perform Play-Pause operation for %s codec"%(streamType)
        test="Play Pause Operation Test"
    print "\n#==============================================================================#"
    print "TEST CASE NAME   : %s %s"%(streamType,test)
    print "TEST CASE ID  : RIALTO_",testCase
    print "DESCRIPTION   : ",description
    print "#==============================================================================#\n"
    tdkTestObj = obj.createTestStep('ExecuteCommand');
    tdkTestObj.addParameter("command", command)
    print "\nExecuting command in DUT: ", command
    tdkTestObj.executeTestCase(expectedResult)
    actualresult = tdkTestObj.getResult()
    output = tdkTestObj.getResultDetails().replace(r'\n', '\n'); output = output[output.find('\n'):]
    print "OUTPUT: ...\n", output

    #Check if the command executed successfully
    if expectedResult in actualresult.upper() and output:
        #Check the output string returned from 'mediapipelinetests' to verify if the test suite executed successfully
        executionStatus = checkMediaPipelineTestStatus (output)

        if expectedResult in executionStatus:
            Status="SUCCESS"
            print "Rialto %s for %s codec using 'playbin', 'rialtomsevideosink' and 'rialtomseaudiosink' was successfull"%(test,streamType)
            print "Mediapipeline test executed successfully\n"
        else:
            Status="FAILURE"
            print "Rialto %s for %s codec using 'playbin', 'rialtomsevideosink' and 'rialtomseaudiosink' failed\n"%(test,streamType)
    else:
        Status="FAILURE"
        print "Mediapipeline test execution failed"

    tdkTestObj.setResultStatus(Status)
    print "\nTEST STEP STATUS :  ",Status
    print "\n##--------- [TEST EXECUTION STATUS] : %s ----------##\n\n"%(Status)
    testCase=testCase+1

#Function to retrieve the device configuration from device config file
def getConfigValue (tdklibObj, configKey):
    try:
        global check_fps
        global ignore_warnings
        result = "SUCCESS"
        #Retrieve the device details(device name) and device type from tdk library
        configValue = ""
        deviceDetails = tdklibObj.getDeviceDetails()
        deviceType = tdklibObj.getDeviceBoxType()
        #Construct the RialtoModuleConfig path in TM
        configPath = tdklibObj.realpath+ "/" + "fileStore/RialtoModuleConfig"
        #Construct the device configuration file path
        #The device configuration file can be either <device-name>.config or <box-type>.config, so we are checking for both
        deviceNameConfigFile = configPath + "/" + deviceDetails["devicename"] + ".config"
        deviceTypeConfigFile = configPath + "/" + deviceType + ".config"
        # Check whether device / platform config files are present
        if os.path.exists (deviceNameConfigFile) == True:
            deviceConfigFile = deviceNameConfigFile
        elif os.path.exists (deviceTypeConfigFile) == True:
            deviceConfigFile = deviceTypeConfigFile
        else:
            print "FAILURE : No Device config file found : " + deviceNameConfigFile + " or " + deviceTypeConfigFile
            result = "FAILURE"
        #Continue only if the device config file exists
        if (len (deviceConfigFile) != 0):
            configParser = ConfigParser.ConfigParser()
            configParser.read(r'%s' % deviceConfigFile)
            #Retrieve the value of config key from device config file
            configValue = configParser.get('device.config', configKey)
            if True:
                ignore_warnings = configParser.get('device.config',"IGNORE_WARNINGS")
            else:
                ignore_warnings = "no"
            try:
                check_fps = configParser.get('device.config',"CHECK_FPS")
            except:
                check_fps = "no"
        else:
            print "DeviceConfig file not available"
            result = "FAILURE"
    except Exception as e:
        print "Exception occurred while retrieving device configuration  : " + str(e)
        result = "FAILURE"
    return result, configValue

#Function to construct the mediapipelinetest command to be executed in the DUT
def getMediaPipelineTestCommand (testName, testUrl, **arguments):
    #First construct the command with mandatory arguments
    command = "mediapipelinetests " + testName + " " + testUrl
    #Based on the test, the arguments can vary, parse through the variabled arguments
    #and add the available variables
    for name, value in arguments.items ():
        command += " " + name + "=" + value
    #Feature to disable video-fps check
    if (check_fps == "no") and "fps" not in command.lower():
        command = command + " checkFPS=no "
    if (ignore_warnings == "yes"):
        #Update GST_LOG_LEVEL to skip error statements check
        command = "export GST_LOG_LEVEL=0;  " + command;
    return command
