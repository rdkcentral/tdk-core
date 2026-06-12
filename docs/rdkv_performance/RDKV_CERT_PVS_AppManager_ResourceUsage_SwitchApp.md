## TestCase ID
RDKV_PERFORMANCE_190
## TestCase Name
RDKV_CERT_PVS_AppManager_ResourceUsage_SwitchApp
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU and memory resource usage remain within acceptable limits when switching between two AppManager-managed applications.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager` plugins should be available and activatable on the device.|
|3|`google_bundle`, `keytest_bundle`, and `app_download_url` must be configured in `PerformanceTestVariables`.|
|4|`PACKAGEMANAGER_FILE_LOCATOR` must be configured in the device config file.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check and Activate Plugins | Check and activate `org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager`. | All plugins in activated state. |
| 3 | Install Google App | Check installation via `org.rdk.PackageManagerRDKEMS.1.listPackages`. Download and install if needed: `org.rdk.DownloadManager.1.download` + `org.rdk.PackageManagerRDKEMS.install`. | Google app installed successfully. |
| 4 | Install KeyTest App | Check installation via `org.rdk.PackageManagerRDKEMS.1.listPackages`. Download and install if needed. | KeyTest app installed successfully. |
| 5 | Launch App1 (Google) in Foreground | Launch the first app using AppManager: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app1_name>","intent":"","launchArgs":""}}` | App1 launched and active in foreground. |
| 6 | Capture Resource Usage — App1 Foreground | Wait 10 seconds then capture CPU and memory usage while App1 is in foreground. | Resource usage with App1 in foreground captured. |
| 7 | Switch to App2 (KeyTest) | Launch App2 to bring it to foreground (App1 moves to background): <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app2_name>","intent":"","launchArgs":""}}` | App2 is in foreground; App1 moves to background. |
| 8 | Capture Resource Usage — App2 Foreground, App1 Background | Wait 10 seconds then capture CPU and memory usage with App2 in foreground and App1 in background. | Resource usage with two apps loaded captured. |
| 9 | Switch Back to App1 | Launch App1 again to bring it to foreground: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app1_name>","intent":"","launchArgs":""}}` | App1 returns to foreground. |
| 10 | Capture Resource Usage — App1 Foreground Again | Wait 10 seconds then capture CPU and memory usage after switching back to App1. | Resource usage after switch-back captured. |
| 11 | Validate Resource Usage (All States) | Validate that resource usage in all three states (App1 only, App1+App2 loaded, after switch) are within acceptable limits. | Resource usage remains within acceptable limits across all switching states. |
| 12 | Cleanup — Terminate Both Apps | Terminate both apps: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app1_name>"}}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app2_name>"}}` | Both apps terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
