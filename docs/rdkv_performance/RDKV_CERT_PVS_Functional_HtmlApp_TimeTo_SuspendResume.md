## TestCase ID
RDKV_PERFORMANCE_79
## TestCase Name
RDKV_CERT_PVS_Functional_HtmlApp_TimeTo_SuspendResume
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to suspend and resume the HtmlApp plugin is within the expected performance threshold.

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
| 2 | Activate HtmlApp | Activate HtmlApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.activate","params":{"callsign":"HtmlApp"}}` | HtmlApp activated. |
| 3 | Record Suspend Start Time | Record UTC timestamp before suspending. | Start time recorded. |
| 4 | Suspend HtmlApp | Suspend HtmlApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.suspend","params":{"callsign":"HtmlApp"}}` | HtmlApp suspended. |
| 5 | Record Suspend End / Resume Start Time | Record suspend end timestamp and immediately start resume. | Times recorded. |
| 6 | Resume HtmlApp | Resume HtmlApp plugin: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"Controller.1.resume","params":{"callsign":"HtmlApp"}}` | HtmlApp resumed. |
| 7 | Record Resume End Time | Record UTC timestamp after resume completes. | End time recorded. |
| 8 | Validate Suspend/Resume Times | Calculate suspend time and resume time separately. Compare against thresholds. | Suspend and resume times for HtmlApp are within expected thresholds. |
| 9 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 4

**Priority** : High

**Release Version** : M94<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
