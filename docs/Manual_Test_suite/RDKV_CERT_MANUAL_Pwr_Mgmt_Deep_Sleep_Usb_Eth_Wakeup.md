## TestCase ID
RDKV_MANUAL_POWER_13
## TestCase Name
RDKV_CERT_MANUAL_Pwr_Mgmt_Deep_Sleep_Usb_Eth_Wakeup

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT wakes up from DEEP SLEEP mode upon connection of a USB Ethernet dongle. This test exercises the `org.rdk.PowerManager` plugin and the RDK power-state machine (including standby, deep-sleep, and wake triggers) to validate power-mode transitions. The test confirms that the application should launch successfully and play content with proper Audio and Video output.

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
| 1 | Navigate to Energy Saver settings | From the RDK UI Home screen, navigate to Settings → Other Settings → Energy Saver and select the Deep Sleep option. | The Deep Sleep mode should be enabled with a tick mark next to the Deep Sleep option.|
| 2 | Navigate to RDK UI Home screen | Navigate to the RDK UI Home screen by pressing the Home button. | The RDK UI Home screen should launch.|
| 3 | Enter Deep Sleep mode via Power key | Press the Power button on the Bluetooth-paired remote to put the DUT into Deep Sleep mode. | The DUT UI should turn off. The serial/SSH console should not be accessible, confirming the device has entered Deep Sleep mode.|
| 4 | Connect USB Ethernet dongle to DUT | Connect a USB Ethernet dongle to the DUT. | The DUT UI should turn on and the serial/SSH console should become accessible, indicating the DUT has woken up from Deep Sleep mode.|
| 5 | Validate DUT power state via API | Validate the power state of the DUT via the serial/SSH console using the curl command.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.getPowerState","params":{}}' http://127.0.0.1:9998/jsonrpc` | The API should return a successful response with the power state indicating `ON`, confirming the DUT has woken up from Deep Sleep mode.|
| 6 | Validate internet access and content playback | Validate internet access on the DUT by launching and playing content on an application such as YouTube. | The application should launch successfully and play content with proper Audio and Video output.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
