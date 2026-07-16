## TestCase ID
RDKV_MANUAL_APPS_26
## TestCase Name
RDKV_CERT_MANUAL_App_Featured_Vod_Third_Home_Exit

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the RDK UI Home screen is launched when the Home button is pressed during the third Featured Video On Demand (VOD) content playback. This test exercises the DAC App Manager service, the RDK UI Home screen Recommended Apps / More Apps tiles, and the App Info page to manage application installation and launch. The test confirms that the video should end gracefully and the RDK UI Home screen should launch.

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
| 1 | Select Featured VOD tile and initiate playback | From the Featured Video on Demand area in the RDK UI Home screen, select the third tile and press OK. | The third Featured Video on Demand content should open and play with proper Audio and Video output. The navigation bar should be visible at the bottom of the screen with Rewind, Pause, and Forward buttons. |
| 2 | Exit to home screen via Home button | Press the Home button during video playback. | The video should end gracefully and the RDK UI Home screen should launch. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
