## TestCase ID
RDKV_PERFORMANCE_59
## TestCase Name
RDKV_CERT_PVS_Functional_Cobalt_WebKitBrowser_Switch
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that switching between Cobalt and WebKitBrowser plugins functions correctly without any crash or instability.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|Cobalt and WebKitBrowser plugins should be available in the build.|
|3|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Check Initial Plugin Status | Retrieve initial states for Cobalt and WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.status@Cobalt"}` | Initial status retrieved. |
| 3 | Launch WebKitBrowser | Activate WebKitBrowser: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"WebKitBrowser"}}` | WebKitBrowser activated. |
| 4 | Switch to Cobalt | Deactivate WebKitBrowser, activate Cobalt: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"Cobalt"}}` | Cobalt activated while WebKitBrowser deactivated. |
| 5 | Switch Back to WebKitBrowser | Deactivate Cobalt, reactivate WebKitBrowser. | WebKitBrowser reactivated. |
| 6 | Validate Stability | Verify both plugins are functional after switching. | Both plugins work correctly; no crashes observed during switching. |
| 7 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M91<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
