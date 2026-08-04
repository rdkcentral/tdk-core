## TestScript Name
RDKV_CERT_AVS_Bluetooth

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [Set_And_Get_Name](#set_and_get_name)
   - [Bluetooth_Toggle_Discoverable_Status](#bluetooth_toggle_discoverable_status)
   - [Bluetooth_On_Request_Failed](#bluetooth_on_request_failed)
   - [Bluetooth_Get_Discovered_LE_Profile_Devices](#bluetooth_get_discovered_le_profile_devices)
   - [Check_API_Version_Number](#check_api_version_number)
   - [Bluetooth_ActivateDeactivate_Event_Test](#bluetooth_activatedeactivate_event_test)
   - [Bluetooth_Pair_Unpair_LoudSpeaker_Device](#bluetooth_pair_unpair_loudspeaker_device)
   - [Bluetooth_Connect_Disconnect_LoudSpeaker_Device](#bluetooth_connect_disconnect_loudspeaker_device)
   - [Bluetooth_ActivateDeactivate_All_Event_Test](#bluetooth_activatedeactivate_all_event_test)
   - [Bluetooth_Verify_Connect_Error](#bluetooth_verify_connect_error)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **Bluetooth** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.Bluetooth` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of Bluetooth plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Bluetooth plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of Bluetooth plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_System_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of System plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate System plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of System plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Bluetooth_Stack_Enable

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Enable Bluetooth stack | Enable on Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.enable"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |

### Plugin Pre-condition 4: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the onDiscoveredDevice event | Register a WebSocket event listener for `onDiscoveredDevice` to receive `onDiscoveredDevice` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.register", "params": {"event": "onDiscoveredDevice", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the onStatusChanged event | Register a WebSocket event listener for `onStatusChanged` to receive `onStatusChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.register", "params": {"event": "onStatusChanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 3 | Subscribe to the onRequestFailed event | Register a WebSocket event listener for `onRequestFailed` to receive `onRequestFailed` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.register", "params": {"event": "onRequestFailed", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 4 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 5 | Subscribe to the all event | Register a WebSocket event listener for `all` to receive `all` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "all", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 5: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure Bluetooth emulator support | `BT_EMULATOR_SUPPORT` must be set to `yes` if a Bluetooth emulator is available in the test setup, otherwise set to `no` | The Bluetooth emulator support flag should be correctly configured in the device-specific config file |
| 2 | Configure Bluetooth emulator IP | `BT_EMU_IP` must be set to the IP address of the Bluetooth emulator device accessible from the DUT. Required only when `BT_EMULATOR_SUPPORT = yes` | The Bluetooth emulator IP address should be correctly configured in the device-specific config file |
| 3 | Configure Bluetooth emulator user name | `BT_EMU_USER_NAME` must be set to the username used to connect to the Bluetooth emulator. Required only when `BT_EMULATOR_SUPPORT = yes` | The Bluetooth emulator username should be correctly configured in the device-specific config file |
| 4 | Configure Bluetooth emulator password | `BT_EMU_PWD` must be set to the password used to authenticate with the Bluetooth emulator. Required only when `BT_EMULATOR_SUPPORT = yes` | The Bluetooth emulator password should be correctly configured in the device-specific config file |
| 5 | Configure Bluetooth emulator device name | `BT_EMU_DEVICE_NAME` must be set to the name of the Bluetooth emulator device as visible during scanning on the DUT. Required only when `BT_EMULATOR_SUPPORT = yes` | The Bluetooth emulator device name should be correctly configured in the device-specific config file |

## Test Cases

<a id="set_and_get_name"></a>
### TestCase Name
Set_And_Get_Name

### TestCase ID
BT_01

### TestCase Objective
Check whether name of the device can be set and get

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Bluetooth device name | Invoke getName on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the device name is returned successfully (`success` : `true`) |
| 2 | Set Bluetooth device name | Invoke setName on org.rdk.Bluetooth with name: "Test Value"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.setName", "params": {"name": "Test Value"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the name is set successfully (`success` : `true`) |
| 3 | Get Bluetooth device name | Invoke getName on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned device name matches `Test Value` set in step 2 with `success`: `true` |

---

<a id="bluetooth_toggle_discoverable_status"></a>
### TestCase Name
Bluetooth_Toggle_Discoverable_Status

### TestCase ID
BT_02

### TestCase Objective
Toggle bluetooth discoverable status

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Is Bluetooth device discoverable | Invoke isDiscoverable on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.isDiscoverable"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current discoverable status is returned as `true` or `false` with `success`: `true`  |
| 2 | Set Bluetooth device discoverable | Invoke setDiscoverable on org.rdk.Bluetooth with timeout: 10<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.setDiscoverable", "params": {"discoverable": <toggled_value>, "timeout": 10}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the discoverable status is set successfully (`success` : `true`) |
| 3 | Is Bluetooth device discoverable | Invoke isDiscoverable on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.isDiscoverable"}' http://127.0.0.1:9998/jsonrpc` | Verify that the discoverable status matches the toggled value from step 1 and `success` is `true`  |

---

<a id="bluetooth_on_request_failed"></a>
### TestCase Name
Bluetooth_On_Request_Failed

### TestCase ID
BT_03

### TestCase Objective
Checks on request failed event

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Bluetooth device scan | Invoke startScan on org.rdk.Bluetooth with profile: "LOUDSPEAKER", timeout: 30<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.startScan", "params": {"timeout": 30, "profile": "LOUDSPEAKER"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the LOUDSPEAKER scan is started successfully with `STATUS`: `AVAILABLE` |
| 2 | Stop Bluetooth device scan | Invoke stopScan on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.stopScan"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the scan is closed successfully |
| 3 | Get discovered devices | Invoke getDiscoveredDevices on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that the discovered devices list is returned and `<BT_EMU_DEVICE_NAME>` is found in the list |
| 4 | Send Bluetooth pairing request | Invoke pair on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.pair", "params": {"deviceID": <invalid_device_id>}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the pair request is sent successfully |
| 5 | Check on request failed event | Listen for event Event_On_Request_Failed | Ensure the `onRequestFailed` event is received with `NEWSTATUS` as `PAIRING_FAILED`, `PAIRED` as `false`, and `CONNECTED` as `false`, confirming the pairing request failed  |

---

<a id="bluetooth_get_discovered_le_profile_devices"></a>
### TestCase Name
Bluetooth_Get_Discovered_LE_Profile_Devices

### TestCase ID
BT_04

### TestCase Objective
Checks whether LE profile devices are getting discovered

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Bluetooth device scan | Invoke startScan on org.rdk.Bluetooth with profile: "LE", timeout: 30<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.startScan", "params": {"timeout": 30, "profile": "LE"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that LE scan is started successfully |
| 2 | Stop Bluetooth device scan | Invoke stopScan on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.stopScan"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the scan is closed successfully |
| 3 | Get discovered devices | Invoke getDiscoveredDevices on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that the discovered devices list does not contain `<BT_EMU_DEVICE_NAME>`  |

---

<a id="check_api_version_number"></a>
### TestCase Name
Check_API_Version_Number

### TestCase ID
BT_05

### TestCase Objective
Checks the API version Number

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get API version number | Invoke getApiVersionNumber on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getApiVersionNumber"}' http://127.0.0.1:9998/jsonrpc` | Verify that the API version number is returned successfully with value `1` |

---

<a id="bluetooth_activatedeactivate_event_test"></a>
### TestCase Name
Bluetooth_ActivateDeactivate_Event_Test

### TestCase ID
BT_06

### TestCase Objective
Validates statechange event on activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of Bluetooth plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Bluetooth plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of Bluetooth plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate Bluetooth plugin | Invoke deactivate on Controller with callsign: "org.rdk.Bluetooth"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check state change event | Listen for event Event_Controller_State_Changed | Verify that the event is received with callsign `org.rdk.bluetooth`, state `deactivated`, and reason `requested`  |
| 3 | Check plugin active status | Invoke status on Controller for org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate Bluetooth plugin | Invoke activate on Controller with callsign: "org.rdk.Bluetooth"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check state change event | Listen for event Event_Controller_State_Changed | Verify that the event is received with callsign `org.rdk.bluetooth`, state `activated`, and reason `requested`  |
| 6 | Check plugin active status | Invoke status on Controller for org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="bluetooth_pair_unpair_loudspeaker_device"></a>
### TestCase Name
Bluetooth_Pair_Unpair_LoudSpeaker_Device

### TestCase ID
BT_07

### TestCase Objective
Verify bluetooth scanning, pairing, discoverydevice, state change, deviceinfo and unpairing functionality

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Bluetooth device scan | Invoke startScan on org.rdk.Bluetooth with timeout: 30, profile: "LOUDSPEAKER"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.startScan", "params": {"timeout": 30, "profile": "LOUDSPEAKER"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the scan is started successfully |
| 2 | Stop Bluetooth device scan | Invoke stopScan on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.stopScan"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the scan is closed successfully |
| 3 | Get discovered devices | Invoke getDiscoveredDevices on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that `<BT_EMU_DEVICE_NAME>` is found in the discovered devices list |
| 4 | Send Bluetooth pairing request | Invoke pair on org.rdk.Bluetooth with deviceID<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.pair", "params": {"deviceID": "<result_step_4>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the pair request is sent successfully with `success`: `true` |
| 5 | Check on status changed event | Listen for event Event_On_Status_Changed | Ensure the `onStatusChanged` event is received with `NEWSTATUS` as `PAIRING_CHANGE` |
| 6 | Get paired devices | Invoke getPairedDevices on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that device `<BT_EMU_DEVICE_NAME>` is found in the paired devices list  |
| 7 | Get device info | Invoke getDeviceInfo on org.rdk.Bluetooth with deviceID<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDeviceInfo", "params": {"deviceID": "<result_step_4>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that device info is returned successfully |
| 8 | Start Bluetooth device scan | Invoke startScan on org.rdk.Bluetooth with profile: "LOUDSPEAKER", timeout: 30<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.startScan", "params": {"timeout": 30, "profile": "LOUDSPEAKER"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the scan is started successfully |
| 9 | Stop Bluetooth device scan | Invoke stopScan on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.stopScan"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the scan is closed successfully |
| 10 | Get discovered devices | Invoke getDiscoveredDevices on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that the paired device ID is not present in the discovered devices list (device may appear under a different ID after pairing)  |
| 11 | Unpair Bluetooth device | Invoke unpair on org.rdk.Bluetooth with deviceID<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.unpair", "params": {"deviceID": "<result_step_4>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the unpair is completed successfully with `success`: `true` |
| 12 | Check on status changed event | Listen for event Event_On_Status_Changed | Ensure the `onStatusChanged` event is received with `NEWSTATUS` as `PAIRING_CHANGE`, `PAIRED` as `false`, and `CONNECTED` as `false`  |
| 13 | Get discovered devices | Invoke getDiscoveredDevices on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that device `<BT_EMU_DEVICE_NAME>` is NOT found in the discovered devices list after unpair  |

### TestCase Post-condition

#### TestCase Post-condition 1: Unpairing_BT_EMU_Device

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get paired devices | Get Paired Devices from Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that `<BT_EMU_DEVICE_NAME>` is found in the paired devices list |
| 2 | Unpair Bluetooth device | *(Conditional statement executed only if previous step condition is met)*<br>Unpair on Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.unpair", "params": {"deviceID": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the unpair request is completed successfully with `success`: `true` |
| 3 | Get paired devices | *(Conditional statement executed only if previous step condition is met)*<br>Get Paired Devices from Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that the paired devices list is empty  |

---

<a id="bluetooth_connect_disconnect_loudspeaker_device"></a>
### TestCase Name
Bluetooth_Connect_Disconnect_LoudSpeaker_Device

### TestCase ID
BT_08

### TestCase Objective
Verify bluetooth scanning, pairing, discoverydevice, state change, connect, disconnect and unpairing functionality

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Bluetooth device scan | Invoke startScan on org.rdk.Bluetooth with profile: "LOUDSPEAKER", timeout: 30<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.startScan", "params": {"timeout": 30, "profile": "LOUDSPEAKER"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the LOUDSPEAKER scan is started successfully with `STATUS`: `AVAILABLE` |
| 2 | Stop Bluetooth device scan | Invoke stopScan on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.stopScan"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the scan is closed successfully |
| 3 | Get discovered devices | Invoke getDiscoveredDevices on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that `<BT_EMU_DEVICE_NAME>` is found in the discovered devices list |
| 4 | Send Bluetooth pairing request | Invoke pair on org.rdk.Bluetooth with deviceID<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.pair", "params": {"deviceID": "<result_step_4>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the pair request is sent successfully with `success`: `true` |
| 5 | Check paired devices | Invoke getPairedDevices on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that device `<BT_EMU_DEVICE_NAME>` is paired with connected state `False`  |
| 6 | Get device Bluetooth mac | Invoke getDeviceInfo on org.rdk.System with params: "bluetooth_mac"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "bluetooth_mac"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the Bluetooth MAC address is retrieved successfully |
| 7 | Connect to Bluetooth device | Invoke connect on org.rdk.Bluetooth with deviceID, deviceType: "LOUDSPEAKER", profile: "LOUDSPEAKER"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.connect", "params": {"deviceID": "<result_step_4>", "deviceType": "LOUDSPEAKER", "profile": "LOUDSPEAKER"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the connection is established successfully |
| 8 | Check on status changed event | Listen for event Event_On_Status_Changed | Ensure the `onStatusChanged` event is received with `NEWSTATUS` as `CONNECTION_CHANGE` |
| 9 | Check connected device active state | Invoke getConnectedDevices on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that device `<BT_EMU_DEVICE_NAME>` is connected with active state `true`  |
| 10 | Check paired device connection status | Invoke getPairedDevices on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that device `<BT_EMU_DEVICE_NAME>` is paired with connected state `True`  |
| 11 | Disconnect from Bluetooth device | Invoke disconnect on org.rdk.Bluetooth with deviceID, deviceType: "LOUDSPEAKER"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.disconnect", "params": {"deviceID": "<result_step_4>", "deviceType": "LOUDSPEAKER"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the disconnection is successful |
| 12 | Check on status changed event | Listen for event Event_On_Status_Changed | Ensure the `onStatusChanged` event is received with `NEWSTATUS` as `CONNECTION_CHANGE` |
| 13 | Get connected devices | Invoke getConnectedDevices on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected devices list is empty  |
| 14 | Unpair Bluetooth device | Invoke unpair on org.rdk.Bluetooth with deviceID<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.unpair", "params": {"deviceID": "<result_step_4>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the unpair is completed successfully with `success`: `true` |
| 15 | Get discovered devices | Invoke getDiscoveredDevices on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that device `<BT_EMU_DEVICE_NAME>` is NOT found in the discovered devices list, confirming the device was unpaired successfully  |

### TestCase Post-condition

#### TestCase Post-condition 1: Unpairing_BT_EMU_Device

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get connected devices | Get Connected Devices from Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected devices list is checked for cleanup — disconnects `<BT_EMU_DEVICE_NAME>` if still connected (may be empty if already disconnected)  |
| 2 | Disconnect from Bluetooth device | *(Conditional statement executed only if the condition in Step 1 is met)*<br>Disconnect on Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.disconnect", "params": {"deviceID": "<result_step_1>", "deviceType": "LOUDSPEAKER"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the disconnection is successful |
| 3 | Get connected devices | *(Conditional statement executed only if the condition in Step 1 is met)*<br>Get Connected Devices from Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected devices list is empty |
| 4 | Get paired devices | Get Paired Devices from Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that the paired devices list is checked for cleanup — unpairs `<BT_EMU_DEVICE_NAME>` if still paired (may be empty if already unpaired)  |
| 5 | Unpair Bluetooth device | *(Conditional statement executed only if the condition in Step 4 is met)*<br>Unpair on Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.unpair", "params": {"deviceID": "<result_step_4>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the unpair operation is successful with `success`: `true`  |
| 6 | Get paired devices | *(Conditional statement executed only if the condition in Step 4 is met)*<br>Get Paired Devices from Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | Verify that the paired devices list is empty |

---

<a id="bluetooth_activatedeactivate_all_event_test"></a>
### TestCase Name
Bluetooth_ActivateDeactivate_All_Event_Test

### TestCase ID
BT_09

### TestCase Objective
Validates all event on activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of Bluetooth plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Bluetooth plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of Bluetooth plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate Bluetooth plugin | Invoke deactivate on Controller with callsign: "org.rdk.Bluetooth"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check all event | Listen for event Event_Controller_All | Verify that the event is received with callsign `org.rdk.bluetooth`, state `deactivated`, and reason `requested`  |
| 3 | Check plugin active status | Invoke status on Controller for org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate Bluetooth plugin | Invoke activate on Controller with callsign: "org.rdk.Bluetooth"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check all event | Listen for event Event_Controller_All | Verify that the event is received with callsign `org.rdk.bluetooth`, state `activated`, and reason `requested`  |
| 6 | Check plugin active status | Invoke status on Controller for org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="bluetooth_verify_connect_error"></a>
### TestCase Name
Bluetooth_Verify_Connect_Error

### TestCase ID
BT_10

### TestCase Objective
Verify that the connect method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of Bluetooth plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Bluetooth plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of Bluetooth plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate Bluetooth plugin | Invoke deactivate on Controller with callsign: "org.rdk.Bluetooth"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check state change event | Listen for event Event_Controller_State_Changed | Verify that the event is received with callsign `org.rdk.bluetooth`, state `deactivated`, and reason `requested`  |
| 3 | Check plugin active status | Invoke status on Controller for org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Check Bluetooth connect API response | Invoke connect on org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.connect"}' http://127.0.0.1:9998/jsonrpc` | Verify that the API returns the expected error: `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.`  |
| 5 | Activate Bluetooth plugin | Invoke activate on Controller with callsign: "org.rdk.Bluetooth"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 6 | Check state change event | Listen for event Event_Controller_State_Changed | Verify that the event is received with callsign `org.rdk.bluetooth`, state `activated`, and reason `requested`  |
| 7 | Check plugin active status | Invoke status on Controller for org.rdk.Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the onDiscoveredDevice event | Unregister the WebSocket event listener for `onDiscoveredDevice` to stop receiving `onDiscoveredDevice` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.unregister", "params": {"event": "onDiscoveredDevice", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the onStatusChanged event | Unregister the WebSocket event listener for `onStatusChanged` to stop receiving `onStatusChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.unregister", "params": {"event": "onStatusChanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 3 | Unsubscribe from the onRequestFailed event | Unregister the WebSocket event listener for `onRequestFailed` to stop receiving `onRequestFailed` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.unregister", "params": {"event": "onRequestFailed", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 4 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 5 | Unsubscribe from the all event | Unregister the WebSocket event listener for `all` to stop receiving `all` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "all", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |

### Plugin Post-condition 2: Bluetooth_Stack_Disable

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Disable Bluetooth stack | Disable on Bluetooth<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Bluetooth.1.disable"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |

## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 35 mins

**Priority** : High

**Release Version** : M81

<div align="right"><a href="#testscript-name">Go to Top</a></div>
