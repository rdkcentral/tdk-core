## TestCase ID
RDKV_MANUAL_APPS_11
## TestCase Name
RDKV_CERT_MANUAL_App_YouTube_Playback_Trickplay

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the YouTube application AV playback and trickplay (fast forward, rewind, pause, and resume) functionality on the DUT. This test confirms that all playback controls operate correctly and the application terminates gracefully afterwards, ensuring that streaming app playback features meet certification standards.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Power on DUT and ensure RDK UI is accessible | Ensure the DUT is powered on and the RDK UI is visible and accessible on the display. | The DUT should be powered on and the RDK UI should be visible and accessible on the display.|
| 2 | Pair Bluetooth remote | Ensure a Bluetooth-paired remote control is available and functional for DUT navigation. | The Bluetooth remote should be paired and functional for DUT navigation.|
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|
| 5 | Install YouTube if not present | If YouTube is not already available in the My Apps section/row of the RDK UI Home screen, select the YouTube tile from the Recommended Apps row (or the More Apps tab if not visible) and press Enter/OK on the remote. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds before disappearing. | The YouTube application should be installed successfully on the DUT.|
| 6 | Verify YouTube listed on home screen | Validate that the installed YouTube application is listed under the My Apps section/row and App Info page of the RDK UI Home screen, confirming it is ready to launch. | The YouTube application should be visible in the My Apps section and on the App Info page, ready to launch.|
| 7 | Sign in to YouTube and verify A/V playback | Sign in to YouTube with valid user credentials and validate A/V playback prior to test execution. | Sign-in should succeed and A/V playback should be functional in the YouTube application.|
| 8 | Verify YouTube launch and content access | Validate that YouTube launches successfully from the RDK UI and that content is accessible prior to test execution. | YouTube should launch correctly from the RDK UI and content should be accessible.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch YouTube app | Select the YouTube application tile from the My Apps/Recommended Apps section/row of the RDK UI Home screen and press Enter/OK on the remote. | The YouTube application should launch successfully (either cold launch or hot launch based on the application's previous state).|
| 2 | Select video content and initiate YouTube playback | Select any video content from the YouTube application and initiate playback. | The selected video content should start playing with proper Audio and Video output.|
| 3 | Perform fast forward during playback | Perform fast forward during video playback. | Fast forward should operate without errors.|
| 4 | Perform rewind during playback | Perform rewind during video playback. | Rewind should operate without errors.|
| 5 | Pause video playback | Pause the video during playback. | The video should pause successfully.|
| 6 | Resume video from paused state | Resume playback from the paused state. | The video should resume playback from the paused position with proper audio and video output.|
| 7 | Exit YouTube via Back key | Close/exit the YouTube application using the Back key press on the remote. | The YouTube application should terminate gracefully and the RDK UI Home screen should be visible on the display.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
