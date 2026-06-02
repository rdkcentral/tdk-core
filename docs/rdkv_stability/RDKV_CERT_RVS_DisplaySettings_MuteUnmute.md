## TestCase ID
RDKV_STABILITY_59
## TestCase Name
RDKV_CERT_RVS_DisplaySettings_MuteUnmute
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by repeatedly muting and unmuting audio on connected audio ports for mute_unmute_max_count iterations, verifying each mute/unmute operation is applied correctly and CPU/memory usage remains within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|org.rdk.DisplaySettings and DeviceInfo plugins must be available in the supported plugins list.|
|3|The device must have at least one connected audio port accessible via `getConnectedAudioPorts`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of org.rdk.DisplaySettings and DeviceInfo plugins. Set required states: org.rdk.DisplaySettings=activated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Get connected audio ports | Retrieve the list of connected audio ports via `org.rdk.DisplaySettings.1.getConnectedAudioPorts`. Select the first available audio port for testing. | Connected audio ports should be retrieved successfully. |
| 4 | Mute and unmute loop (repeat for mute_unmute_max_count iterations) | For each iteration: <br>Mute the audio port: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.DisplaySettings.1.setMuted","params":{"audioPort":"<port>","muted":true}}` <br>Get mute status and verify it is `true`: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.DisplaySettings.1.getMuted","params":{"audioPort":"<port>"}}` <br>Unmute the audio port: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.DisplaySettings.1.setMuted","params":{"audioPort":"<port>","muted":false}}` <br>Get mute status and verify it is `false`. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | Mute and unmute operations should succeed. Muted status should match the set value. CPU load and memory usage should remain within expected limits. |
| 5 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 6 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 7 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the mute/unmute stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-HYB, RPI-Client, Video_Accelerator

**Estimated duration** : 600

**Priority** : High

**Release Version** : M95<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
