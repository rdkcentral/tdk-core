## TestCase ID
RDKV_MANUAL_HDMIHOTPLUG_04
## TestCase Name
RDKV_CERT_MANUAL_HDMIHOTPLUG_THIRD_PARTY_APP_PLAYBACK_ON_RECONNECT

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that content playback in third-party installed applications continues without interruption after an HDMI cable reconnect.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Connect DUT to network | Connect the DUT to an active network via Wi-Fi or Ethernet prior to the test. | The DUT should be connected to an active network with a valid IP address assigned. |
| 2 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully. |
| 3 | Connect HDMI cable and select source | Connect the HDMI cable between the DUT and the TV/display, with the correct input source selected. | The HDMI cable should be connected and the correct input source should be selected on the TV/display. |
| 4 | Install required application | Navigate to the Recommended Apps row on the RDK UI Home screen (or the More Apps tab if the required application is not visible), select the required application tile, and press Enter/OK on the remote. Verify that a buffering/loading indicator appears on the tile, indicating that the app bundle download and installation has started. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds. | The required application should be installed successfully on the DUT. |
| 5 | Verify app listed on home screen | Verify that the installed application is listed under the My Apps section/row and on the App Info page of the RDK UI Home screen, confirming it is ready to launch. | The installed application should be visible in the My Apps section and on the App Info page, ready to launch. |
| 6 | Sign in to premium application | If the installed application is a premium application (such as YouTube, Amazon Prime, or Netflix), sign in with valid user credentials and verify A/V playback is functional prior to test execution. | Sign-in should succeed and A/V playback should be functional in the installed application. |
| 7 | Verify all apps launch correctly | Verify that all installed applications launch correctly from the RDK UI, and that any purchased content and premium features are accessible prior to test execution. | All installed applications should launch correctly and purchased content and premium features should be accessible. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot DUT and verify home screen | Reboot the DUT and wait for it to fully boot up. | The DUT should boot up successfully and the RDK UI Home screen should be visible on the TV/display. |
| 2 | Launch third-party installed application | From the RDK UI Home screen, navigate to the My Apps / Recommended Apps section or the App Info page, select a third-party installed application tile, and press Enter/OK on the remote. | The selected application should launch successfully (cold launch or hot launch based on the app's previous state). |
| 3 | Play content in application | If the launched application is a video application, play any available video content. Otherwise, open and load the application content. | If a video application, the selected video content A/V playback should start. If a non-video application, the application content should be displayed correctly. |
| 4 | Disconnect and reconnect HDMI cable | Disconnect the HDMI cable from the DUT. Wait approximately 10 seconds, then reconnect the HDMI cable to the DUT. | If a video application was playing, video playback should resume with proper audio and video output. If the application does not support A/V, the application content should remain visible after reconnection. |
| 5 | Repeat for all installed applications | Repeat Steps 2 and 3 for all other installed applications listed under the My Apps tab. | The expected results for each application should be consistent with the outcomes described in Steps 2 and 3. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
