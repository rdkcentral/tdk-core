## TestCase ID
RDKV_MEDIA_1053
## TestCase Name
RDKV_CERT_MVS_Video_Seek_FF_DASH_H264_Main
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To launch a Video Player integrated with lightning application via AppManager and perform seek forward, fast-forward, and resume playback of DASH H264 (Main Profile) content, validating the expected media events and player behaviour. The test confirms a combination of seek and fast-forward operations, validating that seeks reposition the video within the acceptable range and that fast-forward advances the video position at the expected increased rate.

<a name="head.Precondition"></a>
## Preconditions
|#| Step Name | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that the WPEFramework process is running on the device. | WPEFramework process should be up and running in the device. | WPEFramework should be active and running on the device. |
| 2 | Verify that the BOLT package host path is configured correctly. | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL.<br>(E.g. `http://<TM_IP>:<port>/images/signed-packages/`) | Ensure that the BOLT package host path is configured and accessible. |
| 3 | Verify that the BOLT app download URL resolves correctly. | MediaValidationVariables.unified_player_app_download_url is derived from the base path and must resolve to the BOLT app package URL. | Ensure that the BOLT app package URL is valid and accessible for download. |
| 4 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.fastfwd_check_interval should be set to the fast-forward check interval (in seconds). | Ensure that the required configuration value is set correctly. |
| 5 | Verify that the stream variable is configured correctly. | Stream variable `video_src_url_dash_h264_main` must be defined in `MediaValidationVariables.py` as `test_streams_base_path + "DASH_H264_AAC_Main/dash_h264_avc_aac_fmp4_main.mpd"`, providing the test stream used for playback testing. | Verify that `video_src_url_dash_h264_main` resolves to a valid, accessible stream location for this test. |
| 6 | Check whether the app is already installed on the device. | Query the installed package list using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}</code>. | Verify that the app is installed on the device. |
| 7 | Download the app package when it is not already available. | If the app is not installed, then download the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>"}}</code>. | Ensure that the app package is downloaded successfully. |
| 8 | Install the downloaded app package through PackageManager. | Install the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.lightning-unified-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}</code>. | Confirm that the app package is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps
|#| Step Name | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Set playback operations for the scenario. | Configure the `seekfwd(30),fastfwd(20),playnow(30)` operations: the video player will seek forward for 30 seconds, then fast-forward for 20 seconds, then resume playback for 30 seconds. | Ensure playback operations are set as specified. |
| 2 | Store the launch URL in PersistentStore. | Store the constructed URL in PersistentStore for AppManager launch. <br>Sample URL: `http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/unifiedplayer/build/index.html?url=<video_src_url_dash_h264_main>.mpd&operations=seekfwd(30),fastfwd(20),playnow(30)&autotest=true&type=dash` | Ensure that the launch URL is stored in PersistentStore. |
| 3 | Launch the app through AppManager. | Launch the test app through AppManager using the URL stored in PersistentStore using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.launchApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code>. | Ensure that the app launches successfully via AppManager. |
| 4 | Check loaded apps and verify app presence. | Check whether the app is listed in loaded apps using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}</code>. | Verify that com.rdkcentral.lightning-unified-player is present in the loaded apps list. |
| 5 | Execute seek and fast-forward operations and capture media events. | The player alternates between seek operations and fast-forward speed changes. For seek steps, a **seeking** event fires on the request and a **seeked** event fires on completion, with the resulting video position validated within the acceptable range of the seek target. For fast-forward steps, a **ratechange** event confirms the speed increase and the video position is monitored to verify faster-than-normal advancement. | Ensure that the expected media events are captured for the configured operations. |
| 6 | Validate observed events for the seek and fast-forward operation and update test result. | If the expected events fire for each operation — **seeking** and **seeked** events for seek steps with the video position within the acceptable range, and **ratechange** events for fast-forward steps with appropriate speed advancement — the app reports SUCCESS, otherwise FAILURE. The test result is updated as SUCCESS or FAILURE based on event validation and process check status. | Ensure that the test result is updated as SUCCESS or FAILURE based on the seek and **fast-forward** event validation and proc check status. |
| 7 | Terminate app and restore test environment. | Terminate the test app through AppManager using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.terminateApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code> and restore the test environment. | Ensure that the app is terminated and the test environment is restored. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models**: RPI-Client, Video_Accelerator

**Estimated duration**: 5 mins

**Priority**: High

**Release Version**: M144<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>