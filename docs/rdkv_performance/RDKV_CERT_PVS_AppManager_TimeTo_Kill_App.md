## TestCase ID
RDKV_PERFORMANCE_97
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_Kill_App

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To measure and validate the total time taken from the killApp request until the APP_STATE_UNLOADED lifecycle event is received for the application, and verify that the time is within the configured performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT_PVS in device config | `PRE_REQ_REBOOT_PVS` must be configured as `Yes` to reboot the device before test execution. The script always passes "yes" to `pre_requisite_reboot`. | The device should reboot successfully before the test begins. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted in PerformanceTestVariables. | The app_download_url should point to a reachable hosting location. |
| 5 | Configure kill threshold in device config | `APPMANAGER_KILL_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be set in the device-specific configuration file. | Threshold and offset values should be correctly configured for performance comparison. |
| 6 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path where downloaded packages are stored on the device. | The file locator path should be correctly configured. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Check the activation state of the required plugins: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager. Activate any that are not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@<plugin_name>"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All three required plugins should be in activated state. |
| 2 | Install and launch the application | Check if com.rdkcentral.google is already installed. If not, download and install it via DownloadManager and PackageManagerRDKEMS, then launch it via AppManager. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The application should be installed and launched successfully and reach APP_STATE_ACTIVE. |
| 3 | Subscribe to lifecycle state change event | Register a WebSocket event listener on the Thunder JSON-RPC endpoint for the onAppLifecycleStateChanged event from org.rdk.AppManager. Wait 10 seconds after registration to ensure the listener is ready. <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}}` | The event subscription should be established successfully. |
| 4 | Trigger killApp and record start time | Record the current UTC timestamp as the kill start time, then send the killApp request to the AppManager. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.killApp", "params": {"appId": "com.rdkcentral.google"}}` | The killApp request should return SUCCESS and the application kill process should begin. |
| 5 | Wait for the APP_STATE_UNLOADED event | Monitor the onAppLifecycleStateChanged event buffer for up to 120 seconds until the APP_STATE_UNLOADED event for com.rdkcentral.google is received. Record the event timestamp. <br>Example event: `{"jsonrpc": "2.0", "method": "client.events.1.onAppLifecycleStateChanged", "params": {"appId": "com.rdkcentral.google", "newState": "APP_STATE_UNLOADED", "oldState": "APP_STATE_TERMINATING", "errorReason": "APP_ERROR_NONE"}}` | The APP_STATE_UNLOADED lifecycle event should be received for com.rdkcentral.google within the timeout period. |
| 6 | Calculate kill time and validate against threshold | Compute the elapsed time in milliseconds as the difference between the APP_STATE_UNLOADED event timestamp and the recorded killApp start time. Compare against `APPMANAGER_KILL_THRESHOLD_VALUE` + `THRESHOLD_OFFSET` from device config. | The time taken from killApp to APP_STATE_UNLOADED should be within the range: 0 < time < (APPMANAGER_KILL_THRESHOLD_VALUE + THRESHOLD_OFFSET) milliseconds. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M150<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
