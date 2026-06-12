## TestCase ID
RDKV_PERFORMANCE_34
## TestCase Name
RDKV_CERT_PACS_Cobalt_ResourceUsage_VideoPlayback
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges during active video playback in the Cobalt application.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt, WebKitBrowser, and DeviceInfo plugins should be available in the build.|
|3|`cobalt_test_url` must be configured in `PerformanceTestVariables`.|
|4|SSH access parameters (method, credentials, video validation script) must be configured in device config.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of Cobalt, WebKitBrowser, and DeviceInfo plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@DeviceInfo"}` | Plugin states retrieved. |
| 3 | Set Plugin Pre-conditions | Activate DeviceInfo and deactivate Cobalt and WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"DeviceInfo"}}` | Plugins set to required state. |
| 4 | Launch Cobalt | Launch Cobalt via RDKShell: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt is launched and in foreground. |
| 5 | Set Video URL | Load the video URL into Cobalt using the deeplink method: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":"<cobalt_test_url>"}` | Deeplink returns success. |
| 6 | Start Video Playback | Press Enter key to start video playback (twice: once to play, once to skip ad): <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":13,"modifiers":[],"delay":1.0}]}}` | Key press sent successfully. |
| 7 | Validate Video Playing | Verify video playback is happening via proc entry validation or wpeframework log via SSH: <br>`cat /opt/logs/wpeframework.log \| grep -inr "State.*changed.*old.*PAUSED.*new.*PLAYING" \| tail -1` | Video playback is confirmed as active. |
| 8 | Validate Resource Usage | Retrieve and validate CPU load and memory usage are within expected thresholds while video is playing. | CPU load and memory usage are within acceptable limits. |
| 9 | Deactivate Cobalt | Deactivate the Cobalt plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"Cobalt"}}` | Cobalt deactivated. |
| 10 | Revert Plugin Status | Restore the original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M87<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
