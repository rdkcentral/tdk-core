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
##########################################################################
import json
import requests
import os
import jwt
import datetime
import uuid
from time import sleep;
from usppaVariables import *

def is_token_expired(token):
# is_token_expired
# Syntax      : is_token_expired(token)
# Description : Function to check if existing token expired or not
# Parameters  : token - JWT token already available in the TOKEN_FILE
# Return Value: True/False
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        exp = payload.get("exp")
        if exp is None:
            return True
        now = datetime.datetime.utcnow().timestamp()
        return now >= exp
    except Exception as e:
        # catches any unexpected errors
        print("Token decode error:", e)
        return True
########## End of Function ##########

def login_and_get_token():
# login_and_get_token
# Syntax      : login_and_get_token()
# Description : Function to generate token and save in TOKEN_FILE
# Parameters  : None
# Return Value: Token/None
    payload = {"email": USERNAME, "password": PASSWORD}
    headers = {"Content-Type": "application/json"}
    LOGIN_URL = CONTROLLER_URI + f"/api/auth/login"
    try:
        response = requests.put(LOGIN_URL, json=payload, headers=headers)

        if response.status_code == 200:
            token = response.text.strip().strip('"')  # clean up quote
            #Catch the issue with TOKEN_FILE variable ie, check if Token file path is empty or not
            if not TOKEN_FILE.strip():
                raise ValueError("TOKEN_FILE path is empty. Please configure it.")
                return None
            with open(TOKEN_FILE, "w") as f:
                f.write(token)
            return token
        else:
            print(f"Login failed: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        # catches any unexpected errors
        print(f"[UNEXPECTED ERROR] {e}")
        print(f"Login failed: {response.status_code}, {response.text}")
        return None

########## End of Function ##########

def usppaQuery(agentID, parameter, method="get"):
# usppaQuery
# Syntax      : usppaQuery(obj, agentID, parameter, method="get")
# Description : Function to create and send curl request to USPPA server
# Parameters  : agentID - AgentID to be passed on to the curl request for uniquely identifying the DUT
#             : parameter - parameter list to be passed on to the curl request
#             : method - whether the method is get or set or get_supported_protocol or get_supported_dm or get_instances or add or delete or operate
# Return Value: USPPA response/None
    if parameter != None:
        usppaQuery.parameter_list=[parameter]
        post_data=json.dumps({"parameters":usppaQuery.parameter_list})
        print(post_data)
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token=f.read().strip()
    else:
        token=None
    if token is None or is_token_expired(token):
        print("Token missing or expired. Logging in...")
        token = login_and_get_token()
        #check if Token generation failed or not
        if token is None:
            return "FAILURE", None
    else:
        print("Using existing valid token.")
    #generate unique msg id
    msgid = str(uuid.uuid4())
    USP_URL = CONTROLLER_URI + f"/api/device/{agentID}/any/generic"
    headers = {"Content-Type": "application/json","Authorization": token}
    if method == "get":
        #Query for GET operation
        name = parameter.get("name")
        payload = {"header": {"msg_id": msgid, "msg_type": "GET"}, "body": {"request": {"get": {"paramPaths": [name]}}}}

    elif method == "set":
        #Query for SET operation
        name = parameter.get("name")
        value = parameter.get("value")
        obj_path,param = name.rsplit('.', 1)
        payload = {"header": {"msg_id": msgid, "msg_type": "SET"}, "body": {"request": {"set": {"allow_partial": False,"update_objs": [{"obj_path": f"{obj_path}.","param_settings": [{"param": f"{param}","value": f"{value}", "required": True}]}]}}}}

    elif method == "get_supported_protocol":
        #Query for GET_SUPPORTED_PROTO operation
        headers = {"Content-Type": "application/json","Authorization": token}
        payload = {"header": {"msg_id": msgid, "msg_type": "GET_SUPPORTED_PROTO"}, "body": {"request": {"get_supported_protocol": {"controller_supported_protocol_versions": "1.0"}}}}

    elif method == "get_supported_dm":
        #Query for GET_SUPPORTED_DM operation
        name = parameter.get("name")
        first_level_only = parameter.get("first_level_only")
        if isinstance(first_level_only, str):
            first_level_only = first_level_only.lower() == "true"
        payload = {"header": {"msg_id": msgid, "msg_type": "GET_SUPPORTED_DM"}, "body": {"request": {"get_supported_dm": {"obj_paths": [f"{name}"],"first_level_only" : first_level_only,"return_commands": True,"return_events": True,"return_params": True}}}}

    elif method == "get_instances":
        #Query for GET_INSTANCES operation
        name = parameter.get("name")
        first_level_only = parameter.get("first_level_only")
        if isinstance(first_level_only, str):
            first_level_only = first_level_only.lower() == "true"
        payload = {"header": {"msg_id": msgid, "msg_type": "GET_INSTANCES"}, "body": {"request": {"get_instances": { "obj_paths": [f"{name}"],"first_level_only": first_level_only}}}}

    elif method == "operate":
        #Query for OPERATE operation
        send_resp = parameter.get("send_resp")
        if isinstance(send_resp, str):
            send_resp  = send_resp.lower() == "true"
        payload = {"header": {"msg_id": msgid, "msg_type": "OPERATE"}, "body": {"request": {"operate": {"command": "Device.Reboot()","command_key": "test61","send_resp": send_resp}}}}

    elif method == "add":
        #Query for ADD  operation
        name = parameter.get("name")
        allow_partial = parameter.get("allow_partial")
        if isinstance(allow_partial, str):
            allow_partial = allow_partial.lower() == "true"
        payload = {"header": {"msg_id": msgid, "msg_type": "ADD"},"body": {"request": {"add": {"allow_partial": allow_partial,"create_objs": [{"obj_path": f"{name}","param_settings": [{"param": "Enable","value": "true"},{"param": "ID","value": "add1"},{"param": "NotifType","value": "ValueChange"},{"param": "ReferenceList","value": "Device.LocalAgent.SoftwareVersion","required": True}]}]}}}}
    elif method == "delete":
        name = parameter.get("name")
        allow_partial = parameter.get("allow_partial")
        if isinstance(allow_partial, str):
            allow_partial = allow_partial.lower() == "true"
        payload = {"header": {"msg_id": msgid, "msg_type": "DELETE"},"body": {"request": {"delete": {"allow_partial": allow_partial,"obj_paths": [f"{name}"]}}}}
    try:
        #send request to the Agent via controller
        resp = requests.put(USP_URL, json=payload, headers=headers)
        print(f"Status: {resp.status_code}")
        print(f" Response: {resp.text}")
        return resp.status_code, resp.text
    except Exception as e:
        # catches any unexpected errors
        print(f"[UNEXPECTED ERROR] {e}")
        print(f"Status: {resp.status_code}")
        print(f" Response: {resp.text}")
        return resp.status_code, resp.text

########## End of Function ##########

def parseUsppaResponse(response, method="get"):
# parseUsppaResponse
# Syntax      : parseUsppaResponse(response, method="get")
# Description : Function to parse the USPPA response
# Parameters  : response - response message to be parsed
#             : method - whether the method was get or set or get_supported_protocol or get_supported_dm or get_instances or add or delete or operate
# Return Value: [SUCCESS/FAILURE, parsedValue]
    responseDict = json.loads(response)
    if(responseDict):
        if method == "get":
            # Extract the requested path
            dmParam = usppaQuery.parameter_list[0]['name']
            if dmParam.endswith("."):
                # Full object path (no single parameter)
                obj_path, param = dmParam, None
            else:
                # Split into object path and parameter name
                obj_path, param = dmParam.rsplit('.', 1)

            resolved = (responseDict.get("req_path_results", [{}])[0].get("resolved_path_results", [{}])[0])
            result_params = resolved.get("result_params", {})
            if param:
                # Single parameter case
                value = result_params.get(param)
            else:
                # Object case, return dict of full paths and values
                value = {f"{resolved.get('resolved_path', '')}{k}": v for k, v in result_params.items()}
            if value:
                return ["SUCCESS",value]
            else:
               return ["FAILURE",value]

        elif method == "set":
            #split the object path and parameter name
            dmParam = usppaQuery.parameter_list[0]['name']
            obj_path,param = dmParam.rsplit('.', 1)
            #Parse the response from set operation
            value = (responseDict.get("updated_obj_results", [{}])[0].get("oper_status", {}).get("OperStatus", {}).get("OperSuccess", {}).get("updated_inst_results", [{}])[0].get("updated_params", {}).get(param))
            if value:
                return ["SUCCESS",value]
            else:
                return ["FAILURE",value]

        elif method == "get_supported_protocol":
            #Parse the response from get_supported_protocol operation
            value = responseDict.get("agent_supported_protocol_versions")
            if value:
                return ["SUCCESS",value]
            else:
                return ["FAILURE",value]

        elif method == "get_supported_dm":
            #Parse the response from get_supported_dm operation
            params_list = []
            commands_list = []
            events_list = []
            metadata_list = []
            for obj_result in responseDict.get("req_obj_results", []):
                data_model_inst_uri = obj_result.get("data_model_inst_uri", "")
                for obj in obj_result.get("supported_objs", []):
                    base_path = obj.get("supported_obj_path", "")
                    metadata = {"supported_obj_path": base_path,"access": obj.get("access"),"is_multi_instance": obj.get("is_multi_instance")}
                    metadata_list.append(metadata)
                    #Filter out the parameters
                    for param in obj.get("supported_params", []):
                        parameter = f"{base_path}{param['param_name']}"
                        params_list.append({"parameter": parameter,**{k: v for k, v in param.items() if k != "param_name"}})
                    #Filter out the commands
                    for cmd in obj.get("supported_commands", []):
                        command = f"{base_path}{cmd['command_name']}"
                        commands_list.append({"command": command,**{k: v for k, v in cmd.items() if k != "command_name"}})
                    #Filter out the events
                    for event in obj.get("supported_events", []):
                        eventName = f"{base_path}{event['event_name']}"
                        events_list.append({"event": eventName,**{k: v for k, v in event.items() if k != "event_name"}})
            #Data model URI
            if data_model_inst_uri:
                print(f"Data Model URI : {data_model_inst_uri}")
            #Metadate
            if metadata_list:
                print("\n Meta data:")
                for metadata in metadata_list:
                    print(f"{metadata}")
            #Supported parameters
            if params_list:
                print("\nSupported params:")
                for param in params_list:
                    print(f"{param}")
            #Supported commands
            if commands_list:
                print("\nSupported commands:")
                for command in commands_list:
                    print(f"{command}")
            #Supported events
            if events_list:
                print("\nSupported events:")
                for event in events_list:
                    print(f"{event}")
            if data_model_inst_uri and metadata_list and params_list:
                value = True
                return ["SUCCESS",value]
            else:
                value = False
                return["FAILURE",value]

        elif method == "get_instances":
            #Parse the response from get_instances operation
            instant_paths = []
            requested_path = ""
            for obj_result in responseDict.get("req_path_results", []):
                requested_path = obj_result.get("requested_path","")
                for obj in  obj_result.get("curr_insts",[]):
                    instantiated_path = obj.get("instantiated_obj_path","")
                    if instantiated_path:
                        instant_paths.append(instantiated_path)
            print(f"\nRequested path : {requested_path}")
            print(f"\n Instantiated paths:")
            for path in instant_paths:
                print(f" - {path}")
            if requested_path and instant_paths:
                value = True
                return ["SUCCESS",value]
            else:
                value = False
                return["FAILURE",value]

        elif method == "operate":
            #Parse the response from operate operation
            send_resp = usppaQuery.parameter_list[0]['send_resp']
            if isinstance(send_resp, str):
                send_resp  = send_resp.lower() == "true"
            if send_resp == True:
                executed_cmd, req_output_args = responseDict.get("operation_results",[{}])[0].get("executed_command"), responseDict.get("operation_results",[{}])[0].get("OperationResp",{}).get("ReqOutputArgs")
                if executed_cmd == "Device.Reboot()" and req_output_args =={}:
                    value = True
                    return ["SUCCESS",value]
                else:
                    value = False
                    return["FAILURE",value]

        elif method == "add":
            #Parse the response from add operation
            created_objs = responseDict.get("created_obj_results", [])
            oper_status = created_objs[0].get("oper_status", {}).get("OperStatus", {}).get("OperSuccess", {})
            instantiated_path = oper_status.get("instantiated_path", "")
            instance_number = instantiated_path.strip(".").split(".")[-1]  # e.g. "2"
            unique_keys = oper_status.get("unique_keys", {})
            # Build full paths for each parameter
            params = {f"{instantiated_path}{k}": v for k, v in unique_keys.items()}
            value = {"instance_number": instance_number, "params": params}
            if instance_number and params:
                return ["SUCCESS",value]
            else:
                return ["FAILURE",value]

        elif method == "delete":
            #Parse the response from delete operation
            deleted_objs = responseDict.get("deleted_obj_results", [])
            for obj in deleted_objs:
                requested_path = obj.get("requested_path")
                affected_paths = (obj.get("oper_status", {}).get("OperStatus", {}).get("OperSuccess", {}).get("affected_paths", []))
            if requested_path and requested_path in affected_paths:
                value = True
                return ["SUCCESS",value]
            else:
                value = False
                return ["FAILURE",value]
    else:
        print("Empty response from the request")
        value = False
        return ["FAILURE",value]

########## End of Function ##########

def usppaPreRequisite(obj):
# usppaPreRequisite
# Syntax      : usppaPreRequisite()
# Description : Function to do the pre requisite of usppa
# Parameters  : obj - Object of the tdk library
# Return Value: SUCCESS/FAILURE
#             : agentID - value that uniquely identify the DUT
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    expectedresult = "SUCCESS"
    returnStatus = "FAILURE"
    usppaStatus = "FAILURE"
    controllerStatus = "FAILURE"
    agentStatus = "FAILURE"

    print("\nChecking the PREREQUISITES")
    #Check for the usppa process
    print("Check if Usppa process is up and running in the device")
    cmd= "pidof UspPa"
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    tdkTestObj.addParameter("command", cmd)
    tdkTestObj.executeTestCase(expectedresult)
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails().strip().replace("\\n", "")
    print("Pid of usppa :%s "%details)
    if expectedresult in actualresult and details.isdigit():
        print("Usppa process is up and running")
        usppaStatus = "SUCCESS"
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        #Check for every 1 min whether the process is up
        retryCount = 0
        MAX_RETRY = 5
        while retryCount < MAX_RETRY:
            sleep(60)
            tdkTestObj.executeTestCase(expectedresult)
            actualresult = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails().strip().replace("\\n", "")
            print(f"Interation {retryCount}, PID : {details}")
            if expectedresult in actualresult and details.isdigit():
                print("Usppa process is up and running in device")
                usppaStatus = "SUCCESS"
                tdkTestObj.setResultStatus("SUCCESS")
                break;
            else:
                retryCount = retryCount + 1
            tdkTestObj.setResultStatus("FAILURE");
    if usppaStatus == "SUCCESS":
        #Check for controller status
        print(f"Check the Controller status by checking the admin status")
        USP_ADMIN_URL = CONTROLLER_URI + f"/api/auth/admin/exists"
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.get(USP_ADMIN_URL, headers=headers)
            if response.status_code == 200 and response.text.strip().lower()== 'true':
                print(f"Controller is up and there is an admin")
                controllerStatus = "SUCCESS"
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print(f"Controller is down or no admin exists ,please check controller setup")
                tdkTestObj.setResultStatus("FAILURE")
        except Exception as e:
            # catches any unexpected errors
             print(f"[UNEXPECTED ERROR] {e}")
             tdkTestObj.setResultStatus("FAILURE")
    if usppaStatus == "SUCCESS" and controllerStatus == "SUCCESS":
        #Get the Agent Endpoint ID for the operation specific query
        print("Get the Agent Endpoint ID for the operations")
        cmd= "UspPa -c get Device.LocalAgent.EndpointID"
        tdkTestObj.addParameter("command",cmd)
        tdkTestObj.executeTestCase(expectedresult)
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        if expectedresult in actualresult and "Device.LocalAgent.EndpointID => " in details:
            #Set the result status of execution
            agentID = details.split("=>")[1].strip().replace("\\n", "")
            print(f"Agent Endpoint ID : {agentID}")
            print("Got the Agent Endpoint ID sucessfully")
            agentStatus = "SUCCESS"
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print("Failed to get the Agent Endpoint ID")
            tdkTestObj.setResultStatus("FAILURE")
    if usppaStatus == "SUCCESS" and controllerStatus == "SUCCESS" and agentStatus == "SUCCESS":
        #Prerequiiste success check
        returnStatus = "SUCCESS"
        print("PREREQUISITES are success\n")
        return tdkTestObj,agentID,returnStatus
    else:
        return tdkTestObj,None,returnStatus
########## End of Function ##########
