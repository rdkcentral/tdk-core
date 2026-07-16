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
import tdklib
from time import sleep
from RFCVariables import *
from tdkutility import *
import json
import requests
from tdkbVariables import *

# get_mac
# Syntax      : get_mac(obj)
# Description : Function to get the device MAC address
# Parameters  : obj - module object
# Return Value: tdkTestObj - test object
#               actualresult - result of the command execution
#               mac - retrieved MAC address
def get_mac(obj):
    query_mac = "sh %s/tdk_platform_utility.sh getCMMACAddress" % TDK_PATH
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, mac = doSysutilExecuteCommand(tdkTestObj, query_mac)
    mac = mac.strip().replace(":", "").upper()
    return tdkTestObj, actualresult, mac
########## End of function ##########

# rfc_configure_feature
# Syntax      : rfc_configure_feature(obj, feature_id, name, param_value_dict)
# Description : Function to configure a feature on the XConf server
# Parameters  : obj - module object
#               feature_id - unique ID for the feature
#               name - feature name
#               param_value_dict - dictionary with clean parameters as keys and values to set
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - response from CURL command
def rfc_configure_feature(obj, feature_id, name, param_value_dict):
    # Always treat as dictionary and add tr181 prefix to all parameters
    config_data = {f"tr181.{param}": value for param, value in param_value_dict.items()}
    json_data = {
        "id": feature_id,
        "name": name,
        "effectiveImmediate": True,
        "enable": True,
        "whitelisted": False,
        "configData": config_data,
        "whitelistProperty": {},
        "applicationType": "stb",
        "featureInstance": name
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-KEY": XCONF_API_KEY
    }
    url = f"{XCONF_URL}/feature?applicationType=stb"
    print("POST %s" % url)
    print("Payload: %s" % json.dumps(json_data))
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    tdkTestObj.executeTestCase("SUCCESS")
    try:
        resp = requests.post(url, headers=headers, json=json_data, timeout=30)
        details = resp.text
        print("Response [%d]: %s" % (resp.status_code, details))
        if not resp.ok or not config_data:
            actualresult = "FAILURE"
        else:
            missing = [p for p, v in config_data.items() if p not in details or str(v) not in details]
            actualresult = "SUCCESS" if (name in details and not missing) else "FAILURE"
    except Exception as e:
        details = str(e)
        actualresult = "FAILURE"
        print("Exception during rfc_configure_feature: %s" % details)
    return tdkTestObj, actualresult, details
########## End of function ##########

# rfc_set_feature_rule
# Syntax      : rfc_set_feature_rule(obj, rule_id, name, mac)
# Description : Function to set a feature rule on the XConf server with estbMacAddress
# Parameters  : obj - module object
#               rule_id - unique ID for the rule
#               name - feature name
#               mac - device MAC address
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - response from CURL command
def rfc_set_feature_rule(obj, rule_id, name, mac):
    json_data = {
        "id": rule_id,
        "name": name,
        "rule": {
            "negated": False,
            "condition": {
                "freeArg": {"type": "STRING", "name": "estbMacAddress"},
                "operation": "IS",
                "fixedArg": {"bean": {"value": {"java.lang.String": mac}}}
            },
            "compoundParts": []
        },
        "priority": 1,
        "featureIds": [rule_id],
        "applicationType": "stb"
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-KEY": XCONF_API_KEY
    }
    url = f"{XCONF_URL}/featurerule?applicationType=stb"
    print("POST %s" % url)
    print("Payload: %s" % json.dumps(json_data))
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    tdkTestObj.executeTestCase("SUCCESS")
    try:
        resp = requests.post(url, headers=headers, json=json_data, timeout=30)
        details = resp.text
        print("Response [%d]: %s" % (resp.status_code, details))
        if name in details and mac.replace(":", "").upper() in details.replace(":", "").upper():
            actualresult = "SUCCESS"
        else:
            actualresult = "FAILURE"
    except Exception as e:
        details = str(e)
        actualresult = "FAILURE"
        print("Exception during rfc_set_feature_rule: %s" % details)
    return tdkTestObj, actualresult, details
########## End of function ##########

# rfc_validate_feature_rule
# Syntax      : rfc_validate_feature_rule(obj, mac, feature_name, param_value_dict)
# Description : Function to validate the feature rule using a GET request with MAC
# Parameters  : obj - module object
#               mac - device MAC address
#               feature_name - name of the feature to validate
#               param_value_dict - dictionary with clean parameters and values expected in response
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - response from CURL command
def rfc_validate_feature_rule(obj, mac, feature_name, param_value_dict):
    sleep(30)
    url = f"{RFC_URL}?estbMacAddress={mac}"
    print("GET %s" % url)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    tdkTestObj.executeTestCase("SUCCESS")
    try:
        resp = requests.get(url, timeout=30)
        details = resp.text
        print("Response [%d]: %s" % (resp.status_code, details))
        # Normalize JSON to avoid whitespace/formatting issues
        try:
            normalized = json.dumps(resp.json(), separators=(",", ":"))
        except ValueError:
            normalized = details
        is_valid = False
        if feature_name in normalized:
            is_valid = any(f'"tr181.{param}":"{value}"' in normalized for param, value in param_value_dict.items())
        actualresult = "SUCCESS" if (resp.ok and is_valid) else "FAILURE"
    except Exception as e:
        details = str(e)
        actualresult = "FAILURE"
        print("Exception during rfc_validate_feature_rule: %s" % details)
    return tdkTestObj, actualresult, details
########## End of function ##########

# rfc_restart_service
# Syntax      : rfc_restart_service(obj)
# Description : Function to restart the RFC service
# Parameters  : obj - module object
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - status of the service
def rfc_restart_service(obj):
    command = "systemctl restart rfc"
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    sleep(10)
    status_cmd = "systemctl status rfc | grep 'Active:'"
    actualresult_status, status_details = doSysutilExecuteCommand(tdkTestObj, status_cmd)
    if "active" in status_details and ("running" in status_details or "exited" in status_details):
        details += "\n" + status_details
        return tdkTestObj, "SUCCESS", details
    else:
        details += "\n" + status_details
        return tdkTestObj, "FAILURE", details
########## End of function ##########

# rfc_revert_dm_value
# Syntax      : rfc_revert_dm_value(sysobj, obj, feature_id, name, param_value_dict)
# Description : Function to revert DM values by updating the existing feature with PUT command
# Parameters  : sysobj - sysutil module object for executing curl commands
#               obj - tr181 module object for get DM operations
#               feature_id - unique ID for the feature
#               name - feature name
#               param_value_dict - dictionary with clean parameters as keys and initial values to revert
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - response from CURL command
def rfc_revert_dm_value(sysobj, obj, feature_id, name, param_value_dict):
    # Always treat as dictionary and add tr181 prefix to all parameters
    config_data = {f"tr181.{param}": value for param, value in param_value_dict.items()}
    json_data = {
        "id": feature_id,
        "name": name,
        "effectiveImmediate": True,
        "enable": True,
        "whitelisted": False,
        "configData": config_data,
        "whitelistProperty": {},
        "applicationType": "stb",
        "featureInstance": name
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-KEY": XCONF_API_KEY
    }
    url = f"{XCONF_URL}/feature?applicationType=stb"
    print("PUT %s" % url)
    print("Payload: %s" % json.dumps(json_data))
    tdkTestObj = sysobj.createTestStep('ExecuteCmd')
    tdkTestObj.executeTestCase("SUCCESS")
    try:
        resp = requests.put(url, headers=headers, json=json_data, timeout=30)
        details = resp.text
        actualresult = "SUCCESS" if resp.ok else "FAILURE"
        sleep(60)
        print("Response [%d]: %s" % (resp.status_code, details))
    except Exception as e:
        details = str(e)
        actualresult = "FAILURE"
        print("Exception during rfc_revert_dm_value PUT: %s" % details)
    if "SUCCESS" in actualresult:
        print("PUT command executed successfully.")
        # Restart RFC service to apply the reverted config
        print("Restarting RFC service...")
        _, restart_result, restart_details = rfc_restart_service(sysobj)
        if "SUCCESS" in restart_result:
            print("RFC service restarted successfully")
            sleep(20)
            print("Sleeping for 20 sec after RFC restart...")
            all_reverted = True
            for param, init_val in param_value_dict.items():
                tdkTestObj_Tr181_Get = obj.createTestStep('TDKB_TR181Stub_Get')
                actualresult_get, reverted_value = getTR181Value(tdkTestObj_Tr181_Get, param)
                reverted_value = reverted_value.strip()
                reverted_ok = "SUCCESS" in actualresult_get and reverted_value == str(init_val)
                if reverted_ok:
                    tdkTestObj_Tr181_Get.setResultStatus("SUCCESS")
                    print(f"{param} successfully reverted to {reverted_value}")
                    details += f"\n{param} successfully reverted to {reverted_value}"
                else:
                    tdkTestObj_Tr181_Get.setResultStatus("FAILURE")
                    print(f"Failed to revert {param}: got {reverted_value}, expected {str(init_val)}")
                    details += f"\nFailed to revert {param}: got {reverted_value}, expected {str(init_val)}"
                    all_reverted = False
            actualresult = "SUCCESS" if all_reverted else "FAILURE"
        else:
            actualresult = "FAILURE"
            details += f"\nRFC service restart failed: {restart_details}"
            print("RFC service restart failed: %s" % restart_details)
    return tdkTestObj, actualresult, details
########## End of function ##########

# rfc_delete_feature_rule
# Syntax      : rfc_delete_feature_rule(obj, feature_id)
# Description : Function to delete a feature rule from the XConf server
# Parameters  : obj - module object
#               feature_id - unique ID for the rule
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - response from CURL command
def rfc_delete_feature_rule(obj, feature_id):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-KEY": XCONF_API_KEY
    }
    url = f"{XCONF_URL}/featurerule/{feature_id}?applicationType=stb"
    print("DELETE %s" % url)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    tdkTestObj.executeTestCase("SUCCESS")
    try:
        resp = requests.delete(url, headers=headers, timeout=30)
        details = resp.text
        print("Response [%d]: %s" % (resp.status_code, details))
        actualresult = "SUCCESS" if resp.status_code in (200, 204) else "FAILURE"
        if actualresult == "FAILURE":
            print(details)
        sleep(20)
    except Exception as e:
        details = str(e)
        actualresult = "FAILURE"
        print("Exception during rfc_delete_feature_rule: %s" % details)
    return tdkTestObj, actualresult, details
########## End of function ##########

# rfc_delete_feature
# Syntax      : rfc_delete_feature(obj, feature_id)
# Description : Function to delete a feature from the XConf server
# Parameters  : obj - module object
#               feature_id - unique ID for the feature
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - response from CURL command
def rfc_delete_feature(obj, feature_id):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-KEY": XCONF_API_KEY
    }
    url = f"{XCONF_URL}/feature/{feature_id}?applicationType=stb"
    print("DELETE %s" % url)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    tdkTestObj.executeTestCase("SUCCESS")
    try:
        resp = requests.delete(url, headers=headers, timeout=30)
        details = resp.text
        print("Response [%d]: %s" % (resp.status_code, details))
        actualresult = "SUCCESS" if resp.status_code in (200, 204) else "FAILURE"
        if actualresult == "FAILURE":
            print(details)
        sleep(20)
    except Exception as e:
        details = str(e)
        actualresult = "FAILURE"
        print("Exception during rfc_delete_feature: %s" % details)
    return tdkTestObj, actualresult, details
########## End of function ##########

