## TestCase ID
RDKV_Media_Validation_1077
## TestCase Name
RDKV_CERT_MVS_Video_PlayPause_STRESS_HEVC_Main10
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test script to launch a Lightning Unified Player application via AppManager and perform pause, play, and repeat playback of HEVC/H.265 content, validating the expected media events and player behaviour.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | WPE Framework Running | Wpeframework process should be up and running in the device. | Ensure that Wpeframework process is active and running on the device. |
| 2 | Unified Player BOLT App Available | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages<br>hosting server URL (e.g. http://<TM_IP>:<port>/images/signed-packages/).<br>MediaValidationVariables.unified_player_app_download_url is derived from this base path and<br>must resolve to the Lightning Unified Player BOLT app package (e.g.<br>http://<TM_IP>:<port>/images/signed-packages/com.rdkcentral.lightning-unified-player+0.1.0.bolt<br>. | Ensure that BOLT app package is available and accessible for download via AppManager. |
| 3 | Pause Interval Stress Configured | MediaValidationVariables.pause_interval_stress should be set to the pause interval value for<br>stress tests (in seconds). | Ensure that MediaValidationVariables.pause_interval_stress is configured with the required<br>value. |
| 4 | Play Interval Stress Configured | MediaValidationVariables.play_interval_stress should be set to the play interval value for<br>stress tests (in seconds). | Ensure that MediaValidationVariables.play_interval_stress is configured with the required<br>value. |
| 5 | Repeat Count Stress Configured | MediaValidationVariables.repeat_count_stress should be set to the repeat count for stress<br>tests. | Ensure that MediaValidationVariables.repeat_count_stress is configured with the required value. |
| 6 | HEVC URL Type Configured | MediaValidationVariables.hevc_url_type should be set to the HEVC stream type value. | Ensure that MediaValidationVariables.hevc_url_type is configured with the required value. |
| 7 | AppManager App Installation Check | AppManager should check if the BOLT app is already installed using :<br>List packages: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}`<br>If it is not already installed then download and install the BOLT package.<br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/unified-player-app"}}`<br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.lightning-unified-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | BOLT app is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure Playback Operations and Test URL | Set playback operations: Pause, play, repeat.<br>Build the test URL with the video_src_url_hevc_main10.<br>Store the constructed URL in PersistentStore for AppManager launch.<br>Sample URL (hlsjs player):<br>`http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/unifiedplayer/build/index.html`<br>`?player=sdk`<br>`&url=http://<TM_IP>:<port>/TDK_Clear_Test_Streams_Sunrise/DASH_HEVC_AAC_Main10/dash_hevc_aac_fmp4_main10.mpd`<br>`&operations=pause,play,repeat&autotest=true` | Ensure that playback operations are configured correctly: Pause, play, repeat. Ensure the test<br>URL is built with video_src_url_hevc_main10. Ensure the URL is stored in PersistentStore<br>(MVS/lightningURL) successfully. |
| 2 | Launch Player App via AppManager | Launch the test app via AppManager using the URL stored in PersistentStore.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.launchApp","params":{"appId":"com.rdkcentral.lightning-unified-player"}}'` | Ensure the app (com.rdkcentral.lightning-unified-player) is launched successfully and should be<br>listed in the loaded apps. |
| 3 | Perform Play Content and Validate Media Events | App performs the configured operations and validates using media events. The 'Observed Event:<br>play' event is monitored to validate successful playback. | Ensure that the app performs all configured operations and validates them using media events.<br>Operations should complete successfully without errors. |
| 4 | Validate Event Result and Update Test Status | If expected event (Observed Event: play) is observed, app gives the validation result as<br>SUCCESS or else FAILURE. | Ensure that the 'play' event is observed as expected. Ensure that the test result is<br>updated as SUCCESS/FAILURE accordingly. |
| 5 | Update Test Result Based on Event Validation | Update the test script result as SUCCESS/FAILURE based on event validation result and proc<br>check status (if applicable). | Ensure that the test result is updated as SUCCESS/FAILURE based on event validation result. |
| 6 | Terminate App and Revert Test Settings | Terminate the test app via AppManager (org.rdk.AppManager.1.terminateApp (appId:com.rdkcentral.lightning-unified-player)) and restore the test environment.<br>`curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"com.rdkcentral.lightning-unified-player"}}'` | Ensure the test environment is restored successfully. Ensure that the app<br>(com.rdkcentral.lightning-unified-player) is terminated via org.rdk.AppManager.1.terminateApp. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M145<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>