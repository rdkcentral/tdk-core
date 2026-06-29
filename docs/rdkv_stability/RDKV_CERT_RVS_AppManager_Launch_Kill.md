## TestCase ID
RDKV_CERT_RVS_10
## TestCase Name
RDKV_CERT_RVS_AppManager_Launch_Kill

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the stability of the AppManager launch and kill workflow by repeatedly launching and forcibly killing a native application for a configured number of iterations, verifying that device resource usage remains within acceptable limits after each launch-kill cycle.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT in device config | The user should configure `PRE_REQ_REBOOT` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Confirm required plugins are available | The org.rdk.DownloadManager and org.rdk.PackageManagerRDKEMS plugins must be present and activatable in the build. | Both required plugins should be available on the DUT. |
| 4 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 5 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted in PerformanceTestVariables. | The app_download_url should point to a reachable hosting location. |
| 6 | Configure launch_kill_count in StabilityTestVariables | `launch_kill_count` must be set to the desired number of launch/kill cycle iterations in StabilityTestVariables (default: 100). | The launch_kill_count variable should be configured with a valid integer value. |
| 7 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. | The file locator path should be correctly configured in the device-specific config file. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT` configuration key. If set to "Yes", the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should come back online successfully if reboot was configured. |
| 2 | Validate device resource usage before test | Check device state and resource usage before starting the stress test by measuring CPU and memory usage via DeviceInfo.1.systeminfo. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should be within the expected range before the test starts. |
| 3 | Verify and activate required plugins | Check the activation state of the required plugins: org.rdk.DownloadManager and org.rdk.PackageManagerRDKEMS. Activate any that are not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@<plugin_name>"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | Both org.rdk.DownloadManager and org.rdk.PackageManagerRDKEMS should be in activated state. |
| 4 | Check if application is already installed | Check the list of installed packages to determine whether com.rdkcentral.google is currently installed on the device. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be retrieved successfully. |
| 5 | Download and install application | If com.rdkcentral.google is not already installed, download the application bundle from the configured URL and install it using PackageManagerRDKEMS. Verify the app appears in the installed packages list before the stress loop begins. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully and appear in the installed packages list. |
| 6 | Launch application (Per Iteration) | For each of the `launch_kill_count` (100) iterations, wait 10 seconds then launch the com.rdkcentral.google application using the AppManager launchApp API. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The application should launch successfully and the API should return SUCCESS. |
| 7 | Verify application is listed in loaded apps (Per Iteration) | After a successful launch, retrieve the list of loaded apps from org.rdk.AppManager.getLoadedApps and confirm that com.rdkcentral.google is present with APP_STATE_ACTIVE lifecycle state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | com.rdkcentral.google should appear in the loaded apps list in APP_STATE_ACTIVE state. |
| 8 | Kill application (Per Iteration) | After a 10-second wait following the successful launch verification, forcibly kill the running application using the AppManager killApp API. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.killApp", "params": {"appId": "com.rdkcentral.google"}}` | The application should be killed successfully and the API should return SUCCESS. |
| 9 | Validate resource usage after kill (Per Iteration) | After each successful kill, wait 10 seconds then measure the current CPU load and memory usage via DeviceInfo.1.systeminfo to confirm resource usage is within acceptable limits. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should remain within the configured expected range after every launch-kill cycle. |
| 10 | Repeat launch-kill cycle for all iterations | Repeat Steps 6 through 9 for all `launch_kill_count` (100) configured iterations. | All iterations should complete successfully and resource validation should pass throughout the stress loop. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 30 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
