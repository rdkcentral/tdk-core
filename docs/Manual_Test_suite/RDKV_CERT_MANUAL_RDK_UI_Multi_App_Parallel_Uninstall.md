## TestCase ID
RDKV_MANUAL_RDKUI_33
## TestCase Name
RDKV_CERT_MANUAL_RDK_UI_Multi_App_Parallel_Uninstall

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that multiple apps can be uninstalled sequentially from the App Info screen, and that all uninstalled apps are no longer listed in the My Apps section. This test exercises the RDK UI home screen, settings menus, and DAC App Manager navigation via Bluetooth remote key-press events to validate the targeted UI behaviour. The test confirms that it should not launch the app, as it is already uninstalled. It should try to download the app again.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Ensure multiple apps are installed | Ensure multiple apps are already installed on the DUT and listed under My Apps. | Multiple apps should be installed and visible in the My Apps section.|
| 3 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 4 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Open App Info page | Navigate to App Info icon in left side of the RDK UI Home screen and press on it | App Info page should launch which should display the installed app's Info. Each row in App Info page displays the details of a specific application -- including the app icon, app name, app version,<br>runtime package version, and three management option -- Launch, Update, and Uninstall|
| 2 | Click Uninstall button for an app | Click on Uninstall button against an app | In the App Info page, when the user clicks Uninstall, a confirmation dialog should appear asking the user to confirm the uninstall action.|
| 3 | Click Yes to confirm uninstall | Click on Yes button in confirmation message | A loading/buffering icon should come and uninstall should be done. After some time, uninstall operation should be completed and the row for the uninstalled app should be removed from App Info page|
| 4 | Repeat uninstall for additional apps | Repeat Steps 2 and 3 for some other apps too | Expected results should be same as steps 2 and 3|
| 5 | Press Home button to go to Home screen | Press Home Button from remote | The RDK UI Home screen should launch.|
| 6 | Verify all uninstalled apps removed from My Apps | Validate that the uninstalled Apps are removed from My Apps. | My Apps section should not list the uninstalled App|
| 7 | Navigate to More Apps page | Click on More Apps button from Recommended Apps section. | More Apps page should load where all apps available in App catalogue are visible|
| 8 | Verify uninstalled app triggers re-download | Click on the App tile of the uninstalled Apps | It should not launch the app, as it is already uninstalled. It should try to download the app again.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
