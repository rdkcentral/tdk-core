## TestCase ID
RDKV_PERFORMANCE_163
## TestCase Name
RDKV_CERT_PVS_WebKitBrowser_Video_Playback_Without_Crash_WithWebinspect
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that WebKitBrowser remains stable and does not crash during extended video playback, as monitored using the Web Inspector tool.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin should be available in the device build.|
|3|Web Inspector must be enabled and accessible on the device.|
|4|A video stream URL must be configured in `PerformanceTestVariables`.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Activate WebKitBrowser | Activate WebKitBrowser plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"WebKitBrowser"}}` | WebKitBrowser activated. |
| 3 | Connect Web Inspector | Connect the Web Inspector to the WebKitBrowser process. | Web Inspector connected. |
| 4 | Load Video URL in WebKitBrowser | Set the video stream URL: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"WebKitBrowser.1.url","params":{"url":"<video_url>"}}` | Video URL loaded and playback started. |
| 5 | Monitor Playback Stability | Monitor WebKitBrowser and web inspector for the configured extended duration, checking for crashes or unresponsive states. | WebKitBrowser remains responsive throughout. |
| 6 | Verify WebKitBrowser Status | After extended playback, verify WebKitBrowser plugin status is still active: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | WebKitBrowser still in activated state. |
| 7 | Validate No Crash Occurred | Confirm WebKitBrowser did not crash during the extended video playback session. | WebKitBrowser completed extended video playback without any crash or instability. |
| 8 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 100

**Priority** : High

**Release Version** : M132<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
