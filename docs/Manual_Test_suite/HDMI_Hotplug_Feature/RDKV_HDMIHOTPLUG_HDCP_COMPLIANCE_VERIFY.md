## TestCase ID
RDKV_MANUAL_HDMIHOTPLUG_14
## TestCase Name
RDKV_CERT_MANUAL_HDMIHOTPLUG_HDCP_COMPLIANCE_VERIFY

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate HDCP compliance by verifying A/V playback behavior across HDMI cable disconnect/reconnect and DUT standby/power-on cycles.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect DUT to network | Connect the DUT to an active network via Wi-Fi or Ethernet prior to the test. | The DUT should be connected to an active network with a valid IP address assigned. |
| 2 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 3 | Connect HDMI cable to HDCP-compliant display | Connect the HDMI cable between the DUT and an HDCP-compliant TV/display, with the correct input source selected. | The HDMI cable should be connected to an HDCP-compliant TV/display and the correct input source should be selected. |
| 4 | Install YouTube application | Navigate to the Recommended Apps row on the RDK UI Home screen (or the More Apps tab if the YouTube application is not visible), select the YouTube application tile, and press Enter/OK on the remote. Verify that a buffering/loading indicator appears on the tile, indicating that the app bundle download and installation has started. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds. | The YouTube application should be installed successfully on the DUT. |
| 5 | Verify YouTube app listed on home screen | Verify that the YouTube application is listed under the My Apps section/row and on the App Info page of the RDK UI Home screen, confirming it is ready to launch. | The YouTube application should be visible in the My Apps section and on the App Info page, ready to launch. |
| 6 | Sign in to YouTube and verify playback | Sign in to the YouTube application with valid user credentials and verify A/V playback is functional prior to test execution. | Sign-in should succeed and A/V playback should be functional in the YouTube application. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch YouTube app and verify A/V playback | From the RDK UI Home screen, navigate to the My Apps / Recommended Apps section, select the YouTube application tile, and press Enter/OK on the remote. | The YouTube application should launch successfully (cold launch or hot launch based on the app's previous state). |
| 2 | Play video and verify on HDCP-compliant display | Play any video from the YouTube application and verify A/V playback on the HDCP-compliant TV/display. | The video should play in the YouTube application with proper audio and video output on the HDCP-compliant TV/display. |
| 3 | Disconnect HDMI and reboot DUT | Disconnect the HDMI cable from the DUT, then reboot the DUT. | The DUT should reboot successfully. |
| 4 | Reconnect HDMI and verify YouTube playback | After the DUT completes bootup, reconnect the HDMI cable to the DUT and verify A/V playback on the YouTube application. | The DUT should boot up and the RDK UI should be visible on the display. YouTube A/V playback should function correctly after HDMI reconnection. |
| 5 | Put DUT into standby mode | Press the Power key on the Bluetooth remote to put the DUT into standby mode. | The DUT should enter standby mode successfully. |
| 6 | Power on DUT from standby | Press the Power key on the Bluetooth remote to power on the DUT. | The DUT should power on and the RDK UI Home screen should be visible on the TV/display. |
| 7 | Disconnect and reconnect HDMI, verify playback | Disconnect the HDMI cable from the DUT, then reconnect it and verify A/V playback on the YouTube application. | The RDK UI should be visible on the display and YouTube A/V playback should function correctly with proper audio and video output after HDMI reconnection. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
