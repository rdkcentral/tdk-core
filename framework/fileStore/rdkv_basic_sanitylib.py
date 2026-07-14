##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2023 RDK Management
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
#########################################################################
import requests
import json
import time
import os
import subprocess
import inspect
import configparser
import threading
from SSHUtility import *
import tdkvThunderWifiUtility as wifiUtil

deviceIP=""
devicePort=""
deviceName=""
deviceType=""

#METHODS
#---------------------------------------------------------------
#INITIALIZE THE MODULE
#---------------------------------------------------------------
def init_module (libobj, port, deviceInfo):
    global deviceIP
    global devicePort
    global deviceName
    global deviceType
    deviceIP = libobj.ip;
    devicePort = port
    deviceName = deviceInfo["devicename"]
    deviceType = deviceInfo["boxtype"]

#----------------------------------------------------------------------
#GET DEVICE CONFIGURATION FROM THE DEVICE CONFIG FILE
# Description  : Read the value of device configuration from the <device>.config file
# Parameters   : basePath - a string to specify the path of the TM
#                configKey - a string to specify the configuration whose value needs to be retrieved from the <device>.config file
# Return Value : value of device configuration or error log in case of failure
#----------------------------------------------------------------------
def rdkv_basic_sanity_getDeviceConfig (basePath, configKey):
    deviceConfigFile=""
    configValue = ""
    output = ""
    configPath = basePath + "/"   + "fileStore/tdkvRDKServiceConfig"
    deviceNameConfigFile = configPath + "/" + deviceName + ".config"
    deviceTypeConfigFile = configPath + "/" + deviceType + ".config"
    # Check whether device / platform config files required for
    # executing the test are present
    if os.path.exists (deviceNameConfigFile) == True:
        deviceConfigFile = deviceNameConfigFile
    elif os.path.exists (deviceTypeConfigFile) == True:
        deviceConfigFile = deviceTypeConfigFile
    else:
        output = "FAILURE : No Device config file found : " + deviceNameConfigFile + " or " + deviceTypeConfigFile
        print(output)
        #print "[ERROR]: No Device config file found : %s or %s" %(deviceNameConfigFile,deviceTypeConfigFile)
    try:
        if (len (deviceConfigFile) != 0) and (len (configKey) != 0):
            config = configparser.ConfigParser ()
            config.read (deviceConfigFile)
            deviceConfig = config.sections ()[0]
            configValue =  config.get (deviceConfig, configKey)
            output = configValue
        else:
            output = "FAILURE : DeviceConfig file or key cannot be empty"
            print(output)
    except Exception as e:
        output = "FAILURE : Exception Occurred: [" + inspect.stack()[0][3] + "] " + e.message
        print(output)
    return output;

#-------------------------------------------------------------------
#EXECUTE A COMMAND IN DUT SHELL AND GET THE OUTPUT
# Description  : Execute a command in DUT through ssh_and_execute() from SSHUtility library and get the output
# Parameters   : 1. sshMethod -  string to specify the SSH method to be used
#                2. credentials - a coma ceparated string to specify the parameters for ssh_and_execute() method. Values are retrieved from <device>.config
#                       a. credentials[0] - string to specify the DUT IP
#                       b. credentials[1] - string to specify the username to ssh to DUT
#                       c. credentials[2] - string to specify the password to ssh to DUT
#                3. command - string to specify the command to be executed in DUT
#                4. sshPort - port of DUT for SSH
# Return Value : console output of the command executed on DUT
#-------------------------------------------------------------------
def rdkv_basic_sanity_executeInDUT (sshMethod, credentials, command, sshPort):
    output = ""
    if sshMethod == "directSSH":
        credentialsList = credentials.split(',')
        host_name = credentialsList[0]
        user_name = credentialsList[1]
        password = credentialsList[2]
    else:
        #TODO
        print("Secure ssh to CPE")
        pass
    try:
        if sshPort != 22:
            output = ssh_and_execute (sshMethod, host_name, user_name, password, command)
        else:
            output = ssh_and_execute (sshMethod, host_name, user_name, password, command, sshPort)
    except Exception as e:
        print("Exception occured during ssh session")
        print(e)
    return output
#-------------------------------------------------------------------
#EXECUTE A COMMAND IN DUT SHELL AND GET THE OUTPUT
# Description  : Execute a command in DUT through ssh_and_execute() from SSHUtility library and get the output
# Parameters   : 1. sshMethod -  string to specify the SSH method to be used
#                2. credentials - a coma ceparated string to specify the parameters for ssh_and_execute() method. Values are retrieved from <device>.config
#                       a. credentials[0] - string to specify the DUT IP
#                       b. credentials[1] - string to specify the username to ssh to DUT
#                       c. credentials[2] - string to specify the password to ssh to DUT
#                3. command - string to specify the command to be executed in DUT
# Return Value : console output of the command executed on DUT
#-------------------------------------------------------------------
def rdkv_basic_sanity_rebootexecution (sshMethod, credentials, command):
    output = ""
    if sshMethod == "directSSH":
        credentialsList = credentials.split(',')
        host_name = credentialsList[0]
        user_name = credentialsList[1]
        password = credentialsList[2]
    else:
        #TODO
        print("Secure ssh to CPE")
        pass
    try:
        output = ssh_and_execute (sshMethod, host_name, user_name, password, command)
    except Exception as e:
        #Here exception is passed to avoid exception error because device will be offline when reboot is triggered from shellscript.
        pass
    return output

#-------------------------------------------------------------------
#CREATE DISPLAY AND VERIFY IT APPEARS IN GETAPPS
# Description  : Creates a display named "testdisplay" using org.rdk.RDKWindowManager.createDisplay
#                and verifies its presence via org.rdk.RDKWindowManager.getApps
# Parameters   : deviceIP - string specifying the IP address of the target device
# Return Value : "SUCCESS" if "testdisplay" is found in getApps result, "FAILURE" otherwise
#-------------------------------------------------------------------
def rdkv_basic_sanity_createAndVerifyDisplay(deviceIP, THUNDER_PORT, DISPLAY_NAME):
    JSONRPC_URL = "http://{}:{}/jsonrpc".format(deviceIP, THUNDER_PORT)
    headers = {"Content-Type": "application/json"}

    # Step 1: Check if testdisplay already exists in getApps before creating
    get_apps_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "org.rdk.RDKWindowManager.getApps"
    }
    try:
        pre_check_response = requests.post(JSONRPC_URL, headers=headers, json=get_apps_payload, timeout=10)
        pre_check_result = pre_check_response.json()
        print("Pre-check getApps response: {}".format(pre_check_result))
        apps_raw = pre_check_result.get("result", "[]")
        if isinstance(apps_raw, str):
            apps_list = json.loads(apps_raw)
        else:
            apps_list = apps_raw
        if DISPLAY_NAME in apps_list:
            print("SUCCESS : '{}' already exists in getApps, skipping createDisplay".format(DISPLAY_NAME))
            return "SUCCESS"
    except Exception as e:
        print("FAILURE : Exception during pre-check getApps: {}".format(e))
        return "FAILURE"

    # Step 2: Create the display (only if not already existing)
    create_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "org.rdk.RDKWindowManager.createDisplay",
        "params": {
            "clientId": DISPLAY_NAME,
            "displayName": DISPLAY_NAME
        }
    }
    try:
        create_response = requests.post(JSONRPC_URL, headers=headers, json=create_payload, timeout=10)
        create_result = create_response.json()
        print("createDisplay response: {}".format(json.dumps(create_result)))
        if "result" not in create_result:
            print("FAILURE : 'result' key missing in createDisplay response")
            return "FAILURE"
        if create_result["result"] is not None:
            print("FAILURE : Expected null in createDisplay result, got: {}".format(create_result["result"]))
            return "FAILURE"
        print("createDisplay result is null as expected")
    except Exception as e:
        print("FAILURE : Exception during createDisplay: {}".format(e))
        return "FAILURE"

    # Step 3: Get the list of apps and verify testdisplay is present
    get_apps_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "org.rdk.RDKWindowManager.getApps"
    }
    try:
        get_apps_response = requests.post(JSONRPC_URL, headers=headers, json=get_apps_payload, timeout=10)
        get_apps_result = get_apps_response.json()
        print("getApps response: {}".format(get_apps_result))
        # The result field is a JSON-encoded string (e.g. "[\"testdisplay\",\"...\"]")
        apps_raw = get_apps_result.get("result", "[]")
        if isinstance(apps_raw, str):
            apps_list = json.loads(apps_raw)
        else:
            apps_list = apps_raw
        if DISPLAY_NAME in apps_list:
            print("SUCCESS : '{}' found in getApps result".format(DISPLAY_NAME))
            return "SUCCESS"
        else:
            print("FAILURE : '{}' not found in getApps result: {}".format(DISPLAY_NAME, apps_list))
            return "FAILURE"
    except Exception as e:
        print("FAILURE : Exception during getApps: {}".format(e))
        return "FAILURE"

#-------------------------------------------------------------------
# WIFI SCAN: START SCAN, WAIT FOR onAvailableSSIDs, VERIFY TARGET SSID, STOP SCAN
# Description  : Triggers a WiFi scan via Thunder NetworkManager, waits for the
#                onAvailableSSIDs WebSocket event, verifies targetSSID is present,
#                then stops the scan
# Parameters   : deviceIP    - IP address of the DUT
#                thunderPort - Thunder JSON-RPC port (e.g. 9998)
#                targetSSID  - SSID name expected in the scan results
# Return Value : "SUCCESS" or "FAILURE: ..."
#-------------------------------------------------------------------
def rdkv_basic_sanity_wifiStartScanAndVerify(deviceIP, thunderPort, targetSSID):
    wifiUtil.setThunderPort(int(thunderPort))
    wifiUtil.ssid_event_received = False
    wifiUtil.ssid_list = []

    scan_thread = threading.Thread(target=wifiUtil.startEventListener, args=(deviceIP,))
    scan_thread.daemon = True
    scan_thread.start()
    time.sleep(2)

    if not wifiUtil.triggerWiFiScan(deviceIP):
        if wifiUtil.ws_instance:
            wifiUtil.ws_instance.close()
        wifiUtil.stopWiFiScan(deviceIP)
        return "FAILURE: StartWiFiScan did not return success=true"

    print("INFO: Waiting for onAvailableSSIDs event (max {}s)...".format(wifiUtil.SCAN_TIMEOUT))
    elapsed = 0
    while elapsed < wifiUtil.SCAN_TIMEOUT:
        if wifiUtil.ssid_event_received:
            break
        time.sleep(1)
        elapsed += 1

    if wifiUtil.ws_instance:
        wifiUtil.ws_instance.close()
    scan_thread.join(timeout=5)

    if not wifiUtil.ssid_event_received:
        wifiUtil.stopWiFiScan(deviceIP)
        return "FAILURE: onAvailableSSIDs event not received within {}s".format(wifiUtil.SCAN_TIMEOUT)

    print("INFO: onAvailableSSIDs received with {} SSIDs".format(len(wifiUtil.ssid_list)))
    ssid_names = [entry.get("ssid", "") for entry in wifiUtil.ssid_list]

    stop_ok = wifiUtil.stopWiFiScan(deviceIP)
    if not stop_ok:
        return "FAILURE: StopWiFiScan did not return success=true"

    if targetSSID in ssid_names:
        print("SUCCESS: '{}' found in scanned SSIDs".format(targetSSID))
        return "SUCCESS"
    else:
        return "FAILURE: '{}' not found in scanned SSIDs".format(targetSSID)

#-------------------------------------------------------------------
# WIFI CONNECT: TRIGGER CONNECT, WAIT FOR onWiFiStateChange EVENT
# Description  : Connects the device to the given SSID via Thunder WiFiConnect,
#                then waits for the onWiFiStateChange WebSocket event to confirm
#                the connection attempt completed
# Parameters   : deviceIP    - IP address of the DUT
#                thunderPort - Thunder JSON-RPC port (e.g. 9998)
#                ssid        - SSID to connect to
#                passphrase  - WiFi password
#                security    - Security type integer (e.g. 6 for WPA2)
# Return Value : "SUCCESS" or "FAILURE: ..."
#-------------------------------------------------------------------
def rdkv_basic_sanity_wifiConnect(deviceIP, thunderPort, ssid, passphrase, security):
    wifiUtil.setThunderPort(int(thunderPort))
    wifiUtil.wifi_state_event_received = False
    wifiUtil.wifi_state_data = {}

    connect_thread = threading.Thread(target=wifiUtil.startWiFiConnectEventListener, args=(deviceIP,))
    connect_thread.daemon = True
    connect_thread.start()
    time.sleep(2)

    if not wifiUtil.triggerWiFiConnect(deviceIP, ssid, passphrase, int(security)):
        if wifiUtil.ws_connect_instance:
            wifiUtil.ws_connect_instance.close()
        return "FAILURE: WiFiConnect did not return success=true"

    print("INFO: Waiting for onWiFiStateChange event (max {}s)...".format(wifiUtil.CONNECT_TIMEOUT))
    elapsed = 0
    while elapsed < wifiUtil.CONNECT_TIMEOUT:
        if wifiUtil.wifi_state_event_received:
            break
        time.sleep(1)
        elapsed += 1

    if wifiUtil.ws_connect_instance:
        wifiUtil.ws_connect_instance.close()
    connect_thread.join(timeout=5)

    if wifiUtil.wifi_state_event_received:
        print("SUCCESS: onWiFiStateChange event received")
        return "SUCCESS"
    else:
        return "FAILURE: onWiFiStateChange event not received within {}s".format(wifiUtil.CONNECT_TIMEOUT)

#-------------------------------------------------------------------
# WIFI VERIFY CONNECTION: GET CONNECTED SSID AND COMPARE
# Description  : Calls GetConnectedSSID via Thunder NetworkManager and verifies
#                the returned SSID matches the expected SSID
# Parameters   : deviceIP     - IP address of the DUT
#                thunderPort  - Thunder JSON-RPC port (e.g. 9998)
#                expectedSSID - SSID that the device should be connected to
# Return Value : "SUCCESS" or "FAILURE: ..."
#-------------------------------------------------------------------
def rdkv_basic_sanity_wifiVerifyConnectedSSID(deviceIP, thunderPort, expectedSSID):
    wifiUtil.setThunderPort(int(thunderPort))
    connected_info = wifiUtil.getConnectedSSID(deviceIP)
    conn_ssid    = connected_info.get("ssid", "")
    conn_success = connected_info.get("success", False)
    if conn_success and conn_ssid == expectedSSID:
        print("SUCCESS: GetConnectedSSID returned SSID='{}'".format(conn_ssid))
        return "SUCCESS"
    else:
        return "FAILURE: Expected SSID='{}' but got '{}' (success={})".format(expectedSSID, conn_ssid, conn_success)

#-------------------------------------------------------------------
# WIFI DISCONNECT
# Description  : Disconnects the device from WiFi via Thunder NetworkManager
#                and verifies success
# Parameters   : deviceIP    - IP address of the DUT
#                thunderPort - Thunder JSON-RPC port (e.g. 9998)
# Return Value : "SUCCESS" or "FAILURE: ..."
#-------------------------------------------------------------------
def rdkv_basic_sanity_wifiDisconnect(deviceIP, thunderPort):
    wifiUtil.setThunderPort(int(thunderPort))
    if wifiUtil.disconnectFromWiFi(deviceIP):
        print("SUCCESS: WiFiDisconnect returned success=true")
        return "SUCCESS"
    else:
        return "FAILURE: WiFiDisconnect did not return success=true"
