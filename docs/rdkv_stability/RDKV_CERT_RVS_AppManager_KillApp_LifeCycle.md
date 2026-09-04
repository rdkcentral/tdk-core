## TestCase ID
RDKV_STABILITY_17
## TestCase Name
RDKV_CERT_RVS_AppManager_KillApp_LifeCycle

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the AppManager correctly transitions an application through all expected kill lifecycle states (APP_STATE_PAUSED, APP_STATE_TERMINATING, and APP_STATE_UNLOADED) by subscribing to onAppLifecycleStateChanged event notifications and verifying that all three states are received in sequence for each kill operation across all configured iterations.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test before test execution begins. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT_PVS in device config | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle filename. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted in PerformanceTestVariables. | The app_download_url should point to a reachable and valid hosting location. |
| 5 | Configure AppManager_test_count in StabilityTestVariables | `AppManager_test_count` must be set to the desired number of kill lifecycle validation iterations in StabilityTestVariables (default: 100). | The AppManager_test_count variable should be configured with a valid integer value. |
| 6 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored, as required by the application installation process. | The file locator path should be correctly configured in the device-specific configuration file. |
| 7 | Confirm required plugins are available | The following plugins must be available and activatable on the device: org.rdk.DownloadManager, org.rdk.AppPackageManager, and org.rdk.AppManager. | All required plugins should be present and activatable on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT_PVS` configuration key. If set to Yes, the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | The device should come back online successfully if reboot was configured. |
| 2 | Verify and activate required plugins | Retrieve the current activation state of org.rdk.DownloadManager, org.rdk.AppPackageManager, and org.rdk.AppManager. Activate any plugin that is not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppPackageManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All three required plugins should be in the activated state before test execution proceeds. |
| 3 | Check if application is already installed | Query the installed package list to determine whether com.rdkcentral.google is currently installed on the device. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.1.listPackages"}` | The installed packages list should be retrieved successfully. |
| 4 | Download application bundle | If com.rdkcentral.google is not already installed, initiate the download of the configured application bundle from the configured download URL using the DownloadManager. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` | The application bundle download should initiate and complete successfully. |
| 5 | Install application on the device | Install the downloaded application bundle using the AppPackageManager install API, providing the file locator path obtained from the `PACKAGEMANAGER_FILE_LOCATOR` device configuration key and the download ID returned by the download step. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.install", "params": {"packageId": "com.rdkcentral.google", "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/<download_id>"}}` | The application should be installed successfully on the device. |
| 6 | Verify application installation | Confirm that com.rdkcentral.google appears in the installed packages list after installation. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.1.listPackages"}` | The application should appear in the installed packages list, confirming successful installation. |
| 7 | Subscribe to lifecycle state change event | Register a WebSocket event listener to subscribe to the onAppLifecycleStateChanged event from org.rdk.AppManager. Wait 5 seconds after registration before starting the iteration loop. <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}}` | The event subscription should be established successfully and the WebSocket event listener should be active and ready. |
| 8 | Launch application (Per Iteration) | For each of the `AppManager_test_count` (100) iterations, launch the com.rdkcentral.google application using the AppManager launchApp API. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google"}}` | The launchApp API should return SUCCESS and the application should be launched successfully for each iteration. |
| 9 | Wait for application to become active (Per Iteration) | After a successful launch, wait 30 seconds to allow the application to reach an active running state before the kill operation. | The application should be in a running state after the wait period. |
| 10 | Kill the application (Per Iteration) | Kill the running application using the AppManager killApp API, which forces an immediate termination of the application process. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.killApp", "params": {"appId": "com.rdkcentral.google"}}` | The killApp API should return SUCCESS for each iteration. |
| 11 | Monitor lifecycle event buffer after kill (Per Iteration) | Monitor the onAppLifecycleStateChanged event buffer for up to 120 seconds after the kill request, collecting all lifecycle state transition events for com.rdkcentral.google. The monitoring loop exits when APP_STATE_UNLOADED is observed or the timeout is reached. | The event buffer should yield lifecycle events within the 120-second monitoring window. |
| 12 | Verify all kill lifecycle states received (Per Iteration) | Verify that all three expected kill lifecycle state transitions are received for com.rdkcentral.google: APP_STATE_PAUSED (app paused before termination), APP_STATE_TERMINATING (app in termination process), and APP_STATE_UNLOADED (app fully unloaded from memory). <br>`{"jsonrpc": "2.0", "method": "client.events.1.onAppLifecycleStateChanged", "params": {"appId": "com.rdkcentral.google", "newState": "APP_STATE_PAUSED"}}` <br><br>`{"jsonrpc": "2.0", "method": "client.events.1.onAppLifecycleStateChanged", "params": {"appId": "com.rdkcentral.google", "newState": "APP_STATE_TERMINATING"}}` <br><br>`{"jsonrpc": "2.0", "method": "client.events.1.onAppLifecycleStateChanged", "params": {"appId": "com.rdkcentral.google", "newState": "APP_STATE_UNLOADED"}}` | All three kill lifecycle states (APP_STATE_PAUSED, APP_STATE_TERMINATING, and APP_STATE_UNLOADED) should be received for each iteration. |
| 13 | Repeat kill lifecycle validation for all iterations | Repeat Steps 8 through 12 for all `AppManager_test_count` (100) configured iterations. | Every iteration should successfully receive all three expected kill lifecycle events, confirming a valid and complete kill lifecycle transition sequence across all iterations. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 250 minutes

**Priority** : High

**Release Version** : M151<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
