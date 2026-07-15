## TestCase ID
RDKV_MANUAL_EXT_AUDIO_01
## TestCase Name
RDKV_CERT_MANUAL_Ext_Audio_BT_Device_Pair_Connect

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that an external Bluetooth device can be successfully paired and connected to the DUT. This test exercises the RDK audio output manager, the HDMI ARC/eARC interface, and the audio settings APIs to validate external audio device connectivity and output routing. The test confirms that the DUT should remain paired and connected to the specified device ID. The curl responses should match those from Step 8 and Step 10.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conduct test in isolated BT environment | Conduct the test in an environment free from interference from multiple Bluetooth devices. | The test environment should be free from Bluetooth interference. |
| 2 | Prepare external Bluetooth device | Ensure the external Bluetooth device used in the test is either a headphone or a Bluetooth soundbar. | A headphone or Bluetooth soundbar should be available and ready for use as the external Bluetooth device. |
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access. |
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Establish SSH/serial console connection | Establish a serial/SSH console connection to the DUT. | The serial/SSH console connection to the DUT should be established successfully. |
| 2 | Activate org.rdk.Bluetooth plugin | Activate the org.rdk.Bluetooth plugin by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method":"Controller.1.activate", "params":{"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth plugin should be activated. The curl response should be:<br>{"jsonrpc":"2.0","id":2,"result":null} |
| 3 | Validate Bluetooth plugin status | Validate the status of the org.rdk.Bluetooth plugin by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth plugin should be in the activated state. The curl response should be:<br>{"jsonrpc":"2.0","id":2,"result":[{"callsign":"org.rdk.Bluetooth","locator":"libWPEFrameworkBluetooth.so","classname":"Bluetooth","autostart":false,"precondition":["Platform"],"startmode":"Deactivated","state":"activated","observers":0,"module":"Plugin_Bluetooth","version":{"hash":"engineering_build_for_debug_purpose_only","major":1,"minor":0,"patch":10}}]} |
| 4 | Enable org.rdk.Bluetooth plugin | Enable the org.rdk.Bluetooth plugin by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.Bluetooth.1.enable"}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth plugin should be enabled. The curl response should be:<br><br>{"jsonrpc":"2.0","id":2,"result":{"success":true}} |
| 5 | Start Bluetooth scanning | Start Bluetooth scanning by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.startScan", "params": {"timeout": "90", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | Bluetooth scanning should start and remain active until the timeout. The curl response should be:<br><br>{"jsonrpc":"2.0","id":3,"result":{"status":"AVAILABLE","success":true}} |
| 6 | Retrieve discovered Bluetooth devices | Retrieve the list of discovered Bluetooth devices by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | The discovered device list should be listed in the jsonrpc response. The curl response should be similar to:<br>Eg :-<br>{"jsonrpc":"2.0","id":3,"result":{"discoveredDevices":[{"deviceID":"83720958864549","name":"TV","deviceType":"TV","connected":false,"paired":false,"rawDeviceType":"2622524","rawBleDeviceType":"0"},{"deviceID":"83774104897620","name":"MiTV-MOOQ0","deviceType":"TV","connected":false,"paired":false,"rawDeviceType":"2622524","rawBleDeviceType":"0"},{"deviceID":"70526358341298","name":"test tv","deviceType":"TV","connected":false,"paired":false,"rawDeviceType":"2622524","rawBleDeviceType":"0"},{"deviceID":"83720958867195","name":"TV","deviceType":"TV","connected":false,"paired":false,"rawDeviceType":"2622524","rawBleDeviceType":"0"},{"deviceID":"70526358616032","name":"test tv","deviceType":"TV","connected":false,"paired":false,"rawDeviceType":"2622524","rawBleDeviceType":"0"},{"deviceID":"17786566777093","name":"MiTV-MOOQ1","deviceType":"TV","connected":false,"paired":false,"rawDeviceType":"2622524","rawBleDeviceType":"0"},{"deviceID":"27415752740586","name":"MiTV-MOOQ1","deviceType":"TV","connected":false,"paired":false,"rawDeviceType":"2622524","rawBleDeviceType":"0"} |
| 7 | Pair external Bluetooth device | Identify the target device ID from the discovered list, update the deviceID parameter in the curl command, and execute the following curl command to pair the external Bluetooth device.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.pair", "params": {"deviceID": "<deviceID>"}}' http://127.0.0.1:9998/jsonrpc` | The DUT should be successfully paired with the specified device ID and curl response should be like this<br>{"jsonrpc":"2.0","id":3,"result":{"success":true}} |
| 8 | Retrieve paired Bluetooth devices | Retrieve the list of paired Bluetooth devices by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | The paired device should appear in the response with the device ID used for pairing. The curl response should be:<br>Eg :-<br>{"jsonrpc":"2.0","id":3,"result":{"pairedDevices":[{"deviceID":"<deviceID>","name":"Creative Stage","deviceType":"WEARABLE HEADSET","connected":true,"rawDeviceType":"2360324","rawBleDeviceType":"0"}],"success":true}} |
| 9 | Connect paired Bluetooth device | Identify the target device ID from the paired list, update the deviceID parameter in the curl command, and execute the following curl command to connect the paired Bluetooth device.<br>`curl --header "Content-Type: application/json" --request POST --data ' {"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.connect", "params": {"deviceID": "<deviceID>", "deviceType": "WEARABLE HEADSET", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The DUT should be successfully connected to the specified paired device ID and curl response should be like this<br><br>{"jsonrpc":"2.0","id":3,"result":{"success":true}} |
| 10 | Retrieve connected Bluetooth devices | Retrieve the list of connected Bluetooth devices by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | It has to show the connected device which we just connected and curl response should be like this<br>Eg :-<br>{"jsonrpc":"2.0","id":3,"result":{"connectedDevices":[{"deviceID":"<deviceID>","name":"Creative Stage","deviceType":"WEARABLE HEADSET","activeState":"1","rawDeviceType":"2360324","rawBleDeviceType":"0"}],"success":true}} |
| 11 | Verify pairing and connection persist | Re-execute Step 8 and Step 10 to validate that the pairing and connection persist for the specified device ID. | The DUT should remain paired and connected to the specified device ID. The curl responses should match those from Step 8 and Step 10. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
