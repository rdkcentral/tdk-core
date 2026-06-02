## TestCase ID
RDKV_STABILITY_08
## TestCase Name
RDKV_CERT_RVS_LongDuration_ChannelChange
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by performing continuous channel changes via webkit_instance for a long duration, verifying CPU and memory usage remains within expected limits throughout the test period.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|webkit_instance plugin must be in resumed state; Cobalt plugin must be deactivated; DeviceInfo plugin must be activated.|
|3|channel_change_url must be configured in StabilityTestVariables; test_streams_base_path must be configured for channels.js; channel_change_duration must be set.|
|4|webinspect_port must be configured in StabilityTestVariables for WebSocket connection to the device's devtools endpoint.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of webkit_instance, Cobalt, and DeviceInfo plugins. Set required states: webkit_instance=resumed, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Configure channels.js | Update the channels.js test application file with `test_streams_base_path` for channel stream URLs. | channels.js should be updated with test stream paths. |
| 4 | Create WebSocket event listener | Connect to the device webinspect port via WebSocket on `/devtools/page/1` using `createEventListener`. | WebSocket connection to webinspect should be established. |
| 5 | Get current URL and set channel change test URL | Retrieve the current URL from webkit_instance. Load the channel change test application: `{"jsonrpc":"2.0","id":1234567890,"method":"webkit_instance.1.url","params":{"value":"<channel_change_url>"}}` | Channel change URL should be set successfully. |
| 6 | Monitor channel changes (for channel_change_duration) | For the configured test duration: <br>Retrieve events from webinspect buffer. <br>Check for "Count" in console log output via `rdkservice_checkChannelChangeLog`. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage` after each detected channel change. | Channel changes should be detected and counted throughout the duration. CPU load and memory usage should remain within expected limits. |
| 7 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all timed measurement data. |
| 8 | Revert URL and plugins | Restore the original URL and revert plugins to their original state. | URL and plugins should be restored to pre-test state. |
| 9 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the long-duration channel change test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 730

**Priority** : High

**Release Version** : M84<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
