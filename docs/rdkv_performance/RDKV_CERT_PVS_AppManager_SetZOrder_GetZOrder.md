## TestCase ID
RDKV_PERFORMANCE_108
## TestCase Name
RDKV_CERT_PVS_AppManager_SetZOrder_GetZOrder
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the z-order of an active application can be set through RDKWindowManager, that the returned z-order matches the requested value, and that resource usage remains within the expected limit after setting and getting the z-order.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the pre-execution reboot preference | Configure `PRE_REQ_REBOOT_PVS` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot preference should be configured according to the test environment requirements. |
| 2 | Confirm the required device plugins are activated | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, `org.rdk.AppManager`, and `org.rdk.RDKWindowManager` are activated. Their status can be queried with `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.DownloadManager"}`, `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.AppPackageManager"}`, `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.AppManager"}`, and `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.RDKWindowManager"}`. | All four required plugins should report the `activated` state. |
| 3 | Configure the application bundle | Configure `google_bundle` with the application bundle name and `app_download_url` with a reachable bundle-hosting URL. The application ID should be the portion of the bundle name before the first `+` character. | The bundle URL should be reachable, and its derived application ID should be available for application operations. |
| 4 | Configure the requested z-order | Configure `requested_zorder` with the integer z-order value to assign to the active application. | A valid integer z-order value should be available for the set and get comparison. |
| 5 | Configure package-manager storage | Configure `PACKAGEMANAGER_FILE_LOCATOR` in the applicable device configuration file so a downloaded bundle can be installed. | A valid package file locator should be available. |
| 6 | Configure resource usage limits | Configure the resource thresholds used by the resource usage validation operation. | The expected resource limits should be available for comparison after setting and getting the z-order. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Load the performance test module | Load the RDKV performance test module and configure the testcase for `RDKV_CERT_PVS_AppManager_SetZOrder_GetZOrder`. | The performance test module should load successfully. |
| 2 | Activate the required plugins when necessary | If any required plugin is not activated, activate it with the following JSON-RPC request for each affected callsign: `{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"<plugin>"}}` where `<plugin>` is one of `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, `org.rdk.AppManager`, or `org.rdk.RDKWindowManager`. | Each required plugin should become activated successfully. |
| 3 | Check whether the application is installed | Query the installed package list with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.1.listPackages"}`. If the derived application ID is present, retain the application; otherwise download and install it. | The installed-package query should complete successfully, and the application installation state should be determined. |
| 4 | Download the application bundle when required | When the application is not installed, request its download using `org.rdk.DownloadManager.1.download` with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<app_download_url>/<google_bundle>"}}`. | The application bundle should download successfully and return a package reference. |
| 5 | Install the application bundle when required | Install the downloaded bundle using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.install","params":{"packageId":"<app_id>","version":"0.2.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<PACKAGEMANAGER_FILE_LOCATOR><package_reference>"}}`. | The application should install successfully. |
| 6 | Verify the application installation | Query the installed package list with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.1.listPackages"}` and confirm that the application ID is listed. | The application ID should appear in the installed package list. |
| 7 | Launch the application | Launch the application using `org.rdk.AppManager.launchApp` with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_id>","intent":"","launchArgs":""}}`. | The application should launch successfully. |
| 8 | Retrieve the active application instance ID | Wait 5 seconds, then query loaded applications using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getLoadedApps"}`. Select the entry whose `appId` is the target application and whose `lifecycleState` is `APP_STATE_ACTIVE`, and obtain its `appInstanceId`. | An active application entry should be returned with a non-empty application instance ID. |
| 9 | Set the application z-order | Set the requested z-order using `org.rdk.RDKWindowManager.setZOrder` with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.RDKWindowManager.setZOrder","params":{"clientId":"<app_instance_id>","zOrder":<requested_zorder>}}`. | The z-order request should return success. |
| 10 | Read back the application z-order | Query the assigned z-order using `org.rdk.RDKWindowManager.getZOrder` with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.RDKWindowManager.getZOrder","params":{"clientId":"<app_instance_id>"}}`. | The get-z-order request should return success and a numeric z-order value. |
| 11 | Compare the requested and returned z-order | Compare the value returned by `getZOrder` with `requested_zorder`. | The returned z-order should exactly match the requested z-order. |
| 12 | Validate resource usage after setting and getting the z-order | Execute the resource usage validation operation and inspect its returned details against the configured expected limits. | The resource usage validation should return success and should not report `ERROR`; the resource usage should remain within the expected limit. |
| 13 | Terminate the application | Terminate the application using `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.1.terminateApp","params":{"appId":"<app_id>"}}`. | The application should terminate successfully. |
| 14 | Unload the performance test module | Unload the RDKV performance test module after completing the z-order validation. | The performance test module should unload cleanly. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 5 minutes

**Priority** : High

**Release Version** : M152<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
