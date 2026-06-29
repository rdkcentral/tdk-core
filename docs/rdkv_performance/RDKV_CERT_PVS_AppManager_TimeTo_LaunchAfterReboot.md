## TestCase ID
RDKV_PERFORMANCE_8
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_LaunchAfterReboot

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to launch a pre-installed application after a device reboot via the AppManager is within the configured performance threshold, measured from the launch request (post-reboot) to the receipt of the APP_STATE_ACTIVE lifecycle state change event.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Confirm required plugins are available | The following plugins must be present and activatable: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, org.rdk.AppManager. | All required plugins should be available in the build. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted. | The app_download_url should point to a reachable hosting location. |
| 5 | Configure launch-after-reboot threshold in device config | `APPMANAGER_LAUNCH_AFTER_REBOOT_THRESHOLD` and `THRESHOLD_OFFSET` must be set in the device-specific configuration file. `REBOOT_WAIT_TIME` must also be configured to specify how long to wait after reboot. | Threshold, offset, and reboot wait time values should be correctly configured. |
| 6 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path where downloaded packages are stored on the device. | The file locator path should be correctly configured. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query and activate the required plugins to ensure they are in the activated state before installation. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All required plugins should be in the activated state. |
| 2 | Install the application without launching it | Download and install the application bundle so it is present on the device before reboot. <br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` <br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully before reboot. |
| 3 | Reboot the device | Trigger a device reboot via the system restart API and wait for the `REBOOT_WAIT_TIME` duration configured in the device config for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | The device should reboot successfully and come back online within the configured wait time. |
| 4 | Validate device uptime post-reboot | After reconnecting, verify that the device uptime is less than 280 seconds, confirming a fresh reboot occurred. | Device uptime should be less than 280 seconds, confirming successful reboot completion. |
| 5 | Verify plugins are active after reboot | Check the status of all required plugins after reboot and activate any that have not yet started. Allow additional startup time if needed. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` | All required plugins should return to the activated state after reboot. |
| 6 | Subscribe to the lifecycle state change event | Register a WebSocket event listener for onAppLifecycleStateChanged to capture the APP_STATE_ACTIVE event after reboot. <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}}` | Event subscription should be established successfully post-reboot. |
| 7 | Launch the application post-reboot and record start time | Record the current UTC timestamp as the launch start time, then send the launch request for the pre-installed application. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The launch request should be accepted by the AppManager after reboot. |
| 8 | Wait for APP_STATE_ACTIVE event and calculate launch time | Monitor the event buffer until the onAppLifecycleStateChanged event containing APP_STATE_ACTIVE is received or a 120-second timeout is reached. Extract the completion timestamp and compute elapsed launch time in milliseconds. Compare against `APPMANAGER_LAUNCH_AFTER_REBOOT_THRESHOLD` + `THRESHOLD_OFFSET`. | The APP_STATE_ACTIVE event should be received within the timeout and the launch time should be within the configured performance threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
