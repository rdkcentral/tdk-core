## TestCase ID
RDKV_PERFORMANCE_200
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_CloseApp
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to close an AppManager-managed application (from the close request to the app reaching the destroyed state) is within the expected threshold limit.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager` plugins should be available and activatable on the device.|
|3|`google_bundle` and `app_download_url` must be configured in `PerformanceTestVariables`.|
|4|`APPMANAGER_CLOSE_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be configured in the device config file (default: 2000ms and 500ms respectively).|
|5|Time in Test Manager and DUT should be in sync with UTC.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check and Activate Plugins | Check and activate `org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager`. | All plugins in activated state. |
| 2 | Install and Launch App | Check `org.rdk.PackageManagerRDKEMS.1.listPackages`. Download and install if not installed. Launch via: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` | App installed and launched in active state. |
| 3 | Subscribe to Lifecycle Events | Register a WebSocket listener for `onAppLifecycleStateChanged`: <br>`{"jsonrpc":"2.0","id":9,"method":"org.rdk.AppManager.1.register","params":{"event":"onAppLifecycleStateChanged","id":"client.events.1"}}` | Event subscription established. |
| 4 | Record Close Start Time | Record current UTC timestamp immediately before sending the close request. | Close start time recorded. |
| 5 | Close App | Send close request to AppManager: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.closeApp","params":{"appId":"<app_name>"}}` | Close request submitted successfully. |
| 6 | Wait for APP_STATE_DESTROYED Event | Monitor the `onAppLifecycleStateChanged` event buffer until `APP_STATE_DESTROYED` is received for the app (up to 120 seconds). Record the event timestamp. | `APP_STATE_DESTROYED` event received. |
| 7 | Calculate and Validate Close Time | Calculate: close time = event timestamp - start time (in ms). Retrieve `APPMANAGER_CLOSE_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` from device config. Validate: close time < (threshold + offset). | Time taken to close the app is within `APPMANAGER_CLOSE_THRESHOLD_VALUE`. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
