## TestCase ID
RDKV_STABILITY_18
## TestCase Name
RDKV_CERT_RVS_Cobalt_VideoPlayback_StandbyToOn
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by playing a video in Cobalt and repeatedly toggling the device between standby and on states, verifying video playback resumes after each power state change and CPU/memory usage remains within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt and org.rdk.System plugins must be available in the supported plugins list.|
|3|cobalt_test_url and max_power_state_changes must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=resumed, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt and start video | Launch Cobalt via applicable API calls. Set the video URL via deeplink: `{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":{"url":"<cobalt_test_url>"}}` | Cobalt should launch and start playing the video. |
| 4 | Standby-to-On loop (repeat for max_power_state_changes iterations) | For each iteration: <br>Set preferred standby mode to LIGHT SLEEP: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPreferredStandbyMode","params":{"standbyMode":"LIGHT_SLEEP"}}` <br>Set device to standby (power state OFF): `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"STANDBY","standbyReason":"TDKTest"}}` <br>Set device power state back to ON: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"ON","standbyReason":"TDKTest"}}` <br>Verify video is still playing via applicable API calls. <br>Validate CPU load and memory usage via applicable API calls. | Power state transitions should complete successfully. Video playback should resume after ON state. CPU load and memory usage should remain within expected limits. |
| 5 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 6 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 7 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 3000

**Priority** : High

**Release Version** : M86<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
