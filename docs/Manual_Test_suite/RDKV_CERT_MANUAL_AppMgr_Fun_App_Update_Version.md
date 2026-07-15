## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_16
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_App_Update_Version

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the Update button in the App Info screen is activated based on the versioning information provided by the AppManager. This test exercises the `org.rdk.AppManager` plugin (including APIs such as `clearAppData`, `launchApp`, and `getAppStatus`) and the RDK UI Home screen navigation to drive the application lifecycle. The test confirms that app should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.

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
| 1 | Navigate to app info icon in | Navigate to App Info icon in left side of the RDK UI Home screen and press enter/Ok button on remote | "App Info page should launch where we should see the Installed app's Info. Each row in App Info page displays the details of a specific application -- including the app icon, app name, app version,<br>runtime package version, and three management option -- Launch, Update, and Uninstall" |
| 2 | Verify Update button state in App Info page | Validate that Update button is active or grayed out. | Based on this versioning info from App catalogue server if new version of App is available update button should be displayed as active and if App is already been in latest version then update button should be in grayed out state |
| 3 | If update button is in active | If Update button is in active state select and  press enter/Ok button on remote | A buffering/loading indicator should be displayed on the app tile during updating to the latest version and a green tick should be displayed for 2-3 seconds on the app tile after successful update. |
| 4 | Launch updated app from App Info page | Select Launch button of the same App and press enter/Ok button on remote | Updated Selected App with latest vesrion should be launched successfully |
| 5 | Select content or load app | Select any Video Content from launched Apps or (load the App if its not a video App). | Selected Video Content AV playback should start or App should load its content |
| 6 | Close apps via Back key | Close/Exit the Apps by back key press on remote. | App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
