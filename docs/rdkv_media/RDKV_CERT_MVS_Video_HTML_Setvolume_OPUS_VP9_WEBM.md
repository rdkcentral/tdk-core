## TestCase ID
RDKV_Media_Validation_929
## TestCase Name
RDKV_CERT_MVS_Video_HTML_Setvolume_OPUS_VP9_WEBM
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test script to launch an HTML video player application via AppManager and perform volume level operation on webm content with Opus and Vp9 codecs for a few minutes and then close the player.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
|1| WPE Framework Running | Wpeframework process should be up and running in the device.| Wpeframework process is active and running on the device.|
|2| Html Player BOLT App Available | HTML Player BOLT app package must be available for download via AppManager. MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL (e.g. http://<TM_IP>:<port>/images/signed-packages/). MediaValidationVariables.html_player_app_download_url is derived from this base path and must resolve to the BOLT app package (e.g. http://<TM_IP>:<port>/images/signed-packages/com.rdkcentral.html-player+0.1.0.bolt).| BOLT app package is available and accessible for download via AppManager.|
|3| Close Interval Configured | MediaValidationVariables.close_interval should be set to the close interval value (in seconds).| MediaValidationVariables.close_interval is configured with the required value.|
|4| AppManager App Installation Check | AppManager should check if the BOLT app is already installed using `org.rdk.PackageManagerRDKEMS.1.listPackages`. If already present, proceed without download/install. If not present, download the BOLT app package via `org.rdk.DownloadManager.1.download` (params: `{"url":"<app_download_url>"}`) and install it via `org.rdk.PackageManagerRDKEMS.install` (params: `{"packageId":"<app_id>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<file_locator>"}`).| BOLT app is installed successfully on the device.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure Playback Operations and Test URL | Set playback operations: Set volume (5s), close the player. Build the test URL with the video_src_url_direct_webm. Store the constructed URL in PersistentStore for AppManager launch. | Verify that playback operations are configured correctly: Set volume (5s), close the player. Confirm the test URL is built with video_src_url_direct_webm. Confirm the URL is stored in PersistentStore (MVS/lightningURL) successfully. |
| 2 | Launch Player App via RDKShell | Launch the WebKit instance with the HTML player test app using the video source URL, and perform volume level operations. | Step executed successfully. |
| 3 | Perform Play Content and Validate Media Events | App performs the provided operations and validates each operation using media events ('Observed Event: play') | Verify that the app performs all configured operations and validates them using media events. Operations should complete successfully without errors. |
| 4 | Update Test Result Based on Event Validation | If expected event ('Observed Event: play') is observed for each operation, app gives the validation result as SUCCESS or else FAILURE. Update the test script result as SUCCESS/FAILURE based on event validation result and proc check status (if applicable) | Check that the test result is updated as SUCCESS/FAILURE based on event validation result. |
| 5 | Terminate App and Revert Test Settings | Terminate the test app via AppManager (org.rdk.AppManager.1.terminateApp (appId: com.rdkcentral.html-player)) and restore the test environment.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"com.rdkcentral.html-player"}}'` | Ensure the test environment is restored successfully. Verify that the app (com.rdkcentral.html-player) is terminated via org.rdk.AppManager.1.terminateApp. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M143<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>