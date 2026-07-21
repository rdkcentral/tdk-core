## TestCase ID
RDKV_MANUAL_HDMICEC_02
## TestCase Name
RDKV_CERT_MANUAL_HDMI_CEC_TV_PowerOn_Screen_Restore

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that when the TV is powered on via a CEC command, the RDK UI correctly restores the screen that was active before the TV was turned off. This test confirms that the TV powers on and the previous screen is restored with playback continuing correctly, ensuring CEC-triggered screen restoration meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display to DUT | An HDMI display shall be connected to the DUT and the correct HDMI input source shall be selected on the display. | The HDMI display should be connected to the DUT and the correct HDMI input source should be selected.|
| 2 | Enable CEC feature on TV | Ensure the connected TV has the CEC feature enabled. | The CEC feature should be enabled on the connected TV.|
| 3 | Enable CEC Control on DUT | Enable the CEC Control toggle on the DUT from Settings > Other Settings > Advanced Settings. | The CEC Control toggle should be turned ON on the DUT.|
| 4 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 5 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT.|
| 6 | Install required application | Navigate to the Recommended Apps row on the RDK UI Home screen (or the More Apps tab if the required application is not visible), select the required application tile, and press Enter/OK on the remote. Verify that a buffering/loading indicator appears on the tile. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds. | The required application should be installed successfully on the DUT.|
| 7 | Verify app listed on home screen | Verify that the installed application is listed under the My Apps section/row and on the App Info page of the RDK UI Home screen, confirming it is ready to launch. | The installed application should be visible in the My Apps section and on the App Info page, ready to launch.|
| 8 | Sign in to premium application | If the installed application is a premium application (such as YouTube or Amazon Prime), sign in with valid user credentials and verify A/V playback is functional prior to test execution. | Sign-in should succeed and A/V playback should be functional.|
| 9 | Verify app launch and content access | Verify that all installed applications launch correctly from the RDK UI, and that any purchased content and premium features are accessible prior to test execution. | All installed applications should launch correctly and content should be accessible.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Query HDMI CEC OTP enabled status | Execute the following curl command in the DUT serial console or SSH terminal to query the HDMI CEC OTP enabled status.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | The response should confirm OTP is enabled.|
| 2 | Enable HDMI CEC OTP via API | If OTP is not enabled, execute the following command to enable it.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.setOTPEnabled","params":{"enabled":true}}' http://127.0.0.1:9998/jsonrpc` | The HDMI CEC OTP option should be enabled successfully.|
| 3 | Send CEC standby command to TV | Send the CEC standby command to turn the TV off.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | The `sendStandbyMessage` API should return a successful response and the TV should turn off.|
| 4 | Send CEC OTP command to power on TV | Send the CEC OTP command to turn the TV on.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | The `performOTPAction` API should return a successful response and the TV should turn on. The RDK UI should restore to the Settings screen that was active before standby.|
| 5 | Navigate to RDK UI Home screen | Press the Home button on the remote. | The RDK UI Home screen should launch.|
| 6 | Launch YouTube app | Select the YouTube App tile from the My Apps / Recommended Apps section and press Enter/OK. | The YouTube App should launch successfully (cold launch or hot launch based on the app's previous state).|
| 7 | Select video and initiate YouTube playback | Select any video content and initiate playback on YouTube. | The selected video content A/V playback should start successfully.|
| 8 | Send CEC standby command to TV | Send the CEC standby command to turn the TV off.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | The `sendStandbyMessage` API should return a successful response and the TV should turn off.|
| 9 | Send CEC OTP command to power on TV | Send the CEC OTP command to turn the TV on.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | The `performOTPAction` API should return a successful response and the TV should turn on. The RDK UI should restore to the YouTube video itself, continuing playback with proper A/V.|
| 10 | Navigate to RDK UI Home screen | Press the Home button on the remote. | The RDK UI Home screen should launch.|
| 11 | Launch another installed app | Select any other installed application tile from the My Apps / Recommended Apps section and press Enter/OK. | The selected application should launch successfully.|
| 12 | Select or load content in app | Select any video content or load the application content (e.g., screensaver, game, or benchmark app). | The selected video content A/V playback should start, or the application content should load correctly.|
| 13 | Send CEC standby command to TV | Send the CEC standby command to turn the TV off.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | The `sendStandbyMessage` API should return a successful response and the TV should turn off.|
| 14 | Send CEC OTP command to power on TV | Send the CEC OTP command to turn the TV on.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | The `performOTPAction` API should return a successful response and the TV should turn on. The RDK UI should restore to the application itself, continuing with proper A/V.|
| 15 | Navigate to RDK UI Home screen | Press the Home button on the remote. | The RDK UI Home screen should launch.|
| 16 | Play VOD from RDK UI Home screen | Play any Video on Demand content from the RDK UI Home screen. | The video should play with proper audio and video output.|
| 17 | Send CEC standby command to TV | Send the CEC standby command to turn the TV off.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | The `sendStandbyMessage` API should return a successful response and the TV should turn off.|
| 18 | Send CEC OTP command to power on TV | Send the CEC OTP command to turn the TV on.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | The `performOTPAction` API should return a successful response and the TV should turn on. The RDK UI should restore to the video itself, continuing playback with proper A/V.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
