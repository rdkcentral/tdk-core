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
To validate that an external Bluetooth device can be successfully paired and connected to the DUT. This test confirms that the DUT remains paired and connected to the specified device and that the paired and connected device lists are correctly updated, ensuring Bluetooth external audio device connectivity meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conduct test in isolated BT environment | Conduct the test in an environment free from interference from multiple Bluetooth devices. | The test environment should be free from Bluetooth interference.|
| 2 | Prepare external Bluetooth device | Ensure the external Bluetooth device used in the test is either a headphone or a Bluetooth soundbar. | A headphone or Bluetooth soundbar should be available and ready for use as the external Bluetooth device.|
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Establish SSH/serial console connection | Establish a serial/SSH console connection to the DUT. | The serial/SSH console connection to the DUT should be established successfully.|
| 2 | Activate org.rdk.Bluetooth plugin | Activate the org.rdk.Bluetooth plugin by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method":"Controller.1.activate", "params":{"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth plugin should be activated.|
| 3 | Validate Bluetooth plugin status | Validate the status of the org.rdk.Bluetooth plugin by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth plugin should be in the activated state.|
| 4 | Enable org.rdk.Bluetooth plugin | Enable the org.rdk.Bluetooth plugin by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.Bluetooth.1.enable"}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth plugin should be enabled.|
| 5 | Start Bluetooth scanning | Start Bluetooth scanning by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.startScan", "params": {"timeout": "90", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | Bluetooth scanning should start and remain active until the timeout.|
| 6 | Retrieve discovered Bluetooth devices | Retrieve the list of discovered Bluetooth devices by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | The discovered device list should be listed in the jsonrpc response.|
| 7 | Pair external Bluetooth device | Identify the target device ID from the discovered list, update the deviceID parameter in the curl command, and execute the following curl command to pair the external Bluetooth device.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.pair", "params": {"deviceID": "163411684589145"}}' http://127.0.0.1:9998/jsonrpc` | The DUT should be successfully paired with the specified device ID|
| 8 | Retrieve paired Bluetooth devices | Retrieve the list of paired Bluetooth devices by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | The paired device should appear in the response with the device ID used for pairing.|
| 9 | Connect paired Bluetooth device | Identify the target device ID from the paired list, update the deviceID parameter in the curl command, and execute the following curl command to connect the paired Bluetooth device.<br>`curl --header "Content-Type: application/json" --request POST --data ' {"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.connect", "params": {"deviceID": "163411684589145", "deviceType": "WEARABLE HEADSET", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The DUT should be successfully connected to the specified paired device ID|
| 10 | Retrieve connected Bluetooth devices | Retrieve the list of connected Bluetooth devices by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | It has to show the connected device which we just connected and|
| 11 | Verify pairing and connection persist | Re-execute Step 8 and Step 10 to validate that the pairing and connection persist for the specified device ID. | The DUT should remain paired and connected to the specified device ID. The curl responses should match those from Step 8 and Step 10.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
