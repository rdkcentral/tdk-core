## TestCase ID
RDKV_PERFORMANCE_103
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_OnToStandby
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken for the device to transition from On to Standby power state is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.System` plugin must be available for power state management.|
|3|`ON_TO_STANDBY_THRESHOLD` must be configured in device config.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Ensure Device is in On State | Verify device power state is On: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.getPowerState"}` | Device confirmed in On state. |
| 3 | Record Transition Start Time | Record UTC timestamp before issuing Standby command. | Start time recorded. |
| 4 | Set Device to Standby | Set power state to Standby: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"STANDBY","standbyReason":"TDKTest"}}` | Standby command sent. |
| 5 | Record Standby Reached Time | Record UTC timestamp when device reaches Standby state. | End time recorded. |
| 6 | Validate Time | Calculate transition time = end timestamp - start timestamp. Compare against threshold. | Time to transition from On to Standby is within the expected threshold. |
| 7 | Restore Device to On | Transition device back to On state. | Device restored to On state. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M98<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
