## TestCase ID
RDKV_STABILITY_29
## TestCase Name
RDKV_CERT_RVS_AppManager_Install_Cancelled_Package
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that a cancelled in-progress application download reports the matching download identifier and file locator, and that immediate installation using the cancelled download file locator fails as expected.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the device connection | Configure the target device IP address and port so that the stability test framework can connect to the device. | The test framework should connect to the target device successfully. |
| 2 | Configure the reboot policy | Configure `PRE_REQ_REBOOT` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot policy should be applied according to the configured value. |
| 3 | Check WPEFramework and device status | Load the `rdkv_stability` module and verify that the device is available before starting the test. | The framework module and device status should report success. |
| 4 | Activate the required application services | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager` are activated. | All required application services should be in the activated state. |
| 5 | Provide a sufficiently large validation bundle | Configure `Large_Validation_File` and `app_download_url` with a reachable large application bundle and its hosting URL. `Large_Validation_File` can be any file of approximately 1 GB. Optionally, create the file with `fallocate -l 1G <directory_path>/<file_name>`. | The large validation bundle should be reachable and large enough to remain in progress when the download progress check is performed, and the application package URL should be constructed successfully. |
| 6 | Configure the stability iteration count | Configure the application manager stability test count used for repeated execution. | A valid positive iteration count should be available for the test. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Subscribe to download status events | Register a listener for application download status events using: `{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.DownloadManager.1.register", "params": {"event": "onAppDownloadStatus", "id": "client.events.1" }}`. | The download status event subscription should be registered successfully. |
| 2 | Start the application download | Clear the event buffer and start downloading the configured large validation application package. | The download request should return success and provide a download identifier. |
| 3 | Verify download identifier uniqueness | Compare the returned download identifier with all identifiers recorded during the test and store it when it has not been used previously. | The download identifier should be unique and should be added to the recorded identifier set. |
| 4 | Poll download progress | Query download progress using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.progress","params":{"downloadId":"<download_id>"}}`. Poll for up to 30 checks until progress becomes greater than zero. | The progress query should return successfully and should report a value greater than zero before cancellation. |
| 5 | Cancel the in-progress download | Cancel the download using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.cancel","params":{"downloadId":"<download_id>"}}`. | The cancellation request should return success while the download is between 0 and 100 percent complete. |
| 6 | Validate the cancellation event | Read the download event buffer for up to 120 seconds until an `onAppDownloadStatus` event containing `DOWNLOAD_FAILURE` is received. Parse the event’s download status and extract its download identifier and file locator. | A cancellation event should be received, its identifier should match the cancelled download, and its file locator should be non-empty. |
| 7 | Attempt immediate installation from the cancelled file locator | Submit an installation request for application using the file locator returned in the cancellation event. | The installation request should fail because the file locator belongs to the cancelled download. |
| 8 | Repeat the cancellation and installation validation | Repeat the download, uniqueness check, progress polling, cancellation, cancellation-event validation, and immediate installation attempt for the configured application manager test count. | The complete validation block should execute for every configured iteration, and each iteration should confirm expected installation failure after cancellation. |
| 9 | Disconnect the event listener and test module | Disconnect the download event listener and unload the `rdkv_stability` test module after all iterations complete. | The event listener and test module should be disconnected and unloaded cleanly. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 300 seconds

**Priority** : High

**Release Version** : M153<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
