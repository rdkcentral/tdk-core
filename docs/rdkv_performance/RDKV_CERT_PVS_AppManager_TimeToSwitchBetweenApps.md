## TestCase ID
RDKV_PERFORMANCE_13
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeToSwitchBetweenApps

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to switch between two running applications via the AppManager is within the configured performance threshold, measured from the switch launch request to the receipt of the APP_STATE_ACTIVE lifecycle event for the target application.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Confirm required plugins are available | The following plugins must be present and activatable: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, org.rdk.AppManager. | All required plugins should be available in the build. |
| 3 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 4 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the first application bundle filename (App 1) in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 5 | Configure keytest_bundle in PerformanceTestVariables | `keytest_bundle` must be set to the second application bundle filename (App 2) in PerformanceTestVariables. | The keytest_bundle variable should be configured with a valid application bundle name. |
| 6 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundles are hosted. | The app_download_url should point to a reachable hosting location. |
| 7 | Configure switch threshold in device config | `APPMANAGER_LAUNCH_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be set in the device-specific configuration file for app switch time validation. | Threshold and offset values should be correctly configured. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query and activate the required plugins to ensure they are in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All required plugins should be in the activated state. |
| 2 | Install App 1 and App 2 | Download and install both application bundles without launching either. <br>For each app — Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<bundle_name>"}}` <br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "<app_id>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | Both applications should be installed successfully. |
| 3 | Subscribe to the lifecycle state change event | Register a WebSocket event listener for onAppLifecycleStateChanged to monitor both app state transitions. <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}}` | Event subscription should be established successfully. |
| 4 | Launch App 1 and wait for active state | Launch App 1 and wait for the lifecycle event confirming it reached APP_STATE_ACTIVE. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<app1_id>", "intent": "", "launchArgs": ""}}` | App 1 should reach APP_STATE_ACTIVE and the lifecycle event should be received. |
| 5 | Switch to App 2 and record start time | Clear the event buffer, record the current UTC timestamp as the switch start time, then send a launch request for App 2 to trigger the app switch. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<app2_id>", "intent": "", "launchArgs": ""}}` | The launch request for App 2 should be accepted, initiating the switch. |
| 6 | Wait for App 2 APP_STATE_ACTIVE event and calculate switch time | Monitor the event buffer until the onAppLifecycleStateChanged event containing APP_STATE_ACTIVE for App 2 is received or a 120-second timeout is reached. Compute the elapsed time in milliseconds between the start time and the event timestamp. Compare against `APPMANAGER_LAUNCH_THRESHOLD_VALUE` + `THRESHOLD_OFFSET` from device config. | App 2 should reach APP_STATE_ACTIVE and the switch time should be within the configured performance threshold. |
| 7 | Terminate both applications for cleanup | Send terminate requests to both App 1 and App 2 to restore the device to its initial state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "<app1_id>"}}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "<app2_id>"}}` | Both applications should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
