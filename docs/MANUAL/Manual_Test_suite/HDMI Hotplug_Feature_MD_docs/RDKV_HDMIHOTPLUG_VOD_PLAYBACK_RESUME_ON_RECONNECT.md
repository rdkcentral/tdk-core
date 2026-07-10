## TestCase ID
RDKV_MANUAL_HDMIHOTPLUG_03
## TestCase Name
RDKV_CERT_MANUAL_HDMIHOTPLUG_VOD_PLAYBACK_RESUME_ON_RECONNECT

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that On Demand video playback resumes correctly on the DUT after an HDMI cable reconnect.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect DUT to network | Connect the DUT to an active network via Wi-Fi or Ethernet prior to the test. | The DUT should be connected to an active network with a valid IP address assigned. |
| 2 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 3 | Connect HDMI cable and select source | Connect the HDMI cable between the DUT and the TV/display, with the correct input source selected. | The HDMI cable should be connected and the correct input source should be selected on the TV/display. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT and verify home screen | Reboot the DUT and wait for it to fully boot up. | The DUT should boot up successfully and the RDK UI Home screen should be visible on the TV/display. |
| 2 | Launch VOD video from featured section | In the RDK UI Home screen, navigate to the Featured Video on Demand section and launch any video (preferably one of the first three available videos). | The selected video should start playing with proper audio and video output. |
| 3 | Disconnect and reconnect HDMI cable | Disconnect the HDMI cable from the DUT. Wait approximately 10 seconds, then reconnect the HDMI cable to the DUT. | The video that was playing prior to HDMI disconnection should resume playback with proper audio and video output. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
