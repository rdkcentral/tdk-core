## TestCase ID
RDKV_PERFORMANCE_212
## TestCase Name
RDKV_CERT_PVS_AppManager_UninstallLaunchedApp_Stability
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the system remains stable and fully functional after uninstalling an AppManager-managed application while it is actively running, with WPEFramework, plugins, and memory all functioning normally post-uninstall.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, `org.rdk.AppManager`, and `org.rdk.SystemServices` plugins should be available and activatable on the device.|
|3|`PACKAGEMANAGER_APPLICATION_HOSTEDURL` and `PACKAGEMANAGER_APPLICATION_NAME` must be configured in the device config file.|
|4|`SUPPORTED_PLUGINS` must include the required plugins.|
|5|Device should be ready for testing (pre-requisite reboot is not required for this test).|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check Plugin Availability | Verify `SUPPORTED_PLUGINS` includes `org.rdk.DownloadManager`, `org.rdk.PackageManagerRDKEMS`, `org.rdk.AppManager`, and `org.rdk.SystemServices`. | All required plugins are supported. |
| 2 | Check and Activate Plugins | Check and activate all required plugins. | All plugins in activated state. |
| 3 | Subscribe to Events | Register WebSocket listeners for lifecycle, download, install, and uninstall events: <br>`{"jsonrpc":"2.0","id":7,"method":"org.rdk.LifecycleManager.1.register","params":{"event":"onAppLifecycleStateChanged","id":"client.events.1"}}`<br>`{"jsonrpc":"2.0","id":8,"method":"org.rdk.DownloadManager.1.register","params":{"event":"onAppDownloadStatus","id":"client.events.2"}}`<br>`{"jsonrpc":"2.0","id":9,"method":"org.rdk.AppManager.1.register","params":{"event":"onAppInstalled","id":"client.events.3"}}`<br>`{"jsonrpc":"2.0","id":10,"method":"org.rdk.AppManager.1.register","params":{"event":"onAppUninstalled","id":"client.events.4"}}` | All event subscriptions established. |
| 4 | Get App Configuration | Retrieve `PACKAGEMANAGER_APPLICATION_HOSTEDURL` and `PACKAGEMANAGER_APPLICATION_NAME` from device config. Check installed apps via `org.rdk.AppManager.1.getInstalledApps`. | App configuration retrieved. |
| 5 | Install App (if not installed) | Download via `org.rdk.DownloadManager.1.download` and install via `org.rdk.PackageManagerRDKEMS.install`. Wait for `onAppInstalled` event. | App installed successfully. |
| 6 | Launch App | Launch the app while it is installed: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_id>","intent":"","launchArgs":""}}` Wait for `APP_STATE_ACTIVE` event. | App launched and running in active state. |
| 7 | Uninstall App While Running | Uninstall the app while it is actively running: <br>`org.rdk.PackageManagerRDKEMS.1.uninstallPackage` with `{"packageId":"<app_id>"}` Wait for `onAppUninstalled` event. | Uninstall request processed; `onAppUninstalled` event received. |
| 8 | Verify System Stability After Uninstall | Check system stability after uninstalling the running app: verify WPEFramework responsiveness via `org.rdk.SystemServices.1.getSystemVersions`, verify plugin responsiveness, check memory stability, and confirm no crash indicators are present. | WPEFramework is responsive, all plugins are functional, memory usage is stable, and no crashes or zombie processes are detected after uninstalling the running app. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
