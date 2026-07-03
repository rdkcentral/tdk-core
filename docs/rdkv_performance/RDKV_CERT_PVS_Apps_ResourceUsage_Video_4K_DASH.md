## TestCase ID
RDKV_PERFORMANCE_27
## TestCase Name
RDKV_CERT_PVS_Apps_ResourceUsage_Video_4K_DASH
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the CPU and memory resource usage of the device during 4K DASH video playback in the Lightning/Unified Player application and verify that resource usage is within acceptable limits.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is operational | The WPEFramework process must be running on the device before test execution begins. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT_PVS setting | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot (if configured) and be ready for test execution. |
| 3 | Confirm LOGGING_METHOD configuration | The `LOGGING_METHOD` key in the device configuration file must be set to either `REST_API` or `WEB_INSPECT`. | The device configuration file should contain a valid `LOGGING_METHOD` value. |
| 4 | Confirm PACKAGEMANAGER_FILE_LOCATOR configuration | The `PACKAGEMANAGER_FILE_LOCATOR` key must be set in the device configuration file. | The `PACKAGEMANAGER_FILE_LOCATOR` configuration key should be set with a valid path. |
| 5 | Confirm the 4K DASH video stream URL is configured | The `video_src_url_4k_dash` variable in MediaValidationVariables must be configured with a valid 4K DASH video stream URL. | The 4K DASH video URL should be configured and accessible. |
| 6 | Confirm required plugins are activated | The DeviceInfo and org.rdk.PersistentStore plugins must be in the activated state. | Both plugins should be in the activated state. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Retrieve device configuration and logging method | Read the device configuration file to obtain the `LOGGING_METHOD` setting. Configure the video test URL using the 4K DASH video source (`video_src_url_4k_dash`) with video type "dash" and DASH HEVC codec player list (`codec_dash_hevc`). Set the close operation with a 5-second interval: `setOperation("close", 5)`. | The device configuration file should be read successfully and the `LOGGING_METHOD` value should be retrieved. |
| 2 | Verify and configure required plugin states | Retrieve the current status of DeviceInfo and org.rdk.PersistentStore plugins: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.PersistentStore"}` <br>If any plugin is not activated, activate it: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"DeviceInfo"}}` <br><br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"org.rdk.PersistentStore"}}` | Both DeviceInfo and org.rdk.PersistentStore plugins should report an activated status. |
| 3 | Build and store 4K DASH video test URL in PersistentStore | Construct the unified player test application URL with the 4K DASH video URL, close operation, and logging arguments. Store it in PersistentStore: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PersistentStore.setValue","params":{"namespace":"MVS","key":"lightningURL","value":"<test_app_url>"}}` | The 4K DASH video test URL should be stored successfully in PersistentStore under namespace MVS with key lightningURL. |
| 4 | Verify if the unified player application is installed | Query the package manager to check whether the unified player application bundle is already installed: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The list of installed packages should be retrieved. If the app is already installed, installation steps should be skipped. |
| 5 | Activate app management plugins and install the application | If the unified player app is not installed, activate the required plugins and download and install the bundle: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<app_download_url>/<app_bundle_name>"}}` <br><br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PackageManagerRDKEMS.install","params":{"packageId":"<app_name>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<file_locator_path>"}}` | The application bundle should be downloaded and installed successfully. |
| 6 | Launch the unified player application with 4K DASH video | Launch the unified player application via AppManager: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` <br>Verify the application is active: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getLoadedApps"}` | The application should be launched and appear in loaded apps with APP_STATE_ACTIVE. The application should begin loading the 4K DASH video stream. |
| 7 | Monitor application log for 4K DASH video playback confirmation | Monitor the application log (via REST_API log file or WEB_INSPECT WebSocket console) for the "URL Info:" message indicating the application has successfully loaded the 4K DASH video URL and started playback. | The "URL Info:" confirmation message should appear in the application log. |
| 8 | Validate resource usage during 4K DASH video playback | After receiving the "URL Info:" confirmation, validate the CPU and memory usage using the resource validation step, which internally invokes `DeviceInfo.1.systeminfo`: <br>`{"jsonrpc":"2.0","id":1,"method":"DeviceInfo.1.systeminfo"}` | The CPU and memory usage should be within the expected threshold limits during 4K DASH video playback. The resource usage validation should return SUCCESS with no ERROR status. |
| 9 | Terminate the unified player application | Terminate the launched application: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_name>"}}` | The application should be terminated successfully. |
| 10 | Revert plugin states to original configuration | If any plugins were modified during test setup, restore their original states. | All plugin states should be restored to their original configuration. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 min

**Priority** : High

**Release Version** : M103<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
