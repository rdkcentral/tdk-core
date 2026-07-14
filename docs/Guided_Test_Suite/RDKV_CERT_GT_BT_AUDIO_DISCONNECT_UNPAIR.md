## TestCase ID
RDKV_GT_BT_AUDIO_03
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
To validate that an actively streaming external Bluetooth wearable headset can be successfully disconnected and unpaired from the DUT using the `org.rdk.Bluetooth.1.disconnect` and `org.rdk.Bluetooth.1.unpair` APIs, as exercised by the `BT_AUDIO_AUTOMATED.sh` test script. The test verifies that after `disconnect` the device is absent from the `getConnectedDevices` response, and after `unpair` it is absent from the `getPairedDevices` response, confirming both teardown operations completed successfully. This test ensures the Bluetooth teardown workflow on the DUT correctly removes a previously active audio streaming device from both connected and paired device lists.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`BT_AUDIO_AUTOMATED.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with all the correct test environment values specific to this test case prior to execution. | The files `BT_AUDIO_AUTOMATED.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Verify interference-free BT environment | Ensure the test is conducted in an environment free from interference caused by multiple active Bluetooth devices. No other Bluetooth devices should be actively scanning or pairing in the test vicinity. | The test environment should have no other Bluetooth devices in discoverable or pairing mode to prevent false device discovery or connection conflicts during the scan. |
| 3 | Confirm external BT device type | Confirm that the external Bluetooth device to be used in the test is a headphone or a Bluetooth soundbar that supports the A2DP audio profile. | The external BT device must be a headphone or Bluetooth soundbar capable of A2DP profile pairing and audio streaming. |
| 4 | Set external BT device to pairing mode | Power on the external Bluetooth device and manually place it into pairing/discoverable mode before starting the test script. | The external BT device should be powered on and actively broadcasting in pairing/discoverable mode so that the DUT can detect it during the Bluetooth scan. |
| 5 | Verify and sign in to YouTube app | Ensure the YouTube App is installed on the DUT and signed in with a valid user account prior to the test. The app must be accessible via `AppManager.launchApp` with `intent: playback` and the configured deeplink URL `<yt_URL>`. | The YouTube App must be installed, signed in with a valid account, and launchable via the AppManager deeplink API so that AV playback can be initiated successfully during Step 10 of the test. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Activate Bluetooth plugin | Activate the `org.rdk.Bluetooth` plugin via the `BT_AUDIO_AUTOMATED.sh` script by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method":"Controller.1.activate", "params":{"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth plugin should be activated and the API response should return `"result":null`. |
| 2 | Verify Bluetooth plugin status | Verify the activation status of the `org.rdk.Bluetooth` plugin by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | The API response should contain `"state":"activated"`. |
| 3 | Enable Bluetooth | Enable the Bluetooth interface on the DUT by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.Bluetooth.1.enable"}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":true`. |
| 4 | Start Bluetooth scan | Start a Bluetooth device scan with a 120-second timeout by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.startScan", "params": {"timeout": "120", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":true`. |
| 5 | Get discovered devices and locate target device | Retrieve the discovered Bluetooth devices and search for `<EXT_BT_devices>` by executing the following curl command. The scan is retried up to `<max_scan_retries>` times if not found:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be found and its `deviceID` extracted. |
| 6 | Pair target BT device | Pair the discovered target device by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.pair", "params": {"deviceID": "<found_device_id>"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.pair API should return `"success":true`. |
| 7 | Verify pairing in paired devices list | Verify that `<EXT_BT_devices>` is present in the paired devices list by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be present in the pairedDevices response. |
| 8 | Connect the paired BT device | Connect the paired target device as a WEARABLE HEADSET by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.connect", "params": {"deviceID": "<found_device_id>", "deviceType": "WEARABLE HEADSET", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.connect API should return `"success":true`. |
| 9 | Verify device in connected devices list | Verify that `<EXT_BT_devices>` is present in the connected devices list by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be present in the connectedDevices response. |
| 10 | Start AV playback via AppManager deeplink | The script verifies YouTube is installed, then launches it with a deeplink URL:<br>`curl -d '{ "jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.launchApp", "params": { "appId": "<youtube_appId>", "intent": "playback", "launchArgs": "<yt_URL>" }}' http://localhost:9998/jsonrpc`<br><br>The script prompts: *"Is YouTube App launched and started AV playback with deeplink URL [yes/no]:"* | The AppManager.launchApp API should return `"result":null` and the tester should confirm AV playback has started. |
| 11 | Verify audio streaming via BT device | The script prompts: *"Are you able to hear the Audio streaming via `<EXT_BT_devices>` BT device? [yes/no]:"* | The tester should confirm with `yes` that audio is streaming through the `<EXT_BT_devices>` Bluetooth device. |
| 12 | Disconnect the paired BT device | Disconnect the connected BT device by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.disconnect", "params": {"deviceID": "<device_id>"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.disconnect API should return `"success":true` confirming successful disconnection. |
| 13 | Verify device removed from connected list | Verify that `<EXT_BT_devices>` is no longer present in the connected devices list by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should not be present in the connectedDevices list, confirming successful disconnection. |
| 14 | Unpair the BT device | Unpair the BT device by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.unpair", "params": {"deviceID": "<device_id>"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.unpair API should return `"success":true` confirming the unpairing was successful. |
| 15 | Verify device removed from paired list | Verify that `<EXT_BT_devices>` is no longer present in the paired devices list by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should not be present in the pairedDevices list, confirming successful unpairing. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
