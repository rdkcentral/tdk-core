## TestCase ID
RDKV_MANUAL_POWER_06
## TestCase Name
RDKV_CERT_MANUAL_Pwr_Mgmt_Light_Sleep_Timer_Disabled

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT does not enter LIGHT SLEEP mode when the Sleep Timer is set to OFF via the RDK UI settings. This test exercises the `org.rdk.PowerManager` plugin and the RDK power-state machine (including standby, deep-sleep, and wake triggers) to validate power-mode transitions. The test confirms that the DUT UI should remain active. The DUT should be accessible via SSH and internet should be accessible.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired with the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully. |
| 2 | Ensure RDK UI is accessible | Ensure the RDK UI is visible and accessible on the DUT. | The RDK UI should be visible and accessible on the DUT. |
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access. |
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to Energy Saver settings | In RDK UI, navigate to Settings → Other Settings → Energy Saver. | The Energy Saver screen should load successfully and display two options: Deep Sleep and Light Sleep. |
| 2 | Validate and select Light Sleep mode | Validate that the Light Sleep option is selected (indicated by a tick mark). If not, select Light Sleep. | Light Sleep should be the default sleep mode after a fresh flash. A tick mark should appear next to the Light Sleep option upon selection. |
| 3 | Navigate to Sleep Timer settings | In RDK UI, navigate to Settings → Other Settings → Sleep Timer. | The Sleep Timer screen should load and display the available time frame options: OFF, 15 Minutes, 30 Minutes, 45 Minutes, and 1 Hour. |
| 4 | Select OFF sleep timer | Select the OFF radio button and navigate to the RDK UI Home screen by pressing the Home key. | The OFF option should be selected and the RDK UI Home screen should launch upon pressing the Home key. |
| 5 | Remain idle to trigger sleep mode | Remain idle on the RDK UI Home screen for more than 15 minutes without any key presses. | No changes should occur. The DUT UI should not turn off, confirming that Light Sleep mode is not triggered when the timer is set to OFF. |
| 6 | Validate DUT accessible via SSH | Validate that the DUT is accessible via SSH from the PC/laptop. | The DUT should be accessible via SSH. |
| 7 | Validate DUT power state via API | Validate the power state using the curl command.<br>Command: `curl --header "Content-Type: application/json" --request POST --data '{"jsonrpc":"2.0","id":"3","method":"org.rdk.System.1.getPowerState","params":{}}' http://127.0.0.1:9998/jsonrpc` | The curl response should be:<br>{"jsonrpc":"2.0","id":3,"result":{"powerState":"ON","success":true}} |
| 8 | Validate the rdk ui display, ssh | Validate the RDK UI display, SSH accessibility, and internet connectivity on the DUT. | The DUT UI should remain active. The DUT should be accessible via SSH and internet should be accessible. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
