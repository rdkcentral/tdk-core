## TestCase ID
RDKV_PERFORMANCE_180
## TestCase Name
RDKV_CERT_PVS_AppManager_InstallAppTwice_Stability
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the stability of the AppManager installation workflow by installing the same application twice consecutively and confirming that resource usage remains within acceptable limits after each install.

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
| 2 | Check Plugin Status | Check and activate `org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager` plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@org.rdk.DownloadManager"}` | All plugins confirmed in activated state. |
| 3 | Iteration 1 — Check if App is Installed | Query `org.rdk.PackageManagerRDKEMS.1.listPackages` to check if app is already installed. If yes, uninstall it first using `org.rdk.PackageManagerRDKEMS.1.uninstallPackage`. | App is either not present or has been successfully uninstalled. |
| 4 | Iteration 1 — Download and Install App | Download bundle: `org.rdk.DownloadManager.1.download`. Install: `org.rdk.PackageManagerRDKEMS.install`. Verify via `org.rdk.PackageManagerRDKEMS.1.listPackages`. | App installed successfully for the first time. |
| 5 | Iteration 1 — Validate Resource Usage | Validate that CPU and memory usage after the first install are within acceptable limits using the resource usage monitoring function. | Resource usage is within the expected limit after first install. |
| 6 | Iteration 2 — Uninstall App | Uninstall the app that was installed in iteration 1 to prepare for the second install: <br>`org.rdk.PackageManagerRDKEMS.1.uninstallPackage` | App uninstalled successfully. |
| 7 | Iteration 2 — Download and Install App Again | Repeat the download and install steps for the same app bundle: `org.rdk.DownloadManager.1.download` then `org.rdk.PackageManagerRDKEMS.install`. Verify via `org.rdk.PackageManagerRDKEMS.1.listPackages`. | App installed successfully for the second time. |
| 8 | Iteration 2 — Validate Resource Usage | Validate that CPU and memory usage after the second install are within acceptable limits. | Resource usage is within the expected limit after second install. |
| 9 | Final Cleanup | Uninstall the app as cleanup: <br>`org.rdk.PackageManagerRDKEMS.1.uninstallPackage` | App uninstalled; environment is clean. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 20

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
