## TestCase ID
RDKV_MANUAL_RDKUI_15
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Voice_Remote_Details

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the Voice Remote Control details are accurately populated on the Voice Remote Control screen. This test exercises the RDK UI home screen, settings menus, and DAC App Manager navigation via Bluetooth remote key-press events to validate the targeted UI behaviour. The test confirms that screen should load with MacAddress, RCU Name,Connection Status, Battery Percent and Software Version of the paired Voice Remote. If pairing is not there, then all of these values will be shown as N/A.

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
| 1 | Navigate to Voice Remote Control screen | Launch Settings/ Voice Remote Control Screen | screen should load with <br>MacAddress, RCU Name,Connection Status, Battery Percent and Software Version of the paired Voice Remote. If pairing is not there, then all of these values will be shown as N/A |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
