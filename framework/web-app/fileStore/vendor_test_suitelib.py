##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
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
import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')
import paramiko
import time
import re
import os
import SSHUtility
import configparser
import json
import sys

#Global variables
failed_testCases = []
#----------------------------------------------------------------------------------------------------------------
# "longWait" can be set to True for certain Test Suites where API has high response time
#  This high response time causes test to run for a longer duration than expected time
#  Even though this is an issue from HAL side, framework must execute and capture the test logs.
#  Whenever "longWait" is set to True and the test suite is run, tester must also analyse why this was necessary
#  and what API is causing this issue and report it as an issue.
#----------------------------------------------------------------------------------------------------------------
longWait = False

#-------------------------------------------------------------------------
# Function:    init_module
# Description: Initializes the module by setting device and library
#              parameters required for testing.
# Parameters:
#              - libobj: Library object containing device details.
#              - port: Port number for communication.
#              - deviceInfo: Dictionary containing device details such as
#                            device name, type, and MAC address.
# Return:
#              - None
#--------------------------------------------------------------------------
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

#-------------------------------------------------------------------------
# Function:    parseTestList
# Description: Parses and extracts test cases from the given output,
#              handling cases where test names span multiple lines.
# Parameters:
#              - output: The string output containing the list of tests.
# Return:
#              - dict: Dictionary containing test names as keys and their
#                      active status as values.
#-------------------------------------------------------------------------
def parseTestList(output):
    """Parses test list from output, handling truncated names across multiple lines."""
    testList = {}
    lines = [line for line in output.splitlines() if line.strip() and not line.startswith("----")]
    start_parsing = False
    current_test = ""
    for line in lines:
        line = line.strip()
        # Ignore empty lines
        if not line.strip():
            continue
        # Start parsing after the header
        if "Test Name" in line:
            start_parsing = True
            continue
        # Stop parsing when reaching the total count
        if "Total Number of Tests" in line:
            if current_test:
                # Add last buffered test
                parts = current_test.rsplit(" ", 1)
                if len(parts) == 2:
                    testList[parts[0].strip()] = parts[1].strip()
            break
        if start_parsing:
            # If the line has both test name and status
            if re.match(r"^\d+\.\s+.+\s+(Yes|No)$", line):
                if current_test:
                    # Store the previous test before starting a new one
                    parts = current_test.rsplit(" ", 1)
                    if len(parts) == 2:
                        testName = parts[0].strip()
                        testName = testName.split(".")[1]
                        testList[parts[0].strip()] = parts[1].strip()
                current_test = line  # Start new test
            else:
                # Append truncated part to previous line
                current_test += " " + line
    return testList

#------------------------------------------------------------------------
# Function:    parseAsserts
# Description: Extracts assertion results from test output and
#              formats them into a structured dictionary.
# Parameters:
#              - output: The output string containing assertion details.
# Return:
#              - dict: Dictionary containing total, ran, passed, failed,
#                      and inactive assertions.
#------------------------------------------------------------------------
def parseAsserts(output):
    """Parses the asserts summary from the output and returns a dictionary."""
    pattern = re.search(r"asserts\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\S+)", output)
    if pattern:
        try:
            total, ran, passed, failed, inactive = pattern.groups()
            return {
                   "total": int(total),
                   "ran": int(ran),
                   "passed": int(passed),
                   "failed": int(failed),
                   "inactive": inactive  # Keep "n/a" as string
            }
        except:
            return {}
    else:
        return {}  # Return empty dictionary if pattern is not found

#---------------------------------------------------------------------
# Function:    printTestSummary
# Description: Displays the summary of test execution results in a
#              formatted tabular structure.
# Parameters:
#              - testData: Dictionary containing test execution data.
# Return:
#              - List of failed test cases.
#---------------------------------------------------------------------
def printTestSummary(testData):
    """Prints the test summary in a tabular column format."""
    global failed_testCases
    # Define column headers
    headers = ["Test", "TotalAsserts", "Ran", "Passed", "Failed", "Inactive"]
    # Ensure each row includes the test name as the first column
    rows = [[test] + values for test, values in testData.items()]
    # Calculate column widths dynamically
    colWidths = [max(len(str(row[i])) for row in [headers] + rows) for i in range(len(headers))]
    # Print Header
    print("\nTest Summary:")
    print("-" * (sum(colWidths) + len(headers) - 1))  # Adjust separator width
    print("  ".join(headers[i].ljust(colWidths[i]) for i in range(len(headers))))
    print("-" * (sum(colWidths) + len(headers) - 1))
    # Print each test result
    for row in rows:
        print("  ".join(str(row[i]).ljust(colWidths[i]) for i in range(len(headers))))
    print("-" * (sum(colWidths) + len(headers) - 1))  # Final separator
    print("\n")
    return failed_testCases

#-------------------------------------------------------------------
# Function:    startSession
# Description: Establishes an SSH session with the DUT for remote
#              command execution.
# Parameters:
#              - hostname: IP of the device.
#              - username: SSH username.
#              - password: SSH password.
# Return:
#              - Tuple: (SSH client object, session object)
#-------------------------------------------------------------------
def startSession(hostname, username, password):
    output = ""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)
        session = client.invoke_shell()
        print("\nCreated ssh session")
        return client,session
    except Exception as e:
        print("Login to device failed")
        print(e)
        session = None
        client = None
        return client,session

#-------------------------------------------------------------------
# Function:    stopSession
# Description: Closes an active SSH session and releases resources.
# Parameters:
#              - client: SSH client object.
#              - session: SSH session object.
# Return:
#              - None
#-------------------------------------------------------------------
def stopSession(client,session):
    if session == None:
        print("\nNo session to close");
    else:
        print("\nClosing session")
        session.close()
        client.close()

#-------------------------------------------------------------------
# Function:    executeCommands
# Description: Executes a list of commands on the DUT via SSH and
#              captures the output.
# Parameters:
#              - session: SSH session object.
#              - commands: List of commands to execute.
#              - runTime: Optional timeout for command execution.
# Return:
#              - str: The output of the last executed command.
#-------------------------------------------------------------------
def executeCommands(session, commands, runTime=0):
    maxCommandRunTime = 10
    global longWait
    if longWait:
        defaultRunTime=30
    else:
        defaultRunTime=10
    maxCommandRunTime = defaultRunTime
    if runTime:
       maxCommandRunTime = runTime
       print("Running time changed to ",runTime)
    numberOfCommands = len(commands)
    if session is None:
        print("\nERROR: No SSH session to execute commands found")
        return "No SSH session"
    commandIterator = 1
    last_data_time = time.time()
    for command in commands:
        if "hal" in command:
            print("Executing command : ",command)
        commandStartTime = time.time()
        try:
            session.send(command + "\n")
            time.sleep(1)  # Initial wait for the command to start executing
            output = ""
            while time.time() - commandStartTime < maxCommandRunTime:
                # Wait for command to finish by checking if the channel is closed
                if longWait:
                    if session.recv_ready():
                        data = session.recv(1024).decode('utf-8',errors='ignore')
                        output += data
                        last_data_time = time.time()
                    else:
                        # Check if we've received no data for a while
                        if time.time() - last_data_time > maxCommandRunTime:
                            break
                        time.sleep(0.1)
                else:
                    if session.recv_ready():
                        output += session.recv(1024).decode('utf-8',errors='ignore')
                if "Enter command:" in output:  # Check if command has completed
                    break
                if session.exit_status_ready() and maxCommandRunTime == defaultRunTime:
                    break
                if ("Segmentation fault" in output) or ("symbol lookup error" in output) or ("core dumped" in output):
                    break;
            if maxCommandRunTime != defaultRunTime:
                maxCommandRunTime = defaultRunTime
                print("Running time reverted to ",defaultRunTime)
            if commandIterator == numberOfCommands:
                return output
            commandIterator += 1
        except Exception as e:
            print("Exception occurred during command execution")
            print(e)
            return None

#------------------------------------------------------------------------
# Function:    getSuiteNumber
# Description: Extracts the suite number for a specific module from
#              test execution output.
# Parameters:
#              - output: Output string containing test execution details.
#              - module: Name of the module to find the suite number for.
# Return:
#              - int: The extracted suite number.
#------------------------------------------------------------------------
def getSuiteNumber(output, module):
    lines = [line for line in output.splitlines() if line.strip() and not line.startswith("----")]
    start_parsing = False
    suiteNumber = 0
    for line in lines:
        line = line.strip()
        # Ignore empty lines
        if not line.strip():
            continue
        if module in line:
            # Extract the number before the dot
            match = re.match(r"\s*(\d+)\.", line)
            if match:
                suiteNumber = int(match.group(1))
                print ("Suite Number : ",suiteNumber)
                break;
    return suiteNumber

#------------------------------------------------------------------------
# Function:    setupEnvironmentInSession
# Description: Executes /setup_environment.env if present in basePath
#              This sets up any pre-requisites required for module test
# Parameters:
#              - session : SSH session
#              - basePath : path where setup_environment.env can be found
# Return:
#              - NIL
#------------------------------------------------------------------------
def setupEnvironmentInSession(session,basePath):
    #Check if environment setup is present
    env_present = "ls " + basePath + "/setup_environment.env"
    print ("Checking if setup_environment.env is present")
    commands = [env_present]
    output = executeCommands(session,commands);
    if "No such file or directory" not in output:
        print ("setup_environment.env is present for device")
        source_command = "cd " + basePath + ";" + " source ./setup_environment.env"
        commands = [source_command]
        output = executeCommands(session,commands)
        print (output)
        print("Environment set successfully")

#-------------------------------------------------------------------
# Function:    startBinary
# Description: Launches the test binary on the DUT and retrieves
#              the available test suite number.
# Parameters:
#              - session: SSH session object.
#              - binaryPath: Path to the test binary.
#              - module: Name of the test module to execute.
# Return:
#              - str: Output from the binary execution.
#-------------------------------------------------------------------
def startBinary(session, binaryPath, module):
    commands = [ binaryPath , "L"]
    print("Starting Binary")
    output = executeCommands(session,commands);
    suiteNumber = getSuiteNumber(output, module)
    commands = [ "S", str(suiteNumber),"L"]
    output = executeCommands(session,commands);
    return output

#--------------------------------------------------------------------------------------
# Function:    runTest
# Description: Executes a list of test cases on the DUT.
# Parameters:
#              - binaryPath: Path to the test binary.
#              - module: Name of the module being tested.
#              - testCaseID: Unique test case identifier.
#              - testList: Dictionary of available test cases.
#              - TestCaseList: (Optional) List of specific test cases to run.
#              - SkipTestCaseList: (Optional) Dictionary of test cases to be skipped.
# Return:
#              - dict: Execution summary of test cases.
#--------------------------------------------------------------------------------------
def runTest(binaryPath, module, testCaseID, testList, TestCaseList=[], SkipTestCaseList={}):
    global session
    global failed_testCases
    global skipped_testCases
    testIterator=1
    executionSummary={}
    errorObserved = False
    TestToBeExecuted = []
    skipped_testCases=[]
    runTime=0
    if TestCaseList:
        for test in testList.keys():
            for testFromList in TestCaseList:
                if testFromList in test:
                    TestToBeExecuted.append(test)
    else:
        TestToBeExecuted = testList.keys()
    for test in TestToBeExecuted:
        skipped = False
        if errorObserved:
            startBinary(session, binaryPath, module)
            errorObserved = False
        print("\n#==============================================================================#")
        print("TEST CASE NAME   : %s"%(test.split(".")[1].strip()))
        print("TEST CASE ID  : %s-%s"%(testCaseID,test.split(".")[0].strip()))
        print("#==============================================================================#\n")
        if SkipTestCaseList:
            for skipTestCase in list(SkipTestCaseList.keys()):
                if skipTestCase in test:
                   print("SKIPPING TESTCASE: ",test)
                   print("REASON : ", SkipTestCaseList[test.split(".")[1].strip()])
                   output = "TESTCASE SKIPPED"
                   SkipTestCaseList.pop(skipTestCase,None)
                   skipped = True
                   skipped_testCases.append(test.split(".")[1].strip())
        if not skipped:    
            print("Executing ",test)
            testIterator=test.split('.')[0].strip()
            print("Test Iterator = ",testIterator)
            commands = [ "S", str(testIterator) ];
            if "PLAT_DS_SetDeepSleep_L1" in test or "L2_SetDeepSleepAndVerifyWakeUp10s" in test:
                print("Test Framework doesn't handle deepsleep scenario")
                print("Marking test as FAILURE , please execute manually and update result")
                output = "TESTCASE FAILURE"
            else:
                if "test_l2_rmfAudioCapture_primary_d" in test:
                    runTime=100
                if "dsGetDisplay_L1" in test or "dsGetDisplayAspectRatio_L1" in test or "dsGetDisplayAspectRatio_L1_" in test:
                    runTime=30
                output = executeCommands(session,commands,runTime);
        def escape_ansi(line):
            if isinstance(line, bytes):
                try:
                    line = line.decode("utf-8", errors="ignore")
                except UnicodeDecodeError as e:
                    print(f"Decode error: {e}")
                    line = ""  # fallback if decode fails even with ignore
            elif not isinstance(line, str):
                line = str(line)  # fallback for unexpected types
            ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
            print(ansi_escape.sub('', line))
        for line in output.splitlines():
            escape_ansi(line)
        testResult = {}
        if "TESTCASE FAILURE" in output:
            status="FAILURE"
        elif "TESTCASE SKIPPED" not in output:
            setFailure = False
            if ("Segmentation fault" in output) or ("symbol lookup error" in output) or ("core dumped" in output):
                print ("Marking test as Failure")
                setFailure = True
            else:
                try:
                    testResult = parseAsserts(output)
                    if testResult == {}:
                       raise KeyError
                    print("\n%s -> %s"%(test,testResult))
                except Exception as e:
                    print ("ERROR : Unable to parse Result\nMarking test as Failure")
                    setFailure = True
            if setFailure:
                testResult["total"] = 1
                testResult["ran"] = 1
                testResult["inactive"] = "n/a"
                testResult["passed"] = 0
                testResult["failed"] = 1
                errorObserved =  True
            testResultValues = [ testResult["total"], testResult["ran"], testResult["passed"], testResult["failed"], testResult["inactive"] ]
            executionSummary[test] = testResultValues;
            print("#" * 80)
            status="FAILURE"
            if testResult["failed"] != 0:
                print("FAILURE : Observed Failure in ",test)
                failed_testCases.append(test.split(".")[1].strip())
            else:
                print("SUCCESS : %s executed successfully without any failures"%(test))
                status="SUCCESS"
            print("TEST STEP STATUS :  ",status)
            print("#" * 80)
        else:
            status="SKIPPED"
        print("\n##--------- [TEST EXECUTION STATUS] : %s ----------##\n\n"%(status))
        testIterator = int(testIterator) + 1
    return executionSummary

#----------------------------------------------------------------------
# Function:    SetupPreRequisites
# Description: Sets up the necessary prerequisites before executing
#              the test cases, including starting an SSH session
#              and launching the test binary.
# Parameters:
#              - host: Device hostname/IP.
#              - username: SSH username.
#              - password: SSH password.
#              - basePath: Base path of test binaries.
#              - binaryName: Name of the test binary.
#              - binaryConfig: YAML configuration file for the binary.
#              - module: Module name for testing.
# Return:
#              - dict: Dictionary containing the list of test cases.
#----------------------------------------------------------------------
def SetupPreRequisites(host, username, password, basePath, binaryName, binaryConfig, module, setupEnvironment = False):
    global client
    global session
    try:
        configuredPath = getDeviceConfigValues("VTS_BASE_PATH")
        print("configuredPath : " ,configuredPath)
        moduleName = os.path.basename(os.path.normpath(basePath)) + "/"
        basePath = configuredPath + moduleName
        print("basePath : ", basePath)
    except:
        print("Using default basePath :  ", basePath)

    binaryPath = "cd " + basePath + " ; ./" + binaryName
    if binaryConfig:
        binaryPath = binaryPath + " -p " + binaryConfig
    print("\n\n#---------------------------- Plugin Pre-requisite ----------------------------#")
    print("\nPre Requisite : Setting_up_VTS_binary\nPre Requisite No : 1")
    try:
        client,session = startSession(host,username,password)
        if setupEnvironment:
            setupEnvironmentInSession(session,basePath)
        output = startBinary(session, binaryPath, module)
        testList = parseTestList(output)
        if not testList:
            print(output)
        print("\nTotal Number of tests : ",len(testList))
    except:
        print("\n#--------- [Pre-requisite Status] : FAILURE ----------#")
        print("Plugin Pre-requisite Status: FAILURE \n\n")
        return {}
    print("\n#--------- [Pre-requisite Status] : SUCCESS ----------#")
    print("Plugin Pre-requisite Status: SUCCESS \n\n")
    return testList

#-------------------------------------------------------------------
# Function:    executePostRequisites
# Description: Executes necessary post-test cleanup operations,
#              including terminating the test binary and closing
#              the SSH session.
# Parameters:
#              - None
# Return:
#              - None
#-------------------------------------------------------------------
def executePostRequisites():
    global session
    print("\n\n#---------------------------- Plugin Post-requisite ----------------------------#")
    print("\nPost Requisite :Exit_from_VTS_binary\nPost Requisite No : 1")
    executeCommands(session,["Q"])
    stopSession(client,session)
    print("\n#--------- [Post-requisite Status] : SUCCESS ----------#")
    print("Plugin Post-requisite Status: SUCCESS \n\n")

#----------------------------------------------------------------------------
# Function:    setVTSResult
# Description: Determines the overall result of the test execution
#              based on failed test cases.
# Parameters:
#              - failed_testCases: List of test cases that failed execution.
# Return:
#              - str: "SUCCESS" if all tests passed, otherwise "FAILURE".
#----------------------------------------------------------------------------
def setVTSResult(failed_testCases):
    if failed_testCases == "ERROR":
        print("\n[TEST EXECUTION RESULT] : FAILURE\n")
        return "FAILURE"
    global skipped_testCases
    if skipped_testCases:
        print("\nSKIPPED TESTCASES : ",skipped_testCases)
    if not failed_testCases:
        print("\n[TEST EXECUTION RESULT] : SUCCESS\n")
        print("SUCCESS : VTS Test Cases ran successfully")
        return "SUCCESS"
    else:
        print("\n\nFAILED TESTCASES LIST :",failed_testCases)
        print("\nNumber of Failed Testcases : ",len(failed_testCases))
        print("\n[TEST EXECUTION RESULT] : FAILURE\n")
        print("FAILURE : Failure observed in VTS Test Execution")
        return "FAILURE"

#------------------------------------------------------------------------------------
# Function:    getDeviceConfigValues
# Description: Retrieves device configuration values from the
#              specified device configuration file.
# Parameters:
#              - configKey: The configuration key whose value needs to be retrieved.
# Return:
#              - str: The value corresponding to the configuration key.
#------------------------------------------------------------------------------------
def getDeviceConfigValues (configKey):
    configValues = ""
    fetching_SSHParams = False
    if configKey == "SSHParams":
        configKeys = ["SSH_USERNAME", "SSH_PASSWORD"]
        fetching_SSHParams = True
    else:
        configKeys = [configKey]
    for configKey in configKeys:
        try:
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
                if "SSH" not in configKey:
                    return configValue
            else:
                print("DeviceConfig file not available")
                result = "FAILURE"
        except Exception as e:
            print("Exception occurred while retrieving device configuration  : " + e)
            result = "FAILURE"
        if configValue == "" and configKey != "SSH_USERNAME" and configKey != "SSH_PASSWORD":
            return result
        elif configValue == "" and configKey == "SSH_USERNAME":
            print ("\nERROR: SSH_USERNAME not configured in ", deviceConfigFile)
            sys.exit(1)
        elif configValue == "" and configKey == "SSH_PASSWORD":
            print ("\nERROR: SSH_PASSWORD not configured in ", deviceConfigFile)
            sys.exit(1)
        else:
            configValues = configValues + " " + configValue
    return str(configValues)
