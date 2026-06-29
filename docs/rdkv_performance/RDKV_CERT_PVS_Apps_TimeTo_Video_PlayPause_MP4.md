## TestCase ID
RDKV_PERFORMANCE_119
## TestCase Name
RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_MP4
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the time taken for the Lightning/Unified Player application to pause and resume an MP4 video stream and verify that both transitions complete within the configured time thresholds.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is operational | The WPEFramework process must be running on the device before test execution begins. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT_PVS setting | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot (if configured) and be ready for test execution. |
| 3 | Confirm LOGGING_METHOD configuration | The `LOGGING_METHOD` key in the device configuration file must be set to either `REST_API` or `WEB_INSPECT`. | The device configuration file should contain a valid `LOGGING_METHOD` value. |
| 4 | Confirm PACKAGEMANAGER_FILE_LOCATOR configuration | The `PACKAGEMANAGER_FILE_LOCATOR` key must be set in the device configuration file. | The `PACKAGEMANAGER_FILE_LOCATOR` configuration key should be set with a valid path. |
| 5 | Confirm PAUSE_TIME_THRESHOLD_VALUE and PLAY_TIME_THRESHOLD_VALUE are configured | The `PAUSE_TIME_THRESHOLD_VALUE`, `PLAY_TIME_THRESHOLD_VALUE`, and `THRESHOLD_OFFSET` values must be set in PerformanceTestVariables. | The timing threshold variables should be configured with valid numeric values. |
| 6 | Confirm the MP4 video stream URL is configured | The `video_src_url_mp4` variable in PerformanceTestVariables must be configured with a valid MP4 video stream URL with video type "mp4". | The MP4 video URL should be configured and accessible. |
| 7 | Confirm required plugins are activated | The DeviceInfo and org.rdk.PersistentStore plugins must be in the activated state. | Both plugins should be in the activated state. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Retrieve device configuration and logging method | Read the device configuration file to obtain the `LOGGING_METHOD` setting. Configure the video test URL using the MP4 video source (`video_src_url_mp4`) with video type "mp4" and MP4 codec player list (`codec_mp4`). Set play and pause operations: `setOperation("pause", 10)` and `setOperation("play", 10)`. | The device configuration file should be read successfully and the `LOGGING_METHOD` value should be retrieved. |
| 2 | Verify and configure required plugin states | Retrieve the current status of DeviceInfo and org.rdk.PersistentStore plugins: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@DeviceInfo"}` <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.PersistentStore"}` <br>If any plugin is not activated, activate it: <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"DeviceInfo"}}` <br>`{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"org.rdk.PersistentStore"}}` | Both DeviceInfo and org.rdk.PersistentStore plugins should report an activated status. |
| 3 | Build and store MP4 video test URL in PersistentStore | Construct the unified player test application URL with the MP4 video URL, pause/play operations, and logging arguments. Store it in PersistentStore: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PersistentStore.setValue","params":{"namespace":"MVS","key":"lightningURL","value":"<test_app_url>"}}` | The MP4 test URL should be stored successfully in PersistentStore under namespace MVS with key lightningURL. |
| 4 | Verify if the unified player application is installed | Query the package manager to check whether the unified player application bundle is already installed: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The list of installed packages should be retrieved. If the app is already installed, installation steps should be skipped. |
| 5 | Activate app management plugins and install the application | If the unified player app is not installed, activate the required plugins and download and install the bundle: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<app_download_url>/<app_bundle_name>"}}` <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.PackageManagerRDKEMS.install","params":{"packageId":"<app_name>","version":"0.1.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<file_locator_path>"}}` | The application bundle should be downloaded and installed successfully. |
| 6 | Launch the unified player application with MP4 video | Launch the application via AppManager: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` <br>Verify the application is active: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getLoadedApps"}` | The application should be launched and appear in loaded apps with APP_STATE_ACTIVE. |
| 7 | Monitor play and pause events during MP4 video playback | Monitor the application log (via REST_API log file or WEB_INSPECT WebSocket console) for the following event messages: "Expected Event: paused", "Observed Event: paused", "Expected Event: play", "Observed Event: play", and "TEST RESULT:". Extract the timestamps from each event message. | All four event messages should be observed in the application log, and "TEST RESULT: SUCCESS" should be received, confirming the MP4 video was successfully paused and resumed. |
| 8 | Calculate and validate time to pause the MP4 video | Calculate TimeTo_Pause as the difference between the observed_pause_evt timestamp and the expected_pause_evt timestamp. Validate: TimeTo_Pause must be less than or equal to `PAUSE_TIME_THRESHOLD_VALUE` + `THRESHOLD_OFFSET`. | The TimeTo_Pause value should be within the configured `PAUSE_TIME_THRESHOLD_VALUE` + `THRESHOLD_OFFSET` limit. The test step should report SUCCESS if the threshold is met. |
| 9 | Calculate and validate time to resume the MP4 video | Calculate TimeTo_Play as the difference between the observed_play_evt timestamp and the expected_play_evt timestamp. Validate: TimeTo_Play must be less than or equal to `PLAY_TIME_THRESHOLD_VALUE` + `THRESHOLD_OFFSET`. | The TimeTo_Play value should be within the configured `PLAY_TIME_THRESHOLD_VALUE` + `THRESHOLD_OFFSET` limit. The test step should report SUCCESS if the threshold is met. |
| 10 | Terminate the unified player application | Terminate the launched application: <br>`{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_name>"}}` | The application should be terminated successfully. |
| 11 | Revert plugin states to original configuration | If any plugins were modified during test setup, restore their original states. | All plugin states should be restored to their original configuration. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 6 min

**Priority** : High

**Release Version** : M99<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
