## TestCase ID
RDKV_MANUAL_HDMIHOTPLUG_10
## TestCase Name
RDKV_CERT_MANUAL_HDMIHOTPLUG_CAST_PLAYBACK_ON_RECONNECT

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that YouTube video casting from a smartphone to the DUT continues without interruption after an HDMI cable reconnect.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect DUT to network | Connect the DUT to an active network via Wi-Fi or Ethernet prior to the test. | The DUT should be connected to an active network with a valid IP address assigned. |
| 2 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 3 | Connect HDMI cable and select source | Connect the HDMI cable between the DUT and the TV/display, with the correct input source selected. | The HDMI cable should be connected and the correct input source should be selected on the TV/display. |
| 4 | Connect smartphone to same Wi-Fi network | Connect the smartphone and the DUT to the same Wi-Fi network. | Both the smartphone and the DUT should be on the same Wi-Fi network and reachable from each other. |
| 5 | Install YouTube application | Navigate to the Recommended Apps row on the RDK UI Home screen (or the More Apps tab if the YouTube application is not visible), select the YouTube application tile, and press Enter/OK on the remote. Verify that a buffering/loading indicator appears on the tile, indicating that the app bundle download and installation has started. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds. | The YouTube application should be installed successfully on the DUT. |
| 6 | Verify YouTube app listed on home screen | Verify that the YouTube application is listed under the My Apps section/row and on the App Info page of the RDK UI Home screen, confirming it is ready to launch. | The YouTube application should be visible in the My Apps section and on the App Info page, ready to launch. |
| 7 | Sign in to YouTube and verify playback | Sign in to the YouTube application with valid user credentials and verify A/V playback is functional prior to test execution. | Sign-in should succeed and A/V playback should be functional in the YouTube application. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT and verify home screen | Reboot the DUT and wait for it to fully boot up. | The DUT should boot up successfully and the RDK UI Home screen should be visible on the TV/display. |
| 2 | Verify YouTube app available on home screen | Verify that the YouTube application is installed and its tile is available in the My Apps / Recommended Apps section of the RDK UI Home screen. | The YouTube application tile should be available in the My Apps / Recommended Apps section of the RDK UI Home screen. |
| 3 | Cast YouTube from smartphone and initiate playback | From the smartphone, cast YouTube to the DUT and initiate video playback. | The YouTube application should launch on the DUT (cold launch or hot launch based on the app's previous state) and the video should play with proper audio and video output. |
| 4 | Disconnect and reconnect HDMI cable | Disconnect the HDMI cable from the DUT. Wait approximately 10 seconds, then reconnect the HDMI cable to the DUT. | The YouTube casting session should not be interrupted and video playback should continue on the DUT with proper audio and video output after HDMI reconnection. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
