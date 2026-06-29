## TestCase ID
RDKV_Media_Validation_266
## TestCase Name
RDKV_CERT_MVS_Video_Play_Widevine_MultiKey_DASH
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a lightning Video player application via AppManager and perform video play operation of  widevine DRM protected multikey dash encryption stream for few minutes and close the player

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
|1| WPE Framework Running | Wpeframework process should be up and running in the device.| Wpeframework process is active and running on the device.|
|2| Unified Player BOLT App Available | Lightning Player BOLT app package must be available for download via AppManager. MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL (e.g. http://<TM_IP>:<port>/images/signed-packages/). MediaValidationVariables.unified_player_app_download_url is derived from this base path and must resolve to the BOLT app package (e.g. http://<TM_IP>:<port>/images/signed-packages/com.rdkcentral.lightning-unified-player+0.1.0.bolt).| BOLT app package is available and accessible for download via AppManager.|
|3| Close Interval Configured | MediaValidationVariables.close_interval should be set to the close interval value (in seconds).| MediaValidationVariables.close_interval is configured with the required value.|
|4| AppManager App Installation Check | AppManager should check if the BOLT app is already installed using `org.rdk.PackageManagerRDKEMS.1.listPackages`. If already present, proceed without download/install. If not present, download the BOLT app package via `org.rdk.DownloadManager.1.download` (params: `{"url":"<app_download_url>"}`) and install it via `org.rdk.PackageManagerRDKEMS.install` (params: `{"packageId":"<app_id>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<file_locator>"}`).| BOLT app is installed successfully on the device.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure Playback Operations and Test URL | Start playback of the content and close the player after the configured duration (close_interval). Build the test URL with the video_src_url_widevine_multikey_dash (DASH stream). Store the constructed URL in PersistentStore for AppManager launch. Sample URL (dashjs player):<br>`http://<TM_IP>:<port>/rdk-test-tool/fileStore/lightning-apps/unifiedplayer/build/index.html?player=sdk&url=http://<TM_IP>:<port>/TDK_Clear_Test_Streams_Sunrise/<video_src_url_widevine_multikey_dash>&operations=close&autotest=true&type=dash` | Verify that playback is configured to start content and close the player after the configured duration (close_interval). Confirm the test URL is built with video_src_url_widevine_multikey_dash. Confirm the URL is stored in PersistentStore (MVS/lightningURL) successfully. |
| 2 | Launch Player App via AppManager | Launch the test app via AppManager using the URL stored in PersistentStore.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.launchApp","params":{"appId":"com.rdkcentral.lightning-unified-player"}}'` | Ensure the app (com.rdkcentral.lightning-unified-player) is launched successfully and should be listed in the loaded apps. |
| 3 | Perform Play Content and Validate Media Events | App starts playing the widevine DRM protected cbcs dash stream video and closes the player after the provided duration. The 'playing' event is monitored to validate successful playback. | Verify that the app performs all configured operations without errors. The 'playing' event should be observed, confirming successful media playback. |
| 4 | Validate Event Result and Update Test Status | If expected event ('playing') is observed then update the result as SUCCESS or else FAILURE | Confirm that expected event ('playing') is observed. Check that the test result is updated as SUCCESS. |
| 5 | Update Test Result Based on Event Validation | Update the test script result as SUCCESS/FAILURE based on event validation result and proc check status (if applicable) | Check that the test result is updated as SUCCESS/FAILURE based on event validation result. |
| 6 | Terminate App and Revert Test Settings | Terminate the test app via AppManager (org.rdk.AppManager.1.terminateApp (appId: com.rdkcentral.lightning-unified-player)) and restore the test environment.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"com.rdkcentral.lightning-unified-player"}}'` | Ensure the test environment is restored successfully. Verify that the app (com.rdkcentral.lightning-unified-player) is terminated via org.rdk.AppManager.1.terminateApp. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M106<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>