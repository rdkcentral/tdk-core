## TestCase ID
RDKV_PERFORMANCE_183
## TestCase Name
RDKV_CERT_PVS_AppManager_ResourceUsage_CloseApp
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU and memory resource usage after closing an AppManager-managed application are within the expected limits.

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
| 2 | Check Plugin Status | Check the status of `org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager` plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@org.rdk.DownloadManager"}` | Plugin status retrieved. |
| 3 | Activate Required Plugins | Activate any plugins not currently active: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"org.rdk.DownloadManager"}}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"org.rdk.PackageManagerRDKEMS"}}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"org.rdk.AppManager"}}` | All plugins in activated state. |
| 4 | Install and Launch App | Check if app is installed via `org.rdk.PackageManagerRDKEMS.1.listPackages`. If not installed, download via `org.rdk.DownloadManager.1.download` and install via `org.rdk.PackageManagerRDKEMS.install`. Then launch: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` | App installed and launched successfully. |
| 5 | Close App | Close the app to move it to background/paused state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.1.closeApp","params":{"appId":"<app_name>"}}` | App closed successfully; transitioning to paused state. |
| 6 | Wait for Cleanup | Wait 10 seconds after closing the app to allow resources to be freed. | System has had time to release resources after app close. |
| 7 | Validate Resource Usage After Close | Capture and validate CPU and memory usage after the app is closed. | Resource usage after app close is within the expected acceptable limits. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
