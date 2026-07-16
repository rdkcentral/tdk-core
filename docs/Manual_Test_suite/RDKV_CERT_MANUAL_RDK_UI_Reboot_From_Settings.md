## TestCase ID
RDKV_MANUAL_RDKUI_13
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Reboot_From_Settings

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DUT can be rebooted from the RDK UI Settings and that the reboot confirmation dialog functions correctly. This test exercises the RDK UI home screen, settings menus, and DAC App Manager navigation via Bluetooth remote key-press events to validate the targeted UI behaviour. The test confirms that a loading indicator should appear briefly and the DUT should reboot and come up with the RDK splash screen followed by the RDK UI Home screen.

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
| 1 | Navigate to Device settings screen | Navigate to Settings / Other Settings / Advanced Settings / Device screen | Screen should launch and it should have Reboot button|
| 2 | Click Reboot button | Click on Reboot | A reboot confirmation dialog should appear.|
| 3 | Click Cancel in confirmation dialog | Click on Cancel | The confirmation dialog should close and the screen should return to Settings → Other Settings → Advanced Settings → Device.|
| 4 | Click Reboot button | Click on Reboot | A reboot confirmation dialog should appear.|
| 5 | Click Confirm to proceed with reboot | Click on Confirm | A loading indicator should appear briefly and the DUT should reboot and come up with the RDK splash screen followed by the RDK UI Home screen.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
