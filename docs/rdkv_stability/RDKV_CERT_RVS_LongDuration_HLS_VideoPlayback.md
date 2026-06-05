## TestCase ID
RDKV_STABILITY_43
## TestCase Name
RDKV_CERT_RVS_LongDuration_HLS_VideoPlayback
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that resource usage (CPU and memory) remains within acceptable limits while playing an HLS video stream in the Lightning unified video player application for a minimum of 10 hours.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`video_src_url_hls` must be configured in StabilityTestVariables with a valid HLS video stream URL of minimum 10 hours duration (default value is empty and must be updated before execution).|
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
| 1 | Pre-requisite Reboot | Conditionally reboot the device before the test It reads the `PRE_REQ_REBOOT` key from the device-specific config file. If set to "Yes", the device is rebooted via `Controller.1.harakiri` and the script waits 150 seconds for it to come back online. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"} | Device should come back online successfully if reboot was triggered. |
| 2 | Check Device Pre-condition State | Validate initial CPU and memory resource usage before the test begins using applicable API calls. Ensures DeviceInfo plugin is activated, invokes to check usage, and reverts the DeviceInfo plugin state afterward. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "<api_method>"} | CPU and memory usage should be within the expected range before the test starts. |
| 3 | Read Device Config and Video URL | Read the device-specific config file to determine `LOGGING_METHOD`. Retrieve the HLS video stream URL from `StabilityTestVariables.video_src_url_hls` and confirm it is non-empty. If the URL is not configured, the test is marked as FAILURE and execution stops. | Device config must be accessible and `video_src_url_hls` must be configured with a valid HLS stream URL. |
| 4 | Build Video Player App URL | Construct the complete Lightning video player test app URL by assembling all URL arguments: execID, execDevId, resultId, logging method, TM server URL, video source URL (HLS), operation (`close(36000)` for 10-hour playback), autotest=true, type=hls. The player "hlsjs" is selected from `MediaValidationVariables.codec_hls_h264`, resolving to `lightning_video_test_app_url` as the base app URL. The URL is URL-encoded for special characters. | Video player test app URL should be constructed successfully with all required parameters. |
| 5 | Check and Activate Required Plugins | Check the status of DeviceInfo and org.rdk.PersistentStore plugins. If either is not in the required activated state, activate it via applicable API calls. Original states are saved for revert on exit. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PersistentStore"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PersistentStore"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}} | DeviceInfo and org.rdk.PersistentStore plugins should be in activated state. |
| 6 | Set Video Test URL in PersistentStore | Store the constructed video player test app URL in PersistentStore so the Lightning app can retrieve it on launch. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "<api_method>", "params": {"video_test_url": "<constructed_video_player_url>"}} | Video test URL should be set successfully in PersistentStore. |
| 7 | Install and Launch Lightning Unified Player App | Check if com.rdkcentral.lightning-unified-player is already installed via applicable API calls. If not installed: activate DownloadManager, PackageManagerRDKEMS, and AppManager plugins; download the bolt package from `bolt_packages_base_path`; install using `PACKAGEMANAGER_FILE_LOCATOR`; verify it appears in the installed packages list. Then launch the app via AppManager. <br>List packages: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}<br>Download: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<bolt_packages_base_path>/com.rdkcentral.lightning-unified-player+0.1.0.bolt"}}<br>Install: {"jsonrpc": "2.0", "id": 1234567890, "method": "<api_method>", "params": {"fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>", "app_id": "com.rdkcentral.lightning-unified-player"}}<br>Launch: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.lightning-unified-player", "intent": "", "launchArgs": ""}} | Unified player app should be installed and launched successfully. |
| 8 | Monitor Playback and Validate Resource Usage (REST API or WebInspect) | Monitor HLS video playback progress and validate CPU/memory resource usage at regular intervals (every 30 seconds) over the 10-hour duration. <br>**REST API mode**: Monitors the app log file for "Video Player CanPlay Through" events. On each event, records CPU load and memory usage. Waits for "TEST RESULT: SUCCESS" in the log to confirm full test completion. If the log file does not appear within 60 seconds or the app hangs for 60 consecutive seconds, the test is marked FAILURE. <br>**WEB_INSPECT mode**: Connects a WebSocket event listener to the WebInspect port (`/devtools/page/1`). Waits for "VIDEO STARTED PLAYING" message, then periodically invokes every 30 seconds. Validates until "TEST RESULT: SUCCESS" is received in the console. Times out with FAILURE if no activity for 180 seconds. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "<api_method>"} | HLS video playback should start successfully and CPU/memory usage should remain within expected limits throughout the 10-hour duration. "TEST RESULT: SUCCESS" must appear in the app output. |
| 9 | Save Resource Usage Log | After playback monitoring completes, write all per-iteration CPU load and memory usage readings to a JSON log file (`CPUMemoryInfo.json`) in the test execution log path for offline analysis. | JSON log file should be created with all recorded CPU and memory data points. |
| 10 | Revert Plugin Statuses | If any plugins were changed from their original state in Step 5, revert them back to their original states using applicable API calls. | Plugin states should be restored to their pre-test values. |
| 11 | Check Device Post-condition State | Validate CPU and memory resource usage after the test completes to confirm the device remains in a healthy state. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "<api_method>"} | CPU and memory usage should be within the expected range after the 10-hour playback test completes. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 630

**Priority** : High

**Release Version** : M92<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
