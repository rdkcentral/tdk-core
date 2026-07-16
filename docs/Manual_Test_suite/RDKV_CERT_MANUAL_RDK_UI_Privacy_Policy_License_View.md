## TestCase ID
RDKV_MANUAL_RDKUI_10
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Privacy_Policy_License_View

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the Privacy Policy and License information are accessible and displayed correctly via the RDK UI Settings. This test exercises the RDK UI home screen, settings menus, and DAC App Manager navigation via Bluetooth remote key-press events to validate the targeted UI behaviour. The test confirms that policy screen should launch and the information should be displayed on screen. The screen should be scrollable to see all the information in screen.

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
| 1 | Navigate to Privacy Settings screen | Launch Settings / Other Settings / Privacy screen | Navigation should be proper and UI should display the available options[Local Device Discovery, USB Media Devices, Audio Input, Clear Cookies and App data, Privacy Policy and License].|
| 2 | Open Privacy Policy and License screen | Click on Privacy policy and License | Policy screen should launch and the information should be displayed on screen. The screen should be scrollable to see all the information in screen|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
