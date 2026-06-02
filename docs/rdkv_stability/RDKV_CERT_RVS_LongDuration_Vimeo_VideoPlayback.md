## TestCase ID
RDKV_STABILITY_66
## TestCase Name
RDKV_CERT_RVS_LongDuration_Vimeo_VideoPlayback
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by playing a Vimeo video stream via webkit_instance for a configured long duration, measuring CPU load and memory usage periodically to ensure resources remain within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|webkit_instance plugin (WebKitBrowser or LightningApp as configured in StabilityTestVariables) must be in resumed state; Cobalt plugin must be deactivated; DeviceInfo plugin must be activated.|
|3|vimeo_video_url and test_duration must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of webkit_instance, Cobalt, and DeviceInfo plugins. Set required states: webkit_instance=resumed, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Set Vimeo video URL | Load the Vimeo video stream in webkit_instance.<br>{"jsonrpc":"2.0","id":1234567890,"method":"webkit_instance.1.url","params":{"value":"<vimeo_video_url>"}} | Vimeo video URL should be set and webkit_instance should start loading the stream. |
| 4 | Validate video playback | Verify that video is playing by checking decoder process entries via `rdkservice_validateProcEntry`. | Video decoder proc entry should be present, confirming Vimeo video playback. |
| 5 | Monitor resource usage (every 300 seconds for test_duration) | Every 5 minutes for the configured test duration: <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage` using DeviceInfo.1.systeminfo. <br>Verify video is still playing by re-checking the proc entry. | CPU load and memory usage should remain within expected limits throughout the test duration. Vimeo video should continue playing without interruption. |
| 6 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all timed measurement data. |
| 7 | Revert URL and plugins | Restore the original URL and revert plugins to their original state. | URL and plugins should be restored to pre-test state. |
| 8 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the long-duration Vimeo playback test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 740

**Priority** : High

**Release Version** : M100<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
