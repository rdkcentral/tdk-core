## TestCase ID
RDKV_STABILITY_45
## TestCase Name
RDKV_CERT_RVS_WebKitBrowser_LaunchAndDestroy
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate WebKitBrowser stability by continuously launching and destroying the plugin for launch_and_destroy_max_count iterations, verifying CPU and memory usage remains within expected limits after each iteration.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin must be available in the supported plugins list.|
|3|Cobalt plugin must be deactivated; DeviceInfo must be activated.|
|4|launch_and_destroy_max_count must be configured in StabilityTestVariables.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes`.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Check device state | Verify the device is in a stable state before starting the test using `check_device_state`. | Device should be in healthy state. |
| 2 | Check and set plugin preconditions | Get the status of WebKitBrowser, Cobalt, and DeviceInfo plugins. Set required states: WebKitBrowser=deactivated, Cobalt=deactivated, DeviceInfo=activated. | All required plugins should be in their expected states. |
| 3 | Launch and destroy loop (repeat for launch_and_destroy_max_count iterations) | For each iteration: <br>Launch WebKitBrowser via `rdkservice_launchAndDestroy`: launch via `org.rdk.RDKShell.1.launch` → verify activated → destroy via `org.rdk.RDKShell.1.destroy` → verify deactivated. <br>Validate CPU load and memory usage via `rdkservice_validateResourceUsage`. | WebKitBrowser should launch and be destroyed successfully in each iteration. CPU load and memory usage should remain within expected limits. |
| 4 | Save CPU/memory data | Save the collected CPU and memory usage data to a JSON file (`CPUMemoryInfo.json`) for post-analysis. | JSON file should be saved with all iteration data. |
| 5 | Revert plugins | Restore plugins to their original state using `rdkservice_setPluginStatus`. | Plugins should be reverted to their pre-test states. |
| 6 | Check device state post-condition | Verify the device is still in a stable state after completing the test using `check_device_state`. | Device should remain stable after the launch/destroy stress test. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-HYB, RPI-Client, Video_Accelerator

**Estimated duration** : 360

**Priority** : High

**Release Version** : M93<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
