## TestCase ID
RDKV_CERT_RVS_15
## TestCase Name
RDKV_CERT_RVS_AppManager_TerminateApp_LifeCycle

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate AppManager terminate application lifecycle state transitions by registering for onAppLifecycleStateChanged event notifications and verifying that all expected lifecycle states (APP_STATE_ACTIVE, APP_STATE_PAUSED, APP_STATE_TERMINATING) are received in the correct sequence following each app terminate operation across all configured iterations.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT_PVS in device config | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Confirm required plugins are available | The org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager plugins must be present and activatable in the build. | All three required plugins should be available on the DUT. |
| 4 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 5 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted in PerformanceTestVariables. | The app_download_url should point to a reachable hosting location. |
| 6 | Configure lifecycle_count in StabilityTestVariables | `lifecycle_count` must be set to the desired number of lifecycle validation iterations in StabilityTestVariables (default: 100). | The lifecycle_count variable should be configured with a valid integer value. |
| 7 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. | The file locator path should be correctly configured in the device-specific config file. |
| 8 | Confirm WebSocket connectivity to Thunder is available | WebSocket connectivity to the Thunder JSON-RPC endpoint on the device must be available for event listener registration. | WebSocket connection to Thunder should be established successfully. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT_PVS` configuration key. If set to "Yes", the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | Device should come back online successfully if reboot was configured. |
| 2 | Verify and activate required plugins | Check the activation state of the required plugins: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, and org.rdk.AppManager. Activate any that are not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@<plugin_name>"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All three required plugins should be in activated state. |
| 3 | Check if application is already installed | Check the list of installed packages to determine whether com.rdkcentral.google is currently installed on the device. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be retrieved successfully. |
| 4 | Download and install application | If com.rdkcentral.google is not already installed, download the application bundle from the configured URL and install it using PackageManagerRDKEMS. Verify the app appears in the installed packages list. The application is not launched at this stage. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully and appear in the installed packages list. |
| 5 | Subscribe to lifecycle state change event | Register a WebSocket event listener to subscribe to the onAppLifecycleStateChanged event from org.rdk.AppManager before beginning the iteration loop. <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}}` | Event subscription should be established successfully and the WebSocket event listener should be active. |
| 6 | Launch application (Per Iteration) | For each of the `lifecycle_count` (100) iterations, launch the com.rdkcentral.google application using the AppManager launchApp API. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The launch API should return SUCCESS for each iteration. |
| 7 | Wait before terminating application (Per Iteration) | After a successful launch, wait 30 seconds to allow the application to fully initialize and reach the active state before initiating the terminate request. | The 30-second wait should allow the application to reach the active running state. |
| 8 | Terminate application (Per Iteration) | Terminate the running application using the AppManager terminateApp API. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.google"}}` | The terminate API should return SUCCESS for each iteration. |
| 9 | Validate all expected terminate lifecycle events (Per Iteration) | Monitor the onAppLifecycleStateChanged event buffer for up to 120 seconds after the terminate request. Verify that all three expected terminate lifecycle states are received for com.rdkcentral.google: APP_STATE_ACTIVE, APP_STATE_PAUSED, and APP_STATE_TERMINATING. The monitoring loop exits when APP_STATE_TERMINATING is observed. <br>Example event: `{"jsonrpc": "2.0", "method": "client.events.1.onAppLifecycleStateChanged", "params": {"appId": "com.rdkcentral.google", "newState": "APP_STATE_TERMINATING", "oldState": "APP_STATE_PAUSED", "errorReason": "APP_ERROR_NONE"}}` | All three expected terminate lifecycle states (APP_STATE_ACTIVE, APP_STATE_PAUSED, APP_STATE_TERMINATING) should be received for each iteration. |
| 10 | Repeat terminate lifecycle validation for all iterations | Repeat Steps 6 through 9 for all `lifecycle_count` (100) configured iterations. | Every iteration should receive all three expected terminate lifecycle events successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 30 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
