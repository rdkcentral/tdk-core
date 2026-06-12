## TestCase ID
RDKV_PERFORMANCE_80
## TestCase Name
RDKV_CERT_PVS_Functional_LightningApp_TimeTo_SuspendResume
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to suspend and resume the LightningApp plugin is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|LightningApp plugin should be available in the device build.|
|3|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Activate LightningApp | Activate LightningApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"LightningApp"}}` | LightningApp activated. |
| 3 | Record Suspend Start Time | Record UTC timestamp before suspending. | Start time recorded. |
| 4 | Suspend LightningApp | Suspend LightningApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.suspend","params":{"callsign":"LightningApp"}}` | LightningApp suspended. |
| 5 | Record Suspend End / Resume Start Time | Record suspend end timestamp. | Times recorded. |
| 6 | Resume LightningApp | Resume LightningApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.resume","params":{"callsign":"LightningApp"}}` | LightningApp resumed. |
| 7 | Record Resume End Time | Record UTC timestamp after resume completes. | End time recorded. |
| 8 | Validate Suspend/Resume Times | Calculate suspend time and resume time. Compare against thresholds. | Suspend and resume times for LightningApp are within expected thresholds. |
| 9 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 4

**Priority** : High

**Release Version** : M94<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
