## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_17
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_App_Reinstall

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that previously uninstalled applications can be successfully reinstalled from the Recommended Apps or More Apps section of the RDK UI on the DUT. This test confirms that the reinstallation and subsequent launch complete successfully, ensuring that app management and installation workflows meet certification requirements.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|
| 4 | Install required apps if not present | If the required App is not already installed, select the App tile from the Recommended Apps row (or the More Apps tab if not visible on Recommended row) of the RDK UI Home screen and press Enter/OK to install it. Skip this step if the required App is already available in the My Apps section. | The required App should be installed and available in the My Apps section/row of the RDK UI Home screen, ready to launch. If already installed, this step may be skipped.|
| 5 | Sign in to premium apps if applicable | This step is applicable only if the required App is a Premium App (such as YouTube, Amazon Prime, or Netflix). If applicable, sign in with valid user credentials and verify AV playback prior to test execution. | If the required App is a Premium App, it should be signed in with valid user credentials and AV playback should be verified successfully prior to test execution.|
| 6 | Verify app launch and AV playback | Verify that all required Apps are launching successfully from the RDK UI Home screen. For Apps that support A/V playback (regardless of whether the App is a Premium App or not), verify that audio and video playback is working correctly prior to test execution. | All required Apps should launch successfully from the RDK UI Home screen. For Apps supporting A/V playback, audio and video playback should be verified as working correctly prior to test execution.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Launch app from Recommended/My Apps | Select the App tile from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Selected App should be launched successfully  (Either cold launch /hot launch based on the app's previous state)|
| 2 | Select content or load app | Select any Video Content from launched Apps or (load the App if its not a video App). | Selected Video Content AV playback should start or App should load its content|
| 3 | Close launched apps via Back key | Close/Exit the launched Apps by back key press on remote. | Launched App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.|
| 4 | Navigate to app info icon in | Navigate to App Info icon in left side of the RDK UI Home screen and press enter/Ok button on remote | "App Info page should launch where we should see the Installed app's Info. Each row in App Info page displays the details of a specific application -- including the app icon, app name, app version,<br>runtime package version, and three management option -- Launch, Update, and Uninstall"|
| 5 | Uninstall app via App Info page | Select Uninstall Button and press enter/Ok button on remote and again press enter on Yes option in the dialogue box to confirm Uninstall | In App Info page, when the user clicks Uninstall, a confirmation dialog YES or NO will appear to verify whether the user truly intends to remove the application. Upon Pressing YES A loading/buffering icon should come and uninstall should be done. After some time, uninstall operation should be completed and the row for the uninstalled app should be removed from App Info page|
| 6 | Press Home and verify uninstalled app removed from My Apps | Press Home Button from remote and Check, if the uninstalled App is removed from My Apps section. | RDK UI Homepage should be launched and My Apps section should not list the uninstalled App|
| 7 | Navigate to More Apps page | Select More Apps button from Recommended Apps section and press enter/Ok button on remote | More Apps page should load where all apps available in App catalogue are visible|
| 8 | Reinstall uninstalled app from More Apps | Select the App tile which has been uninstalled recently and press enter/Ok button on remote | Selected App should not launch instead It should start download that App and once installation is completed installed App should be listed under My App section or RDK UI Homepage|
| 9 | Launch reinstalled app from My Apps and play content | Select the App tile from the My Apps press enter/Ok button on remote and play any AV content | Selected App should be launched successfully  (Either cold launch /hot launch based on the app's previous state) and selected AV Content should play as expected / without errors|
| 10 | Close launched apps via Back key | Close/Exit the launched Apps by back key press on remote. | Launched App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.|
| 11 | Repeat steps for other apps from More Apps | Repeat steps 2 - 11 on other apps from more Apps after Installing it | Expected response should be same as Step 2 - 11|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
