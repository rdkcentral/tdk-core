## TestCase ID
RDKV_MEDIA_688
## TestCase Name
RDKV_CERT_MVS_Video_HTML_Seek_BWD_VORBIS_VP8_WEBM
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To launch a HTML Video Player application via AppManager and perform video seek backward operation of WEBM content with VORBIS and VP8 codecs for few minutes and close the player. The test confirms that a backward seek completes successfully, with the video repositioning to the expected earlier location within the acceptable tolerance range. Both the seek request and completion are validated through media events.

<a name="head.Precondition"></a>
## Preconditions
|#| Step Name | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that the WPEFramework process is running on the device. | WPEFramework process should be up and running in the device. | WPEFramework should be active and running on the device. |
| 2 | Verify that the BOLT package host path is configured correctly. | MediaValidationVariables.bolt_packages_base_path must be configured with the BOLT packages hosting server URL.<br>(E.g. `http://<TM_IP>:<port>/images/signed-packages/`) | Ensure that the BOLT package host path is configured and accessible. |
| 3 | Verify that the BOLT app download URL resolves correctly. | MediaValidationVariables.html_player_app_download_url is derived from the base path and must resolve to the BOLT app package URL. | Ensure that the BOLT app package URL is valid and accessible for download. |
| 4 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.seekbwd_interval should be set to the seek-backward interval value (in seconds). | Ensure that the required configuration value is set correctly. |
| 5 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.seekbwd_check_interval should be set to the seek-backward check interval (in seconds). | Ensure that the required configuration value is set correctly. |
| 6 | Verify that the required interval configuration is set correctly. | MediaValidationVariables.close_interval should be set to the close interval value (in seconds). | Ensure that the required configuration value is set correctly. |
| 7 | Verify that the stream variable is configured correctly. | Stream variable `video_src_url_vorbis_vp8` must be defined in `MediaValidationVariables.py` as `test_streams_base_path + "TDK_Asset_Sunrise_VORBIS_VP8.webm"`, providing the test stream used for playback testing. | Verify that `video_src_url_vorbis_vp8` resolves to a valid, accessible stream location for this test. |
| 8 | Check whether the app is already installed on the device. | Query the installed package list using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}</code>. | Verify that the app is installed on the device. |
| 9 | Download the app package when it is not already available. | If the app is not installed, then download the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>"}}</code>. | Ensure that the app package is downloaded successfully. |
| 10 | Install the downloaded app package through PackageManager. | Install the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.html-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}</code>. | Confirm that the app package is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps
|#| Step Name | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Set playback operations for the scenario. | Configure the `seekbwd(60),close(30)` operations: the video player will seek backward for 60 seconds, then close the player after 30 seconds. | Ensure playback operations are set as specified. |
| 2 | Store the launch URL in PersistentStore. | Store the constructed URL in PersistentStore for AppManager launch. <br>Sample URL: `http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/htmlplayer.html?url=<video_src_url_vorbis_vp8>&operations=seekbwd(60),close(30)&autotest=true` | Ensure that the launch URL is stored in PersistentStore. |
| 3 | Launch the app through AppManager. | Launch the test app through AppManager using the URL stored in PersistentStore using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.launchApp", "params":{"appId": "com.rdkcentral.html-player"}}</code>. | Ensure that the app launches successfully via AppManager. |
| 4 | Check loaded apps and verify app presence. | Check whether the app is listed in loaded apps using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}</code>. | Verify that com.rdkcentral.html-player is present in the loaded apps list. |
| 5 | Execute seek operations and capture media events. | The player seeks the video backward by the configured seek interval from the current position. A **seeking** event fires immediately when the seek is requested, followed by a **seeked** event once the video repositions to the earlier location. The resulting video position is validated to be within the acceptable range of the expected backward seek target. | Ensure that the expected media events are captured for the configured operations. |
| 6 | Validate observed events for the seek backward operation and update test result. | If **seeking** and **seeked** events are received and the video position falls within the acceptable range of the backward seek target after the operation, the app reports SUCCESS, otherwise FAILURE. The test result is updated as SUCCESS or FAILURE based on event validation and process check status. | Ensure that the test result is updated as SUCCESS or FAILURE based on the seek backward event validation and proc check status. |
| 7 | Terminate app and restore test environment. | Terminate the test app through AppManager using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.terminateApp", "params":{"appId": "com.rdkcentral.html-player"}}</code> and restore the test environment. | Ensure that the app is terminated and the test environment is restored. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models**: Video_Accelerator

**Estimated duration**: 5 mins

**Priority**: High

**Release Version**: M143<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>