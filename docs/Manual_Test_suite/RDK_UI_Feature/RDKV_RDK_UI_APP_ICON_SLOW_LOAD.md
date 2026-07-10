## TestCase ID
RDKV_MANUAL_RDKUI_19
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_APP_ICON_SLOW_LOAD

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that when app icons take time to load due to network latency, the RDK UI displays a loading/buffering indicator until the Recommended Apps row data fully loads.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully. |
| 2 | Connect DUT to slow network | Connect the DUT to a slow network to simulate network latency conditions. | The DUT should be connected to a slow network to simulate latency. |
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT | Reboot the DUT | The DUT should come up with the RDK UI Home screen. |
| 2 | Verify loading indicator on Recommended Apps | Validate whether a a loading icon shows over Recommended Apps until data fully loads | The UI should display a<br>loading/buffering indicator (As it is connected to slow network) until the Recommended Apps row data fully loads |
| 3 | Navigate to More Apps page | Click on More Apps button | A dedicated page should open which lists all applications available in DAC App Catalogue. The UI should display a<br>loading/buffering indicator (As it is connected to slow network) until the apps row data fully loads |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
