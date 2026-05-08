## TestCase ID
RDKV_PERFORMANCE_179
## TestCase Name
RDKV_CERT_PVS_AppManager_TerminateApp_LifeCycle
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate AppManager terminate app lifecycle transition events for a launched app.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|DownloadManager, PackageManagerRDKEMS, and AppManager plugins should be available in the build.|
|3|google_bundle should be updated in PerformanceTestVariables.|
|4|app_download_url should be updated in PerformanceTestVariables.|
|5|PACKAGEMANAGER_FILE_LOCATOR in device specific config must be updated with correct path where downloaded package is stored in DUT.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Step 1 | Check status of required plugins and activate if needed: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, org.rdk.AppManager. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"} | Required plugins should be in activated state. |
| 2 | Step 2 | Verify if com.rdkcentral.google is installed. If not installed, download and install the app. <br>List packages: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}<br>Download: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url":"<app_download_url>/<google_bundle>"}}<br>Install: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator":"<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}} | App should be present in installed package list before terminate verification starts. |
| 3 | Step 3 | Launch app com.rdkcentral.google before terminate operation. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}} | App should launch successfully. |
| 4 | Step 4 | Register for onAppLifecycleStateChanged event. <br>{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}} | Event registration should be successful and event listener should be active. |
| 5 | Step 5 | Trigger terminate app operation. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId":"com.rdkcentral.google"}} | Terminate API should return success (result null/None is acceptable in this flow). |
| 6 | Step 6 | Validate lifecycle event transition for terminate operation via onAppLifecycleStateChanged. Verify APP_STATE_ACTIVE, APP_STATE_PAUSED, and APP_STATE_TERMINATING are observed. | Expected terminate lifecycle states should be observed within timeout. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 5

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
