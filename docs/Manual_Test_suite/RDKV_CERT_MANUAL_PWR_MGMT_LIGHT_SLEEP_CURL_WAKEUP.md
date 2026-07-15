## TestCase ID
RDKV_MANUAL_POWER_02
## TestCase Name
RDKV_CERT_MANUAL_Pwr_Mgmt_Light_Sleep_Curl_Wakeup

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT can be set to LIGHT SLEEP mode and then woken up using a curl command from the SSH/serial console. This test exercises the `org.rdk.PowerManager` plugin and the RDK power-state machine (including standby, deep-sleep, and wake triggers) to validate power-mode transitions. The test confirms that the RDK UI should be functioning as expected. Internet should be accessible on the DUT and the launched application should play content with proper Audio and Video.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Ensure RDK UI is accessible | Ensure the RDK UI is visible and accessible on the DUT. | The RDK UI should be visible and accessible on the DUT. |
| 2 | Ensure SSH access | Ensure SSH access to the DUT is available from the PC/laptop. | SSH access should be available and functional on the DUT. |
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access. |
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to Energy Saver settings | In RDK UI, navigate to Settings → Other Settings → Energy Saver. | The Energy Saver screen should load successfully and display two options: Deep Sleep and Light Sleep. |
| 2 | Validate and select Light Sleep mode | Validate that the Light Sleep option is selected (indicated by a tick mark). If not, select Light Sleep. | Light Sleep should be the default sleep mode after a fresh flash. A tick mark should appear next to the Light Sleep option upon selection. |
| 3 | Set DUT to LIGHT_SLEEP mode via API | Set the DUT to LIGHT_SLEEP mode via the following curl command from the SSH console.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.setPowerState","params":{"powerState":"LIGHT_SLEEP","standbyReason":"For Testing"}}' http://127.0.0.1:9998/jsonrpc` | The curl response should be:<br>{"jsonrpc":"2.0","id":3,"result":{"success":true}}<br>The DUT UI should turn off. |
| 4 | SSH into DUT and validate power state | SSH into the DUT from the PC/laptop and validate the power state.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.getPowerState","params":{}}' http://127.0.0.1:9998/jsonrpc` | The DUT should be accessible via SSH and the curl response should be:<br>{"jsonrpc":"2.0","id":3,"result":{"powerState":"STANDBY","success":true}} |
| 5 | Wake DUT to ON state via API | Wake up the DUT from LIGHT_SLEEP mode using the following curl command.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.setPowerState","params":{"powerState":"ON","standbyReason":"For Testing"}}' http://127.0.0.1:9998/jsonrpc` | The curl response should be:<br>{"jsonrpc":"2.0","id":3,"result":{"success":true}}<br>The DUT should wake up from Light Sleep with the RDK UI turning on. |
| 6 | Validate DUT power state via API | Validate the power state using the curl command.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.getPowerState","params":{}}' http://127.0.0.1:9998/jsonrpc` | The curl response should be:<br>{"jsonrpc":"2.0","id":3,"result":{"powerState":"ON","success":true}} |
| 7 | Validate RDK UI and internet connectivity | Validate that the RDK UI is functioning as expected and internet is accessible on the DUT. Launch any internet-dependent application to confirm. | The RDK UI should be functioning as expected. Internet should be accessible on the DUT and the launched application should play content with proper Audio and Video. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
