## TestCase ID
RDKV_MANUAL_POWER_01
## TestCase Name
RDKV_CERT_MANUAL_Pwr_Mgmt_Light_Sleep_BT_Remote_Wakeup

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT enters and exits LIGHT SLEEP mode correctly when woken up via a Power key press from a Bluetooth-paired remote. This test confirms that the RDK UI is operational, internet is accessible, and A/V content playback resumes after wake-up, ensuring the LIGHT SLEEP Bluetooth remote wakeup behavior meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired with the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Ensure RDK UI is accessible | Ensure the RDK UI is visible and accessible on the DUT. | The RDK UI should be visible and accessible on the DUT.|
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to Energy Saver settings | In RDK UI, navigate to Settings → Other Settings → Energy Saver. | The Energy Saver screen should load successfully and display two options: Deep Sleep and Light Sleep.|
| 2 | Validate and select Light Sleep mode | Validate that the Light Sleep option is selected (indicated by a tick mark). If not, select Light Sleep. | Light Sleep should be the default sleep mode after a fresh flash. A tick mark should appear next to the Light Sleep option upon selection.|
| 3 | Enter sleep mode via Power key on remote | Press the Power key from the Bluetooth-paired remote control. | The DUT UI should turn off, indicating the device has entered Light Sleep mode.|
| 4 | SSH into DUT and validate power state | SSH into the DUT from the PC/laptop and validate the power state.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.getPowerState","params":{}}' http://127.0.0.1:9998/jsonrpc` | The DUT should be accessible via SSH and the API should return a successful response with the power state indicating `STANDBY`, confirming the DUT is in Light Sleep mode.|
| 5 | Wake up the dut from light_sleep | Wake up the DUT from LIGHT_SLEEP mode by pressing the Power key on the Bluetooth-paired RCU (Remote Control Unit). | The DUT should wake up from Light Sleep mode and the RDK UI should turn on.|
| 6 | Validate DUT power state via API | Validate the power state using the curl command.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.getPowerState","params":{}}' http://127.0.0.1:9998/jsonrpc` | The API should return a successful response with the power state indicating `ON`, confirming the DUT has woken up from Light Sleep mode.|
| 7 | Validate RDK UI and internet connectivity | Validate that the RDK UI is functioning as expected and internet is accessible on the DUT. Launch any internet-dependent application to confirm. | The RDK UI should be functioning as expected. Internet should be accessible on the DUT and the launched application should play content with proper Audio and Video.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
