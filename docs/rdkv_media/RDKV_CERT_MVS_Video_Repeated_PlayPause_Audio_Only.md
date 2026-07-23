## TestCase ID
RDKV_MEDIA_169
## TestCase Name
RDKV_CERT_MVS_Video_Repeated_PlayPause_Audio_Only
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To launch a Video Player integrated with lightning application via AppManager and perform play pause operations of Audio only stream continuously for given number of times. The test confirms that the video pauses correctly, with the video position remaining stationary during the pause interval, and that playback resumes normally with the video position advancing at the expected rate after resume.

<a name="head.Precondition"></a>
## Preconditions
|#| Step Name | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that the WPEFramework process is running on the device. | WPEFramework process should be up and running in the device. | WPEFramework should be active and running on the device. |
| 2 | Verify that the BOLT package host path is configured correctly. | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL.<br>(E.g. `http://<TM_IP>:<port>/images/signed-packages/`) | Ensure that the BOLT package host path is configured and accessible. |
| 3 | Verify that the BOLT app download URL resolves correctly. | MediaValidationVariables.unified_player_app_download_url is derived from the base path and must resolve to the BOLT app package URL. | Ensure that the BOLT app package URL is valid and accessible for download. |
| 4 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.pause_interval_stress should be set to the pause interval value for repeated tests (in seconds). | Ensure that the required configuration value is set correctly. |
| 5 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.play_interval_stress should be set to the play interval value for repeated tests (in seconds). | Ensure that the required configuration value is set correctly. |
| 6 | Verify that the required configuration is set correctly. | MediaValidationVariables.repeat_count_stress should be set to the repeat count for repeated tests. | Verify that MediaValidationVariables.repeat_count_stress is configured with the required value. |
| 7 | Verify that the stream variable is configured correctly. | Stream variable `video_src_url_audio` must be defined in `MediaValidationVariables.py` as `test_streams_base_path + "DASH_AAC_Audio_Only/master.mpd"`, providing the test stream used for playback testing. | Verify that `video_src_url_audio` resolves to a valid, accessible stream location for this test. |
| 8 | Check whether the app is already installed on the device. | Query the installed package list using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}</code>. | Verify that the app is installed on the device. |
| 9 | Download the app package when it is not already available. | If the app is not installed, then download the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>"}}</code>. | Ensure that the app package is downloaded successfully. |
| 10 | Install the downloaded app package through PackageManager. | Install the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.lightning-unified-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}</code>. | Confirm that the app package is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps
|#| Step Name | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Set playback operations for the scenario. | Configure the `pause(10),play(10),repeat(10)` operations: the video player will play for 10 seconds and then pause the video, then keep paused for 10 seconds and then resume playback, then repeat the preceding operations 10 times. | Ensure playback operations are set as specified. |
| 2 | Store the launch URL in PersistentStore. | Store the constructed URL in PersistentStore for AppManager launch. <br>Sample URL: `http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/unifiedplayer/build/index.html?url=<video_src_url_audio>&operations=pause(10),play(10),repeat(10)&autotest=true` | Ensure that the launch URL is stored in PersistentStore. |
| 3 | Launch the app through AppManager. | Launch the test app through AppManager using the URL stored in PersistentStore using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.launchApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code>. | Ensure that the app launches successfully via AppManager. |
| 4 | Check loaded apps and verify app presence. | Check whether the app is listed in loaded apps using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}</code>. | Verify that com.rdkcentral.lightning-unified-player is present in the loaded apps list. |
| 5 | Execute play and pause operations and capture media events. | After initial playback, the player pauses the video. A **paused** event confirms the video has stopped. During the pause interval, the video position is monitored to confirm it does not advance. The player then resumes playback, and a **play** event confirms the video has resumed. The video position is confirmed to advance again at the normal rate after resumption. | Ensure that the **play** and **pause** events are captured for the configured operations. |
| 6 | Validate observed events for the play and pause operation and update test result. | If the video pauses successfully with no position advancement during the pause interval, and then resumes playing with the position advancing at the normal rate, the app reports SUCCESS, otherwise FAILURE. The test result is updated as SUCCESS or FAILURE based on event validation and process check status. | Ensure that the test result is updated as SUCCESS or FAILURE based on the **play** and **pause** event validation and proc check status. |
| 7 | Terminate app and restore test environment. | Terminate the test app through AppManager using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.terminateApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code> and restore the test environment. | Ensure that the app is terminated and the test environment is restored. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models**: RPI-Client, Video_Accelerator

**Estimated duration**: 10 mins

**Priority**: High

**Release Version**: M94<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>