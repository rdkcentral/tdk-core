## TestCase ID
RDKV_PERFORMANCE_6
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
To validate that the time taken to load an application via the AppManager — encompassing download, installation, and launch to the active state — is within the configured performance thresholds.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Confirm required plugins are available | The following plugins must be present and activatable: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, org.rdk.AppManager. | All required plugins should be available in the build. |
| 3 | Configure device application hosting URL | The device configuration file must have `PACKAGEMANAGER_APPLICATION_HOSTEDURL` set to the hosted URL from which the application bundle can be downloaded. | The application hosted URL should be correctly configured. |
| 4 | Configure application name in device config | The device configuration file must have `PACKAGEMANAGER_APPLICATION_NAME` set to the application ID to be used in the test. | The application package name should be correctly configured. |
| 5 | Configure supported plugins list | The device configuration file must have `SUPPORTED_PLUGINS` populated with the list of plugins available on the device. | The supported plugins list should be correctly configured. |
| 6 | Configure load thresholds in device config | The device configuration file should contain timeout and threshold values for download, install, launch, and load operations. | Threshold values should be present and correctly configured for performance validation. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Query the status of all required plugins and activate any that are not in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.DownloadManager"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}` <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@org.rdk.AppManager"}` <br>Activate if needed: `{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All required plugins should be in the activated state. |
| 2 | Subscribe to lifecycle, download, and install events | Establish a WebSocket event listener and subscribe to all relevant events to track the full app loading sequence. <br>`{"jsonrpc": "2.0", "id": 7, "method": "org.rdk.LifecycleManager.1.register", "params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1"}}` <br>`{"jsonrpc": "2.0", "id": 8, "method": "org.rdk.DownloadManager.1.register", "params": {"event": "onAppDownloadStatus", "id": "client.events.2"}}` <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.AppManager.1.register", "params": {"event": "onAppInstalled", "id": "client.events.3"}}` | All event subscriptions should be established successfully. |
| 3 | Check if the application is already installed | Query the AppManager to determine whether the target application is already present on the device. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.1.getInstalledApps", "params": {}}` | The installed apps list should be returned and the presence or absence of the target application should be determinable. |
| 4 | Download the application bundle (if not installed) | If the application is not already installed, initiate the download from the configured hosted URL and record the download start time. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>", "appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}` | The download should be initiated successfully and the onAppDownloadStatus event should be received on completion. |
| 5 | Install the downloaded application bundle | After download completes, install the application package and wait for the onAppInstalled event. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully and the onAppInstalled event should be received within the install timeout. |
| 6 | Launch the application and measure load time | Record the launch request start time, send the launch request, and wait for the onAppLifecycleStateChanged event confirming APP_STATE_ACTIVE. The load timeout is 180 seconds. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": "", "launchArgs": ""}}` | The application should reach the APP_STATE_ACTIVE lifecycle state within the 180-second load timeout. |
| 7 | Validate load time against configured threshold | Compute the total load time in milliseconds from the launch request to the APP_STATE_ACTIVE event timestamp. Validate the time is within the configured threshold and offset values. | The application load time should be within the configured performance threshold range. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
