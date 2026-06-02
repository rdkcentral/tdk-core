## TestCase ID
RDKV_STABILITY_44
## TestCase Name
RDKV_CERT_RVS_ResidentApp_Navigation
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate ResidentApp navigation stability by repeatedly sending key navigation sequences to the ResidentApp for a configured test duration, verifying CPU and memory usage remains within expected limits throughout.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|ResidentApp plugin must be in resumed state (in front of z-order); DeviceInfo plugin must be activated.|
|3|navigation_key_sequence and navigation_test_duration must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of ResidentApp and DeviceInfo plugins. Set required states: ResidentApp=resumed, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Ensure ResidentApp is in front | Get the z-order via `org.rdk.RDKShell.1.getZOrder`. If ResidentApp is not at the front of the z-order: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.moveToFront","params":{"client":"ResidentApp"}}` | ResidentApp should be at the front of the z-order. |
| 4 | Navigation loop (for navigation_test_duration minutes) | While navigation_test_duration minutes has not elapsed: <br>For each key in navigation_key_sequence: <br>Send key event to ResidentApp via `org.rdk.RDKShell.1.generateKey`: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keyCode":<key>,"modifiers":[],"client":"ResidentApp"}}` <br>After each full navigation_key_sequence cycle: Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | Navigation key events should be delivered successfully. CPU load and memory usage should remain within expected limits throughout the navigation test duration. |
| 5 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all timed measurement data. |
| 6 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 7 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the navigation stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-HYB, RPI-Client, Video_Accelerator

**Estimated duration** : 610

**Priority** : High

**Release Version** : M92<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
