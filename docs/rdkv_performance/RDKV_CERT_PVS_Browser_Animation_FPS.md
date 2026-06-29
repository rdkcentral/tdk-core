## TestCase ID
RDKV_PERFORMANCE_92
## TestCase Name
RDKV_CERT_PVS_Browser_Animation_FPS
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the average FPS value obtained from the browser animation performance benchmark test by installing and launching the animation application bundle and confirming the score meets the configured threshold value.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify WPEFramework status | WPEFramework process must be up and running on the device before test execution begins. | WPEFramework process should be active and accessible on the device. |
| 2 | Configure pre-requisite reboot | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | Device should be in a clean state prior to performance test execution. |
| 3 | Configure animation app bundle name and download URL | `animation_app_bundle_name` (default: `com.rdkcentral.animation+0.1.0.bolt`) and `app_download_url` must be configured in BrowserPerformanceVariables with valid values pointing to the hosted application bundle. | The animation application bundle must be accessible from the configured download URL. |
| 4 | Configure threshold value in device config | `ANIMATION_BENCHMARK_THRESHOLD_VALUE` must be configured in the device-specific configuration file. `PACKAGEMANAGER_FILE_LOCATOR` must also be set with the correct path where downloaded packages are stored on the DUT. | Threshold value and file locator path should be available and non-empty for installation and score validation. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot device as pre-requisite | If `PRE_REQ_REBOOT_PVS` is configured as Yes, reboot the device by issuing the harakiri command and wait 150 seconds for reboot to complete: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should reboot successfully and come back online within the wait period. |
| 2 | Check if animation application is installed | Query the list of installed packages to determine if the animation app (com.rdkcentral.animation) is already present on the device: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be retrieved successfully. If com.rdkcentral.animation is already installed, the installation workflow is skipped. |
| 3 | Activate required AppManager plugins | If the animation app is not installed, verify and activate the required plugin stack — org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}`<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}`<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}}` | All three plugins should be in activated state before download and installation proceed. |
| 4 | Download animation application bundle | Download the animation application bundle from the configured URL: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/com.rdkcentral.animation+0.1.0.bolt"}}` | The animation application bundle should be downloaded successfully and a download ID should be returned. |
| 5 | Install animation application bundle | Install the downloaded animation bundle using PackageManagerRDKEMS with the file locator path from device configuration: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.animation", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The animation app bundle should be installed successfully. |
| 6 | Verify animation application is installed | Confirm the animation app appears in the installed packages list: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | com.rdkcentral.animation should appear in the installed packages list. |
| 7 | Launch animation application | Launch the animation application using AppManager: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.animation", "intent": "", "launchArgs": ""}}` | The animation application should launch successfully. |
| 8 | Verify animation application is running | Confirm the launched app appears in the active loaded apps list: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | com.rdkcentral.animation should be listed as an active loaded application. |
| 9 | Retrieve animation benchmark FPS score | Wait 20 seconds for the animation benchmark to execute, then connect to the WebKit webinspect page to extract the average FPS score from the animation benchmark test results. | The average FPS score should be successfully retrieved from the webinspect page and must not contain the value "Unable to get the browser score". |
| 10 | Validate animation FPS score against threshold | Compare the retrieved animation benchmark FPS score against `ANIMATION_BENCHMARK_THRESHOLD_VALUE` from the device configuration file. | The animation FPS score should be greater than the configured `ANIMATION_BENCHMARK_THRESHOLD_VALUE`. |
| 11 | Terminate animation application | Terminate the animation application after score validation: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminate", "params": {"appId": "com.rdkcentral.animation"}}` | The animation application should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 4

**Priority** : High

**Release Version** : M96<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
