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
import vts_failure_analyzer
import urllib.request
import socket

# Cache for HPK RELEASE.md content keyed by HPK version tag.
_hpk_release_cache = {}

def _urlopen_github(url, timeout=10):
    """urllib.request.urlopen for github.com / raw.githubusercontent.com.
    Any credentials required for private repos are expected to be provided
    via the user's ~/.netrc file.
    """
    return urllib.request.urlopen(urllib.request.Request(url), timeout=timeout)

def _urlretrieve_github(url, dest_path):
    """Download url to dest_path.
    Any credentials required for private repos are expected to be provided
    via the user's ~/.netrc file.
    """
    with urllib.request.urlopen(urllib.request.Request(url), timeout=30) as resp, open(dest_path, "wb") as f:
        f.write(resp.read())

def _resolve_hal_test_version_from_hpk(hpk_version, component):
    """Fetch RELEASE.md from rdk-hpk-documentation at hpk_version and extract
    the HAL Testing version for *component* (e.g. 'Device Settings').
    Mirrors the logic of get_hal_test_version() in vts_compile.sh.
    Returns the version string, or None on any failure.
    """
    global _hpk_release_cache
    if hpk_version not in _hpk_release_cache:
        url = "https://raw.githubusercontent.com/rdkcentral/rdk-hpk-documentation/{}/RELEASE.md".format(hpk_version)
        try:
            with _urlopen_github(url, timeout=10) as resp:
                _hpk_release_cache[hpk_version] = resp.read().decode("utf-8", errors="replace")
            print("[HPK] Fetched RELEASE.md for " + hpk_version)
        except Exception as e:
            print("WARNING: Could not fetch HPK RELEASE.md from " + url + " : " + str(e))
            _hpk_release_cache[hpk_version] = ""
    release_md = _hpk_release_cache[hpk_version]
    if not release_md:
        return None
    # Find the row containing [<component>] (case-insensitive)
    row = None
    for line in release_md.splitlines():
        if "[" + component + "]" in line or "[" + component.lower() + "]" in line.lower():
            row = line
            break
    if not row:
        return None
    # Column 7 in a pipe-delimited Markdown table (1-indexed, leading | counts as field 1).
    cols = row.split("|")
    if len(cols) < 7:
        return None
    cell = cols[6]  # 0-indexed: field 7 = index 6
    # Extract first backtick-quoted token
    m = re.search(r"`([^`]+)`", cell)
    if m and m.group(1).strip() and m.group(1).strip() != "No change":
        return m.group(1).strip()
    # Fallback: extract version from tree/blob URL on the same row
    m2 = re.search(r"rdk[a-z-]*-halif-test-[^/]+/(?:tree|blob)/([^)\s]+)", row)
    if m2:
        return m2.group(1).strip()
    return None

#Global variables
failed_testCases = []
configYAMLData = ""
total_yaml_fetch_time = 0.0
total_analysis_time = 0.0
sshPort = 22
sshParams = []
deviceIP = ""

# Directory containing HAL test source files (used by failure analyzer).
# by default points at the VTS_Source tree produced by vts_compile.sh.
VTS_SOURCE_DIR = ""

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
#              - plugin_name : test module executed
# Return:
#              - List of failed test cases.
#---------------------------------------------------------------------
def printTestSummary(testData, plugin_name):
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

    # Calculate plugin-level summary
    total_tests = len(testData)
    executed_tests = 0
    passed_tests = 0
    failed_tests = 0
    na_tests = 0
    plugin_data_max_length = 71

    for test_name, test_values in testData.items():
        # test_values format: [TotalAsserts, Ran, Passed, Failed, Inactive]
        if len(test_values) >= 4:
            ran = test_values[1]
            passed = test_values[2]
            failed = test_values[3]

            # Count executed tests (Ran > 0)
            if ran > 0:
                executed_tests += 1

            # Count passed tests (Failed == 0 and Ran > 0)
            if ran > 0 and failed == 0:
                passed_tests += 1

            # Count failed tests (Failed > 0)
            if failed > 0:
                failed_tests += 1

    # Calculate N/A tests (not executed)
    na_tests = total_tests - executed_tests

    # Determine final status
    if failed_tests > 0:
        final_status = "FAILURE"
    elif executed_tests == 0:
        final_status = "NOT EXECUTED"
    elif passed_tests == executed_tests:
        final_status = "SUCCESS"
    else:
        final_status = "PARTIAL SUCCESS"

    # Print plugin-level summary
    print("\n" + "=" * plugin_data_max_length)
    print("PLUGIN TEST SUMMARY".center(plugin_data_max_length))
    print("=" * plugin_data_max_length)
    print(f"PLUGIN NAME    :  {plugin_name}")
    print(f"TOTAL TESTS    :  {total_tests}")
    print(f"EXECUTED TESTS :  {executed_tests}")
    print(f"PASSED TESTS   :  {passed_tests}")
    print(f"FAILED TESTS   :  {failed_tests}")
    print(f"N/A TESTS      :  {na_tests}")
    print()
    print(f"Final Plugin Tests Status: {final_status}")
    print("=" * plugin_data_max_length)
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
#              - port: SSH port.
# Return:
#              - Tuple: (SSH client object, session object)
#-------------------------------------------------------------------
def startSession(hostname, username, password, port):
    output = ""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password, port=port)
        session = client.invoke_shell()
        print("Created ssh session")
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
        print("No session to close");
    else:
        print("Closing session")
        session.close()
        client.close()

#-------------------------------------------------------------------
# Function:    executeSingleCommand
# Description: Opens an SSH session, executes a single command on
#              the DUT, captures the output, and closes the session.
# Parameters:
#              - hostname: IP of the device.
#              - username: SSH username.
#              - password: SSH password.
#              - command: The command to execute on the DUT.
#              - port: SSH port (default: 22).
# Return:
#              - str: Output of the executed command, or None on failure.
#-------------------------------------------------------------------
def executeSingleCommand(hostname, username, password, command, port=22):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password, port=int(port))
        print("Created ssh session")
        _stdin, stdout, _stderr = client.exec_command(command, timeout=15)
        output = stdout.read().decode('utf-8', errors='ignore')
        print("Executed command")
        client.close()
        print("Closing session")
        return output
    except Exception as e:
        print("Exception occurred while executing command : ", e)
        return None

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
    try:
        from VTSTestVariables import DEFAULT_TESTCASE_TIMEOUT as defaultRunTime
    except Exception:
        defaultRunTime = 30
    maxCommandRunTime = defaultRunTime
    global longWait
    if longWait:
       maxCommandRunTime = 50
    if runTime:
       maxCommandRunTime = runTime
       print("Running time changed to ",runTime)
    numberOfCommands = len(commands)
    if session is None:
        print("\nERROR: No SSH session to execute commands found")
        return "No SSH session"
    commandIterator = 1
    for command in commands:
        if "hal" in command:
            print("Executing command : ",command)
        commandStartTime = time.time()
        try:
            session.send(command + "\n")
            time.sleep(1)  # Initial wait for the command to start executing
            output = ""
            last_data_time = time.time()
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
                        data = session.recv(1024).decode('utf-8',errors='ignore')
                        output += data
                        last_data_time = time.time()
                    else:
                        # For intermediate commands, break early after 3s idle
                        # For the last command, wait the full maxCommandRunTime
                        if commandIterator < numberOfCommands and time.time() - last_data_time > 3:
                            break
                        time.sleep(0.1)
                if "Enter command:" in output:  # Check if command has completed
                    break
                if session.exit_status_ready() and maxCommandRunTime == defaultRunTime:
                    break
                if ("Segmentation fault" in output) or ("symbol lookup error" in output) or ("core dumped" in output):
                    break
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
        global longWait
        print("Setting longWait to true")
        longWait = True

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
#              - binaryConfig: (Optional) Config file passed to the binary with -p flag.
# Return:
#              - dict: Execution summary of test cases.
#--------------------------------------------------------------------------------------
def runTest(binaryPath, module, testCaseID, testList, TestCaseList=[], SkipTestCaseList={}, binaryConfig=""):
    global session
    global client
    global failed_testCases
    global skipped_testCases
    global sshPort
    global sshParams
    global deviceIP
    testIterator=1
    executionSummary={}
    errorObserved = False
    TestToBeExecuted = []
    skipped_testCases=[]
    runTime=0
    binaryPathWithConfig = binaryPath + " -p " + binaryConfig if binaryConfig else binaryPath
    if TestCaseList:
        for test in testList.keys():
            for testFromList in TestCaseList:
                if testFromList in test:
                    TestToBeExecuted.append(test)
    else:
        TestToBeExecuted = testList.keys()
    for test in TestToBeExecuted:
        skipped = False
        skipped_reason = ""
        if errorObserved:
            try:
                sshParams = getDeviceConfigValues("SSHParams").split()
                sshPort = getDeviceConfigValues("SSH_PORT")
                print("Attempting to re-establish SSH session...")
                client, session = startSession(deviceIP, sshParams[0].strip(), sshParams[1].strip(), sshPort)
            except Exception as reconnect_e:
                print("Failed to re-establish session:", reconnect_e)
            if session:
                startBinary(session, binaryPathWithConfig, module)
            errorObserved = False
        testname = test
        print("\n#==============================================================================#")
        print("TEST CASE NAME   : %s"%(testname.split(".")[1].strip()))
        print("TEST CASE ID  : %s-%s"%(testCaseID,testname.split(".")[0].strip()))
        print("#==============================================================================#\n")
        if SkipTestCaseList:
            for skipTestCase in list(SkipTestCaseList.keys()):
                if skipTestCase in test:
                   print("SKIPPING TESTCASE: ",testname)
                   print("REASON : ", SkipTestCaseList[test.split(".")[1].strip()])
                   skipped_reason = SkipTestCaseList[test.split(".")[1].strip()]
                   output = "TESTCASE SKIPPED"
                   SkipTestCaseList.pop(skipTestCase,None)
                   skipped = True
                   skipped_testCases.append(test.split(".")[1].strip())
        if not skipped:    
            print("Executing ",test)
            testIterator=test.split('.')[0].strip()
            print("Test Iterator = ",testIterator)
            commands = [ "S", str(testIterator) ];
            if "l2_rmf_primary_data_check" in test or "PLAT_SetDeepSleep_pos" in test or "SetDsAndVerifyWakeup" in test:
                runTime=100
            if "dsGetDisplay_L1" in test or "dsGetDisplayAspectRatio_L1" in test or "dsGetDisplayAspectRatio_L1_" in test:
                runTime=30
            output = executeCommands(session,commands,runTime);
            if output is None:
                print("ERROR: Command execution failed (socket may be closed). Attempting to re-establish SSH session...")
                stopSession(client, session)
                time.sleep(3)
                try:
                    client, session = startSession(deviceIP, sshParams[0].strip(), sshParams[1].strip(), sshPort)
                except Exception as reconnect_e:
                    print("Failed to re-establish session:", reconnect_e)
                    session = None
                if session:
                    startBinary(session, binaryPathWithConfig, module)
                    print("Re-running test case : ", test)
                    output = executeCommands(session, commands, runTime)
                    if output is None:
                        print("ERROR: Command execution failed again after re-establishing session. Marking test as FAILURE.")
                        output = "TESTCASE FAILURE"
                        errorObserved = True
                    else:
                        print("Re-run successful")
                else:
                    print("ERROR: Failed to re-establish SSH session. Marking test as FAILURE.")
                    output = "TESTCASE FAILURE"
                    errorObserved = True
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
                        print("Unable to parse result — restarting SSH session...")
                        stopSession(client, session)
                        time.sleep(3)
                        try:
                            client, session = startSession(deviceIP, sshParams[0].strip(), sshParams[1].strip(), sshPort)
                            if session:
                                startBinary(session, binaryPathWithConfig, module)
                                print("SSH session restarted successfully")
                        except Exception as reconnect_e:
                            print("Failed to re-establish session:", reconnect_e)
                            session = None
                        setFailure = True
                    else:
                        print("\n%s -> %s"%(test,testResult))
                except Exception as e:
                    print ("Device not accessible or unknown failure occurred")
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
            global configYAMLData
            global total_yaml_fetch_time
            global total_analysis_time
            try:
                from VTSTestVariables import FAILURE_ANALYSIS
                failure_analysis_enabled = str(FAILURE_ANALYSIS).strip().lower() == "yes"
            except Exception:
                failure_analysis_enabled = True
            if testResult["failed"] != 0:
                print("FAILURE : Observed Failure in ",testname.split(".")[1].strip())
                if not configYAMLData and binaryConfig and failure_analysis_enabled:
                    try:
                        configBasePath = binaryPath.split(';')[0].replace('cd', '').strip().rstrip('/') + "/"
                        configFilePath = configBasePath + binaryConfig
                        yaml_fetch_start = time.time()
                        configYAMLData = executeSingleCommand(deviceIP, sshParams[0].strip(), sshParams[1].strip(), "cat " + configFilePath, sshPort) or ""
                        elapsed_yaml = time.time() - yaml_fetch_start
                        total_yaml_fetch_time += elapsed_yaml
                        print("Config YAML fetch time : %.2f seconds" % elapsed_yaml)
                    except Exception as e:
                        print("WARNING: Unable to fetch config YAML for failure analysis:", e)
                        configYAMLData = ""
                if failure_analysis_enabled:
                    try:
                        ansi_re = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
                        clean_output = ansi_re.sub('', output) if isinstance(output, str) else output

                        # Detect segfault / core dump / symbol error early — no CUnit assertion will
                        # be present in the log so the analyzer cannot run.
                        _crash_cause = None
                        if "Segmentation fault" in clean_output:
                            _crash_cause = "Segmentation fault"
                        elif "core dumped" in clean_output:
                            _crash_cause = "Core dumped"
                        elif "symbol lookup error" in clean_output:
                            _crash_cause = "Symbol lookup error"
                        if _crash_cause:
                            remarks_line = "#==============================[REMARKS]=======================================#"
                            print(remarks_line)
                            if _crash_cause == "Symbol lookup error":
                                # Extract the exact undefined symbol name from the error line.
                                _sym_m = re.search(r'undefined symbol:\s*(\S+)', clean_output)
                                if _sym_m:
                                    print(_sym_m.group(1) + " - Symbol lookup error")
                                else:
                                    _fn_m = re.search(r'\bIn\s+(\w+)\s*\[', clean_output)
                                    _fn_name = _fn_m.group(1) if _fn_m else "the test function"
                                    print("Symbol lookup error occurred while invoking " + _fn_name)
                            else:
                                _fn_m = re.search(r'\bIn\s+(\w+)\s*\[', clean_output)
                                _fn_name = _fn_m.group(1) if _fn_m else "the test function"
                                print(_crash_cause + " occurred while invoking " + _fn_name)
                            print(remarks_line)
                            raise RuntimeError(_crash_cause + " detected — skipping analyzer")

                        clean_configYAMLData = ansi_re.sub('', configYAMLData) if isinstance(configYAMLData, str) else configYAMLData
                        # Strip SSH shell prompt lines (e.g. "root@host:~# cat ...") from YAML
                        clean_configYAMLData = "\n".join(
                            line for line in clean_configYAMLData.splitlines()
                            if not re.match(r'^\s*\w+@[\w\-]+[:#]', line)
                        )
                        analysis_start = time.time()
                        global VTS_SOURCE_DIR
                        global libObj
                        # Extract the failing C source filename from the log.
                        try:
                            source_file, *_ = vts_failure_analyzer.parse_log(clean_output)
                        except BaseException:
                            source_file = None
                        if source_file:
                            # Resolve required repo + version first (needed for cache validation).
                            sf_lower = source_file.lower()
                            try:
                                from VTSTestVariables import HPK_VERSION as _hpk_ver
                            except Exception:
                                _hpk_ver = ""
                            def _ver(override, component):
                                if override:
                                    return override
                                if _hpk_ver:
                                    derived = _resolve_hal_test_version_from_hpk(_hpk_ver, component)
                                    if derived:
                                        print("[HPK] Resolved {} test version: {}".format(component, derived))
                                        return derived
                                return "main"
                            if "deepsleep" in sf_lower:
                                haltest_repo = "rdk-halif-test-deepsleep_manager"
                                try:
                                    from VTSTestVariables import DEEPSLEEP_HAL_TEST_VERSION_OVERRIDE as _ov
                                except Exception:
                                    _ov = ""
                                haltest_version = _ver(_ov, "Deep Sleep Manager")
                            elif "plat_power" in sf_lower or "power" in sf_lower:
                                haltest_repo = "rdk-halif-test-power_manager"
                                try:
                                    from VTSTestVariables import POWER_HAL_TEST_VERSION_OVERRIDE as _ov
                                except Exception:
                                    _ov = ""
                                haltest_version = _ver(_ov, "Power Manager")
                            elif "hdmi_cec" in sf_lower or "rcechal" in sf_lower or "cec" in sf_lower:
                                haltest_repo = "rdk-halif-test-hdmi_cec"
                                try:
                                    from VTSTestVariables import HDMICEC_HAL_TEST_VERSION_OVERRIDE as _ov
                                except Exception:
                                    _ov = ""
                                haltest_version = _ver(_ov, "HDMI CEC")
                            elif "rmf" in sf_lower:
                                haltest_repo = "rdk-halif-test-rmf_audio_capture"
                                try:
                                    from VTSTestVariables import RMF_AUDIO_CAPTURE_HAL_TEST_VERSION_OVERRIDE as _ov
                                except Exception:
                                    _ov = ""
                                haltest_version = _ver(_ov, "RMF Audio Capture")
                            else:
                                haltest_repo = "rdk-halif-test-device_settings"
                                try:
                                    from VTSTestVariables import DS_HAL_TEST_VERSION_OVERRIDE as _ov
                                except Exception:
                                    _ov = ""
                                haltest_version = _ver(_ov, "Device Settings")

                            local_cache_dir = libObj.realpath + "fileStore/VTSFailureAnalysisSource/"
                            os.makedirs(local_cache_dir, exist_ok=True)
                            manifest_path = os.path.join(local_cache_dir, "source_versions.json")

                            # Load existing version manifest.
                            try:
                                import json as _json
                                with open(manifest_path, "r") as _mf:
                                    _version_manifest = _json.load(_mf)
                            except Exception:
                                _version_manifest = {}

                            dest_path = os.path.join(local_cache_dir, source_file)
                            cached_version = _version_manifest.get(source_file, "")
                            need_download = (
                                not os.path.isfile(dest_path) or
                                cached_version != haltest_version
                            )
                            source_ready = False
                            if not need_download:
                                print("[Cache] Using cached {} (version {})".format(source_file, cached_version))
                                source_ready = True
                            else:
                                if os.path.isfile(dest_path) and cached_version != haltest_version:
                                    print("[Cache] Version mismatch for {} (cached: {}, required: {}) — re-downloading".format(
                                        source_file, cached_version, haltest_version))
                                source_url = "https://raw.githubusercontent.com/rdkcentral/{}/{}/src/{}".format(
                                    haltest_repo, haltest_version, source_file
                                )
                                try:
                                    print("Downloading source for analysis: " + source_url)
                                    _urlretrieve_github(source_url, dest_path)
                                    print("Downloaded " + source_file + " (version {}) to local cache".format(haltest_version))
                                    _version_manifest[source_file] = haltest_version
                                    with open(manifest_path, "w") as _mf:
                                        import json as _json
                                        _json.dump(_version_manifest, _mf, indent=2)
                                    source_ready = True
                                except Exception as dl_e:
                                    print("WARNING: Could not download source for analysis — skipping failure analysis:", dl_e)
                                    if haltest_version == "main":
                                        print("HINT: Version resolution fell back to 'main' because HPK_VERSION tag '{}' was not found".format(_hpk_ver or "(not set)"))
                                        print("      Set DS_HAL_TEST_VERSION_OVERRIDE (or the relevant module override) in VTSTestVariables.py to a valid tag, e.g. '6.0.1'")

                            if not source_ready:
                                raise RuntimeError("Source file unavailable for failure analysis")

                            # Also check VTS_SOURCE_DIR (compile-time tree) before overriding.
                            if VTS_SOURCE_DIR:
                                for _root, _dirs, _fnames in os.walk(VTS_SOURCE_DIR):
                                    if source_file in _fnames:
                                        break  # use existing VTS_SOURCE_DIR as-is
                                else:
                                    VTS_SOURCE_DIR = local_cache_dir
                            else:
                                VTS_SOURCE_DIR = local_cache_dir

                        # Guard: if the log contains no ASSERT/FAIL line (e.g. the
                        # device entered deep sleep and never returned CUnit output),
                        # skip the analyzer and print a specific diagnostic instead.
                        _failure_re = re.compile(
                            r",\s*(ASSERT|FAIL)\s*,\s*[\w./\\-]+\.c\s*,\s*\d+\s*:",
                            re.IGNORECASE,
                        )
                        if not _failure_re.search(clean_output):
                            remarks_line = "#==============================[REMARKS]=======================================#"
                            print(remarks_line)
                            print("Device not accessible or unknown failure occurred")
                            print(remarks_line)
                            raise RuntimeError("No ASSERT/FAIL line in output — skipping analyzer")

                        failure_flow, full_failurelog = vts_failure_analyzer.analyze_failure(VTS_SOURCE_DIR, clean_output, clean_configYAMLData)
                        elapsed_analysis = time.time() - analysis_start
                        total_analysis_time += elapsed_analysis
                        print("Failure analysis time  : %.2f seconds" % elapsed_analysis)
                        if failure_flow:
                            remarks_line = "#==============================[REMARKS]=======================================#"
                            print(remarks_line)
                            print(failure_flow)
                            print(remarks_line)
                    except BaseException as e:
                        print("WARNING: Failure analysis could not be completed:", e)
                failed_testCases.append(test.split(".")[1].strip())
            else:
                print("SUCCESS : %s executed successfully without any failures"%(testname.split(".")[1].strip()))
                status="SUCCESS"
            print("TEST STEP STATUS :  ",status)
            print("#" * 80)
        else:
            status="SKIPPED"
            if "RPI doesn't support" in skipped_reason or "Not applicable for RPI" in skipped_reason:
                status = "N/A"
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
        if configuredPath:
            print("configuredPath : ", configuredPath)
            moduleName = os.path.basename(os.path.normpath(basePath)) + "/"
            basePath = configuredPath + moduleName
            print("basePath : ", basePath)
        else:
            print("Using default basePath :  ", basePath)
    except:
        print("Using default basePath :  ", basePath)

    binaryPath = "cd " + basePath + " ; ./" + binaryName
    if binaryConfig:
        binaryPath = binaryPath + " -p " + binaryConfig
    print("\n\n#---------------------------- Plugin Pre-requisite ----------------------------#")
    print("\nPre Requisite : Setting_up_VTS_binary\nPre Requisite No : 1")
    try:
        sshPort = getDeviceConfigValues("SSH_PORT")
        client,session = startSession(host,username,password,sshPort)
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
    global total_yaml_fetch_time
    global total_analysis_time
    if total_yaml_fetch_time > 0.0 or total_analysis_time > 0.0:
        print("\n[FAILURE ANALYSIS TIMING SUMMARY]")
        print("  Total config YAML fetch time : %.2f seconds" % total_yaml_fetch_time)
        print("  Total failure analysis time  : %.2f seconds" % total_analysis_time)
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
