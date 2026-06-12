## TestCase ID
RDKV_PERFORMANCE_72
## TestCase Name
RDKV_CERT_PVS_Functional_HtmlApp_TimeTo_Launch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to launch the HtmlApp plugin is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|HtmlApp plugin should be available in the device build.|
|3|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Record Launch Start Time | Record UTC timestamp before activating HtmlApp. | Start time recorded. |
| 3 | Activate HtmlApp | Activate HtmlApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"HtmlApp"}}` | HtmlApp activated. |
| 4 | Record Launch End Time | Record UTC timestamp after HtmlApp is activated. | End time recorded. |
| 5 | Calculate and Validate Launch Time | Calculate launch time = end timestamp - start timestamp. Compare against threshold. | Time to launch HtmlApp is within the expected threshold. |
| 6 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 3

**Priority** : High

**Release Version** : M94<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
