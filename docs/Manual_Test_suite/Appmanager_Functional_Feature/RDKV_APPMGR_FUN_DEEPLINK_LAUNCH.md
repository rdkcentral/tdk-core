## TestCase ID
RDKV_MANUAL_APPMGR_FUNCTIONAL_15
## TestCase Name
RDKV_CERT_MANUAL_APPMGR_FUN_DEEPLINK_LAUNCH

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the deeplink launch functionality on deeplink-supported installed applications via the AppManager API.

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
| 1 | Verify required apps are installed | Validate that required Apps is already Installed and available in the My Apps/Recommended Apps section/row of RDK UI Homepage. If required Apps are not installed follow the instructions of Pre condition 4 | Required Apps should be installed and Tile should be Available in My Apps/Recommended Apps section/row of RDK UI Homepage. |
| 2 | Get YouTube appId via getInstalledApps API | Execute below curl command to get the appId of the installed YouTube App from list :  <br>curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 5, "method": "org.rdk.AppManager.getInstalledApps"}' http://127.0.0.1:9998/jsonrpc | appId of the installed YouTube App should be available in the API response like below :<br>{"jsonrpc":"2.0","id":5,"result":[{"appId":"com.rdkcentral.base","versionString":"0.1.0","type":"INTERACTIVE_APP","lastActiveTime":"","lastActiveIndex":""},{"appId":"com.rdkcentral.cobalt","versionString":"0.1.0","type":"INTERACTIVE_APP","lastActiveTime":"","lastActiveIndex":""},{"appId":"com.rdkcentral.refui","versionString":"0.0.4","type":"INTERACTIVE_APP","lastActiveTime":"03\/25\/26 11:06:24.264463768","lastActiveIndex":1},{"appId":"com.rdkcentral.wpe-rdk","versionString":"0.1.0","type":"INTERACTIVE_APP","lastActiveTime":"","lastActiveIndex":""},{"appId":"com.rdkcentral.youtube","versionString":"0.1.0","type":"INTERACTIVE_APP","lastActiveTime":"","lastActiveIndex":""}]} |
| 3 | Launch YouTube app with deeplink via API | Execute the below curl command  to launch the YouTube app with deeplink using AppManager.1.launchApp API and LaunchArgs : <br>curl -d '{ "jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.launchApp", "params": { "appId": "com.rdkcentral.youtube", "intent": "<intent>", "launchArgs": "<deeplink videoID>" }}' http://localhost:9998/jsonrpc | YouTube App should launch and play with deeplink url from launchArgs and Expected API Response should be like below : <br>{"jsonrpc":"2.0","id":2,"result":null} |
| 4 | Verify YouTube plays deeplink video | Validate that Youtube started playback for the video ID in deeplink URL and verify the uninterrupted AV playback | YouTube App should launch and instantly play the video given in the deeplink URL and AV playback should be fine |
| 5 | Close YouTube app via Back key | Close/Exit the YouTube App by back key press on remote. | All YouTube App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display. |
| 6 | Get Amazon Prime appId via getInstalledApps API | Execute below curl command to get the appId of the installed Amazon Prime App from list :  <br>curl -H 'content-type:text/plain;' --data-binary '{"jsonrpc": 2.0, "id": 5, "method": "org.rdk.AppManager.getInstalledApps"}' http://127.0.0.1:9998/jsonrpc | appId of the installed Amazon Prime App should be available in the API response like below :<br>{"jsonrpc":"2.0","id":5,"result":[{"appId":"com.rdkcentral.AmazonPrimeWidevine","versionString":"0.1.0","type":"INTERACTIVE_APP","lastActiveTime":"","lastActiveIndex":""},{"appId":"com.rdkcentral.base","versionString":"0.1.0","type":"INTERACTIVE_APP","lastActiveTime":"","lastActiveIndex":""},{"appId":"com.rdkcentral.cobalt","versionString":"0.1.0","type":"INTERACTIVE_APP","lastActiveTime":"","lastActiveIndex":""},{"appId":"com.rdkcentral.refui","versionString":"0.0.4","type":"INTERACTIVE_APP","lastActiveTime":"03\/25\/26 11:06:24.264463768","lastActiveIndex":1},{"appId":"com.rdkcentral.wpe-rdk","versionString":"0.1.0","type":"INTERACTIVE_APP","lastActiveTime":"","lastActiveIndex":""},{"appId":"com.rdkcentral.youtube","versionString":"0.1.0","type":"INTERACTIVE_APP","lastActiveTime":"","lastActiveIndex":""}]} |
| 7 | Launch Amazon Prime app with deeplink via API | Execute the below curl command  to launch the Amazon Prime app with deeplink using AppManager.1.launchApp API and LaunchArgs : <br>curl -d '{ "jsonrpc": "2.0", "id": 2, "method": "org.rdk.AppManager.launchApp", "params": { "appId": "com.rdkcentral.AmazonPrimeWidevine", "intent": "<intent>", "launchArgs": "<deeplink videoID>" }}' http://localhost:9998/jsonrpc | Amazon Prime App should launch and play with deeplink url from launchArgs and Expected API Response should be like below : <br>{"jsonrpc":"2.0","id":2,"result":null} |
| 8 | Verify Amazon Prime plays deeplink video | Validate that Amazon Prime started playback for the video ID in deeplink URL and verify the uninterrupted AV playback | Amazon Prime App should launch and instantly play the video given in the deeplink URL and AV playback should be fine |
| 9 | Close/exit the amazon prime apps by | Close/Exit the Amazon Prime Apps by back key press on remote. | Amazon Prime App should be terminated/ Closed gracefully and the RDK UI Home screen should be visible on the display. |
| 10 | Repeat deeplink launch steps for all supported apps | Repeat steps 1 - 5 all other deeplink launch supported installed Apps from RDK UI Homepage | Expected response should be same as Step 1 - 5 on all supported Apps |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
