## TestCase ID
RDKV_STABILITY_60
## TestCase Name
RDKV_CERT_RVS_DisplaySettings_SetandGetResolution
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by repeatedly setting and getting display resolutions from the list of supported resolutions for set_resolution_max_count iterations, verifying each resolution change is applied correctly and CPU/memory usage remains within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|org.rdk.DisplaySettings and DeviceInfo plugins must be available in the supported plugins list.|
|3|The device must have connected video display accessible via `getConnectedVideoDisplays`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of org.rdk.DisplaySettings and DeviceInfo plugins. Set required states: org.rdk.DisplaySettings=activated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Get connected video displays and current resolution | Retrieve connected video displays: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}` Get and save current resolution as initial value: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.DisplaySettings.1.getCurrentResolution","params":{"videoDisplay":"<display>"}}` Get list of supported resolutions: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.DisplaySettings.1.getSupportedResolutions","params":{"videoDisplay":"<display>"}}` | Connected displays, current resolution, and supported resolutions list should all be retrieved successfully. |
| 4 | Set resolution loop (repeat for set_resolution_max_count iterations cycling through supported resolutions) | For each iteration: <br>Select next resolution from supported resolutions list (cycling through them). <br>Set the resolution: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.DisplaySettings.1.setCurrentResolution","params":{"videoDisplay":"<display>","resolution":"<resolution>"}}` <br>Get the resolution and verify it matches the set value: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.DisplaySettings.1.getCurrentResolution","params":{"videoDisplay":"<display>"}}` <br>Validate CPU load and memory usage via applicable API calls. | Resolution should be set and verified successfully. CPU load and memory usage should remain within expected limits. |
| 5 | Restore initial resolution | Set display resolution back to the initial resolution saved before the test. | Initial resolution should be restored successfully. |
| 6 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 7 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 8 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the resolution change stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 600

**Priority** : High

**Release Version** : M95<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
