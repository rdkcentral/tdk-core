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
#-----------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
import json
import requests
from time import sleep
from datetime import datetime
import tdklib
from tr69Config import *
from tdkutility import *

# Poll configuration for waiting until ACS DB reflects queued task updates.
ACS_REFLECTION_TIMEOUT_SEC = 120
ACS_REFLECTION_INTERVAL_SEC = 10
ACS_TASK_STATUS_TIMEOUT_SEC = 300
ACS_TASK_STATUS_INTERVAL_SEC = 10
# Keep this strict so periodic inform-based late execution does not
# mask connection-request blocked/offline negative scenarios.
ACS_QUEUED_INFORM_MAX_DELAY_SEC = 60

# extract_task_id
# Syntax      : extract_task_id(taskResponse)
# Description : Extract ACS task identifier from task response payload.
# Parameters  : taskResponse - dict/list returned by ACS task APIs.
# Return Value: task_id - task id string if available, otherwise None.
def extract_task_id(taskResponse):
    if isinstance(taskResponse, dict):
        task_id = taskResponse.get("_id")
        print(f"task id : {task_id}")
        return task_id
    if isinstance(taskResponse, list) and taskResponse:
        firstEntry = taskResponse[0]
        if isinstance(firstEntry, dict):
            task_id = firstEntry.get("_id")
            return task_id
    return None
########## End of function ##########

# extract_task_timestamp
# Syntax      : extract_task_timestamp(taskResponse)
# Description : Extract task creation timestamp from ACS task response payload.
# Parameters  : taskResponse - dict/list returned by ACS task APIs.
# Return Value: timestamp string if available, otherwise None.
def extract_task_timestamp(taskResponse):
    # Extract task queue timestamp used for post-queue inform validation.
    if isinstance(taskResponse, dict):
        return taskResponse.get("timestamp")
    if isinstance(taskResponse, list):
        if len(taskResponse) == 0:
            return None
        firstEntry = taskResponse[0]
        if isinstance(firstEntry, dict):
            return firstEntry.get("timestamp")
    return None
########## End of function ##########

# parse_acs_timestamp
# Syntax      : parse_acs_timestamp(timestamp)
# Description : Parse ACS timestamp string to datetime object.
# Parameters  : timestamp - timestamp from ACS task/device response.
# Return Value: datetime object on success, None on parse failure.
def parse_acs_timestamp(timestamp):
    if not timestamp or not isinstance(timestamp, str):
        return None
    # Handle common GenieACS timestamp layouts with/without milliseconds.
    normalized = timestamp.replace("Z", "+0000")
    formats = [
        "%Y-%m-%d %H:%M:%S.%f %z",
        "%Y-%m-%d %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S%z"
    ]
    for timeFormat in formats:
        try:
            return datetime.strptime(normalized, timeFormat)
        except Exception:
            continue
    return None
########## End of function ##########

# get_device_last_inform
# Syntax      : get_device_last_inform(username)
# Description : Fetch and parse the latest lastInform timestamp for a device from ACS DB.
# Parameters  : username - ACS device id.
# Return Value: datetime object if available, otherwise None.
def get_device_last_inform(username):
    try:
        query = {"_id": username}
        params = {"query": json.dumps(query), "projection": "_lastInform"}
        response = requests.get(ACS_NBI_URL + "/devices", params=params)
        if response.status_code != 200:
            return None
        body = response.json()
        if not isinstance(body, list):
            return None
        if len(body) == 0:
            return None
        deviceInfo = body[0]
        if not isinstance(deviceInfo, dict):
            return None
        lastInform = deviceInfo.get("_lastInform")
        if isinstance(lastInform, dict):
            # Handle alternate response shape if ACS wraps values.
            lastInform = lastInform.get("_value") or lastInform.get("value")
        return parse_acs_timestamp(lastInform)
    except Exception as error:
        print(f"Exception while fetching device last inform: {error}")
        return None
########## End of function ##########

# check_device_inform_after_task
# Syntax      : check_device_inform_after_task(username, timeStamp, maxDelaySec)
# Description : Check whether device informed ACS after task was queued.
# Parameters  : username - ACS device id.
#             : timeStamp - timestamp from task creation response.
#             : maxDelaySec - maximum accepted delay for post-task inform.
# Return Value: True if _lastInform is after task timestamp and within allowed delay.
def check_device_inform_after_task(username, timeStamp, maxDelaySec=ACS_QUEUED_INFORM_MAX_DELAY_SEC):
    if not username:
        return False
    taskTimestamp = parse_acs_timestamp(timeStamp)
    if taskTimestamp is None:
        return False
    lastInform = get_device_last_inform(username)
    if lastInform is None:
        return False
    if lastInform < taskTimestamp:
        return False
    # Late periodic inform can otherwise create false success in offline scenarios.
    return (lastInform - taskTimestamp).total_seconds() <= maxDelaySec
########## End of function ##########

# getACSTaskStatus
# Syntax      : getACSTaskStatus(taskId)
# Description : Fetch current task state/details from ACS tasks collection.
# Parameters  : taskId - ACS task id.
# Return Value: state - PENDING/COMPLETED/FAULTED/UNKNOWN.
#             : detail - task detail/fault info when available.
def getACSTaskStatus(taskId):
    # Use search API for ACS tasks
    taskStatusUrl = ACS_NBI_URL + "/tasks"
    params = {"query": json.dumps({"_id": taskId})}
    print(f"task url : {taskStatusUrl}, params : {params}")
    try:
        response = requests.get(taskStatusUrl, params=params)
        print(f"task status code : {response.status_code}")
        print(f"task status text : {response.text}")
        if response.status_code != 200:
            return "UNKNOWN", {"status": response.status_code, "body": response.text}
        try:
            taskList = response.json()
        except ValueError:
            return "UNKNOWN", {"status": response.status_code, "body": response.text}
        # Task list empty means task completed/disappeared from ACS DB
        if not isinstance(taskList, list) or len(taskList) == 0:
            return "COMPLETED", None
        taskInfo = taskList[0]
        if isinstance(taskInfo, dict):
            # Fault can appear either as top-level task fault or nested under _response.
            directFault = taskInfo.get("fault")
            responseFault = None
            responseBody = taskInfo.get("_response")
            if isinstance(responseBody, dict):
                responseFault = responseBody.get("fault")
            if directFault or responseFault:
                return "FAULTED", directFault or responseFault
        return "PENDING", taskInfo
    except Exception as error:
        print(f"Exception occurred while checking task status: {error}")
        return "UNKNOWN", {"error": str(error)}
########## End of function ##########

# waitForTaskTerminalStatus
# Syntax      : waitForTaskTerminalStatus(taskId,timeoutSec,intervalSec)
# Description : Poll ACS task API until terminal state or timeout.
# Parameters  : taskId - ACS task id.
#             : timeoutSec - maximum poll duration in seconds.
#             : intervalSec - wait interval between polls.
# Return Value: task state and detail payload.
def waitForTaskTerminalStatus(taskId,timeoutSec=ACS_TASK_STATUS_TIMEOUT_SEC,intervalSec=ACS_TASK_STATUS_INTERVAL_SEC):
    elapsed = 0
    lastDetail = None
    lastExecutionData = None  # Track if task ever had _response or fault (actual execution)
    while elapsed <= timeoutSec:
        state, detail = getACSTaskStatus(taskId)
        print(f"task state: {state}")
        lastDetail = detail
        # Store task info ONLY if it has actual execution data (RPC response or fault)
        # Queued tasks without _response or fault field don't count as execution data
        if detail and isinstance(detail, dict):
            if detail.get("_response") or detail.get("fault"):
                lastExecutionData = detail
        if state in ("COMPLETED", "FAULTED", "UNKNOWN"):
            # If COMPLETED but task never had _response or fault, device was offline/unreachable
            if state == "COMPLETED" and lastExecutionData is None:
                print(f"WARNING: Task {taskId} disappeared without RPC response - device was likely offline or unreachable")
                return state, None  # Signal offline by returning None
            # Return the task data that had actual execution (response or fault)
            if state in ("FAULTED", "UNKNOWN"):
                return state, detail
            return state, lastExecutionData
        if elapsed >= timeoutSec:
            break
        sleep(intervalSec)
        elapsed += intervalSec
    return "PENDING", lastDetail
########## End of function ##########

# waitForTaskCompletionIfQueued
# Syntax      : waitForTaskCompletionIfQueued(tdkTestObj, status, queryResponse, step, operationName, deviceUsername)
# Description : When a task returns HTTP 202 (queued), extracts the task ID and polls ACS
#               until the task reaches a terminal state (COMPLETED, FAULTED, or timeout)..
# Parameters  : tdkTestObj - Object of the tdk library.
#             : status - HTTP status code returned by tr069ACSQuery.
#             : queryResponse - Response body returned by tr069ACSQuery.
#             : step - Current test step number.
#             : operationName - Name of the operation.
#             : deviceUsername - Device ID used for ACS /devices query when response omits device field.
# Return Value: True if the task execution verifiably succeeded.
#             : False if queued execution cannot be validated or task failed/timed out.
def waitForTaskCompletionIfQueued(tdkTestObj, status, queryResponse, step, operationName, deviceUsername=None):
    # This helper is called only for queued (HTTP 202) task handling.
    taskId = extract_task_id(queryResponse)
    if not taskId:
        tdkTestObj.setResultStatus("FAILURE")
        print("ACTUAL RESULT %d: %s task queued (HTTP 202) but task ID was not returned by ACS, so queued execution cannot be verified." % (step, operationName))
        print("[TEST EXECUTION RESULT] : FAILURE")
        return False
    taskTimestamp = extract_task_timestamp(queryResponse)
    taskDevice = deviceUsername
    if taskDevice is None and isinstance(queryResponse, dict):
        # Fallback when caller does not pass username explicitly.
        taskDevice = queryResponse.get("device")
    print("%s task queued (HTTP 202). Polling ACS task status for task id %s" % (operationName, taskId))
    taskState, taskDetail = waitForTaskTerminalStatus(taskId)
    if taskState == "FAULTED":
        tdkTestObj.setResultStatus("FAILURE")
        print("ACTUAL RESULT %d: %s task faulted in ACS. Possible causes: invalid credentials, RPC fault on device, or unsupported parameter. Details: %s" % (step, operationName, str(taskDetail)))
        print("[TEST EXECUTION RESULT] : FAILURE")
        return False
    elif taskState == "PENDING":
        tdkTestObj.setResultStatus("FAILURE")
        print("ACTUAL RESULT %d: %s task still pending after timeout. Device may be offline, connection request failed, or NAT blocked the request." % (step, operationName))
        print("[TEST EXECUTION RESULT] : FAILURE")
        return False
    elif taskState == "UNKNOWN":
        tdkTestObj.setResultStatus("FAILURE")
        print("ACTUAL RESULT %d: Unable to determine terminal %s task state from ACS. Treating as failure to avoid false success." % (step, operationName))
        print("[TEST EXECUTION RESULT] : FAILURE")
        return False
    elif taskState == "COMPLETED":
        # If task row disappears without execution payload, use inform timing to infer outcome.
        # Task had actual response data - proceed
        if taskDetail is None:
            if check_device_inform_after_task(username=taskDevice, timeStamp=taskTimestamp, maxDelaySec=ACS_QUEUED_INFORM_MAX_DELAY_SEC):
                tdkTestObj.setResultStatus("SUCCESS")
                print("ACTUAL RESULT %d: %s task completed without explicit RPC payload, but device informed ACS after task queue time. Treating as successful queued execution." % (step, operationName))
                print("[TEST EXECUTION RESULT] : SUCCESS")
                return True
            tdkTestObj.setResultStatus("FAILURE")
            print("ACTUAL RESULT %d: %s task completed but device never responded (no RPC execution). Device may be offline, unreachable, behind NAT, or connection request failed." % (step, operationName))
            print("[TEST EXECUTION RESULT] : FAILURE")
            return False
    # If taskState is COMPLETED with data or other non-failure terminal state - proceed
    return True
########## End of function ##########

# normalize_param_list
# Syntax      : normalize_param_list(params)
# Description : Convert scalar parameter/value into list to simplify downstream loops.
# Parameters  : params - scalar or list.
# Return Value: list of values.
def normalize_param_list(params):
    if isinstance(params, list):
        return params
    return [params]
########## End of function ##########

# values_match
# Syntax      : values_match(actual, expected)
# Description : Compare ACS value with expected value using type-tolerant normalization.
# Parameters  : actual - value from ACS.
#             : expected - expected value from script.
# Return Value: True if both values match semantically, else False.
def values_match(actual, expected):
    if isinstance(actual, str) and isinstance(expected, str):
        return actual.strip().lower() == expected.strip().lower()
    if isinstance(actual, bool) or isinstance(expected, bool):
        return str(actual).strip().lower() == str(expected).strip().lower()
    return str(actual).strip() == str(expected).strip()
########## End of function ##########

# is_search_response_fresh
# Syntax      : is_search_response_fresh(queryResponse,queryParam,minTimestamp)
# Description : Validate that SEARCH response contains parameter timestamps newer than task timestamp.
# Parameters  : queryResponse - raw ACS SEARCH response payload.
#             : queryParam - dict containing parameter details with key "name".
#             : minTimestamp - minimum accepted timestamp (datetime).
# Return Value: True if all requested parameters are fresh enough, else False.
def is_search_response_fresh(queryResponse,queryParam,minTimestamp):
    if minTimestamp is None:
        return True
    names = queryParam.get("name")
    if isinstance(names, str):
        names = [names]
    if not isinstance(queryResponse, list) or len(queryResponse) == 0:
        return False
    for param in names:
        data = queryResponse[0]
        for key in param.split("."):
            if not isinstance(data, dict):
                return False
            data = data.get(key)
            if data is None:
                return False
        if not isinstance(data, dict):
            return False
        ts = parse_acs_timestamp(data.get("_timestamp"))
        if ts is None or ts < minTimestamp:
            return False
    return True
########## End of function ##########

# waitForACSValueReflection
# Syntax      : waitForACSValueReflection(username,queryParam,expectedValues,timeoutSec,intervalSec,minTimestamp)
# Description : Polls ACS search API until requested parameter values are available/reflected.
# Parameters  : username - username used in ACS query to identify DUT.
#             : queryParam - dict containing parameter details with key "name".
#             : expectedValues - dict of expected values keyed by parameter name. Optional.
#             : timeoutSec - max wait duration.
#             : intervalSec - poll interval.
#             : minTimestamp - optional freshness timestamp for queued task validation.
# Return Value: status - HTTP status from search API.
#             : parsedResponse - parsed value dict from ACS search.
def waitForACSValueReflection(username,queryParam,expectedValues=None,timeoutSec=ACS_REFLECTION_TIMEOUT_SEC,intervalSec=ACS_REFLECTION_INTERVAL_SEC,minTimestamp=None):
    elapsed = 0
    lastStatus = None
    while elapsed <= timeoutSec:
        status, queryResponse = tr069ACSQuery(username,queryParam,"search")
        lastStatus = status
        if status == 200 and queryResponse is not None:
            parsedResponse = parseTR69ACSResponse(queryResponse,queryParam,"search")
            if parsedResponse is not None:
                # Prevent stale ACS cache from being accepted as queued GET success.
                if is_search_response_fresh(queryResponse,queryParam,minTimestamp):
                    if expectedValues is None:
                        return status, parsedResponse
                    allMatched = True
                    for key, expected in expectedValues.items():
                        actual = parsedResponse.get(key)
                        if actual is None or not values_match(actual, expected):
                            allMatched = False
                            break
                    if allMatched:
                        return status, parsedResponse
        if elapsed >= timeoutSec:
            break
        sleep(intervalSec)
        elapsed += intervalSec
    return lastStatus, None
########## End of function ##########

# tr069ACSPreRequisite
# Syntax      : tr069ACSPreRequisite()
# Description : Function to do the prerequisite of tr069 ACS.
# Parameters  : obj - Object of the tdk library.
#             : sysobj - Object of tdk library.
# Return Value: tdkTestObj_tr181 - Object of tdk library.
#             : username - Connection request username that uniquely identify the DUT.
#             : initialValues - List of original values of the modified Tr69 DMs.
#             : returnStatus - SUCCESS/FAILURE
def tr069ACSPreRequisite(obj,sysobj):
    tdkTestObj = sysobj.createTestStep('ExecuteCmd')
    expectedresult = "SUCCESS"
    returnStatus = "FAILURE"
    tr069paStatus = "FAILURE"
    ConfigStatus = "FAILURE"
    ConnectionStatus = "FAILURE"
    initialValues = []
    tdkTestObj_tr181 = obj.createTestStep('TDKB_TR181Stub_Get')
    print("\nChecking the PREREQUISITES")
    #Check for the tr069 process
    print("Check if tr069 process is up and listening to port 7547")
    cmd= "netstat -tulnp | grep ':7547' | grep CcspTr069PaSsp"
    tdkTestObj = sysobj.createTestStep('ExecuteCmd')
    tdkTestObj.addParameter("command", cmd)
    retryCount = 1
    MAX_RETRY = 5
    while retryCount <= MAX_RETRY:
        #Check for every 1 min whether the process is up
        tdkTestObj.executeTestCase(expectedresult)
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        print(f"Iteration {retryCount}, network status of tr069 : {details}")
        if expectedresult in actualresult and details != "":
            print("tr069pa process is up and listening to port 7547")
            tr069paStatus = "SUCCESS"
            tdkTestObj.setResultStatus("SUCCESS")
            break
        else:
            retryCount = retryCount + 1
        tdkTestObj.setResultStatus("FAILURE")
        if retryCount <= MAX_RETRY:
            sleep(60)
    if tr069paStatus == "SUCCESS":
        #Onboard the device to ACS server.
        print("Get the initial value of Device.ManagementServer.EnableCWMP")
        actualresult, details = getTR181Value(tdkTestObj_tr181,"Device.ManagementServer.EnableCWMP")
        if expectedresult in actualresult:
            tdkTestObj_tr181.setResultStatus("SUCCESS")
            print("Got the parameter value of Device.ManagementServer.EnableCWMP as %s successfully" %details)
            initialValues.append(details)

            print("Get the initial value of Device Management server URL")
            actualresult, details = getTR181Value(tdkTestObj_tr181,"Device.ManagementServer.URL")
            if expectedresult in actualresult:
                tdkTestObj_tr181.setResultStatus("SUCCESS")
                print("Got the parameter value of Device.ManagementServer.URL as %s successfully" %details)
                initialValues.append(details)

                print("Get the initial value of Device.DeviceInfo.X_RDKCENTRAL-COM_Syndication.TR69CertLocation")
                actualresult, details = getTR181Value(tdkTestObj_tr181,"Device.DeviceInfo.X_RDKCENTRAL-COM_Syndication.TR69CertLocation")
                if expectedresult in actualresult:
                    tdkTestObj_tr181.setResultStatus("SUCCESS")
                    print("Got the parameter value of Device.DeviceInfo.X_RDKCENTRAL-COM_Syndication.TR69CertLocation as %s successfully" %details)
                    initialValues.append(details)

                    print("Set the Enable CWMP, Device ManagementServer URL and TR69CertLocation for configuring the DUT with ACS server")
                    tdkTestObj_tr181 = obj.createTestStep("TDKB_TR181Stub_SetMultiple");
                    tdkTestObj_tr181.addParameter("paramList","Device.ManagementServer.EnableCWMP|%s|bool|Device.ManagementServer.URL|%s|string|Device.DeviceInfo.X_RDKCENTRAL-COM_Syndication.TR69CertLocation|%s|string" %("true",ACS_URL,TR069_CERTIFICATE_LOCATION))
                    tdkTestObj_tr181.executeTestCase(expectedresult)
                    actualresult = tdkTestObj_tr181.getResult()
                    details = tdkTestObj_tr181.getResultDetails()
                    if expectedresult in actualresult:
                        tdkTestObj_tr181.setResultStatus("SUCCESS")
                        print("Set the Tr069 ACS configuration values successfully")
                        ConfigStatus = "SUCCESS"
                    else:
                        tdkTestObj_tr181.setResultStatus("FAILURE")
                        print("Failed to set the Tr069 ACS configuration values")
                else:
                    tdkTestObj_tr181.setResultStatus("FAILURE")
                    print("Failed to get the value of Device.DeviceInfo.X_RDKCENTRAL-COM_Syndication.TR69CertLocation")
                    initialValues.append(None)
            else:
                tdkTestObj_tr181.setResultStatus("FAILURE")
                print("Failed to get the value of Device Management server URL")
                initialValues.append(None)
        else:
            tdkTestObj_tr181.setResultStatus("FAILURE")
            print("Failed to get the value of Device.ManagementServer.EnableCWMP")
            initialValues.append(None)
    if tr069paStatus == "SUCCESS" and ConfigStatus == "SUCCESS":
        # Get the connection request username required for DUT to connect with ACS
        print("Get the Username for connection request")
        tdkTestObj_tr181 = obj.createTestStep('TDKB_TR181Stub_Get')
        actualresult, details = getTR181Value(tdkTestObj_tr181,"Device.ManagementServer.ConnectionRequestUsername")
        if expectedresult in actualresult and details != "":
            #Set the result status of execution
            username = details.strip()
            print(f"Got Connection Request Username : {username} successfully")
            tdkTestObj_tr181.setResultStatus("SUCCESS")
            ConnectionStatus = "SUCCESS"
        else :
            print("Failed to retrieve Connection Request Username")
            tdkTestObj_tr181.setResultStatus("FAILURE")

    if tr069paStatus == "SUCCESS" and ConfigStatus == "SUCCESS" and ConnectionStatus == "SUCCESS":
        #Prerequisite success check
        returnStatus = "SUCCESS"
        print("PREREQUISITES are success\n")
        return tdkTestObj_tr181,username,initialValues,returnStatus
    else:
        return tdkTestObj_tr181,None,initialValues,returnStatus
########## End of function ##########

# gettr069ACS
# Syntax      : gettr069ACS(tdkTestObj,username,queryParam,step)
# Description : Function to get value of the parameter.
# Parameters  : tdkTestObj - Object of the tdk library.
#             : username - username to be passed in the ACS request for uniquely identifying the DUT.
#             : queryParam - dict of parameters with parameter details to be included in the ACS request.
#             : step - Test step count.
# Return Value: parsedResponse - parsed response from the query response of ACS.
#             : step  - Current test step count.
def gettr069ACS(tdkTestObj,username,queryParam,step):
    name = queryParam.get("name")
    step += 1
    minimumSearchTimestamp = None
    #Send GET task request to get the parameter details from device
    print("\nTEST STEP %d: Send GET task request to get %s and receive a valid response via ACS server" % (step, name))
    print("EXPECTED RESULT %d: Send GET task request to get %s and receive a valid response successfully via ACS server" % (step,name))

    status, queryResponse = tr069ACSQuery(username, queryParam, "get")
    if status == 200 and queryResponse is not None:
        # Task executed synchronously - proceed directly
        pass
    elif status == 202 and queryResponse is not None:
        # Task queued - poll for terminal state to detect offline device,
        # connection request failures, or RPC faults before proceeding to search query
        if not waitForTaskCompletionIfQueued(tdkTestObj, status, queryResponse, step, "GET", username):
            return None, step
        minimumSearchTimestamp = parse_acs_timestamp(extract_task_timestamp(queryResponse))
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("ACTUAL RESULT %d: GET Task failed to get %s with status %s " % (step, name, str(status)))
        print("[TEST EXECUTION RESULT] : FAILURE")
        return None, step

    tdkTestObj.setResultStatus("SUCCESS")
    print("ACTUAL RESULT %d: GET Task successful for %s via ACS server" % (step, name))
    print("[TEST EXECUTION RESULT] : SUCCESS")

    # Increment step after successful GET
    step += 1
    #Send SEARCH query and poll until ACS reflects the requested value(s)
    print("\nTEST STEP %d: Send SEARCH query to get value of %s from ACS Database" % (step, name))
    print("EXPECTED RESULT %d:  Send SEARCH query to get value of %s from ACS Database successfully" % (step,name))
    status, parsedResponse = waitForACSValueReflection(username,queryParam,minTimestamp=minimumSearchTimestamp)

    if status != 200 or parsedResponse is None:
        tdkTestObj.setResultStatus("FAILURE")
        print("ACTUAL RESULT %d: SEARCH failed or value not reflected for %s within timeout, status %s" % (step, name, str(status)))
        print("[TEST EXECUTION RESULT] : FAILURE")
        return None, step

    tdkTestObj.setResultStatus("SUCCESS")
    print("ACTUAL RESULT %d: SEARCH successful for %s from ACS Database" % (step, name))
    print("Retrieved value of %s successfully" %name)
    for key,value in parsedResponse.items():
        print(f"{key} : {value}")
    print("[TEST EXECUTION RESULT] : SUCCESS")

    return parsedResponse,step
########## End of function ##########

# getTr181DMValue
# Syntax      : getTr181DMValue(obj,queryParam,step)
# Description : Function to get the parameter value from device.
# Parameters  : obj - object of tdk library.
#             : queryParam - dict of parameters with parameter details.
#             : step - Test step count.
# Return Value: tdkTestObj_tr181 - object of tdk library.
#             : getValuesTr181 - dict keyed by parameter name.
#             : step - current test step count.
def getTr181DMValue(obj,queryParam,step):
    parameters = queryParam.get("name")
    expectedresult = "SUCCESS"
    # Normalize to list
    if isinstance(parameters, str):
        parameters = [parameters]
    getValuesTr181 = {}
    # Get the parameter value
    for name in parameters:
        step += 1
        print("\nTEST STEP %d : Get the value of the parameter %s from DUT" %(step,name))
        print("EXPECTED RESULT %d : Get the value of the parameter %s successfully" %(step,name))
        tdkTestObj_tr181 = obj.createTestStep('TDKB_TR181Stub_Get')
        actualresult, details = getTR181Value(tdkTestObj_tr181,name)
        if expectedresult in actualresult:
            getValueTr181 = details.strip("'")
            tdkTestObj_tr181.setResultStatus("SUCCESS")
            print("ACTUAL RESULT %d : Got the parameter %s value as %s successfully" %(step,name,getValueTr181))
            print("[TEST EXECUTION RESULT] : SUCCESS")
            getValuesTr181[name] = getValueTr181
        else:
            tdkTestObj_tr181.setResultStatus("FAILURE")
            print("ACTUAL RESULT %d : Failed to get the parameter %s value" %(step,name))
            print("[TEST EXECUTION RESULT] : FAILURE")
            getValuesTr181[name] = details

    return tdkTestObj_tr181,getValuesTr181,step
########## End of function ##########

# settr069ACS
# Syntax      : settr069ACS(tdkTestObj,username,queryParam,step)
# Description : Function to set value of the parameter.
# Parameters  : tdkTestObj - Object of the tdk library.
#             : username - username to be passed in the ACS request for uniquely identifying the DUT.
#             : queryParam - dict of parameters with parameter details to be included in the ACS request.
#             : step - Test step count.
# Return Value: queryResponse - Query response from ACS server.
#             : step - current test step count.
def settr069ACS(tdkTestObj,username,queryParam,step):
    name = queryParam.get("name")
    value = queryParam.get("value")
    step += 1
    #Send SET task request to set  the parameter value to another value
    print("\nTEST STEP %d: Send SET task request to set the %s to %s and receive a valid response via ACS server" %(step,name,value))
    print("EXPECTED RESULT %d: Send SET task request to set the %s to %s and receive a valid response successfully via ACS server" %(step,name,value))
    status,queryResponse = tr069ACSQuery(username,queryParam,"set")
    if status == 200 and queryResponse is not None:
        # Task executed synchronously
        tdkTestObj.setResultStatus("SUCCESS")
        print("ACTUAL RESULT %d: Sent SET task request to set the %s as %s successfully via ACS server" %(step,name,value))
        names = normalize_param_list(name)
        values = normalize_param_list(value)
        expectedValues = {p: v for p, v in zip(names, values)}
        searchParam = {"name": names}
        searchStatus, reflectedValues = waitForACSValueReflection(username,searchParam,expectedValues)
        if searchStatus == 200 and reflectedValues is not None:
            print("SET value reflected in ACS database")
            print("[TEST EXECUTION RESULT] : SUCCESS")
            return queryResponse,step
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("SET task accepted but value was not reflected in ACS database within timeout")
            print("[TEST EXECUTION RESULT] : FAILURE")
            return None,step
    elif status == 202 and queryResponse is not None:
        # Task queued - poll for terminal state to detect offline device,
        # connection request failures, or RPC faults before checking value reflection
        if not waitForTaskCompletionIfQueued(tdkTestObj, status, queryResponse, step, "SET", username):
            return None, step
        tdkTestObj.setResultStatus("SUCCESS")
        print("ACTUAL RESULT %d: Sent SET task request to set the %s as %s successfully via ACS server" %(step,name,value))
        names = normalize_param_list(name)
        values = normalize_param_list(value)
        expectedValues = {p: v for p, v in zip(names, values)}
        searchParam = {"name": names}
        searchStatus, reflectedValues = waitForACSValueReflection(username,searchParam,expectedValues)
        if searchStatus == 200 and reflectedValues is not None:
            print("SET value reflected in ACS database")
            print("[TEST EXECUTION RESULT] : SUCCESS")
            return queryResponse,step
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("SET task accepted but value was not reflected in ACS database within timeout")
            print("[TEST EXECUTION RESULT] : FAILURE")
            return None,step
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("ACTUAL RESULT %d : Failed to set the parameter %s" %(step,name))
        print("[TEST EXECUTION RESULT] : FAILURE")
        return None,step
########## End of function ##########

# tr069ACSQuery
# Syntax      : tr069ACSQuery(username,parameter,method="get")
# Description : Function to create and send an HTTP request to the ACS server using the requests library.
# Parameters  : username - username to be passed in the ACS request for uniquely identifying the DUT.
#             : parameter - parameter list to be included in the ACS request.
#             : method - whether the method is get or set or search or RefreshObject or AddObject or DeleteObject or FactoryReset or Reboot.
# Return Value:  query response - query response from the ACS server.
def tr069ACSQuery(username,parameter,method="get"):
    ACS_QUERY_URL = ACS_NBI_URL + f"/devices"
    ACS_TASK_URL = ACS_QUERY_URL + f"/{username}/tasks"
    if method == "get":
        #Query for GET task operation
        name = parameter.get("name")
        params = {"timeout": 3000,"connection_request": ""}
        if isinstance(name, list):
            payload = {"name": "getParameterValues","parameterNames": name}
        else:
            payload = {"name": "getParameterValues","parameterNames": [name]}
    elif method == "search":
        #Query for search operation
        name = parameter.get("name")
        if isinstance(name, list):
            projection = ",".join(name)
        else:
            projection = name
        query = {"_id": username}
        params = { "query":json.dumps(query), "projection": projection}
    elif method == "RefreshObject":
        # Query for RefreshObject task operation
        name = parameter.get("name")
        if name:
            payload = {"name": "refreshObject", "objectName":name}
            params = {"timeout": 3000, "connection_request": ""}
        else:
            # payload when all parameters are to be refreshed
            payload = {"name": "refreshObject", "objectName":""}
            params = {"connection_request": ""}
    elif method == "set":
        #Query for SET operation
        parameters = parameter.get("name")
        values = parameter.get("value")
        params = {"timeout": 3000,"connection_request": ""}
        #Normalize to list if single parameter
        if not isinstance(parameters, list):
            parameters = [parameters]
        if not isinstance(values, list):
            values = [values]
        parameterValues = [[p, v] for p, v in zip(parameters, values)]
        payload = {"name": "setParameterValues","parameterValues": parameterValues}
    elif method in ("AddObject","DeleteObject"):
        #Query for AddObject and DeleteObject operation
        name = parameter.get("name")
        params = {"timeout": 3000,"connection_request": ""}
        if method == "AddObject":
            payload = {"name":"addObject","objectName":name}
        else:
            payload = {"name":"deleteObject","objectName":name}
    elif method in ("FactoryReset","Reboot"):
        #Query for FactoryReset and Reboot operation
        params = {"timeout": 3000,"connection_request": ""}
        if method == "FactoryReset":
            payload = {"name":"factoryReset"}
        else:
            payload = {"name":"reboot"}
    try:
        resp = None
        if method in ("get","set","RefreshObject","AddObject","DeleteObject","FactoryReset","Reboot"):
            # Send GET/SET/RefreshObject/AddObject/DeleteObject/FactoryReset/Reboot request to the DUT via ACS server
            resp = requests.post(ACS_TASK_URL,params=params, json=payload)
        elif method == "search":
            resp = requests.get(ACS_QUERY_URL, params=params)
        if resp is not None:
            print(f"Response is not empty")
            if resp.status_code:
                print(f"Status: {resp.status_code}")
                if not resp.text:
                    print(f"Response have empty text response")
                    if method in ("get","set","RefreshObject","AddObject","DeleteObject","FactoryReset","Reboot"):
                        return resp.status_code,{}
                    return resp.status_code,None
                else:
                    print(f"Response Body: {resp.text}")
                    try:
                        data = resp.json()
                    except ValueError:
                        print("Invalid JSON response:", resp.text)
                        if method in ("get","set","RefreshObject","AddObject","DeleteObject","FactoryReset","Reboot"):
                            return resp.status_code,{}
                        return resp.status_code,None
                    print(f"JSON Response : {data}")
                    return resp.status_code,data
            else:
                print(f"Response have empty status code")
                return None,None
        else:
            print(f"Request has no valid response")
            return None,None
    except Exception as e:
        # catches any unexpected errors
        print(f"Exception occurred: {e}")
        return None, None
########## End of function ##########

# parseTR69ACSResponse
# Syntax      : parseTR69ACSResponse(response,parameters,method)
# Description : Function to parse the Tr69 ACS response.
# Parameters  : response - response message to be parsed.
#             : parameters - parameter list with parameter details.
#             : method -  whether the method is to search.
# Return Value: paramValues - dict mapping parameter paths to values.
def parseTR69ACSResponse(response,parameters,method):
    if method == "search":
        # Get requested parameter names
        dmParam = parameters.get('name')
        # Normalize to list
        if isinstance(dmParam, str):
            dmParam = [dmParam]
        # Validate response structure
        if not response or not isinstance(response, list):
            print("Invalid response format")
            return None
        try:
            paramValues = {}
            for param in dmParam:
                keys = param.split(".")
                data = response[0]   # First device object
                #Get the full parameter path
                for key in keys:
                    if not isinstance(data, dict):
                        print(f"Unexpected structure at key: {key}")
                        return None
                    data = data.get(key)
                    if data is None:
                        print(f"Key not found in response: {key}")
                        return None
                # Case 1: Leaf parameter
                if isinstance(data, dict) and "_value" in data:
                    value = data["_value"]
                    value = value.strip("'") if isinstance(value, str) else value
                    paramValues[param] = value

                # Case 2: Object parameter
                elif isinstance(data, dict) and data.get("_object") is True:
                    for child_key, child_val in data.items():
                        if isinstance(child_val, dict) and "_value" in child_val:
                            val = child_val["_value"]
                            val = val.strip("'") if isinstance(val, str) else val
                            # build full parameter path
                            full_param = f"{param}.{child_key}"
                            paramValues[full_param] = val
                else:
                    print("Final node is not a valid parameter or object")
                    return None
            return paramValues
        except Exception as e:
            print("Error parsing search response:", str(e))
            return None
########## End of function ##########

# revertPrerequisite()
# Syntax      : revertPrerequisite(obj,initialValues,step)
# Description : Function to revert the DMs changed during prerequisite
# Parameters  : obj -  Object of tdk library
#             : initialValues - List of initial values of DMs
#             : step - Current test step count
# Return Value: None
def revertPrerequisite(obj,initialValues,step):
    step=step+1
    expectedresult = "SUCCESS"
    tdkTestObj_tr181 = obj.createTestStep("TDKB_TR181Stub_SetMultiple")
    if len(initialValues) == 3 and all(v is not None for v in initialValues):
        print("\nTEST STEP %d : Revert the values of Tr069 Data models Enable CWMP, Device Management server url and Tr69CertLocation modified during prerequisite check" %step)
        print("EXPECTED RESULT %d : The modified values of TR069 Data models should be reverted successfully" %step)
        tdkTestObj_tr181.addParameter("paramList","Device.ManagementServer.EnableCWMP|%s|bool|Device.ManagementServer.URL|%s|string|Device.DeviceInfo.X_RDKCENTRAL-COM_Syndication.TR69CertLocation|%s|string" %(initialValues[0],initialValues[1],initialValues[2]))
        tdkTestObj_tr181.executeTestCase(expectedresult)
        actualresult = tdkTestObj_tr181.getResult()
        details = tdkTestObj_tr181.getResultDetails()
        if expectedresult in actualresult:
            tdkTestObj_tr181.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Reverted the modified Tr069 ACS configuration values successfully")
        else:
            tdkTestObj_tr181.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to revert the Tr069 ACS configuration values.")
    else:
        print("\n Required initial values of modified Tr69 configuration parameters are missing")
        tdkTestObj_tr181.setResultStatus("FAILURE")
########## End of function ##########
