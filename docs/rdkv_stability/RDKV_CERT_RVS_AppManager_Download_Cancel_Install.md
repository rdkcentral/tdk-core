## TestCase ID
RDKV_STABILITY_28
## TestCase Name
RDKV_CERT_RVS_AppManager_Download_Cancel_Install
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that an in-progress application download can be cancelled with the correct failure event and file locator, and that a subsequent application download and installation produce the expected event order and unique download identifiers.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the device connection | Configure the target device IP address and port so that the stability test framework can connect to the device. | The test framework should connect to the target device successfully. |
| 2 | Configure the reboot policy | Configure `PRE_REQ_REBOOT` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot policy should be applied according to the configured value. |
| 3 | Check WPEFramework and device status | Load the `rdkv_stability` module and verify that the device is available before starting the test. | The framework module and device status should report success. |
| 4 | Activate the required application services | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager` are activated. | All required application services should be in the activated state. |
| 5 | Provide sufficiently large validation bundles | Configure `Large_Validation_File` and `app_download_url` with a reachable large application bundle and its hosting URL. `Large_Validation_File` can be any file of approximately 1 GB. Optionally, create the file with `fallocate -l 1G <directory_path>/<file_name>`. | The large validation bundle should be reachable and large enough to remain in progress when the download progress check is performed, and both package URLs should be constructed successfully. |
| 6 | Configure the stability iteration count | Configure the application manager stability test count used for repeated execution. | A valid positive iteration count should be available for the test. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Subscribe to download and installation events | Register listeners for application download and installation status events using the following JSON-RPC payloads:<br>`{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.DownloadManager.1.register", "params": {"event": "onAppDownloadStatus", "id": "client.events.1" }}`<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppPackageManager.1.register", "params": {"event": "onAppInstallationStatus", "id": "client.events.1" }}` | The download and installation event subscriptions should be registered successfully. |
| 2 | Start the validation package download | Clear the event buffer and start downloading the configured large validation package. | The download request should return success and provide a download identifier. |
| 3 | Verify download identifier uniqueness | Compare the new download identifier with all identifiers recorded during the test and store it when it has not been used previously. | The download identifier should be unique and should be added to the recorded identifier set. |
| 4 | Poll download progress | Query download progress using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.progress","params":{"downloadId":"<download_id>"}}`. Poll for up to 30 checks until progress becomes greater than zero. | The progress query should return successfully and should report a value greater than zero before cancellation. |
| 5 | Cancel the in-progress download | Cancel the download using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.cancel","params":{"downloadId":"<download_id>"}}`. | The cancellation request should return success while the download is between 0 and 100 percent complete. |
| 6 | Validate the cancellation event | Read the event buffer for up to 120 seconds and validate an `onAppDownloadStatus` event containing `DOWNLOAD_FAILURE`. Parse its download status and extract the event download identifier and file locator. | A cancellation event should be received, its identifier should match the cancelled download, and its file locator should be non-empty. |
| 7 | Start the replacement application download | Clear the event buffer and start downloading the configured Google application bundle. | The replacement download request should return success and provide a new download identifier. |
| 8 | Verify replacement download identifier uniqueness | Add the replacement download identifier to the recorded identifiers and verify that no identifier has been reused. | The replacement download identifier should be unique. |
| 9 | Validate replacement download completion | Read download status events for up to 120 seconds until an `onAppDownloadStatus` event without `DOWNLOAD_FAILURE` is received. Parse the event and compare its completed download identifier with the replacement download identifier. | A successful download event should be received, its identifier should match, and its file locator should be non-empty. |
| 10 | Install the downloaded application | Submit the installation request using the replacement download file locator and the Google application name as the application identifier. | The installation request should return success and use the freshly downloaded file locator. |
| 11 | Validate the installation event | Read installation status events for up to 120 seconds until an `onAppInstallationStatus` event containing `INSTALLED` and the expected application name is received. | The installation event should be received for the expected application. |
| 12 | Verify event order and identifier uniqueness | Confirm that the cancellation event preceded the successful replacement download and installation flow, and verify that the number of recorded download identifiers equals the number of unique identifiers. | The event sequence should represent download cancellation followed by installation, and no download identifier should be reused. |
| 13 | Uninstall the application | Uninstall the Google application using its application identifier. | The uninstall request should return success and the application should be removed. |
| 14 | Repeat the download and installation validation | Repeat the download, progress polling, cancellation, cancellation-event validation, replacement download, completion-event validation, installation, installation-event validation, uniqueness checks, and uninstall actions for the configured application manager test count. | The complete event-order validation block should execute for every configured iteration, and each iteration should preserve unique download identifiers and the required event sequence. |
| 15 | Disconnect the event listener | Disconnect the event listener and unload the `rdkv_stability` test module after all iterations complete. | The event listener and test module should be disconnected and unloaded cleanly. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 300 seconds

**Priority** : High

**Release Version** : M153<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
