## TestCase ID
RDKV_STABILITY_34
## TestCase Name
RDKV_CERT_RVS_VideoResize
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by repeatedly resizing the video window via RDKShell for resize_max_count iterations while streaming video content, verifying CPU and memory usage remains within expected limits after each resize operation.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin must be in resumed state; Cobalt plugin must be deactivated; DeviceInfo plugin must be activated.|
|3|video_src_url_hls (HLS video stream) and resize_max_count must be configured in StabilityTestVariables.|
|4|resize_params_list must be configured with a list of (x, y, width, height) window dimensions to cycle through.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of WebKitBrowser, Cobalt, and DeviceInfo plugins. Set required states: WebKitBrowser=resumed, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Get current URL and set video stream | Retrieve and save the current URL from WebKitBrowser. Set the HLS video stream URL: `{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"value":"<video_src_url_hls>"}}` | Current URL saved. Video stream URL set and video should start playing. |
| 4 | Validate video playback | Verify video is playing by checking decoder process entries via applicable API calls. | Video decoder proc entry should be present. |
| 5 | Video resize loop (repeat for resize_max_count iterations cycling through resize_params_list) | For each iteration and for each set of resize parameters: <br>Resize the WebKitBrowser window via RDKShell: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.setBounds","params":{"client":"WebKitBrowser","x":<x>,"y":<y>,"w":<w>,"h":<h>}}` <br>Validate video is still playing via applicable API calls. <br>Validate CPU load and memory usage via applicable API calls. | Video should continue playing after each resize. CPU load and memory usage should remain within expected limits. |
| 6 | Restore initial URL | Set WebKitBrowser URL back to the original URL. | Original URL should be restored. |
| 7 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 8 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 9 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the video resize stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 720

**Priority** : High

**Release Version** : M88<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
