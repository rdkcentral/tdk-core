## TestCase ID
RDKV_STABILITY_77
## TestCase Name
RDKV_CERT_RVS_WebKitBrowser_LongDuration_Video_Playback_MemoryUsage_WithWebinspect
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate WebKitBrowser stability and memory health by playing a video for a configured long duration while monitoring JavaScript heap memory via the WebInspect port, ensuring memory remains below the configured webkit_memory_limit_kb threshold throughout playback.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin must be in resumed state with WebInspect port enabled; Cobalt must be deactivated; DeviceInfo must be activated.|
|3|video_src_url_hls (HLS video stream URL), test_duration, webinspect_port, and webkit_memory_limit_kb must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of WebKitBrowser, Cobalt, and DeviceInfo plugins. Set required states: WebKitBrowser=resumed, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Open WebInspect WebSocket connection | Establish a WebSocket connection to the WebKitBrowser WebInspect port (`webinspect_port`). Enable the Runtime and Memory domains: send `{"method":"Runtime.enable"}` and `{"method":"HeapProfiler.enable"}`. | WebSocket connection should be established. Runtime and HeapProfiler domains should be enabled. |
| 4 | Set video stream URL | Load the HLS video stream URL in WebKitBrowser: `{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"value":"<video_src_url_hls>"}}` | Video stream URL set. WebKitBrowser should start loading and playing the video. |
| 5 | Validate video playback | Verify that video is playing by checking decoder process entries via applicable API calls. | Video decoder proc entry should be present. |
| 6 | Memory monitoring loop (periodically for test_duration) | Every configured interval for the test_duration: <br>Request JavaScript heap snapshot via WebInspect: `{"method":"HeapProfiler.takeHeapSnapshot"}` <br>Read memory usage from WebInspect console: `{"method":"Runtime.evaluate","params":{"expression":"performance.memory.usedJSHeapSize"}}` <br>Verify memory usage is below webkit_memory_limit_kb. <br>Validate CPU load and memory via applicable API calls. <br>Confirm video is still playing via applicable API calls. | JS heap memory usage should remain below webkit_memory_limit_kb throughout. CPU load and memory usage should remain within expected limits. Video should continue playing without interruption. |
| 7 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all timed measurement data. |
| 8 | Revert URL and plugins | Restore the original URL and revert plugins to their original state. | URL and plugins should be restored to pre-test state. |
| 9 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the long-duration memory monitoring test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 720

**Priority** : High

**Release Version** : M132<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
