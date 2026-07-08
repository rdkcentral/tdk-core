## TestCase ID
RDKV_PERFORMANCE_30
## TestCase Name
RDKV_CERT_PVS_Apps_TimeTo_Launch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the time taken to launch the Lightning/Unified Player application and verify that the launch time is within the configured threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is operational | The WPEFramework process must be running on the device before test execution begins. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT_PVS setting | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot (if configured) and be ready for test execution. |
| 3 | Confirm LOGGING_METHOD configuration | The `LOGGING_METHOD` key in the device configuration file must be set to either `REST_API` or `WEB_INSPECT` to determine how the Lightning application logs are monitored during the test. | The device configuration file should contain a valid `LOGGING_METHOD` value. |
| 4 | Confirm APP_LAUNCH_THRESHOLD_VALUE configuration | The `APP_LAUNCH_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` keys must be configured in the device configuration file to define the acceptable time range for application launch. | The `APP_LAUNCH_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` keys should be present and populated with valid values in the device configuration file. |
| 5 | Confirm PACKAGEMANAGER_FILE_LOCATOR configuration | The `PACKAGEMANAGER_FILE_LOCATOR` key must be set in the device configuration file to specify the file system path used by PackageManager when installing the application bundle. | The `PACKAGEMANAGER_FILE_LOCATOR` configuration key should be set with a valid path in the device configuration file. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Retrieve device configuration and logging method | Read the device configuration file to obtain the `LOGGING_METHOD` setting that determines how application console logs will be monitored during the test. | The device configuration file should be read successfully and the `LOGGING_METHOD` value should be retrieved. |
| 2 | Verify and configure required plugin states | Retrieve the current status of DeviceInfo and org.rdk.PersistentStore plugins using the following JSON-RPC call: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.PersistentStore"}` <br>If any plugin is not in the activated state, activate it using: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"DeviceInfo"}}` <br><br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"org.rdk.PersistentStore"}}` | Both DeviceInfo and org.rdk.PersistentStore plugins should report an activated status. |
| 3 | Build and store video test URL in PersistentStore | Construct the unified player test application URL with the configured video URL, operations, and logging arguments, then store it in PersistentStore using the following JSON-RPC call: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PersistentStore.setValue","params":{"namespace":"MVS","key":"lightningURL","value":"<test_app_url>"}}` | The video test URL should be stored successfully in PersistentStore under namespace MVS with key lightningURL. |
| 4 | Verify if the unified player application is installed | Query the package manager to determine whether the unified player application bundle is already installed on the device: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The list of installed packages should be retrieved. If the app is already installed, the app name should appear in the package list and installation steps should be skipped. |
| 5 | Activate app management plugins for installation | If the unified player app is not installed, activate the required application management plugins: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"org.rdk.DownloadManager"}}` <br><br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"org.rdk.PackageManagerRDKEMS"}}` <br><br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"org.rdk.AppManager"}}` | The org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager plugins should all be in the activated state. |
| 6 | Download the unified player application bundle | Initiate the download of the application bundle from the configured download URL: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<app_download_url>/<app_bundle_name>"}}` | The application bundle should be downloaded successfully and the download result should be returned. |
| 7 | Install the downloaded application bundle | Install the downloaded application bundle using PackageManager with the file locator path from the device configuration (`PACKAGEMANAGER_FILE_LOCATOR`): <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PackageManagerRDKEMS.install","params":{"packageId":"<app_name>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<file_locator_path>"}}` | The application bundle should be installed successfully. |
| 8 | Verify the application installation | Confirm the application is installed by querying the package list again: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed app name should appear in the package list with an INSTALLED state. |
| 9 | Record start time and launch the unified player application | Record the current UTC timestamp as the launch initiation time, then launch the unified player application via AppManager: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` | The application launch request should be submitted successfully. |
| 10 | Verify the application is active | Confirm the application has been launched and is in the active state by querying the loaded apps: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getLoadedApps"}` | The app ID should appear in the loaded apps list with a lifecycle state of APP_STATE_ACTIVE. |
| 11 | Monitor application log for launch confirmation | Monitor the application log (via REST_API log file monitoring or WEB_INSPECT WebSocket console) for the "URL Info:" message. For REST_API: monitor the app log file (`<logpath>/<execID>_<execDevId>_<resultId>_mvs_applog.txt`) for lines containing "URL Info:". For WEB_INSPECT: connect to the WebInspect WebSocket endpoint and monitor console messages for "URL Info:". The timestamp from this log line is treated as the actual application launch time. | The "URL Info:" confirmation message should appear in the application log, indicating the Lightning application has successfully loaded the URL from PersistentStore. |
| 12 | Calculate and validate application launch time | Calculate the application launch time as the difference between the "URL Info:" log timestamp and the recorded launch initiation time. Retrieve threshold values from the device configuration: `APP_LAUNCH_THRESHOLD_VALUE` and `THRESHOLD_OFFSET`. Validate that the launch time falls within: `0 < launch_time < (APP_LAUNCH_THRESHOLD_VALUE + THRESHOLD_OFFSET)`. | The time taken to launch the application should be within the expected range defined by `APP_LAUNCH_THRESHOLD_VALUE` plus `THRESHOLD_OFFSET`. |
| 13 | Terminate the unified player application | Terminate the launched application using AppManager: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_name>"}}` | The application should be terminated successfully. |
| 14 | Revert plugin states to original configuration | If any plugins were modified during test setup, restore their original states using: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.deactivate","params":{"callsign":"<plugin_name>"}}` | All plugin states should be restored to their original configuration as captured before the test began. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 6 mins

**Priority** : High

**Release Version** : M82<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
