## TestCase ID
RDKV_MANUAL_RDKUI_05
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Language_Msg_Translation

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that error messages and confirmation dialogs displayed in the RDK UI are correctly translated to Spanish after the device language is set to Spanish. This test confirms that all messages appear in Spanish and can be dismissed correctly, ensuring UI message translation accuracy meets certification requirements.
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
| 1 | Attempt Wi-Fi connection with wrong password | Launch WiFi screen from Settings and try to connect to an SSID with wrong password | Error message should be displayed, which should be displayed in Spanish.|
| 2 | Navigate to Advanced Settings | Go to Settings/Other Settings/Advanced Settings | Screen should load where we can see option to reboot|
| 3 | Click Reboot option in Settings | Click on Reboot option | Confirmation message should be displayed which should be displayed in Spanish.|
| 4 | Click Cancel to dismiss dialog | Click on Cancel button | Confirmation message should close|
| 5 | Click Factory Reset option in Settings | Click on Factory Reset option | Confirmation message should be displayed which should be displayed in Spanish.|
| 6 | Click Cancel to dismiss dialog | Click on Cancel button | Confirmation message should close|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
