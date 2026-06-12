## TestCase ID
RDKV_PERFORMANCE_57
## TestCase Name
RDKV_CERT_PVS_Functional_WebKitBrowser_LifeCycleManagement
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate the complete lifecycle management of the WebKitBrowser plugin including activation, suspension, resumption, and deactivation.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin should be available in the device build.|
|3|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Initial Plugin Status | Query initial state of WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@WebKitBrowser"}` | Initial status retrieved. |
| 3 | Activate WebKitBrowser | Activate the WebKitBrowser plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"WebKitBrowser"}}` | WebKitBrowser activated. |
| 4 | Suspend WebKitBrowser | Suspend the WebKitBrowser plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.suspend","params":{"callsign":"WebKitBrowser"}}` | WebKitBrowser suspended. |
| 5 | Resume WebKitBrowser | Resume the WebKitBrowser plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.resume","params":{"callsign":"WebKitBrowser"}}` | WebKitBrowser resumed. |
| 6 | Deactivate WebKitBrowser | Deactivate the WebKitBrowser plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"WebKitBrowser"}}` | WebKitBrowser deactivated. |
| 7 | Validate Lifecycle | Verify each lifecycle state transition completed successfully. | All lifecycle transitions (activate, suspend, resume, deactivate) are successful. |
| 8 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M91<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
