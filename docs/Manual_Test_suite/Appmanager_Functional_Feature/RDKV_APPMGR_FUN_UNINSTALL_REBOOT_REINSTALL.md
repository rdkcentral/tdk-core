## TestCase ID
RDKV_MANUAL_APPMGR_FUNCTIONAL_19
## TestCase Name
RDKV_CERT_MANUAL_APPMGR_FUN_UNINSTALL_REBOOT_REINSTALL

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that apps can be uninstalled from the RDK UI and subsequently reinstalled and launched successfully after a DUT reboot.

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
| 2 | Navigate to app info icon in | Navigate to App Info icon in left side of the RDK UI Home screen and press enter/Ok button on remote | "App Info page should launch where we should see the Installed app's Info. Each row in App Info page displays the details of a specific application -- including the app icon, app name, app version,<br>runtime package version, and three management option -- Launch, Update, and Uninstall" |
| 3 | Uninstall app via App Info page | Select Uninstall Button and press enter/Ok button on remote and again press enter on Yes option in the dialogue box to confirm Uninstall | In App Info page, when the user clicks Uninstall, a confirmation dialog YES or NO will appear to verify whether the user truly intends to remove the application. Upon Pressing YES A loading/buffering icon should come and uninstall should be done. After some time, uninstall operation should be completed and the row for the uninstalled app should be removed from App Info page |
| 4 | Repeat uninstall for all installed apps | Repeat step 3 on all available installed App | Expected response should be same as step 3 |
| 5 | Reboot DUT and wait for bootup | Reboot the DUT and wait for Boot up | Device should be rebooted and RDK UI home page should be displayed on TV |
| 6 | Navigate to More Apps page | Select More Apps button from Recommended Apps section and press enter/Ok button on remote | More Apps page should load where all apps available in App catalogue are visible |
| 7 | Select uninstalled app tile of step | Select uninstalled App tile of step 3 and press enter/Ok button on remote | When App tile is selected a buffering/loading indicator should be displayed on<br>the app tile which indicates app bundle downlad and installation started once installation completed a green tick will shown on the app tile for 2 sec. |
| 8 | Verify app installed in background and appears in My Apps | Validate that app installation completed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage | App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage |
| 9 | Select the installed app tile from | Select the Installed App tile from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Selected App should be launched succesfully  (Either cold launch /hot launch based on the app's previous state) |
| 10 | Select content or load app | Select any Video Content from launched Apps or (load the App if its not a video App). | Selected Video Content AV playback should start or App should load its content |
| 11 | Close launched apps via Back key | Close/Exit the launched Apps by back key press on remote. | Launched App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
