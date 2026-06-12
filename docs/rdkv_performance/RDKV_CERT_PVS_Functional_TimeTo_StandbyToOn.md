## TestCase ID
RDKV_PERFORMANCE_24
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_StandbyToOn
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken for the device to transition from Standby to On power state is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.System` plugin must be available for power state management.|
|3|`STANDBY_TO_ON_THRESHOLD` must be configured in device config.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Set Device to Standby | Set power state to Standby: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"STANDBY","standbyReason":"TDKTest"}}` | Device in Standby state. |
| 3 | Record Transition Start Time | Record UTC timestamp before issuing On command. | Start time recorded. |
| 4 | Set Device to On | Transition device to On state: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.setPowerState","params":{"powerState":"ON","standbyReason":""}}` | On command sent. |
| 5 | Record On Reached Time | Record UTC timestamp when device reaches On state. | End time recorded. |
| 6 | Validate Time | Calculate transition time = end timestamp - start timestamp. Compare against threshold. | Time to transition from Standby to On is within the expected threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M85<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
