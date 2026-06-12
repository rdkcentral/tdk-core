## TestCase ID
RDKV_PERFORMANCE_66
## TestCase Name
RDKV_CERT_PACS_Cobalt_TimeTo_PlayNextVideo
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to start playing the next video in Cobalt after navigating from a currently playing video is within the expected threshold limit.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt and WebKitBrowser plugins should be available in the build.|
|3|`cobalt_test_url` must be configured in `PerformanceTestVariables`.|
|4|SSH access parameters must be configured in device config for wpeframework log access.|
|5|Time in Test Manager and DUT should be in sync.|
|6|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of Cobalt and WebKitBrowser plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugin states retrieved. |
| 3 | Launch Cobalt | Launch Cobalt via RDKShell: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt launched and in foreground. |
| 4 | Set Video URL | Load the video URL into Cobalt using the deeplink method: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":"<cobalt_test_url>"}` | Deeplink returns success. |
| 5 | Start Video Playback | Press Enter key to start video playback: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":13,"modifiers":[],"delay":1.0}]}}` | Key press sent. |
| 6 | Validate First Video Playing | Verify video playback is happening via proc entry validation or wpeframework log via SSH. | Video is playing successfully. |
| 7 | Navigate to Next Video | Send Down Arrow (keyCode 40), Down Arrow (keyCode 40), and Enter (keyCode 13) keys to navigate to and select the next video. Record system time before pressing Enter: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":40,"modifiers":[],"delay":1.0}]}}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":13,"modifiers":[],"delay":1.0}]}}` | Key presses sent; play start time recorded. |
| 8 | Validate Time to Play Next Video | Check wpeframework log via SSH for the PAUSED-to-PLAYING state transition for the new video: <br>`cat /opt/logs/wpeframework.log \| grep -inr "State.*changed.*old.*PAUSED.*new.*PLAYING" \| tail -1` Calculate time from key press to first PLAYING event for the next video. Validate against `COBALT_PLAY_NEXT_VIDEO_TIME_THRESHOLD_VALUE`. | Time taken to start playing the next video is within the expected threshold. |
| 9 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 4

**Priority** : High

**Release Version** : M92<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
