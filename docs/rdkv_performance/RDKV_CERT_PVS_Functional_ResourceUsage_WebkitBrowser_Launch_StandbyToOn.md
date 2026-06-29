## TestCase ID
RDKV_PERFORMANCE_198
## TestCase Name
RDKV_CERT_PVS_Functional_ResourceUsage_WebkitBrowser_Launch_StandbyToOn

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the system resource usage (CPU and memory) remains within acceptable limits when an application is launched via the AppManager after transitioning the device power state from STANDBY to ON.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Confirm org.rdk.System plugin is available | The org.rdk.System plugin must be present and activatable in the device build. | The System plugin should be available in the build. |
| 3 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 4 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 5 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. | The app_download_url should point to a reachable hosting location. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Query current power state | Retrieve the current power state of the device using the System plugin. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.getPowerState"}` | The current power state should be retrieved successfully. |
| 2 | Set device power state to STANDBY | If the device is not already in STANDBY state, set the power state to LIGHT_SLEEP (STANDBY). <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.setPowerState", "params": {"powerState": "LIGHT_SLEEP", "standbyReason": "APIUnitTest"}}` | The device power state should transition to STANDBY successfully. |
| 3 | Set device power state to ON | Set the device power state from STANDBY to ON. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.System.1.setPowerState", "params": {"powerState": "ON", "standbyReason": "APIUnitTest"}}` | The device power state should transition to ON successfully. |
| 4 | Install and launch the application | Download, install, and launch the application bundle (com.rdkcentral.google) after the device returns to ON state. <br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` <br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` <br>Launch: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The application should be installed and launched successfully after device power ON. |
| 5 | Validate resource usage after launch from STANDBY | Allow 10 seconds for the application to stabilize, then measure and validate the system CPU and memory usage. Invoke the DeviceInfo systeminfo API to retrieve current system metrics: <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` <br>Extract CPU load from the `cpuload` field and calculate memory usage using the formula `(totalram - freeram) / totalram × 100`. | Resource usage (CPU and memory) should be within the expected acceptable limits after launching from STANDBY-to-ON transition. |
| 6 | Terminate the application | Send a terminate request to clean up the launched application after the resource measurement. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.google"}}` | The application should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M115<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
