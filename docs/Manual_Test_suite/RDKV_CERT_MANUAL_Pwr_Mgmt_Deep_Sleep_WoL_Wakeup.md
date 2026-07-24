## TestCase ID
RDKV_MANUAL_POWER_04
## TestCase Name
RDKV_CERT_MANUAL_Pwr_Mgmt_Deep_Sleep_WoL_Wakeup

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT can be set to DEEP SLEEP mode and successfully woken up using Wake-on-LAN (WoL). This test confirms that the RDK UI is operational, internet is accessible, and A/V content playback resumes after WoL wake-up, ensuring Wake-on-LAN as a DEEP SLEEP wake source meets certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired with the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Ensure RDK UI is accessible | Ensure the RDK UI is visible and accessible on the DUT. | The RDK UI should be visible and accessible on the DUT.|
| 3 | Connect Ethernet and confirm IP | Connect the Ethernet cable to the DUT and ensure a valid Ethernet IP address is available. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT.|
| 4 | Configure DUT in WoL utility | Pre-configure the DUT in the Wake-on-LAN (WoL) utility on the PC/laptop. | The DUT should be pre-configured in the Wake-on-LAN utility and ready to be woken remotely.|
| 5 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to Energy Saver settings | In RDK UI, navigate to Settings → Other Settings → Energy Saver. | The Energy Saver screen should load successfully and display two options: Deep Sleep and Light Sleep.|
| 2 | Select Deep Sleep mode | Select the Deep Sleep option. | A tick mark should appear next to the Deep Sleep option upon selection.|
| 3 | Enter sleep mode via Power key on remote | Press the Power key from the Bluetooth-paired remote control. | The DUT UI should turn off, indicating the device has entered Deep Sleep mode.|
| 4 | Attempt SSH to verify Deep Sleep state | Attempt to SSH into the DUT from the PC/laptop. | The DUT should not be accessible via SSH, confirming the device is in Deep Sleep mode.|
| 5 | Wake DUT from Deep Sleep via WoL | Wake up the DUT from Deep Sleep mode using the Wake-on-LAN utility on the PC/laptop. | The DUT should wake up from Deep Sleep mode and the RDK UI should turn on.|
| 6 | SSH into DUT and validate power state | SSH into the DUT and validate the power state using the curl command.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.getPowerState","params":{}}' http://127.0.0.1:9998/jsonrpc` | The API should return a successful response with the power state indicating `ON`, confirming the DUT has woken up from Deep Sleep mode.|
| 7 | Validate RDK UI and internet connectivity | Validate that the RDK UI is functioning as expected and internet is accessible on the DUT. Launch any internet-dependent application to confirm. | The RDK UI should be functioning as expected. Internet should be accessible on the DUT and the launched application should play content with proper Audio and Video.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
