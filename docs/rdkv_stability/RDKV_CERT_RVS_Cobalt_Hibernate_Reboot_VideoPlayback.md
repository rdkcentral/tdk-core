## TestCase ID
RDKV_STABILITY_69
## TestCase Name
RDKV_CERT_RVS_Cobalt_Hibernate_Reboot_VideoPlayback
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate Cobalt video playback recovery after hibernate and device reboot by launching Cobalt, playing video, hibernating, rebooting the device, and verifying video playback can be re-established after each reboot.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the supported plugins list and must support hibernate functionality.|
|3|cobalt_test_url and reboot_max_count must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt and DeviceInfo plugins. Set required states: Cobalt=resumed, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Hibernate-Reboot-Playback loop (repeat for reboot_max_count iterations) | For each iteration: <br>Launch Cobalt via `launch_plugin`. <br>Set video URL via deeplink: `{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":{"url":"<cobalt_test_url>"}}` <br>Validate video is playing via `rdkservice_validateProcEntry`. <br>Hibernate Cobalt via `org.rdk.RDKShell.1.suspend`. <br>Reboot device via `org.rdk.System.1.reboot`. <br>Wait for device to come back online and WPEFramework to restart. <br>Re-apply plugin preconditions. <br>Re-launch Cobalt and set video URL. <br>Validate video is playing via `rdkservice_validateProcEntry`. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | Device should reboot successfully. Cobalt should re-launch and play video after each reboot. CPU load and memory usage should remain within expected limits. |
| 4 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 5 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 6 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the hibernate-reboot stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 540

**Priority** : High

**Release Version** : M129<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
