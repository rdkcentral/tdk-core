## TestCase ID
RDKV_MANUAL_EXTERNALAUDIO_03
## TestCase Name
RDKV_CERT_GT_BT_AUDIO_DISCONNECT_UNPAIR

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that an external Bluetooth device that is actively streaming audio can be successfully disconnected and unpaired from the DUT using the org.rdk.Bluetooth plugin APIs, and that the device is no longer present in the connected or paired device lists after the operations.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify interference-free BT environment | Ensure the test is conducted in an environment free from interference caused by multiple active Bluetooth devices. No other Bluetooth devices should be actively scanning or pairing in the test vicinity. | The test environment should have no other Bluetooth devices in discoverable or pairing mode to prevent false device discovery or connection conflicts during the scan. |
| 2 | Confirm external BT device type | Confirm that the external Bluetooth device to be used in the test is a headphone or a Bluetooth soundbar that supports the A2DP audio profile. | The external BT device must be a headphone or Bluetooth soundbar capable of A2DP profile pairing and audio streaming. |
| 3 | Set external BT device to pairing mode | Power on the external Bluetooth device and manually place it into pairing/discoverable mode before starting the test script. | The external BT device should be powered on and actively broadcasting in pairing/discoverable mode so that the DUT can detect it during the Bluetooth scan. |
| 4 | Sign in to YouTube App on DUT | Ensure the YouTube App is installed on the DUT and signed in with a valid user account prior to the test. The app must be accessible via `AppManager.launchApp` with `intent: playback` and the configured deeplink URL `<yt_URL>`. | The YouTube App must be installed, signed in with a valid account, and launchable via the AppManager deeplink API so that AV playback can be initiated successfully during Step 10 of the test. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Activate Bluetooth plugin | The script executes the following curl command to activate the org.rdk.Bluetooth plugin:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method":"Controller.1.activate", "params":{"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth plugin should be activated and the API response should return `"result":null`. |
| 2 | Verify Bluetooth plugin status | The script executes the following curl command to check the activation status of the org.rdk.Bluetooth plugin:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | The API response should contain `"state":"activated"`. |
| 3 | Enable Bluetooth | The script executes the following curl command to enable the Bluetooth interface on the DUT:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.Bluetooth.1.enable"}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":true`. |
| 4 | Start Bluetooth scan | The script executes the following curl command to initiate a Bluetooth scan:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.startScan", "params": {"timeout": "120", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":true`. |
| 5 | Get discovered devices and locate target device | The script retrieves discovered devices and searches for `<EXT_BT_devices>` (retrying up to `<max_scan_retries>` times if needed):<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be found and its `deviceID` extracted. |
| 6 | Pair target BT device | The script pairs the discovered target device:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.pair", "params": {"deviceID": "<found_device_id>"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.pair API should return `"success":true`. |
| 7 | Verify pairing in paired devices list | The script verifies `<EXT_BT_devices>` is in the pairedDevices list:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be present in the pairedDevices response. |
| 8 | Connect the paired BT device | The script connects the paired target device as a WEARABLE HEADSET:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.connect", "params": {"deviceID": "<found_device_id>", "deviceType": "WEARABLE HEADSET", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.connect API should return `"success":true`. |
| 9 | Verify device in connected devices list | The script verifies `<EXT_BT_devices>` is in the connectedDevices list:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be present in the connectedDevices response. |
| 10 | Start AV playback via AppManager deeplink | The script verifies YouTube is installed, then launches it with a deeplink URL:<br>`curl -d '{ "jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.launchApp", "params": { "appId": "<youtube_appId>", "intent": "playback", "launchArgs": "<yt_URL>" }}' http://localhost:9998/jsonrpc`<br><br>The script prompts: *"Is YouTube App launched and started AV playback with deeplink URL [yes/no]:"* | The AppManager.launchApp API should return `"result":null` and the tester should confirm AV playback has started. |
| 11 | Verify audio streaming via BT device | The script prompts: *"Are you able to hear the Audio streaming via `<EXT_BT_devices>` BT device? [yes/no]:"* | The tester should confirm with `yes` that audio is streaming through the `<EXT_BT_devices>` Bluetooth device. |
| 12 | Disconnect the paired BT device | The script executes the following curl command to disconnect the connected BT device:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.disconnect", "params": {"deviceID": "<device_id>"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.disconnect API should return `"success":true` confirming successful disconnection. |
| 13 | Verify device removed from connected list | The script executes the following curl command to retrieve the connected devices list and verifies that `<EXT_BT_devices>` is no longer present:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should not be present in the connectedDevices list, confirming successful disconnection. |
| 14 | Unpair the BT device | The script executes the following curl command to unpair the Bluetooth device:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.unpair", "params": {"deviceID": "<device_id>"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.unpair API should return `"success":true` confirming the unpairing was successful. |
| 15 | Verify device removed from paired list | The script executes the following curl command to retrieve the paired devices list and verifies that `<EXT_BT_devices>` is no longer present:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should not be present in the pairedDevices list, confirming successful unpairing. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
