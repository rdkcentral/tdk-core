## TestCase ID
RDKV_STABILITY_22
## TestCase Name
RDKV_CERT_RVS_DeviceSpecificPlugins_ActivateDeactivate
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by repeatedly activating and deactivating device-specific plugins (org.rdk.ScreenCapture and DisplayInfo) for activate_deactivate_max_count iterations, verifying CPU and memory usage remains within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|org.rdk.ScreenCapture and DisplayInfo plugins must be available in the SUPPORTED_PLUGINS list in the device config.|
|3|DeviceInfo plugin must be activated for resource usage validation.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using applicable API calls. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of DeviceInfo plugin via applicable API calls. Activate DeviceInfo if not already active. | DeviceInfo plugin should be activated. |
| 3 | Get supported plugins list | Get the list of supported plugins on the device via to determine which of the device-specific plugins (org.rdk.ScreenCapture, DisplayInfo) are available. | Supported plugins list should be retrieved. |
| 4 | Activate-Deactivate loop (repeat for activate_deactivate_max_count iterations for each plugin) | For each iteration and for each supported device-specific plugin: <br>Activate the plugin via : `{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"<plugin>"}}` <br>Verify plugin status is "activated" via applicable API calls. <br>Deactivate the plugin via : `{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"<plugin>"}}` <br>Verify plugin status is "deactivated" via applicable API calls. <br>Validate CPU load and memory usage via applicable API calls. | Plugin should activate and deactivate successfully in each iteration. CPU load and memory usage should remain within expected limits. |
| 5 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 6 | Revert plugins | Restore plugins to their original state using applicable API calls. | Plugins should be reverted to their pre-test states. |
| 7 | Check device state post-condition | Verify the device is still in a stable state after completing the test using applicable API calls. | Device should remain stable after the activate/deactivate stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video_Accelerator

**Estimated duration** : 720

**Priority** : High

**Release Version** : M87<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
