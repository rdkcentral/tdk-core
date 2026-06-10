## TestCase ID
RDKV_STABILITY_84
## TestCase Name
RDKV_CERT_RVS_Cobalt_Hibernate_Resume
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate Cobalt hibernate and resume stability by repeatedly hibernating and restoring the Cobalt plugin for hibernate_resume_max_count iterations, verifying CPU and memory usage remains within expected limits throughout.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the supported plugins list and must support hibernate/suspend functionality.|
|3|hibernate_resume_max_count must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=resumed, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt | Launch Cobalt via using `org.rdk.RDKShell.1.launch`. | Cobalt should launch successfully. |
| 4 | Hibernate and resume loop (repeat for hibernate_resume_max_count iterations) | For each iteration: <br>Hibernate Cobalt via `org.rdk.RDKShell.1.suspend` with hibernation parameter: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.suspend","params":{"callsign":"Cobalt"}}` <br>Restore Cobalt via `org.rdk.RDKShell.1.restoreApp`: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.restoreApp","params":{"client":"Cobalt"}}` <br>Resume Cobalt via `org.rdk.RDKShell.1.launch`. <br>Verify Cobalt status is "resumed" via applicable API calls. <br>Validate CPU load and memory usage via applicable API calls. | Cobalt should hibernate and restore successfully in each iteration. Status after restore and resume should be "resumed". CPU load and memory usage should remain within expected limits. |
| 5 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 6 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 7 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the hibernate stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 420

**Priority** : High

**Release Version** : M129<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
