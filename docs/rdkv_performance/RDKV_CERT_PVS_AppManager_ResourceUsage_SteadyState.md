## TestCase ID
RDKV_PERFORMANCE_72
## TestCase Name
RDKV_CERT_PVS_AppManager_ResourceUsage_SteadyState

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the system resource usage (CPU and memory) remains stable and within acceptable limits after an application has been running for an extended period and has reached a steady state via the AppManager.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. | The app_download_url should point to a reachable hosting location. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate the AppManager plugin | Query the AppManager plugin status and activate it if not already active. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br><br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}}` | The org.rdk.AppManager plugin should be in the activated state. |
| 2 | Download the application bundle | Download the application bundle from the configured URL via the DownloadManager. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` | The download should complete successfully and a download ID should be returned. |
| 3 | Install the application | Install the downloaded application bundle without launching it. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully and appear in the installed packages list. |
| 4 | Launch the application | Send a launch request for the installed application so it enters the active running state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The application should be installed and launched successfully, entering the active state. |
| 5 | Wait for application to reach steady state | Allow the application to run for 600 seconds (10 minutes) to stabilize CPU and memory usage and reach a genuine steady-state condition before measurement. | The application should continue running without crashing during the 600-second steady-state period. |
| 6 | Measure resource usage in steady state | Invoke the DeviceInfo systeminfo API to retrieve current system metrics after the steady-state period. Extract CPU load from the `cpuload` field and calculate memory usage using the formula `(totalram - freeram) / totalram × 100`. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | The system metrics (CPU load and memory usage) should be retrieved successfully after the 600-second steady-state period. |
| 7 | Validate steady-state resource usage against thresholds | Compare the measured CPU and memory values against the configured resource usage thresholds to confirm the system has not experienced resource growth or leaks during extended operation. | Resource usage (CPU and memory) in steady state should be within the configured acceptable limits. No memory growth or resource leaks should be observed after prolonged operation. |
| 8 | Terminate the application | Send a terminate request to clean up the running application after the steady-state validation. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.google"}}` | The application should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
