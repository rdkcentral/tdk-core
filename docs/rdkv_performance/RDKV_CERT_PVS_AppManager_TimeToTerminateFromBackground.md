## TestCase ID
RDKV_PERFORMANCE_199
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
To validate that the time taken to terminate an AppManager-managed application while it is running in the background is within the expected threshold limit.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager` plugins should be available and activatable on the device.|
|3|`google_bundle`, `keytest_bundle`, and `app_download_url` must be configured in `PerformanceTestVariables`.|
|4|`APPMANAGER_LAUNCH_THRESHOLD_VALUE` (used as terminate threshold) and `THRESHOLD_OFFSET` must be configured in the device config file.|
|5|Time in Test Manager and DUT should be in sync with UTC.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check and Activate Plugins | Check and activate `org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager`. | All plugins in activated state. |
| 2 | Install Both Apps | Install `google_bundle` (App A) and `keytest_bundle` (App B) if not already installed. | Both apps installed. |
| 3 | Subscribe to Lifecycle Events | Register a WebSocket listener for `onAppLifecycleStateChanged` from AppManager: <br>`{"jsonrpc":"2.0","id":9,"method":"org.rdk.AppManager.1.register","params":{"event":"onAppLifecycleStateChanged","id":"client.events.1"}}` | Event subscription established. |
| 4 | Launch App A in Foreground | Launch App A using AppManager: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_A_name>","intent":"","launchArgs":""}}` | App A launched. Wait for `APP_STATE_ACTIVE` event. Wait 10 seconds. |
| 5 | Launch App B (Move App A to Background) | Launch App B: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_B_name>","intent":"","launchArgs":""}}` | App B is in foreground; App A moves to background state (`APP_STATE_BACKGROUND` or `APP_STATE_SUSPENDED`). |
| 6 | Record Terminate Start Time | Clear the event buffer. Record the current UTC timestamp immediately before sending the terminate request for App A. | Terminate start time recorded. |
| 7 | Terminate App A from Background | Send terminate request for App A while it is in background: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_A_name>"}}` | Terminate request submitted. |
| 8 | Wait for Termination Lifecycle Event | Monitor the `onAppLifecycleStateChanged` event buffer until the termination event for App A is received (up to 120 seconds). Record the event timestamp. | Termination lifecycle event received for App A. |
| 9 | Calculate and Validate Terminate Time | Calculate: terminate time = event timestamp - terminate start time (in ms). Retrieve threshold from device config. Validate that the time is within the acceptable threshold. | Time taken to terminate the app from background is within the configured threshold. |
| 10 | Cleanup — Terminate App B | Terminate App B as cleanup: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_B_name>"}}` | App B terminated. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
