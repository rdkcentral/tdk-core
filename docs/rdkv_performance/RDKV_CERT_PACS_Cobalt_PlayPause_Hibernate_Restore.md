## TestCase ID
RDKV_PERFORMANCE_149
## TestCase Name
RDKV_CERT_PACS_Cobalt_PlayPause_Hibernate_Restore
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that Cobalt can pause and play video correctly after being restored from a hibernated state.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt and WebKitBrowser plugins should be available in the build.|
|3|`cobalt_test_url` must be configured in `PerformanceTestVariables`.|
|4|SSH access parameters must be configured in the device config file.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of Cobalt and WebKitBrowser plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugin states retrieved. |
| 3 | Launch Cobalt | Launch Cobalt via RDKShell: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt is launched and in foreground. |
| 4 | Hibernate Cobalt | Suspend Cobalt to put it into a hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"suspended"}` | Cobalt transitions to hibernated state. |
| 5 | Validate Hibernated State | Confirm Cobalt is in the hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Cobalt state is `hibernated`. |
| 6 | Restore Cobalt | Restore Cobalt from hibernated state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.state","params":"resumed"}` | Cobalt transitions to suspended state. |
| 7 | Launch Cobalt with Video URL | Launch Cobalt and set the video URL via deeplink method: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":"<cobalt_test_url>"}` | Deeplink returns success; URL loaded in Cobalt. |
| 8 | Start Video Playback | Press Enter key to start video playback and OK again to skip ad: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":13,"modifiers":[],"delay":1.0}]}}` | Key presses sent successfully. |
| 9 | Validate Video Playing | Verify video playback is active via wpeframework log or proc entry validation via SSH: <br>`cat /opt/logs/wpeframework.log \| grep -inr "State.*changed.*old.*PAUSED.*new.*PLAYING" \| tail -1` | Log confirms video is in PLAYING state. |
| 10 | Pause Video | Send the Space key (keyCode 32) to pause the video: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":32,"modifiers":[],"delay":1.0}]}}` | Space key press sent. |
| 11 | Validate Video Paused | Verify the video is paused by checking wpeframework log via SSH for PLAYING to PAUSED transition: <br>`cat /opt/logs/wpeframework.log \| grep -inr "State.*changed.*old.*PLAYING.*new.*PAUSED" \| tail -1` | Log confirms video state changed to PAUSED. |
| 12 | Resume Video | Send the Space key again to resume video playback: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":32,"modifiers":[],"delay":1.0}]}}` | Space key press sent. |
| 13 | Validate Video Playing Again | Verify video resumes playback via wpeframework log via SSH. | Log confirms video is in PLAYING state again. |
| 14 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M129<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
