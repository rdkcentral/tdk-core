## TestCase ID
RDKV_PERFORMANCE_98
## TestCase Name
RDKV_CERT_PVS_Functional_ResourceUsage_OnPluginsLaunch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that CPU load and memory usage are within acceptable ranges when multiple plugins are launched simultaneously on the device.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|The plugins to be tested should be available in the device build.|
|3|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Capture Baseline Resource Usage | Record CPU and memory usage before plugin launches. | Baseline recorded. |
| 3 | Launch Plugins | Activate the configured set of plugins using `Controller.1.activate` for each. | All plugins launched. |
| 4 | Capture Resource Usage After Launch | Record CPU and memory usage after all plugins are launched. | Resource data captured. |
| 5 | Validate Resource Usage | Verify CPU load and memory usage during simultaneous plugin launch are within acceptable limits. | CPU load and memory usage with all plugins launched are within the expected limits. |
| 6 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 4

**Priority** : High

**Release Version** : M96<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
