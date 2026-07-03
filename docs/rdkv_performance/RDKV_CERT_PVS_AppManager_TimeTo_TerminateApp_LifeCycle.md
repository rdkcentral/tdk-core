## TestCase ID
RDKV_PERFORMANCE_102
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_TerminateApp_LifeCycle

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To measure and validate the time taken for each lifecycle state transition (APP_STATE_PAUSED, APP_STATE_TERMINATING, APP_STATE_UNLOADED) following an AppManager terminateApp request, and verify that each transition time is within the configured performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT_PVS in device config | `PRE_REQ_REBOOT_PVS` must be configured as `Yes` to reboot the device before test execution. The script always passes "yes" to `pre_requisite_reboot`. | The device should reboot successfully before the test begins. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted in PerformanceTestVariables. | The app_download_url should point to a reachable hosting location. |
| 5 | Configure terminate threshold in device config | `APPMANAGER_TERMINATE_EVENT_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be set in the device-specific configuration file. | Threshold and offset values should be correctly configured for performance comparison. |
| 6 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path where downloaded packages are stored on the device. | The file locator path should be correctly configured. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Check the activation state of the required plugins: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager. Activate any that are not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@<plugin_name>"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All three required plugins should be in activated state. |
| 2 | Check if the application is already installed | Query the installed packages list to determine whether the application is already present on the device. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be returned successfully. |
| 3 | Download the application bundle | If the application is not already installed, download the application bundle from the configured URL via the DownloadManager. This step is skipped if the application was found to be already installed in the previous step. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` | The download should complete successfully and a download ID should be returned. |
| 4 | Install the application | Install the downloaded application bundle without launching it. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully and appear in the installed packages list. |
| 5 | Launch the application | Send a launch request for the installed application via AppManager. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The application should be installed and launched successfully and reach APP_STATE_ACTIVE. |
| 6 | Subscribe to lifecycle state change event | Register a WebSocket event listener on the Thunder JSON-RPC endpoint for onAppLifecycleStateChanged. Wait 20 seconds after registration to ensure the listener is ready. <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}}` | Event subscription should be established successfully. |
| 7 | Trigger terminateApp and record start time | Record the current UTC timestamp as the terminate start time, then send the terminateApp request to the AppManager. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.google"}}` | The terminateApp request should be accepted by the AppManager and return SUCCESS. |
| 8 | Monitor event buffer for terminate lifecycle events | Monitor the onAppLifecycleStateChanged event buffer for up to 120 seconds. Record the timestamps of APP_STATE_PAUSED, APP_STATE_TERMINATING, and APP_STATE_UNLOADED events as they arrive. The loop exits when APP_STATE_UNLOADED is received. | All three terminate lifecycle events (APP_STATE_PAUSED, APP_STATE_TERMINATING, APP_STATE_UNLOADED) should be received within the timeout period. |
| 9 | Verify all terminate lifecycle states received | Confirm that all three expected lifecycle state transitions were received: APP_STATE_PAUSED, APP_STATE_TERMINATING, and APP_STATE_UNLOADED for com.rdkcentral.google. <br>Example event: `{"jsonrpc": "2.0", "method": "client.events.1.onAppLifecycleStateChanged", "params": {"appId": "com.rdkcentral.google", "newState": "APP_STATE_UNLOADED", "oldState": "APP_STATE_TERMINATING", "errorReason": "APP_ERROR_NONE"}}` | All three terminate lifecycle state transitions should be confirmed for the application. |
| 10 | Calculate transition times and validate against threshold | Compute the elapsed time in milliseconds for each transition: terminate start → APP_STATE_PAUSED, APP_STATE_PAUSED → APP_STATE_TERMINATING and APP_STATE_TERMINATING → APP_STATE_UNLOADED. Compare each against `APPMANAGER_TERMINATE_EVENT_THRESHOLD_VALUE` + `THRESHOLD_OFFSET` from device config. | Each individual transition time should be within the range: 0 < time < (APPMANAGER_TERMINATE_EVENT_THRESHOLD_VALUE + THRESHOLD_OFFSET) milliseconds. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M150<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
