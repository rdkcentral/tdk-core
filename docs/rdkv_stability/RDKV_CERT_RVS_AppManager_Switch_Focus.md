## TestCase ID
RDKV_STABILITY_20
## TestCase Name
RDKV_CERT_RVS_AppManager_Switch_Focus

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the RDKWindowManager focus switching mechanism by installing and launching two application instances simultaneously, subscribing to the onFocus event, and iteratively switching focus between the two applications across all configured iterations, verifying that the onFocus event is received with the correct application instance identifier after each focus change operation.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test before test execution begins. | WPEFramework should be up and running on the device. |
| 2 | Configure PRE_REQ_REBOOT_PVS in device config | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle filename. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted in PerformanceTestVariables. | The app_download_url should point to a reachable and valid hosting location. |
| 5 | Configure AppManager_test_count in StabilityTestVariables | `AppManager_test_count` must be set to the desired number of focus switch iterations in StabilityTestVariables (default: 100). | The AppManager_test_count variable should be configured with a valid integer value. |
| 6 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path on the DUT where downloaded packages are stored. | The file locator path should be correctly configured in the device-specific configuration file. |
| 7 | Confirm required plugins are available | The following plugins must be available and activatable on the device: org.rdk.DownloadManager, org.rdk.AppPackageManager, org.rdk.AppManager, and org.rdk.RDKWindowManager. | All required plugins should be present and activatable on the device. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Conditionally reboot device before test | Conditionally reboot the device based on the `PRE_REQ_REBOOT_PVS` configuration key. If set to Yes, the device is rebooted by invoking the Thunder Controller harakiri method and the script waits 150 seconds for the device to come back online. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.harakiri"}` | The device should come back online successfully if reboot was configured. |
| 2 | Verify and activate required plugins | Retrieve the current activation state of org.rdk.DownloadManager, org.rdk.AppPackageManager, org.rdk.AppManager, and org.rdk.RDKWindowManager. Activate any plugin that is not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppPackageManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.AppManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.status@org.rdk.RDKWindowManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All four required plugins should be in the activated state before test execution proceeds. |
| 3 | Install and launch Test App 1 | Check if com.rdkcentral.testapp1 is already installed. If not, download and install the application bundle using DownloadManager and AppPackageManager, then launch com.rdkcentral.testapp1 using the AppManager launchApp API. Wait 5 seconds after launch. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.1.listPackages"}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppPackageManager.install", "params": {"packageId": "com.rdkcentral.testapp1", "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/<download_id>"}}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.testapp1"}}` | Test App 1 should be installed and launched successfully. |
| 4 | Install and launch Test App 2 | Check if com.rdkcentral.testapp2 is already installed. If not, download and install the application bundle, then launch com.rdkcentral.testapp2 using the AppManager launchApp API. Wait 5 seconds after launch. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.testapp2"}}` | Test App 2 should be installed and launched successfully. |
| 5 | Retrieve loaded app instance IDs | Wait 20 seconds, then retrieve the list of loaded applications and extract the appInstanceId for both com.rdkcentral.testapp1 and com.rdkcentral.testapp2 where lifecycleState is APP_STATE_ACTIVE. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.getLoadedApps"}` | Both application instance IDs should be retrieved successfully from the loaded apps list. |
| 6 | Subscribe to RDKWindowManager onFocus event | Register a WebSocket event listener to subscribe to the onFocus event from org.rdk.RDKWindowManager. Wait 10 seconds after registration to ensure the listener is ready before the iteration loop begins. <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.RDKWindowManager.1.register", "params": {"event": "onFocus", "id": "client.events.1"}}` | The onFocus event subscription should be established successfully and the WebSocket event listener should be active. |
| 7 | Clear event buffer (Per Iteration) | For each of the `AppManager_test_count` (100) iterations, clear the event listener buffer to discard any stale events before the focus switch operations for that iteration. | The event buffer should be cleared successfully before each iteration's focus switch operations. |
| 8 | Set focus on Test App 1 (Per Iteration) | Set the window focus to Test App 1 using the RDKWindowManager setFocus API with the appInstanceId of com.rdkcentral.testapp1. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.RDKWindowManager.1.setFocus", "params": {"client": "<app_instance_id_1>"}}` | The setFocus API should return SUCCESS for Test App 1 for each iteration. |
| 9 | Verify onFocus event received for Test App 1 (Per Iteration) | Monitor the event buffer for up to 120 seconds to verify that an onFocus event containing the appInstanceId of com.rdkcentral.testapp1 is received, confirming that focus was successfully transferred to Test App 1. <br>`{"jsonrpc": "2.0", "method": "client.events.1.onFocus", "params": {"client": "<app_instance_id_1>"}}` | The onFocus event should be received with the appInstanceId of com.rdkcentral.testapp1 within the monitoring period. |
| 10 | Set focus on Test App 2 (Per Iteration) | After successfully receiving the focus event for Test App 1, set the window focus to Test App 2 using the RDKWindowManager setFocus API with the appInstanceId of com.rdkcentral.testapp2. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.RDKWindowManager.1.setFocus", "params": {"client": "<app_instance_id_2>"}}` | The setFocus API should return SUCCESS for Test App 2 for each iteration. |
| 11 | Verify onFocus event received for Test App 2 (Per Iteration) | Monitor the event buffer for up to 120 seconds to verify that an onFocus event containing the appInstanceId of com.rdkcentral.testapp2 is received, confirming that focus was successfully transferred to Test App 2. <br>`{"jsonrpc": "2.0", "method": "client.events.1.onFocus", "params": {"client": "<app_instance_id_2>"}}` | The onFocus event should be received with the appInstanceId of com.rdkcentral.testapp2 within the monitoring period. |
| 12 | Repeat focus switch validation for all iterations | Repeat Steps 7 through 11 for all `AppManager_test_count` (100) configured iterations. | Every iteration should successfully switch focus between both applications and receive the corresponding onFocus events with the correct application instance identifiers, confirming reliable focus management across all iterations. |
| 13 | Terminate both applications after test | After completing all focus switching iterations, terminate both com.rdkcentral.testapp1 and com.rdkcentral.testapp2 using the AppManager terminateApp API to clean up the device state. <br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.testapp1"}}` <br><br>`{"jsonrpc": "2.0", "id": 1, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.testapp2"}}` | Both applications should be terminated successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 200 minutes

**Priority** : High

**Release Version** : M151<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
