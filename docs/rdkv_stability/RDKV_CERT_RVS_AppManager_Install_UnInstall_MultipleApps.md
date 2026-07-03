## TestCase ID
RDKV_STABILITY_11
## TestCase Name
RDKV_CERT_RVS_AppManager_Install_Uninstall_MultipleApps

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the stability of the AppManager install and uninstall workflow across multiple application bundles by repeatedly installing and uninstalling all configured apps for a defined number of iterations, verifying that device resource usage remains within acceptable limits after each install cycle.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT in device config | The user should configure `PRE_REQ_REBOOT` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure appmanager_test_apps in StabilityTestVariables | `appmanager_test_apps` must be set to a list of application bundle names to be used for the multi-app install/uninstall test in StabilityTestVariables. | The appmanager_test_apps list should contain valid application bundle names. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundles are hosted in PerformanceTestVariables. | The app_download_url should point to a reachable hosting location. |
| 5 | Configure install_uninstall_count in StabilityTestVariables | `install_uninstall_count` must be set to the desired number of install/uninstall cycle iterations in StabilityTestVariables (default: 100). | The install_uninstall_count variable should be configured with a valid integer value. |
| 6 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. | The file locator path should be correctly configured in the device-specific config file. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT` configuration key. If set to "Yes", the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should come back online successfully if reboot was configured. |
| 2 | Validate device resource usage before test | Check device state and resource usage before starting the stress test by measuring CPU and memory usage via DeviceInfo.1.systeminfo. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should be within the expected range before the test starts. |
| 3 | Verify and activate required plugins | Check the activation state of the required plugins: org.rdk.DownloadManager and org.rdk.PackageManagerRDKEMS. Activate any that are not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@<plugin_name>"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | Both org.rdk.DownloadManager and org.rdk.PackageManagerRDKEMS should be in activated state. |
| 4 | Check if application is already installed for each app (Per Iteration) | For each of the `install_uninstall_count` (100) outer iterations, and for each app_bundle in `appmanager_test_apps`, check the installed packages list to determine whether the app is currently installed. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be retrieved successfully for each app. |
| 5 | Uninstall application if already installed for each app (Per Iteration) | For each app in appmanager_test_apps, if the app is found in the installed packages list, uninstall it before proceeding with the new install cycle. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.uninstall", "params": {"packageId": "<app_name>"}}` | Each application should be uninstalled successfully before the new install cycle. |
| 6 | Download application bundle for each app (Per Iteration) | For each app in appmanager_test_apps, download the application bundle from the configured URL (`app_download_url`/`app_bundle`) using the DownloadManager download API. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<app_bundle>"}}` | Each application bundle should be downloaded successfully and a valid download ID should be returned. |
| 7 | Install application from downloaded bundle for each app (Per Iteration) | For each app in appmanager_test_apps, install the downloaded application bundle using the PackageManagerRDKEMS install API with the file locator path. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "<app_name>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | Each application should be installed successfully. |
| 8 | Validate resource usage after each app install (Per Iteration) | After each application is successfully installed, measure the current CPU load and memory usage via DeviceInfo.1.systeminfo to confirm resource usage is within acceptable limits. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should remain within the configured expected range after each individual app install. |
| 9 | Repeat multi-app install/uninstall cycle for all iterations | Repeat Steps 4 through 8 for all `install_uninstall_count` (100) configured outer iterations, processing all apps in appmanager_test_apps within each iteration. | All outer iterations should complete successfully with resource validation passing after every app install cycle. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 30 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
