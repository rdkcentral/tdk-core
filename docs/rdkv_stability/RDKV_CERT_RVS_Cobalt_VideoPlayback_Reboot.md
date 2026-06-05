## TestCase ID
RDKV_STABILITY_62
## TestCase Name
RDKV_CERT_RVS_Cobalt_VideoPlayback_Reboot
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by playing a video in Cobalt and repeatedly rebooting the device, verifying video playback can be established after each reboot and CPU/memory usage remains within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the supported plugins list.|
|3|cobalt_test_url and reboot_max_count must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=resumed, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt and start video | Launch Cobalt via applicable API calls. Set the video URL via deeplink: `{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":{"url":"<cobalt_test_url>"}}` | Cobalt should launch and start playing the video. |
| 4 | Validate video playback | Verify that video is playing by checking decoder process entries via applicable API calls. | Video should be playing (decoder proc entry present). |
| 5 | Validate initial resource usage | Validate CPU load and memory usage via applicable API calls. | CPU load and memory usage should be within expected limits. |
| 6 | Reboot and re-launch loop (repeat for reboot_max_count iterations) | For each iteration: <br>Reboot the device via `org.rdk.System.1.reboot`. <br>Wait for device to come back online and WPEFramework to restart. <br>Re-apply plugin preconditions. <br>Re-launch Cobalt and set video URL via deeplink. <br>Validate video is playing via applicable API calls. <br>Validate CPU load and memory usage via applicable API calls. | Device should reboot and come back online. Cobalt should re-launch successfully. Video should play after each reboot. CPU load and memory usage should remain within expected limits. |
| 7 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 8 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 9 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the reboot stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 540

**Priority** : High

**Release Version** : M108<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
