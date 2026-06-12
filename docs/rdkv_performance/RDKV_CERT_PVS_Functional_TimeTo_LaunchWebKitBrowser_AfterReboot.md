## TestCase ID
RDKV_PERFORMANCE_68
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_LaunchWebKitBrowser_AfterReboot
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to launch WebKitBrowser after a device reboot is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser plugin must be available in the device build.|
|3|`WEBKIT_LAUNCH_AFTER_REBOOT_THRESHOLD` must be configured in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Record Start Time | Record UTC timestamp when device reboot is initiated via `Controller.1.harakiri`. | Start time recorded. |
| 2 | Reboot Device | Reboot the device. | Device rebooting. |
| 3 | Wait for Device to Come Online | Wait for WPEFramework to come back online. | Device online. |
| 4 | Record WebKitBrowser Launch Start Time | Record UTC timestamp before activating WebKitBrowser. | Start time recorded. |
| 5 | Activate WebKitBrowser | Activate WebKitBrowser plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"WebKitBrowser"}}` | WebKitBrowser activated. |
| 6 | Record Launch End Time | Record UTC timestamp when WebKitBrowser is fully active. | End time recorded. |
| 7 | Validate Time | Calculate launch time = end timestamp - start timestamp (from post-reboot launch). Compare against threshold. | Time to launch WebKitBrowser after reboot is within the expected threshold. |
| 8 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 7

**Priority** : High

**Release Version** : M93<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
