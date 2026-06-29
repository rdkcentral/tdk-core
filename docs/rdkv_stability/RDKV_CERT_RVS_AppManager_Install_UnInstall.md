## TestCase ID
RDKV_CERT_RVS_8
## TestCase Name
RDKV_CERT_RVS_AppManager_Install_UnInstall

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the stability of the AppManager install and uninstall workflow by repeatedly uninstalling and reinstalling a native application for a configured number of iterations, verifying that device resource usage remains within acceptable limits after each install cycle.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT in device config | The user should configure `PRE_REQ_REBOOT` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Confirm required plugins are available | The org.rdk.DownloadManager and org.rdk.PackageManagerRDKEMS plugins must be present and activatable in the build. | Both required plugins should be available on the DUT. |
| 4 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 5 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted in PerformanceTestVariables. | The app_download_url should point to a reachable hosting location. |
| 6 | Configure install_uninstall_count in StabilityTestVariables | `install_uninstall_count` must be set to the desired number of install/uninstall cycle iterations in StabilityTestVariables (default: 100). | The install_uninstall_count variable should be configured with a valid integer value. |
| 7 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. | The file locator path should be correctly configured in the device-specific config file. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT` configuration key. If set to "Yes", the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should come back online successfully if reboot was configured. |
| 2 | Validate device resource usage before test | Check device state and resource usage before starting the stress test by measuring CPU and memory usage via DeviceInfo.1.systeminfo. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should be within the expected range before the test starts. |
| 3 | Verify and activate required plugins | Check the activation state of the required plugins: org.rdk.DownloadManager and org.rdk.PackageManagerRDKEMS. Activate any that are not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@<plugin_name>"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | Both org.rdk.DownloadManager and org.rdk.PackageManagerRDKEMS should be in activated state. |
| 4 | Check if application is already installed (Per Iteration) | For each of the `install_uninstall_count` (100) iterations, check the list of installed packages to determine whether com.rdkcentral.google is currently installed. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be retrieved successfully. |
| 5 | Uninstall application if already installed (Per Iteration) | If com.rdkcentral.google is found in the installed packages list, uninstall it before proceeding with the install cycle. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.uninstall", "params": {"packageId": "com.rdkcentral.google"}}` | The application should be uninstalled successfully. |
| 6 | Download application bundle (Per Iteration) | Download the application bundle from the configured URL (`app_download_url`/`google_bundle`) using the DownloadManager download API. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` | The application bundle should be downloaded successfully and a valid download ID should be returned. |
| 7 | Install application from downloaded bundle (Per Iteration) | Install the downloaded application bundle using the PackageManagerRDKEMS install API with the file locator path (PACKAGEMANAGER_FILE_LOCATOR + download_id). <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully. |
| 8 | Validate resource usage after install (Per Iteration) | After each successful installation, measure the current CPU load and memory usage via DeviceInfo.1.systeminfo to confirm resource usage is within the acceptable limit. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should remain within the configured expected range after every install cycle. |
| 9 | Repeat install/uninstall cycle for all iterations | Repeat Steps 4 through 8 for all `install_uninstall_count` (100) configured iterations. | All iterations should complete successfully and resource validation should pass throughout the stress loop. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 30 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
