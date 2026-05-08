## TestCase ID
RDKV_PERFORMANCE_178
## TestCase Name
RDKV_CERT_PVS_AppManager_LaunchApp_LifeCycle
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate AppManager launch lifecycle events for an app after successful installation.

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
| 2 | Step 2 | Verify if com.rdkcentral.google is installed. If not installed, download and install the app. <br>List packages: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}<br>Download: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url":"<app_download_url>/<google_bundle>"}}<br>Install: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator":"<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}} | App should be present in installed package list before launch verification starts. |
| 3 | Step 3 | Register for onAppLifecycleStateChanged event before launching the app. <br>{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}} | Event registration should be successful and event listener should be active. |
| 4 | Step 4 | Launch app com.rdkcentral.google. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}} | Launch API should return success (result null/None is acceptable in this flow). |
| 5 | Step 5 | Validate lifecycle events for app launch from event stream. Verify APP_STATE_LOADING, APP_STATE_INITIALIZING, APP_STATE_PAUSED, and APP_STATE_ACTIVE are received for com.rdkcentral.google. | All expected launch lifecycle states should be observed within timeout. |
| 6 | Step 6 | Terminate the launched app as cleanup. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId":"com.rdkcentral.google"}} | App should terminate successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 5

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
