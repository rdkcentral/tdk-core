## TestCase ID
RDKV_MANUAL_HDMIHOTPLUG_11
## TestCase Name
RDKV_CERT_MANUAL_HDMI_Hotplug_Miracast_Playback_On_Reconnect

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that Miracast screen casting from a smartphone continues without interruption after an HDMI cable reconnect on the DUT. This test exercises the RDK HDMI hotplug detection service and display manager to validate display connection and disconnection event handling. The test confirms that the Miracast screen casting session should not be interrupted and video playback should continue on the DUT with proper audio and video output after HDMI reconnection.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect DUT to active Wi-Fi network | Connect the DUT to an active Wi-Fi network and ensure it is reachable from the smartphone prior to the test. | The DUT should be connected to an active Wi-Fi network and reachable from the smartphone. |
| 2 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 3 | Connect HDMI cable and select source | Connect the HDMI cable between the DUT and the TV/display, with the correct input source selected. | The HDMI cable should be connected and the correct input source should be selected on the TV/display. |
| 4 | Connect smartphone to same Wi-Fi network | Connect the smartphone and the DUT to the same Wi-Fi network. | Both the smartphone and the DUT should be on the same Wi-Fi network. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT and verify home screen | Reboot the DUT and wait for it to fully boot up. | The DUT should boot up successfully and the RDK UI Home screen should be visible on the TV/display. |
| 2 | Initiate Miracast screen cast from smartphone | Initiate screen casting from the smartphone to the DUT using Miracast and start playing a video from any application on the smartphone. | The smartphone screen should be mirrored on the DUT display and the video should play with proper audio and video output. |
| 3 | Disconnect and reconnect HDMI cable | Disconnect the HDMI cable from the DUT. Wait approximately 10 seconds, then reconnect the HDMI cable to the DUT. | The Miracast screen casting session should not be interrupted and video playback should continue on the DUT with proper audio and video output after HDMI reconnection. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
