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
To validate that error messages and confirmation messages are translated to Spanish after the device language is set to Spanish. This test exercises the RDK UI home screen, settings menus, and DAC App Manager navigation via Bluetooth remote key-press events to validate the targeted UI behaviour. The test confirms that confirmation message should close.

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
| 1 | Attempt Wi-Fi connection with wrong password | Launch Wifi screen from Settings and try to connect to an SSID with wrong password | Error message should be displayed, which should be displayed in Spanish. |
| 2 | Navigate to Advanced Settings | Go to Settings/Other Settings/Advanced Settings | Screen should load where we can see option to reboot |
| 3 | Click Reboot option in Settings | Click on Reboot option | Confirmation message should be displayed which should be displayed in Spanish. |
| 4 | Click Cancel to dismiss dialog | Click on Cancel button | Confirmation message should close |
| 5 | Click Factory Reset option in Settings | Click on Factory Reset option | Confirmation message should be displayed which should be displayed in Spanish. |
| 6 | Click Cancel to dismiss dialog | Click on Cancel button | Confirmation message should close |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
