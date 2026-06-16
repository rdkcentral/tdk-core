## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [Set_And_Get_Name (BT_01)](#set_and_get_name-bt_01)
   - [Bluetooth_Toggle_Discoverable_Status (BT_02)](#bluetooth_toggle_discoverable_status-bt_02)
   - [Bluetooth_On_Request_Failed (BT_03)](#bluetooth_on_request_failed-bt_03)
   - [Bluetooth_Get_Discovered_LE_Profile_Devices (BT_04)](#bluetooth_get_discovered_le_profile_devices-bt_04)
   - [Check_API_Version_Number (BT_05)](#check_api_version_number-bt_05)
   - [Bluetooth_ActivateDeactivate_Event_Test (BT_06)](#bluetooth_activatedeactivate_event_test-bt_06)
   - [Bluetooth_Pair_Unpair_LoudSpeaker_Device (BT_07)](#bluetooth_pair_unpair_loudspeaker_device-bt_07)
   - [Bluetooth_Connect_Disconnect_LoudSpeaker_Device (BT_08)](#bluetooth_connect_disconnect_loudspeaker_device-bt_08)
   - [Bluetooth_ActivateDeactivate_All_Event_Test (BT_09)](#bluetooth_activatedeactivate_all_event_test-bt_09)
   - [Bluetooth_Verify_Connect_Error (BT_10)](#bluetooth_verify_connect_error-bt_10)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **Bluetooth** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.Bluetooth` (version 1)

**API Coverage:**

- **State / Query APIs**: `getApiVersionNumber`, `getConnectedDevices`, `getDeviceInfo`, `getDiscoveredDevices`, `getName`, `getPairedDevices`, `isDiscoverable`
- **Lifecycle / Control APIs**: `connect`, `disconnect`, `pair`, `startScan`, `stopScan`, `unpair`
- **Configuration APIs**: `disable`, `enable`, `setDiscoverable`, `setName`
- **Events**: `onDiscoveredDevice`, `onRequestFailed`, `onStatusChanged`

### APIs Under Test

| API | Description |
|-----|-------------|
| `connect` | Connects to the given Bluetooth device |
| `disable` | Disables the Bluetooth stack |
| `disconnect` | Disconnects the given device from this device |
| `enable` | Enables the Bluetooth stack |
| `getApiVersionNumber` | Provides the current API version number |
| `getConnectedDevices` | Returns a list of connected devices to this device |
| `getDeviceInfo` | Returns the device info of the given device ID |
| `getDiscoveredDevices` | Gives discovered Bluetooth devices |
| `getName` | Provides name of the device as seen by other Bluetooth devices |
| `getPairedDevices` | Returns a list of devices that have paired with this device |
| `isDiscoverable` | Provides discoverable status of the device |
| `pair` | Pairs the given device with this device |
| `setDiscoverable` | Sets the discoverable status of the device |
| `setName` | Sets the name of this device as seen by other Bluetooth devices |
| `startScan` | Searches for available Bluetooth devices |
| `stopScan` | Stops scanning for Bluetooth devices |
| `unpair` | Unpairs the given device with this device |

### Events Under Test

| Event | Description |
|-------|-------------|
| `onDiscoveredDevice` | Gives discovered Bluetooth devices |
| `onRequestFailed` | Indicates on request failed |
| `onStatusChanged` | Gives status change information |

---

## Pre-conditions

### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.Bluetooth"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Activate_System_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.System"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 3: Bluetooth_Stack_Enable

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Enable Bluetooth Stack | Invoke `enable` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.enable"}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |

### Pre-condition 4: Register_And_Listen_Events

- Register and listen to event `Event_On_Discovered_Device` on `Bluetooth` plugin

- Register and listen to event `Event_On_Status_Changed` on `Bluetooth` plugin

- Register and listen to event `Event_On_Request_Failed` on `Bluetooth` plugin

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

- Register and listen to event `Event_Controller_All` on `Controller` plugin

---

## Test Cases

<a id="set_and_get_name-bt_01"></a>
### Set_And_Get_Name (BT_01)

**Objective:** Check whether name of the device can be set and get

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Bluetooth Device Name | Invoke `getName` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getName"}' http://127.0.0.1:9998/jsonrpc` | Device name returned successfully `success`: `true` |
| 2 | Set Bluetooth Device Name | Invoke `setName` on `org.rdk.Bluetooth` with `name`: `"Test Value"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.setName", "params": {"name": "Test Value"}}' http://127.0.0.1:9998/jsonrpc` | Name set successfully `success`: `true` |
| 3 | Get Bluetooth Device Name | Invoke `getName` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getName"}' http://127.0.0.1:9998/jsonrpc` | Expected `Test Value`; `success`: `true` (name matches the value set in step 2) |

---

<a id="bluetooth_toggle_discoverable_status-bt_02"></a>
### Bluetooth_Toggle_Discoverable_Status (BT_02)

**Objective:** Toggle bluetooth discoverable status

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Is Bluetooth Device Discoverable | Invoke `isDiscoverable` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.isDiscoverable"}' http://127.0.0.1:9998/jsonrpc` | Current discoverable status returned (`true` or `false`) `success`: `true` |
| 2 | Set Bluetooth Device Discoverable | Invoke `setDiscoverable` on `org.rdk.Bluetooth` with `discoverable`: toggled value from step 1, `timeout`: `<timeout>`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.setDiscoverable", "params": {"discoverable": <toggled_value>, "timeout": <timeout>}}' http://127.0.0.1:9998/jsonrpc` | Discoverable status set successfully `success`: `true` |
| 3 | Is Bluetooth Device Discoverable | Invoke `isDiscoverable` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.isDiscoverable"}' http://127.0.0.1:9998/jsonrpc` | Discoverable status matches toggled value from step 1 `success`: `true` |

---

<a id="bluetooth_on_request_failed-bt_03"></a>
### Bluetooth_On_Request_Failed (BT_03)

**Objective:** Checks on request failed event

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Scan | Invoke `startScan` on `org.rdk.Bluetooth` with `timeout`: `<timeout>`, `profile`: `"LOUDSPEAKER"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.startScan", "params": {"timeout": <timeout>, "profile": "LOUDSPEAKER"}}' http://127.0.0.1:9998/jsonrpc` | Scan started `STATUS`: `AVAILABLE` |
| 2 | Stop Scan | Invoke `stopScan` on `org.rdk.Bluetooth` (wait 30 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.stopScan"}' http://127.0.0.1:9998/jsonrpc` | Scan closed successfully |
| 3 | Get Discovered Devices | Invoke `getDiscoveredDevices` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | Discovered devices list returned; `<BT_EMU_DEVICE_NAME>` found in list |
| 4 | Pair | Invoke `pair` on `org.rdk.Bluetooth` with an invalid `deviceID` (to trigger pairing failure)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.pair", "params": {"deviceID": <invalid_device_id>}}' http://127.0.0.1:9998/jsonrpc` | Pair request sent successfully |
| 5 | Check On Request Failed Event | Listen for event `Event_On_Request_Failed` | Event received; `NEWSTATUS`: `PAIRING_FAILED`, `PAIRED`: `false`, `CONNECTED`: `false` |

---

<a id="bluetooth_get_discovered_le_profile_devices-bt_04"></a>
### Bluetooth_Get_Discovered_LE_Profile_Devices (BT_04)

**Objective:** Checks whether LE profile devices are getting discovered

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Scan | Invoke `startScan` on `org.rdk.Bluetooth` with `timeout`: `<timeout>`, `profile`: `"LE"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.startScan", "params": {"timeout": <timeout>, "profile": "LE"}}' http://127.0.0.1:9998/jsonrpc` | LE scan started successfully |
| 2 | Stop Scan | Invoke `stopScan` on `org.rdk.Bluetooth` (wait 30 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.stopScan"}' http://127.0.0.1:9998/jsonrpc` | Scan closed successfully |
| 3 | Get Discovered Devices | Invoke `getDiscoveredDevices` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | Discovered devices list should not return `<BT_EMU_DEVICE_NAME>` |

---

<a id="check_api_version_number-bt_05"></a>
### Check_API_Version_Number (BT_05)

**Objective:** Checks the API version Number

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get API Version Number | Invoke `getApiVersionNumber` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getApiVersionNumber"}' http://127.0.0.1:9998/jsonrpc` | Expected `1` |

---

<a id="bluetooth_activatedeactivate_event_test-bt_06"></a>
### Bluetooth_ActivateDeactivate_Event_Test (BT_06)

**Objective:** Validates statechange event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.Bluetooth"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate Bluetooth Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.Bluetooth"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for event `Event_Controller_State_Changed` | Event received: callsign `org.rdk.bluetooth`, state `deactivated`, reason `requested` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate Bluetooth Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.Bluetooth"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check State Change Event | Listen for event `Event_Controller_State_Changed` | Event received: callsign `org.rdk.bluetooth`, state `activated`, reason `requested` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="bluetooth_pair_unpair_loudspeaker_device-bt_07"></a>
### Bluetooth_Pair_Unpair_LoudSpeaker_Device (BT_07)

**Objective:** Verify bluetooth scanning, pairing, discoverydevice, state change, deviceinfo and unpairing functionality

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Scan | Invoke `startScan` on `org.rdk.Bluetooth` with `timeout`: `"<value>"`, `profile`: `"LOUDSPEAKER"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.startScan", "params": {"timeout": "<value>", "profile": "LOUDSPEAKER"}}' http://127.0.0.1:9998/jsonrpc` | Scan started successfully |
| 2 | Stop Scan | Invoke `stopScan` on `org.rdk.Bluetooth` (wait 30 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.stopScan"}' http://127.0.0.1:9998/jsonrpc` | Scan closed successfully |
| 3 | Get Discovered Devices | Invoke `getDiscoveredDevices` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | Expected `<BT_EMU_DEVICE_NAME>` |
| 4 | Pair | Invoke `pair` on `org.rdk.Bluetooth` with `deviceID`: `"<result_step_4>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.pair", "params": {"deviceID": "<result_step_4>"}}' http://127.0.0.1:9998/jsonrpc` | Expected `true` |
| 5 | Check On Status Changed Event | Listen for event `Event_On_Status_Changed` | Expected event status: `PAIRING_CHANGE` |
| 6 | Get Paired Devices | Invoke `getPairedDevices` on `org.rdk.Bluetooth` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | Device `<BT_EMU_DEVICE_NAME>` found in paired devices list |
| 7 | Get Device Info | Invoke `getDeviceInfo` on `org.rdk.Bluetooth` with `deviceID`: `"<result_step_4>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDeviceInfo", "params": {"deviceID": "<result_step_4>"}}' http://127.0.0.1:9998/jsonrpc` | Device Info returned successfully |
| 8 | Start Scan | Invoke `startScan` on `org.rdk.Bluetooth` with `timeout`: `<timeout>`, `profile`: `"LOUDSPEAKER"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.startScan", "params": {"timeout": <timeout>, "profile": "LOUDSPEAKER"}}' http://127.0.0.1:9998/jsonrpc` | Scan started successfully |
| 9 | Stop Scan | Invoke `stopScan` on `org.rdk.Bluetooth` (wait 30 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.stopScan"}' http://127.0.0.1:9998/jsonrpc` | Scan closed successfully |
| 10 | Get Discovered Devices | Invoke `getDiscoveredDevices` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | Paired device ID not present in discovered list (device may appear under a different device ID after pairing) |
| 11 | Unpair | Invoke `unpair` on `org.rdk.Bluetooth` with `deviceID`: `"<result_step_4>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.unpair", "params": {"deviceID": "<result_step_4>"}}' http://127.0.0.1:9998/jsonrpc` | Unpair successful `success`: `true` |
| 12 | Check On Status Changed Event | Listen for event `Event_On_Status_Changed` | Event received `NEWSTATUS`: `PAIRING_CHANGE`, `PAIRED`: `false`, `CONNECTED`: `false` |
| 13 | Get Discovered Devices | Invoke `getDiscoveredDevices` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | Device `<BT_EMU_DEVICE_NAME>` NOT found in discovered devices after unpair |

**Post-condition:**

#### Post-condition 1: Unpairing_BT_EMU_Device

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Paired Devices | Invoke `getPairedDevices` on `org.rdk.Bluetooth` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | Expected `<BT_EMU_DEVICE_NAME>` |
| 2 | Unpair | Invoke `unpair` on `org.rdk.Bluetooth` with `deviceID`: `"<result_step_1>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.unpair", "params": {"deviceID": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Expected `true` |
| 3 | Get Paired Devices | Invoke `getPairedDevices` on `org.rdk.Bluetooth` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | Paired devices list is empty |

---

<a id="bluetooth_connect_disconnect_loudspeaker_device-bt_08"></a>
### Bluetooth_Connect_Disconnect_LoudSpeaker_Device (BT_08)

**Objective:** Verify bluetooth scanning, pairing, discoverydevice, state change, connect, disconnect and unpairing functionality

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Scan | Invoke `startScan` on `org.rdk.Bluetooth` with `timeout`: `<timeout>`, `profile`: `"LOUDSPEAKER"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.startScan", "params": {"timeout": <timeout>, "profile": "LOUDSPEAKER"}}' http://127.0.0.1:9998/jsonrpc` | Scan started `STATUS`: `AVAILABLE` |
| 2 | Stop Scan | Invoke `stopScan` on `org.rdk.Bluetooth` (wait 30 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.stopScan"}' http://127.0.0.1:9998/jsonrpc` | Scan closed successfully |
| 3 | Get Discovered Devices | Invoke `getDiscoveredDevices` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | Expected `<BT_EMU_DEVICE_NAME>` |
| 4 | Pair | Invoke `pair` on `org.rdk.Bluetooth` with `deviceID`: `"<result_step_4>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.pair", "params": {"deviceID": "<result_step_4>"}}' http://127.0.0.1:9998/jsonrpc` | Expected `true` |
| 5 | Check Paired Devices | Invoke `getPairedDevices` on `org.rdk.Bluetooth` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | Device `<BT_EMU_DEVICE_NAME>` paired, connected state: `False` |
| 6 | Get Device Bluetooth Mac | Invoke `getDeviceInfo` on `org.rdk.System` with `params`: `"bluetooth_mac"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "bluetooth_mac"}}' http://127.0.0.1:9998/jsonrpc` | Bluetooth MAC address retrieved successfully |
| 7 | Connect | Invoke `connect` on `org.rdk.Bluetooth` with `deviceID`: `"<result_step_4>"`, `deviceType`: `"LOUDSPEAKER"`, `profile`: `"LOUDSPEAKER"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.connect", "params": {"deviceID": "<result_step_4>", "deviceType": "LOUDSPEAKER", "profile": "LOUDSPEAKER"}}' http://127.0.0.1:9998/jsonrpc` | Connection established successfully |
| 8 | Check On Status Changed Event | Listen for event `Event_On_Status_Changed` | Expected event status `CONNECTION_CHANGE` |
| 9 | Check Connected Device Active State | Invoke `getConnectedDevices` on `org.rdk.Bluetooth` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | Device `<BT_EMU_DEVICE_NAME>` connected with active state: `true` |
| 10 | Check Paired Device Connection Status | Invoke `getPairedDevices` on `org.rdk.Bluetooth` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | Device `<BT_EMU_DEVICE_NAME>` paired, connected state: `True` |
| 11 | Disconnect | Invoke `disconnect` on `org.rdk.Bluetooth` with `deviceID`: `"<result_step_4>"`, `deviceType`: `"LOUDSPEAKER"` (wait 40 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.disconnect", "params": {"deviceID": "<result_step_4>", "deviceType": "LOUDSPEAKER"}}' http://127.0.0.1:9998/jsonrpc` | Disconnection successful |
| 12 | Check On Status Changed Event | Listen for event `Event_On_Status_Changed` | Expected event status: `CONNECTION_CHANGE` |
| 13 | Get Connected Devices | Invoke `getConnectedDevices` on `org.rdk.Bluetooth` (wait 2 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | Connected devices list is empty |
| 14 | Unpair | Invoke `unpair` on `org.rdk.Bluetooth` with `deviceID`: `"<result_step_4>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.unpair", "params": {"deviceID": "<result_step_4>"}}' http://127.0.0.1:9998/jsonrpc` | Expected `true` |
| 15 | Get Discovered Devices | Invoke `getDiscoveredDevices` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | Device `<BT_EMU_DEVICE_NAME>` NOT found in discovered devices (device unpaired) |

**Post-condition:**

#### Post-condition 1: Unpairing_BT_EMU_Device

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Connected Devices | Invoke `getConnectedDevices` on `org.rdk.Bluetooth` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | Connected devices list checked for cleanup (conditional: disconnects `<BT_EMU_DEVICE_NAME>` if still connected; may be empty if already cleaned up) |
| 2 | Disconnect | Invoke `disconnect` on `org.rdk.Bluetooth` with `deviceID`: `"<result_step_1>"`, `deviceType`: `"LOUDSPEAKER"` (wait 40 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.disconnect", "params": {"deviceID": "<result_step_1>", "deviceType": "LOUDSPEAKER"}}' http://127.0.0.1:9998/jsonrpc` | **Conditional** (only if device found in step 1) Disconnect successful |
| 3 | Get Connected Devices | Invoke `getConnectedDevices` on `org.rdk.Bluetooth` (wait 2 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | **Conditional** (only if device found in step 1) Connected devices list confirmed empty |
| 4 | Get Paired Devices | Invoke `getPairedDevices` on `org.rdk.Bluetooth` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | Paired devices list checked for cleanup (conditional: unpairs `<BT_EMU_DEVICE_NAME>` if still paired; may be empty if already cleaned up) |
| 5 | Unpair | Invoke `unpair` on `org.rdk.Bluetooth` with `deviceID`: `"<result_step_4>"` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.unpair", "params": {"deviceID": "<result_step_4>"}}' http://127.0.0.1:9998/jsonrpc` | **Conditional** (only if device found in step 4) Unpair successful `success`: `true` |
| 6 | Get Paired Devices | Invoke `getPairedDevices` on `org.rdk.Bluetooth` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | **Conditional** (only if device found in step 4) Paired devices list confirmed empty |

---

<a id="bluetooth_activatedeactivate_all_event_test-bt_09"></a>
### Bluetooth_ActivateDeactivate_All_Event_Test (BT_09)

**Objective:** Validates all event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.Bluetooth"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate Bluetooth Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.Bluetooth"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check All Event | Listen for event `Event_Controller_All` | Event received: callsign `org.rdk.bluetooth`, state `deactivated`, reason `requested` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate Bluetooth Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.Bluetooth"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check All Event | Listen for event `Event_Controller_All` | Event received: callsign `org.rdk.bluetooth`, state `activated`, reason `requested` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="bluetooth_verify_connect_error-bt_10"></a>
### Bluetooth_Verify_Connect_Error (BT_10)

**Objective:** Verify that the connect method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.Bluetooth"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate Bluetooth Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.Bluetooth"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for event `Event_Controller_State_Changed` | Event received: callsign `org.rdk.bluetooth`, state `deactivated`, reason `requested` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Check Bluetooth Connect API Response | Invoke `connect` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.connect"}' http://127.0.0.1:9998/jsonrpc` | Expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate Bluetooth Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.Bluetooth"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 6 | Check State Change Event | Listen for event `Event_Controller_State_Changed` | Event received: callsign `org.rdk.bluetooth`, state `activated`, reason `requested` |
| 7 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

---

## Post-conditions

### Post-condition 1: Bluetooth_Stack_Disable

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Disable Bluetooth Stack | Invoke `disable` on `org.rdk.Bluetooth`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.disable"}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 35 minutes |
| Priority | Medium |
| TDK Release Version | M81 |