## TestCase ID
RDKV_MANUAL_RDKUI_04
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Language_Change

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the RDK UI language can be changed from English to Spanish via the Settings without any display issues. This test confirms that all text across the Settings screens changes to Spanish and button labels remain properly sized without overflow, ensuring the language change behavior meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to Language settings | Navigate to Settings /Other Settings / Language | Language screen should launch with English and Spanish languages listed|
| 2 | Select Spanish language | Select Spanish Language | Spanish language should be set and a loading icon should come. After that, the texts in screen should change to Spanish(Mainly the Menu text need to be changed)|
| 3 | Validate language change on Home screen | Navigate to Home screen and Validate if the language has taken effect in Home screen | Text in Home screen should be changed to Spanish|
| 4 | Validate Spanish text on all Settings screens | Navigate to all settings screen and verify the texts are changed to Spanish and if any texts are overlapping on buttons | Text in all settings screen should be changed to Spanish.<br>The text on buttons should fit on buttons and should not overlap from button|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
