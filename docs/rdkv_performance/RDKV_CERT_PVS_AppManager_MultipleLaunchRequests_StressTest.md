## TestCase ID
RDKV_PERFORMANCE_181
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
To validate the AppManager's robustness and stability when multiple concurrent launch requests are sent for the same application, ensuring that no duplicate app instances are created and the system remains responsive.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, `org.rdk.AppManager`, and `org.rdk.LifecycleManager` plugins should be available and activatable on the device.|
|3|`PACKAGEMANAGER_APPLICATION_HOSTEDURL` and `PACKAGEMANAGER_APPLICATION_NAME` must be configured in the device config file.|
|4|`MULTIPLE_LAUNCH_REQUEST_COUNT` (default: 5) and `LAUNCH_REQUEST_DELAY_MS` (default: 100ms) can optionally be configured in device config.|
|5|`SUPPORTED_PLUGINS` must include the essential AppManager plugins in device config.|
|6|Device should be ready for testing (pre-requisite reboot is not required for this test).|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check Plugin Availability | Verify that `org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, and `org.rdk.AppManager` are listed in `SUPPORTED_PLUGINS` in device config. | All required plugins are available on this device. |
| 2 | Check and Activate Plugins | Query status of each plugin and activate if not already active: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@org.rdk.AppManager"}` | All AppManager plugins are in activated state. |
| 3 | Subscribe to Events | Register WebSocket listeners for lifecycle changes, download status, and install events: <br>`{"jsonrpc":"2.0","id":7,"method":"org.rdk.LifecycleManager.1.register","params":{"event":"onAppLifecycleStateChanged","id":"client.events.1"}}`<br>`{"jsonrpc":"2.0","id":8,"method":"org.rdk.DownloadManager.1.register","params":{"event":"onAppDownloadStatus","id":"client.events.2"}}`<br>`{"jsonrpc":"2.0","id":9,"method":"org.rdk.AppManager.1.register","params":{"event":"onAppInstalled","id":"client.events.3"}}` | All event subscriptions established. |
| 4 | Get Test App Configuration | Retrieve the app download URL and app ID from device config: `PACKAGEMANAGER_APPLICATION_HOSTEDURL` and `PACKAGEMANAGER_APPLICATION_NAME`. | App URL and ID retrieved successfully. |
| 5 | Install Target App | Download and install the app bundle using the configured URL. Verify via `org.rdk.PackageManagerRDKEMS.1.listPackages`. | App is installed successfully. |
| 6 | Send Multiple Concurrent Launch Requests | Send `MULTIPLE_LAUNCH_REQUEST_COUNT` (default: 5) simultaneous launch requests with `LAUNCH_REQUEST_DELAY_MS` (default: 100ms) between each: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_name>","intent":"","launchArgs":""}}` | All launch requests submitted. |
| 7 | Validate No Duplicate App Instances | Verify that only one instance of the app is active using `org.rdk.AppManager.getLoadedApps` and check lifecycle events. | Only a single app instance is active; duplicate instances are not created. |
| 8 | Validate System Stability | Check that AppManager and other core plugins remain responsive after the stress test by querying plugin status. | System remains stable; no crashes or unresponsive services detected. |
| 9 | Cleanup | Terminate the app and uninstall if required. | App is cleaned up; environment is restored. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
