## TestCase ID
RDKV_PERFORMANCE_46
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_MoveToFrontAndBack
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to move an application to the front and back within the RDKShell display stack is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.RDKShell` plugin must be available in the device build.|
|3|Target application plugin must be launched.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Launch Application | Activate the target plugin. | Application launched. |
| 3 | Record Move to Front Start Time | Record UTC timestamp before moving application to front. | Start time recorded. |
| 4 | Move Application to Front | Send move to front request: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.moveToFront","params":{"client":"<client>"}}` | Move to front request sent. |
| 5 | Record Move to Front End Time | Record UTC timestamp after completion. | End time recorded. |
| 6 | Record Move to Back Start Time | Record UTC timestamp before moving application to back. | Start time recorded. |
| 7 | Move Application to Back | Send move to back request: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.moveToBack","params":{"client":"<client>"}}` | Move to back request sent. |
| 8 | Record Move to Back End Time | Record UTC timestamp after completion. | End time recorded. |
| 9 | Validate Times | Calculate move-to-front and move-to-back times. Compare against thresholds. | Times to move application to front and back are within the expected thresholds. |
| 10 | Revert Plugin Status | Restore original plugin state. | Plugin reverted to original state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M89<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
