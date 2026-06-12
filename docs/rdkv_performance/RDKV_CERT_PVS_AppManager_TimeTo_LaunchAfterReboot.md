## TestCase ID
RDKV_PERFORMANCE_204
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_LaunchAfterReboot
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to launch a pre-installed application via AppManager after a device reboot is within the expected threshold limit.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager` plugins should be available and activatable on the device.|
|3|`google_bundle` and `app_download_url` must be configured in `PerformanceTestVariables`.|
|4|`APPMANAGER_LAUNCH_AFTER_REBOOT_THRESHOLD`, `THRESHOLD_OFFSET`, and `REBOOT_WAIT_TIME` must be configured in the device config file.|
|5|Time in Test Manager and DUT should be in sync with UTC.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check and Activate Plugins | Check and activate `org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager`. | All plugins in activated state. |
| 2 | Install App (Pre-Reboot) | Check `org.rdk.PackageManagerRDKEMS.1.listPackages`. Download and install if not installed. This step is outside the timing measurement. | App installed successfully before reboot. |
| 3 | Reboot Device | Trigger a device reboot using `Controller.1.harakiri` and wait for the device to come back online (using `REBOOT_WAIT_TIME` from device config). Validate device uptime is below 280 seconds. | Device has rebooted and is online. |
| 4 | Wait for Plugins After Reboot | Wait 10 seconds then check plugin status; retry after 15 seconds if not ready. | All plugins are in activated state after reboot. |
| 5 | Subscribe to Lifecycle Events | Register a WebSocket listener for `onAppLifecycleStateChanged` from AppManager: <br>`{"jsonrpc":"2.0","id":9,"method":"org.rdk.AppManager.1.register","params":{"event":"onAppLifecycleStateChanged","id":"client.events.1"}}` | Event subscription established. |
| 6 | Record Launch Start Time | Record the current UTC timestamp immediately before issuing the launch request. | Launch start time recorded. |
| 7 | Launch App After Reboot | Launch the app using AppManager: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` | Launch request submitted. |
| 8 | Wait for APP_STATE_ACTIVE Event | Monitor the `onAppLifecycleStateChanged` event buffer until `APP_STATE_ACTIVE` is received for the app (up to 120 seconds). Record the event timestamp. | `APP_STATE_ACTIVE` event received. |
| 9 | Calculate and Validate Launch Time | Calculate: launch time = event timestamp - start time (in ms). Retrieve `APPMANAGER_LAUNCH_AFTER_REBOOT_THRESHOLD` and `THRESHOLD_OFFSET` from device config. Validate: launch time < (threshold + offset). | Time taken to launch app after reboot is within `APPMANAGER_LAUNCH_AFTER_REBOOT_THRESHOLD`. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
