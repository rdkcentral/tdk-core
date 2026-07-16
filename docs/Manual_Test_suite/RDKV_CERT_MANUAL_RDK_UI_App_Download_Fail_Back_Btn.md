## TestCase ID
RDKV_MANUAL_RDKUI_28
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_App_Download_Fail_Back_Btn

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that when an app fails to download due to a network issue, the RDK UI displays an appropriate error overlay that can be dismissed using the Back button press from the remote. This test exercises the RDK UI home screen, settings menus, and DAC App Manager navigation via Bluetooth remote key-press events to validate the targeted UI behaviour. The test confirms that the overlay should exit and return the user to previous screen.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Connect DUT to network | Connect the DUT to a network prior to this test. | The DUT should be connected to a network.|
| 3 | Ensure some apps are already installed | Ensure some apps are already installed on the DUT. | Some apps should be installed on the DUT.|
| 4 | Verify Recommended Apps row is populated | Ensure the Recommended Apps row lists the apps available in the App Catalogue. | The Recommended Apps row should be populated with available apps.|
| 5 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Disconnect network on DUT | Disconnect the network | The DUT should not be accessible via SSH as the network is disconnected.|
| 2 | Click on an app in recommended | Click on an app in Recommended Apps which is not installed yet | Error overlay indicating the reason as Network Issue should be displayed|
| 3 | Exit the error overlay by back | Exit the error overlay by back button press from remote | The overlay should exit and return the user to previous screen|
| 4 | Reconnect network on DUT | Connect to a network | Connection should be successful|
| 5 | Navigate to More Apps page | Click on More Apps button | More Apps page should load|
| 6 | Disconnect network on DUT | Disconnect the network | The DUT should not be accessible via SSH as the network is disconnected.|
| 7 | Attempt to install app from More Apps (network off) | Click on an app which is not installed yet | Error overlay indicating the reason as Network Issue should be displayed|
| 8 | Exit the error overlay by back | Exit the error overlay by back button press from remote | The overlay should exit and return the user to previous screen|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
