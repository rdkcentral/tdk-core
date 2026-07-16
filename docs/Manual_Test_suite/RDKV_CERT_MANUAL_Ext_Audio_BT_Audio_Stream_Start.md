## TestCase ID
RDKV_MANUAL_EXT_AUDIO_02
## TestCase Name
RDKV_CERT_MANUAL_Ext_Audio_BT_Audio_Stream_Start

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that audio streaming from an external Bluetooth device can be successfully initiated and played back through the DUT. This test exercises the `org.rdk.Bluetooth` plugin APIs, including scanning, pairing, connecting, and audio stream initiation, to validate that the DUT routes audio output through the paired Bluetooth device. The test confirms that audio is audible from the external Bluetooth device during active video playback and that streaming operates correctly throughout the session.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conduct test in isolated BT environment | Conduct the test in an environment free from interference from multiple Bluetooth devices. | The test environment should be free from Bluetooth interference.|
| 2 | Prepare external Bluetooth device | Ensure the external Bluetooth device used in the test is either a headphone or a Bluetooth soundbar. | A headphone or Bluetooth soundbar should be available and ready for use as the external Bluetooth device.|
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|
| 5 | Install YouTube or Amazon Prime Video app | If YouTube or Amazon Prime Video is not already available in the My Apps section/row of the RDK UI Home screen, select the respective application tile from the Recommended Apps row (or the More Apps tab if not visible) and press Enter/OK on the remote. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds before disappearing. | The YouTube or Amazon Prime Video application should be installed successfully on the DUT.|
| 6 | Verify app listed on home screen | Validate that the installed YouTube or Amazon Prime Video application is listed under the My Apps section/row and App Info page of the RDK UI Home screen, confirming it is ready to launch. | The YouTube or Amazon Prime Video application should be visible in the My Apps section and on the App Info page, ready to launch.|
| 7 | Sign in to app and verify A/V playback | Sign in to YouTube or Amazon Prime Video with valid user credentials and validate A/V playback prior to test execution. | Sign-in should succeed and A/V playback should be functional in the application.|
| 8 | Verify app launch and content access | Validate that YouTube or Amazon Prime Video launches successfully from the RDK UI and that content is accessible prior to test execution. | The application should launch correctly from the RDK UI and content should be accessible.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Establish SSH/serial console connection | Establish a serial/SSH console connection to the DUT. | The serial/SSH console connection to the DUT should be established successfully.|
| 2 | Activate org.rdk.Bluetooth plugin | Activate the org.rdk.Bluetooth plugin by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method":"Controller.1.activate", "params":{"callsign": "org.rdk.Bluetooth"}}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth plugin should be activated.|
| 3 | Validate Bluetooth plugin status | Validate the status of the org.rdk.Bluetooth plugin by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "Controller.1.status@org.rdk.Bluetooth"}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth plugin should be in the activated state.|
| 4 | Enable org.rdk.Bluetooth plugin | Enable the org.rdk.Bluetooth plugin by executing the following curl command.<br><br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.Bluetooth.1.enable"}' http://127.0.0.1:9998/jsonrpc` | The org.rdk.Bluetooth plugin should be enabled.|
| 5 | Start Bluetooth scanning | Start Bluetooth scanning by executing the following curl command.<br><br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.startScan", "params": {"timeout": "90", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | Bluetooth scanning should start and remain active until the timeout.|
| 6 | Retrieve discovered Bluetooth devices | Retrieve the list of discovered Bluetooth devices by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getDiscoveredDevices"}' http://127.0.0.1:9998/jsonrpc` | The discovered device list should be listed in the jsonrpc response.|
| 7 | Pair external Bluetooth device | Identify the target device ID from the discovered list, update the deviceID parameter in the curl command, and execute the following curl command to pair the external Bluetooth device.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.pair", "params": {"deviceID": "163411684589145"}}' http://127.0.0.1:9998/jsonrpc` | The DUT should be successfully paired with the specified device ID|
| 8 | Retrieve paired Bluetooth devices | Retrieve the list of paired Bluetooth devices by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getPairedDevices"}' http://127.0.0.1:9998/jsonrpc` | The paired device should appear in the response with the device ID used for pairing.|
| 9 | Connect paired Bluetooth device | Identify the target device ID from the paired list, update the deviceID parameter in the curl command, and execute the following curl command to connect the paired Bluetooth device.<br>`curl --header "Content-Type: application/json" --request POST --data ' {"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.connect", "params": {"deviceID": "163411684589145", "deviceType": "WEARABLE HEADSET", "profile": "DEFAULT"}}' http://127.0.0.1:9998/jsonrpc` | The DUT should be successfully connected to the specified paired device ID|
| 10 | Retrieve connected Bluetooth devices | Retrieve the list of connected Bluetooth devices by executing the following curl command.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.getConnectedDevices"}' http://127.0.0.1:9998/jsonrpc` | The connected external Bluetooth device should appear in the response.|
| 11 | Verify pairing and connection persist | Re-execute Step 8 and Step 10 to validate that the pairing and connection persist for the specified device ID. | The DUT should remain paired and connected to the specified device ID. The curl responses should match those from Step 8 and Step 10.|
| 12 | Launch YouTube or Amazon Prime Video app | Select the YouTube or Amazon Prime Video application tile from the My Apps/Recommended Apps section/row of the RDK RDK UI Home screen and press Enter/OK on the remote. |  The YouTube or Amazon Prime Video application should launch successfully  (Either cold launch /hot launch based on the app’s previous state)|
| 13 | Select content and initiate A/V playback | Select any video content and initiate AV stream playback (YouTube or Amazon Prime Video). | The selected AV stream should play with proper Audio and Video output.|
| 14 | Validate audio streaming from BT device | Validate that audio streaming has started from the external Bluetooth device. | (By default Audio streaming from External BT device should start automatically once its successfully connected which is the expected behaviour)<br>Audio should start streaming from BT Device and should be able to hear the audio from External BT device|
| 15 | Start audio streaming manually if needed | If automatic audio streaming did not start in the previous step, execute the following curl command to start audio streaming manually via the external Bluetooth device.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0", "id":"3", "method":"org.rdk.Bluetooth.1.setAudioStream", "params": {"deviceID": "163411684589145", "audioStreamName": "PRIMARY"}}' http://127.0.0.1:9998/jsonrpc` | Audio should start streaming from the external Bluetooth device and should be audible|
| 16 | Close video app via Back key | Close/exit the launched video application by pressing the Back key on the remote. | The launched video application should terminate gracefully and the RDK RDK UI Home screen should be visible on the display.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
