## TestCase ID
RDKV_MANUAL_RDKUI_37
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Post_Uninstall_App_Reinstall

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that after all apps have been uninstalled, any app can be reinstalled and launched successfully from the My Apps section, More Apps page, and App Info page. This test confirms that the reinstalled app launches correctly from all UI entry points, ensuring app reinstallation after full uninstall meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Ensure all apps are uninstalled | Ensure all apps on the DUT have been uninstalled prior to this test. | The DUT should have no installed apps.|
| 2 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to More Apps page | From RDK UI Home screen, navigate to More Apps | More Apps page should load where all apps available in App catalogue are visible|
| 2 | Reinstall previously uninstalled app from More Apps | Press on the any App which we uninstalled | A buffering/loading indicator should be displayed on the app tile<br>After sometime, buffering/loading icon will disappear and a green tick mark should appear on the tile for 2 to 3 seconds, indicating that the app is successfully installed. A row for My apps should be generated|
| 3 | Launch reinstalled app from My Apps | Launch the just installed app from My Apps by clicking on the app icon | App should be launched|
| 4 | Navigate to More Apps page | Navigate to More Apps and launch the just installed app from More Apps | App should be launched|
| 5 | Exit app and relaunch from My Apps | Exit from the launched app and launch the same app from My Apps | App should be launched|
| 6 | Exit app and open App Info page | Exit from the launched app and navigate to App Info icon in left side of the RDK UI Home screen and press on it | Launched App should be exited to Home screen. App Info page should launch which should display the installed app's Info. Each row in App Info page displays the details of a specific application -- including the app icon, app name, app version,<br>runtime package version, and three management option -- Launch, Update, and Uninstall|
| 7 | Launch app from App Info page | Click on Launch button after selecting the App | App should be launched|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
