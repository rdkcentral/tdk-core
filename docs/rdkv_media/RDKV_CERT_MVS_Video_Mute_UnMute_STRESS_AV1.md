## TestCase ID
RDKV_Media_Validation_230
## TestCase Name
RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_AV1
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a lightning Video player application via AppManager to play AV1 video codec content and perform mute, unmute operations repeatedly for given number of times

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | WPE Framework Running | Wpeframework process should be up and running in the device. | Ensure that Wpeframework process is active and running on the device. |
| 2 | Unified Player BOLT App Available | Lightning Player BOLT app package must be available for download via AppManager.<br>MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages<br>hosting server URL (e.g. http://<TM_IP>:<port>/images/signed-packages/).<br>MediaValidationVariables.unified_player_app_download_url is derived from this base path and<br>must resolve to the BOLT app package (e.g.<br>http://<TM_IP>:<port>/images/signed-packages/com.rdkcentral.lightning-unified-player+0.1.0.bolt<br>. | Ensure that BOLT app package is available and accessible for download via AppManager. |
| 3 | Operation Max Interval Configured | MediaValidationVariables.operation_max_interval should be set to the maximum operation interval<br>value (in seconds). | Ensure that MediaValidationVariables.operation_max_interval is configured with the required<br>value. |
| 4 | Repeat Count Stress Configured | MediaValidationVariables.repeat_count_stress should be set to the repeat count for stress<br>tests. | Ensure that MediaValidationVariables.repeat_count_stress is configured with the required value. |
| 5 | AV1 URL Type Configured | MediaValidationVariables.av1_url_type should be set to the AV1 stream type value. | Ensure that MediaValidationVariables.av1_url_type is configured with the required value. |
| 6 | AppManager App Installation Check | AppManager should check if the BOLT app is already installed using :<br>List packages: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}`<br>If it is not already installed then download and install the BOLT package.<br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/unified-player-app"}}`<br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.lightning-unified-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | BOLT app is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure Playback Operations and Test URL | Set playback operations: Mute audio, unmute audio, repeat.<br>Build the test URL with the video_src_url_av1.<br>Store the constructed URL in PersistentStore for AppManager launch.<br>Sample URL (dashjs player):<br>`http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/unifiedplayer/build/index.html`<br>`?player=sdk`<br>`&url=http://<TM_IP>:<port>/TDK_Clear_Test_Streams_Sunrise/TDK_Asset_DASH_AV1_AAC/master.mpd`<br>`&operations=mute,unmute,repeat&autotest=true` | Ensure that playback operations are configured correctly: Mute audio, unmute audio, repeat.<br>Ensure the test URL is built with video_src_url_av1. Ensure the URL is stored in<br>PersistentStore (MVS/lightningURL) successfully. |
| 2 | Launch Player App via AppManager | Launch the test app via AppManager using the URL stored in PersistentStore.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.launchApp","params":{"appId":"com.rdkcentral.lightning-unified-player"}}'` | Ensure the app (com.rdkcentral.lightning-unified-player) is launched successfully and should be<br>listed in the loaded apps. |
| 3 | Perform Mute / Unmute and Validate Media Events | App performs the mute and unmute operations repeatedly and validates using events | Ensure that the mute and unmute operations repeatedly and validates using events completes<br>successfully without errors. |
| 4 | Validate Event Result and Update Test Status | If expected event volumechange occurs for mute and unmute operations in all the repetition,<br>then app gives the validation result as SUCCESS or else FAILURE | Ensure that expected event volumechange occurs for mute and unmute operations in all the<br>repetition. Ensure that the test result is updated as SUCCESS. |
| 5 | Update Test Result Based on Event Validation | Update the test script result as SUCCESS/FAILURE based on event validation result from the app<br>and proc check status (if applicable) | Ensure that the test result is updated as SUCCESS/FAILURE based on event validation result. |
| 6 | Terminate App and Revert Test Settings | Terminate the test app via AppManager (org.rdk.AppManager.1.terminateApp (appId:com.rdkcentral.lightning-unified-player)) and restore the test environment.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"com.rdkcentral.lightning-unified-player"}}'` | Ensure the test environment is restored successfully. Ensure that the app<br>(com.rdkcentral.lightning-unified-player) is terminated via org.rdk.AppManager.1.terminateApp. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M103<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>