## TestCase ID
RDKV_MANUAL_GT_BT_AUDIO_07
## TestCase Name
RDKV_CERT_MANUAL_GT_BT_Audio_Device_Info

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT's Bluetooth stack correctly exposes complete and accurate device metadata — including name, MAC address, manufacturer ID, device type, and battery level — for a paired and connected external Bluetooth wearable headset. This test confirms that the Bluetooth device information API returns valid attribute values for all required fields, which is a key requirement for Bluetooth external audio certification compliance.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`BT_AUDIO_AUTOMATED.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with all the correct test environment values specific to this test case prior to execution. | The files `BT_AUDIO_AUTOMATED.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with the correct test environment values prior to test execution. |
| 2 | Verify interference-free BT environment | Ensure the test is conducted in an environment free from interference caused by multiple active Bluetooth devices. No other Bluetooth devices should be actively scanning or pairing in the test vicinity. | The test environment should have no other Bluetooth devices in discoverable or pairing mode to prevent false device discovery or connection conflicts during the scan. |
| 3 | Confirm external BT device type | Confirm that the external Bluetooth device to be used in the test is a headphone or a Bluetooth soundbar that supports the A2DP audio profile. | The external BT device must be a headphone or Bluetooth soundbar capable of A2DP profile pairing and connection. |
| 4 | Set external BT device to pairing mode | Power on the external Bluetooth device and manually place it into pairing/discoverable mode before starting the test script. | The external BT device should be powered on and actively broadcasting in pairing/discoverable mode so that the DUT can detect it during the Bluetooth scan. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Activate Bluetooth plugin | Activate the `org.rdk.Bluetooth` plugin via the `BT_AUDIO_AUTOMATED.sh` script by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method":"Controller.1.activate", "params":{"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | The `org.rdk.Bluetooth` plugin should be activated and the API response should return `"result":null`. |
| 2 | Verify Bluetooth plugin status | Verify the activation status of the `org.rdk.Bluetooth` plugin by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | The API response should contain `"state":"activated"`. |
| 3 | Enable Bluetooth | Enable the Bluetooth interface on the DUT by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.Bluetooth.1.enable"}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":true`. |
| 4 | Start Bluetooth scan | Start a Bluetooth device scan with a 120-second timeout by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.startScan", "params": {"timeout": "120", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":true`. |
| 5 | Get discovered devices and locate target device | Retrieve the discovered Bluetooth devices and search for `<EXT_BT_devices>` by executing the following curl command. The scan is retried up to `<max_scan_retries>` times if not found:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be found and its `deviceID` extracted. |
| 6 | Pair target BT device | Pair the discovered target device by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.pair", "params": {"deviceID": "<found_device_id>"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.pair API should return `"success":true`. |
| 7 | Verify pairing in paired devices list | Verify that `<EXT_BT_devices>` is present in the paired devices list by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be present in the pairedDevices response. |
| 8 | Connect the paired BT device | Connect the paired target device as a WEARABLE HEADSET by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.connect", "params": {"deviceID": "<found_device_id>", "deviceType": "WEARABLE HEADSET", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.connect API should return `"success":true`. |
| 9 | Verify device in connected devices list | Verify that `<EXT_BT_devices>` is present in the connected devices list by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be present in the connectedDevices response. |
| 10 | Verify device name and ID via getDeviceInfo | Retrieve complete device information for `<EXT_BT_devices>` using the `org.rdk.Bluetooth.getDeviceInfo` API and verify that the `deviceID` and `name` fields match the expected values by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.getDeviceInfo", "params": {"deviceID": "<found_device_id>"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.getDeviceInfo API should return `"success":true` and the response should contain the correct `deviceID` and `name` matching `<EXT_BT_devices>`. |
| 11 | Verify MAC address from getDeviceInfo | Call `org.rdk.Bluetooth.getDeviceInfo` again and validate that the `MAC` field in the response matches a valid MAC address format (pattern: `XX:XX:XX:XX:XX:XX`). | The API response should contain a `MAC` field with a value matching a valid MAC address format for the `<EXT_BT_devices>` BT device. |
| 12 | Verify manufacturer ID from getDeviceInfo | The script calls `org.rdk.Bluetooth.getDeviceInfo` and verifies that the `manufacturer` field is present and non-empty in the API response. | The API response should contain a non-empty `manufacturer` field identifying the manufacturer of the `<EXT_BT_devices>` BT device. |
| 13 | Verify device type from getDeviceInfo | The script calls `org.rdk.Bluetooth.getDeviceInfo` and verifies that the `deviceType` field is present and non-empty in the API response. | The API response should contain a non-empty `deviceType` field identifying the type of the `<EXT_BT_devices>` BT device. |
| 14 | Verify battery level from getDeviceInfo | The script calls `org.rdk.Bluetooth.getDeviceInfo` and verifies that the `batteryLevel` field is present and returns a non-zero value in the API response. | The API response should contain a `batteryLevel` field with a non-zero value, confirming the battery level of the `<EXT_BT_devices>` BT device is correctly reported. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
