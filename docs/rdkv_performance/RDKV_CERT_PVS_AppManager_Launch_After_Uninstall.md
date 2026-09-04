## TestCase ID
RDKV_PERFORMANCE_106
## TestCase Name
RDKV_CERT_PVS_AppManager_Launch_After_Uninstall
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that an application can be installed and then uninstalled successfully, that AppManager rejects a launch request after the application has been removed, and that resource usage remains within the expected limit after the rejected launch attempt.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the pre-execution reboot preference | Configure `PRE_REQ_REBOOT_PVS` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot preference should be configured according to the test environment requirements. |
| 2 | Confirm the required device plugins are activated | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, `org.rdk.AppManager`, and `org.rdk.RDKWindowManager` are activated. Their status can be queried with `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.DownloadManager"}`, `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.AppPackageManager"}`, `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.AppManager"}`, and `{"jsonrpc":"2.0","id":1,"method":"Controller.1.status@org.rdk.RDKWindowManager"}`. | All four plugins should report the `activated` state. |
| 3 | Configure the application bundle | Configure `google_bundle` with the application bundle name and `app_download_url` with a reachable bundle-hosting URL. The application ID should be the portion of the bundle name before the first `+` character. | The bundle URL should be reachable, and its derived application ID should be available for package operations. |
| 4 | Configure package-manager storage | Configure `PACKAGEMANAGER_FILE_LOCATOR` in the applicable device configuration file so the downloaded bundle can be installed. | A valid package file locator should be available. |
| 5 | Configure resource usage limits | Configure the resource thresholds used by the resource usage validation operation. | The expected resource limits should be available for comparison after the launch attempt is rejected. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Load the performance test module | Load the RDKV performance test module and configure the testcase for `RDKV_CERT_PVS_AppManager_Launch_After_Uninstall`. | The performance test module should load successfully. |
| 2 | Activate the required plugins when necessary | If any required plugin is not activated, activate it with the following JSON-RPC request for each affected callsign: `{"jsonrpc":"2.0","id":1,"method":"Controller.1.activate","params":{"callsign":"<plugin>"}}` where `<plugin>` is one of `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, `org.rdk.AppManager`, or `org.rdk.RDKWindowManager`. | Each required plugin should become activated successfully. |
| 3 | Check whether the application is installed | Query the installed package list with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.1.listPackages"}`. If the derived application ID is present, retain the installed application; otherwise continue with download and installation. | The installed-package query should complete successfully, and the application installation state should be determined. |
| 4 | Download the application bundle when required | When the application is not installed, request its download using `org.rdk.DownloadManager.1.download` with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.DownloadManager.1.download","params":{"url":"<app_download_url>/<google_bundle>"}}`. | The application bundle should download successfully and return a package reference. |
| 5 | Install the downloaded application bundle | Use the configured package file locator and returned package reference to install the application with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.install","params":{"packageId":"<app_id>","version":"0.2.0","additionalMetadata":[{"name":"type","value":"native/dac-app"}],"fileLocator":"<PACKAGEMANAGER_FILE_LOCATOR><package_reference>"}}`. | The application should install successfully. |
| 6 | Verify the application installation | Query the installed package list again with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.1.listPackages"}` and confirm that the derived application ID is listed. | The application ID should appear in the installed package list. |
| 7 | Uninstall the application | Uninstall the application using `org.rdk.AppPackageManager.uninstall` with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppPackageManager.uninstall","params":{"packageId":"<app_id>"}}`. | The uninstall request should return success. |
| 8 | Wait for uninstall completion | Wait 5 seconds after the successful uninstall request before attempting to launch the application. | The device should have sufficient time to complete removal of the application package. |
| 9 | Attempt to launch the uninstalled application | Send a launch request using `org.rdk.AppManager.launchApp` with `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.launchApp","params":{"appId":"<app_id>","intent":"","launchArgs":""}}`. | The launch request should be rejected and should not return success because the application was uninstalled. |
| 10 | Validate resource usage after the rejected launch attempt | Execute the resource usage validation operation and inspect its returned details against the configured expected limits. | The resource usage validation should return success and should not report `ERROR`; the resource usage should remain within the expected limit. |
| 11 | Record the negative launch result | Mark the test successful when the launch result is not `SUCCESS`; mark it unsuccessful if the uninstalled application launches successfully. | The final testcase result should be successful only when AppManager prevents launching the removed application. |
| 12 | Unload the performance test module | Unload the RDKV performance test module after completing the installation, uninstall, and launch validation. | The performance test module should unload cleanly. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 5 minutes

**Priority** : High

**Release Version** : M152<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
