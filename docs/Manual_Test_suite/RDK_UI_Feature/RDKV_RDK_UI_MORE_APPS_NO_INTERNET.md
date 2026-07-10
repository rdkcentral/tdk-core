## TestCase ID
RDKV_MANUAL_RDKUI_21
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_MORE_APPS_NO_INTERNET

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the RDK UI behavior when the More Apps button is pressed and the DUT fails to connect to the App Catalogue server due to a network issue.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Ensure DUT has no network connection | Ensure the DUT is NOT connected to any network prior to this test. | The DUT should have no active network connection. |
| 2 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully. |
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT | Reboot the DUT | The RDK UI should launch with only one tile  -"More Apps" - in Recommended Apps Row. |
| 2 | Open More Apps page | Click on the More Apps Button | Error message should popup giving the reason for error as network issue |
| 3 | Click on the cancel button on | Click on the cancel button on top left of the overlay | Error message should close and return to previous screen |
| 4 | Open More Apps page | Click on the More Apps Button | Error message should popup giving the reason for error as network issue |
| 5 | Click on the back button on | Click on the back button on the remote | Error message should close and return to previous screen |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
