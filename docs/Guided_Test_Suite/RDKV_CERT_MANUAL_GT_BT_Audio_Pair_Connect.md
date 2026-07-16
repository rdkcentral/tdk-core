## TestCase ID
RDKV_MANUAL_GT_BT_AUDIO_01
## TestCase Name
RDKV_CERT_MANUAL_GT_BT_Audio_Pair_Connect

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that an external Bluetooth wearable headset can be successfully discovered, paired, and connected to the DUT using the RDK Bluetooth plugin, completing the full A2DP connection establishment workflow. This test confirms the DUT's Bluetooth stack can discover, pair, and maintain a stable audio connection with an external device in a certified and repeatable manner.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify test script files on DUT | Copy the test script (`BT_AUDIO_AUTOMATED.sh`), the configuration file (`device.conf`), and the helper script (`generic_functions.sh`) to the working directory of the DUT and ensure all files are accessible. Configure the `device.conf` file with all the correct test environment values specific to this test case prior to execution. | The files `BT_AUDIO_AUTOMATED.sh`, `device.conf`, and `generic_functions.sh` must be present and accessible in the DUT's working directory. The `device.conf` file must be populated with all the correct test environment values specific to this test case prior to execution. |
| 2 | Reboot DUT before test | Reboot the DUT before executing the shell script. Verify that the RDK UI home page is visible on the connected HDMI display before proceeding with the test. | The DUT must complete its boot sequence successfully and the RDK UI home page must be visible on the HDMI display prior to test execution. |
| 3 | Verify interference-free BT environment | Ensure the test is conducted in an environment free from interference caused by multiple active Bluetooth devices. No other Bluetooth devices should be actively scanning or pairing in the test vicinity. | The test environment should have no other Bluetooth devices in discoverable or pairing mode to prevent false device discovery or connection conflicts during the scan. |
| 4 | Confirm external BT device type | Confirm that the external Bluetooth device to be used in the test is a headphone or a Bluetooth soundbar that supports the A2DP audio profile. | The external BT device must be a headphone or Bluetooth soundbar capable of A2DP profile pairing and audio streaming. |
| 5 | Set external BT device to pairing mode | Power on the external Bluetooth device and manually place it into pairing/discoverable mode before starting the test script. | The external BT device should be powered on and actively broadcasting in pairing/discoverable mode so that the DUT can detect it during the Bluetooth scan. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Activate Bluetooth plugin | Activate the `org.rdk.Bluetooth` plugin via the `BT_AUDIO_AUTOMATED.sh` script by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method":"Controller.1.activate", "params":{"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth plugin should be activated and the API response should return `"result":null` indicating successful activation. |
| 2 | Verify Bluetooth plugin status | Verify the activation status of the `org.rdk.Bluetooth` plugin by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | The API response should contain `"state":"activated"` confirming that the org.rdk.Bluetooth plugin is in activated state. |
| 3 | Enable Bluetooth | Enable the Bluetooth interface on the DUT by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.Bluetooth.1.enable"}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":true` confirming that Bluetooth is enabled on the DUT. |
| 4 | Start Bluetooth scan | Start a Bluetooth device scan with a 120-second timeout by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.startScan", "params": {"timeout": "120", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The API response should return `"success":true` confirming that the Bluetooth scan has started successfully. |
| 5 | Get discovered devices and locate target device | Retrieve the list of discovered Bluetooth devices and search for `<EXT_BT_devices>` by executing the following curl command. The scan is retried up to `<max_scan_retries>` times if the device is not found:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be found in the discoveredDevices list and its `deviceID` should be extracted successfully. |
| 6 | Pair target BT device | Pair the discovered target device using the extracted `deviceID` by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.pair", "params": {"deviceID": "<found_device_id>"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.pair API should return `"success":true` confirming successful pairing initiation. |
| 7 | Verify pairing in paired devices list | Verify that `<EXT_BT_devices>` is present in the paired devices list by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be listed in the pairedDevices response, confirming successful pairing. The paired devices list should be displayed on the terminal. |
| 8 | Connect the paired BT device | Connect the paired target device as a WEARABLE HEADSET using the DEFAULT profile by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.connect", "params": {"deviceID": "<found_device_id>", "deviceType": "WEARABLE HEADSET", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth.1.connect API should return `"success":true` confirming the connection request was successful. |
| 9 | Verify device in connected devices list | Verify that `<EXT_BT_devices>` is present in the connected devices list by executing the following curl command:<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | The target device `<EXT_BT_devices>` should be listed in the connectedDevices response, confirming successful connection. The connected devices list should be displayed on the terminal. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
