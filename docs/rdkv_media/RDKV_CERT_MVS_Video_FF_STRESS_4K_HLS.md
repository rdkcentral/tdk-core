## TestCase ID
RDKV_MEDIA_454
## TestCase Name
RDKV_CERT_MVS_Video_FF_STRESS_4K_HLS
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To launch a Video Player integrated with lightning application via AppManager and perform video fast forward operation of 4k HLS content repeatedly for given number of times. The test confirms that the player can reliably alternate between fast-forward speed and normal playback speed across the configured number of repetitions, with consistent speed changes and correct position advancement throughout all stress iterations without any degradation.

<a name="head.Precondition"></a>
## Preconditions
|#| Step Name | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that the WPEFramework process is running on the device. | WPEFramework process should be up and running in the device. | WPEFramework should be active and running on the device. |
| 2 | Verify that the BOLT package host path is configured correctly. | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL.<br>(E.g. `http://<TM_IP>:<port>/images/signed-packages/`) | Ensure that the BOLT package host path is configured and accessible. |
| 3 | Verify that the BOLT app download URL resolves correctly. | MediaValidationVariables.unified_player_app_download_url is derived from the base path and must resolve to the BOLT app package URL. | Ensure that the BOLT app package URL is valid and accessible for download. |
| 4 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.fastfwd_check_interval should be set to the fast-forward check interval (in seconds). | Ensure that the required configuration value is set correctly. |
| 5 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.operation_max_interval should be set to the maximum operation interval value (in seconds). | Ensure that the required configuration value is set correctly. |
| 6 | Verify that the stream variable is configured correctly. | Stream variable `video_src_url_4k_hls` must be defined in `MediaValidationVariables.py` as `test_streams_base_path + "HLS_HEVC_AAC/master.m3u8"`, providing the test stream used for playback testing. | Verify that `video_src_url_4k_hls` resolves to a valid, accessible stream location for this test. |
| 7 | Check whether the app is already installed on the device. | Query the installed package list using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}</code>. | Verify that the app is installed on the device. |
| 8 | Download the app package when it is not already available. | If the app is not installed, then download the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>"}}</code>. | Ensure that the app package is downloaded successfully. |
| 9 | Install the downloaded app package through PackageManager. | Install the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.lightning-unified-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}</code>. | Confirm that the app package is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps
|#| Step Name | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Set playback operations for the scenario. | Configure the `fastfwd(10),repeat(3),playnow(10),repeat(1),fastfwd(10),repeat(3),playnow(10)` operations: the video player will fast-forward for 10 seconds, then repeat the preceding operations 3 times, then resume playback for 10 seconds, then repeat the preceding operations 1 time, then fast-forward for 10 seconds, then repeat the preceding operations 3 times, then resume playback for 10 seconds. | Ensure playback operations are set as specified. |
| 2 | Store the launch URL in PersistentStore. | Store the constructed URL in PersistentStore for AppManager launch. <br>Sample URL: `http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/unifiedplayer/build/index.html?url=<video_src_url_4k_hls>&operations=fastfwd(10),repeat(3),playnow(10),repeat(1),fastfwd(10),repeat(3),playnow(10)&autotest=true&type=hls` | Ensure that the launch URL is stored in PersistentStore. |
| 3 | Launch the app through AppManager. | Launch the test app through AppManager using the URL stored in PersistentStore using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.launchApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code>. | Ensure that the app launches successfully via AppManager. |
| 4 | Check loaded apps and verify app presence. | Check whether the app is listed in loaded apps using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}</code>. | Verify that com.rdkcentral.lightning-unified-player is present in the loaded apps list. |
| 5 | Execute fast-forward/rewind operations and capture media events. | The player repeatedly alternates between fast-forward speed and normal playback speed for the configured number of stress iterations. A **ratechange** event is expected for each speed change. The video position is monitored after each fast-forward segment to confirm consistent acceleration without degradation across all repetitions. | Ensure that the expected media events are captured for the configured operations. |
| 6 | Validate observed events for the fast-forward stress operation and update test result. | If **ratechange** events fire correctly for every fast-forward and normal speed resumption across all stress iterations, and the video position advances at the expected faster rate during each fast-forward segment, the app reports SUCCESS, otherwise FAILURE. The test result is updated as SUCCESS or FAILURE based on event validation and process check status. | Ensure that the test result is updated as SUCCESS or FAILURE based on the fast-forward stress event validation and proc check status. |
| 7 | Terminate app and restore test environment. | Terminate the test app through AppManager using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.terminateApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code> and restore the test environment. | Ensure that the app is terminated and the test environment is restored. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models**: Video_Accelerator

**Estimated duration**: 5 mins

**Priority**: High

**Release Version**: M128<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>