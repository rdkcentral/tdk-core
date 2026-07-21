## TestCase ID
RDKV_MANUAL_APPMGR_FUNC_15
## TestCase Name
RDKV_CERT_MANUAL_AppMgr_Fun_Deeplink_Launch

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that deeplink-supported applications can be launched with specific deeplink parameters via the AppManager on the DUT. This test confirms that each application launches to the expected content or state based on the provided deeplink arguments, ensuring that deeplink launch functionality is fully operational for certification.

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
| 1 | Get YouTube appId via getInstalledApps API | Execute below curl command to get the appId of the installed YouTube App from list :  <br>`curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 5, "method": "org.rdk.AppManager.getInstalledApps"}' http://127.0.0.1:9998/jsonrpc` | The `getInstalledApps` API should return a successful response containing the `appId` of the installed YouTube App (e.g., `com.rdkcentral.YouTube`) in the result list.|
| 2 | Launch YouTube app with deeplink via API | Execute the below curl command  to launch the YouTube app with deeplink using AppManager.1.launchApp API and LaunchArgs : <br>`curl -d '{ "jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.launchApp", "params": { "appId": "com.rdkcentral.YouTube", "intent": "<intent>", "launchArgs": "<deeplink videoID>" }}' http://127.0.0.1:9998/jsonrpc` | The `launchApp` API should return a successful response, and the YouTube App should launch with the specified deeplink `launchArgs`.|
| 3 | Verify YouTube plays deeplink video | Validate that YouTube started playback for the video ID in deeplink URL and verify the uninterrupted AV playback | YouTube App should launch and instantly play the video given in the deeplink URL and AV playback should be fine|
| 4 | Close YouTube app via Back key | Close/Exit the YouTube App by back key press on remote. | All YouTube App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.|
| 5 | Get Amazon Prime appId via getInstalledApps API | Execute below curl command to get the appId of the installed Amazon Prime App from list :  <br>`curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 5, "method": "org.rdk.AppManager.getInstalledApps"}' http://127.0.0.1:9998/jsonrpc` | The `getInstalledApps` API should return a successful response containing the `appId` of the installed Amazon Prime App (e.g., `com.rdkcentral.AmazonPrimeWidevine`) in the result list.|
| 6 | Launch Amazon Prime app with deeplink via API | Execute the below curl command  to launch the Amazon Prime app with deeplink using AppManager.1.launchApp API and LaunchArgs : <br>`curl -d '{ "jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.launchApp", "params": { "appId": "com.rdkcentral.AmazonPrimeWidevine", "intent": "<intent>", "launchArgs": "<deeplink videoID>" }}' http://127.0.0.1:9998/jsonrpc` | The `launchApp` API should return a successful response, and the Amazon Prime App should launch with the specified deeplink `launchArgs`.|
| 7 | Verify Amazon Prime plays deeplink video | Validate that Amazon Prime started playback for the video ID in deeplink URL and verify the uninterrupted AV playback | Amazon Prime App should launch and instantly play the video given in the deeplink URL and AV playback should be fine|
| 8 | Close/exit the Amazon Prime app | Close/Exit the Amazon Prime App by back key press on remote. | Amazon Prime App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display.|
| 9 | Repeat deeplink launch steps for all supported apps | Repeat steps 1 - 5 all other deeplink launch supported installed Apps from RDK UI Homepage | Expected response should be same as Step 1 - 5 on all supported Apps|

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
