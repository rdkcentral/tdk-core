## TestCase ID
RDKV_STABILITY_35
## TestCase Name
RDKV_CERT_RVS_FastChannelChange
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by performing 1000 fast channel change operations via webkit_instance, verifying video playback resumes after each change and CPU/memory usage remains within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|webkit_instance plugin must be in resumed state; Cobalt plugin must be deactivated; DeviceInfo plugin must be activated.|
|3|fast_channel_change_url must be configured in StabilityTestVariables pointing to a FastChannelChangeTest.html application.|
|4|webinspect_port must be configured in StabilityTestVariables for WebSocket connection to the device's devtools endpoint.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of webkit_instance, Cobalt, and DeviceInfo plugins. Set required states: webkit_instance=resumed, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Create WebSocket event listener | Connect to the device webinspect port via WebSocket on `/devtools/page/1` using `createEventListener` to capture console log events. | WebSocket connection to webinspect should be established. |
| 4 | Set fast channel change test URL | Load the FastChannelChangeTest.html application in webkit_instance.<br>{"jsonrpc":"2.0","id":1234567890,"method":"webkit_instance.1.url","params":{"value":"<fast_channel_change_url>"}} | Fast channel change URL should be set. |
| 5 | Monitor fast channel changes (until 1000 changes completed) | Loop until 1000 channel changes are counted: <br>Retrieve events from the webinspect event buffer via `getEventsBuffer()`. <br>Check for "Count" in console log output via applicable API calls. <br>Increment channel_change_count when a change event is detected. <br>Continue without delay (fast changes). <br>Validate CPU load and memory usage via after each confirmed change. | 1000 fast channel changes should complete. CPU load and memory usage should remain within expected limits throughout. |
| 6 | Validate video playback after stress | Check for "CHECK PLAYING" event in the webinspect event buffer to verify video playback is confirmed after 1000 fast channel changes. | "CHECK PLAYING" event should be present, confirming video playback after the fast channel change stress. |
| 7 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 8 | Revert URL | Restore the original URL in webkit_instance. | Original URL should be restored. |
| 9 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 10 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the fast channel change stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 600

**Priority** : High

**Release Version** : M88<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
