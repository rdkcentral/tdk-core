## TestCase ID
RDKV_PERFORMANCE_91
## TestCase Name
RDKV_CERT_PVS_AppManager_UninstallApp_HealthCheck

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the system remains stable after uninstalling an application via the AppManager, confirming WPEFramework responsiveness, plugin service availability, memory stability, and the absence of crashes following the uninstall operation.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device application hosting URL | The device configuration file must have `PACKAGEMANAGER_APPLICATION_HOSTEDURL` set to the hosted URL from which the application bundle can be downloaded. | The application hosted URL should be correctly configured in the device-specific config file. |
| 3 | Configure application name in device config | The device configuration file must have `PACKAGEMANAGER_APPLICATION_NAME` set to the application ID (package name) to be used in the test. | The application package name should be correctly configured in the device-specific config file. |
| 4 | Configure supported plugins list | The device configuration file must have `SUPPORTED_PLUGINS` populated with the list of plugins available on the device. | The supported plugins list should be correctly configured so that essential plugin availability checks can be performed. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query the activation state of each required plugin and activate any that are not in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.SystemServices"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All required plugins should be in the activated state before test execution. |
| 2 | Subscribe to lifecycle, download, install, and uninstall events | Establish a WebSocket event listener and subscribe to all relevant AppManager events. <br>`{"jsonrpc": "2.0", "id": 7, "method": "org.rdk.LifecycleManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}}` <br><br>`{"jsonrpc": "2.0", "id": 8, "method": "org.rdk.DownloadManager.1.register", "params": {"event": "onAppDownloadStatus", "id": "client.events.2"}}` <br><br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppInstalled", "id": "client.events.3"}}` <br><br>`{"jsonrpc": "2.0", "id": 10, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppUninstalled", "id": "client.events.4"}}` | All event subscriptions should be established successfully. |
| 3 | Download the application bundle | Download the application bundle from the configured hosted URL. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>/<app_bundle>"}}` | The download should complete successfully and a download ID should be returned. |
| 4 | Install the application | Install the downloaded application bundle on the device. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be downloaded and installed successfully. |
| 5 | Uninstall the application | Send an uninstall request for the installed application without launching it first. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}` | The uninstall request should succeed and the onAppUninstalled event should be received confirming removal. |
| 6 | Verify WPEFramework is still responsive | Check WPEFramework responsiveness after uninstall by querying system version information. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.SystemServices.1.getSystemVersions", "params": {}}` | WPEFramework should remain responsive and return system information successfully, indicating no crash occurred. |
| 7 | Verify essential plugins remain responsive | Check that org.rdk.AppManager and org.rdk.PackageManagerRDKEMS are still responsive and functional following the uninstall. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.getPluginStatus", "params": {}}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.getPluginStatus", "params": {}}` | All essential plugins should remain responsive after the uninstall operation. |
| 8 | Verify memory stability via installed apps query | Confirm memory stability by successfully querying the list of installed applications, which validates that memory management remains intact. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.getInstalledApps", "params": {}}` | The query should succeed, confirming that memory operations are stable post-uninstall. |
| 9 | Validate overall system stability | Confirm no system crashes occurred by evaluating all stability indicators together: WPEFramework responsiveness, plugin service availability, and memory stability. All checks should pass simultaneously. | All stability checks should pass. No crashes should be detected. The system should be in a stable operational state after the uninstall. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
