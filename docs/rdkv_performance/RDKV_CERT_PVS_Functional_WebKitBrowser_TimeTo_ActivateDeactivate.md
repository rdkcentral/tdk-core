## TestCase ID
RDKV_PERFORMANCE_13
## TestCase Name
RDKV_CERT_PVS_Functional_WebKitBrowser_TimeTo_ActivateDeactivate
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to activate and deactivate the WebKitBrowser plugin is within the expected performance thresholds.

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
| 2 | Record Activate Start Time | Record UTC timestamp before activating WebKitBrowser. | Start time recorded. |
| 3 | Activate WebKitBrowser | Activate WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"WebKitBrowser"}}` | WebKitBrowser activated. |
| 4 | Record Activate End Time | Record UTC timestamp after WebKitBrowser is activated. | Activation end time recorded. |
| 5 | Record Deactivate Start Time | Record UTC timestamp before deactivating WebKitBrowser. | Start time recorded. |
| 6 | Deactivate WebKitBrowser | Deactivate WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"WebKitBrowser"}}` | WebKitBrowser deactivated. |
| 7 | Record Deactivate End Time | Record UTC timestamp after WebKitBrowser is deactivated. | Deactivation end time recorded. |
| 8 | Validate Times | Compare activate and deactivate times against their respective thresholds. | Time to activate and deactivate WebKitBrowser are within the expected thresholds. |
| 9 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 4

**Priority** : High

**Release Version** : M84<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
