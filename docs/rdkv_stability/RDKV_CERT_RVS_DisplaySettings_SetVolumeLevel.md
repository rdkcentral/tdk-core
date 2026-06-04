## TestCase ID
RDKV_STABILITY_61
## TestCase Name
RDKV_CERT_RVS_DisplaySettings_SetVolumeLevel
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by repeatedly setting random volume levels on connected audio ports for set_volumelevel_max_count iterations, verifying each volume level is applied correctly and CPU/memory usage remains within expected limits.

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
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of org.rdk.DisplaySettings and DeviceInfo plugins. Set required states: org.rdk.DisplaySettings=activated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Get connected audio ports and initial volume | Retrieve connected audio ports via `org.rdk.DisplaySettings.1.getConnectedAudioPorts`. Get current volume level and save as initial value: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.DisplaySettings.1.getVolumeLevel","params":{"audioPort":"<port>"}}` | Connected audio ports and initial volume level should be retrieved successfully. |
| 4 | Set volume level loop (repeat for set_volumelevel_max_count iterations) | For each iteration: <br>Generate a random volume level between 0 and 100. <br>Set the volume level: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.DisplaySettings.1.setVolumeLevel","params":{"audioPort":"<port>","volumeLevel":<random_value>}}` <br>Get the volume level and verify it matches the set value: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.DisplaySettings.1.getVolumeLevel","params":{"audioPort":"<port>"}}` <br>Validate CPU load and memory usage via applicable API calls. | Volume level should be set and retrieved successfully with the correct value. CPU load and memory usage should remain within expected limits. |
| 5 | Restore initial volume | Set the volume back to the initial value saved before the test. | Volume should be restored to original level. |
| 6 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 7 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 8 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the volume level stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 600

**Priority** : High

**Release Version** : M95<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
