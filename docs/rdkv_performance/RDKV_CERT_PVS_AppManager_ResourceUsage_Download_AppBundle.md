## TestCase ID
RDKV_PERFORMANCE_174
## TestCase Name
RDKV_CERT_PVS_AppManager_ResourceUsage_Download_AppBundle
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device resource usage while downloading an app bundle

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|Wpeframework process should be up and running in the device.|
|2|google_bundle should be updated in PerformanceTestVariables.|
|3|app_download_url should be updated in PerformanceTestVariables.|
|4|Download manager plugin should be available in the device build.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Step 1 | Check the status of org.rdk.DownloadManager <br> {"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"} | Should be able to get the current status of org.rdk.DownloadManager |
| 2 | Step 2 | If org.rdk.DownloadManager is not in activated state, try to activate it <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params":{"callsign":"org.rdk.DownloadManager"}} | Should be able to activate org.rdk.DownloadManager |
| 3 | Step 3 | Start downloading the app bundle <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url":"<app_download_url>/<google_bundle>"}} | Download should be initiated successfully and API should return a download id (for example, "2005") |
| 4 | Step 4 | Validate resource usage while download is in progress using system info API <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"} | Should return system metrics including CPU load and memory values |
| 5 | Step 5 | Verify CPU and memory usage are less than 90% | Resource validation step should pass and report usage within expected limit |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 5

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
