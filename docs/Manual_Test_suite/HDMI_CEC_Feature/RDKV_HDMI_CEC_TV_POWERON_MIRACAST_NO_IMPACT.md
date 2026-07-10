## TestCase ID
RDKV_MANUAL_HDMICEC_04
## TestCase Name
RDKV_CERT_MANUAL_HDMI_CEC_TV_POWERON_MIRACAST_NO_IMPACT

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that powering on the TV via a CEC command does not interrupt or terminate an active Miracast screen casting session.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display to DUT | An HDMI display (CEC-enabled TV) shall be connected to the DUT via HDMI and the correct HDMI input source shall be selected. | The HDMI display should be connected to the DUT and the correct HDMI input source should be selected. |
| 2 | Enable CEC feature on TV | Ensure the connected TV has the CEC feature enabled. | The CEC feature should be enabled on the connected TV. |
| 3 | Enable CEC Control on DUT | Enable the CEC Control toggle on the DUT from Settings > Other Settings > Advanced Settings. | The CEC Control toggle should be turned ON on the DUT. |
| 4 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 5 | Enable Miracast on DUT | Enable Miracast on the DUT. | Miracast should be enabled and functional on the DUT. |
| 6 | Enable Wi-Fi on both devices | Ensure Wi-Fi is turned on on both the smartphone and the DUT. | Wi-Fi should be active on both the smartphone and the DUT. |
| 7 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Enable Miracast on mobile device | Enable Miracast on the mobile device. | Miracast should be enabled on the mobile device. |
| 2 | Search for Miracast devices from mobile | Search for available Miracast-enabled devices from the mobile device. | The DUT (with Miracast enabled) should appear in the list of discoverable devices on the mobile device. |
| 3 | Select DUT from discovered devices list | Select the DUT from the discovered devices list on the mobile device. | The DUT should be selected for Miracast connection. |
| 4 | Accept Miracast connection request | Accept the Miracast connection request on both the mobile device and the DUT. | The mobile device should connect to the DUT successfully via Miracast. |
| 5 | Initiate screen mirroring from mobile | Initiate screen mirroring from the mobile device. | The mobile device screen should be mirrored and visible on the DUT via the connected TV/display. |
| 6 | Query HDMI CEC OTP enabled status | Execute the following curl command in the DUT serial console or SSH terminal to query the HDMI CEC OTP enabled status.<br>Command: curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc | The response should confirm OTP is enabled: {"jsonrpc":"2.0","id":3,"result":{"enabled":true,"success":true}} |
| 7 | Enable HDMI CEC OTP via API | If OTP is not enabled, execute the following command to enable it.<br>Command: curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.setOTPEnabled","params":{"enabled":true}}' http://127.0.0.1:9998/jsonrpc | The HDMI CEC OTP option should be enabled successfully. |
| 8 | Send CEC standby command to TV | Send the CEC standby command to turn the TV off.<br>Command: curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc | The response should be {"jsonrpc":"2.0","id":3,"result":{"success":true}} and the TV should turn off. |
| 9 | Send CEC OTP command to power on TV | Send the CEC OTP command to turn the TV on.<br>Command: curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.performOTPAction"}' http://127.0.0.1:9998/jsonrpc | The response should be {"jsonrpc":"2.0","id":3,"result":{"success":true}} and the TV should turn on. The RDK UI should restore to the Miracast casting screen, confirming the casting session was not interrupted. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
