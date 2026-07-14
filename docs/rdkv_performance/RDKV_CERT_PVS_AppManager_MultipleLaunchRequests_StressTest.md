## TestCase ID
RDKV_PERFORMANCE_64
## TestCase Name
RDKV_CERT_PVS_AppManager_MultipleLaunchRequests_StressTest

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the AppManager handles multiple simultaneous launch requests gracefully under stress conditions, ensuring no duplicate app instances are created, no system crashes occur, and the framework remains responsive after processing the multiple concurrent launch requests.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device application hosting URL | The device configuration file must have `PACKAGEMANAGER_APPLICATION_HOSTEDURL` set to the hosted URL from which the application bundle can be downloaded. | The application hosted URL should be correctly configured. |
| 3 | Configure application name in device config | The device configuration file must have `PACKAGEMANAGER_APPLICATION_NAME` set to the application ID (package name) to be used in the stress test. | The application package name should be correctly configured. |
| 4 | Configure stress test parameters in device config | The device configuration file must have `MULTIPLE_LAUNCH_REQUEST_COUNT` set to the number of concurrent launch requests (default: 5) and `LAUNCH_REQUEST_DELAY_MS` set to the millisecond delay between requests (default: 100 ms). | Stress test configuration parameters should be correctly set. |
| 5 | Configure supported plugins list | The device configuration file must have `SUPPORTED_PLUGINS` populated with the list of plugins available on the device. | The supported plugins list should be correctly configured. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query the status of all required plugins and activate any that are not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All required plugins should be in the activated state. |
| 2 | Subscribe to lifecycle, download, and install events | Establish a WebSocket event listener and subscribe to all relevant events to monitor the system during the stress test. <br>`{"jsonrpc": "2.0", "id": 7, "method": "org.rdk.LifecycleManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}}` <br><br>`{"jsonrpc": "2.0", "id": 8, "method": "org.rdk.DownloadManager.1.register", "params": {"event": "onAppDownloadStatus", "id": "client.events.2"}}` <br><br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppInstalled", "id": "client.events.3"}}` | All event subscriptions should be established successfully. |
| 3 | Download the application bundle | Download the application bundle from `PACKAGEMANAGER_APPLICATION_HOSTEDURL`, preparing it for installation before the multiple launch stress test. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}` | The download should complete successfully and a download ID should be returned. |
| 4 | Install the application | Install the downloaded application bundle on the device. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully before the stress test begins. |
| 5 | Send multiple simultaneous launch requests | Issue `MULTIPLE_LAUNCH_REQUEST_COUNT` (default: 5) consecutive launch requests with `LAUNCH_REQUEST_DELAY_MS` (default: 100 ms) delay between each request. Track the number of launch requests sent, responses received, lifecycle events received, duplicate instances detected, and error responses. <br>Each launch request: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": "", "launchArgs": ""}}` | All launch requests should be submitted. The AppManager should handle the concurrent requests gracefully without crashing. No duplicate application instances should be created. |
| 6 | Verify system health post-stress — AppManager responsiveness | After all launch requests are processed, verify the AppManager remains functional by querying the running applications list. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.getInstalledApps", "params": {}}` | The AppManager should remain responsive and return the installed apps list successfully after the stress test. |
| 7 | Verify system health post-stress — framework responsiveness | Confirm WPEFramework remains responsive after the stress test by querying system information. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.SystemServices.1.getSystemVersions", "params": {}}` | WPEFramework should remain responsive and return system information successfully, confirming no crash occurred. |
| 8 | Validate stress test results | Query the currently running applications to count the number of active instances of the test app, then evaluate all collected stress test metrics: confirm no duplicate instances were created, no excessive error responses were returned, the system remained responsive, and the lifecycle events count is reasonable. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.getRunningApps", "params": {}}` | The stress test should complete with no duplicate app instances, no system crashes, no unhandled errors, and all AppManager responses should indicate graceful handling of the concurrent requests. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
