## TestCase ID
RDKV_MANUAL_RDKUI_06
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_LANGUAGE_PERSIST_POST_REBOOT

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the RDK UI language setting persists as Spanish even after the DUT is rebooted.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully. |
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access. |
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |
| 4 | Set device language to Spanish | Set the device language to Spanish prior to this test (refer to TC_RDKUI_MANUAL_04). | The device language should be set to Spanish. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT | Verify that the text in UI is in Spanish and Reboot the DUT | The DUT should come up with the RDK UI displaying as expected. |
| 2 | Validate Spanish text on Home screen after reboot | In Home screen Validate if the text displayed are in Spanish | Text in Home screen should be displayed in Spanish. |
| 3 | Validate Spanish text on all Settings screens | Navigate to all settings screens and verify the texts are in Spanish | Text in all settings screens should be displayed in Spanish. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
