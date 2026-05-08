## TestCase ID
RDKV_STABILITY_69

## TestCase Name
RDKV_CERT_RVS_AppManager_Launch_Terminate

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate AppManager stability by repeatedly launching and terminating an app, and verifying that resource usage (CPU and memory) remains within expected limits across multiple iterations with no resource leaks.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|DownloadManager, PackageManagerRDKEMS and AppManager plugins should be available in the build.|
|3|google_bundle should be updated in PerformanceTestVariables.|
|4|app_download_url should be updated in PerformanceTestVariables.|
|5|launch_terminate_count should be configured in StabilityTestVariables with required iteration count.|
|6|PACKAGEMANAGER_FILE_LOCATOR in device specific config must be updated with correct path where downloaded package is stored in DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Step 1 | Check device status and initial resource usage by retrieving system info. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"} | Device status should be healthy. CPU load and memory usage should be within expected range before starting stress test. |
| 2 | Step 2 | Check status of required plugins and ensure they are activated: org.rdk.DownloadManager and org.rdk.PackageManagerRDKEMS. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"} | All required plugins should be in activated state (or get activated successfully). |
| 3 | Step 3 | Check whether com.rdkcentral.google is already installed. If not installed, download and install it. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}<br>Download API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url":"<app_download_url>/<google_bundle>"}}<br>Install API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator":"<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}} | App should be available in installed packages before launch-terminate loop starts. |
| 4 | Step 4 | Execute one launch-terminate iteration: launch app com.rdkcentral.google and wait for stabilization. <br>Launch API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}<br>Wait 10 seconds for app initialization. | Launch API should return success (result null/None is acceptable in this flow). App should be running and initialized. |
| 5 | Step 5 | Terminate the launched app. <br>Terminate API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "com.rdkcentral.google"}}<br>Wait 5 seconds for resource cleanup. | Terminate API should return success (result null/None is acceptable). App should be terminated and resources released. |
| 6 | Step 6 | Validate resource usage (CPU and memory) after the launch-terminate cycle. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"} | CPU load and memory usage should remain within configured thresholds. Resource usage should not show increasing trend indicating leaks. |
| 7 | Step 7 | Repeat Step 4, Step 5, and Step 6 for configured launch_terminate_count iterations (same workflow for each iteration). | Every iteration should complete successfully with launch, terminate, and resource validation showing stable resource consumption. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 10-15 (per iteration)

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
