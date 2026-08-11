## TestCase ID
RDKV_PERFORMANCE_81
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeToTerminateFromBackground

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to terminate a background application via the AppManager is within the configured performance threshold, measured from the terminate request to the receipt of the corresponding lifecycle state change event.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the first application bundle filename (App A) in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 3 | Configure keytest_bundle in PerformanceTestVariables | `keytest_bundle` must be set to the second application bundle filename (App B) in PerformanceTestVariables. | The keytest_bundle variable should be configured with a valid application bundle name for App B. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundles are hosted. | The app_download_url should point to a reachable hosting location. |
| 5 | Configure terminate threshold in device config | `APPMANAGER_TERMINATE_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be set in the device-specific configuration file. | Threshold and offset values should be correctly configured for performance comparison. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query and activate all required plugins to ensure they are in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All required plugins should be in the activated state. |
| 2 | Download both application bundles | Download both the google app bundle (App A) and the keytest app bundle (App B) from the configured URLs via the DownloadManager without launching either. <br>App A: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<bundle_name_A>"}}` <br><br>App B: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<bundle_name_B>"}}` | Both downloads should complete successfully and download IDs should be returned. |
| 3 | Install both applications | Install both downloaded application bundles without launching them. <br>App A: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "<app_A_id>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id_A>"}}` <br><br>App B: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "<app_B_id>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id_B>"}}` | Both applications should be installed successfully. |
| 4 | Subscribe to the lifecycle state change event | Register a WebSocket event listener for onAppLifecycleStateChanged to monitor both app state transitions. <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}}` | Event subscription should be established successfully. |
| 5 | Launch App A and wait for active state | Launch App A and wait for its onAppLifecycleStateChanged event to confirm it reached APP_STATE_ACTIVE. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<app_A_id>", "intent": "", "launchArgs": ""}}` | App A should reach APP_STATE_ACTIVE and the lifecycle event should be received. |
| 6 | Launch App B to push App A to background | Launch App B so that App A is moved to a background or suspended state. Wait for the onAppLifecycleStateChanged event confirming App A is in APP_STATE_BACKGROUND or APP_STATE_SUSPENDED. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<app_B_id>", "intent": "", "launchArgs": ""}}` | App B should become active and App A should be confirmed as moved to a background state. |
| 7 | Terminate App A from background and record start time | Clear the event buffer, record the current UTC timestamp as the terminate start time, then send the terminate request for App A which is currently in the background. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "<app_A_id>"}}` | The terminate request should be accepted by the AppManager for App A in its background state. |
| 8 | Wait for lifecycle event and calculate terminate time | Monitor the event buffer until the terminate completion event is received or a 120-second timeout is reached. Compute the elapsed time in milliseconds between the event timestamp and the recorded start time. Compare against `APPMANAGER_TERMINATE_THRESHOLD_VALUE` + `THRESHOLD_OFFSET` from device config. | The terminate-from-background time should be within the configured performance threshold range. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
