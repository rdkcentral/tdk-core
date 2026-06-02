## TestCase ID
RDKV_STABILITY_29
## TestCase Name
RDKV_CERT_RVS_Cobalt_TrickPlay
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by playing a video in Cobalt and performing trick play operations (pause, play, fast-forward, rewind) for a configured duration, verifying video state transitions and CPU/memory usage remain within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the supported plugins list.|
|3|cobalt_test_url and cobalt_trickplay_duration must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=resumed, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt and start video | Launch Cobalt via `launch_plugin`. Set the video URL via deeplink: `{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":{"url":"<cobalt_test_url>"}}` Send OK key to start playback: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keyCode":13,"modifiers":[],"client":"Cobalt"}}` | Cobalt should launch and start playing the video. |
| 4 | Trick play loop (for cobalt_trickplay_duration) | Repeat for the configured duration: <br>Send pause key: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keyCode":19,"modifiers":[],"client":"Cobalt"}}` <br>Check proc entry to verify video is paused. <br>Send play key: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keyCode":415,"modifiers":[],"client":"Cobalt"}}` <br>Check proc entry to verify video is playing. <br>Send fast-forward key. <br>Send rewind key. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | Trick play operations should be performed successfully. Video state should transition between paused/playing correctly. CPU load and memory usage should remain within expected limits. |
| 5 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all timed measurement data. |
| 6 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 7 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 1460

**Priority** : High

**Release Version** : M88<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
