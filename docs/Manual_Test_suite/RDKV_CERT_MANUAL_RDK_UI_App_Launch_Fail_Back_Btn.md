## TestCase ID
RDKV_MANUAL_RDKUI_26
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_App_Launch_Fail_Back_Btn

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that when an app launch fails due to a network issue, the RDK UI displays an appropriate error overlay that can be dismissed using the Back button on the remote. This test confirms that the error overlay exits cleanly and returns the user to the previous screen, ensuring app launch failure error handling via the Back button meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Ensure stable network connection | Ensure a stable network connection is available on the DUT. | The DUT should have a stable network connection.|
| 3 | Ensure app under test is installed | Ensure the app under test is already installed on the DUT and visible in the RDK UI. | The app should be installed and visible in the RDK UI.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Disconnect network on DUT | Disconnect the network | The DUT should not be accessible via SSH as the network is disconnected.|
| 2 | Attempt to launch app from My Apps (network off) | Launch any app from My Apps | Error overlay indicating the reason as Network Issue should be displayed|
| 3 | Dismiss error overlay via Back button | Exit the error overlay using back button press from the remote | The overlay should exit and return the user to previous screen|
| 4 | Attempt to launch app from Recommended Apps (network off) | Launch any installed app from Recommended Apps | Error overlay indicating the reason as Network Issue should be displayed|
| 5 | Dismiss error overlay via Back button | Exit the error overlay using back button press from the remote | The overlay should exit and return the user to previous screen|
| 6 | Navigate to More Apps page | Click on More Apps button | Error overlay indicating the reason as Network Issue should be displayed|
| 7 | Dismiss error overlay via Back button | Exit the error overlay using back button press from the remote | The overlay should exit|
| 8 | Open App Info page | Press on the App Info button on the left side of the UI | App Info page should launch which should display the installed apps Info|
| 9 | Attempt to launch app from App Info (network off) | Press on Launch button against the installed app | Error overlay indicating the reason as Network Issue should be displayed|
| 10 | Dismiss error overlay via Back button | Exit the error overlay using back button press from the remote | The overlay should exit and return the user to previous screen|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
