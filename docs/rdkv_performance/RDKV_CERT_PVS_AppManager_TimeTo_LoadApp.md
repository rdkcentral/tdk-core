## TestCase ID
RDKV_PERFORMANCE_206
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_LoadApp
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the total time taken to load an application (download, install, and launch) via AppManager from a hosted URL is within the expected threshold limit.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, `org.rdk.AppManager`, and `org.rdk.LifecycleManager` plugins should be available and activatable on the device.|
|3|`PACKAGEMANAGER_APPLICATION_HOSTEDURL` and `PACKAGEMANAGER_APPLICATION_NAME` must be configured in the device config file.|
|4|`SUPPORTED_PLUGINS` must include the required plugins.|
|5|Time in Test Manager and DUT should be in sync with UTC.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check Plugin Availability | Verify `SUPPORTED_PLUGINS` from device config includes the required AppManager plugins. | All required plugins are supported on this device. |
| 2 | Check and Activate Plugins | Check status of each plugin and activate if not active. | All plugins in activated state. |
| 3 | Subscribe to Events | Register WebSocket listeners for lifecycle, download, and install events: <br>`{"jsonrpc":"2.0","id":7,"method":"org.rdk.LifecycleManager.1.register","params":{"event":"onAppLifecycleStateChanged","id":"client.events.1"}}`<br>`{"jsonrpc":"2.0","id":8,"method":"org.rdk.DownloadManager.1.register","params":{"event":"onAppDownloadStatus","id":"client.events.2"}}`<br>`{"jsonrpc":"2.0","id":9,"method":"org.rdk.AppManager.1.register","params":{"event":"onAppInstalled","id":"client.events.3"}}` | All event subscriptions established. |
| 4 | Get App Configuration | Retrieve `PACKAGEMANAGER_APPLICATION_HOSTEDURL` and `PACKAGEMANAGER_APPLICATION_NAME` from device config. Check if app is already installed via `org.rdk.AppManager.1.getInstalledApps`. | App configuration retrieved. |
| 5 | Download App (if not installed) | Download the app bundle from the hosted URL: `org.rdk.DownloadManager.1.download`. | Download completed. |
| 6 | Install App (if not installed) | Install the downloaded app bundle: `org.rdk.PackageManagerRDKEMS.install`. Wait for `onAppInstalled` event. | App installed successfully. |
| 7 | Record Load Start Time | Record the current UTC timestamp immediately before launching the app. | Load start time recorded. |
| 8 | Launch App | Launch the app via AppManager: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_id>","intent":"","launchArgs":""}}` | Launch request submitted. |
| 9 | Wait for APP_STATE_ACTIVE Event | Monitor the `onAppLifecycleStateChanged` event buffer until `APP_STATE_ACTIVE` is received. Record the event timestamp. | `APP_STATE_ACTIVE` event received. |
| 10 | Calculate and Validate Load Time | Calculate: load time = event timestamp - start time (in ms). Retrieve the load threshold from device config. Validate: load time < threshold. | Total time to load the app is within the configured threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
