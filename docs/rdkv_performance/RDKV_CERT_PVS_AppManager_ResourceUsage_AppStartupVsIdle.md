## TestCase ID
RDKV_PERFORMANCE_65
## TestCase Name
RDKV_CERT_PVS_AppManager_ResourceUsage_AppStartupVsIdle

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the system resource usage (CPU and memory) during application startup via the AppManager is measurably different from the idle state resource usage, confirming that the system correctly accounts for application resource consumption at startup.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Confirm AppManager plugin is available | The org.rdk.AppManager plugin must be present and activatable in the device build. | The AppManager plugin should be available in the build. |
| 3 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured, providing a clean system state for idle measurement. |
| 4 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 5 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. | The app_download_url should point to a reachable hosting location. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Allow system to reach idle state | After device boot or configuration, allow 10 seconds for the system to reach an idle state with no applications running before taking the baseline resource measurement. | The system should reach a stable idle state before measurement begins. |
| 2 | Measure idle resource usage (baseline) | Measure and record the system CPU and memory usage in the idle state, before any application is launched. This serves as the baseline for comparison. Invoke the DeviceInfo systeminfo API to retrieve current system metrics: <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` <br>Extract CPU load from the `cpuload` field and calculate memory usage using the formula `(totalram - freeram) / totalram × 100`. | The idle resource usage should be captured successfully and represent the system's baseline CPU and memory consumption. |
| 3 | Verify and activate AppManager plugin | Query the AppManager plugin status and activate it if not already active. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}}` | The org.rdk.AppManager plugin should be in the activated state. |
| 4 | Download the application bundle | Download the application bundle from the configured URL via the DownloadManager to bring it to the active state for the startup resource measurement. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` | The download should complete successfully and a download ID should be returned. |
| 5 | Install the application | Install the downloaded application bundle. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully. |
| 6 | Launch the application | Send a launch request for the installed application to bring it to the active state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The application should be launched successfully and reach the active state. |
| 7 | Measure startup resource usage | Allow 10 seconds for the application to stabilize after launch, then measure and record the system CPU and memory usage during the application startup state. Invoke the DeviceInfo systeminfo API to retrieve current system metrics: <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` <br>Extract CPU load from the `cpuload` field and calculate memory usage using the formula `(totalram - freeram) / totalram × 100`. | The startup resource usage should be captured successfully and should reflect resource consumption while the application is active. |
| 8 | Compare startup vs idle resource usage | Compare the startup resource usage measurement against the baseline idle resource usage. Verify that the values differ, confirming the application is contributing to system resource consumption. | The startup resource usage should differ from the idle state resource usage. The system should show higher CPU and/or memory consumption during application startup compared to the idle baseline, confirming accurate resource tracking. |
| 9 | Terminate the application | Send a terminate request to clean up the running application after the comparison is complete. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.google"}}` | The application should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
