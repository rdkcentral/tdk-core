## TestCase ID
RDKV_PERFORMANCE_177
## TestCase Name
RDKV_CERT_PVS_AppManager_ResourceUsage_Terminate_App
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device resource usage while terminating an app

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|Wpeframework process should be up and running in the device.|
|2|google_bundle should be updated in PerformanceTestVariables.|
|3|app_download_url should be updated in PerformanceTestVariables.|
|4|DownloadManager, PackageManagerRDKEMS and AppManager plugins should be available in the device build.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Step 1 | Check the status of org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS and org.rdk.AppManager <br> {"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"} | Should be able to get current status of DownloadManager, PackageManagerRDKEMS and AppManager |
| 2 | Step 2 | If any required plugin is not in activated state, try to activate it <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params":{"callsign":"org.rdk.DownloadManager"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params":{"callsign":"org.rdk.PackageManagerRDKEMS"}}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params":{"callsign":"org.rdk.AppManager"}} | Required plugins should be activated successfully |
| 3 | Step 3 | Check if the app is already installed in the device <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"} | Should be able to retrieve list of installed packages and identify whether com.rdkcentral.google is present |
| 4 | Step 4 | If com.rdkcentral.google is not installed, download and install the app; then launch it before termination test <br>Download API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url":"<app_download_url>/<google_bundle>"}}<br>Install API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator":"<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}<br>Launch API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}} | App should be available in launched state for termination validation |
| 5 | Step 5 | Terminate the launched app <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId":"com.rdkcentral.google"}} | App should terminate successfully and API should return success (for example, result null/None) |
| 6 | Step 6 | Validate resource usage during/after termination using system info API <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"} | Should return system metrics including CPU load and memory values |
| 7 | Step 7 | Verify CPU and memory usage are less than 90% | Resource validation step should pass and report usage within expected limit |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 5

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
