## TestCase ID
RDKV_PERFORMANCE_91
## TestCase Name
RDKV_CERT_PACS_Cobalt_Destroy_OnVideoPlayback
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the Cobalt plugin can be destroyed during active video playback and relaunched to play video successfully again without device instability.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt and WebKitBrowser plugins should be available in the supported plugins list.|
|3|`cobalt_test_url` must be configured in `PerformanceTestVariables`.|
|4|SSH access parameters (method, credentials, video validation script) must be configured in the device config file.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online within the expected time. |
| 2 | Check Plugin Status | Check the current state of plugins Cobalt and WebKitBrowser via: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Plugin states are retrieved successfully. |
| 3 | Set Plugin Pre-conditions | Deactivate WebKitBrowser and Cobalt plugins if not already deactivated: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"WebKitBrowser"}}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"Cobalt"}}` | Plugins are set to deactivated state as required. |
| 4 | Launch Cobalt | Launch the Cobalt plugin via RDKShell and verify it is in the foreground: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.getZOrder"}` | Cobalt is launched and in the foreground in the z-order list. |
| 5 | Set Video URL | Load the configured video URL into Cobalt using the deeplink method: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":"<cobalt_test_url>"}` | Cobalt deeplink API returns success. |
| 6 | Start Video Playback | Press the Enter key twice to initiate video playback (second press to skip ad if present): <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":13,"modifiers":[],"delay":1.0}]}}` | Key press is sent successfully. |
| 7 | Validate Video Playing | Verify video playback has started by checking the wpeframework log via SSH for the state transition from PAUSED to PLAYING: <br>`cat /opt/logs/wpeframework.log \| grep -inr "State.*changed.*old.*PAUSED.*new.*PLAYING" \| tail -1` | Log entry confirms video state changed from PAUSED to PLAYING after the key press time. |
| 8 | Destroy Cobalt | Destroy the Cobalt plugin while video is playing: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.destroy","params":{"callsign":"Cobalt"}}` | Cobalt plugin is destroyed successfully. |
| 9 | Relaunch Cobalt | Launch Cobalt again after destruction and verify it enters the foreground: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.getZOrder"}` | Cobalt is relaunched and present in foreground z-order. |
| 10 | Set Video URL Again | Reload the video URL in the relaunched Cobalt instance using the deeplink method: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":"<cobalt_test_url>"}` | Cobalt deeplink returns success. |
| 11 | Start Video Playback Again | Press the Enter key to play the video in the relaunched Cobalt: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":13,"modifiers":[],"delay":1.0}]}}` | Key press is sent successfully. |
| 12 | Validate Video Playing After Relaunch | Verify video playback is happening after Cobalt was relaunched, by checking wpeframework log via SSH: <br>`cat /opt/logs/wpeframework.log \| grep -inr "State.*changed.*old.*PAUSED.*new.*PLAYING" \| tail -1` | Log confirms video is playing successfully after Cobalt relaunch. |
| 13 | Destroy Cobalt | Destroy Cobalt at the end of the test: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.destroy","params":{"callsign":"Cobalt"}}` | Cobalt is destroyed. Device remains stable. |
| 14 | Revert Plugin Status | Restore original plugin states for Cobalt and WebKitBrowser as captured before the test: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"<plugin>"}}` | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 8

**Priority** : High

**Release Version** : M95<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
