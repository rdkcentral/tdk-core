## TestCase ID
RDKV_STABILITY_55
## TestCase Name
RDKV_CERT_RVS_LightningApp_SetURLAndExit
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate LightningApp stability by repeatedly launching the plugin, setting an app URL, verifying the URL, and destroying the plugin for launch_and_destroy_max_count iterations, verifying CPU and memory usage remains within expected limits.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|LightningApp plugin must be available in the supported plugins list.|
|3|ip_change_app_url and launch_and_destroy_max_count must be configured in StabilityTestVariables.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of LightningApp, Cobalt, and DeviceInfo plugins. Set required states: LightningApp=deactivated, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Set URL and exit loop (repeat for launch_and_destroy_max_count iterations) | For each iteration: <br>Launch LightningApp via `org.rdk.RDKShell.1.launch`. <br>Set app URL: `{"jsonrpc":"2.0","id":1234567890,"method":"LightningApp.1.url","params":{"value":"<ip_change_app_url>"}}` <br>Verify URL is set correctly by getting the current URL. <br>Destroy LightningApp via `org.rdk.RDKShell.1.destroy`. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | LightningApp should launch, load URL, and be destroyed successfully in each iteration. URL should be verified correctly. CPU load and memory usage should remain within expected limits. |
| 4 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 5 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 6 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the set URL and exit stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-HYB, RPI-Client, Video_Accelerator

**Estimated duration** : 840

**Priority** : High

**Release Version** : M94<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
