## TestCase ID
RDKV_MANUAL_APPS_24
## TestCase Name
RDKV_CERT_MANUAL_APP_FEATURED_VOD_SECOND_TRICKPLAY

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the trickplay (fast forward, rewind, pause, and resume) functionality for the second Featured Video On Demand (VOD) content from the RDK UI Home screen.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Power on DUT and ensure RDK UI is accessible | Ensure the DUT is powered on and the RDK UI is visible and accessible on the display. | The DUT should be powered on and the RDK UI should be visible and accessible on the display. |
| 2 | Pair Bluetooth remote | Ensure a Bluetooth-paired remote control is available and functional for DUT navigation. | The Bluetooth remote should be paired and functional for DUT navigation. |
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access. |
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Select Featured VOD tile and initiate playback | From the Featured Video on Demand area in the RDK UI Home screen, select the second tile and press OK. | The second Featured Video on Demand content should open and play with proper Audio and Video output. The navigation bar should be visible at the bottom of the screen with Rewind, Pause, and Forward buttons. |
| 2 | Wait for nav bar to disappear and press Up | Wait a few seconds until the navigation bar disappears, then press the Up button on the remote. | The navigation bar should reappear with the Pause button highlighted. |
| 3 | Press OK to pause video via nav bar | With the Pause button highlighted in the navigation bar, press OK to pause the video. | The video should be paused and the Pause button should change to a Play button. |
| 4 | Press OK to resume video via nav bar | With the Play button highlighted in the navigation bar, press OK to resume the video. | The video should resume playback and the Play button should change to a Pause button. |
| 5 | Press Forward button and verify skip | Navigate to the Forward button and press OK. Repeat multiple times. | For each Forward button press, the video should skip forward by 8 seconds and continue playing with proper Audio and Video output. |
| 6 | Press Rewind button and verify skip | Navigate to the Rewind button and press OK. Repeat multiple times. | For each Rewind button press, the video should skip backward by 8 seconds and continue playing with proper Audio and Video output. |
| 7 | Exit application via Back key | Press the Back key from the application. | The application should exit and the RDK UI Home screen should launch. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
