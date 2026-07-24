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
To validate that user account logins for all installed applications are simultaneously cleared using the bulk app data management capability on the DUT. This test confirms that all applications reflect a logged-out state after the operation, ensuring that bulk app data management functions correctly for certification and user privacy compliance.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|
| 4 | Install YouTube app | If YouTube is not already installed, select the YouTube tile from the Recommended Apps row (or the More Apps tab if not visible) of the RDK UI Home screen and press Enter/OK to install it. Skip this step if YouTube is already available in the My Apps section. | YouTube should be installed and available in the My Apps section/row of the RDK UI Home screen, ready to launch. If already installed, this step may be skipped.|
| 5 | Install Amazon Prime app | If Amazon Prime Video is not already installed, select the Amazon Prime Video tile from the Recommended Apps row (or the More Apps tab if not visible) of the RDK UI Home screen and press Enter/OK to install it. Skip this step if Amazon Prime Video is already available in the My Apps section. | Amazon Prime Video should be installed and available in the My Apps section/row of the RDK UI Home screen, ready to launch. If already installed, this step may be skipped.|
| 6 | Install other login-required apps | If any other apps that require a user login are not already installed, select their tile from the Recommended Apps row (or the More Apps tab if not visible) of the RDK UI Home screen and press Enter/OK to install them. Skip this step for apps already available in the My Apps section. | All other login-required apps should be installed and available in the My Apps section/row of the RDK UI Home screen. If already installed, this step may be skipped.|
| 7 | Log in to YouTube | Launch YouTube from the RDK UI Home screen and sign in with valid user credentials. | YouTube should accept the login credentials and the user should be signed in successfully.|
| 8 | Log in to Amazon Prime | Launch Amazon Prime Video from the RDK UI Home screen and sign in with valid user credentials. | Amazon Prime Video should accept the login credentials and the user should be signed in successfully.|
| 9 | Log in to other login-required apps | Launch each other login-required app from the RDK UI Home screen and sign in with valid user credentials. | All other login-required apps should accept the login credentials and the user should be signed in successfully in each app.|
| 10 | Verify app launch and AV playback | Verify that YouTube, Amazon Prime Video, and all other login-required apps launch successfully from the RDK UI Home screen and that audio and video playback is working correctly in each app prior to test execution. | YouTube, Amazon Prime Video, and all other login-required apps should launch successfully and AV playback should be verified as working correctly prior to test execution.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Clear all installed app data via clearAllAppData API | Clear all the installed App data using the clearAllAppData API by executing below curl command  :<br>`curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 0, "method": "org.rdk.AppManager.clearAllAppData"}' http://127.0.0.1:9998/jsonrpc` | The `clearAllAppData` API should return a successful response, confirming that all installed app data has been cleared.|
| 2 | Launch all installed apps one by one | Launch all the installed Apps one by one from the My Apps/Recommended Apps section/row of RDK UI Home screen and press Enter/OK on the remote | All the installed Apps should be launched successfully (cold launch)|
| 3 | Validate all apps show sign in page | Validate that All the Apps have Sign in page is loaded or not | All installed Apps sign in page should be loaded indicating successful clear data on all apps|
| 4 | Sign in to all apps and verify A/V playback | Sign in with a valid user credentials and Check the AV playback of all tha Apps | Sign in should be successful and App AV playback should happen as expected / without errors on all the Apps|
| 5 | Close apps via Back key | Close/Exit the Apps by back key press on remote. | All Apps should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
