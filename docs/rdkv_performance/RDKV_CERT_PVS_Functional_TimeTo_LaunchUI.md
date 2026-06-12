## TestCase ID
RDKV_PERFORMANCE_52
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_LaunchUI
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to launch the main user interface (UI) after device boot is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|The main UI application must be configured in the build.|
|3|`LAUNCH_UI_THRESHOLD` must be configured in device config.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Record Start Time | Record UTC timestamp when device reboot is initiated via `Controller.1.harakiri`. | Start time recorded. |
| 2 | Reboot Device | Reboot the device to trigger UI launch sequence. | Device begins rebooting. |
| 3 | Wait for UI Launch | Monitor the device until the main UI is visible/active. | Main UI launched. |
| 4 | Record UI Launch Time | Record UTC timestamp when the main UI is displayed. | End time recorded. |
| 5 | Validate Time | Calculate UI launch time = end timestamp - start timestamp. Compare against threshold. | Time to launch main UI on device boot is within the expected threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 30

**Priority** : High

**Release Version** : M90<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
