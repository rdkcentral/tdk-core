## TestCase ID
RDKV_MANUAL_RDKUI_08
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Resolution_Change

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that resolution changes applied via the RDK UI Settings correctly affect the display clarity without altering the screen size. This test confirms that the display reflects the selected resolution change appropriately, ensuring resolution configuration via the RDK UI meets certification requirements.
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
| 1 | Navigate to Video settings | Navigate to Settings /Video | Resolution Menu will be there for which current resolution in The DUT should be displayed|
| 2 | Open Resolution selection screen | Click on Resolution | A resolution selection screen should launch listing the common resolutions supported by both the source (DUT) and sink (display).|
| 3 | Set first listed resolution | Try to set the first resolution listed in the screen | Resolution should be able to set successfully. The set resolution value should be in ticked state|
| 4 | Press Back to return to Video settings | Press Back button so that UI navigates to Settings / Video screen | The newly set resolution value should be displayed in screen|
| 5 | Validate display clarity for resolution | Validate if clarity has reflected in the UI. | For lower resolutions, clarity should be less. If resolution is higher, clarity will be increased.<br>The screen size should not be affected in any cases|
| 6 | Repeat steps for all other resolutions | Execute steps 1 to 5 for other resolutions too. | Similar Results of steps 1 to 5|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
