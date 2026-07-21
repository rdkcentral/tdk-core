## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_22
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_App_Launch_Clear_Err

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that appropriate error messages are displayed when attempting to launch an application after its data has been cleared on the DUT. This test confirms that the application launch fails gracefully with a visible error notification, ensuring robust error handling behavior for AppManager certification.

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
| 3 | Delete app file from apps directory in DUT | In box ssh console, change directory to apps directory and delete the launched app file :<br>Eg : rm com.rdkcentral.YouTube | The app related file(eg:com.rdkcentral.YouTube) should be removed but App functionality or playback shouldn't get affected.|
| 4 | Close launched apps via Back key | Close/Exit the launched Apps by back key press on remote. | Launched App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.|
| 5 | Relaunch closed app from My Apps  | Relaunch closed app from My Apps  the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Selected App should not be launched since app files are removed and app launch failed error message should be displayed on RDK UI|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
