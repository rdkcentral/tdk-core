## TestCase ID
RDKV_STABILITY_95
## TestCase Name
RDKV_CERT_RVS_LightningApp_LongDuration_Video_Playback_MemoryUsage_WithWebinspect
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate LightningApp memory usage during long-duration video playback by connecting via webinspect WebSocket, playing video for a configured duration, and measuring JavaScript heap memory usage to ensure it stays within acceptable limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|LightningApp plugin must be in resumed state; Cobalt must be deactivated; DeviceInfo must be activated.|
|3|lightning_app_webinspect_port and lightning_video_url must be configured in StabilityTestVariables.|
|4|lightning_memory_limit_kb must be configured to define acceptable memory threshold.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of LightningApp, Cobalt, and DeviceInfo plugins. Set required states: LightningApp=resumed, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Open webinspect WebSocket connection | Connect to LightningApp via WebSocket on lightning_app_webinspect_port: `createEventListener(ip, lightning_app_webinspect_port, [], "/devtools/page/1", False)` | WebSocket connection to LightningApp webinspect port should be established. |
| 4 | Set video URL and start playback | Set the video URL in LightningApp: `{"jsonrpc":"2.0","id":1234567890,"method":"LightningApp.1.url","params":{"value":"<lightning_video_url>"}}` | Video URL should be set and video playback should start. |
| 5 | Monitor memory usage (for configured duration) | Periodically over the configured long-duration test period: <br>Request JavaScript heap memory snapshot via the WebSocket devtools protocol. <br>Validate that JavaScript heap usage is below lightning_memory_limit_kb threshold. <br>Validate CPU load and memory usage via applicable API calls. | JavaScript heap memory should remain below the configured limit throughout the test duration. Video should play continuously without memory leaks. |
| 6 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all timed measurement data. |
| 7 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 8 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the long-duration memory usage test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 720

**Priority** : High

**Release Version** : M132<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
