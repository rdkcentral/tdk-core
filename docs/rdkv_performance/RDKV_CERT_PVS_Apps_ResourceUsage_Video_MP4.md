## TestCase ID
RDKV_PERFORMANCE_213
## TestCase Name
RDKV_CERT_PVS_Apps_ResourceUsage_Video_MP4
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges during MP4 video playback in a Lightning application.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser, DeviceInfo, and `org.rdk.PersistentStore` plugins should be available in the build.|
|3|`video_src_url_mp4` (MP4 video URL) and `codec_mp4` must be configured in `MediaValidationVariables`.|
|4|`LOGGING_METHOD` must be configured in the device config file.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check and activate WebKitBrowser, DeviceInfo and `org.rdk.PersistentStore` plugins. Deactivate Cobalt. | Plugins confirmed in required state. |
| 3 | Configure Video Player URL | Build the test app URL with MP4 video source, operations (pause, play), and logging parameters from `MediaValidationVariables.video_src_url_mp4`. | Test app URL constructed. |
| 4 | Launch Video Player App | Load the video player application in WebKitBrowser with the configured URL: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"url":"<test_app_url>"}}` | Video player launches and MP4 video starts playing. |
| 5 | Validate Resource Usage During MP4 Playback | Capture and validate CPU load and memory usage while the MP4 video is playing. | CPU load and memory usage during MP4 playback are within the expected limits. |
| 6 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
