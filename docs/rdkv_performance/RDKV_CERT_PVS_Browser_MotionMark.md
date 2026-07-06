## TestCase ID
RDKV_PERFORMANCE_54
## TestCase Name
RDKV_CERT_PVS_Browser_MotionMark
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the average FPS value obtained from the browser graphics performance benchmark using MotionMark by installing and launching the MotionMark application bundle and confirming the score meets the configured threshold value.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify WPEFramework status | WPEFramework process must be up and running on the device before test execution begins. | WPEFramework process should be active and accessible on the device. |
| 2 | Configure pre-requisite reboot | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | Device should be in a clean state prior to performance test execution. |
| 3 | Configure MotionMark app bundle name and download URL | `motion_app_bundle_name` (default: `com.rdkcentral.motion+0.1.0.bolt`) and `app_download_url` must be configured in BrowserPerformanceVariables. | The MotionMark application bundle must be accessible from the configured download URL. |
| 4 | Configure threshold value in device config | `MOTIONMARK_THRESHOLD_VALUE` must be configured in the device-specific configuration file. `PACKAGEMANAGER_FILE_LOCATOR` must also be set with the correct path where downloaded packages are stored on the DUT. | Threshold value and file locator path should be available and non-empty for installation and score validation. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot device as pre-requisite | If `PRE_REQ_REBOOT_PVS` is configured as Yes, reboot the device by issuing the harakiri command and wait 150 seconds for reboot to complete: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should reboot successfully and come back online within the wait period. |
| 2 | Check if MotionMark application is installed | Query the list of installed packages to determine if the MotionMark app (com.rdkcentral.motion) is already present: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be retrieved successfully. If com.rdkcentral.motion is already installed, the installation workflow is skipped. |
| 3 | Activate required AppManager plugins | If the MotionMark app is not installed, verify and activate the required plugin stack — org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}`<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}`<br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}}` | All three plugins should be in activated state before download and installation proceed. |
| 4 | Download MotionMark application bundle | Download the MotionMark application bundle from the configured URL: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/com.rdkcentral.motion+0.1.0.bolt"}}` | The MotionMark bundle should be downloaded successfully and a download ID should be returned. |
| 5 | Install MotionMark application bundle | Install the downloaded MotionMark bundle using PackageManagerRDKEMS with the file locator from device configuration: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.motion", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The MotionMark app bundle should be installed successfully. |
| 6 | Verify MotionMark application is installed | Confirm the MotionMark app appears in the installed packages list: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | com.rdkcentral.motion should appear in the installed packages list. |
| 7 | Launch MotionMark application | Launch the MotionMark application using AppManager: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.motion", "intent": "", "launchArgs": ""}}` | The MotionMark application should launch successfully. |
| 8 | Verify MotionMark application is running | Confirm the launched app appears in the active loaded apps list: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | com.rdkcentral.motion should be listed as an active loaded application. |
| 9 | Navigate MotionMark UI and start benchmark | Get the app instance ID of com.rdkcentral.motion from the loaded apps, then send key code 9 (Tab) and key code 13 (Enter) to the MotionMark application to navigate the UI and start the benchmark: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.generateKey", "params": {"appInstanceId": "<appInstanceId>", "keys": [{"keyCode": 9, "modifiers": [], "delay": 0.1}, {"keyCode": 13, "modifiers": [], "delay": 0.1}]}}` | Key events should be delivered to the MotionMark application, initiating the benchmark test. |
| 10 | Wait for MotionMark benchmark to complete | Wait 420 seconds (7 minutes) for the MotionMark benchmark to complete all its rendering test iterations. | The MotionMark benchmark should complete execution within the wait period. |
| 11 | Retrieve MotionMark benchmark score | Connect to the WebKit webinspect page and extract the main MotionMark FPS score from the benchmark test results. | The MotionMark score should be successfully retrieved and must not contain the value "Unable to get the browser score". |
| 12 | Validate MotionMark score against threshold | Compare the retrieved MotionMark score against `MOTIONMARK_THRESHOLD_VALUE` from the device configuration file. | The MotionMark benchmark score should be greater than the configured `MOTIONMARK_THRESHOLD_VALUE`. |
| 13 | Terminate MotionMark application | Terminate the MotionMark application after score validation: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminate", "params": {"appId": "com.rdkcentral.motion"}}` | The MotionMark application should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M97<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
