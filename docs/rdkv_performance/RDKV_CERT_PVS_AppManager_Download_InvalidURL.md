## TestCase ID
RDKV_PERFORMANCE_104
## TestCase Name
RDKV_CERT_PVS_AppManager_Download_InvalidURL
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the application download service rejects an invalid URL with a download failure event, accepts a valid URL, reports the successful download through an event, and permits deletion of the downloaded package.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the pre-execution reboot preference | Configure `PRE_REQ_REBOOT_PVS` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot preference should be configured according to the test environment requirements. |
| 2 | Confirm the required device plugins are activated | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, `org.rdk.AppManager`, and `org.rdk.RDKWindowManager` are activated. Their status can be queried with `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.DownloadManager"}`, `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.AppPackageManager"}`, `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.AppManager"}`, and `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.RDKWindowManager"}`. | All four plugins should report the `activated` state. |
| 3 | Configure application bundle URLs | Configure `google_bundle`, `app_download_url`, and `invalid_download_url` with the application bundle name, a reachable base URL, and an intentionally invalid base URL. | The valid URL should be reachable, and the invalid URL should be suitable for negative download testing. |
| 4 | Configure SSH access | Configure `SSH_METHOD`, `SSH_USERNAME`, and `SSH_PASSWORD` in the applicable device configuration file. | Valid SSH connection details should be available for package deletion verification. |
| 5 | Configure resource usage limits | Configure the resource thresholds used by the resource usage validation operation. | The expected resource limits should be available for comparison after deletion of the package. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Load the performance test module | Load the RDKV performance test module and configure the testcase for `RDKV_CERT_PVS_AppManager_Download_InvalidURL`. | The performance test module should load successfully. |
| 2 | Activate the required plugins when necessary | If any required plugin is not activated, activate it with the following JSON-RPC request for each affected callsign: `{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"<plugin>"}}` where `<plugin>` is one of `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, `org.rdk.AppManager`, or `org.rdk.RDKWindowManager`. | Each required plugin should become activated successfully. |
| 3 | Retrieve SSH connection details | Read the configured SSH method and credentials for the device and make them available for remote verification commands. | Valid SSH method and credentials should be retrieved successfully. |
| 4 | Subscribe to application download status events | Register for download status notifications at `/jsonrpc` using `{"jsonrpc": "2.0","id": 2,"method": "org.rdk.DownloadManager.1.register","params": {"event": "onAppDownloadStatus", "id": "client.events.1" }}`. | The event subscription should be established successfully. |
| 5 | Prepare the valid and invalid download URLs | Build the valid URL from `app_download_url` and `google_bundle`, and build the failing URL from `invalid_download_url` and the same bundle name. | Both test URLs should be constructed successfully, with only the valid URL pointing to the application bundle location. |
| 6 | Clear previously received events | Clear the download event buffer before starting the invalid-URL test. | Previously buffered events should be removed. |
| 7 | Request a download from the invalid URL | Submit the invalid URL to `org.rdk.DownloadManager.1.download` using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<invalid_download_url>/<google_bundle>"}}`. | The download request should fail rather than return success. |
| 8 | Process the invalid-URL download result | Execute the invalid-URL download test operation a second time as implemented by the script, then read the returned status and details. | The resulting status should remain unsuccessful for the invalid URL. |
| 9 | Validate the invalid-URL failure event | Poll the subscribed event buffer for up to 120 seconds and retrieve the first available event. | An `onAppDownloadStatus` event should be received and should contain `DOWNLOAD_FAILURE`. |
| 10 | Clear events before the valid download | Clear the event buffer after validating the invalid-URL failure and before starting the valid download. | The event buffer should contain no stale invalid-URL event. |
| 11 | Request a download from the valid URL | Submit the valid URL to `org.rdk.DownloadManager.1.download` using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<app_download_url>/<google_bundle>"}}`. | The download request should return success and a download ID. |
| 12 | Validate the successful download event | Poll the event buffer for up to 120 seconds. Confirm that the received `onAppDownloadStatus` event does not contain `DOWNLOAD_FAILURE`, then parse its download status entry and obtain `downloadId` and `fileLocator`. | A non-failure download status event should be received, and it should contain a valid download ID and file locator. |
| 13 | Match the event to the download request | Compare the event `downloadId` with the returned download ID and confirm that the event file locator contains that download ID. | The event download ID should match the request ID, and the file locator should identify the requested package. |
| 14 | Delete the downloaded package | Delete the package using `org.rdk.DownloadManager.delete` with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.delete","params":{"fileLocator":"<file_locator>"}}`. | The package deletion request should return success. |
| 15 | Verify package deletion from storage | Execute the remote command `ls -l <file_locator>` using the configured SSH connection. | The command output should contain `No such file or directory` or `cannot access`, confirming that the package no longer exists on the device. |
| 16 | Validate resource usage after package deletion | Execute the resource usage validation operation and inspect its returned details against the configured expected limits. | The resource usage validation should return success and should not report `ERROR`; the resource usage should remain within the expected limit. |
| 17 | Close the download event subscription | Disconnect from the download status event stream after all validations are complete. | The event subscription should close cleanly and the testcase should finish without an active listener. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 minutes

**Priority** : High

**Release Version** : M152<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
