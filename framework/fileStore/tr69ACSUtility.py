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
import json
import requests
from time import sleep
import tdklib
from tr69Config import *
from tdkutility import *

# tr069ACSPreRequisite
# Syntax      : tr069ACSPreRequisite()
# Description : Function to do the prerequisite of tr069 ACS.
# Parameters  : obj - Object of the tdk library.
#             : sysobj - Object of tdk library.
# Return Value: tdkTestObj_tr181 - Object of tdk library.
#             : username - Connection request username that uniquely identify the DUT.
#             : returnStatus - SUCCESS/FAILURE
def tr069ACSPreRequisite(obj,sysobj):
    tdkTestObj = sysobj.createTestStep('ExecuteCmd')
    expectedresult = "SUCCESS"
    returnStatus = "FAILURE"
    tr069paStatus = "FAILURE"
    ConfigStatus = "FAILURE"
    ConnectionStatus = "FAILURE"

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
        retryCount = 1
        MAX_RETRY = 5
        tdkTestObj.executeTestCase(expectedresult)
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        print(f"Iteration {retryCount}, network status of tr069 : {details}")
        if expectedresult in actualresult and details:
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
        print("Enable Device.ManagementServer.EnableCWMP parameter")
        tdkTestObj_tr181 = obj.createTestStep('TDKB_TR181Stub_Set')
        actualresult, details = setTR181Value(tdkTestObj_tr181, "Device.ManagementServer.EnableCWMP", "true", "bool")
        if expectedresult in actualresult:
            print("Enabled Device.ManagementServer.EnableCWMP parameter successfully")
            tdkTestObj_tr181.setResultStatus("SUCCESS")

            print("Set the Device Management server URL as ",SERVER_URL)
            actualresult, details = setTR181Value(tdkTestObj_tr181, "Device.ManagementServer.URL", SERVER_URL, "string")
            if expectedresult in actualresult:
                print("Set the Device Management Server URL successfully")
                tdkTestObj_tr181.setResultStatus("SUCCESS")

                print("Set Device.DeviceInfo.X_RDKCENTRAL-COM_Syndication.TR69CertLocation as ", TR069_CERTIFICATE_LOCATION)
                actualresult, details = setTR181Value(tdkTestObj_tr181, "Device.DeviceInfo.X_RDKCENTRAL-COM_Syndication.TR69CertLocation", TR069_CERTIFICATE_LOCATION, "string")
                if expectedresult in actualresult:
                    print("Set Device.DeviceInfo.X_RDKCENTRAL-COM_Syndication.TR69CertLocation successfully")
                    tdkTestObj_tr181.setResultStatus("SUCCESS")
                    ConfigStatus = "SUCCESS"
                else:
                    print("Failed to set Device.DeviceInfo.X_RDKCENTRAL-COM_Syndication.TR69CertLocation")
                    tdkTestObj_tr181.setResultStatus("FAILURE")
            else:
                print("Failed to set Device Management server URL")
                tdkTestObj_tr181.setResultStatus("FAILURE")
        else :
            print("Failed to enable Device.ManagementServer.EnableCWMP")
            tdkTestObj_tr181.setResultStatus("FAILURE")

    if tr069paStatus == "SUCCESS" and ConfigStatus == "SUCCESS":
        # Get the connection request username required for DUT to connect with ACS
        print("Get the Username for connection request")
        tdkTestObj_tr181 = obj.createTestStep('TDKB_TR181Stub_Get')
        actualresult, details = getTR181Value(tdkTestObj_tr181,"Device.ManagementServer.ConnectionRequestUsername")
        if expectedresult in actualresult and details:
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
        return tdkTestObj_tr181,username,returnStatus
    else:
        return None,None,returnStatus

# gettr069ACS
# Syntax      : gettr069ACS(tdkTestObj,username,queryParam,step)
# Description : Function to get value of the parameter.
# Parameters  : tdkTestObj - Object of the tdk library.
#             : username - username to be passed in the ACS request for uniquely identifying the DUT.
#             : queryParam - parameter list to be included in the ACS request.
#             : step - Test step count.
# Return Value: parsedResponse - parsed response from the query response of ACS.
#             : step  - Current test step count.
def gettr069ACS(tdkTestObj,username,queryParam,step):
    name = queryParam.get("name")
    step += 1

    #Send GET task request to get the parameter details from device
    print("TEST STEP %d: Send GET task request to get %s and receive a valid response via ACS server" % (step, name))
    print("EXPECTED RESULT %d: Send GET task request to get %s and receive a valid response successfully via ACS server" % (step,name))

    status, queryResponse = tr069ACSQuery(username, queryParam, "get")

    if status != 200 or queryResponse is None:
        tdkTestObj.setResultStatus("FAILURE")
        print("ACTUAL RESULT %d: GET Task failed to get %s with status %d " % (step, name, status))
        print("[TEST EXECUTION RESULT] : FAILURE")
        return None, step

    tdkTestObj.setResultStatus("SUCCESS")
    print("ACTUAL RESULT %d: GET Task successful for %s via ACS server" % (step, name))
    print("[TEST EXECUTION RESULT] : SUCCESS")

    # Increment step after successful GET
    step += 1

    #Send SEARCH query to get the parameter details
    print("\nTEST STEP %d: Send SEARCH query to get value of %s from ACS Database" % (step, name))
    print("EXPECTED RESULT %d:  Send SEARCH query to get value of %s from ACS Database successfully" % (step,name))
    # Formation ofACS query
    status, queryResponse = tr069ACSQuery(username,queryParam,"search")

    if status != 200 or queryResponse is None:
        tdkTestObj.setResultStatus("FAILURE")
        print("ACTUAL RESULT %d: SEARCH failed for %s with status %d" % (step, name, status))
        print("[TEST EXECUTION RESULT] : FAILURE")
        return None, step

    tdkTestObj.setResultStatus("SUCCESS")
    print("ACTUAL RESULT %d: SEARCH successful for %s from ACS Database" % (step, name))

    # Parse response to retrieve the value of parameter
    parsedResponse = parseTR69ACSResponse(queryResponse,queryParam,"search")

    if parsedResponse is None:
        tdkTestObj.setResultStatus("FAILURE")
        print("Failed to retrieve value of %s from ACS Database" % name)
        print("[TEST EXECUTION RESULT] : FAILURE")
        return None, step

    tdkTestObj.setResultStatus("SUCCESS")
    print("Retrieved value of %s as %s successfully" % (name, parsedResponse))
    print("[TEST EXECUTION RESULT] : SUCCESS")

    return parsedResponse,step

# getTr181DMValue
# Syntax      : getTr181DMValue(obj,queryParam,step)
# Description : Function to get the parameter value from device.
# Parameters  : obj - object of tdk library.
#             : queryParam - parameter list with parameter details.
#             : step - Test step count.
# Return Value: tdkTestObj_tr181 - object of tdk library.
#             : getValuesTr181 - parameter value list from device.
#             : step - current test step count.
def getTr181DMValue(obj,queryParam,step):
    parameters = queryParam.get("name")
    expectedresult = "SUCCESS"

    # Normalize to list
    if isinstance(parameters, str):
        parameters = [parameters]

    getValuesTr181 = []
    # Get the parameter value
    for name in parameters:
        step += 1
        print("\n TEST STEP %d : Get the value of the parameter %s from DUT" %(step,name))
        print("EXPECTED RESULT %d : Get the value of the parameter %s successfully" %(step,name))
        tdkTestObj_tr181 = obj.createTestStep('TDKB_TR181Stub_Get')
        actualresult, details = getTR181Value(tdkTestObj_tr181,name)
        if expectedresult in actualresult and details:
            getValueTr181 = details.strip("'")
            tdkTestObj_tr181.setResultStatus("SUCCESS")
            print("ACTUAL RESULT %d : Got the parameter %s value as %s successfully" %(step,name,getValueTr181))
            print("[TEST EXECUTION RESULT] : SUCCESS")
            getValuesTr181.append(getValueTr181)
        else:
            tdkTestObj_tr181.setResultStatus("FAILURE")
            print("ACTUAL RESULT %d : Failed to get the parameter %s value" %(step,name))
            print("[TEST EXECUTION RESULT] : FAILURE")
            getValuesTr181.append(details)

    return tdkTestObj_tr181,getValuesTr181,step

# settr069ACS
# Syntax      : settr069ACS(tdkTestObj,username,queryParam,step)
# Description : Function to set value of the parameter.
# Parameters  : tdkTestObj - Object of the tdk library.
#             : username - username to be passed in the ACS request for uniquely identifying the DUT.
#             : queryParam - parameter list to be included in the ACS request.
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
        tdkTestObj.setResultStatus("SUCCESS")
        print("ACTUAL RESULT %d: Sent SET task request to set the %s as %s successfully via ACS server" %(step,name,value))
        print("[TEST EXECUTION RESULT] : SUCCESS")
        return queryResponse,step
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("ACTUAL RESULT %d : Failed to set the parameter %s" %(step,name))
        print("[TEST EXECUTION RESULT] : FAILURE")
        return None,step

# tr069ACSQuery
# Syntax      : tr069ACSQuery(username,parameter,method="get")
# Description : Function to create and send an HTTP request to the ACS server using the requests library.
# Parameters  : username - username to be passed in the ACS request for uniquely identifying the DUT.
#             : parameter - parameter list to be included in the ACS request.
#             : method - whether the method is get or set or search or RefreshObject.
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

    try:
        resp = None
        if method in ("get","set","RefreshObject"):
            #send GET/SET/Refresh request to the DUT via ACS server
            resp = requests.post(ACS_TASK_URL,params=params, json=payload)
        elif method == "search":
            resp = requests.get(ACS_QUERY_URL, params=params)
        print(f"Status: {resp.status_code}")
        if not resp.text:
            return resp.status_code,None
        try:
            data = resp.json()
        except ValueError:
            print("Invalid JSON response:", resp.text)
            return resp.status_code,None
        print(f"JSON Response : {data}")
        return resp.status_code,data

    except Exception as e:
        # catches any unexpected errors
        print(f"[UNEXPECTED ERROR] {e}")
        print(f"Status: {resp.status_code}")
        print(f"Response Body: {resp.text}")
        return resp.status_code,None

# parseTR69ACSResponse
# Syntax      : parseTR69ACSResponse(response,parameters,method)
# Description : Function to parse the Tr69 ACS response.
# Parameters  : response - response message to be parsed.
#             : parameters - parameter list with parameter details.
#             : method -  whether the method is to search.
# Return Value: paramValues - list of parameter values.
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
            paramValues = []
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
                # After full traversal, extract _value
                if isinstance(data, dict):
                    value = data.get("_value")
                    value = value.strip("'") if isinstance(value, str) else value
                else:
                    print("Final node is not a dictionary")
                    return None
                print(f"Extracted value for {param}: {value}")
                paramValues.append(value)
            return paramValues
        except Exception as e:
            print(f"Parsing error: {e}")
            return None
