## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_19
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_Uninstall_Reboot

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that apps can be uninstalled from the RDK UI and subsequently reinstalled and launched successfully after a DUT reboot. This test exercises the `org.rdk.AppManager` plugin (including APIs such as `clearAppData`, `launchApp`, and `getAppStatus`) and the RDK UI Home screen navigation to drive the application lifecycle. The test confirms that launched App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully. |
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access. |
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |
| 4 | Install required apps if not present | If the required App is not already installed, select the App tile from the Recommended Apps row (or the More Apps tab if not visible on Recommended row) of the RDK UI Home screen and press Enter/OK to install it. Skip this step if the required App is already available in the My Apps section. | The required App should be installed and available in the My Apps section/row of the RDK UI Home screen, ready to launch. If already installed, this step may be skipped. |
| 5 | Sign in to premium apps if applicable | This step is applicable only if the required App is a Premium App (such as YouTube, Amazon Prime, or Netflix). If applicable, sign in with valid user credentials and verify AV playback prior to test execution. | If the required App is a Premium App, it should be signed in with valid user credentials and AV playback should be verified successfully prior to test execution. |
| 6 | Verify app launch and AV playback | Verify that all required Apps are launching successfully from the RDK UI Home screen. For Apps that support A/V playback (regardless of whether the App is a Premium App or not), verify that audio and video playback is working correctly prior to test execution. | All required Apps should launch successfully from the RDK UI Home screen. For Apps supporting A/V playback, audio and video playback should be verified as working correctly prior to test execution. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Navigate to app info icon in | Navigate to App Info icon in left side of the RDK UI Home screen and press enter/Ok button on remote | "App Info page should launch where we should see the Installed app's Info. Each row in App Info page displays the details of a specific application -- including the app icon, app name, app version,<br>runtime package version, and three management option -- Launch, Update, and Uninstall" |
| 2 | Uninstall app via App Info page | Select Uninstall Button and press enter/Ok button on remote and again press enter on Yes option in the dialogue box to confirm Uninstall | In App Info page, when the user clicks Uninstall, a confirmation dialog YES or NO will appear to verify whether the user truly intends to remove the application. Upon Pressing YES A loading/buffering icon should come and uninstall should be done. After some time, uninstall operation should be completed and the row for the uninstalled app should be removed from App Info page |
| 3 | Repeat uninstall for all installed apps | Repeat step 3 on all available installed App | Expected response should be same as step 3 |
| 4 | Reboot DUT and wait for bootup | Reboot the DUT and wait for Boot up | Device should be rebooted and RDK UI home page should be displayed on TV |
| 5 | Navigate to More Apps page | Select More Apps button from Recommended Apps section and press enter/Ok button on remote | More Apps page should load where all apps available in App catalogue are visible |
| 6 | Select uninstalled app tile of step | Select uninstalled App tile of step 3 and press enter/Ok button on remote | When App tile is selected a buffering/loading indicator should be displayed on<br>the app tile which indicates app bundle download and installation started once installation completed a green tick will shown on the app tile for 2 sec. |
| 7 | Verify app installed in background and appears in My Apps | Validate that app installation completed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage | App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage |
| 8 | Launch installed app from My Apps  | Select the Installed App tile from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Selected App should be launched successfully  (Either cold launch /hot launch based on the app's previous state) |
| 9 | Select content or load app | Select any Video Content from launched Apps or (load the App if its not a video App). | Selected Video Content AV playback should start or App should load its content |
| 10 | Close launched apps via Back key | Close/Exit the launched Apps by back key press on remote. | Launched App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
