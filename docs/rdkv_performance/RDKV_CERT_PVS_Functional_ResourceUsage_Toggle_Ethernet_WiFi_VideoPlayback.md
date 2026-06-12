## TestCase ID
RDKV_PERFORMANCE_133
## TestCase Name
RDKV_CERT_PVS_Functional_ResourceUsage_Toggle_Ethernet_WiFi_VideoPlayback
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage remain within acceptable ranges while toggling between Ethernet and WiFi network interfaces during active video playback.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Both Ethernet and WiFi network interfaces must be available on the device.|
|3|A video playback stream URL must be configured in `PerformanceTestVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Start Video Playback | Launch the video playback application and start streaming. | Video playback in progress. |
| 3 | Capture Baseline Resource Usage | Record CPU and memory usage during video playback. | Baseline recorded. |
| 4 | Toggle to WiFi | Disable Ethernet and enable WiFi interface while video is playing. | Network switch to WiFi completed. |
| 5 | Capture Resource Usage (WiFi) | Record CPU and memory usage during WiFi video playback. | Resource data captured. |
| 6 | Toggle to Ethernet | Disable WiFi and enable Ethernet interface while video is playing. | Network switch to Ethernet completed. |
| 7 | Capture Resource Usage (Ethernet) | Record CPU and memory usage during Ethernet video playback. | Resource data captured. |
| 8 | Validate Resource Usage | Verify CPU load and memory usage during interface toggling and video playback are within acceptable limits. | CPU load and memory usage during interface toggling with video playback are within the expected limits. |
| 9 | Revert Plugin Status | Restore original plugin and network state. | Plugin and network state reverted. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M107<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
