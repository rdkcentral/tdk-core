## TestCase ID
RDKV_STABILITY_05
## TestCase Name
RDKV_CERT_RVS_WebKitBrowser_SuspendResume
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate WebKitBrowser stability by continuously suspending and resuming the plugin for suspend_resume_max_count iterations, verifying CPU and memory usage remains within expected limits after each suspend/resume cycle.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin must be in resumed state; Cobalt plugin must be deactivated; DeviceInfo plugin must be activated.|
|3|suspend_resume_max_count must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of WebKitBrowser, Cobalt, and DeviceInfo plugins. Set required states: WebKitBrowser=resumed, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Suspend and resume loop (repeat for suspend_resume_max_count iterations) | For each iteration: <br>Suspend WebKitBrowser via `suspend_plugin`: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.suspend","params":{"callsign":"WebKitBrowser"}}` <br>Verify WebKitBrowser status is "suspended" via `rdkservice_getPluginStatus`. <br>Resume WebKitBrowser via `resume_plugin`: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"WebKitBrowser","type":"","uri":""}}` <br>Verify WebKitBrowser status is "resumed". <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | WebKitBrowser should suspend and resume successfully in each iteration. CPU load and memory usage should remain within expected limits. |
| 4 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 5 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 6 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the suspend/resume stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 420

**Priority** : High

**Release Version** : M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
