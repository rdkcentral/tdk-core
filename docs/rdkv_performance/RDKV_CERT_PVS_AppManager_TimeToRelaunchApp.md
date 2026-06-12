## TestCase ID
RDKV_PERFORMANCE_195
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeToRelaunchApp
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to relaunch an AppManager-managed application after it has been terminated is within the expected threshold limit.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager` plugins should be available and activatable on the device.|
|3|`google_bundle` and `app_download_url` must be configured in `PerformanceTestVariables`.|
|4|`APPMANAGER_RELAUNCH_THRESHOLD_VALUE` (or `APPMANAGER_LAUNCH_THRESHOLD_VALUE`) and `THRESHOLD_OFFSET` must be configured in the device config file.|
|5|Time in Test Manager and DUT should be in sync with UTC.|
|6|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check and Activate Plugins | Check and activate `org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager`. | All plugins in activated state. |
| 3 | Install App | Check `org.rdk.PackageManagerRDKEMS.1.listPackages`. Download and install if not installed. | App installed successfully. |
| 4 | Initial Warm-up Launch | Perform an initial launch of the app (warm-up, not timed) to cache any runtime resources: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` | App launched for warm-up. Wait 5 seconds. |
| 5 | Subscribe to Lifecycle Events | Register a WebSocket listener for `onAppLifecycleStateChanged`: <br>`{"jsonrpc":"2.0","id":9,"method":"org.rdk.AppManager.1.register","params":{"event":"onAppLifecycleStateChanged","id":"client.events.1"}}` | Event subscription established. |
| 6 | Terminate App | Terminate the app before timing the relaunch: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_name>"}}` | App terminated successfully. |
| 7 | Record Relaunch Start Time | Record the current UTC timestamp immediately before the relaunch request. | Start time recorded. |
| 8 | Relaunch App | Relaunch the app using AppManager: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` | Relaunch request submitted. |
| 9 | Wait for APP_STATE_ACTIVE Event | Monitor the `onAppLifecycleStateChanged` event buffer until `APP_STATE_ACTIVE` event is received (up to 120 seconds). Record the event timestamp. | `APP_STATE_ACTIVE` event received after relaunch. |
| 10 | Calculate and Validate Relaunch Time | Calculate: relaunch time = event timestamp - start time (in ms). Retrieve `APPMANAGER_RELAUNCH_THRESHOLD_VALUE` (fallback: `APPMANAGER_LAUNCH_THRESHOLD_VALUE`) and `THRESHOLD_OFFSET` from device config. Validate that relaunch time < (threshold + offset). | Time taken to relaunch the app is within the configured threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
