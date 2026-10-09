## TestCase ID
RDKV_STABILITY_30
## TestCase Name
RDKV_CERT_RVS_AppManager_ClearAppData_Launch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the configured application can be launched, have its application data cleared while running, be terminated successfully, and leave resource usage within the expected limit during repeated execution.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the device connection | Configure the target device IP address and port so that the stability test framework can connect to the device. | The test framework should connect to the target device successfully. |
| 2 | Configure the reboot policy | Configure `PRE_REQ_REBOOT` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot policy should be applied according to the configured value. |
| 3 | Check WPEFramework and device status | Load the `rdkv_stability` module and verify that the device is available before starting the test. | The framework module and device status should report success. |
| 4 | Activate the required application services | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager` are activated. | All required application services should be in the activated state. |
| 5 | Configure the application package | Configure the Google application bundle and a valid application download base URL. The application identifier must be `com.rdkcentral.google`. | The application package should be available for installation and its application identifier should be configured correctly. |
| 6 | Configure the stability iteration count | Configure the application manager stability test count used for repeated execution. | A valid positive iteration count should be available for the test. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Activate the required application services | Query the device application service states and activate any service that is not already active: `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager`. | The required application services should be activated successfully. |
| 2 | Install the application under test | Download and install the configured Google application bundle for application `com.rdkcentral.google`, and verify that installation succeeds. | The application should be installed successfully before lifecycle validation begins. |
| 3 | Launch the application | Submit an application launch request using `com.rdkcentral.google` as the application name. | The launch request should return success. |
| 4 | Verify application loading | After the launch request, read the loaded-application list and verify that `com.rdkcentral.google` is present. | The application should appear in the loaded-application list. |
| 5 | Clear application data | Clear data for the running application using the AppManager JSON-RPC method: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.clearAppData","params":{"appId":"com.rdkcentral.google"}}`. | The clear-data request should return success and the application data should be cleared. |
| 6 | Terminate the application | Terminate `com.rdkcentral.google` using its application identifier. | The application termination request should return success. |
| 7 | Verify application termination | After termination, read the loaded-application list and verify that `com.rdkcentral.google` is no longer present. | The application should not appear in the loaded-application list after termination. |
| 8 | Validate resource usage | Request resource-usage validation after the application is terminated. | Resource usage should be reported within the expected limit and should not return an error. |
| 9 | Repeat the application lifecycle validation | Repeat the launch, loaded-state verification, app-data clearing, termination, termination verification, and resource-usage validation actions for the configured application manager test count. | The complete lifecycle block should execute for every configured iteration, and any failed lifecycle or resource check should mark the corresponding iteration unsuccessful. |
| 10 | Complete the test module | Unload the `rdkv_stability` test module after the lifecycle iterations complete. | The test module should be unloaded cleanly and the final test status should reflect the observed results. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 300 seconds

**Priority** : High

**Release Version** : M153<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
