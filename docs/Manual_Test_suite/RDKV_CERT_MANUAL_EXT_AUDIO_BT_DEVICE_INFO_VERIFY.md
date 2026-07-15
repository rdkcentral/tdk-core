## TestCase ID
RDKV_MANUAL_EXT_AUDIO_08
## TestCase Name
RDKV_CERT_MANUAL_Ext_Audio_BT_Device_Info_Verify

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the device information of a connected external Bluetooth device can be retrieved accurately from the DUT. This test exercises the RDK audio output manager, the HDMI ARC/eARC interface, and the audio settings APIs to validate external audio device connectivity and output routing. The test confirms that the device type and device ID of the connected Bluetooth device should be listed in the jsonrpc response {"jsonrpc":"2.0","id":3,"result":{"deviceInfo":{"deviceID":" ","name":"Creative Stage","deviceType":"WEARABLE….

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
| 1 | Execute TC01 steps as prerequisite | Execute all steps from TC_EXTERNALAUDIO_MANUAL_01 (Pair and connect an external Bluetooth device) as a prerequisite for this test. | Refer to the expected results of TC_EXTERNALAUDIO_MANUAL_01 (Pair and connect an external Bluetooth device). |
| 2 | Retrieve BT device information | Execute the following curl command to retrieve the device information of the connected external Bluetooth device.<br>`curl --header "Content-Type: application/json" --request POST --data ' {"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.getDeviceInfo", "params": {"deviceID": "<deviceID>"}}' http://127.0.0.1:9998/jsonrpc` | The connected external Bluetooth device information should be listed in the response. Curl response should be like this<br>       {"jsonrpc":"2.0","id":3,"result":{"deviceInfo":{"deviceID":"<deviceID>","name":"Creative Stage","deviceType":"WEARABLE HEADSET","manufacturer":"1881","MAC":"94:9F:3F:69:7E:59","signalStrength":"0","rssi":"0","batteryLevel":"0","modalias":"","firmwareRevision":"","supportedProfile":"Audio Source;Audio Sink;AV Remote Target;AV Remote;PnP Information"},"success":true}} |
| 3 | Validate MAC address in device info | Validate that the curl response contains the MAC address of the connected Bluetooth device.<br>`curl --header "Content-Type: application/json" --request POST --data ' {"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.getDeviceInfo", "params": {"deviceID": "<deviceID>"}}' http://127.0.0.1:9998/jsonrpc` | The MAC address of the connected Bluetooth device should be listed in the jsonrpc response<br><br> {"jsonrpc":"2.0","id":3,"result":{"deviceInfo":{"deviceID":"<deviceID>","name":"Creative Stage","deviceType":"WEARABLE HEADSET","manufacturer":"1881","MAC":"94:9F:3F:69:7E:59","signalStrength":"0","rssi":"0","batteryLevel":"0","modalias":"","firmwareRevision":"","supportedProfile":"Audio Source;Audio Sink;AV Remote Target;AV Remote;PnP Information"},"success":true}}<br><br>Curl response should have this              "MAC":"94:9F:3F:69:7E:59"    |
| 4 | Validate manufacturer ID in device info | Validate that the curl response contains the manufacturer ID of the connected Bluetooth device.<br>`curl --header "Content-Type: application/json" --request POST --data ' {"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.getDeviceInfo", "params": {"deviceID": "<deviceID>"}}' http://127.0.0.1:9998/jsonrpc` | The manufacturer ID of the connected Bluetooth device should be listed in the jsonrpc response<br><br> {"jsonrpc":"2.0","id":3,"result":{"deviceInfo":{"deviceID":"<deviceID>","name":"Creative Stage","deviceType":"WEARABLE HEADSET","manufacturer":"1881","MAC":"94:9F:3F:69:7E:59","signalStrength":"0","rssi":"0","batteryLevel":"0","modalias":"","firmwareRevision":"","supportedProfile":"Audio Source;Audio Sink;AV Remote Target;AV Remote;PnP Information"},"success":true}}<br><br>Curl response should have this              "manufacturer":"1881" |
| 5 | Validate device type and ID in device info | Validate that the curl response contains the device type and device ID of the connected Bluetooth device.<br>`curl --header "Content-Type: application/json" --request POST --data ' {"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.getDeviceInfo", "params": {"deviceID": "<deviceID>"}}' http://127.0.0.1:9998/jsonrpc` | The device type and device ID of the connected Bluetooth device should be listed in the jsonrpc response<br><br>{"jsonrpc":"2.0","id":3,"result":{"deviceInfo":{"deviceID":"<deviceID>","name":"Creative Stage","deviceType":"WEARABLE HEADSET","manufacturer":"1881","MAC":"94:9F:3F:69:7E:59","signalStrength":"0","rssi":"0","batteryLevel":"0","modalias":"","firmwareRevision":"","supportedProfile":"Audio Source;Audio Sink;AV Remote Target;AV Remote;PnP Information"},"success":true}}<br><br>Curl response should have this              "deviceID":"<deviceID>","deviceType":"WEARABLE HEADSET" |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
