## TestCase ID
RDKV_STABILITY_71
## TestCase Name
RDKV_CERT_RVS_Cobalt_LongDuration_Hibernate
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate Cobalt hibernate persistence over a long duration by placing Cobalt in hibernate state, waiting for a configured period, and then restoring it to verify that Cobalt can successfully resume operation.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the supported plugins list and must support hibernate functionality.|
|3|hibernate_wait_duration must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=resumed, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt | Launch Cobalt via `launch_plugin` using `org.rdk.RDKShell.1.launch`. | Cobalt should launch successfully. |
| 4 | Hibernate Cobalt | Hibernate Cobalt via `org.rdk.RDKShell.1.suspend`. Verify Cobalt status is "suspended" (hibernated). | Cobalt should enter hibernated state successfully. |
| 5 | Wait for long duration | Wait for hibernate_wait_duration seconds (configured long-duration period). | Device should remain stable with Cobalt in hibernated state throughout the wait period. |
| 6 | Restore Cobalt from long-duration hibernate | Restore Cobalt from hibernate via `org.rdk.RDKShell.1.restoreApp`. Resume Cobalt via `org.rdk.RDKShell.1.launch`. Verify Cobalt status is "resumed". | Cobalt should restore successfully after the long hibernate duration. Status should be "resumed". |
| 7 | Validate resource usage | Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | CPU load and memory usage should be within expected limits after long-duration hibernate. |
| 8 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with measurement data. |
| 9 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 10 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the long-duration hibernate test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 120

**Priority** : High

**Release Version** : M129<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
