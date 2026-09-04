## TestCase ID
RDKV_STABILITY_25
## TestCase Name
RDKV_CERT_RVS_AppManager_Download_InvalidURL

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DownloadManager correctly rejects download requests made with an invalid URL by returning a failure response and emitting the onAppDownloadStatus DOWNLOAD_FAILURE event, while subsequently accepting and completing a valid URL download successfully, with the downloaded package deleted and confirmed absent from device storage, across all configured iterations.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test before test execution begins. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT_PVS in device config | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle filename. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. The valid download URL is constructed as `app_download_url.rstrip("/") + "/" + google_bundle`. | The app_download_url should point to a reachable and valid hosting location. |
| 5 | Confirm invalid_download_url is set in PerformanceTestVariables | `invalid_download_url` must be set to a non-reachable URL to simulate a download failure. The default value is `"http://invalid.com/"`. The failing download URL is constructed as `invalid_download_url + google_bundle`. | The invalid_download_url should be configured with a URL that is unreachable or does not serve the requested bundle. |
| 6 | Configure AppManager_test_count in StabilityTestVariables | `AppManager_test_count` must be set to the desired number of invalid and valid URL download iterations in StabilityTestVariables (default: 100). | The AppManager_test_count variable should be configured with a valid integer value. |
| 7 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. | The file locator path should be correctly configured in the device-specific configuration file. |
| 8 | Configure SSH access parameters in device config | SSH method and credentials must be configured in the device configuration file to allow file existence verification on the DUT via SSH commands after the valid download and delete operations. | SSH parameters should be correctly configured and accessible from the device configuration file. |
| 9 | Confirm required plugins are available | The following plugins must be available and activatable on the device: org.rdk.DownloadManager, org.rdk.AppPackageManager, org.rdk.AppManager, and org.rdk.RDKWindowManager. | All required plugins should be present and activatable on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT_PVS` configuration key. If set to Yes, the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | The device should come back online successfully if reboot was configured. |
| 2 | Verify and activate required plugins | Retrieve the current activation state of org.rdk.DownloadManager, org.rdk.AppPackageManager, org.rdk.AppManager, and org.rdk.RDKWindowManager. Activate any plugin that is not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppPackageManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.RDKWindowManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All four required plugins should be in the activated state before test execution proceeds. |
| 3 | Subscribe to onAppDownloadStatus event | Register a WebSocket event listener to subscribe to the onAppDownloadStatus event from org.rdk.DownloadManager. Wait 5 seconds after registration. <br>`{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.DownloadManager.1.register", "params": {"event": "onAppDownloadStatus", "id": "client.events.1"}}` | The onAppDownloadStatus event subscription should be established successfully and the WebSocket event listener should be active. |
| 4 | Clear event buffer (Per Iteration) | For each of the `AppManager_test_count` (100) iterations, clear the event listener buffer to discard any stale events before the download operations for that iteration. | The event buffer should be cleared successfully at the start of each iteration. |
| 5 | Attempt download from invalid URL (Per Iteration) | Attempt to initiate a download using the DownloadManager download API with the configured invalid URL (`http://invalid.com/<google_bundle>`). This request is expected to fail. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "http://invalid.com/<google_bundle>"}}` | The download API should return a failure response, indicating the DownloadManager correctly rejected the invalid URL for each iteration. |
| 6 | Verify DOWNLOAD_FAILURE event is received for invalid URL (Per Iteration) | Monitor the event listener buffer for up to 120 seconds to verify that an onAppDownloadStatus event carrying the DOWNLOAD_FAILURE status is received, confirming the DownloadManager correctly reported the failure for the invalid URL download attempt. <br>`{"jsonrpc": "2.0", "method": "client.events.1.onAppDownloadStatus", "params": {"downloadStatus": "[{\"downloadStatus\": \"DOWNLOAD_FAILURE\"}]"}}` | The onAppDownloadStatus event with DOWNLOAD_FAILURE status should be received within the monitoring period for each iteration. |
| 7 | Clear event buffer after invalid URL failure (Per Iteration) | Clear the event listener buffer after receiving the DOWNLOAD_FAILURE event to prepare for the valid URL download attempt. | The event buffer should be cleared successfully before initiating the valid URL download. |
| 8 | Download application bundle from valid URL (Per Iteration) | Initiate the download of the application bundle from the valid configured download URL using the DownloadManager download API. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<valid_app_download_url>/<google_bundle>"}}` | The download API should return SUCCESS and provide a valid download ID for each iteration. |
| 9 | Verify successful onAppDownloadStatus event for valid URL (Per Iteration) | Monitor the event listener buffer for up to 120 seconds to receive the onAppDownloadStatus event for the valid URL download. Verify the event does not carry DOWNLOAD_FAILURE status, and parse the event to extract the downloadId and fileLocator fields. Confirm the event download ID matches the download ID returned by the download API, and the download ID is present in the fileLocator URL. <br>`{"jsonrpc": "2.0", "method": "client.events.1.onAppDownloadStatus", "params": {"downloadStatus": "[{\"downloadId\": \"<id>\", \"fileLocator\": \"<url>\"}]"}}` | The onAppDownloadStatus event should not contain DOWNLOAD_FAILURE, the download ID should match the API response, and the download ID should be present in the fileLocator URL for each iteration. |
| 10 | Delete downloaded package from device (Per Iteration) | Delete the successfully downloaded application bundle from the device storage using the DownloadManager delete API, providing the fileLocator URL obtained from the valid download event. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.delete", "params": {"fileLocator": "<filelocator_url>"}}` | The delete API should return SUCCESS for each iteration. |
| 11 | Verify downloaded package file is deleted from device storage (Per Iteration) | Verify that the downloaded package file no longer exists on the DUT by executing an SSH file listing command against the fileLocator URL path. <br>`ls -l <filelocator_url>` | The file listing command should return a "No such file or directory" response, confirming that the package was successfully deleted from device storage for each iteration. |
| 12 | Repeat invalid and valid URL download validation for all iterations | Repeat Steps 4 through 11 for all `AppManager_test_count` (100) configured iterations. | Every iteration should successfully reject the invalid URL download with a DOWNLOAD_FAILURE event, complete the valid URL download, receive the correct onAppDownloadStatus event, delete the package, and confirm file removal from device storage. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 170 minutes

**Priority** : High

**Release Version** : M151<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
