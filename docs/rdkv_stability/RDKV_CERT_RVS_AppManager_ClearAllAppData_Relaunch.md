## TestCase ID
RDKV_STABILITY_27
## TestCase Name
RDKV_CERT_RVS_AppManager_ClearAllAppData_Relaunch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that clearing application data for all installed applications does not remove the applications, that each application remains launchable and terminable afterward, and that resource usage remains within the expected limit during repeated execution.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the device connection | Configure the target device IP address and port so that the stability test framework can connect to the device. | The test framework should connect to the target device successfully. |
| 2 | Configure the reboot policy | Configure `PRE_REQ_REBOOT_PVS` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot policy should be applied according to the configured value. |
| 3 | Check WPEFramework and device status | Load the `rdkv_stability` module and verify that the device is available before starting the test. | The framework module and device status should report success. |
| 4 | Activate the required application services | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager` are activated. | All three application services should be in the activated state. |
| 5 | Configure the application bundle set | Configure at least two application bundles in the stability application list. Each bundle must provide an application name and a valid downloadable application package location. | At least two application bundles should be available for installation and testing. |
| 6 | Configure the stability iteration count | Configure the application manager stability test count used for repeated execution. | A valid positive iteration count should be available for the test. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Activate the required application services | Query the device application service states and activate any service that is not already active: `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager`. | The required application services should be activated successfully. |
| 2 | Install the configured applications | For each configured application bundle, check its installation state, download the package when required, install the package, and verify the resulting installation. | Every configured application should be installed successfully. |
| 3 | Record the installed application set | Record the application names obtained from the configured application bundles as the expected installed application set. | The expected application set should contain all configured applications. |
| 4 | Clear data for all applications | Request removal of application data for all applications using the AppManager JSON-RPC method: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.clearAllAppData","params":{}}`. | The clear-all-data request should return success, and application data should be cleared without removing installed applications. |
| 5 | Retrieve the installed application set | Query the installed applications using: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.getInstalledApps","params":{}}`. | The installed application query should return success. |
| 6 | Verify installed applications remain present | Compare the returned installed application set with the recorded application names and identify any missing applications. | No configured application should be missing after application data is cleared. |
| 7 | Launch each installed application | For each configured application, submit the application launch request with the application name as the `app_name` parameter. | Each launch request should return success. |
| 8 | Verify application loading | After each launch, read the device loaded-application list and verify that the launched application is present. | Each application should appear in the loaded-application list after launch. |
| 9 | Terminate each launched application | Terminate the launched application using its application name as the `app_id` parameter. | Each application should terminate successfully. |
| 10 | Validate resource usage | Request resource-usage validation after application termination. | Resource usage should be reported within the expected limit and should not return an error. |
| 11 | Repeat the stability action block | Repeat the clear-all-data, installed-application verification, per-application launch verification, termination, and resource-usage validation actions for the configured application manager test count. | The complete action block should execute for every configured iteration, and any failure should mark the corresponding iteration as unsuccessful. |
| 12 | Complete the test module | Unload the `rdkv_stability` test module after the test flow completes. | The test module should be unloaded cleanly and the final test status should reflect the observed results. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 300 seconds

**Priority** : High

**Release Version** : M153<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
