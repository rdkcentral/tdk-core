## TestCase ID
RDKV_STABILITY_26
## TestCase Name
RDKV_CERT_RVS_AppManager_Redownload

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DownloadManager supports repeated download of the same application bundle across all configured iterations, verifying that each download produces a unique download ID, the downloaded package size matches the configured expected size (10240 KB), the package can be deleted successfully after the initial download, a subsequent re-download of the same file completes correctly, and the disk usage remains within acceptable limits throughout the test.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test before test execution begins. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT_PVS in device config | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the validation file is hosted. The full download URL is constructed as `app_download_url + "/" + Small_Validation_File` ("10_MB_File.bin"). | The app_download_url should point to a reachable and valid hosting location. |
| 4 | Configure AppManager_test_count in StabilityTestVariables | `AppManager_test_count` must be set to the desired number of download, delete, and re-download iterations in StabilityTestVariables (default: 100). | The AppManager_test_count variable should be configured with a valid integer value. |
| 5 | Configure Redownload_Package_Size_MB in StabilityTestVariables | `Redownload_Package_Size_MB` must be set to the expected size of the validation file in megabytes in StabilityTestVariables (default: 10 MB, equivalent to 10240 KB). | The Redownload_Package_Size_MB variable should be configured with the correct expected package size. |
| 6 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. This path is also used to determine the download staging directory for disk usage monitoring. | The file locator path should be correctly configured in the device-specific configuration file. |
| 7 | Configure MEMORY_OFFSET in device config | `MEMORY_OFFSET` must be set to an allowable disk usage margin (in KB) in the device configuration file, used to account for filesystem overhead during disk usage comparisons. | The MEMORY_OFFSET value should be correctly configured in the device-specific configuration file. |
| 8 | Configure SSH access parameters in device config | SSH method and credentials must be configured in the device configuration file to allow file size verification and disk usage monitoring via SSH commands on the DUT. | SSH parameters should be correctly configured and accessible from the device configuration file. |
| 9 | Confirm required plugins are available | The following plugins must be available and activatable on the device: org.rdk.DownloadManager, org.rdk.AppPackageManager, org.rdk.AppManager, and org.rdk.RDKWindowManager. | All required plugins should be present and activatable on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT_PVS` configuration key. If set to Yes, the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | The device should come back online successfully if reboot was configured. |
| 2 | Verify and activate required plugins | Retrieve the current activation state of org.rdk.DownloadManager, org.rdk.AppPackageManager, org.rdk.AppManager, and org.rdk.RDKWindowManager. Activate any plugin that is not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppPackageManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.RDKWindowManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All four required plugins should be in the activated state before test execution proceeds. |
| 3 | Record initial disk usage of download staging directory | Retrieve the initial disk usage of the download staging directory derived from `PACKAGEMANAGER_FILE_LOCATOR` via SSH to establish a baseline for post-deletion disk usage comparison. <br>`du -sk <file_locator> \| awk '{print $1}'` | The initial disk usage value (in KB) should be retrieved successfully and stored as the baseline for all disk usage validations. |
| 4 | Subscribe to onAppDownloadStatus event | Register a WebSocket event listener to subscribe to the onAppDownloadStatus event from org.rdk.DownloadManager. Wait 5 seconds after registration. <br>`{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.DownloadManager.1.register", "params": {"event": "onAppDownloadStatus", "id": "client.events.1"}}` | The onAppDownloadStatus event subscription should be established successfully and the WebSocket event listener should be active. |
| 5 | Initiate first download of validation file (Per Iteration) | For each of the `AppManager_test_count` (100) iterations, initiate the download of the 10 MB validation file ("10_MB_File.bin") from the configured URL using the DownloadManager download API. Wait 15 seconds after initiating the download. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/10_MB_File.bin"}}` | The download API should return SUCCESS and provide a unique download ID for each iteration. |
| 6 | Verify onAppDownloadStatus event for first download (Per Iteration) | Monitor the event listener buffer for up to 120 seconds to receive the onAppDownloadStatus event for the first download. Parse the event to extract the downloadId and fileLocator fields. <br>`{"jsonrpc": "2.0", "method": "client.events.1.onAppDownloadStatus", "params": {"downloadStatus": "[{\"downloadId\": \"<id>\", \"fileLocator\": \"<url>\"}]"}}` | The onAppDownloadStatus event should be received within the monitoring period, providing the download ID and fileLocator for each iteration. |
| 7 | Verify first download ID is unique (Per Iteration) | Confirm that the download ID received in the onAppDownloadStatus event has not appeared in any previous iteration of the test. | The first download ID should be unique and not present in the list of previously seen download IDs for each iteration. |
| 8 | Verify downloaded file size via SSH (Per Iteration) | Measure the size of the downloaded file on the DUT via SSH and compare it against the expected package size of 10240 KB (`Redownload_Package_Size_MB` × 1024). <br>`du -sk <filelocator_url> \| awk '{print $1}'` | The measured downloaded file size should equal the expected size of 10240 KB, confirming a complete and correct download for each iteration. |
| 9 | Verify download ID is embedded in file locator URL (Per Iteration) | Confirm that the download ID from the API response matches the downloadId field in the event, and that the download ID string is present within the fileLocator URL. | The event download ID should match the API-returned download ID, and the download ID should be present in the fileLocator URL, confirming correct download tracking for each iteration. |
| 10 | Delete first downloaded package from device (Per Iteration) | Delete the downloaded validation file from the device storage using the DownloadManager delete API, providing the fileLocator URL obtained from the first download event. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.delete", "params": {"fileLocator": "<filelocator_url>"}}` | The delete API should return SUCCESS for each iteration. |
| 11 | Verify first downloaded file is deleted from device storage (Per Iteration) | Verify that the downloaded file no longer exists on the DUT by executing an SSH file listing command against the file path extracted from the fileLocator URL. <br>`ls -l <file_path>` | The file listing command should return a "No such file or directory" response, confirming that the package was successfully removed from device storage for each iteration. |
| 12 | Initiate re-download of same validation file (Per Iteration) | Re-download the same 10 MB validation file ("10_MB_File.bin") from the configured URL using the DownloadManager download API to verify that the file can be downloaded again after deletion. Wait 15 seconds after initiating the re-download. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/10_MB_File.bin"}}` | The re-download API should return SUCCESS and provide a new unique download ID for each iteration. |
| 13 | Verify onAppDownloadStatus event for re-download (Per Iteration) | Monitor the event listener buffer for up to 120 seconds to receive the onAppDownloadStatus event for the re-download. Parse the event to extract the new downloadId and fileLocator fields. | The onAppDownloadStatus event should be received for the re-download within the monitoring period for each iteration. |
| 14 | Verify re-download ID is unique and file size matches expected (Per Iteration) | Confirm that the re-download ID has not appeared in any previous iteration. Measure the size of the re-downloaded file via SSH and compare it against the expected 10240 KB. <br>`du -sk <filelocator_url> \| awk '{print $1}'` | The re-download ID should be unique, and the re-downloaded file size should equal 10240 KB, confirming a complete and correct re-download for each iteration. |
| 15 | Verify disk usage remains within acceptable limit after re-download (Per Iteration) | Check the current disk usage of the download staging directory via SSH and verify that it is less than the initial baseline disk usage plus the expected package size (10240 KB) plus the configured `MEMORY_OFFSET` value. <br>`du -sk <file_locator> \| awk '{print $1}'` | The current disk usage should be less than `initial_used_memory + 10240 + MEMORY_OFFSET`, confirming that disk space usage is within acceptable limits after the re-download for each iteration. |
| 16 | Delete re-downloaded package from device (Per Iteration) | Delete the re-downloaded validation file from the device storage using the DownloadManager delete API, providing the fileLocator URL from the re-download event. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.delete", "params": {"fileLocator": "<filelocator_url>"}}` | The delete API should return SUCCESS for each iteration. |
| 17 | Verify re-downloaded file is deleted from device storage (Per Iteration) | Verify that the re-downloaded file no longer exists on the DUT by executing an SSH file listing command against the file path extracted from the re-download fileLocator URL. <br>`ls -l <file_path>` | The file listing command should return a "No such file or directory" response, confirming that the re-downloaded package was successfully removed from device storage for each iteration. |
| 18 | Repeat download, delete, and re-download validation for all iterations | Repeat Steps 5 through 17 for all `AppManager_test_count` (100) configured iterations. | Every iteration should produce a unique download ID for both the initial download and the re-download, correctly measure file sizes at 10240 KB, successfully delete both downloads, and confirm disk usage remains within the configured acceptable limit throughout. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 180 minutes

**Priority** : High

**Release Version** : M151<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
