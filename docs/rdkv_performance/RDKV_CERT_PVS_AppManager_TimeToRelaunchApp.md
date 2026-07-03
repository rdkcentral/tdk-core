## TestCase ID
RDKV_PERFORMANCE_77
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeToRelaunchApp

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to relaunch a previously terminated application via the AppManager is within the configured performance threshold, measured from the relaunch request to the receipt of the APP_STATE_ACTIVE lifecycle state change event.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. | The app_download_url should point to a reachable hosting location. |
| 5 | Configure relaunch threshold in device config | `APPMANAGER_RELAUNCH_THRESHOLD_VALUE` (or `APPMANAGER_LAUNCH_THRESHOLD_VALUE` as fallback) and `THRESHOLD_OFFSET` must be set in the device-specific configuration file. | Threshold and offset values should be correctly configured for relaunch performance comparison. |
| 6 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path where downloaded packages are stored on the device. | The file locator path should be correctly configured. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query and activate the required plugins to ensure they are in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All required plugins should be in the activated state. |
| 2 | Download the application bundle | Download the application bundle from the configured URL via the DownloadManager so it is ready for the warm-up launch. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` | The download should complete successfully and a download ID should be returned. |
| 3 | Install the application | Install the downloaded application bundle. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully. |
| 4 | Perform warm-up initial launch | Launch the application once as a warm-up to populate any caches before the measured relaunch. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The application should launch successfully in the warm-up phase. |
| 5 | Subscribe to the lifecycle state change event | Register a WebSocket event listener for onAppLifecycleStateChanged before the terminate and relaunch sequence. <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}}` | Event subscription should be established successfully. |
| 6 | Terminate the application before relaunch | Send a terminate request to stop the warm-up running instance before measuring the relaunch time. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.google"}}` | The application should be terminated successfully. |
| 7 | Relaunch the application and record start time | Record the current UTC timestamp as the relaunch start time, then send the launch request. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The relaunch request should be accepted by the AppManager. |
| 8 | Wait for APP_STATE_ACTIVE event and calculate relaunch time | Monitor the event buffer until the onAppLifecycleStateChanged event containing APP_STATE_ACTIVE is received or a 120-second timeout is reached. Compute the elapsed time in milliseconds between the event timestamp and the relaunch start time. Compare against `APPMANAGER_RELAUNCH_THRESHOLD_VALUE` (or `APPMANAGER_LAUNCH_THRESHOLD_VALUE` if relaunch threshold is absent) + `THRESHOLD_OFFSET`. | The APP_STATE_ACTIVE event should be received and the relaunch time should be within the configured performance threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
