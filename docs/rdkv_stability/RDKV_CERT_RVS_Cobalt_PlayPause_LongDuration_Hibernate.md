## TestCase ID
RDKV_STABILITY_90
## TestCase Name
RDKV_CERT_RVS_Cobalt_PlayPause_LongDuration_Hibernate
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate Cobalt video playback after an extended long-duration hibernate period by hibernating Cobalt, waiting for a configured duration, restoring it, and verifying that video playback can be re-established and resources remain within limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the supported plugins list and must support hibernate functionality.|
|3|hibernate_wait_duration and cobalt_test_url must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt and DeviceInfo plugins. Set required states: Cobalt=resumed, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt | Launch Cobalt via using `org.rdk.RDKShell.1.launch`. | Cobalt should launch successfully. |
| 4 | Hibernate Cobalt for long duration | Hibernate Cobalt via `org.rdk.RDKShell.1.suspend`. Verify Cobalt is in suspended/hibernated state. Wait for hibernate_wait_duration seconds. | Cobalt should enter and remain in hibernated state for the configured duration. |
| 5 | Restore Cobalt from long-duration hibernate | Restore Cobalt from hibernate via `org.rdk.RDKShell.1.restoreApp`. Verify Cobalt is resumed. | Cobalt should restore successfully after the long-duration hibernation. |
| 6 | Set video URL and validate playback | Set video URL via deeplink: `{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":{"url":"<cobalt_test_url>"}}` Validate video is playing via applicable API calls. | Video should play successfully after restoring from long-duration hibernate. |
| 7 | Validate resource usage | Validate CPU load and memory usage via applicable API calls. | CPU load and memory usage should be within expected limits. |
| 8 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with measurement data. |
| 9 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 10 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the long-duration hibernate test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 120

**Priority** : High

**Release Version** : M129<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
