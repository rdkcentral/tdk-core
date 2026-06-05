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
        tdkTestObj_tr181 = obj.createTestStep('TDKB_TR181Stub_Get')
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
        return None,None,initialValues,returnStatus

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

    #Send GET task request to get the parameter details from device
    print("\nTEST STEP %d: Send GET task request to get %s and receive a valid response via ACS server" % (step, name))
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
        tdkTestObj.setResultStatus("SUCCESS")
        print("ACTUAL RESULT %d: Sent SET task request to set the %s as %s successfully via ACS server" %(step,name,value))
        print("[TEST EXECUTION RESULT] : SUCCESS")
        return queryResponse,step
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
                    return resp.status_code,None
                else:
                    print(f"Response Body: {resp.text}")
                    try:
                        data = resp.json()
                    except ValueError:
                        print("Invalid JSON response:", resp.text)
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
    if len(initialValues) == 3 and all(v is not None for v in initialValues)::
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

