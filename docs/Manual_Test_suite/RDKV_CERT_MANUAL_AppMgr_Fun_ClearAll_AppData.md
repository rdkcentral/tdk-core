## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_07
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_ClearAll_AppData

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that user account logins for all installed applications (YouTube, Amazon Prime Video, Netflix, etc.) are cleared after the clearAllAppData API call. This test exercises the `org.rdk.AppManager` plugin (including APIs such as `clearAppData`, `launchApp`, and `getAppStatus`) and the RDK UI Home screen navigation to drive the application lifecycle. The test confirms that all Apps should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.

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
| 1 | Verify YouTube app is installed | Validate that YouTube App is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If YouTube is not installed follow the instructions of Precondition 4 | YouTube App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage.|
| 2 | Verify Amazon Prime app is installed | Validate that Amazon Prime App is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If Amazon Prime is not installed follow the instructions of Precondition 4 | Amazon Prime App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage.|
| 3 | Verify other user-login apps are installed | Validate that other Apps (User login required Apps) is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If Other Apps are not installed follow the instructions of Precondition 4 | Other App should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage.|
| 4 | Clear all installed app data via clearAllAppData API | Clear all the installed App data using the clearAllAppData API by executing below curl command  :<br>`curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 0, "method": "org.rdk.AppManager.clearAllAppData"}' http://127.0.0.1:9998/jsonrpc` | The `clearAllAppData` API should return a successful response, confirming that all installed app data has been cleared.|
| 5 | Launch all installed apps one by one | Launch all the installed Apps one by one from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | All the installed Apps should be launched successfully (cold launch)|
| 6 | Validate all apps show sign in page | Validate that All the Apps have Sign in page is loaded or not | All installed Apps sign in page should be loaded indicating successful clear data on all apps|
| 7 | Sign in to all apps and verify A/V playback | Sign in with a valid user credentials and Check the AV playback of all tha Apps | Sign in should be successful and App AV playback should happen as expected / without errors on all the Apps|
| 8 | Close apps via Back key | Close/Exit the Apps by back key press on remote. | All Apps should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
