## TestCase ID
RDKV_PERFORMANCE_108
## TestCase Name
RDKV_CERT_PVS_Functional_TimeTo_GetKeys
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the time taken to get key events from the remote control is within the expected performance threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|`org.rdk.RDKShell` plugin must be available.|
|3|Remote control input must be available and configured.|
|4|`GET_KEYS_THRESHOLD` must be configured in device config.|
|5|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Record Start Time | Record UTC timestamp before generating a key event. | Start time recorded. |
| 3 | Generate Key Event | Send a key event to RDKShell: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"org.rdk.RDKShell.1.generateKey","params":{"keyCode":<code>,"modifiers":[],"client":"<client>"}}` | Key event sent. |
| 4 | Record Key Received Time | Record UTC timestamp when the key event is received by the application. | End time recorded. |
| 5 | Validate Time | Calculate key event time = end timestamp - start timestamp. Compare against threshold. | Time to get key events is within the expected threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 7

**Priority** : High

**Release Version** : M98<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
