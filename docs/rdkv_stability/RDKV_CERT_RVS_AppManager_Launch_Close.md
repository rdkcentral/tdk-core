## TestCase ID
RDKV_STABILITY_67

## TestCase Name
RDKV_CERT_RVS_AppManager_Launch_Close

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate AppManager stability by repeatedly launching and closing an app using the closeApp method, and verifying that resource usage (CPU and memory) remains within expected limits across multiple iterations with no resource leaks.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|DownloadManager, PackageManagerRDKEMS and AppManager plugins should be available in the build.|
|3|google_bundle should be updated in PerformanceTestVariables.|
|4|app_download_url should be updated in PerformanceTestVariables.|
|5|launch_close_count should be configured in StabilityTestVariables with required iteration count.|
|6|PACKAGEMANAGER_FILE_LOCATOR in device specific config must be updated with correct path where downloaded package is stored in DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Step 1 | Check device status and initial resource usage by retrieving system info. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"} | Device status should be healthy. CPU load and memory usage should be within expected range before starting stress test. |
| 2 | Step 2 | Check status of required plugins and ensure they are activated: org.rdk.DownloadManager and org.rdk.PackageManagerRDKEMS. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"} | All required plugins should be in activated state (or get activated successfully). |
| 3 | Step 3 | Check whether com.rdkcentral.google is already installed. If not installed, download and install it. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}<br>Download API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url":"<app_download_url>/<google_bundle>"}}<br>Install API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator":"<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}} | App should be available in installed packages before launch-close loop starts. |
| 4 | Step 4 | Execute one launch-close iteration: launch app com.rdkcentral.google and wait before closing. <br>Launch API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}<br>Wait 10 seconds for app initialization. | Launch API should return success (result null/None is acceptable). App should be running and initialized. |
| 5 | Step 5 | Verify app is in the loaded apps list to confirm successful launch. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"} | App com.rdkcentral.google should be present in the list of loaded apps with APP_STATE_ACTIVE state. |
| 6 | Step 6 | Close the launched app using the closeApp method. <br>Close API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.closeApp", "params": {"appId": "com.rdkcentral.google"}}<br>Wait 10 seconds for resource cleanup. | Close API should return success (result null/None is acceptable). App should be gracefully closed and resources released. |
| 7 | Step 7 | Validate resource usage (CPU and memory) after the launch-close cycle. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"} | CPU load and memory usage should remain within configured thresholds. Resource usage should not show increasing trend indicating leaks. |
| 8 | Step 8 | Repeat Step 4, Step 5, Step 6, and Step 7 for configured launch_close_count iterations (same workflow for each iteration). | Every iteration should complete successfully with launch, close, and resource validation showing stable resource consumption. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 10-15 (per iteration)

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>

