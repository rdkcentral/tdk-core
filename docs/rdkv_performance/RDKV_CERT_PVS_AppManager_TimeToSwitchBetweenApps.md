## TestCase ID
RDKV_PERFORMANCE_198
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeToSwitchBetweenApps
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to switch from one AppManager-managed application to another is within the expected threshold limit.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager` plugins should be available and activatable on the device.|
|3|`google_bundle`, `keytest_bundle`, and `app_download_url` must be configured in `PerformanceTestVariables`.|
|4|`APPMANAGER_LAUNCH_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be configured in the device config file.|
|5|Time in Test Manager and DUT should be in sync with UTC.|
|6|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check and Activate Plugins | Check and activate `org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager`. | All plugins in activated state. |
| 3 | Install Both Apps | Install `google_bundle` and `keytest_bundle` if not already installed via `org.rdk.PackageManagerRDKEMS.1.listPackages` + download + install flow. | Both apps installed. |
| 4 | Subscribe to Lifecycle Events | Register a WebSocket listener for `onAppLifecycleStateChanged` from AppManager: <br>`{"jsonrpc":"2.0","id":9,"method":"org.rdk.AppManager.1.register","params":{"event":"onAppLifecycleStateChanged","id":"client.events.1"}}` | Event subscription established. |
| 5 | Launch App1 | Launch App1 (Google app) using AppManager: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app1_name>","intent":"","launchArgs":""}}` | App1 launched and `APP_STATE_ACTIVE` received. Wait 2 seconds. |
| 6 | Record Switch Start Time | Clear the event buffer. Record current UTC timestamp immediately before launching App2. | Switch start time recorded. |
| 7 | Switch to App2 | Launch App2 (KeyTest app) to bring it to foreground: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app2_name>","intent":"","launchArgs":""}}` | Launch request submitted; App1 moves to background. |
| 8 | Wait for App2 APP_STATE_ACTIVE Event | Monitor the `onAppLifecycleStateChanged` event buffer until App2 `APP_STATE_ACTIVE` is received (up to 120 seconds). Record the event timestamp. | App2 `APP_STATE_ACTIVE` event received. |
| 9 | Calculate and Validate Switch Time | Calculate: switch time = event timestamp - switch start time (in ms). Retrieve `APPMANAGER_LAUNCH_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` from device config. Validate: switch time < (threshold + offset). | Time taken to switch between apps is within the configured threshold. |
| 10 | Cleanup — Terminate Both Apps | Terminate both apps: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app1_name>"}}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app2_name>"}}` | Both apps terminated. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
