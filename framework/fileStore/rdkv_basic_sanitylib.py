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
#                configKey - a string specifying the configuration key(s) to retrieve
#                            from the <device>.config file. Can be:
#                            - A plain key name (e.g. "SSH_PORT") : returns the single config value
#                            - A JSON-encoded list of keys (e.g. '["SSH_PORT","SSH_METHOD"]') :
#                              returns a dict mapping each key to its value
#                              e.g. {"SSH_PORT": "22", "SSH_METHOD": "directSSH"}
# Return Value : config value string (if configKey is a plain string),
#                dict of {key: value} pairs (if configKey is a JSON list),
#                or error string in case of failure
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
    # Determine whether configKey encodes a list or is a plain key name
    try:
        parsed = json.loads(configKey)
        keyList = parsed if isinstance(parsed, list) else None
    except (ValueError, TypeError):
        keyList = None

    try:
        if (len (deviceConfigFile) != 0) and (len (configKey) != 0):
            config = configparser.ConfigParser ()
            config.read (deviceConfigFile)
            deviceConfig = config.sections ()[0]
            if keyList is not None:
                result_dict = {}
                for key in keyList:
                    try:
                        result_dict[key] = config.get(deviceConfig, key)
                    except Exception as keyErr:
                        result_dict[key] = "FAILURE : Key not found: {}".format(key)
                        print("FAILURE : Key '{}' not found in config".format(key))
                output = result_dict
            else:
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
# Description  : Creates a display using org.rdk.RDKWindowManager.createDisplay
#                and verifies its presence via org.rdk.RDKWindowManager.getApps.
#                Uses global deviceIP and devicePort.
# Parameters   : DISPLAY_NAME - string specifying the name of the display to create
# Return Value : "SUCCESS" if DISPLAY_NAME is found in getApps result, "FAILURE" otherwise
#-------------------------------------------------------------------
def rdkv_basic_sanity_createAndVerifyDisplay(DISPLAY_NAME):
    JSONRPC_URL = "http://{}:{}/jsonrpc".format(deviceIP, devicePort)
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
#                then stops the scan. Uses global deviceIP and devicePort.
# Parameters   : targetSSID  - SSID name expected in the scan results
# Return Value : "SUCCESS" or "FAILURE: ..."
#-------------------------------------------------------------------
def rdkv_basic_sanity_wifiStartScanAndVerify(targetSSID):
    wifiUtil.setThunderPort(int(devicePort))
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
#                the connection attempt completed. Uses global deviceIP and devicePort.
# Parameters   : ssid        - SSID to connect to
#                passphrase  - WiFi password
#                security    - Security type integer (e.g. 6 for WPA2)
# Return Value : "SUCCESS" or "FAILURE: ..."
#-------------------------------------------------------------------
def rdkv_basic_sanity_wifiConnect(ssid, passphrase, security):
    wifiUtil.setThunderPort(int(devicePort))
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
#                the returned SSID matches the expected SSID.
#                Uses global deviceIP and devicePort.
# Parameters   : expectedSSID - SSID that the device should be connected to
# Return Value : "SUCCESS" or "FAILURE: ..."
#-------------------------------------------------------------------
def rdkv_basic_sanity_wifiVerifyConnectedSSID(expectedSSID):
    wifiUtil.setThunderPort(int(devicePort))
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
#                and verifies success. Uses global deviceIP and devicePort.
# Parameters   : None
# Return Value : "SUCCESS" or "FAILURE: ..."
#-------------------------------------------------------------------
def rdkv_basic_sanity_wifiDisconnect():
    wifiUtil.setThunderPort(int(devicePort))
    if wifiUtil.disconnectFromWiFi(deviceIP):
        print("SUCCESS: WiFiDisconnect returned success=true")
        return "SUCCESS"
    else:
        return "FAILURE: WiFiDisconnect did not return success=true"

#-------------------------------------------------------------------
# HDMI CONNECTION CHECK: GET CONNECTED VIDEO DISPLAYS AND VERIFY HDMI
# Description  : Calls org.rdk.DisplaySettings.getConnectedVideoDisplays via
#                Thunder JSON-RPC and verifies that at least one HDMI display
#                is connected. Uses global deviceIP and devicePort.
# Parameters   : None
# Return Value : "SUCCESS" or "FAILURE: ..."
#-------------------------------------------------------------------
def rdkv_basic_sanity_hdmiConnectionCheck():
    jsonrpc_url = "http://{}:{}/jsonrpc".format(deviceIP, devicePort)
    payload = {
        "jsonrpc": "2.0",
        "id": 42,
        "method": "org.rdk.DisplaySettings.getConnectedVideoDisplays"
    }
    try:
        response = requests.post(jsonrpc_url, json=payload, timeout=10)
        response_json = response.json()
        print("INFO: getConnectedVideoDisplays response: {}".format(json.dumps(response_json)))
        result_obj         = response_json.get("result", {})
        connected_displays = result_obj.get("connectedVideoDisplays", [])
        success            = result_obj.get("success", False)
        print("INFO: connectedVideoDisplays: {}".format(connected_displays))
        if not success:
            return "FAILURE: getConnectedVideoDisplays did not return success=true"
        hdmi_connected = any(str(d).upper().startswith("HDMI") for d in connected_displays)
        if hdmi_connected:
            print("SUCCESS: HDMI is connected")
            return "SUCCESS"
        else:
            return "FAILURE: HDMI is not connected. Connected displays: {}".format(connected_displays)
    except Exception as e:
        return "FAILURE: Exception during getConnectedVideoDisplays: {}".format(str(e))

#-------------------------------------------------------------------
# GSTREAMER EOS CHECK: VERIFY "Got EOS" IN GSTREAMER OUTPUT
# Description  : Checks whether the GStreamer output contains the "Got EOS"
#                marker, indicating that end-of-stream was reached.
# Parameters   : gst_output - string output captured from the gst-launch command
# Return Value : "SUCCESS" if "Got EOS" is found, "FAILURE: ..." otherwise
#-------------------------------------------------------------------
def rdkv_basic_sanity_verifyEOS(gst_output):
    if "Got EOS" in gst_output:
        print("SUCCESS: 'Got EOS' detected in GStreamer output")
        return "SUCCESS"
    else:
        return "FAILURE: 'Got EOS' was not detected in GStreamer output"

#-------------------------------------------------------------------
# GSTREAMER PROGRESS CHECK: VERIFY PLAYBACK REACHED >= 99.5% COMPLETION
# Description  : Parses percentage values from GStreamer output and verifies
#                that the maximum progress reached is at least 99.5%.
# Parameters   : gst_output - string output captured from the gst-launch command
# Return Value : "SUCCESS" if max progress >= 99.5%, "FAILURE: ..." otherwise
#-------------------------------------------------------------------
def rdkv_basic_sanity_checkPlaybackProgress(gst_output):
    import re
    percentages = [float(m) for m in re.findall(r'\(([0-9]+(?:\.[0-9]+)?)\s*%\)', gst_output)]
    max_percent = max(percentages) if percentages else 0.0
    print("INFO: Maximum playback progress detected: {:.1f}%".format(max_percent))
    if max_percent >= 99.5:
        print("SUCCESS: Playback reached {:.1f}%, meets >= 99.5% threshold".format(max_percent))
        return "SUCCESS"
    else:
        return "FAILURE: Playback reached only {:.1f}%, expected >= 99.5%".format(max_percent)

#-------------------------------------------------------------------
# LAUNCH GSTREAMER PLAYBACK: VERIFY STREAM, FORM AND EXECUTE gst-launch
# Description  : Verifies the given playback stream is accessible, then
#                forms a gst-launch-1.0 playbin command with the supplied
#                flags and WAYLAND_DISPLAY env, and executes it on the DUT
#                via SSH. Stream check: file:/ URIs are verified via SSH,
#                http/https URIs via HTTP HEAD request.
# Parameters   : playback_stream - URI of the stream to play (file:/ or http/https)
#                gst_play_flags  - playbin flags string (e.g. "audio+video")
#                DISPLAY_NAME    - Wayland display name for WAYLAND_DISPLAY env var
#                sshMethod       - SSH method string (e.g. "directSSH")
#                credentials     - comma-separated string "host,username,password"
#                sshPort         - SSH port (string or int)
# Return Value : Raw gst-launch stdout on success, "FAILURE: ..." otherwise
#-------------------------------------------------------------------
def rdkv_basic_sanity_launchPlayback(playback_stream, gst_play_flags, DISPLAY_NAME, sshMethod, credentials, sshPort):
    # Verify playback stream is accessible
    if playback_stream.startswith("file:/"):
        local_path = playback_stream[len("file:"):]
        try:
            check_cmd = '[ -f "{}" ] && echo "exists" || echo "not found"'.format(local_path)
            check_output = rdkv_basic_sanity_executeInDUT (sshMethod, credentials, check_cmd, sshPort)
            last_line = check_output.splitlines()[-1].strip() if check_output else ""
            if last_line != "exists":
                return "FAILURE: Playback file not found on DUT: {}".format(local_path)
            print("INFO: Playback file found on DUT: {}".format(local_path))
        except Exception as e:
            return "FAILURE: Could not verify playback file on DUT: {}".format(e)
    else:
        try:
            resp = requests.head(playback_stream, timeout=10)
            if resp.status_code >= 400:
                return "FAILURE: Playback stream returned HTTP {}: {}".format(resp.status_code, playback_stream)
            print("INFO: Playback stream is accessible: {}".format(playback_stream))
        except Exception as e:
            return "FAILURE: Playback stream is not accessible: {}".format(e)

    # Form and execute the gst-launch command
    env_set = "WAYLAND_DISPLAY={} XDG_RUNTIME_DIR=/tmp".format(DISPLAY_NAME)
    gst_cmd = "gst-launch-1.0 -v playbin uri={} flags={}".format(playback_stream, gst_play_flags)
    command = env_set + " " + gst_cmd
    return rdkv_basic_sanity_executeInDUT (sshMethod, credentials, command, sshPort)

#-------------------------------------------------------------------
# GET THE VALUE OF A METHOD VIA JSON-RPC
# Description  : Executes a Thunder JSON-RPC GET call for the specified method
#                and returns the result.
# Parameters   : method - string specifying the full Thunder JSON-RPC method name
#                         (e.g. "org.rdk.DisplaySettings.getConnectedVideoDisplays")
# Return Value : Result of the JSON-RPC call or "EXCEPTION OCCURRED" on error
#-------------------------------------------------------------------
def rdkv_basic_sanity_getValue(method):
    data = '"method": "'+method+'"'
    result = execute_step(data)
    return result

#-------------------------------------------------------------------
# SET VALUE FOR A METHOD VIA JSON-RPC
# Description  : Executes a Thunder JSON-RPC SET call for the specified method
#                with the given parameters and returns the result.
# Parameters   : method - string specifying the full Thunder JSON-RPC method name
#                value  - JSON-formatted string of parameters to pass to the method
# Return Value : Result of the JSON-RPC call or "EXCEPTION OCCURRED" on error
#-------------------------------------------------------------------
def rdkv_basic_sanity_setValue(method,value):
    data = '"method": "'+method+'","params": '+value
    result = execute_step(data)
    return result

#-------------------------------------------------------------------
# GET THE LIST OF INSTALLED PACKAGES USING PACKAGE MANAGER
# Description  : Retrieves the list of packages with state "INSTALLED" from
#                the device via the org.rdk.PackageManagerRDKEMS Thunder plugin.
# Parameters   : None
# Return Value : Tuple (status, package_ids) where status is "SUCCESS" or
#                "FAILURE" and package_ids is a list of installed package ID
#                strings (empty list on failure)
#-------------------------------------------------------------------
def rdkv_get_InstalledPackages():
    try:
        print(f"\nGetting the list of installed packages")

        result = rdkv_basic_sanity_getValue("org.rdk.PackageManagerRDKEMS.1.listPackages")
        if result != "EXCEPTION OCCURRED":
            package_ids = [item["packageId"] for item in result if item["state"] == "INSTALLED"]
            print(f"\nList of packages installed in device: {package_ids}")
            return "SUCCESS", package_ids
        else:
            print(f"\nFailed to get the list of installed packages")
            return "FAILURE", []

    except Exception as e:
        print(f"\nException occurred while getting the list of installed packages: {e}")
        return "FAILURE", []
