## TestCase ID
RDKV_STABILITY_26
## TestCase Name
RDKV_CERT_RVS_WebKitBrowser_KeyStress
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate WebKitBrowser stability by sending 1000 random key events to the browser while it is playing a video, verifying the video continues playing and CPU/memory usage remains within expected limits throughout.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin must be in resumed state; Cobalt plugin must be deactivated; DeviceInfo plugin must be activated.|
|3|video_src_url_hls (HLS video stream) and key_stress_max_count must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of WebKitBrowser, Cobalt, and DeviceInfo plugins. Set required states: WebKitBrowser=resumed, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Get current URL and set video stream | Retrieve and save the current URL from WebKitBrowser. Set the HLS video stream URL: `{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"value":"<video_src_url_hls>"}}` | Video stream URL set. |
| 4 | Validate video playback | Verify video is playing by checking decoder process entries via applicable API calls. | Video decoder proc entry should be present. |
| 5 | Key stress loop (100 outer iterations × 10 key events) | For each of 100 outer iterations: <br>Send 10 random key events to WebKitBrowser via `org.rdk.RDKShell.1.generateKey`: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keyCode":<random_key>,"modifiers":[],"client":"WebKitBrowser"}}` <br>Validate video is still playing via applicable API calls. <br>Validate CPU load and memory usage via applicable API calls. | Random key events should be delivered. Video should continue playing after each outer iteration. CPU load and memory usage should remain within expected limits. |
| 6 | Restore initial URL | Set WebKitBrowser URL back to the original URL. | Original URL should be restored. |
| 7 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 8 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 9 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the key stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 720

**Priority** : High

**Release Version** : M88<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
