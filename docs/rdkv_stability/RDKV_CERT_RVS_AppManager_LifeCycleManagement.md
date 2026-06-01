## TestCase ID
RDKV_STABILITY_71

## TestCase Name
RDKV_CERT_RVS_AppManager_LifeCycleManagement

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the complete application lifecycle management by testing app installation, launch, termination, and uninstallation in multiple iterations, while verifying that resource usage (CPU and memory) remains within expected limits across all lifecycle operations.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|DownloadManager, PackageManagerRDKEMS and AppManager plugins should be available and activated in the build.|
|3|google_bundle should be updated in PerformanceTestVariables.|
|4|app_download_url should be updated in PerformanceTestVariables.|
|5|lifecyclecount should be configured in StabilityTestVariables with required iteration count.|
|6|PACKAGEMANAGER_FILE_LOCATOR in device specific config must be updated with correct path where downloaded package is stored in DUT.|
|7|Device should be rebooted before starting the performance testing if "pre_req_reboot_pvs" is configured as "Yes".|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Step 1 | Check status of required AppManager plugins and ensure they are activated: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"} | All three required plugins should be in activated state (or get activated successfully). |
| 2 | Step 2 | Execute one complete lifecycle iteration: Install app com.rdkcentral.channel. <br>Check if app is already installed: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}<br>Download if needed: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url":"<app_download_url>/<google_bundle>"}}<br>Install: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.channel", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator":"<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}} | App com.rdkcentral.channel should be successfully installed and present in installed packages list. |
| 3 | Step 3 | Launch the installed app com.rdkcentral.channel. <br>Launch API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.channel", "intent": "", "launchArgs": ""}} | Launch API should return success (result null/None is acceptable). App should be running. |
| 4 | Step 4 | Verify app is in the loaded apps list to confirm successful launch. Wait 20 seconds for app stabilization. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"} | App com.rdkcentral.channel should be present in the list of loaded apps with APP_STATE_ACTIVE state. |
| 5 | Step 5 | Terminate the launched app. Wait 30 seconds for cleanup and resource deallocation. <br>Terminate API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId":"com.rdkcentral.channel"}} | Terminate API should return success. App should be gracefully terminated and removed from loaded apps list. |
| 6 | Step 6 | Uninstall the terminated app com.rdkcentral.channel. <br>Uninstall API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.uninstall", "params": {"packageId": "com.rdkcentral.channel"}} | Uninstall API should return success. App should be removed from installed packages list. |
| 7 | Step 7 | Validate resource usage (CPU and memory) after the complete lifecycle cycle. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"} | CPU load and memory usage should remain within configured thresholds. Resource usage should not show increasing trend indicating leaks. |
| 8 | Step 8 | Repeat Step 2 through Step 7 for configured lifecyclecount iterations (same workflow for each iteration). | Every iteration should complete successfully with all lifecycle operations (install, launch, terminate, uninstall) and resource validation showing stable resource consumption. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 10-15 (per iteration)

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
