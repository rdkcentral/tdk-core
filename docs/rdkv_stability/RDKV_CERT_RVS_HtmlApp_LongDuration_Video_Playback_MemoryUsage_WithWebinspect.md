## TestCase ID
RDKV_STABILITY_76
## TestCase Name
RDKV_CERT_RVS_HtmlApp_LongDuration_Video_Playback_MemoryUsage_WithWebinspect
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate HtmlApp memory usage during long-duration video playback by connecting via webinspect WebSocket, playing video for a configured duration, and measuring JavaScript heap memory usage to ensure it stays within acceptable limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|HtmlApp plugin must be in resumed state; Cobalt must be deactivated; DeviceInfo must be activated.|
|3|html_app_webinspect_port and html_video_url must be configured in StabilityTestVariables.|
|4|html_memory_limit_kb must be configured to define acceptable memory threshold.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of HtmlApp, Cobalt, and DeviceInfo plugins. Set required states: HtmlApp=resumed, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Open webinspect WebSocket connection | Connect to HtmlApp via WebSocket on html_app_webinspect_port: `createEventListener(ip, html_app_webinspect_port, [], "/devtools/page/1", False)` | WebSocket connection to HtmlApp webinspect port should be established. |
| 4 | Set video URL and start playback | Set the video URL in HtmlApp: `{"jsonrpc":"2.0","id":1234567890,"method":"HtmlApp.1.url","params":{"value":"<html_video_url>"}}` | Video URL should be set and video playback should start. |
| 5 | Monitor memory usage (for configured duration) | Periodically over the configured long-duration test period: <br>Request JavaScript heap memory snapshot via the WebSocket devtools protocol. <br>Validate that JavaScript heap usage is below html_memory_limit_kb threshold. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | JavaScript heap memory should remain below the configured limit throughout the test duration. Video should play continuously without memory leaks. |
| 6 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all timed measurement data. |
| 7 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 8 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the long-duration memory usage test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 720

**Priority** : High

**Release Version** : M132<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
