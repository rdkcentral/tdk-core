## TestCase ID
RDKV_STABILITY_24
## TestCase Name
RDKV_CERT_RVS_AppManager_Cancel_LargeFile_Download

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DownloadManager correctly cancels an in-progress large file download, emits the onAppDownloadStatus DOWNLOAD_FAILURE event with the correct download identification, successfully deletes the partially downloaded package from the device, and confirms that disk usage is restored to the pre-download level after each cancel and delete operation across all configured iterations.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test before test execution begins. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT_PVS in device config | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the large validation file is hosted. The full download URL is constructed as `app_download_url + Large_Validation_File` ("1_GB_File.bin"). | The app_download_url should point to a reachable and valid hosting location for the large validation file. |
| 4 | Configure AppManager_test_count in StabilityTestVariables | `AppManager_test_count` must be set to the desired number of download cancel and delete iterations in StabilityTestVariables (default: 100). | The AppManager_test_count variable should be configured with a valid integer value. |
| 5 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. This is used to determine the download staging directory and to monitor disk usage. | The file locator path should be correctly configured in the device-specific configuration file. |
| 6 | Configure SSH access parameters in device config | SSH method and credentials must be configured in the device configuration file to allow file existence checks and disk usage monitoring via SSH commands. | SSH parameters should be correctly configured and accessible from the device configuration file. |
| 7 | Confirm required plugins are available | The following plugins must be available and activatable on the device: org.rdk.DownloadManager, org.rdk.AppPackageManager, org.rdk.AppManager, and org.rdk.RDKWindowManager. | All required plugins should be present and activatable on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT_PVS` configuration key. If set to Yes, the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | The device should come back online successfully if reboot was configured. |
| 2 | Verify and activate required plugins | Retrieve the current activation state of org.rdk.DownloadManager, org.rdk.AppPackageManager, org.rdk.AppManager, and org.rdk.RDKWindowManager. Activate any plugin that is not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppPackageManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.RDKWindowManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All four required plugins should be in the activated state before test execution proceeds. |
| 3 | Record initial disk usage of download directory | Record the initial disk usage of the download staging directory via SSH to establish a baseline for post-deletion disk usage comparison. <br>`du -sk <file_locator> \| awk '{print $1}'` | The initial disk usage value should be retrieved successfully and stored as the baseline for disk usage validation. |
| 4 | Subscribe to onAppDownloadStatus event | Register a WebSocket event listener to subscribe to the onAppDownloadStatus event from org.rdk.DownloadManager. Wait 5 seconds after registration. <br>`{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.DownloadManager.1.register", "params": {"event": "onAppDownloadStatus", "id": "client.events.1"}}` | The onAppDownloadStatus event subscription should be established successfully and the WebSocket event listener should be active. |
| 5 | Clear event buffer and initiate large file download (Per Iteration) | For each of the `AppManager_test_count` (100) iterations, clear the event buffer and initiate the download of the large validation file ("1_GB_File.bin") from the configured URL using the DownloadManager download API. Wait 15 seconds after initiating the download. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<Large_Validation_File>"}}` | The download API should return SUCCESS and provide a download ID for each iteration. |
| 6 | Check download progress is in progress (Per Iteration) | Wait 2 seconds after the download initiation, then query the download progress using the DownloadManager progress API to verify the download has started but is not yet complete (progress > 0 and < 100). <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.progress", "params": {"downloadId": "<download_id>"}}` | The download progress should be greater than 0 and less than 100, confirming the download is actively in progress for each iteration. |
| 7 | Cancel the in-progress download (Per Iteration) | Cancel the active download using the DownloadManager cancel API with the download ID obtained from the download initiation response. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.cancel", "params": {"downloadId": "<download_id>"}}` | The cancel API should return SUCCESS for each iteration. |
| 8 | Monitor event buffer for DOWNLOAD_FAILURE cancellation event (Per Iteration) | Monitor the event listener buffer for up to 120 seconds after the cancellation request to receive the onAppDownloadStatus event carrying the DOWNLOAD_FAILURE status, which confirms the download was cancelled. | The onAppDownloadStatus event with DOWNLOAD_FAILURE status should be received within the monitoring period for each iteration. |
| 9 | Verify cancellation event download ID and file locator (Per Iteration) | Parse the received onAppDownloadStatus cancellation event to extract and verify the downloadId and fileLocator fields. The event download ID must match the download ID from the download initiation response, and the download ID must be present within the fileLocator URL string. <br>`{"jsonrpc": "2.0", "method": "client.events.1.onAppDownloadStatus", "params": {"downloadStatus": "[{\"downloadId\": \"<id>\", \"fileLocator\": \"<url>\"}]"}}` | The cancellation event download ID should match the initiated download ID, and the download ID should be present in the fileLocator URL, confirming the event relates to the correct download. |
| 10 | Delete the partially downloaded package from device (Per Iteration) | Delete the partially downloaded file from the device storage using the DownloadManager delete API, providing the fileLocator URL obtained from the cancellation event. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.delete", "params": {"fileLocator": "<filelocator_url>"}}` | The delete API should return SUCCESS for each iteration. |
| 11 | Verify partial download file is deleted from device storage (Per Iteration) | Verify that the partially downloaded file no longer exists on the DUT by executing an SSH file listing command against the fileLocator URL path. <br>`ls -l <filelocator_url>` | The file listing command should return a "No such file or directory" response, confirming that the partially downloaded package was successfully removed from device storage for each iteration. |
| 12 | Verify disk usage is restored to baseline after deletion (Per Iteration) | Check the current disk usage of the download staging directory via SSH and verify that it has not exceeded the initial baseline disk usage recorded before testing, confirming that no residual storage consumption remains after the cancel and delete operations. <br>`du -sk <file_locator> \| awk '{print $1}'` | The current disk usage should be less than or equal to the initial baseline disk usage value, confirming that disk space is correctly reclaimed after each cancel and delete cycle. |
| 13 | Repeat download cancel and delete validation for all iterations | Repeat Steps 5 through 12 for all `AppManager_test_count` (100) configured iterations. | Every iteration should successfully download the large file to an in-progress state, cancel the download, receive the DOWNLOAD_FAILURE cancellation event with correct identification, delete the partial package, and confirm disk usage is restored to the initial baseline. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 150 minutes

**Priority** : High

**Release Version** : M151<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
