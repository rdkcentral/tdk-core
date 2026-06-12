## TestCase ID
RDKV_PERFORMANCE_21
## TestCase Name
RDKV_CERT_PACS_WiFi_Cobalt_ResourceUsage_VideoPlayback
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges during video playback in Cobalt when the device is connected to a 2.4 GHz WiFi network.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt, WebKitBrowser, and DeviceInfo plugins should be available in the build.|
|3|`cobalt_test_url` must be configured in `PerformanceTestVariables`.|
|4|The DUT should be connected to a 2.4 GHz WiFi Access Point.|
|5|SSH access parameters must be configured in device config for proc/log validation.|
|6|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Check the current state of Cobalt, WebKitBrowser, and DeviceInfo plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}`<br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@DeviceInfo"}` | Plugin states retrieved. |
| 3 | Set Plugin Pre-conditions | Activate DeviceInfo and deactivate Cobalt and WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"DeviceInfo"}}` | Plugins set to required state. |
| 4 | Launch Cobalt | Launch Cobalt via RDKShell: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` | Cobalt launched and in foreground. |
| 5 | Set Video URL | Load the video URL into Cobalt via deeplink: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":"<cobalt_test_url>"}` | Deeplink returns success. |
| 6 | Start Video Playback | Press Enter key to start video playback (twice to skip ad): <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keys":[{"keyCode":13,"modifiers":[],"delay":1.0}]}}` | Key presses sent. |
| 7 | Validate Video Playing | Verify video playback is active via proc entry validation or wpeframework log via SSH. | Video playback is confirmed as active. |
| 8 | Validate Resource Usage | Retrieve and validate CPU load and memory usage while video is playing over WiFi. | CPU load and memory usage are within acceptable limits. |
| 9 | Deactivate Cobalt | Deactivate the Cobalt plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"Cobalt"}}` | Cobalt deactivated. |
| 10 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 15

**Priority** : High

**Release Version** : M85<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
