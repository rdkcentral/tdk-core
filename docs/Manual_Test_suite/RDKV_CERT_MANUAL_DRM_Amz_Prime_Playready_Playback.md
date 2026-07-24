## TestCase ID
RDKV_MANUAL_DRM_04
## TestCase Name
RDKV_CERT_MANUAL_DRM_Amz_Prime_Playready_Playback

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that Amazon Prime Video PlayReady DRM-protected content playback is functional on the DUT. This test confirms that the protected content plays with proper audio and video output, ensuring PlayReady DRM integration meets operator-specific certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 2 | Connect DUT to Smart TV via HDMI | Connect the DUT to a Smart TV via HDMI and select the correct HDMI input source on the display. | The DUT should be connected to the Smart TV via HDMI and the correct source should be selected and visible.|
| 3 | Verify Amazon Prime app on home screen | Validate that the Amazon Prime App is available in the My Apps section/row of the RDK UI Home screen. If not present, install the Amazon Prime App from the Recommended Apps row. | The Amazon Prime App should be available and ready to launch from the RDK UI Home screen.|
| 4 | Sign in to Amazon Prime and verify DRM content | After installation and launch of the Amazon Prime App, sign in with valid user credentials and validate that purchased DRM video content is available prior to test execution. | The sign-in should succeed and purchased DRM video content should be visible and accessible in the Amazon Prime account.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch Amazon Prime app | Select the Amazon Prime App tile from the My Apps/Recommended Apps section/row of the RDK UI Home screen and press the Enter/OK button on the remote. | The Amazon Prime App should be launched successfully (either cold launch or hot launch based on the app's previous state).|
| 2 | Navigate to Movies section | Navigate to the Movies section within the Amazon Prime App. | The available movies should be listed in the Movies section.|
| 3 | Select and initiate PlayReady content playback | Select any purchased content that is PlayReady encrypted and initiate playback. | The selected PlayReady encrypted content should play with proper audio and video without any artifacts or errors.|
| 4 | Validate playback functions | Validate the playback functions: Play/Pause/Play, Forward (FWD), and Rewind (RWD). | All playback functions should operate as expected without any errors or interruptions.|
| 5 | Exit Amazon Prime app | Close/Exit the Amazon Prime App by pressing the Back key on the remote. | The Amazon Prime App should be terminated gracefully and the RDK UI Home screen should be visible on the TV.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
