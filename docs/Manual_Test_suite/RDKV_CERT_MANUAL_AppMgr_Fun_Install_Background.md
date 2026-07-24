## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_18
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_Install_Background

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that an application download and installation continues in the background when the user navigates away from the More Apps section on the DUT. This test confirms that the installation completes successfully without requiring continued user interaction, ensuring that background installation behavior meets certification standards.

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
| 1 | Navigate to More Apps page | Select More Apps button from Recommended Apps section and press Enter/OK on the remote | More Apps page should load where all apps available in App catalogue are visible|
| 2 | Select app and start download | Select any App tile and press Enter/OK on the remote | When App tile is selected a buffering/loading indicator should be displayed on<br>the app tile which indicates app bundle download and installation started|
| 3 | Navigate away and observe background install | Immediately press Home key from remote and observe the behaviour | RDK UI Home screen should be loaded and App installation should proceed in background without any interruption|
| 4 | Verify app installed in background and appears in My Apps | Validate that app installation completed and available in the My Apps/Recommended Apps section/row of RDK UI Home screen | App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Home screen|
| 5 | Launch installed app from My Apps  | Select the Installed App tile from the My Apps/Recommended Apps section/row of RDK UI Home screen and press Enter/OK on the remote | Selected App should be launched successfully  either as a cold launch or hot launch depending on the app's previous state.|
| 6 | Select content or load app | Select any Video Content from launched Apps or (load the App if its not a video App). | Selected Video Content AV playback should start or App should load its content|
| 7 | Close launched apps via Back key | Close/Exit the launched Apps by back key press on remote. | Launched App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
