## TestCase ID
RDKV_MANUAL_APPS_15
## TestCase Name
RDKV_CERT_MANUAL_App_Prime_Video_Exit_Back_Key

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the Amazon Prime Video application can be exited gracefully using the Back key press on the remote control. This test exercises the DAC App Manager service, the RDK UI Home screen Recommended Apps / More Apps tiles, and the App Info page to manage application installation and launch. The test confirms that video playback should end gracefully. The application should close and the RDK UI Home screen should launch.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Power on DUT and ensure RDK UI is accessible | Ensure the DUT is powered on and the RDK UI is visible and accessible on the display. | The DUT should be powered on and the RDK UI should be visible and accessible on the display.|
| 2 | Pair Bluetooth remote | Ensure a Bluetooth-paired remote control is available and functional for DUT navigation. | The Bluetooth remote should be paired and functional for DUT navigation.|
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|
| 5 | Install Amazon Prime Video if not present | If Amazon Prime Video is not already available in the My Apps section/row of the RDK UI Home screen, select the Amazon Prime Video tile from the Recommended Apps row (or the More Apps tab if not visible) and press Enter/OK on the remote. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds before disappearing. | The Amazon Prime Video application should be installed successfully on the DUT.|
| 6 | Verify Amazon Prime Video listed on home screen | Validate that the installed Amazon Prime Video application is listed under the My Apps section/row and App Info page of the RDK UI Home screen, confirming it is ready to launch. | The Amazon Prime Video application should be visible in the My Apps section and on the App Info page, ready to launch.|
| 7 | Sign in to Amazon Prime Video and verify A/V playback | Sign in to Amazon Prime Video with valid user credentials and validate A/V playback prior to test execution. | Sign-in should succeed and A/V playback should be functional in the Amazon Prime Video application.|
| 8 | Verify Amazon Prime Video launch and content access | Validate that Amazon Prime Video launches successfully from the RDK UI and that content is accessible prior to test execution. | Amazon Prime Video should launch correctly from the RDK UI and content should be accessible.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch Amazon Prime Video app | Select the Amazon Prime Video application tile from the My Apps/Recommended Apps section/row of the RDK UI Home screen and press Enter/OK on the remote. | The Amazon Prime Video application should launch successfully (either cold launch or hot launch based on the application's previous state).|
| 2 | Select video content and initiate Amazon Prime playback | Select any video content from the Amazon Prime Video application and initiate playback. | The selected video content should start playing with proper Audio and Video output.|
| 3 | Press Back key multiple times to navigate back | Press the Back key multiple times (approximately 3 times) until a confirmation screen appears prompting to exit from the application. | For each Back key press, the screen should navigate one level back. A confirmation screen should appear offering the option to exit or continue in the application.|
| 4 | Select exit from confirmation screen | Select the exit option from the confirmation screen. | Video playback should end gracefully. The application should close and the RDK UI Home screen should launch.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
