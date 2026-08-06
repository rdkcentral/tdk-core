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
import websocket
import requests
import json
import threading
import time

# Global state for WiFi scan flow
ssid_event_received = False
ssid_list = []
ws_instance = None
event_thread = None

# Global state for WiFi connect flow
wifi_state_event_received = False
wifi_state_data = {}
ws_connect_instance = None
connect_event_thread = None

THUNDER_PORT = 9998
SCAN_TIMEOUT = 30    # seconds to wait for onAvailableSSIDs event
CONNECT_TIMEOUT = 30  # seconds to wait for onWiFiStateChange event

#----------------------------------------------------------------------
# SET THUNDER PORT
#----------------------------------------------------------------------
def setThunderPort(thunderPort):
    global THUNDER_PORT
    THUNDER_PORT = thunderPort

#----------------------------------------------------------------------
# WEBSOCKET CALLBACKS
#----------------------------------------------------------------------
def on_message(ws, message):
    global ssid_event_received, ssid_list
    try:
        data = json.loads(message)
        method = data.get("method", "")
        if "onAvailableSSIDs" in method:
            params = data.get("params", {})
            ssids = params.get("ssids", [])
            ssid_list = ssids
            ssid_event_received = True
            print("INFO: onAvailableSSIDs event received with {} SSIDs".format(len(ssids)))
            ws.close()
    except Exception as e:
        print("INFO: Could not parse websocket message: {}".format(e))

def on_error(ws, error):
    print("INFO: Websocket error: {}".format(error))

def on_close(ws, close_status_code, close_msg):
    print("INFO: Websocket connection closed")

def on_open(ws):
    # Register for onAvailableSSIDs event
    register_payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "org.rdk.NetworkManager.1.register",
        "params": {
            "event": "onAvailableSSIDs",
            "id": "client.events.1"
        }
    })
    ws.send(register_payload)
    print("INFO: Registered for onAvailableSSIDs event")

#----------------------------------------------------------------------
# START WEBSOCKET LISTENER IN BACKGROUND THREAD
#----------------------------------------------------------------------
def startEventListener(deviceIP):
    global ws_instance
    ws_url = "ws://{}:{}/jsonrpc".format(deviceIP, THUNDER_PORT)
    print("INFO: Connecting to websocket: {}".format(ws_url))
    ws_instance = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws_instance.run_forever()

#----------------------------------------------------------------------
# TRIGGER WIFI SCAN VIA HTTP JSON-RPC
#----------------------------------------------------------------------
def triggerWiFiScan(deviceIP):
    url = "http://{}:{}/jsonrpc".format(deviceIP, THUNDER_PORT)
    payload = {
        "jsonrpc": "2.0",
        "id": 42,
        "method": "org.rdk.NetworkManager.1.StartWiFiScan",
        "params": {
            "frequency": "",
            "ssids": []
        }
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        print("INFO: StartWiFiScan response: {}".format(json.dumps(result)))
        success = result.get("result", {}).get("success", False)
        if success:
            print("INFO: WiFi scan started successfully")
            return True
        else:
            print("FAILURE: WiFi scan did not return success=true")
            return False
    except Exception as e:
        print("FAILURE: Exception during StartWiFiScan: {}".format(e))
        return False

#----------------------------------------------------------------------
# STOP WIFI SCAN VIA HTTP JSON-RPC
#----------------------------------------------------------------------
def stopWiFiScan(deviceIP):
    url = "http://{}:{}/jsonrpc".format(deviceIP, THUNDER_PORT)
    payload = {
        "jsonrpc": "2.0",
        "id": 42,
        "method": "org.rdk.NetworkManager.1.StopWiFiScan"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        print("INFO: StopWiFiScan response: {}".format(json.dumps(result)))
        success = result.get("result", {}).get("success", False)
        if success:
            print("INFO: WiFi scan stopped successfully")
        else:
            print("FAILURE: StopWiFiScan did not return success=true")
        return success
    except Exception as e:
        print("INFO: Exception during StopWiFiScan: {}".format(e))
        return False

#----------------------------------------------------------------------
# MAIN FUNCTION: REGISTER EVENT, TRIGGER SCAN, WAIT FOR RESULT
# Returns list of SSIDs on success, empty list on failure
#----------------------------------------------------------------------
def startWiFiScanAndGetSSIDs(deviceIP, targetSSID="COMCAST_LAB_5G"):
    global ssid_event_received, ssid_list, event_thread

    ssid_event_received = False
    ssid_list = []

    # Start websocket listener in background thread
    event_thread = threading.Thread(target=startEventListener, args=(deviceIP,))
    event_thread.daemon = True
    event_thread.start()

    # Allow time for websocket connection and event registration
    time.sleep(2)

    # Trigger the WiFi scan
    scan_started = triggerWiFiScan(deviceIP)
    if not scan_started:
        if ws_instance:
            ws_instance.close()
        stopWiFiScan(deviceIP)
        return []

    # Wait for onAvailableSSIDs event up to SCAN_TIMEOUT
    print("INFO: Waiting for onAvailableSSIDs event (max {}s)...".format(SCAN_TIMEOUT))
    elapsed = 0
    while elapsed < SCAN_TIMEOUT:
        if ssid_event_received:
            break
        time.sleep(1)
        elapsed += 1

    if ws_instance:
        ws_instance.close()
    event_thread.join(timeout=5)
    stopWiFiScan(deviceIP)

    if ssid_event_received:
        print("SUCCESS: onAvailableSSIDs received with {} SSIDs".format(len(ssid_list)))
        ssid_names = [entry.get("ssid", "") for entry in ssid_list]
        if targetSSID in ssid_names:
            print("SUCCESS: '{}' is present in the scanned SSIDs".format(targetSSID))
        else:
            print("INFO: '{}' is NOT present in the scanned SSIDs".format(targetSSID))
        return ssid_list
    else:
        print("FAILURE: onAvailableSSIDs event not received within {}s".format(SCAN_TIMEOUT))
        return []

#----------------------------------------------------------------------
# WEBSOCKET CALLBACKS FOR WIFI CONNECT
#----------------------------------------------------------------------
def on_wifi_state_message(ws, message):
    global wifi_state_event_received, wifi_state_data
    try:
        data = json.loads(message)
        method = data.get("method", "")
        if "onWiFiStateChange" in method:
            params = data.get("params", {})
            wifi_state_data = params
            wifi_state_event_received = True
            print("INFO: onWiFiStateChange event received: {}".format(json.dumps(params)))
            ws.close()
    except Exception as e:
        print("INFO: Could not parse websocket message: {}".format(e))

def on_wifi_connect_error(ws, error):
    print("INFO: Websocket error (connect): {}".format(error))

def on_wifi_connect_close(ws, close_status_code, close_msg):
    print("INFO: Websocket connection closed (connect)")

def on_wifi_connect_open(ws):
    register_payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "org.rdk.NetworkManager.1.register",
        "params": {
            "event": "onWiFiStateChange",
            "id": "client.events.2"
        }
    })
    ws.send(register_payload)
    print("INFO: Registered for onWiFiStateChange event")

#----------------------------------------------------------------------
# START WEBSOCKET LISTENER FOR WIFI CONNECT IN BACKGROUND THREAD
#----------------------------------------------------------------------
def startWiFiConnectEventListener(deviceIP):
    global ws_connect_instance
    ws_url = "ws://{}:{}/jsonrpc".format(deviceIP, THUNDER_PORT)
    print("INFO: Connecting to websocket for WiFiConnect: {}".format(ws_url))
    ws_connect_instance = websocket.WebSocketApp(
        ws_url,
        on_open=on_wifi_connect_open,
        on_message=on_wifi_state_message,
        on_error=on_wifi_connect_error,
        on_close=on_wifi_connect_close
    )
    ws_connect_instance.run_forever()

#----------------------------------------------------------------------
# TRIGGER WIFI CONNECT VIA HTTP JSON-RPC
#----------------------------------------------------------------------
def triggerWiFiConnect(deviceIP, ssid, passphrase, security):
    url = "http://{}:{}/jsonrpc".format(deviceIP, THUNDER_PORT)
    payload = {
        "jsonrpc": "2.0",
        "id": 42,
        "method": "org.rdk.NetworkManager.1.WiFiConnect",
        "params": {
            "ssid": ssid,
            "passphrase": passphrase,
            "security": security
        }
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        print("INFO: WiFiConnect response: {}".format(json.dumps(result)))
        success = result.get("result", {}).get("success", False)
        if success:
            print("INFO: WiFiConnect call returned success=true")
            return True
        else:
            print("FAILURE: WiFiConnect did not return success=true")
            return False
    except Exception as e:
        print("FAILURE: Exception during WiFiConnect: {}".format(e))
        return False

#----------------------------------------------------------------------
# DISCONNECT FROM WIFI VIA HTTP JSON-RPC
#----------------------------------------------------------------------
def disconnectFromWiFi(deviceIP):
    url = "http://{}:{}/jsonrpc".format(deviceIP, THUNDER_PORT)
    payload = {
        "jsonrpc": "2.0",
        "id": 42,
        "method": "org.rdk.NetworkManager.1.WiFiDisconnect"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        print("INFO: WiFiDisconnect response: {}".format(json.dumps(result)))
        success = result.get("result", {}).get("success", False)
        if success:
            print("INFO: WiFiDisconnect returned success=true")
        else:
            print("FAILURE: WiFiDisconnect did not return success=true")
        return success
    except Exception as e:
        print("INFO: Exception during WiFiDisconnect: {}".format(e))
        return False

#----------------------------------------------------------------------
# GET CONNECTED SSID VIA HTTP JSON-RPC
#----------------------------------------------------------------------
def getConnectedSSID(deviceIP):
    url = "http://{}:{}/jsonrpc".format(deviceIP, THUNDER_PORT)
    payload = {
        "jsonrpc": "2.0",
        "id": 42,
        "method": "org.rdk.NetworkManager.1.GetConnectedSSID"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        print("INFO: GetConnectedSSID response: {}".format(json.dumps(result)))
        return result.get("result", {})
    except Exception as e:
        print("FAILURE: Exception during GetConnectedSSID: {}".format(e))
        return {}

#----------------------------------------------------------------------
# MAIN FUNCTION: CONNECT TO WIFI SSID AND VERIFY
# Returns True on success, False on failure
#----------------------------------------------------------------------
def connectToWiFiSSID(deviceIP, ssid, passphrase, security=6):
    global wifi_state_event_received, wifi_state_data, ws_connect_instance, connect_event_thread

    wifi_state_event_received = False
    wifi_state_data = {}

    # Start websocket listener for onWiFiStateChange in background thread
    connect_event_thread = threading.Thread(target=startWiFiConnectEventListener, args=(deviceIP,))
    connect_event_thread.daemon = True
    connect_event_thread.start()

    # Allow time for websocket connection and event registration
    time.sleep(2)

    # Trigger WiFi connect
    connect_triggered = triggerWiFiConnect(deviceIP, ssid, passphrase, security)
    if not connect_triggered:
        if ws_connect_instance:
            ws_connect_instance.close()
        return False

    # Wait for onWiFiStateChange event up to CONNECT_TIMEOUT
    print("INFO: Waiting for onWiFiStateChange event (max {}s)...".format(CONNECT_TIMEOUT))
    elapsed = 0
    while elapsed < CONNECT_TIMEOUT:
        if wifi_state_event_received:
            break
        time.sleep(1)
        elapsed += 1

    if ws_connect_instance:
        ws_connect_instance.close()
    connect_event_thread.join(timeout=5)

    if not wifi_state_event_received:
        print("FAILURE: onWiFiStateChange event not received within {}s".format(CONNECT_TIMEOUT))
        return False

    # Verify connection via GetConnectedSSID
    connected_info = getConnectedSSID(deviceIP)
    connected_ssid = connected_info.get("ssid", "")
    conn_success = connected_info.get("success", False)

    if conn_success and connected_ssid == ssid:
        print("SUCCESS: Connected to SSID '{}' successfully".format(ssid))
        result = True
    else:
        print("FAILURE: Expected SSID '{}' but got '{}' (success={})".format(ssid, connected_ssid, conn_success))
        result = False

    # Disconnect after validation
    disconnectFromWiFi(deviceIP)
    return result

#----------------------------------------------------------------------
# COMMAND-LINE ENTRY POINT
# Usage:
#   python tdkvThunderWifiUtility.py scan   <deviceIP> [thunderPort] [targetSSID]
#   python tdkvThunderWifiUtility.py connect <deviceIP> <ssid> <passphrase> [security] [thunderPort]
#----------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    def _usage():
        print("Usage:")
        print("  python tdkvThunderWifiUtility.py scan    <deviceIP> [thunderPort] [targetSSID]")
        print("  python tdkvThunderWifiUtility.py connect <deviceIP> <ssid> <passphrase> [security] [thunderPort]")
        sys.exit(1)

    if len(sys.argv) < 3:
        _usage()

    command   = sys.argv[1].lower()
    device_ip = sys.argv[2]

    if command == "scan":
        port       = int(sys.argv[3]) if len(sys.argv) > 3 else 9998
        target     = sys.argv[4] if len(sys.argv) > 4 else None
        setThunderPort(port)
        ssids = startWiFiScanAndGetSSIDs(device_ip, targetSSID=target) if target else startWiFiScanAndGetSSIDs(device_ip)
        print("INFO: Total SSIDs found: {}".format(len(ssids)))

    elif command == "connect":
        if len(sys.argv) < 5:
            _usage()
        ssid       = sys.argv[3]
        passphrase = sys.argv[4]
        security   = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        port       = int(sys.argv[6]) if len(sys.argv) > 6 else 9998
        setThunderPort(port)

        # Step 1: Scan and verify SSID is visible before connecting
        print("INFO: Scanning for SSID '{}' before connecting...".format(ssid))
        ssids = startWiFiScanAndGetSSIDs(device_ip, targetSSID=ssid)
        ssid_names = [entry.get("ssid", "") for entry in ssids]
        if ssid not in ssid_names:
            print("FAILURE: SSID '{}' not found in scan results. Aborting connect.".format(ssid))
            sys.exit(1)
        print("INFO: SSID '{}' found in scan. Proceeding to connect...".format(ssid))

        # Step 2: Connect, verify, disconnect
        ok = connectToWiFiSSID(device_ip, ssid, passphrase, security)
        sys.exit(0 if ok else 1)

    else:
        print("ERROR: Unknown command '{}'. Use 'scan' or 'connect'.".format(command))
        _usage()
