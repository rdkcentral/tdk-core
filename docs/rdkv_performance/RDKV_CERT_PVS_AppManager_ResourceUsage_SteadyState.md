## TestCase ID
RDKV_PERFORMANCE_189
## TestCase Name
RDKV_CERT_PVS_AppManager_ResourceUsage_SteadyState
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU and memory resource usage of an AppManager-managed application remain within acceptable limits after reaching the steady state (stabilized after 10 minutes of runtime).

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
| 2 | Check and Activate AppManager Plugin | Check the status of `org.rdk.AppManager` and activate if not active: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@org.rdk.AppManager"}` | AppManager plugin is in activated state. |
| 3 | Install and Launch App | Check installed packages via `org.rdk.PackageManagerRDKEMS.1.listPackages`. If not installed, download and install. Launch via: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` | App installed and launched successfully. |
| 4 | Wait for Steady State | Wait 600 seconds (10 minutes) for the application's CPU and memory usage to fully stabilize and reach a steady state. | App has been running for 10 minutes and resources have stabilized. |
| 5 | Capture and Validate Steady State Resource Usage | Capture CPU and memory usage in the steady state and validate they are within the expected limits. | Steady state resource usage is within the configured acceptable limits. |
| 6 | Terminate App | Terminate the app as cleanup: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_name>"}}` | App terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 20

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
