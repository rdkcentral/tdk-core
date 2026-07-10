## TestCase ID
RDKV_MANUAL_RDKUI_12
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_TIME_CHANGE_SETTINGS

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the displayed time on the RDK UI can be updated by changing the timezone via Settings.

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
| 1 | Navigate to Device settings screen | Navigate to Settings / Other Settings / Advanced Settings / Device screen | Screen should launch and it should have Timezone button |
| 2 | Open Timezone selection | Click on Timezone | It should show the current Timezone in ticked state |
| 3 | Select new timezone and verify time update | Select another Timezone | Selected Timezone should be set and a tick mark should be seen against it. The time on UI should be updated according to the newly selected Time zone |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
