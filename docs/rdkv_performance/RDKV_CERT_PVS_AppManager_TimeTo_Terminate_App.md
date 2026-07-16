## TestCase ID
RDKV_PERFORMANCE_89
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_Terminate_App

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to terminate a running application via the AppManager is within the configured performance threshold, measured from the terminate request to the receipt of the APP_STATE_UNLOADED lifecycle state change event.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. | The app_download_url should point to a reachable location hosting the application bundle. |
| 5 | Configure terminate threshold in device config | `APPMANAGER_TERMINATE_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be set in the device-specific configuration file with appropriate millisecond values. | Threshold and offset values should be correctly configured for performance comparison. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query and activate the required plugins to ensure they are in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All required plugins should be in the activated state. |
| 2 | Download the application bundle | Download the application bundle from the configured URL via the DownloadManager. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` | The download should complete successfully and a download ID should be returned. |
| 3 | Install the application | Install the downloaded application bundle without launching it. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully and appear in the installed packages list. |
| 4 | Launch the application | Send a launch request for the installed application so it is in the active running state prior to the terminate measurement. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The application should be installed and launched successfully, reaching the APP_STATE_ACTIVE lifecycle state. |
| 5 | Subscribe to the lifecycle state change event | Register a WebSocket event listener for onAppLifecycleStateChanged to capture the APP_STATE_UNLOADED event that signals termination completion. <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}}` | Event subscription should be established successfully. |
| 6 | Trigger app termination and record start time | Record the current UTC timestamp as the terminate start time, then send the terminate request to the AppManager. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.google"}}` | The terminate request should be accepted by the AppManager. |
| 7 | Wait for the APP_STATE_UNLOADED lifecycle event | Monitor the event buffer until the onAppLifecycleStateChanged event containing APP_STATE_UNLOADED is received or a 120-second timeout is reached. Extract the completion timestamp from the event payload. | The APP_STATE_UNLOADED event should be received within the timeout period, confirming the application was terminated. |
| 8 | Calculate terminate time and validate against threshold | Compute the elapsed time in milliseconds as the difference between the APP_STATE_UNLOADED event timestamp and the recorded start time. Compare against `APPMANAGER_TERMINATE_THRESHOLD_VALUE` + `THRESHOLD_OFFSET` from device config. | The time taken to terminate the app should be within the range: 0 < time_taken < (APPMANAGER_TERMINATE_THRESHOLD_VALUE + THRESHOLD_OFFSET) milliseconds. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
