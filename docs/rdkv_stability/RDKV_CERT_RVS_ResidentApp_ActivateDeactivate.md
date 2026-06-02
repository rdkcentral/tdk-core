## TestCase ID
RDKV_STABILITY_15
## TestCase Name
RDKV_CERT_RVS_ResidentApp_ActivateDeactivate
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate device stability by repeatedly activating and deactivating the ResidentApp plugin for activate_deactivate_max_count iterations, verifying that the app launches and destroys correctly and CPU/memory usage remains within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|ResidentApp plugin must be available in the supported plugins list.|
|3|DeviceInfo plugin must be activated for resource usage validation.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of ResidentApp and DeviceInfo plugins. Activate DeviceInfo if not already active. Get the ResidentApp URL for launching. | DeviceInfo should be activated. ResidentApp URL should be retrieved. |
| 3 | Activate-Deactivate loop (repeat for activate_deactivate_max_count iterations) | For each iteration: <br>If ResidentApp is deactivated: Launch via `org.rdk.RDKShell.1.launch` with URL: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.launch","params":{"callsign":"ResidentApp","type":"ResidentApp","uri":"<resident_app_url>"}}` Verify status is "activated/resumed". <br>If ResidentApp is activated: Destroy via `org.rdk.RDKShell.1.destroy`: `{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.destroy","params":{"callsign":"ResidentApp"}}` Verify status is "deactivated". <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | ResidentApp should activate and deactivate successfully in each iteration. CPU load and memory usage should remain within expected limits. |
| 4 | Verify ResidentApp URL after loop | After completing the activate/deactivate loop, verify ResidentApp is running with the correct URL. | ResidentApp should be running with the expected URL. |
| 5 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 6 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 7 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the activate/deactivate stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, RPI-HYB, Video_Accelerator

**Estimated duration** : 600

**Priority** : High

**Release Version** : M86<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
