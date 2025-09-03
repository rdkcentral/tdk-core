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
from tdkbVariables import *;
from tdkutility import *
from WebconfigVariables import *
import json


#getMacAddress
# Syntax      : getMacAddress(obj)
# Description : Function to get the MAC address of the device
# Parameters  : obj - module object
# Return Value: tdkTestObj - test object
#               actualresult - result of the command execution
#               ret_value - MAC address of the device

def getMacAddress(obj):
    estbMAC = ""
    query = "sh %s/tdk_platform_utility.sh getCMMACAddress" %TDK_PATH
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj,query)
    estbMAC = details.strip().replace(":","").upper()
    return tdkTestObj, actualresult, estbMAC
########## End of function ##########

#setWebconfigTrigger
# Syntax      : setWebconfigTrigger(obj, value, step)
# Description : Function to set the Device.X_RDK_WebConfig.ForceSync trigger parameter
# Parameters  : obj - module object
#               value - value to be set for the trigger parameter
#               step - step number for logging
# Return Value: flag - 0 if the value is set successfully, 1 if it fails

def setWebconfigTrigger(obj, value, step):
    expectedresult = "SUCCESS"
    flag = 0
    print("\nTEST STEP %d : Set the Device.X_RDK_WebConfig.ForceSync to %s" %(step,value))
    print("EXPECTED RESULT %d: The value must be set successfully" %step)

    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_SetOnly')
    tdkTestObj.addParameter("ParamName","Device.X_RDK_WebConfig.ForceSync")
    tdkTestObj.addParameter("ParamValue", value)
    tdkTestObj.addParameter("Type", "string")
    tdkTestObj.executeTestCase("SUCCESS")
    actualresult = tdkTestObj.getResult()

    if expectedresult in actualresult:
        print("ACTUAL RESULT %d: The value is set successfully." %step)
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        flag = 1
        print("ACTUAL RESULT %d: Failed to set the value." %step)
        tdkTestObj.setResultStatus("FAILURE")
    return flag
########### End of function ##########

#configureWebconfigSettings
# Syntax      : configureWebconfigSettings(obj, mac, values)
# Description : Function to configure the Device.X_RDK_WebConfig settings
# Parameters  : obj - module object
#               values - value to be set for the settings if provided, default None
#               mac - Mac address of DUT
# Return Value: tdkTestObj - object
#               getValue - List of current values of the parameters before setting
#               flag - 0 if all values are set successfully, 1 if any fails

def configureWebconfigSettings(obj, mac, values=None):
    flag = 0
    expectedresult = "SUCCESS"
    params = ["Device.X_RDK_WebConfig.URL","Device.X_RDK_WebConfig.SupplementaryServiceUrls.Telemetry"]

    getValue = []
    # If values is not provided, use default URL
    if values == None:
        url = f"{WEBCONFIG_URL}:9007/api/v1/device/{mac}/config"
        values = [url] * 2

    webconfig_params = dict(zip(params, values))
    print("\n Webconfig Settings to be set : %s \n" %webconfig_params)

    for param, setValue in webconfig_params.items():
        tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Get')
        result, current_value = getTR181Value(tdkTestObj, param)
        getValue.append(current_value)
        if expectedresult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"Retrieved {param} successfully: {current_value}\n")

            if current_value != setValue:
                tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Set')
                setResult, details = setTR181Value(tdkTestObj, param, setValue, "string")
                if setResult != expectedresult:
                    flag = 1
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"Failed to set {param}. Details: {details}\n")
                else:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"Successfully Set {param} to {setValue}\n")
            else:
                print(f"{param} is already set correctly.\n")

        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"Failed to retrieve {param}. Result: {result}\n")

    return tdkTestObj, flag, getValue
########### End of function ##########

#getMultipleParams
# Syntax      : getMultipleParams(obj, paramList)
# Description : Function to get multiple DM values
# Parameters  : obj - module object
#               paramList - List of Parameters/DMs to be set
# Return Value: tdkTestObj - object
#               result - list of SUCCESS/FAILURE for each param
#               details - Get values of DMs

def getMultipleParams(obj, paramList):
    result = [None] * len(paramList)
    values = [None] * len(paramList)

    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Get')
    for index in range(len(paramList)):
        print("\n Getting parameter: %s" %paramList[index])
        result[index], values[index] = getTR181Value(tdkTestObj, paramList[index])

    details = dict(zip(paramList, values))
    print("Retrieved values: ", details)
    return tdkTestObj, result, details
########### End of function ##########

#CurlCommand
# Syntax      : CurlCommand(obj, subdoc_name, paramname, subdoc_info, mac)
# Description : Function to create and execute curl command to update subdocs via webconfig server
# Parameters  : obj - module object
#               subdoc_name - Subdoc Name
#               paramname - Parameter Name for the paricular subdoc
#               subdoc_info - subdoc information in the specified format
#               mac - Mac address of DUT
# Return Value: tdkTestObj - object
#               actualresult - SUCCESS/FAILURE
#               details - Get values of DMs

def CurlCommand(obj, subdoc_name, paramname, subdoc_info, mac):

    tdkTestObj = obj.createTestStep('ExecuteCmd')

    command = (
    f"curl -s -i \"{WEBCONFIG_URL}:9008/api/v1/device/{mac}/document/{subdoc_name}?param_name={paramname}\" "
    f"-H 'Content-type: application/json' "
    f"--data '{json.dumps(subdoc_info)}' "
    f"-X POST")

    print("Command : %s" %command)
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)

    return tdkTestObj, actualresult, details

########### End of function ##########

#getSubdocInfo
# Syntax      : getSubdocInfo(subdoc_name, subdoc_type, WIFI_RADIO="")
# Description : Function to get subdoc info in the specified json request format
# Parameters  : subdoc_name - Subdoc Name
#               subdoc_type - pos/neg for Positive/Negative cases
#               WIFI_RADIO - 2g, 5g, or 6g. Only used in the case of private_ssid subdoc. Defult is empty.
#               radio_entries - No of radio entries supported in the platform
#               initial_param_values - Values to be reverted in case of negative scenario for lan and private_ssid subdocs. Default is None.
# Return Value: subdoc_info : Subdoc with configurations

def getSubdocInfo(subdoc_name, subdoc_type, WIFI_RADIO="", radio_entries=0, initial_param_values=None):

    subdoc_info = {}
    # Define the subdoc information based on the subdoc name and subdoc_type

    if subdoc_name == "lan":
        start_ip, end_ip = DHCP_START_IP, DHCP_END_IP
        if subdoc_type == "neg":
            start_ip, end_ip = end_ip, start_ip

        subdoc_info = {
            "DhcpServerEnable": DHCP_SERVER_ENABLE,
            "LanIPAddress": LAN_IP,
            "LanSubnetMask": LAN_SUBNET_MASK,
            "DhcpStartIPAddress": start_ip,
            "DhcpEndIPAddress": end_ip,
            "LeaseTime": LEASE_TIME
        }

        if initial_param_values != None:
            subdoc_info = dict(zip(subdoc_info.keys(), initial_param_values.values()))
            subdoc_info["LeaseTime"] = int(subdoc_info["LeaseTime"])
            revert_value = iter(initial_param_values.values())
            for key in subdoc_info.values():
                if isinstance(key, dict):
                    for k in key.keys():
                        key[k] = next(revert_value)
                else:
                    # If key is not a dict, assign directly
                    key = next(revert_value)



    elif subdoc_name == "portforwarding":
        internalclient = INTERNAL_CLIENT
        # If subdoc_type is negative, set an invalid internal client IP
        if subdoc_type == "neg":
            internalclient = "10:0.0.123"
        subdoc_info = [{
            "InternalClient": internalclient,
            "ExternalPortEndRange": EXTERNAL_PORT_END_RANGE,
            "Enable": PORTFORWARDING_ENABLE,
            "Protocol": PROTOCOL,
            "Description": DESCRIPTION,
            "ExternalPort": EXTERNAL_PORT
        }]

    elif subdoc_name == "privatessid":
        if  radio_entries == 0 or initial_param_values == None:
            print("\nWifi parameters are not defined properly.")
        else:
            radios = ["2g", "5g"] if radio_entries == 2 else ["2g", "5g", "6g"]

            for r in radios:
                subdoc_info[f"private_ssid_{r}"] = {"SSID": "", "Enable": "", "SSIDAdvertisementEnabled": ""}
                subdoc_info[f"private_security_{r}"] = {"EncryptionMethod": "", "ModeEnabled": "", "Passphrase": ""}

            AP = 0

            for r in radios:
                initial_value = initial_param_values[r]
                if r == "2g":
                    AP = 1 #Private AP for 2.4G Radio
                elif r == "5g":
                    AP = 2 #Private AP for 5G Radio
                elif r == "6g":
                    AP = 17 #Private AP for 6G Radio

                #If the r is the target radio, the values will be taken from WebconfigVariables file otherwise it will be fetched from initial list
                if r == WIFI_RADIO:
                    if subdoc_type == "neg":
                        temp = globals()[f"SSID_NAME_{r}"]
                        globals()[f"SSID_NAME_{r}"] = "abcbaaba1234567ab-cabacabacabsbcagsafdgyw"

                    # Assign values from WebconfigVariables.py for the target radio (lowercase)
                    subdoc_info[f"private_ssid_{r}"] = {
                        "SSID": globals()[f"SSID_NAME_{r}"],
                        "Enable": globals()[f"SSID_ENABLE_{r}"],
                        "SSIDAdvertisementEnabled": globals()[f"SSID_ADVERTISEMENT_ENABLED_{r}"]
                    }
                    subdoc_info[f"private_security_{r}"] = {
                        "EncryptionMethod": globals()[f"ENCRYPTION_METHOD_{r}"],
                        "ModeEnabled": globals()[f"SECURITY_MODE_ENABLED_{r}"],
                        "Passphrase": globals()[f"SECURITY_PASSPHRASE_{r}"]
                    }

                    if subdoc_type == "neg":
                        globals()[f"SSID_NAME_{WIFI_RADIO}"] = temp

                else:
                    # Use initial_param_values for other radios
                    subdoc_info[f"private_ssid_{r}"] = {
                        "SSID": initial_value[f"Device.WiFi.SSID.{AP}.SSID"],
                        "Enable": initial_value[f"Device.WiFi.SSID.{AP}.Enable"],
                        "SSIDAdvertisementEnabled": initial_value[f"Device.WiFi.AccessPoint.{AP}.SSIDAdvertisementEnabled"]
                    }
                    subdoc_info[f"private_security_{r}"] = {
                        "EncryptionMethod": initial_value[f"Device.WiFi.AccessPoint.{AP}.Security.X_CISCO_COM_EncryptionMethod"],
                        "ModeEnabled": initial_value[f"Device.WiFi.AccessPoint.{AP}.Security.ModeEnabled"],
                        "Passphrase": initial_value[f"Device.WiFi.AccessPoint.{AP}.Security.X_COMCAST-COM_KeyPassphrase"]
                    }

    else:
        print("Invalid subdoc name provided")

    return subdoc_info
########### End of function ##########

#getPartialSubdocInfo
# Syntax      : getPartialSubdocInfo(subdoc_info)
# Description : Function to get partial subdoc info by removing one key-value pair
# Parameters  : subdoc_info - Subdoc information
# Return Value: subdoc_info - Partial Subdoc with configurations

def getPartialSubdocInfo(subdoc_info):
    if isinstance(subdoc_info, dict):
        if all(isinstance(value, dict) for value in subdoc_info.values()):
            for item in subdoc_info.values():
                item.popitem()
        else:
            subdoc_info.popitem()
    elif isinstance(subdoc_info, list):
        for item in subdoc_info:
            if isinstance(item, dict):
                item.popitem()
    return subdoc_info

########### End of function ##########

#extractValues
# Syntax      : extractValues(info)
# Description : Function to extract all values from a nested dictionary or list
# Parameters  : info - nested dictionary or list
# Return Value: values - list of extracted values

def extractValues(info):
    values = []
    if isinstance(info, dict):
        for value in info.values():
            if isinstance(value, dict):
                values.extend(extractValues(value))
            else:
                values.append(value)
    elif isinstance(info, list):
        for item in info:
            if isinstance(item, dict):
                values.extend(extractValues(item))
            else:
                values.append(item)
    return values
########### End of function ##########


