## TestCase ID
RDKV_PERFORMANCE_83
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_Download_AppBundle

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to download an application bundle via the DownloadManager is within the configured performance threshold, measured from the download request to the receipt of the onAppDownloadStatus event.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Confirm org.rdk.DownloadManager plugin is available | The org.rdk.DownloadManager plugin must be present and activatable in the device build. | The DownloadManager plugin should be available in the build. |
| 3 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 4 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 5 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. | The app_download_url should point to a reachable hosting location from the device network. |
| 6 | Configure download threshold in device config | `APPMANAGER_DOWNLOAD_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be set in the device-specific configuration file with appropriate millisecond values. | Threshold and offset values should be correctly configured for performance comparison. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate the DownloadManager plugin | Query the DownloadManager plugin status and activate it if not already active. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}` | The org.rdk.DownloadManager plugin should be in the activated state. |
| 2 | Subscribe to the download status event | Register a WebSocket event listener for onAppDownloadStatus to capture the timestamp when the download completes. <br>`{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.DownloadManager.1.register", "params": {"event": "onAppDownloadStatus", "id": "client.events.1"}}` | Event subscription should be established successfully. |
| 3 | Trigger app bundle download and record start time | Construct the full bundle URL by appending the bundle filename to the base download URL, record the current UTC timestamp as the download start time, then initiate the download. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` | The download request should be accepted and the download should begin. |
| 4 | Wait for the onAppDownloadStatus event and extract completion timestamp | Monitor the event buffer until the onAppDownloadStatus event is received or a 120-second timeout is reached. Extract the download completion timestamp embedded in the event payload. | The onAppDownloadStatus event should be received within the timeout, confirming the download completed. |
| 5 | Calculate download time and validate against threshold | Compute the elapsed time in milliseconds as the difference between the onAppDownloadStatus event timestamp and the recorded start time. Compare against `APPMANAGER_DOWNLOAD_THRESHOLD_VALUE` + `THRESHOLD_OFFSET` from device config. | The time taken to download the app bundle should be within the range: 0 < time_taken < (APPMANAGER_DOWNLOAD_THRESHOLD_VALUE + THRESHOLD_OFFSET) milliseconds. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
