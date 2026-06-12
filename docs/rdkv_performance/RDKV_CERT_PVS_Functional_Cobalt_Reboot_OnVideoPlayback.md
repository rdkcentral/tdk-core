## TestCase ID
RDKV_PERFORMANCE_70
## TestCase Name
RDKV_CERT_PVS_Functional_Cobalt_Reboot_OnVideoPlayback
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that Cobalt (YouTube) remains stable and functional after a device reboot performed during active video playback.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin should be available in the device build.|
|3|`cobalt_test_url` must be configured in `PerformanceTestVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Verify and set plugin states — activate Cobalt. | Cobalt confirmed in activated state. |
| 3 | Launch Cobalt and Start Video | Launch Cobalt via RDKShell: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"Cobalt","type":"","uri":""}}` Load video URL and start playback. | Video playing in Cobalt. |
| 4 | Reboot Device During Playback | Reboot the device while video is playing: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.harakiri"}` | Device reboots. |
| 5 | Wait for Device to Come Online | Wait for the device to reboot and WPEFramework to restart. | Device comes online. |
| 6 | Verify Cobalt Stability | After reboot, verify Cobalt can be activated and a URL can be loaded without crashes: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"Cobalt"}}` | Cobalt is stable and functional after reboot during video playback. |
| 7 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 7

**Priority** : High

**Release Version** : M93<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
