## TestCase ID
RDKV_PERFORMANCE_109
## TestCase Name
RDKV_CERT_PVS_AppManager_TimeTo_Preload_App
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that an installed application can be preloaded successfully and that the elapsed time from the preload request to the paused lifecycle event remains within the configured threshold and offset.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the pre-execution reboot preference | Configure `PRE_REQ_REBOOT_PVS` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot preference should be configured according to the test environment requirements. |
| 2 | Confirm the required device plugins are activated | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager` are activated. Their status can be queried with `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.DownloadManager"}`, `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.AppPackageManager"}`, and `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.AppManager"}`. | All three required plugins should report the `activated` state. |
| 3 | Configure the application bundle | Configure `google_bundle` with the application bundle name and `app_download_url` with a reachable bundle-hosting URL. The application ID should be the portion of the bundle name before the first `+` character. | The bundle URL should be reachable, and its derived application ID should be available for application operations. |
| 4 | Configure preload timing thresholds | Configure `APPMANAGER_LAUNCH_THRESHOLD_VALUE` and `THRESHOLD_OFFSET` in the applicable device configuration file. | Both threshold values should be available as numeric millisecond values for the elapsed-time comparison. |
| 5 | Configure package-manager storage | Configure `PACKAGEMANAGER_FILE_LOCATOR` so a downloaded bundle can be installed when the application is not already present. | A valid package file locator should be available. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Load the performance test module | Load the RDKV performance test module and configure the testcase for `RDKV_CERT_PVS_AppManager_TimeTo_Preload_App`. | The performance test module should load successfully. |
| 2 | Activate the required plugins when necessary | If any required plugin is not activated, activate it with the following JSON-RPC request for each affected callsign: `{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"<plugin>"}}` where `<plugin>` is one of `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, or `org.rdk.AppManager`. | Each required plugin should become activated successfully. |
| 3 | Check whether the application is installed | Query the installed package list with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.1.listPackages"}`. If the derived application ID is present, retain the application; otherwise continue with download and installation. | The installed-package query should complete successfully, and the application installation state should be determined. |
| 4 | Download the application bundle when required | When the application is not installed, request its download using `org.rdk.DownloadManager.1.download` with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<app_download_url>/<google_bundle>"}}`. | The application bundle should download successfully and return a package reference. |
| 5 | Install the application bundle when required | Install the downloaded bundle using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.install","params":{"packageId":"<app_id>","version":"0.2.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<PACKAGEMANAGER_FILE_LOCATOR><package_reference>"}}`. | The application should install successfully. |
| 6 | Verify the application installation | Query the installed package list again with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.1.listPackages"}` and confirm that the application ID is listed. | The application ID should appear in the installed package list. |
| 7 | Subscribe to application lifecycle events | Register for lifecycle state notifications at `/jsonrpc` using `{"jsonrpc": "2.0","id": 9,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppLifecycleStateChanged", "id": "client.events.1" }}` and wait 5 seconds for registration readiness. | The lifecycle event subscription should be established successfully. |
| 8 | Start the application preload and record the start time | Record the current UTC time immediately before sending `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.preloadApp","params":{"appId":"<app_id>"}}`. | The preload request should return success, and a precise preload start timestamp should be recorded. |
| 9 | Poll for the preload lifecycle event | Poll the event buffer for up to 120 seconds, selecting an event for the target application that contains `onAppLifecycleStateChanged` and `APP_STATE_PAUSED`. | A matching paused lifecycle event should be received within the polling period. |
| 10 | Record the preload completion time | Extract the event timestamp from the received lifecycle event and record it as the preload completion time. | The preload completion timestamp should be parsed successfully from the received event. |
| 11 | Calculate the preload duration | Calculate the elapsed time in milliseconds between the recorded preload start and completion timestamps using `completion_time - start_time`. | The calculated preload duration should be a positive value in milliseconds. |
| 12 | Validate the preload duration against the configured threshold | Compare the calculated duration with `APPMANAGER_LAUNCH_THRESHOLD_VALUE + THRESHOLD_OFFSET` and require `0 < duration < threshold + offset`. | The preload duration should be within the configured expected range. |
| 13 | Terminate the preloaded application | Terminate the application using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_id>"}}`. | The application should terminate successfully. |
| 14 | Close the lifecycle event subscription | Disconnect from the application lifecycle event stream after the timing and termination checks are complete. | The event subscription should close cleanly. |
| 15 | Unload the performance test module | Unload the RDKV performance test module after completing the preload timing validation. | The performance test module should unload cleanly. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5 minutes

**Priority** : High

**Release Version** : M152<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
