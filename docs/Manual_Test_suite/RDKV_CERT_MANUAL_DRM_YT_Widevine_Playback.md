## TestCase ID
RDKV_MANUAL_DRM_03
## TestCase Name
RDKV_CERT_MANUAL_DRM_YT_Widevine_Playback

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that YouTube Widevine DRM-protected content playback is functional on the DUT. This test confirms that the protected content plays with proper audio and video output, ensuring Widevine DRM integration meets operator-specific certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Purchase Widevine videos for YouTube account | Purchase Widevine encrypted videos for the YouTube account to be used for testing. | Widevine encrypted videos should be purchased and available in the YouTube account.|
| 2 | Pair Bluetooth remote | Pair and connect the Bluetooth remote to the DUT. | The Bluetooth remote should be paired and connected to the DUT successfully.|
| 3 | Connect DUT to Smart TV via HDMI | Connect the DUT to a Smart TV via HDMI and select the correct HDMI input source on the display. | The DUT should be connected to the Smart TV via HDMI and the correct source should be selected and visible.|
| 4 | Verify YouTube app on home screen | Validate that the YouTube App is available in the My Apps section/row of the RDK UI Home screen. If not present, install the YouTube App from the Recommended Apps row. | The YouTube App should be available and ready to launch from the RDK UI Home screen.|
| 5 | Sign in to YouTube and verify DRM content | After installation and launch of the YouTube App, sign in with valid user credentials and validate that purchased DRM video content is available prior to test execution. | The sign-in should succeed and purchased DRM video content should be visible and accessible in the YouTube account.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch YouTube app | Select the YouTube App tile from the My Apps/Recommended Apps section/row of the RDK UI Home screen and press the Enter/OK button on the remote. | The YouTube App should be launched successfully (either cold launch or hot launch based on the app's previous state).|
| 2 | Navigate to Library → Your Movies section | Navigate to Library → Your Movies section within the YouTube App. | The purchased videos should be listed in the Your Movies section.|
| 3 | Select and initiate Widevine content playback | Select any purchased content that is Widevine encrypted and initiate playback. | The selected Widevine encrypted content should play with proper audio and video without any artifacts or errors.|
| 4 | Validate playback functions | Validate the playback functions: Play/Pause/Play, Forward (FWD), and Rewind (RWD). | All playback functions should operate as expected without any errors or interruptions.|
| 5 | Exit YouTube app | Close/Exit the YouTube App by pressing the Back key on the remote. | The YouTube App should be terminated gracefully and the RDK UI Home screen should be visible on the TV.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
