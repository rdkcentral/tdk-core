## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_04
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_Amz_ClearData_Reboot

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the logged-out state of the Amazon Prime Video application persists across a DUT power cycle after an app data clear operation. This test confirms that the application data remains cleared after reboot and the application continues to function correctly, ensuring the durability of app data management for certification.

<a name="head.Precondition"></a>
## Preconditions

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pair Bluetooth remote | Ensure the Bluetooth Remote is paired and connected to the DUT. | The Bluetooth Remote should be paired and connected to the DUT successfully.|
| 2 | Connect DUT to network | Connect the DUT to Ethernet or Wi-Fi with active internet access. | The DUT should be connected to the network with active internet access.|
| 3 | Connect DUT to TV/display via HDMI | Connect the DUT to a TV or display and select the correct HDMI source. | The DUT should be connected to the TV/display and the correct HDMI source should be selected.|
| 4 | Install Amazon Prime app | If Amazon Prime Video is not already installed, select its tile from the Recommended Apps row of the RDK UI Home screen and press Enter/OK to install. Skip this step if it is already available in the My Apps section. | Amazon Prime Video should be installed and available in the My Apps section/row of the RDK UI Home screen. If already installed, this step may be skipped.|
| 5 | Sign in to Amazon Prime Video | Ensure Amazon Prime Video is logged in with valid user credentials on the DUT. | Amazon Prime Video should be signed in with valid user credentials on the DUT.|
| 6 | Verify playback in Amazon Prime Video | Launch Amazon Prime Video from the RDK UI Home screen and verify that audio and video playback is working correctly prior to test execution. | Amazon Prime Video should launch successfully and AV playback should be verified as working correctly prior to test execution.|

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Clear Amazon Prime app data via clearAppData API | Clear the Amazon Prime App data using the clearAppData API by executing below curl command  :<br>`curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 1, "method": "org.rdk.AppManager.clearAppData", "params": {"appId": "<Amazon App ID>"}}' http://127.0.0.1:9998/jsonrpc` | The `clearAppData` API should return a successful response, and the Amazon Prime App should be closed once the API execution is completed.|
| 2 | Relaunch Amazon Prime app after data clear | Launch Amazon Prime App again from the My Apps/Recommended Apps section/row of RDK UI Home screen and press Enter/OK on the remote | Amazon Prime App should be launched successfully (cold launch)|
| 3 | Validate Amazon Prime sign in page is loaded | Validate that Amazon Prime Sign in page is loaded or not | Amazon Prime App sign in page should be loaded|
| 4 | Close Amazon Prime app via Back key | Close/Exit the Amazon Prime App by back key press on remote. | Amazon Prime App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.|
| 5 | Reboot DUT and wait for bootup | Reboot the DUT and wait for Boot up | Device should be rebooted and RDK UI home page should be displayed on TV|
| 6 | Relaunch Amazon Prime app after data clear | Launch Amazon Prime App again from the My Apps/Recommended Apps section/row of RDK UI Home screen and press Enter/OK on the remote | Amazon Prime App should be launched successfully (cold launch)|
| 7 | Validate Amazon Prime sign in page is loaded | Validate that Amazon Prime Sign in page is loaded or not | Amazon Prime App sign in page should be loaded|
| 8 | Sign in to Amazon Prime and verify A/V playback | Sign in with a valid user credentials and Check the Amazon Prime App AV playback | Sign in should be successful and Amazon Prime App AV playback should happen as expected / without errors|
| 9 | Close Amazon Prime app via Back key | Close/Exit the Amazon Prime App by back key press on remote. | Amazon Prime App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

<div align="right"><sup><a href="#head.TOC">Go To Top</a></sup></div>
