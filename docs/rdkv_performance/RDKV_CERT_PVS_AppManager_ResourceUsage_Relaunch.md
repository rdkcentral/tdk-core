## TestCase ID
RDKV_PERFORMANCE_187
## TestCase Name
RDKV_CERT_PVS_AppManager_ResourceUsage_Relaunch
<atml:name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU and memory resource usage during the first launch and relaunch of an AppManager-managed application are within the expected acceptable limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager` plugins should be available and activatable on the device.|
|3|`google_bundle` and `app_download_url` must be configured in `PerformanceTestVariables`.|
|4|`PACKAGEMANAGER_FILE_LOCATOR` must be configured in the device config file.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status and Activate | Check the status of `org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager`; activate if needed. | All plugins in activated state. |
| 3 | Install App | Check `org.rdk.PackageManagerRDKEMS.1.listPackages`. If not installed, download via `org.rdk.DownloadManager.1.download` and install via `org.rdk.PackageManagerRDKEMS.install`. | App installed successfully. |
| 4 | First Launch | Launch the app using AppManager: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` | App launched for the first time. |
| 5 | Wait and Capture First Launch Resource Usage | Wait 10 seconds for app to stabilize, then capture CPU and memory usage. | First launch resource usage captured. |
| 6 | Terminate App | Terminate the app: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_name>"}}` | App terminated. |
| 7 | Wait Before Relaunch | Wait 5 seconds before relaunching. | System stabilized after termination. |
| 8 | Relaunch App (Second Launch) | Launch the app again using AppManager: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` | App relaunched successfully. |
| 9 | Wait and Capture Second Launch Resource Usage | Wait 10 seconds for app to stabilize, then capture CPU and memory usage for the relaunch. | Second launch resource usage captured. |
| 10 | Validate Resource Usage (Both Launches) | Validate that resource usage after both first launch and relaunch are within the expected acceptable limits. | Resource usage for both launches is within acceptable limits. |
| 11 | Cleanup — Terminate App | Terminate the app: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_name>"}}` | App terminated. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
