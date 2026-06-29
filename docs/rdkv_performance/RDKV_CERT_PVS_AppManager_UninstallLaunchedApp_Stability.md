## TestCase ID
RDKV_PERFORMANCE_1
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
To validate that the system remains stable after uninstalling a launched application via the AppManager, verifying WPEFramework responsiveness, plugin functionality, memory operations, and service availability post-uninstall.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Confirm required plugins are available | The following plugins must be present in the device build: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, org.rdk.AppManager, org.rdk.SystemServices. | All required AppManager plugins should be available in the build. |
| 3 | Configure device application hosting URL | The device configuration file must have `PACKAGEMANAGER_APPLICATION_HOSTEDURL` set to the hosted URL from which the application bundle can be downloaded. | The application hosted URL should be correctly configured in the device-specific config file. |
| 4 | Configure application name in device config | The device configuration file must have `PACKAGEMANAGER_APPLICATION_NAME` set to the application ID (package name) to be used in the test. | The application package name should be correctly configured in the device-specific config file. |
| 5 | Configure supported plugins list | The device configuration file must have `SUPPORTED_PLUGINS` populated with the list of plugins available on the device. | The supported plugins list should be correctly configured so that essential plugin availability checks can be performed. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query the activation state of each required plugin and activate any that are not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.SystemServices"}` <br>Activate any inactive plugin: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All required plugins should be in the activated state. |
| 2 | Subscribe to lifecycle, download, install, and uninstall events | Establish a WebSocket event listener and subscribe to the following events to capture all AppManager lifecycle transitions during the test. <br>`{"jsonrpc": "2.0", "id": 7, "method": "org.rdk.LifecycleManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}}` <br>`{"jsonrpc": "2.0", "id": 8, "method": "org.rdk.DownloadManager.1.register", "params": {"event": "onAppDownloadStatus", "id": "client.events.2"}}` <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppInstalled", "id": "client.events.3"}}` <br>`{"jsonrpc": "2.0", "id": 10, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppUninstalled", "id": "client.events.4"}}` | Event subscriptions should be established successfully. All four event types should be actively monitored. |
| 3 | Download and install the application | Download the application bundle from the configured hosted URL and install the package. Verify the app appears in the installed packages list. <br>Download: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>/<app_bundle>"}}` <br>List installed packages: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` <br>Install: `{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application bundle should be downloaded and installed successfully. The app should appear in the installed packages list. |
| 4 | Launch the installed application | Send a launch request for the installed application and wait for the app to reach the active state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": "", "launchArgs": ""}}` | The application should launch successfully and reach the APP_STATE_ACTIVE lifecycle state. |
| 5 | Uninstall the launched application | Send an uninstall request for the currently launched application. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}` | The uninstall request should succeed and the onAppUninstalled event should be received. |
| 6 | Assess system stability — verify WPEFramework responsiveness | Check that WPEFramework remains responsive after the uninstall operation by invoking a system information API. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.SystemServices.1.getSystemVersions", "params": {}}` | WPEFramework should remain responsive and return system version information successfully. |
| 7 | Assess system stability — verify AppManager functionality | Confirm that the AppManager plugin is still functional after uninstall by querying the list of installed applications. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.getInstalledApps", "params": {}}` | The AppManager should respond successfully, confirming plugin operational stability post-uninstall. |
| 8 | Assess system stability — verify memory operations | Validate memory operation stability by querying the list of currently running applications. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.getRunningApps", "params": {}}` | The running apps query should succeed, indicating that memory operations remain stable. |
| 9 | Assess system stability — verify plugin service availability | Confirm the availability and activation state of each essential plugin (org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, org.rdk.AppManager) to validate overall service health. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` | All essential plugin services should be available and responsive post-uninstall, confirming system stability. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
