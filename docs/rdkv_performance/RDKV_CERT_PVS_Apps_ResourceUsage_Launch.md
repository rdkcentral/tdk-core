## TestCase ID
RDKV_PERFORMANCE_17
## TestCase Name
RDKV_CERT_PVS_Apps_ResourceUsage_Launch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the CPU and memory resource usage of the device while launching the Lightning/Unified Player application and verify that the resource usage is within acceptable limits.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is operational | The WPEFramework process must be running on the device before test execution begins. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT_PVS setting | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot (if configured) and be ready for test execution. |
| 3 | Confirm LOGGING_METHOD configuration | The `LOGGING_METHOD` key in the device configuration file must be set to either `REST_API` or `WEB_INSPECT` to determine how the Lightning application logs are monitored during the test. | The device configuration file should contain a valid `LOGGING_METHOD` value. |
| 4 | Confirm PACKAGEMANAGER_FILE_LOCATOR configuration | The `PACKAGEMANAGER_FILE_LOCATOR` key must be set in the device configuration file to specify the file system path used by PackageManager when installing the application bundle. | The `PACKAGEMANAGER_FILE_LOCATOR` configuration key should be set with a valid path in the device configuration file. |
| 5 | Confirm required plugins are activated | The DeviceInfo and org.rdk.PersistentStore plugins must be in the activated state on the device. | The DeviceInfo and org.rdk.PersistentStore plugins should be in the activated state. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Retrieve device configuration and logging method | Read the device configuration file to obtain the `LOGGING_METHOD` setting that determines how application console logs will be monitored during the test. | The device configuration file should be read successfully and the `LOGGING_METHOD` value should be retrieved. |
| 2 | Verify and configure required plugin states | Retrieve the current status of DeviceInfo and org.rdk.PersistentStore plugins using: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@DeviceInfo"}` <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.PersistentStore"}` <br>If any plugin is not activated, activate it: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"DeviceInfo"}}` <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"org.rdk.PersistentStore"}}` | Both DeviceInfo and org.rdk.PersistentStore plugins should report an activated status. |
| 3 | Build and store video test URL in PersistentStore | Construct the unified player test application URL with the configured video URL, operations, and logging arguments, then store it in PersistentStore: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PersistentStore.setValue","params":{"namespace":"MVS","key":"lightningURL","value":"<test_app_url>"}}` | The video test URL should be stored successfully in PersistentStore under namespace MVS with key lightningURL. |
| 4 | Verify if the unified player application is installed | Query the package manager to check whether the unified player application bundle is already installed: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The list of installed packages should be retrieved. If the app is already installed, the app name should appear in the package list. |
| 5 | Activate app management plugins for installation | If the unified player app is not installed, activate the required application management plugins: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"org.rdk.DownloadManager"}}` <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"org.rdk.PackageManagerRDKEMS"}}` <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"org.rdk.AppManager"}}` | The org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager plugins should be in the activated state. |
| 6 | Download the unified player application bundle | Initiate the download of the application bundle from the configured download URL: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<app_download_url>/<app_bundle_name>"}}` | The application bundle should be downloaded successfully. |
| 7 | Install the downloaded application bundle | Install the downloaded application bundle using PackageManager with the file locator from the device configuration (`PACKAGEMANAGER_FILE_LOCATOR`): <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PackageManagerRDKEMS.install","params":{"packageId":"<app_name>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<file_locator_path>"}}` | The application bundle should be installed successfully. |
| 8 | Verify the application installation | Confirm the application is installed by querying the package list: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed app name should appear in the package list with an INSTALLED state. |
| 9 | Launch the unified player application | Launch the unified player application via AppManager: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` <br>Verify the application is active: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getLoadedApps"}` | The application should be launched successfully and appear in the loaded apps list with a lifecycle state of APP_STATE_ACTIVE. |
| 10 | Monitor application log for launch confirmation | Monitor the application log (via REST_API log file or WEB_INSPECT WebSocket console) for the "URL Info:" message, which indicates the Lightning application has successfully loaded the URL from PersistentStore and begun video playback initialization. | The "URL Info:" confirmation message should appear in the application log, indicating the application has loaded and is ready. |
| 11 | Validate resource usage after application launch | After receiving the "URL Info:" confirmation, validate the CPU and memory usage of the device using the resource validation step, which internally invokes `DeviceInfo.1.systeminfo` to measure current CPU load and memory utilization: <br>`{"jsonrpc":"2.0","id":1,"method":"DeviceInfo.1.systeminfo"}` | The CPU and memory usage should be within the expected threshold limits. The resource usage validation should return SUCCESS with no ERROR status. |
| 12 | Terminate the unified player application | Terminate the launched application using AppManager: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_name>"}}` | The application should be terminated successfully. |
| 13 | Revert plugin states to original configuration | If any plugins were modified during test setup, restore their original states: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.deactivate","params":{"callsign":"<plugin_name>"}}` | All plugin states should be restored to their original configuration as captured before the test began. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 min

**Priority** : High

**Release Version** : M84<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
