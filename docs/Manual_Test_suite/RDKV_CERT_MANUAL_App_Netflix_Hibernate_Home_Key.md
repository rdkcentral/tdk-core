## TestCase ID
RDKV_MANUAL_APPS_20
## TestCase Name
RDKV_CERT_MANUAL_App_Netflix_Hibernate_Home_Key

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the Netflix application hibernate behavior when the Home key is pressed during playback, and subsequent hot launch from the last hibernated state. This test exercises the DAC App Manager service, the RDK UI Home screen Recommended Apps / More Apps tiles, and the App Info page to manage application installation and launch. The test confirms that the Netflix AV playback should resume from the previously noted time position after the application is hot launched from hibernation, confirming that hibernation is functioning as expected.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Power on DUT and ensure RDK UI is accessible | Ensure the DUT is powered on and the RDK UI is visible and accessible on the display. | The DUT should be powered on and the RDK UI should be visible and accessible on the display.|
| 2 | Pair Bluetooth remote | Ensure a Bluetooth-paired remote control is available and functional for DUT navigation. | The Bluetooth remote should be paired and functional for DUT navigation.|
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|
| 5 | Install Netflix if not present | If Netflix is not already available in the My Apps section/row of the RDK UI Home screen, select the Netflix tile from the Recommended Apps row (or the More Apps tab if not visible) and press Enter/OK on the remote. On successful installation, a green tick icon should appear on the tile for approximately 2 seconds before disappearing. | The Netflix application should be installed successfully on the DUT.|
| 6 | Verify Netflix listed on home screen | Validate that the installed Netflix application is listed under the My Apps section/row and App Info page of the RDK UI Home screen, confirming it is ready to launch. | The Netflix application should be visible in the My Apps section and on the App Info page, ready to launch.|
| 7 | Sign in to Netflix and verify A/V playback | Sign in to Netflix with valid user credentials and validate A/V playback prior to test execution. | Sign-in should succeed and A/V playback should be functional in the Netflix application.|
| 8 | Verify Netflix launch and content access | Validate that Netflix launches successfully from the RDK UI and that content is accessible prior to test execution. | Netflix should launch correctly from the RDK UI and content should be accessible.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch Netflix app | Select the Netflix application tile from the My Apps/Recommended Apps section/row of the RDK UI Home screen and press Enter/OK on the remote. | The Netflix application should launch successfully (either cold launch or hot launch based on the application's previous state).|
| 2 | Select video content and initiate Netflix playback | Select any video content from the Netflix application and initiate playback. | The selected video content should start playing with proper Audio and Video output.|
| 3 | Note playback position and press Home key | Note the current video time position, then press the Home key on the remote. | The Netflix application should move to the background (hibernate) and the RDK UI Home screen should launch.|
| 4 | Verify Netflix is hibernated and home screen visible | Validate that the Netflix application is hibernated and the RDK UI Home screen is displayed. | The Netflix application should be in a hibernated state and the RDK UI Home screen should be visible on the display.|
| 5 | Launch Netflix app | Select the Netflix application tile from the My Apps/Recommended Apps section/row of the RDK UI Home screen again and press Enter/OK. | The Netflix application should launch successfully via hot launch from the last hibernated state.|
| 6 | Verify Netflix resumes from hibernated position | Validate that the Netflix AV playback resumes from the time position noted in Step 3. | The Netflix AV playback should resume from the time position noted in Step 3, confirming that hibernation is functioning as expected.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
