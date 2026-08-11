## TestCase ID
RDKV_PERFORMANCE_101
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_SetVisible_App

<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To measure and validate the time taken to receive the onVisible event from RDKWindowManager after calling setVisible with visible=true on a previously hidden application, and verify that the time is within the configured performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Confirm WPEFramework is running | WPEFramework process must be active and responsive on the device under test. | WPEFramework should be up and running on the device. |
| 2 | Configure device reboot preference | The user should configure `PRE_REQ_REBOOT_PVS` as `Yes` to reboot the device before test execution, or as `No` to skip reboot before test execution. | The device should reboot or skip reboot as configured before test execution begins. |
| 3 | Configure google_bundle in PerformanceTestVariables | `google_bundle` must be set to the application bundle filename in PerformanceTestVariables. | The google_bundle variable should be configured with a valid application bundle name. |
| 4 | Configure app_download_url in PerformanceTestVariables | `app_download_url` must be set to the base URL where the application bundle is hosted in PerformanceTestVariables. | The app_download_url should point to a reachable hosting location. |
| 5 | Configure visible threshold in device config | `APPMANAGER_SET_VISIBLE_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` must be set in the device-specific configuration file. | Threshold and offset values should be correctly configured for performance comparison. |
| 6 | Configure PACKAGEMANAGER_FILE_LOCATOR in device config | `PACKAGEMANAGER_FILE_LOCATOR` must be set to the correct path where downloaded packages are stored on the device. | The file locator path should be correctly configured. |

<a name="head.TestSteps"></a>
## Test Steps

|#|Step Name | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Verify and activate required plugins | Check the activation state of the required plugins: org.rdk.DownloadManager, org.rdk.PackageManagerRDKEMS, org.rdk.AppManager, and org.rdk.RDKWindowManager. Activate any that are not already in the activated state. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.status@<plugin_name>"}` <br><br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "Controller.1.activate", "params": {"callsign": "<plugin_name>"}}` | All four required plugins should be in activated state. |
| 2 | Check if the application is already installed | Query the installed packages list to determine whether the application is already present on the device. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}` | The installed packages list should be returned successfully. |
| 3 | Download the application bundle | If the application is not already installed, download the application bundle from the configured URL via the DownloadManager. This step is skipped if the application was found to be already installed in the previous step. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<app_download_url>/<google_bundle>"}}` | The download should complete successfully and a download ID should be returned. |
| 4 | Install the application | Install the downloaded application bundle without launching it. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.PackageManagerRDKEMS.install", "params": {"packageId": "com.rdkcentral.google", "version": "0.1.0", "additionalMetadata": [{"name": "type", "value": "native/dac-app"}], "fileLocator": "<PACKAGEMANAGER_FILE_LOCATOR>/package<download_id>"}}` | The application should be installed successfully and appear in the installed packages list. |
| 5 | Launch the application | Send a launch request for the installed application via AppManager and wait 10 seconds after launch to allow the app to reach APP_STATE_ACTIVE. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.launchApp", "params": {"appId": "com.rdkcentral.google", "intent": "", "launchArgs": ""}}` | The application should be installed, launched successfully, and reach APP_STATE_ACTIVE. |
| 6 | Retrieve the app instance ID | Query the loaded apps list and extract the appInstanceId for com.rdkcentral.google in APP_STATE_ACTIVE state. This instance ID is required as the client identifier for subsequent RDKWindowManager calls. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.getLoadedApps"}` | The appInstanceId should be retrieved successfully for the active application instance. |
| 7 | Set the application visibility to false | Call org.rdk.RDKWindowManager.setVisible with visible=false for the retrieved appInstanceId to hide the application. Wait 5 seconds to ensure the hidden state is applied before the test measurement begins. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.RDKWindowManager.1.setVisible", "params": {"client": "<appInstanceId>", "visible": false}}` | The setVisible(false) request should be accepted successfully and the application should be hidden. |
| 8 | Subscribe to the onVisible event | Register a WebSocket event listener on the Thunder JSON-RPC endpoint for the onVisible event from org.rdk.RDKWindowManager. Wait 3 seconds after registration to ensure the listener is ready. <br>`{"jsonrpc": "2.0", "id": 9, "method": "org.rdk.RDKWindowManager.1.register", "params": {"event": "onVisible", "id": "client.events.1"}}` | The onVisible event subscription should be established successfully. |
| 9 | Trigger setVisible(true) and record start time | Record the current UTC timestamp as the start time, then call org.rdk.RDKWindowManager.setVisible with visible=true for the retrieved appInstanceId to make the application visible again. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.RDKWindowManager.1.setVisible", "params": {"client": "<appInstanceId>", "visible": true}}` | The setVisible(true) request should be accepted successfully. |
| 10 | Wait for the onVisible event | Monitor the event buffer for up to 120 seconds until the onVisible event containing the appInstanceId is received. Record the event timestamp. | The onVisible event should be received for the application instance within the timeout period. |
| 11 | Calculate visible time and validate against threshold | Compute the elapsed time in milliseconds as the difference between the onVisible event timestamp and the recorded setVisible(true) start time. Compare against `APPMANAGER_SET_VISIBLE_THRESHOLD_VALUE` + `THRESHOLD_OFFSET` from device config. | The time taken to receive the onVisible event should be within the range: 0 < time < (APPMANAGER_SET_VISIBLE_THRESHOLD_VALUE + THRESHOLD_OFFSET) milliseconds. |
| 12 | Terminate the application | Terminate the running application using the AppManager terminateApp API. <br>`{"jsonrpc": "2.0", "id": 1234567890, "method": "org.rdk.AppManager.terminateApp", "params": {"appId": "com.rdkcentral.google"}}` | The application should terminate successfully. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M150<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
