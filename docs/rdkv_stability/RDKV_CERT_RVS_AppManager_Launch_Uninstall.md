## TestCase ID
RDKV_STABILITY_33
## TestCase Name
RDKV_CERT_RVS_AppManager_Launch_Uninstall
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that uninstalling an active application is rejected safely, that the active application record remains consistent, and that the application is automatically removed after it is terminated.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the device connection | Configure the target device IP address and port so that the stability test framework can connect to the device. | The test framework should connect to the target device successfully. |
| 2 | Configure the reboot policy | Configure `PRE_REQ_REBOOT` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot policy should be applied according to the configured value. |
| 3 | Check WPEFramework and device status | Load the `rdkv_stability` module and verify that the device is available before starting the test. | The framework module and device status should report success. |
| 4 | Activate the required application services | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager` are activated. | All required application services should be in the activated state. |
| 5 | Configure the application package | Configure the Google application bundle and a valid application download base URL. The application identifier must be `com.rdkcentral.google`. | The application package should be available for installation and its application identifier should be configured correctly. |
| 6 | Configure the stability iteration count | Configure the application manager stability test count used for repeated uninstall-conflict validation. | A valid positive iteration count should be available for the test. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Activate the required application services | Query the device application service states and activate any service that is not already active: `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager`. | The required application services should be activated successfully. |
| 2 | Subscribe to uninstall events | Register a listener for application uninstall events using: `{"jsonrpc": "2.0","id": 1,"method": "org.rdk.AppManager.1.register","params": {"event": "onAppUninstalled", "id": "client.events.1" }}`. | The uninstall event subscription should be registered successfully. |
| 3 | Install or verify the application | Download and install the configured Google application bundle for `com.rdkcentral.google`, or verify that the application is already installed. | The application should be installed and available for launch. |
| 4 | Launch the application | Submit a launch request for `com.rdkcentral.google`. | The launch request should return success. |
| 5 | Verify the application is active | Query loaded applications using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getLoadedApps","params":{}}`. Confirm that `com.rdkcentral.google` is present and has the `APP_STATE_ACTIVE` lifecycle state. | The application should be present in the loaded-application list with an active lifecycle state. |
| 6 | Attempt to uninstall the active application | Submit an uninstall request for `com.rdkcentral.google` while it remains active. | The uninstall request should fail, and the active application record should remain valid. |
| 7 | Verify the active application remains loaded | After the rejected uninstall request, read the loaded-application list and verify that `com.rdkcentral.google` is still present. | The application should remain present in the loaded-application list after the rejected uninstall attempt. |
| 8 | Terminate the active application | Terminate `com.rdkcentral.google` using its application identifier. | The termination request should return success. |
| 9 | Verify automatic removal after termination | Query installed applications using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getInstalledApps","params":{}}`. | `com.rdkcentral.google` should no longer appear in the installed-application list after termination. |
| 10 | Repeat the uninstall-conflict validation | Repeat application installation or verification, launch, active-state validation, active uninstall attempt, loaded-state validation, termination, and installed-application validation for the configured application manager test count. | Each configured iteration should reject uninstall while the application is active and should remove the application after successful termination. |
| 11 | Complete the test module | Unload the `rdkv_stability` test module after all iterations complete. | The test module should be unloaded cleanly and the final test status should reflect the observed results. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 300 seconds

**Priority** : High

**Release Version** : M153<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
