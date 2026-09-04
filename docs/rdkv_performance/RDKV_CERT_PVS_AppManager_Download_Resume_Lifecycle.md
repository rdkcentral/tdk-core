## TestCase ID
RDKV_PERFORMANCE_105
## TestCase Name
RDKV_CERT_PVS_AppManager_Download_Resume_Lifecycle
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that a large application download can be paused while in progress, remains paused without progress change, resumes with measurable progress advancement, and that resource usage remains within the expected limit after the download resumes.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the pre-execution reboot preference | Configure `PRE_REQ_REBOOT_PVS` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot preference should be configured according to the test environment requirements. |
| 2 | Confirm the required device plugins are activated | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, `org.rdk.AppManager`, and `org.rdk.RDKWindowManager` are activated. Their status can be queried with `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.DownloadManager"}`, `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.AppPackageManager"}`, `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.AppManager"}`, and `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.RDKWindowManager"}`. | All four plugins should report the `activated` state. |
| 3 | Provide a sufficiently large validation bundle | Configure `Large_Validation_File` and `app_download_url` with a reachable large application bundle and its hosting URL. `Large_Validation_File` can be any file of approximately 1 GB in size. Optionally, such a file can be created with `fallocate -l <size> <directory_path>/<file_name>`, where `<size>` is the desired file size, for example `1G`. | The bundle should be large enough to remain in progress during the progress polling period. |
| 4 | Configure the progress polling interval | Configure `progress_wait_time` with the maximum number of one-second polling attempts allowed while waiting for active download progress. | The polling limit should provide sufficient time for the large bundle to reach a state where `0 < progress < 100`. |
| 5 | Configure resource usage limits | Configure the resource thresholds used by the resource usage validation operation. | The expected resource limits should be available for comparison after the download resumes. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Load the performance test module | Load the RDKV performance test module and configure the testcase for `RDKV_CERT_PVS_AppManager_Download_Resume_Lifecycle`. | The performance test module should load successfully. |
| 2 | Activate the required plugins when necessary | If any required plugin is not activated, activate it with the following JSON-RPC request for each affected callsign: `{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"<plugin>"}}` where `<plugin>` is one of `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, `org.rdk.AppManager`, or `org.rdk.RDKWindowManager`. | Each required plugin should become activated successfully. |
| 3 | Construct the application download URL | Combine the configured `app_download_url` with `Large_Validation_File` to form the bundle URL. | The resulting download URL should identify the configured large validation bundle. |
| 4 | Start the application bundle download | Request the download using `org.rdk.DownloadManager.1.download` with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<app_download_url>/<Large_Validation_File>"}}`. | The download request should return success and a valid download ID. |
| 5 | Poll for active download progress | For up to `progress_wait_time` one-second attempts, query the download percentage using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.progress","params":{"downloadId":"<download_id>"}}`. Stop polling when the returned numeric value is greater than 0 and less than 100. | The download should reach an active in-progress state with a numeric percentage satisfying `0 < progress < 100`. |
| 6 | Pause the active download | Pause the download using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.pause","params":{"downloadId":"<download_id>"}}`. | The pause request should return success. |
| 7 | Read progress after pausing | Wait 3 seconds, then query progress again using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.progress","params":{"downloadId":"<download_id>"}}`. Compare the returned value with the progress recorded before pausing. | The progress value after the pause should equal the value recorded before the pause, demonstrating that downloading is suspended. |
| 8 | Resume the paused download | Resume the download using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.resume","params":{"downloadId":"<download_id>"}}`. | The resume request should return success. |
| 9 | Read progress after resuming | Wait 5 seconds, then query progress using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.progress","params":{"downloadId":"<download_id>"}}`. Compare the returned value with the paused progress value. | The resumed progress should be numeric and greater than the paused progress, demonstrating that downloading has continued. |
| 10 | Validate resource usage after download resume | Execute the resource usage validation operation and inspect its returned details against the configured expected limits. | The resource usage validation should return success and should not report `ERROR`; the resource usage should remain within the expected limit. |
| 11 | Complete the pause and resume lifecycle validation | Mark the test successful only when the pause request succeeds, progress remains unchanged while paused, the resume request succeeds, and progress advances after resuming. | The complete download pause-and-resume lifecycle should be validated successfully. |
| 12 | Unload the performance test module | Unload the RDKV performance test module after the lifecycle checks finish. | The performance test module should unload cleanly. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 5 minutes

**Priority** : High

**Release Version** : M152<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
