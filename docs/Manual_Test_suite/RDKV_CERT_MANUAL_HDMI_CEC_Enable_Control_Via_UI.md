## TestCase ID
RDKV_MANUAL_HDMICEC_01
## TestCase Name
RDKV_CERT_MANUAL_HDMI_CEC_Enable_Control_Via_UI

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CEC control can be enabled from the RDK UI and that the DUT can control the TV power state via HDMI CEC commands. This test confirms that the TV power state responds correctly to CEC commands when CEC is enabled, ensuring that CEC enable control and TV power management meet certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display to DUT | An HDMI display shall be connected to the DUT and the correct HDMI input source shall be selected on the display. | The HDMI display should be connected to the DUT and the correct HDMI input source should be selected.|
| 2 | Enable CEC feature on TV | Ensure the connected TV has the CEC feature enabled. | The CEC feature should be enabled on the connected TV.|
| 3 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 4 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to Advanced Settings | Navigate to Settings > Other Settings > Advanced Settings. | The Advanced Settings screen should launch with the CEC Control and Device menus in a selectable state.|
| 2 | Enable CEC Control toggle | Enable the CEC Control toggle if it is currently disabled. | The CEC Control toggle should be turned on.|
| 3 | Query HDMI CEC OTP enabled status | Execute the following curl command in the DUT serial console or SSH terminal to query the HDMI CEC OTP enabled status.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | The response should confirm OTP is enabled.|
| 4 | Enable HDMI CEC OTP via API | If OTP is not enabled, execute the following command to enable it.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.setOTPEnabled","params":{"enabled":true}}' http://127.0.0.1:9998/jsonrpc` | The HDMI CEC OTP option should be enabled successfully.|
| 5 | Send CEC standby command to TV | Send the CEC standby command to turn the TV off.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | The `sendStandbyMessage` API should return a successful response and the TV should turn off.|
| 6 | Send CEC OTP command to power on TV | Send the CEC OTP command to turn the TV on.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | The `performOTPAction` API should return a successful response and the TV should turn on.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
