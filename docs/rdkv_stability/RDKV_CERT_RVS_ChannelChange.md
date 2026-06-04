## TestCase ID
RDKV_STABILITY_01
## TestCase Name
RDKV_CERT_RVS_ChannelChange
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by performing channel changes for a configurable number of iterations via webkit_instance, verifying CPU and memory usage remains within expected limits after each channel change.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|webkit_instance plugin must be in resumed state; Cobalt plugin must be deactivated; DeviceInfo plugin must be activated.|
|3|channel_change_url must be configured in StabilityTestVariables; test_streams_base_path must be configured for channels.js.|
|4|webinspect_port must be configured in StabilityTestVariables for WebSocket connection to the device's devtools endpoint.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of webkit_instance, Cobalt, and DeviceInfo plugins via applicable API calls. Set required states: webkit_instance=resumed, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Configure channels.js | Update the channels.js test application file with `test_streams_base_path` for channel stream URLs. | channels.js should be updated with test stream paths. |
| 4 | Create WebSocket event listener | Connect to the device webinspect port via WebSocket on `/devtools/page/1` using `createEventListener` to capture console log events. | WebSocket connection to webinspect should be established. |
| 5 | Get current URL | Retrieve the current URL loaded in webkit_instance.<br>{"jsonrpc":"2.0","id":1234567890,"method":"webkit_instance.1.url"} | Current URL should be retrieved successfully. |
| 6 | Set channel change test URL | Load the channel change test application in webkit_instance.<br>{"jsonrpc":"2.0","id":1234567890,"method":"webkit_instance.1.url","params":{"value":"<channel_change_url>"}} | Channel change URL should be set successfully. |
| 7 | Monitor channel changes (until max_channel_change_count is reached) | While channel change count is less than max_channel_change_count: <br>Retrieve events from the webinspect event buffer via `getEventsBuffer()`. <br>Check for "Count" in console log output using applicable API calls. <br>Increment channel_change_count when a change event is detected. <br>Validate CPU load and memory usage via after each confirmed channel change. <br>Exit monitoring loop if continue_count exceeds 20 (no new events). | Channel changes should be detected in the console log. CPU load and memory usage should remain within limits per iteration. |
| 8 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with iteration data. |
| 9 | Revert URL | Restore the original URL in webkit_instance. | Original URL should be restored. |
| 10 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 11 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 168

**Priority** : High

**Release Version** : M82<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
