## TestCase ID
RDKV_STABILITY_12
## TestCase Name
RDKV_CERT_RVS_WiFi_ChannelChange
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability over a WiFi network by monitoring live TV channel changes for a configured test duration, verifying that channel changes complete successfully and CPU/memory usage remains within expected limits throughout.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|webkit_instance plugin must be in resumed state; org.rdk.NetworkManager (or org.rdk.Wifi) and DeviceInfo plugins must be activated.|
|3|channel_change_url and test_duration must be configured in StabilityTestVariables.|
|4|WiFi credentials must be configured in StabilityTestVariables (if device is currently on Ethernet, it will be switched to WiFi).|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of webkit_instance, org.rdk.NetworkManager, and DeviceInfo plugins. Set required states: webkit_instance=resumed, org.rdk.NetworkManager=activated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Check current interface and switch to WiFi if needed | Check the current default network interface via `check_current_interface`. If the device is on Ethernet (eth0): switch to WiFi by connecting to the configured SSID using org.rdk.NetworkManager. | Device should be connected via WiFi interface. |
| 4 | Set channel change URL | Load the channel change test URL in webkit_instance: `{"jsonrpc":"2.0","id":1234567890,"method":"webkit_instance.1.url","params":{"value":"<channel_change_url>"}}` | Channel change URL should be set and webkit_instance should start loading the stream. |
| 5 | Channel change monitoring loop (for test_duration) | For test_duration minutes: <br>Register for channel change events via WebInspect WebSocket (webinspect_port). <br>Monitor for channel change event messages from the webkit_instance. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage` at each interval. | Channel change events should be received. CPU load and memory usage should remain within expected limits throughout the test duration. |
| 6 | Verify webkit_instance is still running | After the test duration, verify webkit_instance remains in "resumed" state. | webkit_instance should remain active throughout the test. |
| 7 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all timed measurement data. |
| 8 | Revert network and plugins | Restore the original network interface (if switched to WiFi) and revert plugins to their original state. | Network settings and plugins should be restored to pre-test state. |
| 9 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the WiFi channel change test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 170

**Priority** : High

**Release Version** : M85<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
