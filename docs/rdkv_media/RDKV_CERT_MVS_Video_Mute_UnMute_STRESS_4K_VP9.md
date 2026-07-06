## TestCase ID
RDKV_Media_Validation_473
## TestCase Name
RDKV_CERT_MVS_Video_Mute_UnMute_STRESS_4K_VP9
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
Test Script to launch a lightning Video player application through AppManager to play 4K VP9 video content and perform mute, unmute operations repeatedly for given number of times

<a name="head.Precondition"></a>
## Preconditions
|#| StepName | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that the WPEFramework process is running on the device. | WPEFramework process should be up and running in the device. | Ensure that WPEFramework should be active and running on the device. |
| 2 | Verify that the BOLT package host path is configured correctly. | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL.<br>(E.g. `http://<TM_IP>:/images/signed-packages/`) | Ensure that the BOLT package host path is configured and accessible. |
| 3 | Verify that the BOLT app download URL resolves correctly. | MediaValidationVariables.unified_player_app_download_url is derived from the base path and must resolve to the BOLT app package URL. | Ensure that the BOLT app package URL is valid and accessible for download. |
| 4 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.operation_max_interval should be set to the maximum operation interval value (in seconds). | Ensure that the required configuration value is set correctly. |
| 5 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.repeat_count_stress should be set to the repeat count for stress tests. | Ensure that the required configuration value is set correctly. |
| 6 | Verify that the required URL type configuration is set correctly. | MediaValidationVariables.vp9_4k_url_type should be set to the VP9 4K stream type value. | Ensure that the required URL type configuration should be set correctly. |
| 7 | Check whether the app is already installed on the device. | Query the installed package list using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}</code>. | Verify that the app is installed on the device. |
| 8 | Download the app package when it is not already available. | If the app is not installed, then download the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>"}}</code>. | Ensure that the app package is downloaded successfully. |
| 9 | Install the downloaded app package through PackageManager. | Install the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.lightning-unified-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}</code>. | Confirm that the app package is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#| StepName | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Set playback operations for the scenario. | Configure the `mute(5),unmute(5),repeat(15)` operations: the player will play the content for 5 seconds and then mute the audio, keep it muted for 5 seconds, then unmute, and repeat this mute/unmute cycle 15 times. | Ensure playback operations are set as specified. |
| 2 | Build the test URL using video_src_url_4k_vp9. | Build the test URL with the video_src_url_4k_vp9. | Verify that the test URL is built using video_src_url_4k_vp9. |
| 3 | Store the launch URL in PersistentStore. | Store the constructed URL in PersistentStore for AppManager launch. <br>Sample URL: `http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/unifiedplayer/build/index.html?url=<video_src_url_4k_vp9>.webm&operations=mute(5),unmute(5),repeat(15)&autotest=true&type=webm`| Ensure that the launch URL is stored in PersistentStore. |
| 4 | Launch the app through AppManager. | Launch the test app through AppManager using the URL stored in PersistentStore using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.launchApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code>. | Ensure that the app launches successfully via AppManager. |
| 5 | Check loaded apps and verify app presence. | Check whether the app is listed in loaded apps using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}</code>. | Verify that com.rdkcentral.lightning-unified-player is present in the loaded apps list. |
| 6 | Run mute/unmute operations and validate events. | App performs the mute and unmute operations repeatedly and validates using events. | Ensure that mute/unmute operations complete and expected events are observed. |
| 7 | Validate observed events and set pass/fail status. | If expected event volumechange occurs for mute and unmute operations in all the repetition, then the app reports SUCCESS; otherwise, it reports FAILURE. | Ensure that pass/fail status matches observed event validation. |
| 8 | Update test result based on validation. | Update the test script result as SUCCESS/FAILURE based on event validation result from the app and proc check status (if applicable). | Ensure that the final test result is updated based on validation and proc-check status. |
| 9 | Terminate app and restore test environment. | Terminate the test app through AppManager using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.terminateApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code> and restore the test environment. | Ensure that the app is terminated and the test environment is restored. |
<a name="head.Attributes"></a>
## Test Attributes

**Supported Models**: Video_Accelerator

**Estimated duration**: 10

**Priority**: High

**Release Version**: M130<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>



























