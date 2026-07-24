## TestCase ID
RDKV_MANUAL_RDKUI_32
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_App_Install_Navigate_Away

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that navigating away from the More Apps page while an app is downloading does not interrupt the download, and that the app installs and launches successfully in the background. This test confirms that background app downloads complete and the app is launchable after installation, ensuring background download continuity meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to More Apps page | Click on More Apps button from Recommended Apps section. | More Apps page should load where all apps available in App catalogue are visible|
| 2 | Select app to start download | Press on an App which is not installed yet | It should start downloading the app and a buffering/loading icon should be displayed on the app tile|
| 3 | Press Home button to go to Home screen | Press Home Button from remote | The RDK UI Home screen should launch.|
| 4 | After some time, validate that the | After some time, validate that the App which we tried to download is available in My Apps | Even though we navigated away during download, app should be downloaded and installed and should be available in My Apps section|
| 5 | Launch the just installed app | Launch the just installed app | App should be launched|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
