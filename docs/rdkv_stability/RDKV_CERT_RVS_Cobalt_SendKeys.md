## TestCase ID
RDKV_STABILITY_06
## TestCase Name
RDKV_CERT_RVS_Cobalt_SendKeys
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by launching Cobalt to play a video and continuously sending random key events for a configured duration, verifying the video remains playing and CPU/memory usage stays within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the supported plugins list.|
|3|cobalt_randomkey_test_url (a long-duration video URL) and cobalt_randomkey_test_duration must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=resumed, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt and start video | Launch Cobalt via `launch_plugin` using `org.rdk.RDKShell.1.launch`. Set the long-duration video URL: `{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":{"url":"<cobalt_randomkey_test_url>"}}` | Cobalt should launch and start playing the video. |
| 4 | Send random keys loop (for cobalt_randomkey_test_duration) | Every 5 seconds for the configured test duration: <br>Send random key events to Cobalt via `org.rdk.RDKShell.1.generateKey`: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keyCode":<random_key>,"modifiers":[],"client":"Cobalt"}}` <br>Validate that video is still playing via `rdkservice_validateProcEntry`. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | Random key events should be delivered successfully. Video should continue playing. CPU load and memory usage should remain within expected limits. |
| 5 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all timed measurement data. |
| 6 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 7 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 620

**Priority** : High

**Release Version** : M83<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
