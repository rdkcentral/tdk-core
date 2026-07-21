## TestCase ID
RDKV_MANUAL_RDKUI_17
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Boot_App_Listing

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that on every device boot, the RDK UI Recommended Apps row lists the first four available apps from the App Catalogue in alphabetical order along with a More Apps tile. This test confirms that the app listing on the home screen is correctly populated in alphabetical order after every boot, ensuring the boot-time app listing behavior meets certification requirements.
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
| 1 | Reboot DUT | Reboot the DUT | The DUT should come up with the RDK UI Home screen.|
| 2 | Observe and validate RDK UI Home screen layout | Observe the RDK UI Home screen page | In Recommended Apps row, the UI should list the first four DAC apps from the App Catalogue in the tiles in alphabetical order,<br>along with a final tile for the "More Apps" option|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
