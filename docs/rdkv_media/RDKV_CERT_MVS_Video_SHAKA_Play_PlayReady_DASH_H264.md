## TestCase ID
RDKV_MEDIA_731
## TestCase Name
RDKV_CERT_MVS_Video_SHAKA_Play_PlayReady_DASH_H264
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To launch a Shaka Player integrated with lightning application via AppManager and perform video play operation of PlayReady DRM protected H264 codec DASH stream for few minutes and close the player. The test confirms that the stream opens and plays back successfully, that playback starts without errors, and that the video progresses continuously without stalls or interruptions for the configured duration before the player closes.

<a name="head.Precondition"></a>
## Preconditions
|#| Step Name | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that the WPEFramework process is running on the device. | WPEFramework process should be up and running in the device. | WPEFramework should be active and running on the device. |
| 2 | Verify that the BOLT package host path is configured correctly. | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL.<br>(E.g. `http://<TM_IP>:<port>/images/signed-packages/`) | Ensure that the BOLT package host path is configured and accessible. |
| 3 | Verify that the BOLT app download URL resolves correctly. | MediaValidationVariables.unified_player_app_download_url is derived from the base path and must resolve to the BOLT app package URL. | Ensure that the BOLT app package URL is valid and accessible for download. |
| 4 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.close_interval should be set to the close interval value (in seconds). | Ensure that the required configuration value is set correctly. |
| 5 | Verify that the stream variable is configured correctly. | Stream variable `video_src_url_playready_dash_h264` must be configured in `MediaValidationVariables.py` with the appropriate stream URL for this test. This variable is environment-specific and must be set to a valid, accessible URL before running the test. | Verify that `video_src_url_playready_dash_h264` is configured with a valid, accessible stream URL in `MediaValidationVariables.py`. |
| 6 | Verify that the DRM configuration is set correctly. | DRM configuration variable `video_src_url_playready_dash_h264_drmconfigs` must be configured in `MediaValidationVariables.py` with the PlayReady license server URL and any required HTTP headers. Use the format: `com.microsoft.playready[<license_url>]|headers[<header_name>:<header_value>]`. This variable is environment-specific and must be set before running the test. | Verify that `video_src_url_playready_dash_h264_drmconfigs` is configured with valid PlayReady DRM license server details in `MediaValidationVariables.py`. |
| 7 | Check whether the app is already installed on the device. | Query the installed package list using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}</code>. | Verify that the app is installed on the device. |
| 8 | Download the app package when it is not already available. | If the app is not installed, then download the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>"}}</code>. | Ensure that the app package is downloaded successfully. |
| 9 | Install the downloaded app package through PackageManager. | Install the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.lightning-unified-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}</code>. | Confirm that the app package is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps
|#| Step Name | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that PlayReady DRM is supported on the device. | Check the OCDM plugin status and activate it if not already active. Query the list of supported DRMs using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "OCDM.1.drms"}</code>. Verify that PlayReady is present in the returned DRM list. If PlayReady is not supported, the test is marked as Not Applicable and skipped. | PlayReady DRM must be supported on the device. If not supported, the test is marked as Not Applicable. |
| 2 | Set playback operations for the scenario. | Configure the `close(30)` operations: the video player will play the content for 30 seconds and automatically close the player. | Ensure playback operations are set as specified. |
| 3 | Store the launch URL in PersistentStore. | Store the constructed URL in PersistentStore for AppManager launch. <br>Sample URL: `http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/unifiedplayer/build/index.html?url=<video_src_url_playready_dash_h264>.mpd&operations=close(30)&autotest=true` | Ensure that the launch URL is stored in PersistentStore. |
| 4 | Launch the app through AppManager. | Launch the test app through AppManager using the URL stored in PersistentStore using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.launchApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code>. | Ensure that the app launches successfully via AppManager. |
| 5 | Check loaded apps and verify app presence. | Check whether the app is listed in loaded apps using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}</code>. | Verify that com.rdkcentral.lightning-unified-player is present in the loaded apps list. |
| 6 | Run video playback and capture media events. | The player opens the stream and starts playback. A **play** event confirms that the video has started. The video position is monitored during playback to confirm the content is advancing continuously without stalls or interruptions. The player closes automatically after the configured duration. | Ensure that the video playback events are captured for the configured duration. |
| 7 | Validate observed events for the video playback operation and update test result. | If playback starts successfully and the video position advances continuously throughout the configured duration without stalls or interruptions, the app reports SUCCESS, otherwise FAILURE. The test result is updated as SUCCESS or FAILURE based on event validation and process check status. | Ensure that the test result is updated as SUCCESS or FAILURE based on the video playback event validation and proc check status. |
| 8 | Terminate app and restore test environment. | Terminate the test app through AppManager using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.terminateApp", "params":{"appId": "com.rdkcentral.lightning-unified-player"}}</code> and restore the test environment. | Ensure that the app is terminated and the test environment is restored. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models**: Video_Accelerator

**Estimated duration**: 7 mins

**Priority**: High

**Release Version**: M140<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>