## TestCase ID
RDKV_MANUAL_POWER_08
## TestCase Name
RDKV_CERT_MANUAL_Pwr_Mgmt_Deep_Sleep_Timer_Disabled

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT does not enter DEEP SLEEP mode when the Sleep Timer is disabled via the RDK UI settings. This test confirms that the DUT UI remains active and internet remains accessible after the configured interval, ensuring the DEEP SLEEP timer-disabled behavior meets certification requirements.

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
| 2 | Select Deep Sleep mode | Select the Deep Sleep option. | A tick mark should appear next to the Deep Sleep option upon selection.|
| 3 | Navigate to Sleep Timer settings | In RDK UI, navigate to Settings → Other Settings → Sleep Timer. | The Sleep Timer screen should load and display the available time frame options: OFF, 15 Minutes, 30 Minutes, 45 Minutes, and 1 Hour.|
| 4 | Select OFF sleep timer | Select the OFF radio button and navigate to the RDK UI Home screen by pressing the Home key. | The OFF option should be selected and the RDK UI Home screen should launch upon pressing the Home key.|
| 5 | Remain idle to trigger sleep mode | Remain idle on the RDK UI Home screen for more than 15 minutes without any key presses. | No changes should occur. The DUT UI should not turn off, confirming that Deep Sleep mode is not triggered when the timer is set to OFF.|
| 6 | Validate DUT accessible via SSH | Validate that the DUT is accessible via SSH from the PC/laptop. | The DUT should be accessible via SSH.|
| 7 | Validate DUT power state via API | Validate the power state using the curl command.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.getPowerState","params":{}}' http://127.0.0.1:9998/jsonrpc` | The API should return a successful response with the power state indicating `ON`, confirming the DUT remains active and has not entered Deep Sleep mode.|
| 8 | Validate the rdk ui display, ssh | Validate the RDK UI display, SSH accessibility, and internet connectivity on the DUT. | The DUT UI should remain active. The DUT should be accessible via SSH and internet should be accessible.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
