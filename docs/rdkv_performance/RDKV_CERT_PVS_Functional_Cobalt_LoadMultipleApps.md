## TestCase ID
RDKV_PERFORMANCE_214
## TestCase Name
RDKV_CERT_PVS_Functional_Cobalt_LoadMultipleApps
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that Cobalt and other applications can be launched simultaneously without affecting system stability or application functionality.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt, WebKitBrowser, and other supported plugins should be available in the build.|
|3|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Plugin Status | Verify plugin status for Cobalt and other supported plugins. | Plugin states retrieved. |
| 3 | Launch Cobalt | Activate and launch Cobalt: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"Cobalt"}}` | Cobalt launched. |
| 4 | Launch Additional Apps | Activate additional applications (e.g., WebKitBrowser, LightningApp) alongside Cobalt. | All applications launched. |
| 5 | Validate All Apps Running | Verify all launched applications are in activated state and functional. | All apps running simultaneously without crashes. |
| 6 | Revert Plugin Status | Restore original plugin states for all launched plugins. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M148<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
