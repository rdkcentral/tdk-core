## TestCase ID
RDKV_MANUAL_RDKUI_03
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_VOLUME_KEY_OVERLAY

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that volume overlay screens are displayed in the RDK UI when Volume Up, Volume Down, and Mute keys are pressed on the remote.

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
| 1 | Launch app and play content with audio | Launch any app which can play Audio and play any content | App should load as expected / without errors and audio should be heard |
| 2 | Press Volume Up key and verify overlay | Press Vol up key from remote multiple times | An overlay should come in top of the UI where we can see the Volume icon and volume level. Volume value should increase on each key press and actual volume should increase accordingly |
| 3 | Press Volume Down key and verify overlay | Press Vol down key from remote multiple times | An overlay should come in top of the UI where we can see the Volume icon and volume level. Volume value should decrease on each key press and actual volume should decrease accordingly |
| 4 | Press Mute key and verify overlay | Press mute key from remote | An overlay should come in top of the UI where we can see the muted icon. The volume should be muted in device |
| 5 | Press Mute key again to unmute | Press mute key again from remote | An overlay should come in top of the UI where we can see the unmuted icon. The volume should be unmuted in device |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
