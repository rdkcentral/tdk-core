## TestCase ID
RDKV_MANUAL_EXTERNALAUDIO_07
## TestCase Name
RDKV_CERT_GT_BT_AUDIO_DEVICE_INFO

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the org.rdk.Bluetooth.getDeviceInfo API returns accurate and complete device information — including device name, MAC address, manufacturer ID, device type, and battery level — for a connected external Bluetooth device.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify interference-free BT environment | Ensure the test is conducted in an environment free from interference caused by multiple active Bluetooth devices. No other Bluetooth devices should be actively scanning or pairing in the test vicinity. | The test environment should have no other Bluetooth devices in discoverable or pairing mode to prevent false device discovery or connection conflicts during the scan. |
| 2 | Confirm external BT device type | Confirm that the external Bluetooth device to be used in the test is a headphone or a Bluetooth soundbar that supports the A2DP audio profile. | The external BT device must be a headphone or Bluetooth soundbar capable of A2DP profile pairing and connection. |
| 3 | Set external BT device to pairing mode | Power on the external Bluetooth device and manually place it into pairing/discoverable mode before starting the test script. | The external BT device should be powered on and actively broadcasting in pairing/discoverable mode so that the DUT can detect it during the Bluetooth scan. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Activate Bluetooth plugin | The script activates the org.rdk.Bluetooth plugin:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method":"Controller.1.activate", "params":{"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"result":null`. |
| 2 | Verify Bluetooth plugin status | The script checks the activation status of the org.rdk.Bluetooth plugin:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | The API response should contain `"state":"activated"`. |
| 3 | Enable Bluetooth | The script enables the Bluetooth interface:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.Bluetooth.1.enable"}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":true`. |
| 4 | Start Bluetooth scan | The script starts a Bluetooth scan:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.startScan", "params": {"timeout": "120", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":true`. |
| 5 | Get discovered devices and locate target device | The script retrieves discovered devices and searches for `<EXT_BT_devices>` (with retry up to `<max_scan_retries>` times):<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be found and its `deviceID` extracted. |
| 6 | Pair target BT device | The script pairs the target device:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.pair", "params": {"deviceID": "<found_device_id>"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.pair API should return `"success":true`. |
| 7 | Verify pairing in paired devices list | The script verifies `<EXT_BT_devices>` is present in the pairedDevices list:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be present in the pairedDevices response. |
| 8 | Connect the paired BT device | The script connects the paired target device as a WEARABLE HEADSET:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.connect", "params": {"deviceID": "<found_device_id>", "deviceType": "WEARABLE HEADSET", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.connect API should return `"success":true`. |
| 9 | Verify device in connected devices list | The script verifies `<EXT_BT_devices>` is present in the connectedDevices list:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be present in the connectedDevices response. |
| 10 | Verify device name and ID via getDeviceInfo | The script executes the following curl command to retrieve device information and verifies that the `deviceID` and `name` fields match the expected `<EXT_BT_devices>` device:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.getDeviceInfo", "params": {"deviceID": "<found_device_id>"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.getDeviceInfo API should return `"success":true` and the response should contain the correct `deviceID` and `name` matching `<EXT_BT_devices>`. |
| 11 | Verify MAC address from getDeviceInfo | The script calls `org.rdk.Bluetooth.getDeviceInfo` again and validates that the `MAC` field in the response matches a valid MAC address format (pattern: `XX:XX:XX:XX:XX:XX`). | The API response should contain a `MAC` field with a value matching a valid MAC address format for the `<EXT_BT_devices>` BT device. |
| 12 | Verify manufacturer ID from getDeviceInfo | The script calls `org.rdk.Bluetooth.getDeviceInfo` and verifies that the `manufacturer` field is present and non-empty in the API response. | The API response should contain a non-empty `manufacturer` field identifying the manufacturer of the `<EXT_BT_devices>` BT device. |
| 13 | Verify device type from getDeviceInfo | The script calls `org.rdk.Bluetooth.getDeviceInfo` and verifies that the `deviceType` field is present and non-empty in the API response. | The API response should contain a non-empty `deviceType` field identifying the type of the `<EXT_BT_devices>` BT device. |
| 14 | Verify battery level from getDeviceInfo | The script calls `org.rdk.Bluetooth.getDeviceInfo` and verifies that the `batteryLevel` field is present and returns a non-zero value in the API response. | The API response should contain a `batteryLevel` field with a non-zero value, confirming the battery level of the `<EXT_BT_devices>` BT device is correctly reported. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
