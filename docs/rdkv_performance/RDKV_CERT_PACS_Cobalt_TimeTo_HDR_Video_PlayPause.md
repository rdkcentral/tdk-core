## TestCase ID
RDKV_PERFORMANCE_150
## TestCase Name
RDKV_CERT_PACS_Cobalt_TimeTo_HDR_Video_PlayPause
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to play and pause an HDR video on YouTube in the Cobalt application is within the expected threshold limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt and WebKitBrowser plugins should be available in the build.|
|3|`HDRvideo_test_url` must be configured in `PerformanceTestVariables`.|
|4|SSH access parameters must be configured in device config for wpeframework log access.|
|5|Time in Test Manager and DUT should be in sync with UTC.|
|6|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of Cobalt and WebKitBrowser plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugin states retrieved. |
| 3 | Set Plugin Pre-conditions | Deactivate Cobalt and WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"Cobalt"}}` | Plugins deactivated. |
| 4 | Launch Cobalt | Launch Cobalt via RDKShell: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt launched and in foreground. |
| 5 | Set HDR Video URL | Load the HDR video URL into Cobalt using the deeplink method: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":"<HDRvideo_test_url>"}` | Deeplink returns success. |
| 6 | Start HDR Video Playback | Save current system time and press Enter key to start HDR video playback: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":13,"modifiers":[],"delay":1.0}]}}` | Key press sent; playback start time recorded. |
| 7 | Validate Time to Play | Check wpeframework log via SSH for the PAUSED-to-PLAYING state transition and validate time: <br>`cat /opt/logs/wpeframework.log \| grep -inr "State.*changed.*old.*PAUSED.*new.*PLAYING" \| tail -1` | Video play time is within the configured threshold. |
| 8 | Pause HDR Video | Save current system time and press Space key (keyCode 32) to pause the HDR video: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":32,"modifiers":[],"delay":1.0}]}}` | Space key press sent; pause start time recorded. |
| 9 | Validate Time to Pause | Check wpeframework log via SSH for the PLAYING-to-PAUSED state transition and validate the pause time: <br>`cat /opt/logs/wpeframework.log \| grep -inr "State.*changed.*old.*PLAYING.*new.*PAUSED" \| tail -1` | Video pause time is within the configured `COBALT_VIDEO_PAUSE_TIME_THRESHOLD_VALUE`. |
| 10 | Resume HDR Video | Save current system time and press Space key again to resume: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":32,"modifiers":[],"delay":1.0}]}}` | Space key press sent; resume start time recorded. |
| 11 | Validate Time to Resume | Check wpeframework log via SSH for PAUSED-to-PLAYING transition and validate the resume time. | Resume time is within the configured threshold. |
| 12 | Deactivate Cobalt | Deactivate the Cobalt plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"Cobalt"}}` | Cobalt deactivated. |
| 13 | Revert Plugin Status | Restore the original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M121<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
