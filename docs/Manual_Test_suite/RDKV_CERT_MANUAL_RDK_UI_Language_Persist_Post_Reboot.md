## TestCase ID
RDKV_MANUAL_RDKUI_06
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Language_Persist_Post_Reboot

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the RDK UI language setting is retained as Spanish after the DUT is rebooted. This test confirms that all Settings screens continue to display text in Spanish following the reboot, ensuring language setting persistence across reboots meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|
| 4 | Navigate to Language settings | Navigate to Settings > Other Settings > Language to access the language selection screen. | The Language settings screen should launch, displaying both English and Spanish language options.|
| 5 | Select Spanish language | Select Spanish from the language list. | Spanish should be set as the device language; a loading indicator should appear briefly, and all on-screen text should change to Spanish.|
| 6 | Validate language change on Home screen | Navigate to the Home screen and validate that the language change has taken effect. | All text on the Home screen should be displayed in Spanish.|
| 7 | Validate Spanish text on all Settings screens | Navigate through all Settings screens and verify that all text is displayed in Spanish, with no button text overlapping or overflowing button boundaries. | All text on all Settings screens should be displayed in Spanish; button labels should fit within button boundaries without overflow.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT | Verify that the text in UI is in Spanish and Reboot the DUT | The DUT should come up with the RDK UI displaying as expected.|
| 2 | Validate Spanish text on Home screen after reboot | In Home screen Validate if the text displayed are in Spanish | Text in Home screen should be displayed in Spanish.|
| 3 | Validate Spanish text on all Settings screens | Navigate to all settings screens and verify the texts are in Spanish | Text in all settings screens should be displayed in Spanish.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
