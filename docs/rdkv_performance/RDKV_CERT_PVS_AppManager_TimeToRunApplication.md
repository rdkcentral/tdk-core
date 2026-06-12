## TestCase ID
RDKV_PERFORMANCE_197
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeToRunApplication
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the total time taken from issuing a launch request to the application reaching an actively running state via AppManager is within the expected threshold limit.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager` plugins should be available and activatable on the device.|
|3|`google_bundle` and `app_download_url` must be configured in `PerformanceTestVariables`.|
|4|`APPMANAGER_RUNAPP_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be configured in the device config file (default: 3500ms and 500ms respectively).|
|5|Time in Test Manager and DUT should be in sync with UTC.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check and Activate Plugins | Check and activate `org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager`. | All plugins in activated state. |
| 2 | Install App | Check `org.rdk.PackageManagerRDKEMS.1.listPackages`. Download and install if not installed. | App installed successfully. |
| 3 | Subscribe to Lifecycle Events | Register a WebSocket listener for `onAppLifecycleStateChanged` from AppManager: <br>`{"jsonrpc":"2.0","id":9,"method":"org.rdk.AppManager.1.register","params":{"event":"onAppLifecycleStateChanged","id":"client.events.1"}}` | Event subscription established. |
| 4 | Record Start Time and Launch App | Record the current UTC timestamp. Launch the app: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` | Launch request submitted; start time recorded. |
| 5 | Wait for APP_STATE_ACTIVE Event | Monitor the `onAppLifecycleStateChanged` event buffer until `APP_STATE_ACTIVE` is received (up to 120 seconds). | `APP_STATE_ACTIVE` event received. |
| 6 | Calculate and Validate Run Time | Record current timestamp after stabilization (3 seconds after ACTIVE). Calculate total run time = end time - start time (in ms). Retrieve `APPMANAGER_RUNAPP_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` from device config. Validate: run time < (threshold + offset). | Time taken from launch request to app running is within `APPMANAGER_RUNAPP_THRESHOLD_VALUE`. |
| 7 | Terminate App | Terminate the app as cleanup: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_name>"}}` | App terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
