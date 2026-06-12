## TestCase ID
RDKV_PERFORMANCE_188
## TestCase Name
RDKV_CERT_PVS_AppManager_ResourceUsage_Runtime_App
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU and memory resource usage remain within acceptable limits while an AppManager-managed application is actively running over a monitoring period.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.AppManager` and `org.rdk.RuntimeManager` plugins should be available and activatable on the device.|
|3|`google_bundle` and `app_download_url` must be configured in `PerformanceTestVariables`.|
|4|`PACKAGEMANAGER_FILE_LOCATOR` must be configured in the device config file.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the status of `org.rdk.AppManager` and `org.rdk.RuntimeManager`: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@org.rdk.AppManager"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@org.rdk.RuntimeManager"}` | Plugin status retrieved. |
| 3 | Activate Required Plugins | Activate `org.rdk.AppManager` and `org.rdk.RuntimeManager` if not currently active. | All plugins in activated state. |
| 4 | Install App (if not installed) | Check `org.rdk.PackageManagerRDKEMS.1.listPackages`. If not installed, download via `org.rdk.DownloadManager.1.download` and install via `org.rdk.PackageManagerRDKEMS.install`. | App installed successfully. |
| 5 | Launch App | Launch the app using AppManager: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` | App launched successfully. |
| 6 | Monitor Runtime Resource Usage | Continuously capture CPU and memory usage every 5 seconds for 60 seconds while the app is running. | Resource usage samples collected at regular intervals throughout the monitoring window. |
| 7 | Validate Runtime Resource Usage | Validate that all captured resource usage samples during the 60-second runtime are within the expected acceptable limits. | All runtime resource usage samples are within the acceptable limits. |
| 8 | Terminate App | Terminate the app as cleanup: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_name>"}}` | App terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
