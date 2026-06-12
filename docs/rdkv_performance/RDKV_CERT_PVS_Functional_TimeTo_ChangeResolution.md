## TestCase ID
RDKV_PERFORMANCE_97
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_ChangeResolution
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to change the display resolution is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.RDKShell` plugin should be available for resolution control.|
|3|Target resolution must be configured in `PerformanceTestVariables`.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Record Start Time | Record UTC timestamp before sending the resolution change request. | Start time recorded. |
| 3 | Change Resolution | Send resolution change request: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.setResolution","params":{"client":"","w":<width>,"h":<height>}}` | Resolution change request sent. |
| 4 | Record End Time | Record UTC timestamp after resolution change completes. | End time recorded. |
| 5 | Validate Time | Calculate time to change resolution = end timestamp - start timestamp. Compare against threshold. | Time to change resolution is within the expected threshold. |
| 6 | Revert Resolution | Restore the original display resolution. | Resolution reverted. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 5

**Priority** : High

**Release Version** : M96<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
