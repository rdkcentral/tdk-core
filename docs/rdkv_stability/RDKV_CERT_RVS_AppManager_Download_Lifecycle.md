## TestCase ID
RDKV_STABILITY_23
## TestCase Name
RDKV_CERT_RVS_AppManager_Download_Lifecycle

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the DownloadManager correctly downloads an application bundle, emits the onAppDownloadStatus event with a unique download ID and correct file locator path for each iteration, and successfully deletes the downloaded package from the device storage, confirming the file is no longer present after deletion, across all configured iterations.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test before test execution begins. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT_PVS in device config | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle filename. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. The full download URL is constructed as `app_download_url + "/" + google_bundle`. | The app_download_url should point to a reachable and valid hosting location. |
| 5 | Configure AppManager_test_count in StabilityTestVariables | `AppManager_test_count` must be set to the desired number of download and delete iterations in StabilityTestVariables (default: 100). | The AppManager_test_count variable should be configured with a valid integer value. |
| 6 | Configure SSH access parameters in device config | SSH method and credentials must be configured in the device configuration file to allow the test to verify file deletion on the DUT via SSH commands. | SSH parameters should be correctly configured and accessible from the device configuration file. |
| 7 | Confirm required plugins are available | The following plugins must be available and activatable on the device: org.rdk.DownloadManager, org.rdk.AppPackageManager, org.rdk.AppManager, and org.rdk.RDKWindowManager. | All required plugins should be present and activatable on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT_PVS` configuration key. If set to Yes, the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | The device should come back online successfully if reboot was configured. |
| 2 | Verify and activate required plugins | Retrieve the current activation state of org.rdk.DownloadManager, org.rdk.AppPackageManager, org.rdk.AppManager, and org.rdk.RDKWindowManager. Activate any plugin that is not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppPackageManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.RDKWindowManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All four required plugins should be in the activated state before test execution proceeds. |
| 3 | Subscribe to onAppDownloadStatus event | Register a WebSocket event listener to subscribe to the onAppDownloadStatus event from org.rdk.DownloadManager. Wait 5 seconds after registration to ensure the listener is ready. <br>`{"jsonrpc": "2.0", "id": 2, "method": "org.rdk.DownloadManager.1.register", "params": {"event": "onAppDownloadStatus", "id": "client.events.1"}}` | The onAppDownloadStatus event subscription should be established successfully and the WebSocket event listener should be active. |
| 4 | Download application bundle (Per Iteration) | For each of the `AppManager_test_count` (100) iterations, initiate the download of the application bundle from the configured download URL using the DownloadManager download API. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` | The download API should return SUCCESS and provide a unique download ID for each iteration. |
| 5 | Monitor event buffer for onAppDownloadStatus (Per Iteration) | Monitor the event listener buffer for up to 120 seconds after initiating the download to receive the onAppDownloadStatus event confirming the download completion. | The onAppDownloadStatus event should be received within the monitoring period for each iteration. |
| 6 | Verify unique download ID and parse file locator (Per Iteration) | Parse the received onAppDownloadStatus event to extract the downloadId and fileLocator fields from the event payload. Verify that the download ID is unique and has not appeared in any previous iteration, and that the download ID is embedded in the fileLocator URL. <br>`{"jsonrpc": "2.0", "method": "client.events.1.onAppDownloadStatus", "params": {"downloadStatus": "[{\"downloadId\": \"<id>\", \"fileLocator\": \"<url>\"}]"}}` | The download ID should be unique across all previous iterations, and the fileLocator URL should contain the download ID, confirming correct download identification. |
| 7 | Delete downloaded package from device (Per Iteration) | Delete the downloaded application bundle from the device storage using the DownloadManager delete API, providing the fileLocator URL obtained from the onAppDownloadStatus event. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.delete", "params": {"fileLocator": "<filelocator_url>"}}` | The delete API should return SUCCESS for each iteration. |
| 8 | Verify package file is deleted from device storage (Per Iteration) | Verify that the downloaded package file no longer exists on the DUT by executing an SSH file listing command against the file path extracted from the fileLocator URL. <br>`ls -l <file_path>` | The file listing command should return a "No such file or directory" response, confirming that the package was successfully deleted from device storage for each iteration. |
| 9 | Repeat download and delete validation for all iterations | Repeat Steps 4 through 8 for all `AppManager_test_count` (100) configured iterations. | Every iteration should successfully download the application bundle, receive the onAppDownloadStatus event with a unique download ID, delete the package, and confirm the file is no longer present on the device. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 150 minutes

**Priority** : High

**Release Version** : M151<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
