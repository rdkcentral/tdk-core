## TestCase ID
RDKV_STABILITY_64
## TestCase Name
RDKV_CERT_RVS_AppManager_CloseApp_LifeCycle
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate AppManager close-app lifecycle behavior by repeatedly launching and closing an app, and verifying lifecycle events.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|DownloadManager, PackageManagerRDKEMS and AppManager plugins should be available in the build.|
|3|google_bundle should be updated in PerformanceTestVariables.|
|4|app_download_url should be updated in PerformanceTestVariables.|
|5|lifecycle_count should be configured in StabilityTestVariables with required iteration count.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Step 1 | Check status of required plugins and ensure they are activated: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, org.rdk.AppManager <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"} | All required plugins should be in activated state (or get activated successfully). |
| 2 | Step 2 | Check whether com.rdkcentral.google is already installed. If not installed, download and install it. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}<br>Download API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url":"<app_download_url>/<google_bundle>"}}<br>Install API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator":"<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}} | App should be available in installed packages before lifecycle loop starts. |
| 3 | Step 3 | Register lifecycle event listener before loop execution. <br>{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}} | Event registration should be successful and listener should start receiving lifecycle notifications. |
| 4 | Step 4 | Execute one lifecycle iteration: launch app then close app. <br>Launch API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}<br>Close API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.closeApp", "params": {"appId": "com.rdkcentral.google"}} | Both APIs should return success (result null/None is acceptable in this flow). |
| 5 | Step 5 | Validate lifecycle events for the iteration using onAppLifecycleStateChanged notification. Verify APP_STATE_ACTIVE and APP_STATE_PAUSED are observed for com.rdkcentral.google. <br>Example event: {"jsonrpc":"2.0","method":"client.events.1.onAppLifecycleStateChanged","params":{"appId":"com.rdkcentral.google","newState":"APP_STATE_ACTIVE/APP_STATE_PAUSED"}} | Required lifecycle events should be received for the app within timeout. |
| 6 | Step 6 | Repeat Step 4 and Step 5 for configured lifecycle_count iterations (same workflow for each iteration). | Every iteration should complete successfully with launch, close, and expected lifecycle event validation. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 5

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
