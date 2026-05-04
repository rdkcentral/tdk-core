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
#-----------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
from firmwareUpgradeVariables import *
from tdkutility import *
from tdkbVariables import *
import json
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
        command = "sh %s/tdk_utility.sh parseConfigFile %s" % (TDK_PATH, key)
        tdkTestObj, actualresult, config_values[key] = get_config_values(obj, command)
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
        print("Query: %s" %query)

        tdkTestObj = obj.createTestStep('ExecuteCmd')
        actualresult, details = doSysutilExecuteCommand(tdkTestObj, query)

        print("TEST STEP %d: Fetch device's current firmware name" %step)
        print("EXPECTED RESULT %d: Should fetch device's current firmware name" %step)
        print("ACTUAL RESULT %d: Image name %s " %(step, details))
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
        print("Query: %s" %query)
        # check target image in HTTP server deployed
        expectedresult = "SUCCESS"
        tdkTestObj = obj.createTestStep('ExecuteCmd')
        actualresult, details = doSysutilExecuteCommand(tdkTestObj, query)

        print("TEST STEP %d: Check whether the target image is available in HTTP server" %step)
        print("EXPECTED RESULT %d: Should get the target image filename from HTTP server" %step)
        if expectedresult in actualresult and "200 OK" in details:
            tdkTestObj.setResultStatus("SUCCESS")
            print("ACTUAL RESULT %d: Image %s is available in the server." %(step, FirmwareFilename))
            print("[TEST EXECUTION RESULT] : SUCCESS\n")
            return (FirmwareVersion, FirmwareFilename)
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("ACTUAL RESULT %d: The %s file is not found in the server" %(step, FirmwareFilename))
            print("[TEST EXECUTION RESULT] : FAILURE\n")
            return (None, None)
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("Failed to fetch values from the tdk_platform.properties.")
        return (None, None)
########## End of function ##########

# getFWUpgradeConfig
# Syntax      : getFWUpgradeConfig(obj, step)
# Description : Function to get the Firmware Upgrade URL, FirmwareToDownload and FirmwareDownloadNow values
# Parameters  : obj - module object
#               step - test step number
# Return Value: flag - 1 if get successfully, else 0


def getFWUpgradeConfig(obj, step):
    fw_params = ["Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareDownloadURL","Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareToDownload", "Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareDownloadNow"]
    flag = 0
    getResult = [None] * 3
    fw_values = [None] * 3

    for index in range(3):
        print("\nGetting the value of %s" %fw_params[index])
        tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Get')
        getResult[index], fw_values[index] = getTR181Value(tdkTestObj, fw_params[index])

    details = dict(zip(fw_params, fw_values))
    print("\nTEST STEP %d : Get the FirmwareDownloadURL, FirmwareToDownload and FirmwareDownloadNow values" %step)
    print("EXPECTED RESULT %d: Should get the values successfully." %step)
    if "FAILURE" not in getResult:
        tdkTestObj.setResultStatus("SUCCESS")
        print("ACTUAL RESULT %d: Successfully retrieved the values.\nRetrieved Values : %s" %(step, details))
        print("[TEST EXECUTION RESULT] : SUCCESS\n")
        flag = 1
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("ACTUAL RESULT %d: Failed to get the values.\nDetails : %s" %(step, details))
        print("[TEST EXECUTION RESULT] : FAILURE\n")
    return flag, details
########## End of function ##########

# setFWUpgradeConfig
# Syntax      : setFWUpgradeConfig(obj, step, FirmwareFilename, FirmwareLocation)
# Description : Function to set the Firmware Upgrade URL, FirmwareToDownload and FirmwareDownloadNow values
# Parameters  : obj - module object
#               step - test step number
#               FirmwareFilename - Targert Image name
#               FirmwareLocation - Location of the firmware file [Image hosting Server URL]
# Return Value: flag - 1 if set successfully, else 0


def setFWUpgradeConfig(obj, step, FirmwareFilename, FirmwareLocation=FIRMWARE_LOCATION):
    fw_params = ["Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareDownloadURL","Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareToDownload", "Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareDownloadNow"]
    fw_values = [FirmwareLocation, FirmwareFilename, "true"]
    fw_datatypes = ["string", "string", "boolean"]
    flag = 0
    setResult = [None] * 3
    details = [None] * 3

    for index in range(3):
        print("\nSetting %s to %s" %(fw_params[index], fw_values[index]))
        if index == 2:
            tdkTestObj = obj.createTestStep('TDKB_TR181Stub_SetOnly')
        else:
            tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Set')

        setResult[index], details[index] = setTR181Value(tdkTestObj, fw_params[index], fw_values[index], fw_datatypes[index])

    print("TEST STEP %d : Set the FirmwareDownloadURL, FirmwareToDownload and FirmwareDownloadNow values" %step)
    print("EXPECTED RESULT %d: The values must be set successfully" %step)
    if "FAILURE" not in setResult:
        tdkTestObj.setResultStatus("SUCCESS")
        print("ACTUAL RESULT %d: Successfully set the FirmwareDownloadURL, FirmwareToDownload and FirmwareDownloadNow. Details : %s" %(step, details))
        print("[TEST EXECUTION RESULT] : SUCCESS\n")
        flag = 1
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("ACTUAL RESULT %d: Failed to set th values. Details : %s" %(step, details))
        print("[TEST EXECUTION RESULT] : FAILURE\n")
    return flag
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
    print("TEST STEP %d: Fetch INTERFACE from the tdk_platform.properties" %step)
    print("EXPECTED RESULT %d: Should fetch INTERFACE from the tdk_platform.properties" %step)
    tdkTestObj, actualresult, value = GetPlatformProperties(obj, ["INTERFACE"])
    interface = value["INTERFACE"]
    if expectedresult in actualresult and interface != "":
        tdkTestObj.setResultStatus("SUCCESS")
        print("ACTUAL RESULT %d: Fetched INTERFACE from the tdk_platform.properties successfully. INTERFACE is %s " %(step, interface))
        print("[TEST EXECUTION RESULT] : SUCCESS\n")

        query = f"ifconfig {interface} | grep 'inet addr' | awk '{{print $2}}' | cut -d: -f2"
        print("Query: %s" %query)

        tdkTestObj = obj.createTestStep('ExecuteCmd')
        actualresult, details = doSysutilExecuteCommand(tdkTestObj, query)
        ip = details.strip()

        step += 1
        print("TEST STEP %d: Get erouter IP" %step)
        print("EXPECTED RESULT %d: Should get the erouter IP " %step)
        print("ACTUAL RESULT %d: erouter IP obtained is %s " %(step, details))
        if expectedresult in actualresult and ip != "":
            tdkTestObj.setResultStatus("SUCCESS")
            print("[TEST EXECUTION RESULT] : SUCCESS\n")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("[TEST EXECUTION RESULT] : FAILURE\n")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("ACTUAL RESULT %d: Failed to fetch INTERFACE from the tdk_platform.properties. INTERFACE is %s" %(step, interface))
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
    query = "sh %s/tdk_platform_utility.sh getCMMACAddress" %TDK_PATH
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
                "id": SUPPORTED_MODEL_ID,
                "description": "Test model"
            }

            # 2. MAC list addition
            mac_list_data = {
                "id": MAC_LIST_ID,
                "data": [estbMAC]
            }

            # 3. Firmware config with properties
            config_data = {
                "id": FWCONFIG_ID,
                "description": FWCONFIG_ID,
                "supportedModelIds": [SUPPORTED_MODEL_ID],
                "firmwareFilename": FirmwareFilename,
                "firmwareVersion": FirmwareVersion,
                "applicationType": "stb",
                "firmwareDownloadProtocol": Protocol,
                "rebootImmediately": False
            }

            # 4. Firmware rule
            mac_rule_data = {
                "name": MAC_RULE_ID,
                "macListRef": MAC_LIST_ID,
                "targetedModelIds": [SUPPORTED_MODEL_ID],
                "firmwareConfig": {"id": FWCONFIG_ID}
            }

            # 5. Define properties
            define_properties_data = {
                "id": DEFINE_PROPERTIES_ID,
                "name": DEFINE_PROPERTIES_ID,
                "applicableAction":
                {
                    "type": DEFINE_PROPERTIES_TYPE,
                    "actionType": "DEFINE_PROPERTIES",
                    "properties":
                    {
                        "firmwareDownloadProtocol": Protocol,
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
    # Constructing the curl commands for deleting xconf server configuration in reverse order
    delete_endpoints = [
        # 5. Delete define properties rule
        f"{XCONF_URL}/firmwarerule/{DEFINE_PROPERTIES_ID}?applicationType=stb",
        # 4. Delete firmware rule
        f"{XCONF_URL}/delete/rules/macs/{MAC_RULE_ID}?applicationType=stb",
        # 3. Delete firmware config
        f"{XCONF_URL}/delete/firmwares/{FWCONFIG_ID}?applicationType=stb",
        # 2. Delete MAC list
        f"{XCONF_URL}/delete/nsLists/{MAC_LIST_ID}",
        # 1. Delete model
        f"{XCONF_URL}/delete/models/{SUPPORTED_MODEL_ID}"
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
        #Validate firmware download initiation from logs
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
