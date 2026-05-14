## TestCase ID
RDKV_STABILITY_73

## TestCase Name
RDKV_CERT_RVS_AppManager_TerminateApp_LifeCycle

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate AppManager termination lifecycle events for an app by registering for lifecycle state change notifications and verifying that all expected lifecycle states (APP_STATE_ACTIVE, APP_STATE_PAUSED, APP_STATE_TERMINATING) are received during app termination in multiple iterations.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|DownloadManager, PackageManagerRDKEMS, and AppManager plugins should be available and activated in the build.|
|3|google_bundle should be updated in PerformanceTestVariables.|
|4|app_download_url should be updated in PerformanceTestVariables.|
|5|lifecycle_count should be configured in StabilityTestVariables with required iteration count.|
|6|PACKAGEMANAGER_FILE_LOCATOR in device specific config must be updated with correct path where downloaded package is stored in DUT.|
|7|Device should be rebooted before starting the performance testing if "pre_req_reboot_pvs" is configured as "Yes".|
|8|WebSocket connectivity to Thunder/WPEFramework on the device must be available.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Step 1 | Check status of required AppManager plugins and ensure they are activated: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}<br>{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"} | All three required plugins should be in activated state (or get activated successfully). |
| 2 | Step 2 | Check whether com.rdkcentral.google is already installed. If not installed, download and install it. <br>{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}<br>Download API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url":"<app_download_url>/<google_bundle>"}}<br>Install API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator":"<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}} | App com.rdkcentral.google should be available in installed packages before termination lifecycle validation starts. |
| 3 | Step 3 | Register for onAppLifecycleStateChanged event using WebSocket connection before starting the test iterations. <br>{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}} | Event registration should be successful and event listener should be active to capture all termination lifecycle state changes. |
| 4 | Step 4 | Execute one termination lifecycle validation iteration: Launch app com.rdkcentral.google. <br>Launch API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}} | Launch API should return success (result null/None is acceptable). App should be running. |
| 5 | Step 5 | Wait 30 seconds for app to stabilize and reach fully active state. | App should complete initialization and reach stable APP_STATE_ACTIVE state. |
| 6 | Step 6 | Terminate the launched app. <br>Terminate API: {"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId":"com.rdkcentral.google"}} | Terminate API should return success (result null/None is acceptable). App termination lifecycle events should be triggered. |
| 7 | Step 7 | Validate all expected termination lifecycle events from the event stream. Verify that APP_STATE_ACTIVE, APP_STATE_PAUSED, and APP_STATE_TERMINATING events are received for com.rdkcentral.google within the specified timeout (120 seconds). <br>Example event: {"jsonrpc":"2.0","method":"client.events.1.onAppLifecycleStateChanged","params":{"appId":"com.rdkcentral.google","newState":"APP_STATE_TERMINATING","oldState":"APP_STATE_PAUSED","errorReason":"APP_ERROR_NONE"}} | All three expected termination lifecycle states (ACTIVE, PAUSED, TERMINATING) should be observed in the correct order for each iteration. |
| 8 | Step 8 | Repeat Step 4, Step 5, Step 6, and Step 7 for configured lifecycle_count iterations (same workflow for each iteration). | Every iteration should receive all expected termination lifecycle events and complete successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 15-20 (per iteration)

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
