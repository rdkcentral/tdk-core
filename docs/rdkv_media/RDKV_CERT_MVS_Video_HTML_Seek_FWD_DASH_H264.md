<!-- AUTO-INFERRED: This document was generated from Python code because no embedded XML metadata was found. Fields marked <TO_BE_UPDATED> must be reviewed and filled in. -->

## TestCase ID
<TO_BE_UPDATED>
## TestCase Name
RDKV_CERT_MVS_Video_HTML_Seek_FWD_DASH_H264
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test script to launch a HTML5 Player application via AppManager and perform seek forward of DASH content, validating the expected media events and player behaviour.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
|1| WPE Framework Running | Wpeframework process should be up and running in the device.| Wpeframework process is active and running on the device.|
|2| Html Player BOLT App Available | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL (e.g. http://<TM_IP>:<port>/images/signed-packages/). MediaValidationVariables.html_player_app_download_url is derived from this base path and must resolve to the HTML5 Player BOLT app package (e.g. http://<TM_IP>:<port>/images/signed-packages/com.rdkcentral.html-player+0.1.0.bolt).| BOLT app package is available and accessible for download via AppManager.|
|3| Seekbwd Interval Configured | MediaValidationVariables.seekbwd_interval should be set to the seek-backward interval value (in seconds).| MediaValidationVariables.seekbwd_interval is configured with the required value.|
|4| Seekbwd Check Interval Configured | MediaValidationVariables.seekbwd_check_interval should be set to the seek-backward check interval (in seconds).| MediaValidationVariables.seekbwd_check_interval is configured with the required value.|
|5| Close Interval Configured | MediaValidationVariables.close_interval should be set to the close interval value (in seconds).| MediaValidationVariables.close_interval is configured with the required value.|
|6| AppManager App Installation Check | AppManager should check if the BOLT app is already installed using `org.rdk.PackageManagerRDKEMS.1.listPackages`. If already present, proceed without download/install. If not present, download the BOLT app package via `org.rdk.DownloadManager.1.download` (params: `{"url":"<app_download_url>"}`) and install it via `org.rdk.PackageManagerRDKEMS.install` (params: `{"packageId":"<app_id>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<file_locator>"}`).| BOLT app is installed successfully on the device.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure Playback Operations and Test URL | Set playback operations: Seek forward (30s), close the player. Build the test URL with the video_src_url_dash. Store the constructed URL in PersistentStore for AppManager launch. | Verify that playback operations are configured correctly: Seek forward (30s), close the player. Confirm the test URL is built with video_src_url_dash. Confirm the URL is stored in PersistentStore (MVS/lightningURL) successfully. |
| 2 | Launch Player App via AppManager | Launch the test app via AppManager using the URL stored in PersistentStore.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.launchApp","params":{"appId":"com.rdkcentral.html-player"}}'` | Ensure the app (com.rdkcentral.html-player) is launched successfully and should be listed in the loaded apps. |
| 3 | Perform Play Content and Validate Media Events | App performs the configured operations and validates using media events. The 'playing' event is monitored to validate successful playback. | Verify that the app performs all configured operations without errors. The 'playing' event should be observed, confirming successful media playback. |
| 4 | Validate Event Result and Update Test Status | If expected event (Video Player Playing) is observed, app gives the validation result as SUCCESS or else FAILURE. | Confirm the expected event is observed. Check that the test result is updated as SUCCESS/FAILURE accordingly. |
| 5 | Update Test Result Based on Event Validation | Update the test script result as SUCCESS/FAILURE based on event validation result and proc check status (if applicable). | Check that the test result is updated as SUCCESS/FAILURE based on event validation result. |
| 6 | Terminate App and Revert Test Settings | Terminate the test app via AppManager (org.rdk.AppManager.1.terminateApp (appId: com.rdkcentral.html-player)) and restore the test environment.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"com.rdkcentral.html-player"}}'` | Ensure the test environment is restored successfully. Verify that the app (com.rdkcentral.html-player) is terminated via org.rdk.AppManager.1.terminateApp. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 7

**Priority** : High

**Release Version** : <TO_BE_UPDATED><div align="right"><sup>[Go To Top](#head.TOC)</sup></div>