## TestCase ID
RDKV_STABILITY_46
## TestCase Name
RDKV_CERT_RVS_ResidentApp_SuspendResume
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate ResidentApp stability by continuously suspending and resuming the plugin for suspend_resume_max_count iterations, verifying CPU and memory usage remains within expected limits after each suspend/resume cycle.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|ResidentApp plugin must be in resumed state; DeviceInfo plugin must be activated.|
|3|suspend_resume_max_count must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of ResidentApp and DeviceInfo plugins. Set required states: ResidentApp=resumed, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Get current URL | Retrieve the current URL of ResidentApp via `ResidentApp.1.url` before starting the stress test. | Current URL should be retrieved for reference. |
| 4 | Suspend and resume loop (repeat for suspend_resume_max_count iterations) | For each iteration: <br>Suspend ResidentApp via : `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.suspend","params":{"callsign":"ResidentApp"}}` <br>Verify ResidentApp status is "suspended" via applicable API calls. <br>Resume ResidentApp via : `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"ResidentApp","type":"","uri":""}}` <br>Verify ResidentApp status is "resumed". <br>Validate CPU load and memory usage via applicable API calls. | ResidentApp should suspend and resume successfully in each iteration. CPU load and memory usage should remain within expected limits. |
| 5 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 6 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 7 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the suspend/resume stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 600

**Priority** : High

**Release Version** : M93<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
