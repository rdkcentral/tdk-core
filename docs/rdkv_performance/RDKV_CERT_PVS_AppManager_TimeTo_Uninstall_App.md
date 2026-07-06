## TestCase ID
RDKV_PERFORMANCE_90
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_Uninstall_App

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to uninstall an application via the AppManager is within the configured performance threshold, measured from the uninstall request to the receipt of the onAppUninstalled event.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename (e.g., `com.rdkcentral.google+0.1.0+...`) in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. | The app_download_url should point to a reachable location hosting the application bundle. |
| 5 | Configure uninstall threshold in device config | `APPMANAGER_UNINSTALL_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be set in the device-specific configuration file with appropriate millisecond values. | Threshold and offset values should be correctly configured for performance comparison. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query and activate the required plugins to ensure they are in the activated state before proceeding. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All required plugins should be in the activated state. |
| 2 | Check if the application is already installed | Query the installed packages list to determine whether the application is already present on the device. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be returned successfully. |
| 3 | Download the application bundle | If the application is not already installed, download the application bundle from the configured URL via the DownloadManager. This step is skipped if the application was found to be already installed in the previous step. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` | The download should complete successfully and a download ID should be returned. |
| 4 | Install the application | Install the downloaded application bundle without launching it. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully and appear in the installed packages list. |
| 5 | Subscribe to the uninstall event | Register a WebSocket event listener for the onAppUninstalled event to capture the precise timestamp when uninstall completes. <br>`{"jsonrpc": "2.0", "id": 10, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppUninstalled", "id": "client.events.4"}}` | Event subscription should be established successfully. |
| 6 | Trigger app uninstall and record start time | Record the current UTC timestamp as the uninstall start time, then send the uninstall request. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.uninstall", "params": {"packageId": "com.rdkcentral.google"}}` | The uninstall request should be accepted and processing should begin. |
| 7 | Wait for the onAppUninstalled event and extract completion timestamp | Monitor the event buffer until the onAppUninstalled event is received or a 120-second timeout is reached. Extract the completion timestamp embedded in the event payload. | The onAppUninstalled event should be received within the timeout period, and the completion timestamp should be extractable from the event data. |
| 8 | Calculate uninstall time and validate against threshold | Compute the elapsed time in milliseconds as the difference between the event completion timestamp and the recorded start time. Compare against `APPMANAGER_UNINSTALL_THRESHOLD_VALUE` + `THRESHOLD_OFFSET` from device config. | The time taken to uninstall the app should be within the range: 0 < time_taken < (APPMANAGER_UNINSTALL_THRESHOLD_VALUE + THRESHOLD_OFFSET) milliseconds. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
