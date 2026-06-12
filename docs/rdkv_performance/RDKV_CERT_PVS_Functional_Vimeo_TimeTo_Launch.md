## TestCase ID
RDKV_PERFORMANCE_127
## TestCase Name
RDKV_CERT_PVS_Functional_Vimeo_TimeTo_Launch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to launch the Vimeo application is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|The application plugin used for Vimeo must be available in the build.|
|3|Vimeo app URL must be configured in `PerformanceTestVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Record Launch Start Time | Record UTC timestamp before activating the Vimeo application. | Start time recorded. |
| 3 | Launch Vimeo Application | Activate the plugin and navigate to the Vimeo URL. | Vimeo launch initiated. |
| 4 | Record Launch End Time | Record UTC timestamp when Vimeo is fully loaded and active. | End time recorded. |
| 5 | Validate Time | Calculate launch time = end timestamp - start timestamp. Compare against threshold. | Time to launch Vimeo is within the expected threshold. |
| 6 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 6

**Priority** : High

**Release Version** : M104<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
