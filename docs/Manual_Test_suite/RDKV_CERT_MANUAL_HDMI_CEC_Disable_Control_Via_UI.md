## TestCase ID
RDKV_MANUAL_HDMICEC_06
## TestCase Name
RDKV_CERT_MANUAL_HDMI_CEC_Disable_Control_Via_UI

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CEC control can be disabled from the RDK UI and that all CEC API commands are rejected when CEC is in the disabled state on the DUT. This test confirms that the API correctly rejects CEC commands and the TV does not respond when CEC is disabled, ensuring that CEC disable control meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect HDMI display to DUT | An HDMI display (CEC-enabled TV) shall be connected to the DUT via HDMI and the correct HDMI input source shall be selected. | The HDMI display should be connected to the DUT and the correct HDMI input source should be selected.|
| 2 | Enable CEC feature on TV | Ensure the connected TV has the CEC feature enabled. | The CEC feature should be enabled on the connected TV.|
| 3 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 4 | Ensure SSH or console access | Ensure that SSH access or serial console access to the DUT is available from the PC/laptop. | SSH or serial console access should be available and functional on the DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Disable CEC Control toggle via UI | Navigate to Settings > Other Settings > Advanced Settings and disable the CEC Control toggle. | The Settings screen should load and the CEC Control toggle should be turned off successfully.|
| 2 | Query HDMI CEC OTP enabled status | Execute the following curl command to query the HDMI CEC OTP enabled status.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | Since CEC is disabled, the API should return an error.|
| 3 | Enable HDMI CEC OTP via API | Attempt to enable the HDMI CEC OTP option via the API.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.setOTPEnabled","params":{"enabled":true}}' http://127.0.0.1:9998/jsonrpc` | The API should reject the request since CEC is disabled.|
| 4 | Send CEC standby command to TV | Attempt to send the CEC standby command to turn the TV off.<br>Command: `curl -d '{"jsonrpc":"2.0","id":"3","method":"org.rdk.HdmiCecSource.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | The API should reject the command since CEC is disabled. The TV should not turn off.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
