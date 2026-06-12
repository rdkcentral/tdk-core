## TestCase ID
RDKV_PERFORMANCE_90
## TestCase Name
RDKV_CERT_PVS_Functional_HtmlApp_LifeCycleManagement
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the complete lifecycle management of the HtmlApp plugin including activation, suspension, resumption, and deactivation.

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
| 2 | Check Initial Plugin Status | Query initial state of HtmlApp: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@HtmlApp"}` | Initial status retrieved. |
| 3 | Activate HtmlApp | Activate the HtmlApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"HtmlApp"}}` | HtmlApp activated. |
| 4 | Suspend HtmlApp | Suspend the HtmlApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.suspend","params":{"callsign":"HtmlApp"}}` | HtmlApp suspended. |
| 5 | Resume HtmlApp | Resume the HtmlApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.resume","params":{"callsign":"HtmlApp"}}` | HtmlApp resumed. |
| 6 | Deactivate HtmlApp | Deactivate the HtmlApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"HtmlApp"}}` | HtmlApp deactivated. |
| 7 | Validate Lifecycle | Verify each lifecycle state transition completed successfully. | All lifecycle transitions (activate, suspend, resume, deactivate) are successful. |
| 8 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M95<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
