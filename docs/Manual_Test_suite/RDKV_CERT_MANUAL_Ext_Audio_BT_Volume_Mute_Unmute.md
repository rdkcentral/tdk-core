## TestCase ID
RDKV_MANUAL_EXT_AUDIO_06
## TestCase Name
RDKV_CERT_MANUAL_Ext_Audio_BT_Volume_Mute_Unmute

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that audio streaming can be successfully muted and unmuted on an external Bluetooth device during active playback on the DUT. This test confirms that the mute and unmute states are correctly applied and reflected after each operation, ensuring Bluetooth audio mute control meets certification requirements.

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
| 1 | Execute TC02 steps as prerequisite | Execute all steps from TC_EXTERNALAUDIO_MANUAL_02 (Start streaming from External BT device) as a prerequisite for this test. | Refer to the expected results of TC_EXTERNALAUDIO_MANUAL_02 (Start streaming from External BT device).|
| 2 | Mute audio stream via BT API | Execute the following curl command to mute the audio stream via the external Bluetooth device (set the mute parameter to 1 to mute).<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 42, "method": "org.rdk.Bluetooth.setDeviceVolumeMuteInfo", "params": {"deviceID": "163411684589145", "deviceType": "WEARABLE HEADSET", "volume": "150", "mute": "1"}}' http://127.0.0.1:9998/jsonrpc` | Audio streaming should be muted and no audio should be heard from the external Bluetooth device|
| 3 | Retrieve volume and mute status | Execute the following curl command to retrieve the current volume and mute status of the external Bluetooth device.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 42, "method": "org.rdk.Bluetooth.getDeviceVolumeMuteInfo", "params": {"deviceID": "163411684589145", "deviceType": "WEARABLE HEADSET"}}' http://127.0.0.1:9998/jsonrpc` | Mute value should return true|
| 4 | Unmute audio stream via BT API | Execute the following curl command to unmute the audio stream via the external Bluetooth device (set the mute parameter to 0 to unmute).<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 42, "method": "org.rdk.Bluetooth.setDeviceVolumeMuteInfo", "params": {"deviceID": "163411684589145", "deviceType": "WEARABLE HEADSET", "volume": "150", "mute": "0"}}' http://127.0.0.1:9998/jsonrpc` | Audio streaming should resume and audio should be heard from the external Bluetooth device|
| 5 | Retrieve volume and mute status | Execute the following curl command to retrieve the current volume and mute status of the external Bluetooth device.<br>`curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc": "2.0", "id": 42, "method": "org.rdk.Bluetooth.getDeviceVolumeMuteInfo", "params": {"deviceID": "163411684589145", "deviceType": "WEARABLE HEADSET"}}' http://127.0.0.1:9998/jsonrpc` | Mute value should return false|
| 6 | Validate audio streaming is functional | Validate audio streaming from the external Bluetooth device. | Audio streaming from the external Bluetooth device should be functioning as expected and audio should be audible.|
| 7 | Close video app via Back key | Close/exit the launched video application by pressing the Back key on the remote. | The launched video application should terminate gracefully and the RDK RDK UI Home screen should be visible on the display.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
