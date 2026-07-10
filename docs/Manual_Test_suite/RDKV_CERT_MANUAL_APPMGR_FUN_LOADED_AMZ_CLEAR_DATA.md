## TestCase ID
RDKV_MANUAL_APPMGR_FUNCTIONAL_02
## TestCase Name
RDKV_CERT_MANUAL_APPMGR_FUN_LOADED_AMZ_CLEAR_DATA

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the user account login for the Amazon Prime Video application is cleared when the clearAppData API is called while the application is in a loaded state.

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
| 1 | Select amazon prime app tile from | Select Amazon Prime App tile from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Amazon Prime App should be launched succesfully  (Either cold launch /hot launch based on the app's previous state) |
| 2 | Select video and initiate Amazon Prime playback | Select any Video Content from Amazon Prime App and start playback | Selected Video Content AV playback should start |
| 3 | Clear Amazon Prime app data via clearAppData API | Clear the Amazon Prime App data using the clearAppData API by executing below curl command  :<br>curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 1, "method": "org.rdk.AppManager.clearAppData", "params": {"appId": "<Amazon App ID>"}}' http://127.0.0.1:9998/jsonrpc | Expected response should be like below :<br>{"jsonrpc":"2.0","id":1,"result":null}<br>And Amazon Prime app should be closed once clearAppData API execution is completed |
| 4 | Relaunch Amazon Prime app after data clear | Launch Amazon Prime App again from the My Apps/Recommended Apps section/row of RDK UI Homepage and press enter/Ok button on remote | Amazon Prime App should be launched succesfully (cold launch) |
| 5 | Validate Amazon Prime sign in page is loaded | Validate that Amazon Prime Sign in page is loaded or not | Amazon Prime App sign in page should be loaded |
| 6 | Sign in to Amazon Prime and verify A/V playback | Sign in with a valid user credentials and Check the Amazon Prime App AV playback | Sign in should be successful and Amazon Prime App AV playback should happen as expected / without errors |
| 7 | Close Amazon Prime app via Back key | Close/Exit the Amazon Prime App by back key press on remote. | Amazon Prime App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
