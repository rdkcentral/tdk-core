## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_06
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_Amz_ClearData_Idle

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the user account login for the Amazon Prime Video application is cleared when the clearAppData API is called even if the application has not been launched. This test exercises the `org.rdk.AppManager` plugin (including APIs such as `clearAppData`, `launchApp`, and `getAppStatus`) and the RDK UI Home screen navigation to drive the application lifecycle. The test confirms that amazon Prime App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|
| 4 | Install required apps if not present | If the required App is not already installed, select the App tile from the Recommended Apps row (or the More Apps tab if not visible on Recommended row) of the RDK UI Home screen and press Enter/OK to install it. Skip this step if the required App is already available in the My Apps section. | The required App should be installed and available in the My Apps section/row of the RDK UI Home screen, ready to launch. If already installed, this step may be skipped.|
| 5 | Launch Amazon Prime and sign in | Launch the Amazon Prime App from the My Apps section of the RDK UI Home screen and sign in with valid user credentials prior to test execution. Verify AV playback is working after sign-in. | Amazon Prime App should launch successfully and the user should be signed in with valid credentials. AV playback should be verified as working prior to test execution.|
| 6 | Verify app launch and AV playback | Verify that all required Apps are launching successfully from the RDK UI Home screen. For Apps that support A/V playback (regardless of whether the App is a Premium App or not), verify that audio and video playback is working correctly prior to test execution. | All required Apps should launch successfully from the RDK UI Home screen. For Apps supporting A/V playback, audio and video playback should be verified as working correctly prior to test execution.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Clear Amazon Prime app data via clearAppData API | Clear the Amazon Prime App data using the clearAppData API by executing below curl command  :<br>`curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 1, "method": "org.rdk.AppManager.clearAppData", "params": {"appId": "<Amazon App ID>"}}' http://127.0.0.1:9998/jsonrpc` | The `clearAppData` API should return a successful response, and the Amazon Prime App should be closed once the API execution is completed.|
| 2 | Launch Amazon Prime from My Apps | Launch Amazon Prime App from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Amazon Prime App should be launched successfully (cold launch)|
| 3 | Validate Amazon Prime sign in page is loaded | Validate that Amazon Prime Sign in page is loaded or not | Amazon Prime App sign in page should be loaded|
| 4 | Sign in to Amazon Prime and verify A/V playback | Sign in with a valid user credentials and Check the Amazon Prime App AV playback | Sign in should be successful and Amazon Prime App AV playback should happen as expected / without errors|
| 5 | Close Amazon Prime app via Back key | Close/Exit the Amazon Prime App by back key press on remote. | Amazon Prime App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
