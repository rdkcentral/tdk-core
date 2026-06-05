## TestCase ID
RDKV_STABILITY_79
## TestCase Name
RDKV_CERT_RVS_HtmlApp_LaunchURL_StressTest
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate HtmlApp plugin stability by repeatedly setting a video stream URL 100 times without destroying the plugin between iterations, verifying the URL is loaded correctly and CPU/memory usage remains within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|HtmlApp plugin must be in resumed state; Cobalt plugin must be deactivated; DeviceInfo plugin must be activated.|
|3|video_src_url_hls (HLS video stream URL) must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of HtmlApp, Cobalt, and DeviceInfo plugins. Set required states: HtmlApp=resumed, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | URL stress test loop (100 iterations without destroy) | For each of 100 iterations: <br>Set the HLS video stream URL in HtmlApp: `{"jsonrpc":"2.0","id":1234567890,"method":"HtmlApp.1.url","params":{"value":"<video_src_url_hls>"}}` <br>Verify the URL is set correctly by getting the current URL: `{"jsonrpc":"2.0","id":1234567890,"method":"HtmlApp.1.url"}` <br>Validate CPU load and memory usage via applicable API calls. Note: HtmlApp is NOT destroyed between iterations. | URL should be set and verified successfully in each iteration. CPU load and memory usage should remain within expected limits without plugin restart. |
| 4 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 5 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 6 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the URL stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 20

**Priority** : High

**Release Version** : M135<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
