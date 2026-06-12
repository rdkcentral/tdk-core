## TestCase ID
RDKV_PERFORMANCE_182
## TestCase Name
RDKV_CERT_PVS_AppManager_ResourceUsage_AppStartupVsIdle
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that resource usage (CPU and memory) during application startup differs from idle state, and that startup resource usage remains within acceptable limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.AppManager`, `org.rdk.DownloadManager`, and `org.rdk.PackageManagerRDKEMS` plugins should be available and activatable on the device.|
|3|`google_bundle` and `app_download_url` must be configured in `PerformanceTestVariables`.|
|4|`PACKAGEMANAGER_FILE_LOCATOR` must be configured in the device config file.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Allow System to Stabilize | Wait 10 seconds for the system to reach a stable idle state. | System is in idle state. |
| 3 | Capture Idle Resource Usage | Capture current CPU and memory utilization while the device is idle. | Idle resource usage captured and recorded. |
| 4 | Check and Activate AppManager Plugins | Check status of `org.rdk.AppManager`, activate if not active: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@org.rdk.AppManager"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"org.rdk.AppManager"}}` | AppManager plugin is in activated state. |
| 5 | Check if App is Installed | Query installed packages: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.PackageManagerRDKEMS.1.listPackages"}` | Install status determined. |
| 6 | Download and Install App (if not installed) | Download bundle via `org.rdk.DownloadManager.1.download`. Install via `org.rdk.PackageManagerRDKEMS.install`. Verify via `org.rdk.PackageManagerRDKEMS.1.listPackages`. | App installed successfully. |
| 7 | Launch App | Launch the app using AppManager: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` | App launched successfully. |
| 8 | Allow Startup to Complete | Wait 10 seconds for app to complete startup sequence. | App startup has completed. |
| 9 | Capture Startup Resource Usage | Capture current CPU and memory utilization during the app startup phase. | Startup resource usage captured and recorded. |
| 10 | Compare Startup vs Idle Usage | Compare the startup resource usage values against the idle resource usage values. | Startup resource usage is measurably different from idle state, confirming the app is actively consuming resources during startup. |
| 11 | Terminate App | Terminate the app to clean up: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_name>"}}` | App terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
