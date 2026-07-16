## TestCase ID
RDKV_STABILITY_12
## TestCase Name
RDKV_CERT_RVS_AppManager_LifeCycleManagement

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the full AppManager application lifecycle management by repeatedly performing the complete install, launch, terminate, and uninstall workflow for a configured number of iterations, verifying that device resource usage remains within acceptable limits after each full lifecycle cycle.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT in device config | The user should configure `PRE_REQ_REBOOT` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted in PerformanceTestVariables. | The app_download_url should point to a reachable hosting location. |
| 5 | Configure lifecyclecount in StabilityTestVariables | `lifecyclecount` must be set to the desired number of full lifecycle iterations in StabilityTestVariables (default: 100). | The lifecyclecount variable should be configured with a valid integer value. |
| 6 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. | The file locator path should be correctly configured in the device-specific config file. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT` configuration key. If set to "Yes", the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should come back online successfully if reboot was configured. |
| 2 | Verify and activate required plugins | Check the activation state of the required plugins: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager. Activate any that are not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@<plugin_name>"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All three required plugins should be in activated state. |
| 3 | Check if application is already installed (Per Iteration) | For each of the `lifecyclecount` (100) iterations, check the list of installed packages to determine whether com.rdkcentral.google is currently installed on the device. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be retrieved successfully. |
| 4 | Download, install, and launch application (Per Iteration) | If com.rdkcentral.google is not already installed, download the application bundle from the configured URL and install it using PackageManagerRDKEMS. Then launch the application using AppManager launchApp. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The application should be installed and launched successfully in each iteration. |
| 5 | Verify application is in loaded apps list (Per Iteration) | After launching, verify that com.rdkcentral.google appears in the list of loaded apps with APP_STATE_ACTIVE lifecycle state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | com.rdkcentral.google should appear in the loaded apps list in APP_STATE_ACTIVE state. |
| 6 | Terminate application (Per Iteration) | After a 20-second wait, terminate the running application using the AppManager terminateApp API. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.google"}}` | The application should terminate successfully. |
| 7 | Uninstall application (Per Iteration) | After a 30-second wait following termination, uninstall the application using the PackageManagerRDKEMS uninstall API. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.uninstall", "params": {"packageId": "com.rdkcentral.google"}}` | The application should be uninstalled successfully. |
| 8 | Validate resource usage after uninstall (Per Iteration) | After each successful uninstall, measure the current CPU load and memory usage via DeviceInfo.1.systeminfo to confirm resource usage is within acceptable limits. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should remain within the configured expected range after every full lifecycle cycle. |
| 9 | Repeat full lifecycle management for all iterations | Repeat Steps 3 through 8 for all `lifecyclecount` (100) configured iterations. | All iterations should complete the full install, launch, terminate, and uninstall lifecycle successfully with resource validation passing throughout the loop. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 30 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
