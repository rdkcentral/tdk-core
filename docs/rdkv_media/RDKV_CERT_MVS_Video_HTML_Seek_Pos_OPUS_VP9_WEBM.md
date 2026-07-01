## TestCase ID
RDKV_Media_Validation_917
## TestCase Name
RDKV_CERT_MVS_Video_HTML_Seek_Pos_OPUS_VP9_WEBM
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a HTML Video player application via AppManager and perform video seek position operation of webm content with Opus and VP9 codecs for few minutes and close the player

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | WPE Framework Running | Wpeframework process should be up and running in the device. | Ensure that Wpeframework process is active and running on the device. |
| 2 | Html Player BOLT App Available | HTML Player BOLT app package must be available for download via AppManager.<br>MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages<br>hosting server URL (e.g. http://<TM_IP>:<port>/images/signed-packages/).<br>MediaValidationVariables.html_player_app_download_url is derived from this base path and must<br>resolve to the BOLT app package (e.g.<br>http://<TM_IP>:<port>/images/signed-packages/com.rdkcentral.html-player+0.1.0.bolt). | Ensure that BOLT app package is available and accessible for download via AppManager. |
| 3 | Seekbwd Interval Configured | MediaValidationVariables.seekbwd_interval should be set to the seek-backward interval value (in<br>seconds). | Ensure that MediaValidationVariables.seekbwd_interval is configured with the required value. |
| 4 | Seekbwd Check Interval Configured | MediaValidationVariables.seekbwd_check_interval should be set to the seek-backward check<br>interval (in seconds). | Ensure that MediaValidationVariables.seekbwd_check_interval is configured with the required<br>value. |
| 5 | Close Interval Configured | MediaValidationVariables.close_interval should be set to the close interval value (in seconds). | Ensure that MediaValidationVariables.close_interval is configured with the required value. |
| 6 | AppManager App Installation Check | AppManager should check if the BOLT app is already installed using :<br>List packages: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}`<br>If it is not already installed then download and install the BOLT package.<br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/html-player-app"}}`<br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.html-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | BOLT app is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure Playback Operations and Test URL | Set playback operations: Seek forward (30s), seek backward (30s), close the player.<br>Build the test URL with the video_src_url_direct_webm.<br>Store the constructed URL in PersistentStore for AppManager launch. | Ensure that playback operations are configured correctly: Seek forward (30s), seek backward<br>(30s), close the player. Ensure the test URL is built with video_src_url_direct_webm. Ensure<br>the URL is stored in PersistentStore (MVS/lightningURL) successfully. |
| 2 | Launch Player App via AppManager | Launch the test app via AppManager using the URL stored in PersistentStore.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.launchApp","params":{"appId":"com.rdkcentral.html-player"}}'` | Ensure the app (com.rdkcentral.html-player) is launched successfully and should be listed in<br>the loaded apps. |
| 3 | Perform Play Content and Validate Media Events | App performs the provided operations and validates each operation using media events<br>('playing') | Ensure that the app performs all configured operations without errors. The 'playing' event<br>should be observed, confirming successful media playback. |
| 4 | Update Test Result Based on Event Validation | If expected event ('playing') is observed for each operation, app gives the validation result<br>as SUCCESS or else FAILURE. Update the test script result as SUCCESS/FAILURE based on event<br>validation result and proc check status (if applicable) | Ensure that the test result is updated as SUCCESS/FAILURE based on event validation result. |
| 5 | Terminate App and Revert Test Settings | Terminate the test app via AppManager (org.rdk.AppManager.1.terminateApp (appId:com.rdkcentral.html-player)) and restore the test environment.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"com.rdkcentral.html-player"}}'` | Ensure the test environment is restored successfully. Ensure that the app<br>(com.rdkcentral.html-player) is terminated via org.rdk.AppManager.1.terminateApp. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M143<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>