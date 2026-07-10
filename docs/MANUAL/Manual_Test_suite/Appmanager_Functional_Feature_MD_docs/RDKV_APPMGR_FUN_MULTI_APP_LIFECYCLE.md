## TestCase ID
RDKV_MANUAL_APPMGR_FUNCTIONAL_08
## TestCase Name
RDKV_CERT_MANUAL_APPMGR_FUN_MULTI_APP_LIFECYCLE

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the lifecycle management behavior of multiple applications launched and suspended from the RDK UI.

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
| 1 | Verify YouTube app is installed | Validate that YouTube App is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If YouTube is not installed follow the instructions of Pre condition 4 | YouTube App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage. |
| 2 | Verify Amazon Prime app is installed | Validate that Amazon Prime App is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If Amazon Prime is not installed follow the instructions of Pre condition 4 | Amazon Prime App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage. |
| 3 | Verify other apps are installed | Validate that other Apps is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If Other Apps are not installed follow the instructions of Pre condition 4 | Other App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage. |
| 4 | Launch any installed app from home screen | Select any installed Apps from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Installed Apps should be launched succesfully (cold launch) |
| 5 | Select content or load app | Select any Video Content from launched Apps or (load the App if its not a video App). | Selected Video Content AV playback should start or App should load its content |
| 6 | Press Home key to suspend app | Press Home key from remote on the launched Apps | App should not terminate but goes to a suspended or hibernated state |
| 7 | Repeat launch/suspend steps for multiple apps | Repeat the steps 4 - 6 on multiple Apps | Expected Response should be same as step 4 -6 |
| 8 | Relaunch all installed apps and verify state | Launch all the installed Apps again one by one and verify the App state | All the apps should resume from the last closed state when its relaunched and playback should be fine |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
