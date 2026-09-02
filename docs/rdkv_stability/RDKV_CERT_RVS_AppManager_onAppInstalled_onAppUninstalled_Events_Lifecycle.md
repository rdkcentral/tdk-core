## TestCase ID
RDKV_STABILITY_21
## TestCase Name
RDKV_CERT_RVS_AppManager_AppLifeCycleState
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the AppManager correctly tracks and reports the lifecycle state of an application through preload, launch, close, and terminate operations, ensuring the lifecycleState matches the targetLifecycleState at each transition point, and that system resource usage remains within acceptable limits across all configured iterations.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test before test execution begins. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT in device config | The user should configure `PRE_REQ_REBOOT` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Verify device CPU and memory usage are within limits | The device CPU and memory usage must be within the acceptable range before the test begins. The DeviceInfo plugin is activated if needed to retrieve resource usage metrics. | CPU and memory usage should be within the expected acceptable range on the device. |
| 4 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle filename. |
| 5 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted in PerformanceTestVariables. | The app_download_url should point to a reachable and valid hosting location. |
| 6 | Configure AppManager_test_count in StabilityTestVariables | `AppManager_test_count` must be set to the desired number of lifecycle validation iterations in StabilityTestVariables (default: 100). | The AppManager_test_count variable should be configured with a valid integer value. |
| 7 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. | The file locator path should be correctly configured in the device-specific configuration file. |
| 8 | Confirm required plugins are available | The following plugins must be available and activatable on the device: org.rdk.DownloadManager, org.rdk.AppPackageManager, org.rdk.AppManager, and org.rdk.RDKWindowManager. | All required plugins should be present and activatable on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT` configuration key. If set to Yes, the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | The device should come back online successfully if reboot was configured. |
| 2 | Validate device resource usage state | Check the activation state of the DeviceInfo plugin and activate it if needed, then validate that the device CPU and memory usage are within the acceptable range before proceeding. <br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@DeviceInfo"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}` | Device CPU and memory usage should be within the expected range, confirming the device is in a healthy state before testing. |
| 3 | Verify and activate required plugins | Retrieve the current activation state of org.rdk.DownloadManager, org.rdk.AppPackageManager, org.rdk.AppManager, and org.rdk.RDKWindowManager. Activate any plugin that is not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppPackageManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.RDKWindowManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All four required plugins should be in the activated state before test execution proceeds. |
| 4 | Check if application is already installed | Query the installed package list to determine whether com.rdkcentral.test_app is currently installed on the device. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.1.listPackages"}` | The installed packages list should be retrieved successfully. |
| 5 | Download and install application | If com.rdkcentral.test_app is not already installed, download the configured application bundle and install it on the device. The application is installed without launching at this stage. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.install", "params": {"packageId": "com.rdkcentral.test_app", "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/<download_id>"}}` | The application should be downloaded and installed successfully. The app should appear in the installed packages list. |
| 6 | Preload application (Per Iteration) | For each of the `AppManager_test_count` (100) iterations, preload the application com.rdkcentral.test_app using the AppManager preloadApp API to initiate the preload lifecycle state. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.preloadApp", "params": {"appId": "com.rdkcentral.test_app"}}` | The preloadApp API should return SUCCESS for each iteration. |
| 7 | Verify lifecycle state after preload (Per Iteration) | Wait 10 seconds and then retrieve the list of loaded applications to verify that the lifecycleState of com.rdkcentral.test_app matches its targetLifecycleState following the preload operation. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.getLoadedApps"}` | The lifecycleState should match the targetLifecycleState in the getLoadedApps response for com.rdkcentral.test_app after preloading. |
| 8 | Launch application (Per Iteration) | Launch com.rdkcentral.test_app using the AppManager launchApp API after the preload state is confirmed. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.test_app"}}` | The launchApp API should return SUCCESS for each iteration. |
| 9 | Verify lifecycle state after launch (Per Iteration) | Wait 20 seconds and then retrieve the list of loaded applications to verify that the lifecycleState of com.rdkcentral.test_app matches its targetLifecycleState following the launch operation. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.getLoadedApps"}` | The lifecycleState should match the targetLifecycleState in the getLoadedApps response for com.rdkcentral.test_app after launching. |
| 10 | Close application (Per Iteration) | Close the running application com.rdkcentral.test_app using the AppManager closeApp API. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.closeApp", "params": {"appId": "com.rdkcentral.test_app"}}` | The closeApp API should return SUCCESS for each iteration. |
| 11 | Verify lifecycle state after close (Per Iteration) | Wait 10 seconds and then retrieve the list of loaded applications to verify that the lifecycleState of com.rdkcentral.test_app matches its targetLifecycleState following the close operation. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.getLoadedApps"}` | The lifecycleState should match the targetLifecycleState in the getLoadedApps response for com.rdkcentral.test_app after closing. |
| 12 | Validate resource usage (Per Iteration) | Validate that the device CPU and memory resource usage are within the configured acceptable limits after the close operation. | Device CPU and memory usage should be within the expected acceptable range, confirming no resource leak after the lifecycle operations. |
| 13 | Terminate application (Per Iteration) | Terminate the application com.rdkcentral.test_app using the AppManager terminateApp API to fully unload it from memory before the next iteration. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.test_app"}}` | The terminateApp API should return SUCCESS and the application should be fully unloaded for each iteration. |
| 14 | Repeat lifecycle state validation for all iterations | Repeat Steps 6 through 13 for all `AppManager_test_count` (100) configured iterations. | Every iteration should successfully complete all lifecycle transitions (preload, launch, close, terminate) with matching lifecycleState and targetLifecycleState at each stage, and resource usage should remain within acceptable limits throughout. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 250 minutes

**Priority** : High

**Release Version** : M151<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
