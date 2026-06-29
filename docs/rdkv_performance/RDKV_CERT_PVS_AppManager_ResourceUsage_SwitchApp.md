## TestCase ID
RDKV_PERFORMANCE_20
## TestCase Name
RDKV_CERT_PVS_AppManager_ResourceUsage_SwitchApp

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the system resource usage (CPU and memory) remains within acceptable limits across all phases of switching between two applications managed by the AppManager — specifically during App 1 foreground, App 2 foreground with App 1 in background, and App 1 back in foreground states.

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

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query and activate all required plugins to ensure they are in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All required plugins should be in the activated state. |
| 2 | Install both App 1 and App 2 | Download and install both application bundles without launching either. <br>For each app — Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<bundle_name>"}}` <br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "<app_id>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | Both applications should be installed successfully. |
| 3 | Launch App 1 to foreground | Send a launch request for App 1 and wait for it to become active. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<app1_id>", "intent": "", "launchArgs": ""}}` | App 1 should launch successfully and be in the active foreground state. |
| 4 | Validate resource usage — App 1 in foreground | Allow 10 seconds for the app to stabilize, then measure and validate the system CPU and memory usage while App 1 is in the foreground. Invoke the DeviceInfo systeminfo API to retrieve current system metrics: <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` <br>Extract CPU load from the `cpuload` field and calculate memory usage using the formula `(totalram - freeram) / totalram × 100`. | System resource usage with App 1 active in the foreground should be within the configured acceptable limits. |
| 5 | Switch to App 2 (App 1 moves to background) | Launch App 2 to move it to the foreground while App 1 transitions to the background. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<app2_id>", "intent": "", "launchArgs": ""}}` | App 2 should become active in the foreground and App 1 should move to the background state. |
| 6 | Validate resource usage — App 2 foreground, App 1 background | Allow 10 seconds for stabilization, then measure and validate CPU and memory usage with App 2 in the foreground and App 1 in the background. Invoke the DeviceInfo systeminfo API to retrieve current system metrics: <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` <br>Extract CPU load from the `cpuload` field and calculate memory usage using the formula `(totalram - freeram) / totalram × 100`. | Resource usage with two apps loaded (one foreground, one background) should remain within the configured acceptable limits. |
| 7 | Switch back to App 1 | Launch App 1 again to bring it back to the foreground. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<app1_id>", "intent": "", "launchArgs": ""}}` | App 1 should resume to the foreground successfully. |
| 8 | Validate resource usage — App 1 back in foreground | Allow 10 seconds for stabilization, then measure and validate CPU and memory usage with App 1 resumed to the foreground. Invoke the DeviceInfo systeminfo API to retrieve current system metrics: <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` <br>Extract CPU load from the `cpuload` field and calculate memory usage using the formula `(totalram - freeram) / totalram × 100`. | Resource usage with App 1 back in the foreground should remain within the configured acceptable limits. |
| 9 | Terminate both applications for cleanup | Send terminate requests for both App 1 and App 2 to clean up after the test. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "<app1_id>"}}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "<app2_id>"}}` | Both applications should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
