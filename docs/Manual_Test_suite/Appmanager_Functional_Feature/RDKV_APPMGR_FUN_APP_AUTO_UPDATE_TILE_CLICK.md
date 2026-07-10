## TestCase ID
RDKV_MANUAL_APPMGR_FUNCTIONAL_09
## TestCase Name
RDKV_CERT_MANUAL_APPMGR_FUN_APP_AUTO_UPDATE_TILE_CLICK

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that if a newer version of an installed application is available, clicking the app tile from the Recommended Apps row automatically updates the application to the latest version.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully. |
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access. |
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify required apps are installed | Validate that required Apps is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If required Apps are not installed follow the instructions of Pre condition 4 | Required Apps should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage. |
| 2 | Launch app from Recommended/My Apps | Select the App tile from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Selected App should be launched succesfully  (Either cold launch /hot launch based on the app's previous state) if new version of App is available App shouldn't launch |
| 3 | Verify app is downloading and upgrading | If selected App is not launching Validate that the App is downloading and upgrading to the latest verison | When required App tile is selected a buffering/loading indicator should be displayed on<br>the app tile which indicates app bundle downlad and installation started. On successful installation a green tick icon should appear on the tile for approximately 2s before disappearing |
| 4 | Launch app from Recommended/My Apps | Select the App tile again from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Selected App should be launched succesfully with Newer Version  (Either cold launch /hot launch based on the app's previous state) |
| 5 | Select content or load app | Select any Video Content from launched Apps or (load the App if its not a video App). | Selected Video Content AV playback should start or App should load its content |
| 6 | Close/exit the app by back key | Close/Exit the App by back key press on remote. | App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
