## TestCase ID
RDKV_STABILITY_39
## TestCase Name
RDKV_CERT_RVS_LightningApp_LifeCycleManagement
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate LightningApp plugin stability by executing a complete lifecycle management sequence (launch, set URL, suspend, resume, moveToBack, moveToFront, destroy) for lifecycle_max_count iterations, verifying CPU and memory usage remains within expected limits throughout.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|LightningApp plugin must be available in the supported plugins list.|
|3|ip_change_app_url and lifecycle_max_count must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of LightningApp, Cobalt, and DeviceInfo plugins. Set required states: LightningApp=deactivated, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Lifecycle management loop (repeat for lifecycle_max_count iterations) | For each iteration, execute lifecycle operations for LightningApp: <br>Launch LightningApp via `org.rdk.RDKShell.1.launch`. <br>Set app URL: `{"jsonrpc":"2.0","id":1234567890,"method":"LightningApp.1.url","params":{"value":"<ip_change_app_url>"}}` <br>Verify URL is set correctly. <br>Suspend LightningApp via `org.rdk.RDKShell.1.suspend` and verify status is "suspended". <br>Resume LightningApp via `org.rdk.RDKShell.1.launch` and verify status is "resumed". <br>Move LightningApp to back via `org.rdk.RDKShell.1.moveToBack`. <br>Move LightningApp to front via `org.rdk.RDKShell.1.moveToFront`. <br>Destroy LightningApp via `org.rdk.RDKShell.1.destroy`. <br>Validate CPU load and memory usage via applicable API calls. | All lifecycle transitions should succeed. URL should be set and verified correctly. CPU load and memory usage should remain within expected limits. |
| 4 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 5 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 6 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the lifecycle stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 1500

**Priority** : High

**Release Version** : M90<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
