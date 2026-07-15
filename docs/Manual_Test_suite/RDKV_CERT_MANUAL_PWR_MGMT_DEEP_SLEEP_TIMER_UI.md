## TestCase ID
RDKV_MANUAL_POWER_07
## TestCase Name
RDKV_CERT_MANUAL_Pwr_Mgmt_Deep_Sleep_Timer_UI

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT enters DEEP SLEEP mode automatically after the inactivity timer configured via the RDK UI settings expires. This test exercises the `org.rdk.PowerManager` plugin and the RDK power-state machine (including standby, deep-sleep, and wake triggers) to validate power-mode transitions. The test confirms that the DUT UI should come up. The DUT should be accessible via SSH and internet should be accessible.

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
| 2 | Select Deep Sleep mode | Select the Deep Sleep option. | A tick mark should appear next to the Deep Sleep option upon selection. |
| 3 | Navigate to Sleep Timer settings | In RDK UI, navigate to Settings → Other Settings → Sleep Timer. | The Sleep Timer screen should load and display the available time frame options: OFF, 15 Minutes, 1 Hour, 1.5 Hours, 2 Hours, and 3 Hours. |
| 4 | Select 15 Minutes sleep timer | Select the 15 Minutes radio button and navigate to the RDK UI Home screen by pressing the Home key. | The 15 Minutes option should be selected and the RDK UI Home screen should launch upon pressing the Home key. |
| 5 | Remain idle to trigger sleep mode | Remain idle on the RDK UI Home screen for more than 15 minutes without any key presses. | No changes should occur for the first 15 minutes. After 15 minutes of inactivity, the DUT UI should turn off, indicating the device has entered Deep Sleep mode. |
| 6 | Attempt SSH to verify Deep Sleep state | Attempt to SSH into the DUT from the PC/laptop. | The DUT should not be accessible via SSH, confirming the device is in Deep Sleep mode. |
| 7 | Wake DUT from Deep Sleep and verify | Wake up the DUT from Deep Sleep mode using the Power key press on the Bluetooth-paired remote and validate the RDK UI, SSH accessibility, and internet connectivity. | The DUT UI should come up. The DUT should be accessible via SSH and internet should be accessible. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
