## TestCase ID
RDKV_PERFORMANCE_103
## TestCase Name
RDKV_CERT_PVS_AppManager_Cancel_LargeFile_Download
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that a large application download can be cancelled while in progress, that the cancellation status event contains the correct download information, and that deleting the cancelled package restores disk usage to its initial level.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the pre-execution reboot preference | Configure `PRE_REQ_REBOOT_PVS` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot preference should be configured according to the test environment requirements. |
| 2 | Confirm the required device plugins are activated | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, `org.rdk.AppManager`, and `org.rdk.RDKWindowManager` are activated. Their status can be queried with `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.DownloadManager"}`, `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.AppPackageManager"}`, `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.AppManager"}`, and `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.RDKWindowManager"}`. | All four plugins should report the `activated` state. |
| 3 | Configure package storage and SSH access | Configure `PACKAGEMANAGER_FILE_LOCATOR`, `SSH_METHOD`, `SSH_USERNAME`, and `SSH_PASSWORD` in the applicable device configuration file. | The package locator and complete SSH connection details should be available to the test. |
| 4 | Provide a sufficiently large validation bundle | Configure `Large_Validation_File` and `app_download_url` with a reachable large application bundle and its hosting URL. `Large_Validation_File` can be any file of approximately 1 GB in size. | The bundle should be large enough to remain in progress when the progress check is performed. |
| 5 | Configure resource usage limits | Configure the resource thresholds used by the resource usage validation operation. | The expected resource limits should be available for comparison after deletion of the package. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Load the performance test module | Load the RDKV performance test module and configure the testcase for `RDKV_CERT_PVS_AppManager_Cancel_LargeFile_Download`. | The performance test module should load successfully. |
| 2 | Activate the required plugins when necessary | If any required plugin is not activated, activate it with the following JSON-RPC request for each affected callsign: `{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"<plugin>"}}` where `<plugin>` is one of `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, `org.rdk.AppManager`, or `org.rdk.RDKWindowManager`. | Each required plugin should become activated successfully. |
| 3 | Retrieve the package storage locator | Read `PACKAGEMANAGER_FILE_LOCATOR` from the device configuration and derive the package directory by retaining the path before `/package`. | The package storage directory should be resolved successfully. |
| 4 | Retrieve SSH connection details | Read the configured SSH method, device IP, username, and password from the device configuration for remote command execution. | Valid SSH method and credentials should be available. |
| 5 | Measure initial package storage usage | Execute the following remote command against the package storage directory: `du -sk <file_locator>/CDL/ \| awk '{print $1}'`. | The initial package storage usage should be returned as a numeric value in KB. |
| 6 | Subscribe to application download status events | Register for download status notifications at `/jsonrpc` using the following payload: `{"jsonrpc": "2.0","id": 2,"method": "org.rdk.DownloadManager.1.register","params": {"event": "onAppDownloadStatus", "id": "client.events.1" }}`. | The event subscription should be established successfully. |
| 7 | Start downloading the large application bundle | Request the bundle download using `org.rdk.DownloadManager.1.download` with the configured URL and the `Large_Validation_File` name: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<app_download_url><Large_Validation_File>"}}`. | The download request should return success and a download ID. |
| 8 | Query the download progress | Query the download progress for the returned download ID using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.progress","params":{"downloadId":"<download_id>"}}`. | The progress request should return a numeric percentage greater than 0 and less than 100. |
| 9 | Cancel the active download | Cancel the in-progress download using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.cancel","params":{"downloadId":"<download_id>"}}`. | The cancellation request should return success. |
| 10 | Poll for the cancellation status event | Poll the subscribed event buffer for up to 120 seconds and retrieve the first available event. | An `onAppDownloadStatus` event should be received and should indicate `DOWNLOAD_FAILURE` for the cancelled download. |
| 11 | Validate the cancellation event details | Parse the event and compare its `downloadId` with the requested download ID. Confirm that its `fileLocator` contains the same download ID. The event data must contain fields equivalent to `{"downloadId":"<download_id>","fileLocator":"<file_locator>"}` within the download status entry. | The event download ID should match the requested ID, and the file locator should identify the cancelled package. |
| 12 | Delete the cancelled package | Delete the package identified by the event file locator using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.delete","params":{"fileLocator":"<file_locator>"}}`. | The package deletion request should return success. |
| 13 | Verify package deletion from storage | Execute the following remote command for the event file locator: `ls -l <file_locator>`. | The command output should contain `No such file or directory`, confirming that the cancelled package was removed. |
| 14 | Measure package storage after deletion | Execute `du -sk <file_locator_directory> \| awk '{print $1}'` against the package storage directory and compare the result with the initial usage. | The final package storage usage should be less than or equal to the initial usage. |
| 15 | Validate resource usage after package deletion | Execute the resource usage validation operation and inspect its returned details against the configured expected limits. | The resource usage validation should return success and should not report `ERROR`; the resource usage should remain within the expected limit. |
| 16 | Close the download event subscription | Disconnect from the download status event stream after all validations are complete. | The event subscription should close cleanly and the testcase should finish without an active listener. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 minutes

**Priority** : High

**Release Version** : M152<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
