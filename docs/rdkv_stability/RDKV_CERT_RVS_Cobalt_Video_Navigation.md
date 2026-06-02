## TestCase ID
RDKV_STABILITY_56
## TestCase Name
RDKV_CERT_RVS_Cobalt_Video_Navigation
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate Cobalt navigation stability by sending 1000 key navigation events and verifying the device remains stable with CPU and memory usage within expected limits throughout.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt plugin must be available in the supported plugins list.|
|3|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of Cobalt, WebKitBrowser, and DeviceInfo plugins. Set required states: Cobalt=resumed, WebKitBrowser=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch Cobalt | Launch Cobalt via `launch_plugin` using `org.rdk.RDKShell.1.launch`. | Cobalt should launch successfully. |
| 4 | Navigation loop (100 outer iterations × 10 key navigations) | For each of 100 outer iterations: <br>Send 10 navigation key events to Cobalt via `org.rdk.RDKShell.1.generateKey` (arrow keys for navigation). <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | Navigation key events should be delivered successfully. CPU load and memory usage should remain within expected limits throughout the 1000 total key events. |
| 5 | Destroy Cobalt | Destroy Cobalt via `org.rdk.RDKShell.1.destroy`. | Cobalt should be destroyed successfully. |
| 6 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 7 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 8 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the navigation stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 60

**Priority** : High

**Release Version** : M94<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
