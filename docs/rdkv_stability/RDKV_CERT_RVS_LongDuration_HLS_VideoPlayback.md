## TestCase ID
RDKV_CERT_RVS_5
## TestCase Name
RDKV_CERT_RVS_LongDuration_HLS_VideoPlayback

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability and resource usage during long-duration HLS video playback in the unified video player application for a minimum of 10 hours, confirming that CPU and memory usage remain within acceptable limits throughout the playback session.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT in device config | The user should configure `PRE_REQ_REBOOT` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure video_src_url_hls in StabilityTestVariables | `video_src_url_hls` must be set to a valid HLS video stream URL of at least 10 hours duration in StabilityTestVariables. | The video URL variable should point to a reachable HLS stream. |
| 4 | Configure unified_player_app_download_url in MediaValidationVariables | `unified_player_app_download_url` must be set to the full download URL of the unified video player application bundle. | The app download URL should be configured and the bundle should be reachable. |
| 5 | Configure codec_hls_h264 player list in MediaValidationVariables | `codec_hls_h264` must contain the player instance name(s) to be used for playback (comma-separated). | The player list should contain at least one valid player name. |
| 6 | Configure LOGGING_METHOD in device config | `LOGGING_METHOD` must be configured in the device-specific config file as either `REST_API` or `WEB_INSPECT`. | The LOGGING_METHOD key should be set to a valid value in the device config file. |
| 7 | Confirm DeviceInfo and PersistentStore plugins are available | The DeviceInfo and org.rdk.PersistentStore plugins must be present and activatable in the build. | Both plugins should be available and activatable on the DUT. |
| 8 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. | The file locator path should be correctly configured in the device-specific config file. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT` configuration. If set to "Yes", the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should come back online successfully if reboot was configured. |
| 2 | Validate device resource usage before test | Check device state and resource usage before starting the long-duration test. The DeviceInfo plugin is queried, activated if needed, and resource usage is measured via DeviceInfo.1.systeminfo. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should be within the expected range before the test starts. |
| 3 | Verify and activate required plugins | Check the activation state of the DeviceInfo and org.rdk.PersistentStore plugins. Activate any that are not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PersistentStore"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PersistentStore"}}` | Both DeviceInfo and org.rdk.PersistentStore should be in activated state. |
| 4 | Store HLS video test URL in PersistentStore | Store the configured HLS video test URL (from `video_src_url_hls`) into the PersistentStore so the unified video player application can retrieve it on launch. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "TDKVideoPlayer", "key": "video_test_url", "value": "<video_test_url>"}}` | The HLS video test URL should be successfully stored in PersistentStore. |
| 5 | Install unified video player application | Check if the unified video player application bundle is already installed. If not, activate DownloadManager, PackageManagerRDKEMS, and AppManager plugins, download the app bundle via DownloadManager, install it via PackageManagerRDKEMS, and verify it appears in the installed packages list. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<app_bundle_name>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "<app_name>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully and appear in the installed packages list. |
| 6 | Launch unified video player application | Launch the installed video player application using the AppManager launchApp API and verify the app is in the active state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<app_name>", "intent": "", "launchArgs": ""}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | The application should launch successfully and appear in the list of loaded apps in APP_STATE_ACTIVE. |
| 7 | Monitor HLS video playback and validate resource usage | Monitor the long-duration HLS video playback session for the configured test duration (36000 seconds / 10 hours). Depending on the logging method, resource usage is periodically measured. The app presence is confirmed via org.rdk.AppManager.getLoadedApps and CPU load and memory usage are measured. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | HLS video playback should continue without crash or termination throughout the entire 10-hour test duration. CPU and memory usage should remain within acceptable thresholds. |
| 8 | Terminate video player application | After the long-duration playback session completes or on failure, terminate the video player application via AppManager terminateApp. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "<app_name>"}}` | The application should terminate successfully. |
| 9 | Revert plugin statuses | If any plugins were activated during Step 3, revert them back to their original states using the Controller deactivate API. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.deactivate", "params": {"callsign": "<plugin_name>"}}` | Plugin states should be restored to their pre-test values. |
| 10 | Validate device resource usage after test | Check device state and resource usage after the long-duration test completes to confirm the device remains healthy. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should be within the expected range after the long-duration test completes. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 630 mins

**Priority** : High

**Release Version** : M92<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
