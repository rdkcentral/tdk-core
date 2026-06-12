## TestCase ID
RDKV_PERFORMANCE_119
## TestCase Name
RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_MP4
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken for play and pause operations on an MP4 video in a Lightning application is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser and DeviceInfo plugins should be available in the build.|
|3|`video_src_url_mp4` (MP4 video URL) and `codec_mp4` must be configured in `MediaValidationVariables`.|
|4|`LOGGING_METHOD` must be configured in the device config file.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check and activate WebKitBrowser and DeviceInfo, deactivate Cobalt. | Plugins confirmed in required state. |
| 3 | Configure Video Player URL | Build the test app URL with MP4 source from `MediaValidationVariables.video_src_url_mp4` and operations (pause 10s, play 10s). | Test app URL constructed. |
| 4 | Launch Video Player App | Load the video player application in WebKitBrowser with MP4 video: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"url":"<test_app_url>"}}` | Video player launches and MP4 video starts playing. |
| 5 | Perform Play/Pause Operations | Video player automatically performs pause and play operations; timestamps recorded for each. | Play/pause operations complete successfully. |
| 6 | Validate Play/Pause Time | Calculate the time taken for play and pause on MP4 video. Compare against threshold. | Time taken for play/pause on MP4 video is within the expected threshold. |
| 7 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 6

**Priority** : High

**Release Version** : M99<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
