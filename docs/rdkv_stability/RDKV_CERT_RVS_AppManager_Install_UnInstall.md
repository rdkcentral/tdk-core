## TestCase ID
RDKV_STABILITY_66
## TestCase Name
RDKV_CERT_RVS_AppManager_Install_UnInstall
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate repeated uninstall and install lifecycle of an app and verify device resource usage remains within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|DeviceInfo, org.rdk.DownloadManager, and org.rdk.PackageManagerRDKEMS plugins should be available in the build.|
|3|google_bundle should be updated in PerformanceTestVariables.|
|4|app_download_url should be updated in PerformanceTestVariables.|
|5|PACKAGEMANAGER_FILE_LOCATOR in device specific config must point to the app download path in the DUT.|
|6|install_uninstall_count should be configured in StabilityTestVariables with required iteration count.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Step 1 | Check baseline device state and resource usage before starting stress loop. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"} | Device state validation should pass and CPU/memory should be within expected limit. |
| 2 | Step 2 | Verify required plugin status and activate if needed: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"} | Required plugins should be in activated state before proceeding. |
| 3 | Step 3 | Check installed packages to determine whether com.rdkcentral.google is present. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"} | Installed package list should be returned successfully. |
| 4 | Step 4 | If com.rdkcentral.google is already installed, uninstall it before the new install cycle. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.uninstall", "params": {"packageId": "com.rdkcentral.google"}} | App should be uninstalled successfully (or step skipped if not installed). |
| 5 | Step 5 | Download app bundle from configured URL. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url":"<app_download_url>/<google_bundle>"}} | App bundle should be downloaded successfully and a valid download ID should be returned. |
| 6 | Step 6 | Install com.rdkcentral.google using downloaded package locator. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator":"<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}} | App should be installed successfully. |
| 7 | Step 7 | Validate resource usage after install within the same iteration. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"} | CPU and memory usage should remain within configured expected range. |
| 8 | Step 8 | Repeat Step 3 to Step 7 for configured install_uninstall_count iterations (same sequence for every iteration). | All iterations should complete successfully without failures and resource validation should pass throughout the loop. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 10

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
