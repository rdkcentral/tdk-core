## TestCase ID
RDKV_MANUAL_BLUETOOTH_07
## TestCase Name
RDKV_CERT_MANUAL_BTRemote_Volume_Press

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the Volume Up, Volume Down, and Mute key presses on the paired Bluetooth remote function correctly during A/V content playback. This test exercises the RDK Bluetooth pairing stack, the remote-control key-mapping service, and the RDK UI to validate remote-control button behaviour. The test confirms that the unmute icon should be displayed on screen and the audio should be restored to the previous volume level.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Connect Ethernet cable  | Connect the DUT to an active network via Ethernet prior to the test. | The Ethernet cable should be connected and a valid IP address should be assigned to the DUT. |
| 2 |  Connect HDMI display  | Connect the HDMI display to the DUT and select the correct HDMI input source on the display. | The HDMI display should be connected and the correct HDMI input source should be selected on the display. |
| 3 |  Ensure bluetooth remote already paired  | Ensure the Bluetooth remote is successfully paired with the DUT prior to the test. | The Bluetooth remote should be paired and functional on the DUT. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 |  Open A/V application  | On the RDK UI Home screen, use the remote navigation keys to navigate to and open an A/V application such as YouTube or Amazon Prime Video. | The selected application should open successfully. |
| 2 |  Play video content with audio  | Play any video content from the application that includes audio. | The video should play with audio output. |
| 3 |  Press volume up key  | Press the Volume Up key on the remote. | The volume bar should be displayed on screen and the audio volume should increase. |
| 4 |  Press volume down key  | Press the Volume Down key on the remote. | The volume bar should be displayed on screen and the audio volume should decrease. |
| 5 |  Press mute key  | Press the Mute key on the remote. | The mute icon should be displayed on screen and the audio should be muted. |
| 6 |  Press mute key again to unmute  | Press the Mute key again on the remote. | The unmute icon should be displayed on screen and the audio should be restored to the previous volume level. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
