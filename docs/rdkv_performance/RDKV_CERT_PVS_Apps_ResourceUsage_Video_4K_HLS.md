## TestCase ID
RDKV_PERFORMANCE_126
## TestCase Name
RDKV_CERT_PVS_Apps_ResourceUsage_Video_4K_HLS
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges during 4K HLS video playback in a Lightning application.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser and DeviceInfo plugins should be available in the build.|
|3|`video_src_url_hls_2160p` (4K HLS video URL) and `app_url` must be configured in `MediaValidationVariables` and `PerformanceTestVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check and activate WebKitBrowser, deactivate Cobalt: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugins confirmed in required state. |
| 3 | Launch Video Player App | Load the video player application with 4K HLS video URL in WebKitBrowser. | Application launched and video is playing. |
| 4 | Validate Resource Usage During 4K HLS Playback | Capture and validate CPU load and memory usage while a 4K HLS video is playing. | CPU load and memory usage during 4K HLS playback are within the expected limits. |
| 5 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M103<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
