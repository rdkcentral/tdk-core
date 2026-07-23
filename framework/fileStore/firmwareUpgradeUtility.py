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
#
#
# -----------------------------------------------------------------------------
# module imports
# ------------------------------------------------------------------------------
from firmwareUpgradeVariables import *
from tdkutility import *
from tdkbVariables import *
import json
import time
from time import sleep
from urllib.parse import urlparse


# GetPlatformProperties
# Syntax      : GetPlatformProperties(obj, param)
# Description : Function to locate tdk_platform.properties file and fetch value of the given variable
# Parameters  : obj - module object
#               config_keys - List of variable names to be fetched from the properties file
# Return Value: tdkTestObj - module object
#               actualresult_all - List of actual results for each variable fetched
#               config_values - Dictionary of variable names and their corresponding values

def GetPlatformProperties(obj, config_keys):
    config_values = {}
    actualresult_all = []
    for key in config_keys:
        command = f"sh {TDK_PATH}/tdk_utility.sh parseConfigFile {key}"
        tdkTestObj, actualresult, config_values[key] = get_config_values(
            obj, command)
        actualresult_all.append(actualresult)
    return tdkTestObj, actualresult_all, config_values
########## End of function ##########

# getCurrentFirmware
# Syntax      : getCurrentFirmware(obj, step)
# Description : Function to get the current firmware name from the device
# Parameters  : obj - module object
#               step - test step number
# Return Value: FirmwareVersion - Image name without suffix if successful, else None
#               FirmwareFilename - Image name with suffix if successful, else None


def getCurrentFirmware(obj, step):
    expectedresult = "SUCCESS"
    tdkTestObj, actualresult, value = GetPlatformProperties(obj, ["FW_NAME_SUFFIX"])
    suffix = value["FW_NAME_SUFFIX"]
    # Get details of the current firmware in the device
    if "FAILURE" not in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        print("Fetched FW_NAME_SUFFIX from the tdk_platform.properties successfully.")

        query = 'cat /version.txt | grep -i imagename | cut -c 11- | tr "\n" " "'
        print(f"Query: {query}")

        tdkTestObj = obj.createTestStep('ExecuteCmd')
        actualresult, details = doSysutilExecuteCommand(tdkTestObj, query)

        print(f"TEST STEP {step}: Fetch device's current firmware name")
        print(f"EXPECTED RESULT {step}: Should fetch device's current firmware name")
        print(f"ACTUAL RESULT {step}: Image name {details} ")
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS")
            print("[TEST EXECUTION RESULT] : SUCCESS\n")
            FirmwareVersion = details.strip()
            FirmwareFilename = FirmwareVersion + suffix

            return (FirmwareVersion, FirmwareFilename)
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("[TEST EXECUTION RESULT] : FAILURE\n")
            return (None, None)
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("Failed to fetch FW_NAME_SUFFIX from the tdk_platform.properties.")
        return (None, None)
########## End of function ##########

# getFirmwareDetailsFromServer
# Syntax      : getFirmwareDetailsFromServer(obj, step)
# Description : Function to get the target firmware details and check its availability in the server
# Parameters  : obj - module object
#               step - test step number
# Return Value: FirmwareVersion - Image name without suffix if successful, else None
#               FirmwareFilename - Image name with suffix if successful, else None


def getFirmwareDetailsFromServer(obj, step):
    config_keys = ["DEVICETYPE", "FW_NAME_SUFFIX"]
    tdkTestObj, actual_result_all, config_values = GetPlatformProperties(obj, config_keys)

    platform = config_values["DEVICETYPE"]
    suffix = config_values["FW_NAME_SUFFIX"]

    if "FAILURE" not in actual_result_all:
        tdkTestObj.setResultStatus("SUCCESS")
        print("Fetched values from the tdk_platform.properties successfully.")

        TARGET_FIRMWARE_UPGRADE = "FIRMWARE_UPGRADE_" + platform
        FirmwareVersion = globals()[TARGET_FIRMWARE_UPGRADE]
        FirmwareFilename = FirmwareVersion + suffix
        query = f"curl -I {FIRMWARE_LOCATION}/{FirmwareFilename}  2>/dev/null | head -n 1"
        print(f"Query: {query}")
        # check target image in HTTP server deployed
        expectedresult = "SUCCESS"
        tdkTestObj = obj.createTestStep('ExecuteCmd')
        actualresult, details = doSysutilExecuteCommand(tdkTestObj, query)

        print(f"TEST STEP {step}: Check whether the target image is available in HTTP server")
        print(f"EXPECTED RESULT {step}: Should get the target image filename from HTTP server")
        if expectedresult in actualresult and "200 OK" in details:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Image {FirmwareFilename} is available in the server.")
            print("[TEST EXECUTION RESULT] : SUCCESS\n")
            return (FirmwareVersion, FirmwareFilename)
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: The {FirmwareFilename} file is not found in the server")
            print("[TEST EXECUTION RESULT] : FAILURE\n")
            return (None, None)
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("Failed to fetch values from the tdk_platform.properties.")
        return (None, None)
########## End of function ##########


# getFirmwareDownloadConfigValues
# Syntax      : getFirmwareDownloadConfigValues(FirmwareLocation, FirmwareProtocol)
# Description : Function to derive the protocol and URL values required by the firmware download TR-181 parameters
# Parameters  : FirmwareLocation - Location of the firmware file [Image hosting Server URL]
#               FirmwareProtocol - Protocol used for firmware download
# Return Value: fw_protocol - Firmware download protocol
#               fw_download_url - Firmware download URL with the scheme prefix


def getFirmwareDownloadConfigValues(FirmwareLocation=FIRMWARE_LOCATION, FirmwareProtocol=FIRMWARE_PROTOCOL):
    if FirmwareLocation == "":
        return FirmwareProtocol, ""

    fw_download_url = FirmwareLocation if "://" in FirmwareLocation else f"{FirmwareProtocol}://{FirmwareLocation}"
    parsed_location = urlparse(fw_download_url)

    fw_protocol = parsed_location.scheme if parsed_location.scheme else FirmwareProtocol
    fw_download_url = fw_download_url.rstrip("/")

    return fw_protocol, fw_download_url
########## End of function ##########


_XCONF_RESOURCE_IDS = None


def getXconfResourceIds():
    global _XCONF_RESOURCE_IDS
    if _XCONF_RESOURCE_IDS is None:
        timestamp = str(int(time.time()))
        _XCONF_RESOURCE_IDS = {
            "FWCONFIG_ID": f"TDKB_CURL_Firmware_CONFIG_{timestamp}",
            "MAC_RULE_ID": f"TDKB_CURL_MACRULE_{timestamp}",
            "MAC_LIST_ID": f"TDKB_CURL_MACLIST_{timestamp}",
            "SUPPORTED_MODEL_ID": f"BPI_TDKB_TEST_{timestamp}",
            "DEFINE_PROPERTIES_ID": f"TDKB_CURL_DEFINE_PROPERTIES_{timestamp}"
        }
    return _XCONF_RESOURCE_IDS
########## End of function ##########

# getFWUpgradeConfig
# Syntax      : getFWUpgradeConfig(obj, step)
# Description : Function to get the Firmware Download Protocol, Firmware Upgrade URL, FirmwareToDownload and FirmwareDownloadAndFactoryReset values
# Parameters  : obj - module object
#               step - test step number
# Return Value: flag - 1 if get successfully, else 0


def getFWUpgradeConfig(obj, step):
    fw_params = FW_UPGRADE_DM_PARAMS
    flag = 0
    getResult = [None] * len(fw_params)
    fw_values = [None] * len(fw_params)

    for index in range(len(fw_params)):
        print(f"\nGetting the value of {fw_params[index]}")
        tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Get')
        getResult[index], fw_values[index] = getTR181Value(tdkTestObj, fw_params[index])

    details = dict(zip(fw_params, fw_values))
    print(f"\nTEST STEP {step} : Get the FirmwareDownloadProtocol, FirmwareDownloadURL, FirmwareToDownload and FirmwareDownloadAndFactoryReset values")
    print(f"EXPECTED RESULT {step}: Should get the values successfully.")
    if "FAILURE" not in getResult:
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Successfully retrieved the values.\nRetrieved Values : {details}")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")
        flag = 1
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to get the values.\nDetails : {details}")
        print("[TEST EXECUTION RESULT] : FAILURE\n")
    return flag, details
########## End of function ##########

# setFWUpgradeConfig
# Syntax      : setFWUpgradeConfig(obj, step, FirmwareFilename, FirmwareLocation, FirmwareProtocol, trigger_download)
# Description : Function to set the Firmware Download Protocol, Firmware Upgrade URL, FirmwareToDownload and optionally trigger FirmwareDownloadAndFactoryReset
# Parameters  : obj - module object
#               step - test step number
#               FirmwareFilename - Targert Image name
#               FirmwareLocation - Location of the firmware file [Image hosting Server URL]
#               FirmwareProtocol - Protocol used for firmware download
#               trigger_download - True to trigger the firmware download, False to update only the config values
# Return Value: flag - 1 if set successfully, else 0


def setFWUpgradeConfig(obj, step, FirmwareFilename, FirmwareLocation=FIRMWARE_LOCATION, FirmwareProtocol=FIRMWARE_PROTOCOL, trigger_download=True):
    fw_protocol, fw_download_url = getFirmwareDownloadConfigValues(FirmwareLocation, FirmwareProtocol)
    fw_params = [FW_DOWNLOAD_PROTOCOL_DM,
                 FW_DOWNLOAD_URL_DM, FW_TO_DOWNLOAD_DM]
    fw_values = [fw_protocol.upper(), fw_download_url, FirmwareFilename]
    fw_datatypes = ["string", "string", "string"]

    if trigger_download:
        fw_params.append(FW_DOWNLOAD_DM)
        fw_values.append("1")
        fw_datatypes.append("int")

    flag = 0
    setResult = [None] * len(fw_params)
    details = [None] * len(fw_params)

    for index in range(len(fw_params)):
        print(f"\nSetting {fw_params[index]} to {fw_values[index]}")
        if trigger_download and index == len(fw_params) - 1:
            tdkTestObj = obj.createTestStep('TDKB_TR181Stub_SetOnly')
        else:
            tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Set')

        setResult[index], details[index] = setTR181Value(tdkTestObj, fw_params[index], fw_values[index], fw_datatypes[index])

    print(f"TEST STEP {step} : Set the FirmwareDownloadProtocol, FirmwareDownloadURL and FirmwareToDownload values")
    if trigger_download:
        print(f"EXPECTED RESULT {step}: The firmware download config values must be set and FirmwareDownloadAndFactoryReset must trigger successfully")
    else:
        print(f"EXPECTED RESULT {step}: The firmware download config values must be set successfully")
    if "FAILURE" not in setResult:
        tdkTestObj.setResultStatus("SUCCESS")
        if trigger_download:
            print(f"ACTUAL RESULT {step}: Successfully set the FirmwareDownloadProtocol, FirmwareDownloadURL, FirmwareToDownload and FirmwareDownloadAndFactoryReset. Details : {details}")
            sleep(5)
        else:
            print(f"ACTUAL RESULT {step}: Successfully set the FirmwareDownloadProtocol, FirmwareDownloadURL and FirmwareToDownload. Details : {details}")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")
        flag = 1
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to set the values. Details : {details}")
        print("[TEST EXECUTION RESULT] : FAILURE\n")
    return flag
########## End of function ##########


# getFirmwareDownloadStatus
# Syntax      : getFirmwareDownloadStatus(obj, step, expected_status)
# Description : Function to get the FirmwareDownloadStatus value and validate it against the expected status when provided
# Parameters  : obj - module object
#               step - test step number
#               expected_status - Expected FirmwareDownloadStatus value, or None to skip value comparison
# Return Value: tdkTestObj - test object
#               details - FirmwareDownloadStatus value or error details
#               status_ok - True if the status get and validation succeeded, else False


def getFirmwareDownloadStatus(obj, step, expected_status=None):
    expectedresult = "SUCCESS"
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Get')
    actual_result, details = getTR181Value(tdkTestObj, FW_DOWNLOAD_STATUS_DM)
    print(f"TEST STEP {step} : Get the Firmware Download Status")
    if expected_status is None:
        print(f"EXPECTED RESULT {step}: Should get the Firmware Download Status")
    else:
        print(f"EXPECTED RESULT {step}: Firmware Download Status should be {expected_status}")
    print(f"ACTUAL RESULT {step}: Firmware Download Status is {details}")

    status_ok = expectedresult in actual_result and (expected_status is None or details == expected_status)
    if status_ok:
        tdkTestObj.setResultStatus("SUCCESS")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("[TEST EXECUTION RESULT] : FAILURE\n")

    return tdkTestObj, details, status_ok
########## End of function ##########

# getErouterIP
# Syntax       : getErouterIP(obj, step)
# Description : Function to get the the interface name and erouter IP in the device
# Parameters   : obj - module object
#                step - test step number
# Return Value : ip - erouter IP if successful, else ""
#                step - updated test step number


def getErouterIP(obj, step):
    expectedresult = "SUCCESS"
    ip = ""
    interface = ""
    print(f"TEST STEP {step}: Fetch INTERFACE from the tdk_platform.properties")
    print(f"EXPECTED RESULT {step}: Should fetch INTERFACE from the tdk_platform.properties")
    tdkTestObj, actualresult, value = GetPlatformProperties(obj, ["INTERFACE"])
    interface = value["INTERFACE"]
    if expectedresult in actualresult and interface != "":
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Fetched INTERFACE from the tdk_platform.properties successfully. INTERFACE is {interface} ")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")

        query = f"ifconfig {interface} | grep 'inet addr' | awk '{{print $2}}' | cut -d: -f2"
        print(f"Query: {query}")

        tdkTestObj = obj.createTestStep('ExecuteCmd')
        actualresult, details = doSysutilExecuteCommand(tdkTestObj, query)
        ip = details.strip()

        step += 1
        print(f"TEST STEP {step}: Get erouter IP")
        print(f"EXPECTED RESULT {step}: Should get the erouter IP ")
        print(f"ACTUAL RESULT {step}: erouter IP obtained is {details} ")
        if expectedresult in actualresult and ip != "":
            tdkTestObj.setResultStatus("SUCCESS")
            print("[TEST EXECUTION RESULT] : SUCCESS\n")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("[TEST EXECUTION RESULT] : FAILURE\n")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to fetch INTERFACE from the tdk_platform.properties. INTERFACE is {interface}")
        print("[TEST EXECUTION RESULT] : FAILURE\n")
    return tdkTestObj, ip, step

########## End of function ##########
# getMacAddress
# Syntax      : getMacAddress(obj)
# Description : Function to get the MAC address of the device
# Parameters  : obj - module object
# Return Value: tdkTestObj - test object
#               actualresult - result of the command execution
#               estbMAC - MAC address of the device


def getMacAddress(obj):
    estbMAC = ""
    query = f"sh {TDK_PATH}/tdk_platform_utility.sh getCMMACAddress"
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, query)
    estbMAC = details.strip()
    return tdkTestObj, actualresult, estbMAC
########## End of function ##########

# getXCONFServer_CreateConfigCmd
# Syntax : getXCONFServer_CreateConfigCmd(obj, FirmwareVersion, FirmwareFilename, action, step, scenario)
# Description : Function to construct curl commands for XConf server configuration
# Parameters : obj - module object
#              FirmwareVersion - Target Image name without suffix
#              FirmwareFilename - Target Image name with suffix
#              action - "POST" for creating config, "PUT" for updating config
#              step - test step number
#              scenario - to find if scenario is invalid_url or default
# Return Value: Curl commands for XCONF server configuration


def getXCONFServer_CreateConfigCmd(obj, FirmwareVersion, FirmwareFilename, action, step, scenario=""):
    xconf_ids = getXconfResourceIds()
    if scenario == "invalid_url":
        fw_location = "http://invalid_url/"
    else:
        fw_location = FIRMWARE_LOCATION
    Curl_CMD = {}
    # get MAC details from device
    expectedresult = "SUCCESS"
    tdkTestObj, actualresult, value = GetPlatformProperties(obj, ["INTERFACE"])
    propVal = value["INTERFACE"]
    if "FAILURE" not in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        print("Fetched Interface from device successfully.")
        interface = propVal

        tdkTestObj, actualresult, estbMAC = getMacAddress(obj)
        print(f"TEST STEP {step}: Fetch DUT MAC from device")
        print(f"EXPECTED RESULT {step}: Should Fetch DUT MAC from device")
        print(f"ACTUAL RESULT {step}: DUT MAC is {estbMAC} ")

        if expectedresult in actualresult and estbMAC != "":
            tdkTestObj.setResultStatus("SUCCESS")
            print("[TEST EXECUTION RESULT] : SUCCESS\n")

            # Constructing the curl commands for XCONF based on action (POST/PUT). "POST" - Create Config and "PUT" - Update Config
            # To create the rule, all 4 commands are required
            # To update the rule, only the config command needs to be updated with new image information

            # Data dicts
            # 1. Model addition
            model_data = {
                "id": xconf_ids["SUPPORTED_MODEL_ID"],
                "description": "Test model"
            }

            # 2. MAC list addition
            mac_list_data = {
                "id": xconf_ids["MAC_LIST_ID"],
                "data": [estbMAC]
            }

            # 3. Firmware config with properties
            config_data = {
                "id": xconf_ids["FWCONFIG_ID"],
                "description": xconf_ids["FWCONFIG_ID"],
                "supportedModelIds": [xconf_ids["SUPPORTED_MODEL_ID"]],
                "firmwareFilename": FirmwareFilename,
                "firmwareVersion": FirmwareVersion,
                "applicationType": "stb",
                "firmwareDownloadProtocol": FIRMWARE_PROTOCOL,
                "rebootImmediately": False
            }

            # 4. Firmware rule
            mac_rule_data = {
                "name": xconf_ids["MAC_RULE_ID"],
                "macListRef": xconf_ids["MAC_LIST_ID"],
                "targetedModelIds": [xconf_ids["SUPPORTED_MODEL_ID"]],
                "firmwareConfig": {"id": xconf_ids["FWCONFIG_ID"]}
            }

            # 5. Define properties
            define_properties_data = {
                "id": xconf_ids["DEFINE_PROPERTIES_ID"],
                "name": xconf_ids["DEFINE_PROPERTIES_ID"],
                "applicableAction":
                {
                    "type": DEFINE_PROPERTIES_TYPE,
                    "actionType": "DEFINE_PROPERTIES",
                    "properties":
                    {
                        "firmwareDownloadProtocol": FIRMWARE_PROTOCOL,
                        "firmwareLocation": fw_location
                    }
                },
                "rule":
                {
                    "compoundParts":
                    [
                        {
                            "condition":
                            {
                                "freeArg":
                                {
                                    "type": "STRING",
                                    "name": "eStbMac"
                                },
                                "operation": "IS",
                                "fixedArg":
                                {
                                    "bean":
                                    {
                                        "value":
                                        {
                                            "java.lang.String": estbMAC
                                        }
                                    }
                                }
                            },
                            "negated": False
                        }
                    ],
                    "negated": False
                },
                "type": DEFINE_PROPERTIES_FILTER,
                "active": True,
                "applicationType": "stb"
            }

            if action == "POST":
                # 1. Model addition
                XCONF_SERVER_URL = XCONF_URL + "/updates/models"
                Curl_CMD["Model"] = build_curl(XCONF_SERVER_URL, "POST", model_data)
                # 2. MAC list addition
                XCONF_SERVER_URL = XCONF_URL + "/updates/nsLists?applicationType=stb"
                Curl_CMD["MAC List"] = build_curl(XCONF_SERVER_URL, "POST", mac_list_data)
                # 3. Firmware config
                XCONF_SERVER_URL = XCONF_URL + "/updates/firmwares?applicationType=stb"
                Curl_CMD["Firmware Config"] = build_curl(XCONF_SERVER_URL, "POST", config_data)
                # 4. Firmware rule
                XCONF_SERVER_URL = XCONF_URL + "/updates/rules/macs?applicationType=stb"
                Curl_CMD["Firmware Rule"] = build_curl(XCONF_SERVER_URL, "POST", mac_rule_data)
                # 5. Define properties rule
                XCONF_SERVER_URL = XCONF_URL + "/firmwarerule/?applicationType=stb"
                Curl_CMD["Define Properties Rule"] = build_curl(XCONF_SERVER_URL, "POST", define_properties_data)

            elif action == "PUT":
                XCONF_SERVER_URL = XCONF_URL + "/updates/firmwares?applicationType=stb"
                Curl_CMD["Modified Firmware Config"] = build_curl(XCONF_SERVER_URL, "PUT", config_data)

            parsed_url = urlparse(XCONF_URL)
            XCONF_BASE_URL = f"{parsed_url.scheme}://{parsed_url.netloc}"

            XCONF_SERVER_URL = XCONF_BASE_URL + "/xconf/swu/stb?eStbMac=" + estbMAC
            Curl_CMD["Get Config"] = f"curl -X GET {XCONF_SERVER_URL}"

        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("[TEST EXECUTION RESULT] : FAILURE\n")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("Failed to fetch Interface from device")
    return Curl_CMD

########## End of function ##########


# build_curl
# Syntax : build_curl(url, action, data_dict=None)
# Description: Function to build a curl command string with payload
# Parameters : url - URL for the curl command
#              action - HTTP action (GET, POST, PUT, DELETE)
#              data_dict - Dictionary containing the payload (for POST/PUT)
# Return Value: cmd - Formatted curl command string
def build_curl(url, action, data_dict=None):
    cmd = f"curl -X {action} {url} -H \"Accept: application/json\" -H \"Content-Type: application/json\" -H \"X-API-Key: {XCONF_API_KEY}\""
    if data_dict is not None:
        cmd += f" -d '{json.dumps(data_dict)}'"
    return cmd
########### End of function #########

# checkValidResponse
# Syntax : checkValidResponse(response)
# Description: Function to check if the response from curl command is valid or not
# Parameters : response - Response string from curl command
# Return Value: True if response is valid, else False


def checkValidResponse(response):
    if not response or not response.strip():
        return False  # empty response

    response = response.strip()

    # Check for user-defined exception in JSON values or plain text
    if "Exception" in response or "did not match any rule" in response:
        return False

    # Check for HTML error page
    if "<html>" in response.lower() or "HTTP ERROR" in response.lower():
        return False

    return True
########### End of function #########

# getXCONFServer_DeleteConfigCmd
# Syntax : getXCONFServer_DeleteConfigCmd()
# Description : Function to construct curl commands for deleting XConf server configuration
# Parameters : None
# Return Value: Curl commands for deleting XConf configuration


def getXCONFServer_DeleteConfigCmd():
    xconf_ids = getXconfResourceIds()
    # Constructing the curl commands for deleting xconf server configuration in reverse order
    delete_endpoints = [
        # 5. Delete define properties rule
        f"{XCONF_URL}/firmwarerule/{xconf_ids['DEFINE_PROPERTIES_ID']}?applicationType=stb",
        # 4. Delete firmware rule
        f"{XCONF_URL}/delete/rules/macs/{xconf_ids['MAC_RULE_ID']}?applicationType=stb",
        # 3. Delete firmware config
        f"{XCONF_URL}/delete/firmwares/{xconf_ids['FWCONFIG_ID']}?applicationType=stb",
        # 2. Delete MAC list
        f"{XCONF_URL}/delete/nsLists/{xconf_ids['MAC_LIST_ID']}",
        # 1. Delete model
        f"{XCONF_URL}/delete/models/{xconf_ids['SUPPORTED_MODEL_ID']}"
    ]
    return [build_curl(endpoint, "DELETE") for endpoint in delete_endpoints]

########## End of function #########

# triggerFirmwareDownload
# Syntax      : triggerFirmwareDownload(obj, fw_binary, logFile, step)
# Description : Function to trigger firmware download and validate its initiation from logs
# Parameters  : obj - module object
#               fw_binary - Firmware download binary command
#               logFile - Log file to check for download initiation
#               step - test step number
#               scenario - "" if default scenario, "invalid" if the scenario is invalid
# Return Value: tdkTestObj - test object
#               fw_flag - 1 if firmware download is triggered and validated successfully, else 0
#               step - updated test step number


def triggerFirmwareDownload(obj, fw_binary, logFile, step, scenario=""):
    expectedresult = "SUCCESS"
    fw_flag = 0
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    command = f"{fw_binary} > {logFile} 2>&1"
    print(f"Command: {command}")
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"TEST STEP {step}: Trigger firmware download by executing the firmware download binary")
    print(f"EXPECTED RESULT {step}: Firmware download should be triggered successfully")
    if actualresult in expectedresult and details.strip() == "":
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Firmware download triggered.")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")

        sleep(5)
        step += 1
        # Validate firmware download initiation from logs
        command = f"grep -i 'Firmware upgrade is in progress' {logFile}"
        print(f"Command: {command}")
        tdkTestObj = obj.createTestStep('ExecuteCmd')
        actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
        print(f"Command Details: {details.strip()}")
        print(f"TEST STEP {step}: Validate firmware upgrade initiation from logs.")
        if scenario == "invalid":
            print(f"EXPECTED RESULT {step}: The firmware upgrade initiation should fail")
        else:
            print(f"EXPECTED RESULT {step}: The firmware upgrade initiation should be validated successfully.")
        if actualresult in expectedresult and details.strip() != "":
            fw_flag = 1
            print(f"ACTUAL RESULT {step}: Firmware download initiation is validated from logs. Details : {details.strip()}")
        else:
            print(f"ACTUAL RESULT {step}: Failed to validate firmware download initiation from logs.")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to trigger firmware download. Details : {details.strip()}")
        print("[TEST EXECUTION RESULT] : FAILURE\n")
    return tdkTestObj, fw_flag, step
########## End of function #########


# monitorFirmwareUpgrade
# Syntax      : monitorFirmwareUpgrade(obj, FirmwareFilename, FW_DOWNLOAD_PATH, step)
# Description : Function to monitor the firmware upgrade progress by checking the presence of firmware file in the
#               download location
# Parameters  : obj - module object
#               FirmwareFilename - Target Image name with suffix
#               FW_DOWNLOAD_PATH - Path where firmware is downloaded in the device
#               step - test step number
#               scenario - "" if default scenario, "invalid" if the scenario is invalid
# Return Value: tdkTestObj - test object
#               monitor_flag - 1 if firmware file is found in the download location indicating download progress, else 0
def monitorFirmwareUpgrade(obj, FirmwareFilename, FW_DOWNLOAD_PATH, step, scenario=""):
    expectedresult = "SUCCESS"
    monitor_flag = 0
    command = f"find {FW_DOWNLOAD_PATH}/{FirmwareFilename}"
    print(f"Command: {command}")
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"TEST STEP {step}: Monitor whether the firmware is present in the download location indicating download progress.")
    if scenario == "invalid":
        print(f"EXPECTED RESULT {step}: The firmware file should not be found in the download location")
    else:
        print(f"EXPECTED RESULT {step}: The firmware file should be found in the download location indicating download progress")
    if actualresult in expectedresult and details.strip() == f"{FW_DOWNLOAD_PATH}/{FirmwareFilename}":
        monitor_flag = 1
        print(f"ACTUAL RESULT {step}: Firmware is present in the download location indicating download progress. Details : {details.strip()}")
    else:
        print(f"ACTUAL RESULT {step}: Firmware is not found in the download location. Details : {details.strip()}")

    return tdkTestObj, monitor_flag
########## End of function #########

# manageFirmwareUpgradeCronJob
# Syntax      : manageFirmwareUpgradeCronJob(obj, step, enable=False)
# Description : Function to enable or disable the firmware upgrade cron job
# Parameters  : obj - module object
#               step - test step number
#               enable - True to enable (postrequisite), False to disable (prerequisite)
# Return Value: flag - 1 if operation successful, else 0


def manageFirmwareUpgradeCronJob(obj, step, enable=False):
    flag = 0
    action = "Enable" if enable else "Disable"
    cron_command = f"crontab -l | sed '/fwupgrade/s/^{'#' if enable else ''}/{'#' if not enable else ''}/' | crontab -"
    print(f"Command Details: {cron_command}")
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, cron_command)
    print(f"TEST STEP {step}: {action} firmware upgrade cron job")
    print(f"EXPECTED RESULT {step}: Firmware upgrade cron job should be {action.lower()}d successfully")
    if "SUCCESS" in actualresult and details.strip() == "":
        flag = 1
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"Firmware upgrade cron job {action.lower()}d successfully.")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print(f"Failed to {action.lower()} firmware upgrade cron job.")
        print("[TEST EXECUTION RESULT] : FAILURE\n")
    return flag
########## End of function #########
