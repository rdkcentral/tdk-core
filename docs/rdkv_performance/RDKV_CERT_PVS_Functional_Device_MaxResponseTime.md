## TestCase ID
RDKV_PERFORMANCE_145
## TestCase Name
RDKV_CERT_PVS_Functional_Device_MaxResponseTime
<a name="head.TOC"></a>
## Table Of Contents
- [Objective](#head.Objective)
- [Precondition](#head.Precondition)
- [Test Steps](#head.TestSteps)
- [Test Attributes](#head.Attributes)

<a name="head.Objective"></a>
## Objective
To validate that the maximum response time for getting device information is within the expected threshold.

<a name="head.Precondition"></a>
## Preconditions
|#|Conditions|
|-|----------|
|1|WPEFramework process should be up and running in the device.|
|2|DeviceInfo plugin should be available in the device build.|
|3|`MAX_RESPONSE_TIME_THRESHOLD` must be configured in device config.|
|4|Device should be rebooted before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config.|

<a name="head.TestSteps"></a>
## Test Steps

|#|StepName | Step Description| Expected Result|
|-|---------|-----------------|----------------|
| 1 | Reboot Pre-requisite | Reboot the device before test execution if `pre_req_reboot_pvs` is configured as `Yes` in device config, using `Controller.1.harakiri`. | Device reboots and comes back online. |
| 2 | Record Request Start Time | Record UTC timestamp before sending the device info request. | Start time recorded. |
| 3 | Query Device Information | Query device details via DeviceInfo API: <br>`{"jsonrpc":"2.0","id":1234567890,"method":"DeviceInfo.1.systeminfo"}` | Device information returned. |
| 4 | Record Response Time | Record UTC timestamp after receiving the response. | Response time recorded. |
| 5 | Calculate Max Response Time | Calculate: max response time = response timestamp - request timestamp. Repeat multiple times and take the maximum. | Response times calculated. |
| 6 | Validate Response Time | Compare maximum response time against `MAX_RESPONSE_TIME_THRESHOLD`. | Maximum device response time is within the expected threshold. |

<a name="head.Attributes"></a>
## Test Attributes

**Supported Models** : RPI-Client, Video Accelerator

**Estimated duration** : 10

**Priority** : High

**Release Version** : M116<div align="right"><sup>[Go To Top](#head.TOC)</sup></div>
