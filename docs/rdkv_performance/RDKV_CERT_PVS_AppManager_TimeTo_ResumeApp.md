## TestCase ID
RDKV_PERFORMANCE_5
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_ResumeApp

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to resume a background application to the foreground via the AppManager is within the configured performance threshold, measured from the resume launch request to the receipt of the APP_STATE_ACTIVE lifecycle state change event.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Confirm required plugins are available | The following plugins must be present and activatable: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, org.rdk.AppManager. | All required plugins should be available in the build. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the first application bundle filename (App A) in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name for App A. |
| 4 | Configure keytest_bundle in PerformanceTestVariables | `keytest_bundle` must be set to the second application bundle filename (App B) in PerformanceTestVariables. | The keytest_bundle variable should be configured with a valid application bundle name for App B. |
| 5 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundles are hosted. | The app_download_url should point to a reachable hosting location. |
| 6 | Configure resume threshold in device config | The device-specific configuration file must contain threshold and offset values used for resume time validation. | Threshold and offset configuration should be present for performance comparison. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query and activate the required plugins to ensure they are in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All required plugins should be in the activated state. |
| 2 | Install both App A and App B | Download and install both the google app bundle (App A) and the keytest app bundle (App B) without launching either. <br>For each app — Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<bundle_name>"}}` <br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "<app_id>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | Both applications should be installed successfully and available in the installed packages list. |
| 3 | Subscribe to the lifecycle state change event | Register a WebSocket event listener for onAppLifecycleStateChanged to capture state transitions for both apps. <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}}` | Event subscription should be established successfully. |
| 4 | Launch App A and wait for active state | Send a launch request for App A and wait until the onAppLifecycleStateChanged event confirms it has reached APP_STATE_ACTIVE. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<app_A_id>", "intent": "", "launchArgs": ""}}` | App A should launch successfully and the APP_STATE_ACTIVE event should be received. |
| 5 | Launch App B to move App A to background | Send a launch request for App B. App A should transition to a background or suspended state. Wait for the onAppLifecycleStateChanged event confirming App A has moved to APP_STATE_BACKGROUND or APP_STATE_SUSPENDED. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<app_B_id>", "intent": "", "launchArgs": ""}}` | App B should become active and App A should transition to a background state, confirmed by the lifecycle event. |
| 6 | Resume App A and record start time | Clear the event buffer, record the current UTC timestamp as the resume start time, then send a launch request for App A to bring it back to the foreground. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<app_A_id>", "intent": "", "launchArgs": ""}}` | The resume launch request should be accepted by the AppManager. |
| 7 | Wait for App A APP_STATE_ACTIVE event | Monitor the event buffer until the onAppLifecycleStateChanged event containing APP_STATE_ACTIVE for App A is received or a 120-second timeout is reached. Extract the completion timestamp from the event payload. | App A should transition back to the APP_STATE_ACTIVE state and the lifecycle event should be received within the timeout. |
| 8 | Calculate resume time and validate against threshold | Compute the elapsed time in milliseconds between the resume launch request timestamp and the APP_STATE_ACTIVE event timestamp. Compare against the configured threshold and offset values from the device config. | The time taken to resume the app should be within the configured performance threshold range. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
