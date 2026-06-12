## TestCase ID
RDKV_PERFORMANCE_196
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeToRepeatedLaunch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to launch an AppManager-managed application across 3 repeated launch-terminate cycles is consistently within the expected threshold limit.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager` plugins should be available and activatable on the device.|
|3|`google_bundle` and `app_download_url` must be configured in `PerformanceTestVariables`.|
|4|`APPMANAGER_LAUNCH_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be configured in the device config file.|
|5|Time in Test Manager and DUT should be in sync with UTC.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check and Activate Plugins | Check and activate `org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager`. | All plugins in activated state. |
| 2 | Install App | Check `org.rdk.PackageManagerRDKEMS.1.listPackages`. Download and install if not installed. | App installed successfully. |
| 3 | Subscribe to Lifecycle Events | Register a WebSocket listener for `onAppLifecycleStateChanged` from AppManager: <br>`{"jsonrpc":"2.0","id":9,"method":"org.rdk.AppManager.1.register","params":{"event":"onAppLifecycleStateChanged","id":"client.events.1"}}` | Event subscription established. |
| 4 | Iteration 1 — Launch App (Timed) | Record UTC timestamp. Launch the app: `org.rdk.AppManager.launchApp`. Wait for `APP_STATE_ACTIVE` event (up to 120 seconds). Record event timestamp. Calculate launch time in milliseconds. Terminate app: `org.rdk.AppManager.1.terminateApp`. | App launched and terminated. Launch time recorded. |
| 5 | Iteration 2 — Relaunch App (Timed) | Repeat the same launch-terminate cycle and record the second launch time. | App launched and terminated. Second launch time recorded. |
| 6 | Iteration 3 — Relaunch App (Timed) | Repeat the same launch-terminate cycle and record the third launch time. | App launched and terminated. Third launch time recorded. |
| 7 | Validate All Launch Times | Retrieve `APPMANAGER_LAUNCH_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` from device config. Validate that all 3 launch times are within (threshold + offset). | All 3 repeated launch times are within the configured `APPMANAGER_LAUNCH_THRESHOLD_VALUE`. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
