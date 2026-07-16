## TestCase ID
RDKV_MANUAL_RDKUI_01
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Home_Screen_Boot_Load

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the RDK UI loads successfully on the DUT after a reboot, with no ill effects such as a black screen or display anomalies. This test exercises the RDK UI home screen, settings menus, and DAC App Manager navigation via Bluetooth remote key-press events to validate the targeted UI behaviour. The test confirms that in Home screen and different settings screens, UI should be proper. Texts should be readable and no overlapping should be there with other screens.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully. |
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access. |
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT | Reboot the DUT | The DUT should come up with the RDK UI displaying as expected. |
| 2 | Validate RDK UI Home screen and Settings screens | Check in home screen and different Settings screens whether the UI is showing as expected / without errors | In Home screen and different settings screens, UI should be proper. Texts should be readable and no overlapping should be there with other screens |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
