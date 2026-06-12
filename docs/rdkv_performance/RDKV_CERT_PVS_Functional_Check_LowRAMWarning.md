## TestCase ID
RDKV_PERFORMANCE_140
## TestCase Name
RDKV_CERT_PVS_Functional_Check_LowRAMWarning
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the `onDeviceLowRamWarning` and `onDeviceCriticallyLowRamWarning` events are triggered when multiple plugins are launched and destroyed on the device.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|WebKitBrowser, Cobalt, and DeviceInfo plugins should be available in the build.|
|3|`org.rdk.DeviceDiagnostics` or equivalent RAM monitoring plugin must be present.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Subscribe to RAM Warning Events | Subscribe to `onDeviceLowRamWarning` and `onDeviceCriticallyLowRamWarning` events. | Event subscriptions established. |
| 3 | Launch Multiple Plugins | Activate multiple plugins in sequence (WebKitBrowser, Cobalt, etc.) to consume RAM: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"WebKitBrowser"}}` | Multiple plugins launched. |
| 4 | Destroy Plugins | Deactivate and destroy the plugins: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.deactivate","params":{"callsign":"WebKitBrowser"}}` | Plugins destroyed. |
| 5 | Validate RAM Warning Events | Check event buffers for `onDeviceLowRamWarning` and `onDeviceCriticallyLowRamWarning` events. | Low RAM warning events are triggered when memory is low during plugin lifecycle operations. |
| 6 | Revert Plugin Status | Restore original plugin states. | Plugins reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M111<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
