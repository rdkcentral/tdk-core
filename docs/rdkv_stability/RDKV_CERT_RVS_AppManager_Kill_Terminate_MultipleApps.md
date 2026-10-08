## TestCase ID
RDKV_STABILITY_31
## TestCase Name
RDKV_CERT_RVS_AppManager_Kill_Terminate_MultipleApps
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the launch, kill, relaunch, and terminate lifecycle of two distinct applications and confirm the expected loaded-application state after every lifecycle action during repeated execution.

<a name="head.Precondition"></a>
## Preconditions
|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Configure the device connection | Configure the target device IP address and port so that the stability test framework can connect to the device. | The test framework should connect to the target device successfully. |
| 2 | Configure the reboot policy | Configure `PRE_REQ_REBOOT_PVS` as Yes to reboot the device before test execution, or as No to skip the reboot. | The device reboot policy should be applied according to the configured value. |
| 3 | Check WPEFramework and device status | Load the `rdkv_stability` module and verify that the device is available before starting the test. | The framework module and device status should report success. |
| 4 | Activate the required application services | Ensure that `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager` are activated. | All required application services should be in the activated state. |
| 5 | Configure two distinct application bundles | Configure at least two application bundles in the stability application list. Each bundle must resolve to a distinct application identifier and be available from the application download URL. | At least two distinct application bundles should be available for installation. |
| 6 | Configure the stability iteration count | Configure the application manager stability test count used for repeated lifecycle cycles. | A valid positive iteration count should be available for the test. |

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Activate the required application services | Query the device application service states and activate any service that is not already active: `org.rdk.DownloadManager`, `org.rdk.AppPackageManager`, and `org.rdk.AppManager`. | The required application services should be activated successfully. |
| 2 | Install the first application | Download and install the first configured application bundle without launching it. | The first application should be installed successfully. |
| 3 | Install the second application | Download and install the second configured application bundle without launching it. | The second application should be installed successfully, and its identifier should be distinct from the first application identifier. |
| 4 | Launch the first application | Submit a launch request for the first configured application. | The launch request should return success, and the first application should be present in the loaded-application list with an active state. |
| 5 | Launch the second application | Submit a launch request for the second configured application. | The launch request should return success, and the second application should be present in the loaded-application list with an active state. |
| 6 | Kill the first application | Kill the first application using the AppManager JSON-RPC method: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.killApp","params":{"appId":"<app_id_1>"}}`. | The kill request should return success, and the first application should be absent from the loaded-application list. |
| 7 | Kill the second application | Kill the second application using the AppManager JSON-RPC method: `{"jsonrpc":"2.0","id":1,"method":"org.rdk.AppManager.killApp","params":{"appId":"<app_id_2>"}}`. | The kill request should return success, and the second application should be absent from the loaded-application list. |
| 8 | Relaunch the first application | Submit a launch request for the first configured application a second time. | The launch request should return success, and the first application should be present in the loaded-application list with an active state. |
| 9 | Relaunch the second application | Submit a launch request for the second configured application a second time. | The launch request should return success, and the second application should be present in the loaded-application list with an active state. |
| 10 | Terminate the first application | Terminate the first application using its application identifier. | The termination request should return success, and the first application should be absent from the loaded-application list. |
| 11 | Terminate the second application | Terminate the second application using its application identifier. | The termination request should return success, and the second application should be absent from the loaded-application list. |
| 12 | Repeat the multi-application lifecycle sequence | Repeat the launch, launch, kill, kill, launch, launch, terminate, and terminate actions, including loaded-application state validation after each action, for the configured application manager test count. | Every configured cycle should preserve the expected active or absent state for both applications, and any failed lifecycle request or state check should mark the cycle unsuccessful. |
| 13 | Complete the test module | Unload the `rdkv_stability` test module after all lifecycle cycles complete. | The test module should be unloaded cleanly and the final test status should reflect the observed results. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 300 seconds

**Priority** : High

**Release Version** : M153<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
