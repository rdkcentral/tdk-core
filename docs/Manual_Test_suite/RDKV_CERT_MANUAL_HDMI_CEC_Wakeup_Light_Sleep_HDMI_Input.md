## TestCase ID
RDKV_MANUAL_HDMICEC_05
## TestCase Name
RDKV_CERT_MANUAL_HDMI_CEC_Wakeup_Light_Sleep_HDMI_Input

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT wakes up from Light Sleep state when the HDMI input source is selected on the connected CEC-enabled TV. This test exercises the `org.rdk.HdmiCec` plugin and the HDMI CEC bus to validate device-level CEC command transmission and reception. The test confirms that the DUT should wake up from Light Sleep mode and the RDK UI Home screen should be displayed on the TV.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display to DUT | An HDMI display (CEC-enabled TV) shall be connected to the DUT via HDMI and the correct HDMI input source shall be selected. | The HDMI display should be connected to the DUT and the correct HDMI input source should be selected. |
| 2 | Enable CEC feature on TV | Ensure the connected TV has the CEC feature enabled. | The CEC feature should be enabled on the connected TV. |
| 3 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 4 | Enable CEC Control on DUT | Enable the CEC Control toggle on the DUT from Settings > Other Settings > Advanced Settings. | The CEC Control toggle should be turned ON on the DUT. |
| 5 | Configure Energy Saver to Light Sleep | Configure Energy Saver to "Light Sleep" mode from Settings > Other Settings. | The Energy Saver should be set to Light Sleep mode on the DUT. |
| 6 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT | Reboot the DUT. | The DUT should boot successfully and the RDK UI Home screen should be displayed. |
| 2 | Put DUT into Light Sleep mode | Press the Power button on the remote to put the DUT into Light Sleep mode. | The DUT should transition to Light Sleep mode. |
| 3 | Query HDMI CEC OTP enabled status | Execute the following curl command in the DUT serial console or SSH terminal to query the HDMI CEC OTP enabled status.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | The response should confirm OTP is enabled: {"jsonrpc":"2.0","id":3,"result":{"enabled":true,"success":true}} |
| 4 | Enable HDMI CEC OTP via API | If OTP is not enabled, execute the following command to enable it.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.setOTPEnabled","params":{"enabled":true}}' http://127.0.0.1:9998/jsonrpc` | The HDMI CEC OTP option should be enabled successfully. |
| 5 | Select HDMI input on TV to wake DUT | On the TV, select the HDMI input source to which the DUT is connected. | The DUT should wake up from Light Sleep mode and the RDK UI Home screen should be displayed on the TV. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
