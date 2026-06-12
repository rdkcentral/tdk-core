## TestCase ID
RDKV_PERFORMANCE_158
## TestCase Name
RDKV_CERT_PVS_LightningApp_Video_Playback_MemoryUsage_WithWebinspect
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that LightningApp memory usage does not grow beyond acceptable limits during extended video playback, as measured using the Web Inspector tool.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|LightningApp plugin should be available in the device build.|
|3|Web Inspector must be enabled and accessible on the device.|
|4|A video stream URL must be configured in `PerformanceTestVariables`.|
|5|Memory usage threshold must be configured in device config.|
|6|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Activate LightningApp | Activate LightningApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"LightningApp"}}` | LightningApp activated. |
| 3 | Connect Web Inspector | Connect the Web Inspector to the LightningApp process to enable memory profiling. | Web Inspector connected. |
| 4 | Load Video URL in LightningApp | Set the video stream URL: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"LightningApp.1.url","params":{"url":"<video_url>"}}` | Video URL loaded and playback started. |
| 5 | Record Initial Memory Usage | Record the initial JavaScript heap and DOM memory usage via Web Inspector. | Initial memory usage recorded. |
| 6 | Continue Video Playback | Allow video to play for the configured extended duration while monitoring memory. | Video playing for the full duration. |
| 7 | Record Final Memory Usage | Record the final JavaScript heap and DOM memory usage via Web Inspector after extended playback. | Final memory usage recorded. |
| 8 | Validate Memory Usage | Verify that memory growth during playback does not exceed the acceptable threshold. | LightningApp memory usage during extended video playback is within the acceptable limit as measured by Web Inspector. |
| 9 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 300

**Priority** : High

**Release Version** : M132<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
