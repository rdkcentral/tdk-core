## TestCase ID
RDKV_MANUAL_EXTERNALAUDIO_02
## TestCase Name
RDKV_CERT_GT_BT_AUDIO_AV_STREAMING

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that active AV audio streaming can be established from the DUT to a connected external Bluetooth wearable headset, as exercised by the `BT_AUDIO_AUTOMATED.sh` test script. The test triggers AV playback via the `org.rdk.AppManager.launchApp` API with `intent: playback` and a configured YouTube deeplink URL (`<yt_URL>`), then verifies that audio is audible through the connected external BT device with tester confirmation. This test confirms that the DUT Bluetooth audio routing to a paired external wearable headset is fully operational during active YouTube media streaming.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Ensure the test script (`BT_AUDIO_AUTOMATED.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) are present in the working directory of the DUT before executing the test. The `device.conf` file must be configured with the correct values required for this specific test prior to execution. | The files `BT_AUDIO_AUTOMATED.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Verify interference-free BT environment | Ensure the test is conducted in an environment free from interference caused by multiple active Bluetooth devices. No other Bluetooth devices should be actively scanning or pairing in the test vicinity. | The test environment should have no other Bluetooth devices in discoverable or pairing mode to prevent false device discovery or connection conflicts during the scan. |
| 3 | Confirm external BT device type | Confirm that the external Bluetooth device to be used in the test is a headphone or a Bluetooth soundbar that supports the A2DP audio profile. | The external BT device must be a headphone or Bluetooth soundbar capable of A2DP profile pairing and audio streaming. |
| 4 | Set external BT device to pairing mode | Power on the external Bluetooth device and manually place it into pairing/discoverable mode before starting the test script. | The external BT device should be powered on and actively broadcasting in pairing/discoverable mode so that the DUT can detect it during the Bluetooth scan. |
| 5 | Sign in to YouTube App on DUT | Ensure the YouTube App is installed on the DUT and signed in with a valid user account prior to the test. The app must be accessible via `AppManager.launchApp` with `intent: playback` and the configured deeplink URL `<yt_URL>`. | The YouTube App must be installed, signed in with a valid account, and launchable via the AppManager deeplink API so that AV playback can be initiated successfully during Step 10 of the test. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Activate Bluetooth plugin | Activate the `org.rdk.Bluetooth` plugin via the `BT_AUDIO_AUTOMATED.sh` script by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method":"Controller.1.activate", "params":{"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | The `org.rdk.Bluetooth` plugin should be activated and the API response should return `"result":null`. |
| 2 | Verify Bluetooth plugin status | The script executes the following curl command to check the activation status of the org.rdk.Bluetooth plugin:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | The API response should contain `"state":"activated"`. |
| 3 | Enable Bluetooth | The script executes the following curl command to enable the Bluetooth interface on the DUT:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.Bluetooth.1.enable"}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":true`. |
| 4 | Start Bluetooth scan | The script executes the following curl command to initiate a Bluetooth device scan with a 120-second timeout:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.startScan", "params": {"timeout": "120", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":true` confirming that the Bluetooth scan has started. |
| 5 | Get discovered devices and locate target device | The script executes the following curl command to retrieve discovered devices and searches for `<EXT_BT_devices>`. Scan is retried up to `<max_scan_retries>` times if not found:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be found in the discoveredDevices list and its `deviceID` should be extracted. |
| 6 | Pair target BT device | The script executes the following curl command to pair the discovered target device:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.pair", "params": {"deviceID": "<found_device_id>"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.pair API should return `"success":true`. |
| 7 | Verify pairing in paired devices list | The script executes the following curl command to verify `<EXT_BT_devices>` appears in the pairedDevices list:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be present in the pairedDevices response. |
| 8 | Connect the paired BT device | The script executes the following curl command to connect the paired target device as a WEARABLE HEADSET:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.connect", "params": {"deviceID": "<found_device_id>", "deviceType": "WEARABLE HEADSET", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.connect API should return `"success":true`. |
| 9 | Verify device in connected devices list | The script executes the following curl command to verify `<EXT_BT_devices>` appears in the connectedDevices list:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be present in the connectedDevices response. |
| 10 | Start AV playback via AppManager deeplink | The script checks if YouTube is installed via `AppManager.getInstalledApps` and `AppManager.isInstalled`, then launches it with a deeplink playback URL using the following curl command:<br>`curl -d '{ "jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.launchApp", "params": { "appId": "<youtube_appId>", "intent": "playback", "launchArgs": "<yt_URL>" }}' http://localhost:9998/jsonrpc`<br><br>The script then prompts: *"Is YouTube App launched and started AV playback with deeplink URL [yes/no]:"* — the tester must respond `yes` to confirm. | The AppManager.launchApp API should return `"result":null` and the tester should confirm that YouTube launched and AV playback started successfully via deeplink. |
| 11 | Verify audio streaming via BT device | The script prompts: *"Are you able to hear the Audio streaming via `<EXT_BT_devices>` BT device? [yes/no]:"* — the tester must listen to the connected BT device and respond `yes` if audio is audible. | The tester should confirm with `yes` that audio streaming is audible through the `<EXT_BT_devices>` Bluetooth device. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
