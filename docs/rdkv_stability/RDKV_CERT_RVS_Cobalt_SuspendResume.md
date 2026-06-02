## TestCase ID
RDKV_STABILITY_07
## TestCase Name
RDKV_CERT_RVS_Cobalt_SuspendResume
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by continuously suspending and resuming the Cobalt plugin for suspend_resume_max_count iterations, verifying CPU and memory usage remains within expected limits after each suspend/resume cycle.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be in resumed state; WebKitBrowser must be deactivated; DeviceInfo must be activated.|
|3|SUPPORTED_PLUGINS in device config must include Cobalt and DeviceInfo.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins via `rdkservice_getPluginStatus`. Set required states: Cobalt=resumed, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Suspend and resume loop (repeat for suspend_resume_max_count iterations) | For each iteration: <br>Suspend Cobalt using `org.rdk.RDKShell.1.suspend` via `suspend_plugin`: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.suspend","params":{"callsign":"Cobalt"}}` <br>Get Cobalt plugin status via `rdkservice_getPluginStatus` and verify status is "suspended". <br>Resume Cobalt using `org.rdk.RDKShell.1.launch` via `resume_plugin`: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` <br>Get Cobalt plugin status and verify status is "resumed". <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage` using DeviceInfo.1.systeminfo. | Cobalt should suspend and resume successfully in each iteration. CPU load and memory usage should remain within expected limits. |
| 4 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 5 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 6 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 420

**Priority** : High

**Release Version** : M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
