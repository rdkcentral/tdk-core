## TestCase ID
RDKV_MANUAL_GT_BT_AUDIO_04
## TestCase Name
RDKV_CERT_MANUAL_GT_BT_Audio_Reboot_Reconnect

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT correctly detects an audio interruption when a connected Bluetooth wearable headset is rebooted, and that the external device automatically re-establishes its Bluetooth connection to the DUT after powering back on. This test confirms the resilience and auto-reconnect behavior of the RDK Bluetooth stack, ensuring a paired BT audio device can rejoin the DUT after a power cycle without manual re-pairing.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`BT_AUDIO_AUTOMATED.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with all the correct test environment values specific to this test case prior to execution. | The files `BT_AUDIO_AUTOMATED.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with the correct test environment values prior to test execution. |
| 2 | Connect HDMI display to DUT | Connect an HDMI display to the DUT and ensure the correct HDMI input source is selected on the display prior to the test. | The HDMI display must be connected to the DUT and the RDK UI must be visible on the screen prior to test execution. |
| 3 | Verify DUT network connectivity | Ensure the DUT is connected to an active network (WiFi or Ethernet) prior to test execution. | The DUT must have active network connectivity so that YouTube AV playback can be initiated successfully during the test. |
| 4 | Verify interference-free BT environment | Ensure the test is conducted in an environment free from interference caused by multiple active Bluetooth devices. No other Bluetooth devices should be actively scanning or pairing in the test vicinity. | The test environment should have no other Bluetooth devices in discoverable or pairing mode to prevent false device discovery or connection conflicts during the scan. |
| 5 | Confirm external BT device type | Verify that the external Bluetooth device to be used in the test supports the A2DP audio profile (e.g., wearable headset, Bluetooth soundbar, or wireless speaker). | The external BT device must support the A2DP audio profile and be capable of A2DP pairing and audio streaming with the DUT. |
| 6 | Set external BT device to pairing mode | Power on the external Bluetooth device and manually place it into pairing/discoverable mode before starting the test script. | The external BT device should be powered on and actively broadcasting in pairing/discoverable mode so that the DUT can detect it during the Bluetooth scan. |
| 7 | Verify and sign in to YouTube app | Ensure the YouTube App is installed on the DUT and signed in with a valid user account prior to the test. The app must be accessible via `AppManager.launchApp` with `intent: playback` and the configured deeplink URL `<yt_URL>`. | The YouTube App must be installed, signed in with a valid account, and launchable via the AppManager deeplink API so that AV playback can be initiated successfully during Step 10 of the test. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Activate Bluetooth plugin | Activate the `org.rdk.Bluetooth` plugin via the `BT_AUDIO_AUTOMATED.sh` script by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method":"Controller.1.activate", "params":{"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | The `org.rdk.Bluetooth` plugin should be activated and the API response should return `"result":null` indicating successful activation. |
| 2 | Verify Bluetooth plugin status | Verify the activation status of the `org.rdk.Bluetooth` plugin by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | The API response should contain `"state":"activated"`, confirming the org.rdk.Bluetooth plugin is in activated state. |
| 3 | Enable Bluetooth | Enable the Bluetooth interface on the DUT by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.Bluetooth.1.enable"}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":true`, confirming the Bluetooth interface is enabled and ready for device scanning. |
| 4 | Start Bluetooth scan | Start a Bluetooth device scan with a 120-second timeout by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.startScan", "params": {"timeout": "120", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":true` and the DUT should begin actively scanning for nearby Bluetooth devices. |
| 5 | Get discovered devices and locate target device | Retrieve the discovered Bluetooth devices and search for `<EXT_BT_devices>` by executing the following curl command. The scan is retried up to `<max_scan_retries>` times if not found:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be found and its `deviceID` extracted. |
| 6 | Pair target BT device | Pair the discovered target device by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.pair", "params": {"deviceID": "<found_device_id>"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.pair API should return `"success":true` and the target BT device should be successfully paired with the DUT. |
| 7 | Verify pairing in paired devices list | Verify that `<EXT_BT_devices>` is present in the paired devices list by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be listed in the pairedDevices response, confirming successful pairing. The paired devices list should be displayed on the terminal. |
| 8 | Connect the paired BT device | Connect the paired target device as a WEARABLE HEADSET by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.connect", "params": {"deviceID": "<found_device_id>", "deviceType": "WEARABLE HEADSET", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.connect API should return `"success":true` and the BT device should be successfully connected to the DUT and available for audio streaming. |
| 9 | Verify device in connected devices list | Verify that `<EXT_BT_devices>` is present in the connected devices list by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be listed in the connectedDevices response, confirming successful connection. The connected devices list should be displayed on the terminal. |
| 10 | Start AV playback via AppManager deeplink | The script verifies YouTube is installed and launches it with a deeplink URL:<br>`curl -d '{ "jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.launchApp", "params": { "appId": "<youtube_appId>", "intent": "playback", "launchArgs": "<yt_URL>" }}' http://localhost:9998/jsonrpc`<br><br>The script prompts: *"Is YouTube App launched and started AV playback with deeplink URL [yes/no]:"* | The AppManager.launchApp API should return `"result":null` and the tester should confirm AV playback has started. |
| 11 | Verify audio streaming via BT device | The script prompts: *"Are you able to hear the Audio streaming via `<EXT_BT_devices>` BT device? [yes/no]:"* | The tester should confirm with `yes` that audio is streaming through the `<EXT_BT_devices>` Bluetooth device. |
| 12 | Reboot BT device and verify audio stops | The script displays the message: *"Reboot the External Bt Device and wait..."*<br><br>The tester must manually reboot the external BT device. The script then prompts: *"Are you able to hear the Audio streaming via `<EXT_BT_devices>` BT device few seconds after reboot? [yes/no]:"* | The tester should respond `no` — audio streaming should stop after the BT device is rebooted. If the tester responds `yes` (audio continues) the step is marked FAIL, as the expected behavior is that audio stops when the BT device reboots. |
| 13 | Verify BT device auto-reconnects to DUT | The script waits 30 seconds, then polls `org.rdk.Bluetooth.1.getConnectedDevices` up to `<max_reconnect_check>` times (with 20-second intervals) to check if the BT device has auto-reconnected:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc`<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should reappear in the connectedDevices list within the polling period, confirming successful auto-reconnect. The connected and paired device lists should be displayed on the terminal. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
