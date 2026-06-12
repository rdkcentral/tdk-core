## TestCase ID
RDKV_PERFORMANCE_146
## TestCase Name
RDKV_CERT_PACS_Cobalt_VideoPlayback_Without_Crash
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that video playback in the Cobalt application proceeds without any crash during the playback session.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt and WebKitBrowser plugins should be available in the build.|
|3|`cobalt_test_url` must be configured in `PerformanceTestVariables`.|
|4|SSH access parameters must be configured in device config for wpeframework log access.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of Cobalt and WebKitBrowser plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugin states retrieved. |
| 3 | Launch Cobalt | Launch Cobalt via RDKShell: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt launched and in foreground. |
| 4 | Set Video URL | Load the video URL into Cobalt using the deeplink method: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":"<cobalt_test_url>"}` | Deeplink returns success. |
| 5 | Start Video Playback | Press Enter key twice to start video and skip ad: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":13,"modifiers":[],"delay":1.0}]}}` | Key presses sent. |
| 6 | Validate Video Playing | Verify video playback has started by checking wpeframework log for PAUSED-to-PLAYING state transition via SSH: <br>`cat /opt/logs/wpeframework.log \| grep -inr "State.*changed.*old.*PAUSED.*new.*PLAYING" \| tail -1` | Log confirms video is in PLAYING state. |
| 7 | Check for Crash | Verify no crash is observed in wpeframework logs during the video playback session via SSH log analysis. | No crash log entries are found; device and Cobalt remain stable throughout playback. |
| 8 | Deactivate Cobalt | Deactivate the Cobalt plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"Cobalt"}}` | Cobalt deactivated. |
| 9 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M118<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
