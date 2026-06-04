## TestCase ID
RDKV_STABILITY_85
## TestCase Name
RDKV_CERT_RVS_Cobalt_LongDuration_Encrypted_VideoPlayback
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by playing an encrypted video from Cobalt for a configured duration, measuring CPU load and memory usage every 5 minutes to ensure resources remain within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available and activated; all other plugins must be deactivated.|
|3|cobalt_test_url (encrypted video stream URL) and cobalt_test_duration must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=resumed, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt | Launch Cobalt using via `org.rdk.RDKShell.1.launch`. | Cobalt should launch successfully. |
| 4 | Set encrypted video URL | Set the configured encrypted video URL in Cobalt using the deeplink method.<br>{"jsonrpc":"2.0","id":1234567890,"method":"Cobalt.1.deeplink","params":{"url":"<cobalt_encrypted_url>"}} | Encrypted video URL should be set and Cobalt should start loading/decrypting and playing the video. |
| 5 | Validate video playback | Verify that the encrypted video is playing by checking decoder process entries via applicable API calls. | Video should be playing (video decoder proc entry should be present). |
| 6 | Monitor resource usage (every 300 seconds for cobalt_test_duration) | Every 5 minutes for the configured test duration: <br>Validate CPU load and memory usage via using DeviceInfo.1.systeminfo. <br>Verify encrypted video is still playing by re-checking the proc entry for video decoder. | CPU load and memory usage should remain within expected limits. Encrypted video should play without interruption. |
| 7 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all timed measurement data. |
| 8 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 9 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the long-duration test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 740

**Priority** : High

**Release Version** : M101<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
