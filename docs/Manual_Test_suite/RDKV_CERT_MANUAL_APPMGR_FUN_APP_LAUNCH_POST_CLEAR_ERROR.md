## TestCase ID
RDKV_MANUAL_APPMGR_FUNCTIONAL_22
## TestCase Name
RDKV_CERT_MANUAL_APPMGR_FUN_APP_LAUNCH_POST_CLEAR_ERROR

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that appropriate error messages are displayed when attempting to launch an application after its application data has been cleared.

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
| 2 | Launch app from Recommended/My Apps | Select the App tile from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Selected App should be launched succesfully  (Either cold launch /hot launch based on the app's previous state) |
| 3 | Select content or load app | Select any Video Content from launched Apps or (load the App if its not a video App). | Selected Video Content AV playback should start or App should load its content |
| 4 | Delete app file from /opt/dac_apps/apps | Naviage to cd /opt/dac_apps/apps and delete the launched app file :<br>Eg : rm com.rdkcentral.youtube | com.rdkcentral.youtube app related file should be removed but App functionality or playback shouldn't get affected. |
| 5 | Close launched apps via Back key | Close/Exit the launched Apps by back key press on remote. | Launched App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display. |
| 6 | Select the closed app tile from | Select the closed app tile from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Selected App should not be launched since app files are removed and app launch failed error message should be displayed on RDK UI |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
