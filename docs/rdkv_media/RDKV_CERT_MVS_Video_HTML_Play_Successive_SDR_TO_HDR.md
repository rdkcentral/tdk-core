## TestCase ID
RDKV_MEDIA_1097
## TestCase Name
RDKV_CERT_MVS_Video_HTML_Play_Successive_SDR_TO_HDR
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To launch an HTML Player application and perform successive video playback of a SDR stream followed by a HDR stream and close the player. The test confirms that both streams playback successfully and gets the consolidated playback results.

<a name="head.Precondition"></a>
## Preconditions
|#| Step Name | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Verify that the WPEFramework process is running on the device. | WPEFramework process must be active and running on the device. | WPEFramework should be active and running on the device. |
| 2 | Verify that BOLT package host path is configured. | MediaValidationVariables.bolt_packages_base_path must be set to the BOLT packages hosting server URL.<br>(E.g. `http://<TM_IP>:<port>/images/signed-packages/`) | Ensure that the BOLT package host path is configured and accessible. |
| 3 | Verify that BOLT app download URL resolves correctly. | MediaValidationVariables.html_player_app_download_url is derived from the base path and must resolve to the BOLT app package URL. | Ensure that the BOLT app package URL is valid and accessible for download. |
| 4 | Verify that close interval is configured. | MediaValidationVariables.close_interval must be set to the close interval value (in seconds). | Ensure that the close interval value is configured correctly. |
| 5 | Verify that SDR stream variable is configured. | Stream variable `video_src_url_mp4` must be defined in `MediaValidationVariables.py` as `test_streams_base_path + "TDK_Asset_Sunrise_MP4.mp4"` and must resolve to a valid, accessible stream location. | Verify that `video_src_url_mp4` resolves to a valid, accessible stream location for this test. |
| 6 | Verify that HDR stream variable is configured. | Stream variable `video_src_url_hevc_hdr` must be defined in `MediaValidationVariables.py` as `test_streams_base_path + "TDK_Asset_Waterfall_HDR.MOV"` and must resolve to a valid, accessible stream location. | Verify that `video_src_url_hevc_hdr` resolves to a valid, accessible stream location for this test. |
| 7 | Check whether the app is installed or not. | Query the installed package list using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppPackageManager.1.listPackages"}</code>. | Verify that the app is installed on the device. |
| 8 | Download the app package when it is not already available. | If the app is not installed, then download the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>"}}</code>. | Ensure that the app package is downloaded successfully. |
| 9 | Install the downloaded app package through PackageManager. | Install the package using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppPackageManager.install", "params": {"packageId": "com.rdkcentral.html-player", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}</code>. | Confirm that the app package is installed successfully on the device. |

<a name="head.TestSteps"></a>
## Test Steps
|#| Step Name | Step Description | Expected Result |
|-|---------|-----------------|----------------|
| 1 | Set playback operations for both streams. | Configure the `close(30)` operations for each stream: the video player will play each stream for 30 seconds. | Ensure playback operations are set as specified for both streams. |
| 2 | Store both stream URLs as a list in PersistentStore. | Construct and store both stream URLs as an ordered list in PersistentStore for AppManager launch.<br>Sample URLs:<br>1. `http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/htmlplayer.html?url=<video_src_url_mp4>&operations=close(30)&autotest=true`<br>2. `http://<TM_IP>:<port>/tdkservice/fileStore/lightning-apps/htmlplayer.html?url=<video_src_url_hevc_hdr>&operations=close(30)&autotest=true` | Ensure that both launch URLs are stored in PersistentStore as a list. |
| 3 | Launch the app through AppManager. | Launch the test app through AppManager using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.launchApp", "params":{"appId": "com.rdkcentral.html-player"}}</code>. | Ensure that the app launches successfully via AppManager. |
| 4 | Check loaded apps and verify app presence. | Check whether the app is listed in loaded apps using the following request: <br><code>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}</code>. | Verify that com.rdkcentral.html-player is present in the loaded apps list. |
| 5 | Load the first stream (SDR) and capture media events. | The player loads the first URL from the list and starts playback of the SDR stream. A **play** event confirms that the video has started. The video position is monitored during playback to confirm the content is advancing continuously without stalls or interruptions for the configured duration. | Ensure that the media events are captured for the SDR playback. |
| 6 | Validate observed events for the first playback and record intermediate result. | If the SDR stream plays back successfully and the video position advances continuously throughout the configured duration without stalls or interruptions, the app reports SUCCESS, otherwise FAILURE. The intermediate result is recorded for the first stream. | Ensure that the intermediate result is recorded as SUCCESS or FAILURE for the SDR playback. |
| 7 | Clear the browser, load the second stream (HDR) and capture media events. | The browser is cleared after the first playback. The player then loads the second URL from the list and starts playback of the HDR stream. A **play** event confirms that the video has started. The video position is monitored during playback to confirm the content is advancing continuously without stalls or interruptions for the configured duration. | Ensure that the browser is cleared and the HDR stream loads and media events are captured. |
| 8 | Validate observed events for the second playback and record intermediate result. | If the HDR stream plays back successfully and the video position advances continuously throughout the configured duration without stalls or interruptions, the app reports SUCCESS, otherwise FAILURE. The intermediate result is recorded for the second stream. | Ensure that the intermediate result is recorded as SUCCESS or FAILURE for the HDR playback. |
| 9 | Get successive playback result and set the final test result. | The successive playback result is computed as a summary of both individual playback results. The final test result is updated as SUCCESS only if both the SDR and HDR playbacks succeed, otherwise FAILURE. | Ensure that the consolidated result correctly reflects the outcome of both playbacks. |
| 10 | Terminate the app and restore test environment. | Terminate the test app through AppManager using the following request: <br><code>{"jsonrpc":"2.0", "id":1, "method":"org.rdk.AppManager.1.terminateApp", "params":{"appId": "com.rdkcentral.html-player"}}</code> and restore the test environment. | Ensure that the app is terminated and the test environment is restored. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models**: Video_Accelerator

**Estimated duration**: 10 mins

**Priority**: High

**Release Version**: M152<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>