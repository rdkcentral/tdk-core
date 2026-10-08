## TestCase ID
RDKV_STABILITY_32
## TestCase Name
RDKV_CERT_RVS_AppManager_Preload_Launch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the application can be preloaded into the paused lifecycle state, activated through launch, terminated without leaving an orphaned instance, and maintained within the expected resource usage limit during repeated execution.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the device connection | Configure the target device IP address and port so that the stability test framework can connect to the device. | The test framework should connect to the target device successfully. |
| 2 | Configure the reboot policy | Configure `PRE_REQ_REBOOT_PVS` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot policy should be applied according to the configured value. |
| 3 | Check WPEFramework and device status | Load the `rdkv_stability` module and verify that the device is available before starting the test. | The framework module and device status should report success. |
| 4 | Activate the required application services | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, `org.rdk.AppManager`, and `org.rdk.RDKWindowManager` are activated. | All required application services should be in the activated state. |
| 5 | Configure the application package | Configure the Google application bundle and a valid application download base URL. The application identifier must be `com.rdkcentral.google`. | The application package should be available for installation and its application identifier should be configured correctly. |
| 6 | Configure the stability iteration count | Configure the application manager stability test count used for repeated preload and lifecycle validation. | A valid positive iteration count should be available for the test. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Activate the required application services | Query the device application service states and activate any service that is not already active: `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, `org.rdk.AppManager`, and `org.rdk.RDKWindowManager`. | The required application services should be activated successfully. |
| 2 | Install the application under test | Download and install the configured Google application bundle for application `com.rdkcentral.google` without launching it. | The application should be installed successfully before preload validation begins. |
| 3 | Preload the application | Request application preload using the AppManager JSON-RPC method: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.preloadApp","params":{"appId":"com.rdkcentral.google"}}`. | The preload request should return success. |
| 4 | Verify the preloaded lifecycle state | Query loaded applications using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getLoadedApps","params":{}}`. Confirm that the entry for `com.rdkcentral.google` has both `lifecycleState` and `targetLifecycleState` set to `APP_STATE_PAUSED`. | The application should be present with `APP_STATE_PAUSED` as both its current and target lifecycle state. |
| 5 | Launch the preloaded application | Submit a launch request for `com.rdkcentral.google` to activate the preloaded application. | The launch request should return success. |
| 6 | Verify the active lifecycle state | Query loaded applications again using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getLoadedApps","params":{}}`. Confirm that the application entry has `lifecycleState` set to `APP_STATE_ACTIVE`. | The application should transition to and remain in the `APP_STATE_ACTIVE` lifecycle state. |
| 7 | Terminate the application | Terminate `com.rdkcentral.google` using its application identifier. | The termination request should return success. |
| 8 | Verify that no orphaned instance remains | Read the loaded-application list after termination and verify that `com.rdkcentral.google` is absent. | The application should not appear in the loaded-application list, and no orphaned instance should remain. |
| 9 | Validate resource usage | Request resource-usage validation after the application is terminated. | Resource usage should be reported within the expected limit and should not return an error. |
| 10 | Repeat the preload and lifecycle validation | Repeat the preload request, paused-state verification, launch request, active-state verification, termination, orphan check, and resource-usage validation for the configured application manager test count. | The complete lifecycle block should execute for every configured iteration, and any failed state, termination, orphan, or resource check should mark the corresponding iteration unsuccessful. |
| 11 | Complete the test module | Unload the `rdkv_stability` test module after all iterations complete. | The test module should be unloaded cleanly and the final test status should reflect the observed results. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 300 seconds

**Priority** : High

**Release Version** : M153<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
