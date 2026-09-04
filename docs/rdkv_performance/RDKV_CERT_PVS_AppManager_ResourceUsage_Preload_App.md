## TestCase ID
RDKV_PERFORMANCE_107
## TestCase Name
RDKV_CERT_PVS_AppManager_ResourceUsage_Preload_App
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that an installed application can be preloaded through AppManager and that its resource usage remains within the configured expected limits before the application is terminated.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the pre-execution reboot preference | Configure `PRE_REQ_REBOOT_PVS` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot preference should be configured according to the test environment requirements. |
| 2 | Confirm the required device plugins are activated | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager` are activated. Their status can be queried with `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.DownloadManager"}`, `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.AppPackageManager"}`, and `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.AppManager"}`. | All three required plugins should report the `activated` state. |
| 3 | Configure the application bundle | Configure `google_bundle` with the application bundle name and `app_download_url` with a reachable bundle-hosting URL. The application ID should be the portion of the bundle name before the first `+` character. | The bundle URL should be reachable, and its derived application ID should be available for application operations. |
| 4 | Configure package-manager storage | Configure `PACKAGEMANAGER_FILE_LOCATOR` in the applicable device configuration file so a downloaded bundle can be installed. | A valid package file locator should be available. |
| 5 | Configure resource usage limits | Configure the resource thresholds used by the resource usage validation operation. | The expected resource limits should be available for comparison after preloading. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Load the performance test module | Load the RDKV performance test module and configure the testcase for `RDKV_CERT_PVS_AppManager_ResourceUsage_Preload_App`. | The performance test module should load successfully. |
| 2 | Activate the required plugins when necessary | If any required plugin is not activated, activate it with the following JSON-RPC request for each affected callsign: `{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"<plugin>"}}` where `<plugin>` is one of `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, or `org.rdk.AppManager`. | Each required plugin should become activated successfully. |
| 3 | Check whether the application is installed | Query the installed package list with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.1.listPackages"}`. If the derived application ID is present, retain the installed application; otherwise continue with download and installation. | The installed-package query should complete successfully, and the application installation state should be determined. |
| 4 | Download the application bundle when required | When the application is not installed, request its download using `org.rdk.DownloadManager.1.download` with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<app_download_url>/<google_bundle>"}}`. | The application bundle should download successfully and return a package reference. |
| 5 | Install the downloaded application bundle | Use the configured package file locator and returned package reference to install the application with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.install","params":{"packageId":"<app_id>","version":"0.2.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<PACKAGEMANAGER_FILE_LOCATOR><package_reference>"}}`. | The application should install successfully. |
| 6 | Verify the application installation | Query the installed package list again with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.1.listPackages"}` and confirm that the derived application ID is listed. | The application ID should appear in the installed package list. |
| 7 | Preload the installed application | Preload the application with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.preloadApp","params":{"appId":"<app_id>"}}`. | The preload request should return success. |
| 8 | Validate application resource usage | Execute the resource usage validation operation and inspect its returned details against the configured expected limits. | The resource usage validation should return success and should not report `ERROR`; the application resource usage should remain within the expected limit. |
| 9 | Terminate the preloaded application | Terminate the application using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_id>"}}`. | The application should terminate successfully. |
| 10 | Unload the performance test module | Unload the RDKV performance test module after resource validation and application termination. | The performance test module should unload cleanly. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 5 minutes

**Priority** : High

**Release Version** : M152<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
