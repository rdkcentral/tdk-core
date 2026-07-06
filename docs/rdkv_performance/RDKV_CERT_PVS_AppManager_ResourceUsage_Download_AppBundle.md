## TestCase ID
RDKV_PERFORMANCE_67
## TestCase Name
RDKV_CERT_PVS_AppManager_ResourceUsage_Download_AppBundle

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the system resource usage (CPU and memory) remains within acceptable limits during and immediately after downloading an application bundle via the DownloadManager.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. | The app_download_url should point to a reachable hosting location accessible from the device network. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate the DownloadManager plugin | Query the DownloadManager plugin status and activate it if not already active. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}` | The org.rdk.DownloadManager plugin should be in the activated state. |
| 2 | Initiate the application bundle download | Construct the full download URL by appending the bundle filename to the base URL, then initiate the download of the application bundle. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` | The download should be initiated successfully and the download operation should begin. |
| 3 | Validate system resource usage during and after download | Immediately after initiating the download, measure and validate the system CPU and memory usage against the configured resource usage thresholds to confirm that the download operation does not cause excessive resource consumption. Invoke the DeviceInfo systeminfo API to retrieve current system metrics: <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` <br>Extract CPU load from the `cpuload` field and calculate memory usage using the formula `(totalram - freeram) / totalram × 100`. | Resource usage (CPU and memory) during the download operation should be within the configured acceptable limits. No resource spikes or excessive consumption should be observed. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
