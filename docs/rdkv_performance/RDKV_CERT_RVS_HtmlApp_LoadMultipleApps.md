## TestCase ID
RDKV_PERFORMANCE_219
## TestCase Name
RDKV_CERT_RVS_HtmlApp_LoadMultipleApps
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that HtmlApp and multiple other applications can be loaded simultaneously without stability issues in a Retail Validation Scenario.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|HtmlApp and other supported application plugins must be available in the device build.|
|3|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Verify plugin status for HtmlApp and other supported plugins. | Plugin states retrieved. |
| 3 | Launch HtmlApp | Activate HtmlApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"HtmlApp"}}` | HtmlApp launched. |
| 4 | Launch Additional Apps | Activate additional applications alongside HtmlApp. | All applications launched. |
| 5 | Validate All Apps Running | Verify all launched applications are in activated state and functional without crashes. | All apps running simultaneously without crashes. |
| 6 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
