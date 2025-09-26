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
#------------------------------------------------------------------------------
# module imports
#------------------------------------------------------------------------------
from firmwareUpgradeVariables import *
from tdkutility import *
from tdkbVariables import *

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
    tdkTestObj, actualresult,value = GetPlatformProperties(obj, ["FW_NAME_SUFFIX"])
    suffix = value["FW_NAME_SUFFIX"]
    ###get details of the current firmware in the device

    if "FAILURE" not in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        print("Fetched FW_NAME_SUFFIX from the tdk_platform.properties successfully.")

        query = 'cat /version.txt | grep -i imagename | cut -c 11- | tr "\n" " "'
        print("Query: %s" %query)

        tdkTestObj = obj.createTestStep('ExecuteCmd')
        actualresult, details = doSysutilExecuteCommand(tdkTestObj,query)

        print("TEST STEP %d: Fetch device's current firmware name" %step)
        print("EXPECTED RESULT %d: Should fetch device's current firmware name" %step)
        print("ACTUAL RESULT %d: Image name %s " %(step,details))
        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS")
            print("[TEST EXECUTION RESULT] : SUCCESS\n")
            FirmwareVersion = details.strip()
            FirmwareFilename =FirmwareVersion + suffix
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
# Description : Function to get the name of firmware to be upgraded from local HTTP server
# Parameters  : obj - module object
#               step - test step number
# Return Value: FirmwareVersion - Image name without suffix if successful, else None
#               FirmwareFilename - Image name with suffix if successful, else None

def getFirmwareDetailsFromServer(obj , step):
    config_keys = ["DEVICETYPE" , "FW_NAME_SUFFIX"]
    tdkTestObj, actual_result_all, config_values = GetPlatformProperties(obj, config_keys)

    platform = config_values["DEVICETYPE"]
    suffix = config_values["FW_NAME_SUFFIX"]

    if "FAILURE" not in actual_result_all:
        tdkTestObj.setResultStatus("SUCCESS")
        print("Fetched values from the tdk_platform.properties successfully.")

        TARGET_FIRMWARE_UPGRADE = "FIRMWARE_UPGRADE_" + platform
        FirmwareVersion = globals()[TARGET_FIRMWARE_UPGRADE]
        FirmwareFilename =FirmwareVersion + suffix
        query = f"curl -I {FIRMWARE_LOCATION}{FirmwareFilename}  2>/dev/null | head -n 1"
        print("Query: %s" %query)
        ###check target image in HTTP server deployed
        expectedresult = "SUCCESS"
        tdkTestObj = obj.createTestStep('ExecuteCmd')
        actualresult, details = doSysutilExecuteCommand(tdkTestObj,query)

        print("TEST STEP %d: Check whether the target image is available in HTTP server" %step)
        print("EXPECTED RESULT %d: Should get the target image filename from HTTP server" %step)
        if expectedresult in actualresult and "200 OK" in details:
            tdkTestObj.setResultStatus("SUCCESS")
            print("ACTUAL RESULT %d: Image %s is available in the server." %(step,FirmwareFilename))
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
    fw_params = ["Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareDownloadURL", "Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareToDownload", "Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareDownloadNow"]
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
    return flag,details
########## End of function ##########

# setFWUpgradeConfig
# Syntax      : setFWUpgradeConfig(obj, step, FirmwareFilename, FirmwareLocation)
# Description : Function to set the Firmware Upgrade URL, FirmwareToDownload and FirmwareDownloadNow values
# Parameters  : obj - module object
#               step - test step number
#               FirmwareFilename - Targert Image name
#               FirmwareLocation - Location of the firmware file [Server URL]
# Return Value: flag - 1 if set successfully, else 0

def setFWUpgradeConfig(obj, step, FirmwareFilename, FirmwareLocation=FIRMWARE_LOCATION):
    fw_params = ["Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareDownloadURL", "Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareToDownload", "Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareDownloadNow"]
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
        print("ACTUAL RESULT %d: Successfully set the FirmwareDownloadURL, FirmwareToDownload and FirmwareDownloadNow. Details : %s" %(step,details))
        print("[TEST EXECUTION RESULT] : SUCCESS\n")
        flag = 1
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("ACTUAL RESULT %d: Failed to set th values. Details : %s" %(step,details))
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
        print("ACTUAL RESULT %d: Fetched INTERFACE from the tdk_platform.properties successfully. INTERFACE is %s " %(step,interface))
        print("[TEST EXECUTION RESULT] : SUCCESS\n")

        query = f"ifconfig {interface} | grep 'inet addr' | awk '{{print $2}}' | cut -d: -f2"
        print("Query: %s" %query)

        tdkTestObj = obj.createTestStep('ExecuteCmd')
        actualresult, details = doSysutilExecuteCommand(tdkTestObj,query)
        ip = details.strip()

        step += 1
        print("TEST STEP %d: Get erouter IP" %step)
        print("EXPECTED RESULT %d: Should get the erouter IP " %step)
        print("ACTUAL RESULT %d: erouter IP obtained is %s " %(step,details))
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
    return ip, step

########## End of function ##########
