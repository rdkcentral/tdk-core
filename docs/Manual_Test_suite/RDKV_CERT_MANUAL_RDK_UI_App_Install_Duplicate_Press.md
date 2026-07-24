## TestCase ID
RDKV_MANUAL_RDKUI_24
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_App_Install_Duplicate_Press

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that pressing an installed app tile from various locations in the RDK UI always launches the application successfully regardless of whether it is a cold or hot launch. This test confirms that the launched app closes correctly and the RDK UI Home screen is restored, ensuring consistent app launch behavior from multiple UI entry points meets certification requirements.
<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Ensure app under test is installed | Ensure the app under test is already installed on the DUT and visible in the RDK UI. | The app should be installed and visible in the RDK UI.|
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch installed app from Recommended Apps | Navigate to Recommended Apps and press on any App tile which is already installed | The selected App should launch|
| 2 | Close app via Back key | Press Back button(number of back button presses may vary depending on the app and app state)  so that app can be closed | Launched App should close and The RDK UI Home screen should launch.|
| 3 | Open More Apps page | Press on More Apps button and press on the same App tile (which we opened in step 1) | The selected App should launch|
| 4 | Close app via Back key | Press Back button(number of back button presses may vary depending on the app and app state)  so that app can be closed | Launched App should close and The RDK UI Home screen should launch.|
| 5 | Launch installed app from My Apps | In My Apps section, press on the same App tile (which we opened in step 1) | The selected App should launch|
| 6 | Close app via Back key | Press Back button(number of back button presses may vary depending on the app and app state)  so that app can be closed | Launched App should close and The RDK UI Home screen should launch.|
| 7 | Open App Info page | Press on App Info button in the left side of RDK UI Home screen | App Info page should launch which should display the installed app's Info. Each row in App Info page displays the details of a specific application -- including the app icon, app name, app version,<br>runtime package version, and three management option -- Launch, Update, and Uninstall|
| 8 | Launch app from App Info page | Press on the Launch button against the same app tile (which we opened in step1) | The selected App should launch|
| 9 | Close app via Back key | Press Back button(number of back button presses may vary depending on the app and app state)  so that app can be closed | Launched App should close and The RDK UI Home screen should launch.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
