## TestCase ID
RDKV_MANUAL_APPS_17
## TestCase Name
RDKV_CERT_MANUAL_App_Xumo_Playback_Trickplay

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the Xumo application AV playback functionality including live content, movies, and trickplay operations. This test exercises the DAC App Manager service, the RDK UI Home screen Recommended Apps / More Apps tiles, and the App Info page to manage application installation and launch. The test confirms that the Xumo application should terminate gracefully and the RDK UI Home screen should be visible on the display.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Power on DUT and ensure RDK UI is accessible | Ensure the DUT is powered on and the RDK UI is visible and accessible on the display. | The DUT should be powered on and the RDK UI should be visible and accessible on the display.|
| 2 | Pair Bluetooth remote | Ensure a Bluetooth-paired remote control is available and functional for DUT navigation. | The Bluetooth remote should be paired and functional for DUT navigation.|
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|
| 5 | Install Xumo if not present | If Xumo is not already available in the My Apps section/row of the RDK UI Home screen, select the Xumo tile from the Recommended Apps row (or the More Apps tab if not visible) and press Enter/OK on the remote. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds before disappearing. | The Xumo application should be installed successfully on the DUT.|
| 6 | Verify Xumo listed on home screen | Validate that the installed Xumo application is listed under the My Apps section/row and App Info page of the RDK UI Home screen, confirming it is ready to launch. | The Xumo application should be visible in the My Apps section and on the App Info page, ready to launch.|
| 7 | Verify Xumo launch and content access | Validate that Xumo launches successfully from the RDK UI and that content is accessible prior to test execution. | Xumo should launch correctly from the RDK UI and content should be accessible.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch Xumo app | Select the Xumo application tile from the My Apps/Recommended Apps section/row of the RDK UI Home screen and press Enter/OK on the remote. | The Xumo application should launch successfully (either cold launch or hot launch based on the application's previous state).|
| 2 | Verify live content auto-plays in Xumo | Validate that the Live content section is highlighted and the first live content plays automatically. | The Live content should be highlighted and the first live content should play automatically with proper Audio and Video output.|
| 3 | Verify other live content items play | Validate that other live content items can be selected and played. | Other live content items should also play with proper Audio and Video output.|
| 4 | Navigate to Movies category and play | Navigate to a different content category tile (e.g., Movies), select it, and play a movie. | The Movies tile should be selectable and the selected movie should play with proper Audio and Video output.|
| 5 | Perform fast forward during playback | Perform fast forward during video playback. | Fast forward should operate without errors.|
| 6 | Perform rewind during playback | Perform rewind during video playback. | Rewind should operate without errors.|
| 7 | Pause video playback | Pause the video during playback. | The video should pause successfully.|
| 8 | Resume video from paused state | Resume playback from the paused state. | The video should resume playback from the paused position with proper audio and video output.|
| 9 | Exit Xumo via Back key | Close/exit the Xumo application using the Back key press on the remote. | The Xumo application should terminate gracefully and the RDK UI Home screen should be visible on the display.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
