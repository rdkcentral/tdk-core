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
        allow_partial = parameter.get("allow_partial")
        if isinstance(allow_partial, str):
            allow_partial = allow_partial.lower() == "true"
        obj_path,param = name.rsplit('.', 1)
        payload = {"header": {"msg_id": msgid, "msg_type": "SET"}, "body": {"request": {"set": {"allow_partial": allow_partial,"update_objs": [{"obj_path": f"{obj_path}.","param_settings": [{"param": param,"value": value, "required": True}]}]}}}}

    elif method == "get_supported_protocol":
        #Query for GET_SUPPORTED_PROTO operation
        headers = {"Content-Type": "application/json","Authorization": token}
        payload = {"header": {"msg_id": msgid, "msg_type": "GET_SUPPORTED_PROTO"}, "body": {"request": {"get_supported_protocol": {"controller_supported_protocol_versions": "1.0"}}}}

    elif method == "get_supported_dm":
        #Query for GET_SUPPORTED_DM operation
        name = parameter.get("name")
        ret_param = parameter.get("ret_params")
        ret_cmd = parameter.get("ret_cmd")
        ret_event =parameter.get("ret_event")
        first_level_only = parameter.get("first_level_only")

        if isinstance(first_level_only, str):
            first_level_only = first_level_only.lower() == "true"
        if isinstance(ret_param, str):
            ret_param = ret_param.lower() == "true"
        if isinstance(ret_cmd, str):
            ret_cmd = ret_cmd.lower() == "true"
        if isinstance(ret_event, str):
            ret_event = ret_event.lower() == "true"
        payload = {"header": {"msg_id": msgid, "msg_type": "GET_SUPPORTED_DM"}, "body": {"request": {"get_supported_dm": {"obj_paths": [name],"first_level_only" : first_level_only,"return_commands": ret_cmd,"return_events": ret_event,"return_params": ret_param}}}}

    elif method == "get_instances":
        #Query for GET_INSTANCES operation
        name = parameter.get("name")
        first_level_only = parameter.get("first_level_only")
        if isinstance(first_level_only, str):
            first_level_only = first_level_only.lower() == "true"
        payload = {"header": {"msg_id": msgid, "msg_type": "GET_INSTANCES"}, "body": {"request": {"get_instances": { "obj_paths": [name],"first_level_only": first_level_only}}}}

    elif method == "operate":
        #Query for OPERATE operation
        name = parameter.get("name")
        send_resp = parameter.get("send_resp")
        if isinstance(send_resp, str):
            send_resp  = send_resp.lower() == "true"
        payload = {"header": {"msg_id": msgid, "msg_type": "OPERATE"}, "body": {"request": {"operate": {"command": name ,"command_key": "test61","send_resp": send_resp}}}}

    elif method == "add":
        #Query for ADD  operation
        name = parameter.get("name")
        allow_partial = parameter.get("allow_partial")
        if isinstance(allow_partial, str):
            allow_partial = allow_partial.lower() == "true"
        payload = {"header": {"msg_id": msgid, "msg_type": "ADD"},"body": {"request": {"add": {"allow_partial": allow_partial,"create_objs": [{"obj_path": name,"param_settings": [{"param": "Enable","value": "true"},{"param": "ID","value": "add1"},{"param": "NotifType","value": "ValueChange"},{"param": "ReferenceList","value": "Device.LocalAgent.SoftwareVersion","required": True}]}]}}}}
    elif method == "delete":
        name = parameter.get("name")
        allow_partial = parameter.get("allow_partial")
        if isinstance(allow_partial, str):
            allow_partial = allow_partial.lower() == "true"
        payload = {"header": {"msg_id": msgid, "msg_type": "DELETE"},"body": {"request": {"delete": {"allow_partial": allow_partial,"obj_paths": [name]}}}}
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

def parseUsppaResponse(response, method="get", scenario="positive"):
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
            all_values = {}
            #When test scenario is positive
            if scenario == "positive":
                req_results = responseDict.get("req_path_results", [{}])[0].get("resolved_path_results", [])
                for resolved in req_results:
                    result_params = resolved.get("result_params", {})
                    resolved_path = resolved.get("resolved_path", "")
                    if param:
                        # Single parameter case only, look for this param
                        if param in result_params:
                            all_values = result_params[param]
                    else:
                        # Object case, collect all params with full paths
                        for k, v in result_params.items():
                            all_values[f"{resolved_path}{k}"] = v
            #When test scenario is negative
            elif scenario == "negative":
                req_results = responseDict.get("req_path_results", [{}])[0]
                requested_path = req_results.get("requested_path")
                err_code = req_results.get("err_code")
                err_msg = req_results.get("err_msg")
                if requested_path and err_code and err_msg:
                    print(f"Requested path : {requested_path}")
                    print(f"Error code : {err_code}")
                    print(f"Error message : {err_msg}")
                    #Check if requested path matches with query input and an appropriate error code
                    if requested_path == dmParam and err_code:
                        print("Requested path matches with query input and returned an appropriate error code")
                        all_values = True
                    else:
                        print("Requested path doesn't match with query input and an unexpected error code")
                        all_values = False
                else:
                    print("Empty Requested path or error code or error message")
                    all_values = False
            if all_values:
                print("Agent proccesses correctly the expected behaviour for specific get scenario")
                return ["SUCCESS", all_values]
            else:
                print("Agent failed to proccess the expected behaviour for specific get scenario")
                return ["FAILURE", all_values]

        elif method == "set":
            #split the object path and parameter name
            dmParam = usppaQuery.parameter_list[0]['name']
            obj_path,param = dmParam.rsplit('.', 1)
            #Parse the response from set operation
            value = (responseDict.get("updated_obj_results", [{}])[0].get("oper_status", {}).get("OperStatus", {}).get("OperSuccess", {}).get("updated_inst_results", [{}])[0].get("updated_params", {}).get(param))
            if value:
                print("Agent proccesses correctly the expected behaviour for specific set scenario")
                return ["SUCCESS",value]
            else:
                print("Failed to get updated_obj_results or oper_status or OperStatus or OperSuccess or updated_inst_results or updated_params element in response")
                return ["FAILURE",value]

        elif method == "get_supported_protocol":
            #Parse the response from get_supported_protocol operation
            value = responseDict.get("agent_supported_protocol_versions")
            #Check if expected response returned or not
            if value:
                print("agent_supported_protocol_versions element is avaialble in response")
                return ["SUCCESS",value]
            else:
                print("Failed to get agent_supported_protocol_versions element in response")
                return ["FAILURE",value]

        elif method == "get_supported_dm":
            #Parse the response from get_supported_dm operation
            params_list = []
            commands_list = []
            events_list = []
            metadata_list = []
            dmParam = usppaQuery.parameter_list[0]['name']
            ret_param = usppaQuery.parameter_list[0]['ret_param']
            ret_cmd = usppaQuery.parameter_list[0]['ret_cmd']
            ret_event = usppaQuery.parameter_list[0]['ret_event']
            if scenario == "negative":
                obj_results = responseDict.get("req_obj_results", [])
                if obj_results:
                    obj = obj_results[0]
                    requested_path = obj.get("req_obj_path","")
                    err_code = obj.get("err_code", "")
                    err_msg =  obj.get("err_msg", "")
                    if requested_path and err_code and err_msg:
                        print(f"Requested Path : {requested_path}")
                        print(f"Error code : {err_code}")
                        print(f"Error Message : {err_msg}")
                        if dmParam == requested_path and err_code:
                            print("Agent correctly process the param_errs element containing a single error with a param_path of {dmParam} , and an appropriate error code")
                            value = True
                            return ["SUCCESS",value]
                        else:
                            print(f"Agent failed to process param_errs element containing a single error with a param_path of {dmParam} , and an appropriate error code.")
                            value = False
                            return["FAILURE",value]
                    else:
                        print("Requested Path or Error code or Error Message is empty")
                        value = False
                        return["FAILURE",value]
                else:
                    print("Empty req_obj_results element")
                    value = False
                    return["FAILURE",value]

            elif scenario == "positive":
                missing_param, missing_cmd, missing_event = [], [], []
                for obj_result in responseDict.get("req_obj_results", []):
                    data_model_inst_uri = obj_result.get("data_model_inst_uri", "")
                    for obj in obj_result.get("supported_objs", []):
                        base_path = obj.get("supported_obj_path", "")
                        metadata = {"supported_obj_path": base_path,"access": obj.get("access"),"is_multi_instance": obj.get("is_multi_instance")}
                        metadata_list.append(metadata)
                        #Filter out the parameters
                        param_check =  obj.get("supported_params", [])
                        cmd_check = obj.get("supported_commands", [])
                        event_check = obj.get("supported_events", [])

                        #Filter out the parameters
                        if ret_param:
                            for param in obj.get("supported_params", []):
                                parameter = f"{base_path}{param['param_name']}"
                                required_fields = ["param_name", "access", "value_type", "value_change"]
                                missing_param = [f for f in required_fields if f not in param]
                                if missing_param:
                                    print(f"Parameter at {parameter} missing fields: {missing_param}")
                                    break
                                params_list.append({"parameter": parameter,**{k: v for k, v in param.items() if k != "param_name"}})
                        else:
                            if param_check:
                                print("Supported parameter list is not empty for return_parameters set to False")
                                value = False
                                return["FAILURE",value]
                            elif data_model_inst_uri and metadata_list:
                                print("Supported parameter list is empty for return_parameters set to False as expected")
                                value = True
                                return["SUCCESS",value]

                        #Filter out the commands
                        if ret_cmd:
                            for cmd in obj.get("supported_commands", []):
                                command = f"{base_path}{cmd['command_name']}"
                                required_fields = ["command_name", "command_type"]
                                missing_cmd = [f for f in required_fields if f not in cmd]
                                if missing_cmd:
                                    print(f"Command at {command} missing fields: {missing_cmd}")
                                    break
                                commands_list.append({"command": command,**{k: v for k, v in cmd.items() if k != "command_name"}})
                        else:
                            if cmd_check:
                                print("Supported command list is not empty for return_commands set to False")
                                value = False
                                return["FAILURE",value]
                            elif data_model_inst_uri and metadata_list :
                                print("Supported command list is empty for return_commands set to False as expected")
                                value = True
                                return["SUCCESS",value]

                        #Filter out the events
                        if ret_event:
                            for event in obj.get("supported_events", []):
                                eventName = f"{base_path}{event['event_name']}"
                                required_fields = ["event_name"]
                                missing_event = [f for f in required_fields if f not in event]
                                if missing_event:
                                    print(f"Event at {eventName} missing fields: {missing_event}")
                                    break
                                events_list.append({"event": eventName,**{k: v for k, v in event.items() if k != "event_name"}})
                        else:
                            if event_check:
                                print("Supported event list is not empty for return_events set to False")
                                value = False
                                return["FAILURE",value]
                            elif data_model_inst_uri and metadata_list :
                                print("Supported event list is empty for return_events set to False as expected")
                                value = True
                                return["SUCCESS",value]
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

                missing = 0
                if missing_param or missing_cmd or missing_event:
                    missing = 1
                #Check if data model uri, metadata are present and there is no missing in supported types
                if data_model_inst_uri and metadata_list and not missing:
                    print("Data model uri and metadata are present and there is no missing in fields of supported types")
                    value = True
                    return ["SUCCESS",value]
                else:
                    print("Failed to get the req_obj_results element or sub elements like SupportedParamResult or SupportedCommandResult or SupportedEventResult as expected in the response")
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
            #Check if requested path and instantiated path are not empty
            if requested_path and instant_paths:
                print("Requested path and instantiated path are not empty")
                value = True
                return ["SUCCESS",value]
            else:
                print("Empty Requested path or instantiated path")
                value = False
                return["FAILURE",value]

        elif method == "operate":
            #Parse the response from operate operation
            send_resp = usppaQuery.parameter_list[0]['send_resp']
            name = usppaQuery.parameter_list[0]['name']
            if isinstance(send_resp, str):
                send_resp  = send_resp.lower() == "true"
            if send_resp == True:
                executed_cmd, req_output_args = responseDict.get("operation_results",[{}])[0].get("executed_command"), responseDict.get("operation_results",[{}])[0].get("OperationResp",{}).get("ReqOutputArgs")
                #Check for executed command and expect output arguement as empty
                if executed_cmd == name and req_output_args == {}:
                    print("executed_cmd is having reboot command and output arguement is empty as expected")
                    value = True
                    return ["SUCCESS",value]
                else:
                    print("Incorrect Exexcute command or non-empty output arguements")
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
            #Check if instance number and parameter list are not empty
            if instance_number and params:
                print("Instance number and parameter list are not empty")
                return ["SUCCESS",value]
            else:
                print("Empty instance number or parameters")
                return ["FAILURE",value]

        elif method == "delete":
            #Parse the response from delete operation
            dmParam = usppaQuery.parameter_list[0]['name']
            allow_partial = usppaQuery.parameter_list[0]['allow_partial']
            if isinstance(allow_partial, str):
                allow_partial  = allow_partial.lower() == "true"
            deleted_objs = responseDict.get("deleted_obj_results", [])
            if scenario == "positive":
                if deleted_objs:
                    obj = deleted_objs[0]
                    requested_path = obj.get("requested_path")
                    affected_paths = (obj.get("oper_status", {}).get("OperStatus", {}).get("OperSuccess", {}).get("affected_paths", []))
                    if requested_path and requested_path in affected_paths:
                        print(f"Affected Path : {affected_paths}")
                        print("Requested path is same as the Affected path")
                        value = True
                        return ["SUCCESS",value]
                    else:
                        print("Empty Requested path or Requested path not in Affected path")
                        value = False
                        return ["FAILURE",value]
                else:
                    print("Empty deleted_objs element")
                    value = False
                    return ["FAILURE",value]

            #negative scenarios
            elif scenario == "negative":
                #invalid object/object instance with allow_partial false
                if allow_partial == False :
                    if not deleted_objs:
                        top_err_code =  responseDict.get("err_code")
                        top_err_msg =  responseDict.get("err_msg")
                        param_err =  responseDict.get("param_errs", [{}])[0]
                        param_path = param_err.get("param_path")
                        param_err_code = param_err.get("err_code")
                        param_err_msg = param_err.get("err_msg")
                        if top_err_code and top_err_msg and param_err and param_path and param_err_code and param_err_msg:
                            print(f"Generic Error code : {top_err_code}")
                            print(f"Generic Error Message : {top_err_msg}")
                            print(f"Parameter Path : {param_path}")
                            print(f"Parameter Error code : {param_err_code}")
                            print(f"Parameter Error message : {param_err_msg}")
                        #Check if parameter path matches the queried parameter and has an appropriate error code
                        if param_path == dmParam and param_err_code:
                            print("Parameter path matches the queried parameter and has an appropriate error code")
                            value = True
                            return ["SUCCESS",value]
                        else:
                            print("Parameter Path is not in requested query or unexpected error code")
                            value = False
                            return ["FAILURE",value]
                    else:
                        obj = deleted_objs[0]  # take the first element
                        requested_path = obj.get("requested_path",{})
                        oper_success = (obj.get("oper_status", {}).get("OperStatus", {}))
                        result_invalidObjectInstance = oper_success.get("OperSuccess", {})
                        if oper_success:
                            if requested_path:
                                print(f"Requested Path : {requested_path}")
                            if result_invalidObjectInstance == {}:
                                print("Opersuccess element is empty as expected")
                                value = True
                                return ["SUCCESS",value]
                            else:
                                print("Opersuccess element is not empty as expected")
                                value = False
                                return ["FAILURE",value]
                        else:
                            print("Opersuccess element is not empty as expected")
                            value = False
                            return ["FAILURE",value]

                #invalid object instance and invalid object with allow_partial as True
                elif allow_partial == True:
                    obj = deleted_objs[0]  # take the first element
                    requested_path = obj.get("requested_path",{})
                    oper_success = (obj.get("oper_status", {}).get("OperStatus", {}))
                    result_invalidObjectInstance = oper_success.get("OperSuccess", {})
                    result_invalidObject = oper_success.get("OperFailure", {})
                    if requested_path:
                        print(f"Requested Path : {requested_path}")
                    # invalid object with allow_partial as True
                    if result_invalidObject:
                        err_code = result_invalidObject.get("err_code")
                        err_msg = result_invalidObject.get("err_msg")
                        if err_code and err_msg:
                            print(f"Error code : {err_code}")
                            print(f"Error message : {err_msg}")
                        #Check if requested path matches the queried parameter and has an appropriate error code
                        if requested_path == dmParam and err_code:
                            print("Requested path matches the queried parameter and has an appropriate error code")
                            value = True
                            return ["SUCCESS",value]
                        else:
                            print("Opersuccess element is not empty as expected")
                            value = False
                            return ["FAILURE",value]
                    #invalid object instance with allow_partial as True
                    else:
                        if result_invalidObjectInstance == {}:
                            print("Opersuccess element is empty as expected")
                            value = True
                            return ["SUCCESS",value]
                        else:
                            print("Opersuccess element is not empty as expected")
                            value = False
                            return ["FAILURE",value]

        #Invalid method passes
        else:
            print("Invalid method")
            value = False
            return ["FAILURE",value]
    #empty response for the request
    else:
        print("Empty response for the request")
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
