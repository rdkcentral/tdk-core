## TestCase ID
RDKV_PERFORMANCE_131
## TestCase Name
RDKV_CERT_PVS_Functional_Vimeo_ResourceUsage_VideoPlayBack
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges during Vimeo video playback.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|The application plugin used for Vimeo must be available in the build.|
|3|Vimeo video stream URL must be configured in `PerformanceTestVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Launch Vimeo and Start Video | Launch Vimeo application and begin video playback. | Vimeo video playing. |
| 3 | Capture Baseline Resource Usage | Record CPU and memory usage at steady state during video playback. | Baseline recorded. |
| 4 | Continue Video Playback | Allow video to play for the configured duration. | Video playing continuously. |
| 5 | Capture Final Resource Usage | Record CPU and memory usage after playback period. | Resource data captured. |
| 6 | Validate Resource Usage | Verify CPU load and memory usage during Vimeo video playback are within acceptable limits. | CPU load and memory usage during Vimeo video playback are within the expected limits. |
| 7 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M106<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
