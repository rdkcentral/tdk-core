## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_01
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_YT_ClearData_Active

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the user account login data for the YouTube application is cleared when the app is in a loaded (active) state on the DUT. This test confirms that the application terminates gracefully and the logged-out state is restored, ensuring that app data management works correctly for certification.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|
| 4 | Install YouTube app | If YouTube is not already installed, select its tile from the Recommended Apps row of the RDK UI Home screen and press Enter/OK to install. Skip this step if it is already available in the My Apps section. | YouTube should be installed and available in the My Apps section/row of the RDK UI Home screen. If already installed, this step may be skipped.|
| 5 | Sign in to YouTube | Ensure YouTube is logged in with valid user credentials on the DUT. | YouTube should be signed in with valid user credentials on the DUT.|
| 6 | Verify playback in YouTube | Launch YouTube from the RDK UI Home screen and verify that audio and video playback is working correctly prior to test execution. | YouTube should launch successfully and AV playback should be verified as working correctly prior to test execution.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Clear YouTube app data via clearAppData API | Clear the YouTube App data using the clearAppData API by executing below curl command  :<br>`curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 1, "method": "org.rdk.AppManager.clearAppData", "params": {"appId": "<YouTube App ID>"}}' http://127.0.0.1:9998/jsonrpc` | The `clearAppData` API should return a successful response, confirming that the YouTube App data has been cleared successfully.|
| 2 | Relaunch YouTube app after data clear | Launch YouTube App again from the My Apps/Recommended Apps section/row of RDK UI Home screen and press Enter/OK on the remote | YouTube App should be launched successfully (cold launch)|
| 3 | Validate that the "sign in" option is visible | Validate that the "Sign in" option is prominently visible in the sidebar or account menu, indicating no account is currently linked | "Sign in" option should be visible in the sidebar or account menu of YouTube App and no account should be linked|
| 4 | Sign in to YouTube and verify A/V playback | Sign in with a valid user credentials and Check the YouTube App AV playback | Sign in should be successful and YouTube App AV playback should happen as expected / without errors|
| 5 | Close YouTube app via Back key | Close/Exit the YouTube App by back key press on remote. | YouTube App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
