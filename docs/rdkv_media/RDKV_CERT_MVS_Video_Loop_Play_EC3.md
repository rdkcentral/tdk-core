## TestCase ID
RDKV_MEDIA_708
## TestCase Name
RDKV_CERT_MVS_Video_Loop_Play_EC3
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To launch a Video Player integrated with lightning application via AppManager and perform video loop playback of DASH EC3 codec content. The test confirms that the video loops seamlessly when it reaches the end of the stream, restarting from the beginning without user intervention. The expected number of loop cycles is validated within the configured observation duration.

<a name="head.Precondition"></a>
## Preconditions
|#| Step Name | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that the WPEFramework process is running on the device. | WPEFramework process should be up and running in the device. | WPEFramework should be active and running on the device. |
| 2 | Verify that the BOLT package host path is configured correctly. | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL.<br>(E.g. `http://<TM_IP>:<port>/images/signed-packages/`) | Ensure that the BOLT package host path is configured and accessible. |
| 3 | Verify that the BOLT app download URL resolves correctly. | MediaValidationVariables.unified_player_app_download_url is derived from the base path and must resolve to the BOLT app package URL. | Ensure that the BOLT app package URL is valid and accessible for download. |
| 4 | Verify that the stream variable is configured correctly. | Stream variable `video_src_url_short_duration_ec3` must be defined in `MediaValidationVariables.py` as `test_streams_base_path + "DASH_H264_EC3_30Sec/master.mpd"`, providing the test stream used for playback testing. | Verify that `video_src_url_short_duration_ec3` resolves to a valid, accessible stream location for this test. |
| 5 | Check whether the app is already installed on the device. | Query the installed package list using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}</code>. | Verify that the app is installed on the device. |
| 6 | Download the app package when it is not already available. | If the app is not installed, then download the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>"}}</code>. | Ensure that the app package is downloaded successfully. |
| 7 | Install the downloaded app package through PackageManager. | Install the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.lightning-unified-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}</code>. | Confirm that the app package is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps
|#| Step Name | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Set playback operations for the scenario. | Configure the `checkloop(60)` operations: the video will loop continuously for 60 seconds. The loop count is calculated from how many times the video repeats within that duration (e.g., a 15-second video looping for 60 seconds = 4 loops). | Ensure playback operations are set as specified. |
| 2 | Store the launch URL in PersistentStore. | Store the constructed URL in PersistentStore for AppManager launch. <br>Sample URL: `http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/unifiedplayer/build/index.html?url=<video_src_url_short_duration_ec3>&operations=checkloop(60)&autotest=true` | Ensure that the launch URL is stored in PersistentStore. |
| 3 | Launch the app through AppManager. | Launch the test app through AppManager using the URL stored in PersistentStore using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.launchApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code>. | Ensure that the app launches successfully via AppManager. |
| 4 | Check loaded apps and verify app presence. | Check whether the app is listed in loaded apps using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}</code>. | Verify that com.rdkcentral.lightning-unified-player is present in the loaded apps list. |
| 5 | Run loop playback and capture media events. | The player opens a short-duration stream with looping enabled. A **play** event confirms that playback has started. The video position is monitored, and when it resets to the beginning, it indicates a loop has occurred. The app counts the number of loops that happen within the configured duration and validates that the expected loop count is reached. | Ensure that the video loop and playback events are captured for the configured duration. |
| 6 | Validate observed events for the loop playback operation and update test result. | If a **play** event fires and the expected number of video loops is detected within the configured duration, the app reports SUCCESS, otherwise FAILURE. The test result is updated as SUCCESS or FAILURE based on event validation and process check status. | Ensure that the test result is updated as SUCCESS or FAILURE based on the loop playback event validation and proc check status. |
| 7 | Terminate app and restore test environment. | Terminate the test app through AppManager using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.terminateApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code> and restore the test environment. | Ensure that the app is terminated and the test environment is restored. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models**: RPI-Client, Video_Accelerator

**Estimated duration**: 5 mins

**Priority**: High

**Release Version**: M139<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>