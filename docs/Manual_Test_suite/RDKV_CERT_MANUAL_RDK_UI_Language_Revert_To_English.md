## TestCase ID
RDKV_MANUAL_RDKUI_07
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Language_Revert_To_English

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the RDK UI language can be changed back to English from Spanish via the Settings. This test confirms that all text across Settings screens is correctly restored to English after the language change, ensuring the language revert behavior meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|
| 4 | Set device language to Spanish | Set the device language to Spanish prior to this test (refer to TC_RDKUI_MANUAL_04). | The device language should be set to Spanish.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to Language settings | Navigate to Settings /Other Settings / Language | Language screen should launch with English and Spanish languages listed|
| 2 | Select English language | Select English Language | English language should be set and a loading icon should come. After that, the texts in screen should change to English|
| 3 | Validate language change on Home screen | Navigate to Home screen and Validate if the language has taken effect in Home screen | Text in Home screen should be changed to English|
| 4 | Validate English text on all Settings screens | Navigate to all settings screen and verify the texts are changed to English | Text in all settings screen should be changed to English|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
