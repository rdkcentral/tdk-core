## TestCase ID
RDKV_PERFORMANCE_67
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_UserFactory_ResetDevice
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to perform a user factory reset of the device is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.System` plugin must be available.|
|3|`USER_FACTORY_RESET_THRESHOLD` must be configured in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Record Start Time | Record UTC timestamp before issuing the factory reset command. | Start time recorded. |
| 2 | Initiate User Factory Reset | Issue user factory reset command: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.System.1.resetToFactory","params":{"resetType":"userFactoryReset"}}` | Factory reset initiated. |
| 3 | Wait for Device to Come Online | Monitor the device until it completes reset and WPEFramework is back online. | Device reset complete and online. |
| 4 | Record Reset Complete Time | Record UTC timestamp when the device is fully operational after reset. | End time recorded. |
| 5 | Validate Time | Calculate reset time = end timestamp - start timestamp. Compare against threshold. | Time to perform user factory reset is within the expected threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M92<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
