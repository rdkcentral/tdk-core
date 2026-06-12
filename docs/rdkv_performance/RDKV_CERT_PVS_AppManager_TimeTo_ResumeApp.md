## TestCase ID
RDKV_PERFORMANCE_207
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
To validate that the time taken to resume an AppManager-managed application from the background to the foreground active state is within the expected threshold limit.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager` plugins should be available and activatable on the device.|
|3|`google_bundle`, `keytest_bundle`, and `app_download_url` must be configured in `PerformanceTestVariables`.|
|4|`APPMANAGER_LAUNCH_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be configured in the device config file.|
|5|Time in Test Manager and DUT should be in sync with UTC.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check and Activate Plugins | Check and activate `org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager`. | All plugins in activated state. |
| 2 | Install Both Apps | Install App A (google_bundle) and App B (keytest_bundle) using: `org.rdk.PackageManagerRDKEMS.1.listPackages` + download + install flow. | Both apps installed. |
| 3 | Subscribe to Lifecycle Events | Register a WebSocket listener for `onAppLifecycleStateChanged` from AppManager: <br>`{"jsonrpc":"2.0","id":9,"method":"org.rdk.AppManager.1.register","params":{"event":"onAppLifecycleStateChanged","id":"client.events.1"}}` | Event subscription established. |
| 4 | Launch App A in Foreground | Launch App A: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_A_name>","intent":"","launchArgs":""}}` | App A launched; wait for `APP_STATE_ACTIVE` event. |
| 5 | Launch App B (Move App A to Background) | Launch App B to bring it to foreground: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_B_name>","intent":"","launchArgs":""}}` | App B is in foreground; App A receives `APP_STATE_BACKGROUND` or `APP_STATE_SUSPENDED` event. |
| 6 | Record Resume Start Time | Clear the event buffer. Record the current UTC timestamp immediately before resuming App A. | Resume start time recorded. |
| 7 | Resume App A (Launch from Background) | Launch App A again to bring it back to foreground: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_A_name>","intent":"","launchArgs":""}}` | Resume request submitted. |
| 8 | Wait for APP_STATE_ACTIVE Event for App A | Monitor the `onAppLifecycleStateChanged` event buffer until App A `APP_STATE_ACTIVE` is received (up to 120 seconds). Record the event timestamp. | App A `APP_STATE_ACTIVE` event received. |
| 9 | Calculate and Validate Resume Time | Calculate: resume time = event timestamp - start time (in ms). Retrieve `APPMANAGER_LAUNCH_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` from device config. Validate: resume time < (threshold + offset). | Time taken to resume App A from background is within the configured threshold. |
| 10 | Cleanup — Terminate Both Apps | Terminate both apps: `org.rdk.AppManager.1.terminateApp` for each app. | Both apps terminated. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
