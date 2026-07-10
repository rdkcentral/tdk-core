## TestCase ID
RDKV_MANUAL_RDKUI_36
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_ALL_APPS_UNINSTALL_HOME_VIEW

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that after uninstalling all installed apps, the RDK UI Home screen displays only two rows -- Recommended Apps and Video on Demand.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully. |
| 2 | Ensure multiple apps are installed | Ensure multiple apps are already installed on the DUT and listed under My Apps. | Multiple apps should be installed and visible in the My Apps section. |
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access. |
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Open App Info page | Navigate to App Info icon in left side of the RDK UI Home screen and press on it | App Info page should launch which should display the installed app's Info. Each row in App Info page displays the details of a specific application -- including the app icon, app name, app version,<br>runtime package version, and three management option -- Launch, Update, and Uninstall |
| 2 | Click Uninstall button for an app | Click on Uninstall button against an app | Confirmation message should ask if we want to do the action |
| 3 | Click OK/Confirm button | Click on OK button | A loading/buffering icon should come and uninstall should be done. After some time, uninstall operation should be completed and the row for the uninstalled app should be removed from App Info page |
| 4 | Repeat uninstall for all remaining apps | Repeat Steps 2 and 3 for all other apps | Expected results should be same as steps 2 and 3. After the last app's uninstallation, the page should display an informational message stating 'No Apps installed' |
| 5 | Exit message and verify Home screen layout | Exit the error message and navigate to Home screen and Validate if all installed Apps are removed | the My Apps row should no longer be visible in home screen. The home page of the UI should have only two rows - Recommended Apps and Video on Demand. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
