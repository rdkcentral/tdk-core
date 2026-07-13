##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2026 RDK Management
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
from tdkutility import *
from tdkbRRDVariables import *

# checkRRDPrerequisites
# Syntax: checkRRDPrerequisites(tr181obj, sysobj, step, profile_type,logFile, debug_report_path)
# Description: Function to perform the prerequisite checks before starting the test execution
# Parameters: tr181obj - The TDK scripting library object for TR181 component
#            sysobj - The TDK scripting library object for sysutil component
#            step - The test step number
#            profile_type - The type of debug report (static or dynamic)
#            logFile - The RRD log file path
#            debug_report_path - The location where debug reports are generated
# Return Value: prereq_flag - Flag indicating whether the prerequisite checks were successful or not
#               revert_flag - Flag indicating whether the RDKRemoteDebugger Enable parameter value was modified and needs to be reverted or not
#               step - The updated test step number after performing the prerequisite checks


def checkRRDPrerequisites(tr181obj, sysobj, step, profile_type, logFile=rrd_log_file, debug_report_path=report_generation_location):
    prereq_flag = True
    revert_flag = False
    # Validate whether the value of RemoteDebugger Enable RFC is true, if not set it to true
    print("PREREQUISITE : Validate whether the value of RemoteDebugger Enable RFC is true, if not set it to true")
    tdkTestObj, get_flag, rrd_enable = getRDKRemoteDebuggerEnable(tr181obj, step)
    if get_flag:
        if rrd_enable == "false":
            print(f"RDKRemoteDebugger Enable is false, setting it to true for the test execution")
            step += 1
            revert_flag = setRDKRemoteDebuggerEnable(tr181obj, "true", step)
            if revert_flag:
                print(f"PREREQUISITE SUCCESS : Successfully set RDKRemoteDebugger Enable to true")
            else:
                prereq_flag = False
                print(f"PREREQUISITE FAILURE : Failed to set RDKRemoteDebugger Enable to true. Cannot proceed with the test execution")
        else:
            print(f"PREREQUISITE SUCCESS : RDKRemoteDebugger Enable is already true.")
    else:
        prereq_flag = False
        print(f"PREREQUISITE FAILURE : Failed to get the value of RDKRemoteDebugger Enable. Cannot proceed with the test execution")

    if prereq_flag:
        # Check if the RRD log file is present in the DUT
        step += 1
        print(f"\nPREREQUISITE : Checking if the RRD log file {logFile} is present in the DUT")
        tdkTestObj, file_flag = isRRDLogFilePresent(sysobj, step, logFile)
        if file_flag:
            print(f"PREREQUISITE SUCCESS : RRD log file {logFile} is present in the DUT")

            # Clear the RRD log file to ensure that the logs captured during the test execution are only related to the current test execution
            step += 1
            tdkTestObj, clear_flag = clearRRDLogFile(sysobj, step, logFile)
            if clear_flag:
                print(f"PREREQUISITE SUCCESS : Successfully cleared the RRD log file {logFile}")

                # Remove the existing debug reports in the report generation location before starting the test execution
                step += 1
                print(f"\nPREREQUISITE : Remove the existing debug reports in the report generation location {debug_report_path} before starting the test execution")
                tdkTestObj, remove_flag = removeDebugReports(sysobj, step, debug_report_path)
                if remove_flag:
                    print(f"PREREQUISITE SUCCESS : Successfully removed the existing debug reports in the report generation location {debug_report_path}")

                    # Remove the existing json profile if present before starting the test execution in case of dynamic profile
                    if profile_type == "dynamic":
                        step += 1
                        print(f"\nPREREQUISITE : Remove the existing {profile_type} json profile if present before starting the test execution")
                        tdkTestObj, remove_flag = removeJsonProfile(sysobj, profile_type, dynamic_json_file, step)
                        if remove_flag:
                            print(f"PREREQUISITE SUCCESS : Successfully removed the existing {profile_type} json profile if present")
                        else:
                            prereq_flag = False
                            print(f"PREREQUISITE FAILURE : Failed to remove the existing {profile_type} json profile")
                else:
                    prereq_flag = False
                    print(f"PREREQUISITE FAILURE : Failed to remove the existing debug reports in the report generation location {debug_report_path}")
            else:
                prereq_flag = False
                print(f"PREREQUISITE FAILURE : Failed to clear the RRD log file {logFile}")
        else:
            prereq_flag = False
            print(f"PREREQUISITE FAILURE : RRD log file {logFile} is not present in the DUT")
    return prereq_flag, revert_flag, step
############ End of function ##########

# isRRDLogFilePresent
# Syntax: isRRDLogFilePresent(obj, step, log_file)
# Description: Function to check whether the RRD log file is present in the DUT
# Parameters: obj - The TDK scripting library object for sysutil component
#             step - The test step number
#             log_file - The RRD log file path
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               file_flag - Flag indicating whether the RRD log file is present or not


def isRRDLogFilePresent(obj, step, log_file):
    expectedresult = "SUCCESS"
    file_flag = False
    print(f"\nTEST STEP {step} : Check whether the RRD log file {log_file} is present in the DUT")
    print(f"EXPECTED RESULT {step} : RRD log file {log_file} should be present in the DUT")
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = isFilePresent(tdkTestObj, log_file)
    if expectedresult in actualresult and details.strip() == log_file:
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step} : RRD log file {log_file} is present")
        file_flag = True
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step} : RRD log file {log_file} is not present. Details : {details}")
    return tdkTestObj, file_flag
############ End of function ##########

# clearRRDLogFile
# Syntax: clearRRDLogFile(obj, step, log_file)
# Description: Function to clear the RRD log file in the DUT
# Parameters: obj - The TDK scripting library object for sysutil component
#             step - The test step number
#             log_file - The RRD log file path
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               flag - Flag indicating whether the RRD log file is cleared successfully or not


def clearRRDLogFile(obj, step, log_file):
    expectedresult = "SUCCESS"
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    print(f"\nTEST STEP {step} : Clear the RRD log file {log_file} before starting the test execution")
    print(f"EXPECTED RESULT {step} : Should clear the RRD log file {log_file} successfully")
    command = f"cat /dev/null > {log_file}"
    print(f"Command : {command}")
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    if expectedresult in actualresult:
        print(f"ACTUAL RESULT {step} : Successfully cleared the RRD log file {log_file}. Details : {details}")
        tdkTestObj.setResultStatus("SUCCESS")
        flag = True
    else:
        print(f"ACTUAL RESULT {step} : Failed to clear the RRD log file {log_file}. Details : {details}")
        tdkTestObj.setResultStatus("FAILURE")
        flag = False
    return tdkTestObj, flag
########## End of function ##########


# removeDebugReports
# Syntax: removeDebugReports(obj, step, debug_report_location)
# Description: Function to remove the existing debug reports in the report generation location
# Parameters: obj - The TDK scripting library object for sysutil component
#             step - The test step number
#             debug_report_location - The location where debug reports are generated
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               flag - Flag indicating whether the debug reports were removed successfully or not


def removeDebugReports(obj, step, debug_report_location):
    expectedresult = "SUCCESS"
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    print(f"\nTEST STEP {step} : Remove the existing debug reports in the report generation location {debug_report_location} before starting the test execution")
    print(f"EXPECTED RESULT {step} : Should remove the existing debug reports in the report generation location {debug_report_location} successfully")
    command = f"rm -rf '{debug_report_location}'/*"
    print(f"Command : {command}")
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    if expectedresult in actualresult:
        print(f"ACTUAL RESULT {step} : Successfully removed the existing debug reports in the report generation location {debug_report_location}. Details : {details}")
        tdkTestObj.setResultStatus("SUCCESS")
        flag = True
    else:
        print(f"ACTUAL RESULT {step} : Failed to remove the existing debug reports in the report generation location {debug_report_location}. Details : {details}")
        tdkTestObj.setResultStatus("FAILURE")
        flag = False
    return tdkTestObj, flag
########## End of function ##########


# removeJsonProfile
# Syntax: removeJsonProfile(obj, profile_type, profile_path, step)
# Description: Function to remove the existing json profile if present before starting the test execution
# Parameters: obj - The TDK scripting library object for sysutil component
#             profile_type - The type of debug report (static or dynamic)
#             profile_path - The path where the json profile is present
#             step - The test step number
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               flag - Flag indicating whether the json profile was removed successfully or not


def removeJsonProfile(obj, profile_type, profile_path, step):
    expectedresult = "SUCCESS"
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    print(f"\nTEST STEP {step} : Remove the existing {profile_type} json profile at {profile_path} before starting the test execution")
    print(f"EXPECTED RESULT {step} : Should remove the existing {profile_type} json profile at {profile_path} successfully")
    command = f"rm -rf '{profile_path}'"
    print(f"Command : {command}")
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    if expectedresult in actualresult:
        print(f"ACTUAL RESULT {step} : Successfully removed the existing {profile_type} json profile at {profile_path}. Details : {details}")
        tdkTestObj.setResultStatus("SUCCESS")
        flag = True
    else:
        print(f"ACTUAL RESULT {step} : Failed to remove the existing {profile_type} json profile at {profile_path}. Details : {details}")
        tdkTestObj.setResultStatus("FAILURE")
        flag = False
    return tdkTestObj, flag

########## End of function ##########

# getRDKRemoteDebuggerIssueType
# Syntax: getRDKRemoteDebuggerIssueType(obj, step)
# Description: Function to get the value of RDKRemoteDebugger IssueType parameter using TR181 Get operation.
# Parameters: obj - The TDK scripting library object for TR181 component
#             step - The test step number
# Return Value: tdkTestObj - The TDK test object created for TR181 Get operation
#               get_flag - Flag indicating whether the TR181 Get operation was successful or not
#               value - The value of the RDKRemoteDebugger IssueType parameter


def getRDKRemoteDebuggerIssueType(obj, step):
    expectedresult = "SUCCESS"
    value = ""
    get_flag = False
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Get')
    print(f"\nTEST STEP {step} : Get the value of RDKRemoteDebugger IssueType")
    print(f"EXPECTED RESULT {step} : Should get the value of RDKRemoteDebugger IssueType")
    actualresult, value = getTR181Value(tdkTestObj, "Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.RDKRemoteDebugger.IssueType")
    if expectedresult in actualresult:
        get_flag = True
        print(f"ACTUAL RESULT {step} : Value of RDKRemoteDebugger IssueType is {value}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
    else:
        print(f"ACTUAL RESULT {step} : Failed to get the value of RDKRemoteDebugger IssueType")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return tdkTestObj, get_flag, value
########## End of function ##########

# setRDKRemoteDebuggerIssueType
# Syntax: setRDKRemoteDebuggerIssueType(obj, step, value)
# Description: Function to set the value of RDKRemoteDebugger IssueType parameter using TR181 Set operation.
# Parameters: obj - The TDK scripting library object for TR181 component
#             step - The test step number
#             value - The value to be set for RDKRemoteDebugger IssueType parameter
# Return Value: set_flag - Flag indicating whether the TR181 Set operation was successful or not


def setRDKRemoteDebuggerIssueType(obj, step, value):
    expectedresult = "SUCCESS"
    set_flag = False
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Set')
    print(f"\nTEST STEP {step} : Set the value of RDKRemoteDebugger IssueType as {value}")
    print(f"EXPECTED RESULT {step} : Should set the value of RDKRemoteDebugger IssueType as {value}")
    actualresult, details = setTR181Value(tdkTestObj, "Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.RDKRemoteDebugger.IssueType", value, "string")
    if expectedresult in actualresult and details != "":
        set_flag = True
        print(f"ACTUAL RESULT {step} : Successfully set the value of RDKRemoteDebugger IssueType to {value}. Details : {details}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
    else:
        print(f"ACTUAL RESULT {step} : Failed to set the value of RDKRemoteDebugger IssueType to {value}. Details : {details}")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return set_flag
########## End of function ##########

# checkDebugReportGenerated
# Syntax: checkDebugReportGenerated(obj, profile_type, step)
# Description: Function to check whether the debug report got created in the designated location
# Parameters: obj - The TDK scripting library object for TR181 component
#             profile_type - The type of debug report (static or dynamic)
#             step - The test step number
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               flag - Flag indicating whether the debug report is generated or not


def checkDebugReportGenerated(obj, profile_type, step):
    expectedresult = "SUCCESS"
    flag = False
    file_path = report_generation_location
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    print(f"\nTEST STEP {step} : Check if the {profile_type} debug report is generated at {file_path}")
    print(f"EXPECTED RESULT {step} : The {profile_type} debug report should be present at {file_path}")
    command = f"ls {file_path}/Device-DebugReport*"
    print(f"Command : {command}")
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Command Output : {details}")
    if expectedresult in actualresult and details.strip() != "":
        print(f"ACTUAL RESULT {step} : The {profile_type} debug report is present at {file_path}")
        flag = True
    else:
        print(f"ACTUAL RESULT {step} : The {profile_type} debug report is not present at {file_path}")
    return tdkTestObj, flag
########## End of function ##########

# startDebugReportTarFileTracker
# Syntax: startDebugReportTarFileTracker(obj, profile_type, step, monitor_path, wait_time)
# Description: Function to start a background tracker that stores the generated tar file name when it appears.
# Parameters: obj - The TDK scripting library object for sysutil component
#             profile_type - The type of debug report (static or dynamic)
#             step - The test step number
#             monitor_path - The location where debug reports are generated
#             wait_time - Maximum duration in seconds to track the tar file
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               flag - Flag indicating whether the tracker was started successfully or not


def startDebugReportTarFileTracker(obj, profile_type, step, monitor_path=report_generation_location, wait_time=60):
    expectedresult = "SUCCESS"
    flag = False
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    print(f"\nTEST STEP {step} : Start tracking the {profile_type} debug report tar(.tgz) creation in {monitor_path}")
    print(f"EXPECTED RESULT {step} : The background tracker should detect the {profile_type} debug report tar(.tgz) file and store its name from {monitor_path}")
    # Use fast polling (0.1s) to catch ephemeral tar(.tgz) files that are deleted quickly after upload
    # Using nohup to ensure background process survives
    command = (
        f"sh -c 'rm -f {debug_report_tracker_file}; "
        f"nohup sh -c \"end=\\$(( \\$(date +%s) + {wait_time} )); "
        f"while [ \\$(date +%s) -lt \\$end ]; do "
        f"f=\\$(ls {monitor_path}/*.tgz 2>/dev/null | head -n1); "
        f"[ -n \\\"\\$f\\\" ] && basename \\\"\\$f\\\" > {debug_report_tracker_file} && exit 0; "
        f"sleep 0.1; "
        f"done\" >/dev/null 2>&1 &'"
    )
    print(f"Command : {command}")
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Command Output : {details}")
    if expectedresult in actualresult:
        print(f"ACTUAL RESULT {step} : Started tracking the {profile_type} debug report tar(.tgz) file creation and file name")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
        flag = True
    else:
        print(f"ACTUAL RESULT {step} : Failed to start tracking the {profile_type} debug report tar(.tgz) file creation and file name")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return tdkTestObj, flag
########## End of function ##########

# isDebugReportTarFileCreated
# Syntax: isDebugReportTarFileCreated(obj, profile_type, step, wait_time)
# Description: Function to check whether a tar(.tgz) file creation was captured by the background tracker and return its name.
# Parameters: obj - The TDK scripting library object for sysutil component
#             profile_type - The type of debug report (static or dynamic)
#             step - The test step number
#             wait_time - Maximum duration in seconds to wait for the tracked tar(.tgz) creation
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               flag - Flag indicating whether a debug report tar(.tgz) creation was detected or not
#               report_name - The detected debug report tar(.tgz) file name


def isDebugReportTarFileCreated(obj, profile_type, step, wait_time=30):
    expectedresult = "SUCCESS"
    flag = False
    report_name = ""
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    print(f"\nTEST STEP {step} : Check whether the tracked {profile_type} debug report tar(.tgz) file was created and get its file name")
    print(f"EXPECTED RESULT {step} : The tracker should confirm that a {profile_type} debug report tar(.tgz) file was created and return its file name")
    # Check if tracker file has content (background tracker should have written to it)
    command = (
        f"sh -c 'if [ -s \"{debug_report_tracker_file}\" ]; then "
        f"cat \"{debug_report_tracker_file}\"; "
        f"rm -f \"{debug_report_tracker_file}\"; "
        f"exit 0; "
        f"else "
        f"echo \"\"; "
        f"exit 1; "
        f"fi'"
    )
    print(f"Command : {command}")
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Command Output : {details}")
    if expectedresult in actualresult and details.strip() != "":
        report_name = details.strip().splitlines()[0].strip()
        print(f"ACTUAL RESULT {step} : A {profile_type} debug report tar(.tgz) file was created with file name {report_name}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
        flag = True
    else:
        print(f"ACTUAL RESULT {step} : No {profile_type} debug report tar(.tgz) file creation was detected. Ensure sufficient sleep time before this check.")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return tdkTestObj, flag, report_name
########## End of function ##########

# checkJsonProfileAvailable
# Syntax: checkJsonProfileAvailable(obj, profile_type, issue_type, step)
# Description: Function to check whether the profile debug report is fetched and present at the designated location
# Parameters: obj - The TDK scripting library object for TR181 component
#             profile_type - The type of debug report (static or dynamic)
#             issue_type - The issue type for which the debug report is generated
#             step - The test step number
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               flag - Flag indicating whether the profile debug report is fetched and present or not


def checkJsonProfileAvailable(obj, profile_type, issue_type, step):
    expectedresult = "SUCCESS"
    flag = False
    profile_path = ""
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    if profile_type == "static":
        profile_path = static_json_file
        print(f"\nTEST STEP {step} : Check if the {profile_type} debug report is present at {profile_path}")
    elif profile_type == "dynamic":
        profile_path = dynamic_json_file
        print(f"\nTEST STEP {step} : Check if the {profile_type} debug report is fetched from the server and present at {profile_path}")
    print(f"EXPECTED RESULT {step} : The {profile_type} debug report should be present at {profile_path}")
    command = f"cat {profile_path} | grep -i {issue_type.split('.')[1]}"
    print(f"Command : {command}")
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Command Output : {details}")
    if expectedresult in actualresult and details.strip() != "":
        print(f"ACTUAL RESULT {step} : The {profile_type} debug report is present at {profile_path}")
        flag = True
    else:
        print(f"ACTUAL RESULT {step} : The {profile_type} debug report is not present at {profile_path}")
    return tdkTestObj, flag


########## End of function ##########

# getRDKRemoteDebuggerEnable
# Syntax: getRDKRemoteDebuggerEnable(obj, step)
# Description: Function to get the value of RDKRemoteDebugger Enable parameter using TR181 Get operation.
# Parameters: obj - The TDK scripting library object for TR181 component
#             step - The test step number
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               get_flag - Flag indicating whether the TR181 Get operation was successful or not
#               value - The value of RDKRemoteDebugger Enable parameter
def getRDKRemoteDebuggerEnable(obj, step):
    expectedresult = "SUCCESS"
    value = ""
    get_flag = False
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Get')
    print(f"\nTEST STEP {step} : Get the value of RDKRemoteDebugger Enable")
    print(f"EXPECTED RESULT {step} : Should get the value of RDKRemoteDebugger Enable")
    actualresult, value = getTR181Value(tdkTestObj, "Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.RDKRemoteDebugger.Enable")
    if expectedresult in actualresult:
        get_flag = True
        print(f"ACTUAL RESULT {step} : Value of RDKRemoteDebugger Enable is {value}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
    else:
        print(f"ACTUAL RESULT {step} : Failed to get the value of RDKRemoteDebugger Enable. Details : {value}")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return tdkTestObj, get_flag, value
########## End of function ##########

# setRDKRemoteDebuggerEnable
# Syntax: setRDKRemoteDebuggerEnable(obj, value, step)
# Description: Function to set the value of RDKRemoteDebugger Enable parameter using TR181 Set operation.
# Parameters: obj - The TDK scripting library object for TR181 component
#             value - The value to be set for RDKRemoteDebugger Enable parameter
#             step - The test step number
# Return Value: set_flag - Flag indicating whether the TR181 Set operation was successful or not


def setRDKRemoteDebuggerEnable(obj, value, step):
    expectedresult = "SUCCESS"
    set_flag = False
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Set')
    print(f"\nTEST STEP {step} : Set the value of RDKRemoteDebugger Enable as {value}")
    print(f"EXPECTED RESULT {step} : Should set the value of RDKRemoteDebugger Enable as {value}")
    actualresult, details = setTR181Value(tdkTestObj, "Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.RDKRemoteDebugger.Enable", value, "bool")
    if expectedresult in actualresult and details != "":
        set_flag = True
        print(f"ACTUAL RESULT {step} : Successfully set the value of RDKRemoteDebugger Enable to {value}. Details : {details}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
    else:
        print(f"ACTUAL RESULT {step} : Failed to set the value of RDKRemoteDebugger Enable to {value}. Details : {details}")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return set_flag
########## End of function ##########

# validateDebugReportUpload
# Syntax: validateDebugReportUpload(obj, profile_type, upload_server_url, report_name, step)
# Description: Function to check whether the specific debug report file exists in the upload server.
# Parameters: obj - The TDK scripting library object for TR181 component
#             profile_type - The type of debug report (static or dynamic)
#             upload_server_url - The report upload server location URL
#             report_name - The debug report file name captured by the tracker
#             step - The test step number
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               flag - Flag indicating whether the debug report is present in the upload server or not


def validateDebugReportUpload(obj, profile_type, upload_server_url, report_name, step):
    flag = False
    expectedresult = "SUCCESS"
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    report_url = f"{upload_server_url.rstrip('/')}/{report_name}" if report_name != "" else ""
    print(f"\nTEST STEP {step} : Check if the {profile_type} debug report {report_name} exists in the upload server {upload_server_url}")
    print(f"EXPECTED RESULT {step} : The {profile_type} debug report {report_name} should exist in the upload server {upload_server_url}")
    command = f"curl -L -s -o /dev/null -w '%{{http_code}}' '{report_url}'"
    print(f"Command : {command}")
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Command Output : {details}")
    if expectedresult in actualresult and details.strip() == "200":
        print(f"ACTUAL RESULT {step} : The {profile_type} debug report {report_name} exists in the upload server {upload_server_url}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
        flag = True
    else:
        print(f"ACTUAL RESULT {step} : The {profile_type} debug report {report_name} does not exist in the upload server {upload_server_url}")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return tdkTestObj, flag
########## End of function ##########

# getRDKRemoteDebuggerCDLModuleURL
# Syntax: getRDKRemoteDebuggerCDLModuleURL(obj, step)
# Description: Function to get the download server URL configured in the DUT
# Parameters: obj - The TDK scripting library object for TR181 component
#             step - The test step number
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               get_flag - Flag indicating whether the TR181 Get operation was successful or not
#               value - The download server URL configured in the DUT


def getRDKRemoteDebuggerCDLModuleURL(obj, step):
    expectedresult = "SUCCESS"
    value = ""
    get_flag = False
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Get')
    print(f"\nTEST STEP {step} : Get the download server URL configured in the DUT")
    print(f"EXPECTED RESULT {step} : Should get the download server URL configured in the DUT")
    actualresult, value = getTR181Value(tdkTestObj, "Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.CDLDM.CDLModuleUrl")
    if expectedresult in actualresult:
        get_flag = True
        print(f"ACTUAL RESULT {step} : Download server URL configured in the DUT is {value}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
    else:
        print(f"ACTUAL RESULT {step} : Failed to get the download server URL configured in the DUT")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return tdkTestObj, get_flag, value
########## End of function ##########

# setRDKRemoteDebuggerCDLModuleURL
# Syntax: setRDKRemoteDebuggerCDLModuleURL(obj, server_url, step)
# Description: Function to set the download server URL in the DUT
# Parameters: obj - The TDK scripting library object for TR181 component
#             server_url - The download server URL to be set in the DUT
#             step - The test step number
# Return Value: set_flag - Flag indicating whether the TR181 Set operation was successful or not


def setRDKRemoteDebuggerCDLModuleURL(obj, server_url, step):
    expectedresult = "SUCCESS"
    set_flag = False
    # Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.CDLDM.CDLModuleUrl
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Set')
    print(f"\nTEST STEP {step} : Configure the download server URL {server_url} in the DUT")
    print(f"EXPECTED RESULT {step} : Should configure the download server URL {server_url} in the DUT")
    actualresult, details = setTR181Value(tdkTestObj, "Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.CDLDM.CDLModuleUrl", server_url, "string")
    if expectedresult in actualresult and details != "":
        set_flag = True
        print(f"ACTUAL RESULT {step} : Successfully configured the download server URL {server_url} in the DUT. Details : {details}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
    else:
        print(f"ACTUAL RESULT {step} : Failed to configure the download server URL {server_url} in the DUT. Details : {details}")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return set_flag
########## End of function ##########


# getUpstreamRRDURL
# Syntax: getUpstreamRRDURL(sysobj, upstreamRRDURLpath, step)
# Description: Function to get the upload server URL assigned to UPSTREAM_RRD_URL in the specified file path in the DUT
# Parameters: sysobj - The TDK scripting library object for sysutil component
#             upstreamRRDURLpath - The file path where the UPSTREAM_RRD_URL is assigned in the DUT
#             step - The test step number
# Return Value: get_flag - Flag indicating whether the upload server URL is successfully obtained
#               value - upload server URL value configured.

def getUpstreamRRDURL(sysobj, upstreamRRDURLpath, step):
    expectedresult = "SUCCESS"
    value = ""
    get_flag = False
    tdkTestObj = sysobj.createTestStep('ExecuteCmd')
    print(f"\nTEST STEP {step} : Get the upload server URL assigned to UPSTREAM_RRD_URL in {upstreamRRDURLpath}")
    print(f"EXPECTED RESULT {step} : Should get the upload server URL assigned to UPSTREAM_RRD_URL in {upstreamRRDURLpath}")
    command = f"sed -n 's/^UPSTREAM_RRD_URL=//p' {upstreamRRDURLpath}"

    print(f"Command : {command}")
    actualresult, value = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Command Output : {value}")
    if expectedresult in actualresult and value.strip() != "":
        get_flag = True
        print(f"ACTUAL RESULT {step} : Upload server URL assigned to UPSTREAM_RRD_URL in {upstreamRRDURLpath} is {value.strip()}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
    else:
        print(f"ACTUAL RESULT {step} : Failed to get the upload server URL assigned to UPSTREAM_RRD_URL in {upstreamRRDURLpath}")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return get_flag, value.strip()
########## End of function ##########


# setUpstreamRRDURL
# Syntax: setUpstreamRRDURL(sysobj, server_url, upstream_rrd_url_path, step)
# Description: Function to set the upload server URL to UPSTREAM_RRD_URL in the specified file path in the DUT
# Parameters: sysobj - The TDK scripting library object for sysutil component
#             server_url - The upload server URL to be set for UPSTREAM_RRD_URL in the DUT
#             upstreamRRDURLpath - The file path where the UPSTREAM_RRD_URL is assigned in the DUT
#             step - The test step number
# Return Value: set_flag - Flag indicating whether the upload server URL is set to UPSTREAM_RRD_URL successfully or not


def setUpstreamRRDURL(sysobj, server_url, upstreamRRDURLpath, step):
    expectedresult = "SUCCESS"
    set_flag = False
    # Assign the upload server URL to UPSTREAM_RRD_URL in upstreamRRDURLpath
    tdkTestObj = sysobj.createTestStep('ExecuteCmd')
    print(f"\nTEST STEP {step} : Assign the upload server URL to UPSTREAM_RRD_URL in {upstreamRRDURLpath}")
    print(f"EXPECTED RESULT {step} : Should assign the upload server URL to UPSTREAM_RRD_URL in {upstreamRRDURLpath}")
    command = f"sed -i 's|^UPSTREAM_RRD_URL=.*|UPSTREAM_RRD_URL={server_url}|' {upstreamRRDURLpath}"
    print(f"Command : {command}")
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Command Output : {details}")
    if expectedresult in actualresult:
        set_flag = True
        print(f"ACTUAL RESULT {step} : Successfully assigned the upload server URL to UPSTREAM_RRD_URL in {upstreamRRDURLpath}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
    else:
        print(f"ACTUAL RESULT {step} : Failed to assign the upload server URL to UPSTREAM_RRD_URL in {upstreamRRDURLpath}")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return set_flag
########## End of function ##########
