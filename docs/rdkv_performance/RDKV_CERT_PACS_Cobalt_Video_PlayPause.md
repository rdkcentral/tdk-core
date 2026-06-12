## TestCase ID
RDKV_PERFORMANCE_11
## TestCase Name
RDKV_CERT_PACS_Cobalt_Video_PlayPause
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that video in Cobalt can be paused using the Space key and resumed to continue playing correctly.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt and WebKitBrowser plugins should be available in the build.|
|3|`cobalt_test_url` must be configured in `PerformanceTestVariables`.|
|4|SSH access parameters must be configured in device config for proc/log validation.|
|5|TV must be connected to the DUT.|
|6|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of WebKitBrowser and Cobalt plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Plugin states retrieved. |
| 3 | Launch Cobalt | Launch Cobalt via RDKShell: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt launched and in foreground. |
| 4 | Set Video URL | Load the video URL into Cobalt using the deeplink method: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":"<cobalt_test_url>"}` | Deeplink returns success. |
| 5 | Start Video Playback | Press Enter key to start video, then again to skip any ad: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":13,"modifiers":[],"delay":1.0}]}}` | Key presses sent. |
| 6 | Validate Video Playing | Verify video playback is active via proc entry validation or wpeframework log via SSH. | Video is playing successfully. |
| 7 | Pause Video | Send Space key (keyCode 32) to pause the video: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":32,"modifiers":[],"delay":1.0}]}}` | Space key press sent; video pauses. |
| 8 | Validate Video Paused | Verify the video is paused via proc entry validation or wpeframework log via SSH. | Video is confirmed as paused. |
| 9 | Resume Video | Send Space key again (keyCode 32) to resume the video: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":32,"modifiers":[],"delay":1.0}]}}` | Space key press sent; video resumes. |
| 10 | Validate Video Playing Again | Verify video playback is active again via proc entry validation or wpeframework log via SSH. | Video is confirmed as playing again. |
| 11 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
