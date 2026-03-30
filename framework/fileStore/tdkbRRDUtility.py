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

# clearLogsAndDebugReports
# Syntax: clearLogsAndDebugReports(obj)
# Description: Function to clear the RRD log file and delete the existing debug reports before starting the test execution
# Parameters: obj - The TDK scripting library object for sysutil component
# Return Value: prereq_flag - Flag indicating whether the prerequisite steps are successful or not (1 for success, 0 for failure)
def clearLogsAndDebugReports(obj):
    #Remove the existing debug reports in the report generation location before starting the test execution
    expectedresult = "SUCCESS"
    prereq_flag = False
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    print(f"\nPREREQUISITE : Remove the existing debug reports in the report generation location {report_generation_location} before starting the test execution")
    command = f"rm -rf {report_generation_location}/*"
    print(f"Command : {command}")
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    if actualresult in expectedresult:
        print(f"PREREQUISITE SUCCESS : Successfully removed the existing debug reports in the report generation location {report_generation_location}")
        tdkTestObj.setResultStatus("SUCCESS")

        # Clear the RRD log file to ensure that the logs captured during the test execution are only related to the current test execution
        tdkTestObj = obj.createTestStep('ExecuteCmd')
        print(f"\nPREREQUISITE : Clear the RRD log file {rrd_log_file} before starting the test execution")
        command = f"cat /dev/null > {rrd_log_file}"
        print(f"Command : {command}")
        actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
        if actualresult in expectedresult:
            print(f"PREREQUISITE SUCCESS : Successfully cleared the RRD log file {rrd_log_file}")
            tdkTestObj.setResultStatus("SUCCESS")
            prereq_flag = True
        else:
            print(f"PREREQUISITE FAILURE : Failed to clear the RRD log file {rrd_log_file}")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print(f"PREREQUISITE FAILURE : Failed to remove the existing debug reports in the report generation location {report_generation_location}")
        tdkTestObj.setResultStatus("FAILURE")
    return prereq_flag
########## End of function ##########

# getRDKRemoteDebuggerIssueType
# Syntax: getRDKRemoteDebuggerIssueType(obj, step)
# Description: Function to get the value of RDKRemoteDebugger IssueType parameter using TR181 Get operation.
# Parameters: obj - The TDK scripting library object for TR181 component
#             step - The test step number
# Return Value: tdkTestObj - The TDK test object created for TR181 Get operation
#               get_flag - Flag indicating whether the TR181 Get operation was successful or not (1 for success, 0 for failure)
#               value - The value of the RDKRemoteDebugger IssueType parameter
def getRDKRemoteDebuggerIssueType(obj, step):
    expectedresult="SUCCESS"
    value = ""
    get_flag = 0
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Get')
    print(f"\nTEST STEP {step} : Get the value of RDKRemoteDebugger IssueType")
    print(f"EXPECTED RESULT {step} : Should get the value of RDKRemoteDebugger IssueType")
    actualresult, value = getTR181Value(tdkTestObj,"Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.RDKRemoteDebugger.IssueType")
    if actualresult in expectedresult:
        get_flag = 1
        print(f"ACTUAL RESULT {step} : Value of RDKRemoteDebugger IssueType is {value}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
    else:
        print(f"ACTUAL RESULT {step} : Failed to get the value of RDKRemoteDebugger IssueType")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return tdkTestObj,get_flag, value
########## End of function ##########

# setRDKRemoteDebuggerIssueType
# Syntax: setRDKRemoteDebuggerIssueType(obj, step, value)
# Description: Function to set the value of RDKRemoteDebugger IssueType parameter using TR181 Set operation.
# Parameters: obj - The TDK scripting library object for TR181 component
#             step - The test step number
#             value - The value to be set for RDKRemoteDebugger IssueType parameter
# Return Value: set_flag - Flag indicating whether the TR181 Set operation was successful or not (1 for success, 0 for failure)
def setRDKRemoteDebuggerIssueType(obj, step, value):
    expectedresult="SUCCESS"
    set_flag = 0
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Set')
    print(f"\nTEST STEP {step} : Set the value of RDKRemoteDebugger IssueType as {value}")
    print(f"EXPECTED RESULT {step} : Should set the value of RDKRemoteDebugger IssueType as {value}")
    actualresult, details = setTR181Value(tdkTestObj,"Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.RDKRemoteDebugger.IssueType", value, "string")
    if actualresult in expectedresult and details != "":
        set_flag = 1
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
#               flag - Flag indicating whether the debug report is generated or not (1 for success, 0 for failure)

def checkDebugReportGenerated(obj, profile_type, step):
    expectedresult="SUCCESS"
    flag = False
    file_path = report_generation_location
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    print(f"\nTEST STEP {step} : Check if the {profile_type} debug report is generated at {file_path}")
    print(f"EXPECTED RESULT {step} : The {profile_type} debug report should be present at {file_path}")
    command = f"find {file_path}/Device-DebugReport*"
    print(f"Command : {command}")
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Command Output : {details}")
    if expectedresult in actualresult and 'No such file or directory' not in details:
        print(f"ACTUAL RESULT {step} : The {profile_type} debug report is present at {file_path}")
        flag = True
    else:
        print(f"ACTUAL RESULT {step} : The {profile_type} debug report is not present at {file_path}")
    return tdkTestObj, flag
########## End of function ##########

# checkJsonProfileAvailable
# Syntax: checkJsonProfileAvailable(obj, profile_type, step)
# Description: Function to check whether the profile debug report is fetched and present at the designated location
# Parameters: obj - The TDK scripting library object for TR181 component
#             profile_type - The type of debug report (static or dynamic)
#             issue_type - The issue type for which the debug report is generated
#             step - The test step number
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               flag - Flag indicating whether the profile debug report is fetched and present or not (1 for success, 0 for failure)

def checkJsonProfileAvailable(obj, profile_type, issue_type, step):
    expectedresult="SUCCESS"
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

#getRDKRemoteDebuggerEnable
# Syntax: getRDKRemoteDebuggerEnable(obj, step)
# Description: Function to get the value of RDKRemoteDebugger Enable parameter using TR181 Get operation.
# Parameters: obj - The TDK scripting library object for TR181 component
#             step - The test step number
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               get_flag - Flag indicating whether the TR181 Get operation was successful or not (1 for success, 0 for failure)
#               value - The value of RDKRemoteDebugger Enable parameter
def getRDKRemoteDebuggerEnable(obj, step):
    expectedresult="SUCCESS"
    value = ""
    get_flag = 0
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Get')
    print(f"\nTEST STEP {step} : Get the value of RDKRemoteDebugger Enable")
    print(f"EXPECTED RESULT {step} : Should get the value of RDKRemoteDebugger Enable")
    actualresult, value = getTR181Value(tdkTestObj,"Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.RDKRemoteDebugger.Enable")
    if actualresult in expectedresult:
        get_flag = 1
        print(f"ACTUAL RESULT {step} : Value of RDKRemoteDebugger Enable is {value}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
    else:
        print(f"ACTUAL RESULT {step} : Failed to get the value of RDKRemoteDebugger Enable. Details : {value}")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return tdkTestObj, get_flag, value
########## End of function ##########

#setRDKRemoteDebuggerEnable
# Syntax: setRDKRemoteDebuggerEnable(obj, value, step)
# Description: Function to set the value of RDKRemoteDebugger Enable parameter using TR181 Set operation.
# Parameters: obj - The TDK scripting library object for TR181 component
#             value - The value to be set for RDKRemoteDebugger Enable parameter
#             step - The test step number
# Return Value: set_flag - Flag indicating whether the TR181 Set operation was successful or not (1 for success, 0 for failure)

def setRDKRemoteDebuggerEnable(obj, value, step):
    expectedresult="SUCCESS"
    set_flag = 0
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Set')
    print(f"\nTEST STEP {step} : Set the value of RDKRemoteDebugger Enable as {value}")
    print(f"EXPECTED RESULT {step} : Should set the value of RDKRemoteDebugger Enable as {value}")
    actualresult, details = setTR181Value(tdkTestObj,"Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.RDKRemoteDebugger.Enable", value, "bool")
    if actualresult in expectedresult and details != "":
        set_flag = 1
        print(f"ACTUAL RESULT {step} : Successfully set the value of RDKRemoteDebugger Enable to {value}. Details : {details}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
    else:
        print(f"ACTUAL RESULT {step} : Failed to set the value of RDKRemoteDebugger Enable to {value}. Details : {details}")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return set_flag
########## End of function ##########

#validateDebugReportUpload
# Syntax: validateDebugReportUpload(obj, profile_type, upload_server_url, step)
# Description: Function to check whether the debug report got uploaded in the designated location from the RRD log file
# Parameters: obj - The TDK scripting library object for TR181 component
#             profile_type - The type of debug report (static or dynamic)
#             upload_server_url - The report upload server location URL
#             log_file - The RRD log file path
#             step - The test step number
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               flag - Flag indicating whether the debug report is generated or not (1 for success, 0 for failure)

def validateDebugReportUpload(obj, profile_type, upload_server_url, log_file, step):
    flag = 0
    expectedresult="SUCCESS"
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    print(f"\nTEST STEP {step} : Check if the {profile_type} debug report is uploaded to the server {upload_server_url}")
    print(f"EXPECTED RESULT {step} : The {profile_type} debug report should be uploaded to the server {upload_server_url}")
    command = f"cat {log_file} | grep 'Debug Information Report upload Success'"
    print(f"Command : {command}")
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Command Output : {details}")
    if expectedresult in actualresult and details != "":
        print(f"ACTUAL RESULT {step} : The {profile_type} debug report is successfully uploaded to the server {upload_server_url}")
        flag = 1
    else:
        print(f"ACTUAL RESULT {step} : The {profile_type} debug report is not uploaded to the server {upload_server_url}")
    return tdkTestObj, flag
########## End of function ##########

# getRDKRemoteDebuggerCDLModuleURL
# Syntax: getRDKRemoteDebuggerCDLModuleURL(obj, step)
# Description: Function to get the download server URL configured in the DUT
# Parameters: obj - The TDK scripting library object for TR181 component
#             step - The test step number
# Return Value: tdkTestObj - The TDK test object created for the command execution
#               get_flag - Flag indicating whether the TR181 Get operation was successful or not (1 for success, 0 for failure)
#               value - The download server URL configured in the DUT

def getRDKRemoteDebuggerCDLModuleURL(obj, step):
    expectedresult="SUCCESS"
    value = ""
    get_flag = 0
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Get')
    print(f"\nTEST STEP {step} : Get the download server URL configured in the DUT")
    print(f"EXPECTED RESULT {step} : Should get the download server URL configured in the DUT")
    actualresult, value = getTR181Value(tdkTestObj,"Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.CDLDM.CDLModuleUrl")
    if actualresult in expectedresult:
        get_flag = 1
        print(f"ACTUAL RESULT {step} : Download server URL configured in the DUT is {value}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
    else:
        print(f"ACTUAL RESULT {step} : Failed to get the download server URL configured in the DUT")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return tdkTestObj, get_flag, value
########## End of function ##########

#setRDKRemoteDebuggerCDLModuleURL
# Syntax: setRDKRemoteDebuggerCDLModuleURL(obj, server_url, step)
# Description: Function to set the download server URL in the DUT
# Parameters: obj - The TDK scripting library object for TR181 component
#             server_url - The download server URL to be set in the DUT
#             step - The test step number
# Return Value: set_flag - Flag indicating whether the TR181 Set operation was successful or not

def setRDKRemoteDebuggerCDLModuleURL(obj, server_url, step):
    expectedresult="SUCCESS"
    set_flag = 0
    #Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.CDLDM.CDLModuleUrl
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Set')
    print(f"\nTEST STEP {step} : Configure the download server URL {server_url} in the DUT")
    print(f"EXPECTED RESULT {step} : Should configure the download server URL {server_url} in the DUT")
    actualresult, details = setTR181Value(tdkTestObj,"Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.CDLDM.CDLModuleUrl", server_url, "string")
    if actualresult in expectedresult and details != "":
        set_flag = 1
        print(f"ACTUAL RESULT {step} : Successfully configured the download server URL {server_url} in the DUT. Details : {details}")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"TEST EXECUTION RESULT : SUCCESS")
    else:
        print(f"ACTUAL RESULT {step} : Failed to configure the download server URL {server_url} in the DUT. Details : {details}")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"TEST EXECUTION RESULT : FAILURE")
    return set_flag
########## End of function ##########
