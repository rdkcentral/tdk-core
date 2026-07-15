## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_03
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_Yt_ClearData_Reboot

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that after a clearAppData operation on the YouTube application, the logged-out state persists across a DUT power cycle and that the application remains functional. This test exercises the `org.rdk.AppManager` plugin (including APIs such as `clearAppData`, `launchApp`, and `getAppStatus`) and the RDK UI Home screen navigation to drive the application lifecycle. The test confirms that youTube App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.

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
| 1 | Select youtube app tile from the | Select YouTube App tile from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | YouTube App should be launched successfully  (Either cold launch /hot launch based on the app's previous state) |
| 2 | Select video and initiate YouTube playback | Select any Video Content from YouTube App and start playback | Selected Video Content AV playback should start |
| 3 | Clear YouTube app data via clearAppData API | Clear the YouTube App data using the clearAppData API by executing below curl command  :<br>`curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 1, "method": "org.rdk.AppManager.clearAppData", "params": {"appId": "<YouTube App ID>"}}' http://127.0.0.1:9998/jsonrpc` | Expected response should be like below :<br>{"jsonrpc":"2.0","id":1,"result":null} |
| 4 | Relaunch YouTube app after data clear | Launch Youtube App again from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | YouTube App should be launched successfully (cold launch) |
| 5 | Validate that the "sign in" option | Validate that the "Sign in" option is prominently visible in the sidebar or account menu, indicating no account is currently linked | "Sign in" option should be visible in the sidebar or account menu of Youtube App and no account should be linked |
| 6 | Close YouTube app via Back key | Close/Exit the YouTube App by back key press on remote. | YouTube App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display. |
| 7 | Reboot DUT and wait for bootup | Reboot the DUT and wait for Boot up | Device should be rebooted and RDK UI home page should be displayed on TV |
| 8 | Relaunch YouTube app after data clear | Launch Youtube App again from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | YouTube App should be launched successfully (cold launch mostly beacuse after reboot ) |
| 9 | Validate that the "sign in" option | Validate that the "Sign in" option is prominently visible in the sidebar or account menu, indicating no account is currently linked | "Sign in" option should be visible in the sidebar or account menu of Youtube App and no account should be linked |
| 10 | Sign in to YouTube and verify A/V playback | Sign in with a valid user credentials and Check the YouTube App AV playback | Sign in should be successful and YouTube App AV playback should happen as expected / without errors |
| 11 | Close YouTube app via Back key | Close/Exit the YouTube App by back key press on remote. | YouTube App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
