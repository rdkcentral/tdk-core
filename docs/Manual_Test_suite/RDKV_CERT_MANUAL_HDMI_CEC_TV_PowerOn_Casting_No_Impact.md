## TestCase ID
RDKV_MANUAL_HDMICEC_03
## TestCase Name
RDKV_CERT_MANUAL_HDMI_CEC_TV_PowerOn_Casting_No_Impact

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that powering on the TV via a CEC command does not interrupt or terminate an active YouTube casting session on the DUT. This test exercises the `org.rdk.HdmiCec` plugin and the HDMI CEC bus to validate device-level CEC command transmission and reception. The test confirms that the response should be {"jsonrpc":"2.0","id":3,"result":{"success":true}} and the TV should turn on. The RDK UI should restore to the YouTube video. The casting session should not be lost and video should continue playing with proper A/V.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display to DUT | An HDMI display (CEC-enabled TV) shall be connected to the DUT via HDMI and the correct HDMI input source shall be selected. | The HDMI display should be connected to the DUT and the correct HDMI input source should be selected. |
| 2 | Enable CEC feature on TV | Ensure the connected TV has the CEC feature enabled. | The CEC feature should be enabled on the connected TV. |
| 3 | Enable CEC Control on DUT | Enable the CEC Control toggle on the DUT from Settings > Other Settings > Advanced Settings. | The CEC Control toggle should be turned ON on the DUT. |
| 4 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 5 | Enable XDial (Local Device Discovery) | Enable XDial on the DUT from Settings > Other Settings > Privacy > Local Device Discovery. | XDial should be enabled and the DUT should be discoverable on the local network. |
| 6 | Ensure internet access and same network | Ensure internet access is available on both the DUT and the smartphone, and both are connected to the same network. | Internet access should be available on both devices and they should be on the same network. |
| 7 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT. |
| 8 | Install required application | Navigate to the Recommended Apps row on the RDK UI Home screen (or the More Apps tab if the required application is not visible), select the required application tile, and press Enter/OK on the remote. Verify that a buffering/loading indicator appears on the tile. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds. | The required application should be installed successfully on the DUT. |
| 9 | Verify app listed on home screen | Verify that the installed application is listed under the My Apps section/row and on the App Info page of the RDK UI Home screen, confirming it is ready to launch. | The installed application should be visible in the My Apps section and on the App Info page, ready to launch. |
| 10 | Sign in to premium application | If the installed application is a premium application (such as YouTube or Amazon Prime), sign in with valid user credentials and verify A/V playback is functional prior to test execution. | Sign-in should succeed and A/V playback should be functional. |
| 11 | Verify app launch and content access | Verify that all installed applications launch correctly from the RDK UI, and that any purchased content and premium features are accessible prior to test execution. | All installed applications should launch correctly and content should be accessible. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT | Reboot the DUT. | The DUT should boot successfully and the RDK UI Home screen should be displayed. |
| 2 | Verify YouTube app is available | Verify that the YouTube App is installed and available in the My Apps / Recommended Apps section. If not installed, follow the instructions in Preconditions 8–11. | The YouTube App tile should be available in the My Apps / Recommended Apps section. |
| 3 | Cast YouTube from smartphone to DUT | Cast YouTube from the smartphone to the DUT and initiate video playback. | The YouTube application should launch on the DUT and begin playing the video. |
| 4 | Query HDMI CEC OTP enabled status | Execute the following curl command in the DUT serial console or SSH terminal to query the HDMI CEC OTP enabled status.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | The response should confirm OTP is enabled: {"jsonrpc":"2.0","id":3,"result":{"enabled":true,"success":true}} |
| 5 | Enable HDMI CEC OTP via API | If OTP is not enabled, execute the following command to enable it.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.setOTPEnabled","params":{"enabled":true}}' http://127.0.0.1:9998/jsonrpc` | The HDMI CEC OTP option should be enabled successfully. |
| 6 | Send CEC standby command to TV | Send the CEC standby command to turn the TV off.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | The response should be {"jsonrpc":"2.0","id":3,"result":{"success":true}} and the TV should turn off. |
| 7 | Send CEC OTP command to power on TV | Send the CEC OTP command to turn the TV on.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | The response should be {"jsonrpc":"2.0","id":3,"result":{"success":true}} and the TV should turn on. The RDK UI should restore to the YouTube video. The casting session should not be lost and video should continue playing with proper A/V. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
