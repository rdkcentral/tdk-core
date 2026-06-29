## TestCase ID
RDKV_PERFORMANCE_84
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_Install_App

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to install an application bundle via the PackageManagerRDKEMS is within the configured performance threshold, measured from the install request to the receipt of the onAppInstalled event.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Confirm required plugins are available | The following plugins must be present and activatable: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS. | All required plugins should be available in the build. |
| 3 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 4 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 5 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. | The app_download_url should point to a reachable hosting location. |
| 6 | Configure install threshold in device config | `APPMANAGER_INSTALL_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be set in the device-specific configuration file with appropriate millisecond values. | Threshold and offset values should be correctly configured for performance comparison. |
| 7 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the device where downloaded packages are stored. | The file locator path should be correctly configured in the device-specific config file. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query and activate the DownloadManager and PackageManagerRDKEMS plugins. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | DownloadManager and PackageManagerRDKEMS should be in the activated state. |
| 2 | Check if the application is already installed | Query the list of installed packages to determine if the application is already present on the device. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be returned successfully. |
| 3 | Uninstall existing application if present | If the application is already installed, uninstall it to ensure a clean install measurement. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.uninstall", "params": {"packageId": "com.rdkcentral.google"}}` | The application should be uninstalled successfully, ensuring a fresh installation can be measured. |
| 4 | Download the application bundle | Download the application bundle from the configured URL and record the download ID from the result. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` | The download should complete successfully. The download ID should be returned for constructing the file locator path. |
| 5 | Subscribe to the install event | Register a WebSocket event listener for onAppInstalled to capture the precise timestamp when installation completes. <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppInstalled", "id": "client.events.1"}}` | Event subscription should be established successfully. |
| 6 | Trigger app installation and record start time | Construct the file locator path from `PACKAGEMANAGER_FILE_LOCATOR` and the download ID, record the current UTC timestamp as the install start time, then send the install request. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/<download_id>"}}` | The install request should be accepted by the PackageManagerRDKEMS. |
| 7 | Wait for the onAppInstalled event and extract completion timestamp | Monitor the event buffer until the onAppInstalled event is received or a 120-second timeout is reached. Extract the completion timestamp embedded in the event payload. | The onAppInstalled event should be received within the timeout, confirming installation completed. |
| 8 | Calculate install time and validate against threshold | Compute the elapsed time in milliseconds as the difference between the onAppInstalled event timestamp and the recorded start time. Compare against `APPMANAGER_INSTALL_THRESHOLD_VALUE` + `THRESHOLD_OFFSET` from device config. | The time taken to install the app should be within the range: 0 < time_taken < (APPMANAGER_INSTALL_THRESHOLD_VALUE + THRESHOLD_OFFSET) milliseconds. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
