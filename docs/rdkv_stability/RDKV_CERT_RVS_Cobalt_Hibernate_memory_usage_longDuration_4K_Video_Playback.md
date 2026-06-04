## TestCase ID
RDKV_STABILITY_74
## TestCase Name
RDKV_CERT_RVS_Cobalt_Hibernate_memory_usage_longDuration_4K_Video_Playback
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate memory usage during Cobalt 4K video playback and hibernate state by measuring memory before playback, during playback, after hibernate, and after restore, ensuring memory is properly managed throughout the lifecycle.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the supported plugins list and must support hibernate functionality.|
|3|cobalt_4k_url (4K video stream) and hibernate_wait_duration must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt and DeviceInfo plugins. Set required states: Cobalt=resumed, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt and set 4K video URL | Launch Cobalt via applicable API calls. Set 4K video URL via deeplink: `{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":{"url":"<cobalt_4k_url>"}}` | Cobalt should launch and start loading the 4K video. |
| 4 | Validate 4K video playback | Verify 4K video is playing via applicable API calls. | Video decoder proc entry should be present, indicating 4K video is playing. |
| 5 | Measure memory during playback | Record memory usage of Cobalt process via DeviceInfo.1.systeminfo. | Memory usage during 4K playback should be within configured acceptable limits. |
| 6 | Hibernate Cobalt | Hibernate Cobalt via `org.rdk.RDKShell.1.suspend`. Verify Cobalt is suspended. Record memory usage during hibernate. | Cobalt should enter hibernated state. Memory usage should decrease after hibernation. |
| 7 | Restore Cobalt from hibernate | Restore Cobalt from hibernate via `org.rdk.RDKShell.1.restoreApp`. Resume Cobalt via `org.rdk.RDKShell.1.launch`. Verify Cobalt is resumed and video playback resumes. | Cobalt should restore successfully. Video should resume playing. |
| 8 | Validate resource usage after restore | Validate CPU load and memory usage via applicable API calls. | CPU load and memory usage should be within expected limits after restore. |
| 9 | Save CPU/memory data | Save the collected memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all measurement data. |
| 10 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 11 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the 4K hibernate memory test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : Video_Accelerator

**Estimated duration** : 740

**Priority** : High

**Release Version** : M130<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
