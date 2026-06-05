## TestCase ID
RDKV_STABILITY_91
## TestCase Name
RDKV_CERT_RVS_LongDuration_VideoPlayback_4K_DASH
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that resource usage (CPU and memory) remains within acceptable limits while playing a 4K DASH video stream in the Lightning unified video player application for a minimum of 10 hours.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`video_src_url_4k_dash` must be configured in MediaValidationVariables with a valid 4K DASH (HEVC/AAC) stream URL (e.g., DASH_HEVC_AAC_4K_Only/atfms_291_dash_tdk_hevc_aac_fmp4_4konly.mpd under test_streams_base_path).|
|3|`bolt_packages_base_path` must be configured in MediaValidationVariables with the base URL from which the unified player bolt package (com.rdkcentral.lightning-unified-player+0.1.0.bolt) can be downloaded.|
|4|`lightning_video_test_app_url` must be configured in MediaValidationVariables with the URL of the Lightning video player test application.|
|5|`LOGGING_METHOD` in device-specific config must be set to either `REST_API` or `WEB_INSPECT` to determine how playback progress and resource usage logs are collected.|
|6|`PACKAGEMANAGER_FILE_LOCATOR` in device-specific config must be updated with the correct path where downloaded packages are stored on the DUT.|
|7|Device should be rebooted before test execution if `PRE_REQ_REBOOT` is configured as `Yes` in device config.|
|8|DeviceInfo and org.rdk.PersistentStore plugins should be available in the build.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Pre-requisite Reboot | Conditionally reboot the device before starting the test It reads the `PRE_REQ_REBOOT` key from the device-specific config file. If set to "Yes", it issues a reboot via `Controller.1.harakiri` and waits 150 seconds for the device to recover. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"} | Device should come back online successfully if reboot was triggered. |
| 2 | Check Device Pre-condition State | Validate initial CPU and memory resource usage before the test begins using applicable API calls. Ensures DeviceInfo plugin is activated, then invokes the relevant API. DeviceInfo plugin status is reverted after the check. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "<api_method>"} | CPU and memory usage should be within the expected range before the test starts. |
| 3 | Read Device Config and Video URL | Read the device-specific config file to determine `LOGGING_METHOD`. Retrieve the 4K DASH video URL from `MediaValidationVariables.video_src_url_4k_dash` and confirm both `video_src_url_4k_dash` and video type ("dash") are non-empty. | Device config must be accessible and both video URL and type must be configured. |
| 4 | Build Video Player App URL | Construct the complete Lightning video player test app URL by assembling all URL arguments: execID, execDevId, resultId, logging method, TM server URL, operation (`close(36000)` for 10-hour playback), video source URL (4K DASH), options (looptest), autotest=true, type=dash. The player "hlsjs" is selected from `MediaValidationVariables.codec_hls_h264`, resolving to `lightning_video_test_app_url` as the base app URL. | Video player test app URL should be constructed successfully with all required parameters. |
| 5 | Check and Activate Required Plugins | Check the status of DeviceInfo and org.rdk.PersistentStore plugins. If either is not in the required activated state, activate it using applicable API calls. The original states are stored for revert on exit. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PersistentStore"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PersistentStore"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}} | DeviceInfo and org.rdk.PersistentStore plugins should be in activated state. |
| 6 | Set Video Test URL in PersistentStore | Store the constructed video player test app URL in the PersistentStore so the Lightning app can retrieve it on launch. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "<api_method>", "params": {"video_test_url": "<constructed_video_player_url>"}} | Video test URL should be set successfully in PersistentStore. |
| 7 | Install and Launch Lightning Unified Player App | Check if com.rdkcentral.lightning-unified-player is already installed using applicable API calls. If not installed: activate DownloadManager, PackageManagerRDKEMS, and AppManager plugins, download the bolt package from `bolt_packages_base_path`, install it using `PACKAGEMANAGER_FILE_LOCATOR`, and verify it appears in the installed packages list. Then launch the app via AppManager. <br>List packages: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}<br>Download: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<bolt_packages_base_path>/com.rdkcentral.lightning-unified-player+0.1.0.bolt"}}<br>Install: {"jsonrpc": "2.0", "id": 1234567890, "method": "<api_method>", "params": {"fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>", "app_id": "com.rdkcentral.lightning-unified-player"}}<br>Launch: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.lightning-unified-player", "intent": "", "launchArgs": ""}} | Unified player app should be installed and launched successfully. |
| 8 | Monitor Playback and Validate Resource Usage (REST API or WebInspect) | Monitor video playback progress and validate CPU/memory resource usage at regular intervals (every 30 seconds) over the 10-hour duration. <br>**REST API mode**: Monitors the app log file for "Video Player CanPlay Through" events. On each event, records CPU load and memory usage. Waits for "TEST RESULT: SUCCESS" in the log to confirm full test completion. If the log file does not appear within 60 seconds or the app hangs for 60 consecutive seconds, the test is marked FAILURE. <br>**WEB_INSPECT mode**: Connects a WebSocket event listener to the WebInspect port (`/devtools/page/1`). Waits for "VIDEO STARTED PLAYING" message, then periodically invokes every 30 seconds. Validates until "TEST RESULT: SUCCESS" is received in the console. Times out with FAILURE if no activity for 180 seconds. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "<api_method>"} | Video playback should start successfully and CPU/memory usage should remain within expected limits throughout the 10-hour duration. "TEST RESULT: SUCCESS" must appear in the app output. |
| 9 | Terminate the App | After the test completes (or on failure), terminate the Lightning unified player app using applicable API calls. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "<api_method>", "params": {"app_id": "com.rdkcentral.lightning-unified-player"}} | App should be terminated successfully. |
| 10 | Revert Plugin Statuses | If any plugins were changed from their original state in Step 5, revert them back to their original states using applicable API calls. | Plugin states should be restored to their pre-test values. |
| 11 | Check Device Post-condition State | Validate CPU and memory resource usage after the test completes to confirm the device is in a healthy state. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "<api_method>"} | CPU and memory usage should be within the expected range after test completion. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

**Estimated duration** : 630

**Priority** : High

**Release Version** : M103<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
