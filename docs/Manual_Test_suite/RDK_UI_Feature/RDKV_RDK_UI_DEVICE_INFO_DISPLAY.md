## TestCase ID
RDKV_MANUAL_RDKUI_11
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_DEVICE_INFO_DISPLAY

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that device information is displayed correctly on the Device Info screen in the RDK UI Settings.

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
| 1 | Navigate to Device settings screen | Navigate to Settings / Other Settings / Advanced Settings / Device screen | Screen should launch and it should have Info button |
| 2 | Open Device Info screen | Press on Info button | Info screen should launch.<br>It should have the details of the following things populated.<br>Serial Number<br>Supported DRM & Key System<br>Firmware Version<br>App Info |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
