## TestCase ID
RDKV_CERT_RVS_7
## TestCase Name
RDKV_CERT_RVS_WebKitBrowser_Load_GraphicsApp

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability and resource usage while loading and running a graphics application URL in the unified player application via WebKitBrowser for a configured duration of up to 6 hours, confirming that CPU and memory usage remain within acceptable limits throughout the test.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT in device config | The user should configure `PRE_REQ_REBOOT` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure graphics_app_url in StabilityTestVariables | `graphics_app_url` must be set to a valid graphics application URL in StabilityTestVariables (e.g., a TDK object animations LightningApp URL with count, fps, object, autotest, and duration arguments). | The graphics_app_url variable should be configured with a valid and reachable URL. |
| 4 | Configure load_graphics_app_test_duration in StabilityTestVariables | `load_graphics_app_test_duration` must be set to the desired test duration in minutes in StabilityTestVariables (default: 360 minutes). | The test duration variable should be configured with a valid integer value. |
| 5 | Configure animation_graphics_app_download_url in MediaValidationVariables | `animation_graphics_app_download_url` must be set to the full download URL of the graphics application bundle in MediaValidationVariables. | The app download URL should be configured and the bundle should be reachable. |
| 6 | Confirm DeviceInfo and PersistentStore plugins are available | The DeviceInfo and org.rdk.PersistentStore plugins must be present and activatable in the build. | Both plugins should be available and activatable on the DUT. |
| 7 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. | The file locator path should be correctly configured in the device-specific config file. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT` configuration. If set to "Yes", the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should come back online successfully if reboot was configured. |
| 2 | Validate device resource usage before test | Check device state and resource usage before starting the long-duration test by measuring CPU and memory usage via DeviceInfo.1.systeminfo. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should be within the expected range before the test starts. |
| 3 | Verify and activate required plugins | Check the activation state of the DeviceInfo and org.rdk.PersistentStore plugins. Activate any that are not already in the activated state. Original states are saved for revert. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PersistentStore"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PersistentStore"}}` | Both DeviceInfo and org.rdk.PersistentStore should be in activated state. |
| 4 | Store graphics application test URL in PersistentStore | Store the configured `graphics_app_url` into the PersistentStore so the graphics application can retrieve it on launch. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PersistentStore.1.setValue", "params": {"namespace": "TDKVideoPlayer", "key": "video_test_url", "value": "<graphics_app_url>"}}` | The graphics application test URL should be successfully stored in PersistentStore. |
| 5 | Install graphics application | Check if the graphics application bundle is already installed. If not, activate DownloadManager, PackageManagerRDKEMS, and AppManager plugins, download the bundle from `animation_graphics_app_download_url` via DownloadManager, install it via PackageManagerRDKEMS, and verify it appears in the installed packages list. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<animation_graphics_app_download_url>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "<app_name>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The graphics application should be installed successfully and appear in the installed packages list. |
| 6 | Launch graphics application | Launch the installed graphics application using the AppManager launchApp API and verify the app is in the active running state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<app_name>", "intent": "", "launchArgs": ""}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | The graphics application should launch successfully and appear in the list of loaded apps in APP_STATE_ACTIVE. |
| 7 | Verify application is running and validate resource usage (Per Interval) | At each 30-second interval (test_interval = 30) throughout the configured test duration (load_graphics_app_test_duration), verify the graphics application is still running by checking the loaded apps list, then measure CPU load and memory usage. Resource usage data is recorded per iteration. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | The application should remain running throughout the test duration. CPU and memory usage should remain within acceptable thresholds at every 30-second interval. |
| 8 | Repeat resource validation for all test duration intervals | Repeat Step 7 at every 30-second interval for the entire configured test duration (load_graphics_app_test_duration minutes). | All resource validation checks should pass throughout the configured test duration with the application remaining in the active state. |
| 9 | Revert plugin statuses | If any plugins were activated during Step 3, revert them back to their original states via the Controller deactivate API. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.deactivate", "params": {"callsign": "<plugin_name>"}}` | Plugin states should be restored to their pre-test values. |
| 10 | Validate device resource usage after test | Check device state and resource usage after the test completes to confirm the device remains in a healthy state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "DeviceInfo.1.systeminfo"}` | CPU and memory usage should be within the expected range after the graphics application test completes. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 370 mins

**Priority** : High

**Release Version** : M89<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
